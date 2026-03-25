"""
OpenAlex API data source adapter.

OpenAlex is an open catalog of scholarly papers, authors, institutions, and funders.
Can be used to find funding acknowledgments in papers.

API: https://docs.openalex.org/
"""

import requests
import time
from typing import Iterator, Optional, Dict, Any, List
from datetime import datetime
from .base import DataSource, Grant


class OpenAlexSource(DataSource):
    """
    Fetch funding information from OpenAlex.

    OpenAlex tracks funding acknowledgments in academic papers.
    Use this to find what research has been funded, extracted from publications.

    API endpoint: https://api.openalex.org/
    """

    BASE_URL = "https://api.openalex.org"

    def __init__(self, config: dict):
        super().__init__(config)

        oa_config = config.get('openalex', {})

        # Can search by funder, concept, institution
        self.funder_ids = oa_config.get('funder_ids', [])  # e.g., ["https://openalex.org/F4320332161"] (NIH)
        self.concepts = oa_config.get('concepts', [])  # e.g., ["environmental health", "toxicology"]
        self.from_year = oa_config.get('from_year', 2020)
        self.to_year = oa_config.get('to_year', 2025)

        # Email for polite pool (faster rate limits)
        self.email = oa_config.get('email', None)

        self.rate_limit_ms = oa_config.get('rate_limit_ms', 100)
        self.page_size = oa_config.get('page_size', 100)

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch grants/funding from OpenAlex works."""

        cursor = '*'

        while cursor:
            url = self._build_url(cursor)

            try:
                resp = requests.get(url, timeout=60)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"  Error fetching OpenAlex data: {e}")
                break

            results = data.get('results', [])
            if not results:
                break

            # Update total
            if self._total_count is None:
                self._total_count = data.get('meta', {}).get('count', 0)

            for work in results:
                # Extract grants from this work
                for grant in self._extract_grants(work):
                    yield grant

            # Get next cursor
            cursor = data.get('meta', {}).get('next_cursor')

            time.sleep(self.rate_limit_ms / 1000)

    def _build_url(self, cursor: str) -> str:
        """Build API URL with filters."""

        filters = []

        if self.funder_ids:
            filters.append(f"grants.funder:{','.join(self.funder_ids)}")

        if self.concepts:
            # Search in concepts
            concept_filter = '|'.join(self.concepts)
            filters.append(f"concepts.display_name.search:{concept_filter}")

        filters.append(f"publication_year:{self.from_year}-{self.to_year}")
        filters.append("grants.funder:!")  # Must have grants

        filter_str = ','.join(filters)

        url = f"{self.BASE_URL}/works?filter={filter_str}&per-page={self.page_size}&cursor={cursor}"

        if self.email:
            url += f"&mailto={self.email}"

        return url

    def _extract_grants(self, work: Dict[str, Any]) -> Iterator[Grant]:
        """Extract grant records from a work."""

        grants_data = work.get('grants', [])

        for g in grants_data:
            funder = g.get('funder_display_name', '')
            award_id = g.get('award_id', '')

            # Create unique ID from funder + award
            grant_id = f"{funder}:{award_id}" if award_id else f"{funder}:{work.get('id', '')}"

            yield Grant(
                id=grant_id,
                title=work.get('title', ''),
                abstract=work.get('abstract', ''),
                amount=0.0,  # Not available from paper acknowledgments
                start_date=self.parse_date(str(work.get('publication_year', ''))),
                end_date=None,
                institution=work.get('authorships', [{}])[0].get('institutions', [{}])[0].get('display_name', ''),
                state='',
                pi_name=work.get('authorships', [{}])[0].get('author', {}).get('display_name', ''),
                program='',
                source_type='openalex',
                metadata={
                    'funder': funder,
                    'award_id': award_id,
                    'paper_doi': work.get('doi', ''),
                    'paper_id': work.get('id', ''),
                    'concepts': [c.get('display_name', '') for c in work.get('concepts', [])[:5]],
                }
            )

    def get_total_count(self) -> Optional[int]:
        return self._total_count


class PubMedSource(DataSource):
    """
    Extract funding from PubMed papers.

    Uses PubMed E-utilities to search papers and extract grant information
    from the <Grant> elements in the XML.
    """

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, config: dict):
        super().__init__(config)

        pm_config = config.get('pubmed', {})

        self.search_terms = pm_config.get('search_terms', [])
        self.from_date = pm_config.get('from_date', '2020/01/01')
        self.to_date = pm_config.get('to_date', '2025/12/31')

        # API key for higher rate limits
        self.api_key = pm_config.get('api_key', None)

        self.rate_limit_ms = pm_config.get('rate_limit_ms', 334)  # 3/sec without key
        self.batch_size = pm_config.get('batch_size', 100)

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch grants mentioned in PubMed papers."""

        # First, search for PMIDs
        pmids = self._search_pmids()
        self._total_count = len(pmids)

        # Fetch in batches
        for i in range(0, len(pmids), self.batch_size):
            batch = pmids[i:i + self.batch_size]

            for grant in self._fetch_grants_for_pmids(batch):
                yield grant

            time.sleep(self.rate_limit_ms / 1000)

    def _search_pmids(self) -> List[str]:
        """Search PubMed and return list of PMIDs."""
        import xml.etree.ElementTree as ET

        query = ' AND '.join(self.search_terms) if self.search_terms else '*'
        query += f" AND {self.from_date}:{self.to_date}[dp]"

        url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': 10000,
            'retmode': 'xml',
        }
        if self.api_key:
            params['api_key'] = self.api_key

        try:
            resp = requests.get(url, params=params, timeout=60)
            resp.raise_for_status()

            root = ET.fromstring(resp.content)
            return [id_elem.text for id_elem in root.findall('.//Id')]
        except Exception as e:
            print(f"  Error searching PubMed: {e}")
            return []

    def _fetch_grants_for_pmids(self, pmids: List[str]) -> Iterator[Grant]:
        """Fetch paper details and extract grant info."""
        import xml.etree.ElementTree as ET

        url = f"{self.BASE_URL}/efetch.fcgi"
        params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml',
        }
        if self.api_key:
            params['api_key'] = self.api_key

        try:
            resp = requests.get(url, params=params, timeout=120)
            resp.raise_for_status()

            root = ET.fromstring(resp.content)

            for article in root.findall('.//PubmedArticle'):
                # Extract grants
                grant_list = article.findall('.//Grant')
                if not grant_list:
                    continue

                # Get paper info
                title_elem = article.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else ''

                abstract_elem = article.find('.//AbstractText')
                abstract = abstract_elem.text if abstract_elem is not None else ''

                pmid_elem = article.find('.//PMID')
                pmid = pmid_elem.text if pmid_elem is not None else ''

                for grant_elem in grant_list:
                    grant_id = grant_elem.findtext('GrantID', '')
                    agency = grant_elem.findtext('Agency', '')
                    country = grant_elem.findtext('Country', '')

                    yield Grant(
                        id=f"{agency}:{grant_id}" if grant_id else f"PMID:{pmid}",
                        title=title,
                        abstract=abstract,
                        amount=0.0,
                        start_date=None,
                        end_date=None,
                        institution='',
                        state='',
                        pi_name='',
                        program=agency,
                        source_type='pubmed',
                        metadata={
                            'pmid': pmid,
                            'agency': agency,
                            'country': country,
                            'grant_id': grant_id,
                        }
                    )

        except Exception as e:
            print(f"  Error fetching PubMed details: {e}")

    def get_total_count(self) -> Optional[int]:
        return self._total_count
