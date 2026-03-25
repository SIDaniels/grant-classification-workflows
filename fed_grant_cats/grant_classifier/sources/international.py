"""
International funding source adapters.

- Horizon Europe (EU) via CORDIS
- UKRI (UK Research and Innovation)
- ARC (Australian Research Council)
"""

import requests
import time
from typing import Iterator, Optional, Dict, Any, List
from datetime import datetime
from .base import DataSource, Grant


class HorizonEuropeSource(DataSource):
    """
    Fetch EU Horizon Europe grants from CORDIS.

    CORDIS (Community Research and Development Information Service)
    provides data on EU-funded research projects.

    API: https://cordis.europa.eu/data
    """

    # CORDIS OpenSearch API
    BASE_URL = "https://cordis.europa.eu/search/result_en"

    def __init__(self, config: dict):
        super().__init__(config)

        he_config = config.get('horizon_europe', {})

        self.keywords = he_config.get('keywords', [])
        self.programme = he_config.get('programme', 'HORIZON')  # HORIZON, H2020, FP7
        self.from_year = he_config.get('from_year', 2021)
        self.to_year = he_config.get('to_year', 2027)

        self.rate_limit_ms = he_config.get('rate_limit_ms', 500)
        self.page_size = he_config.get('page_size', 25)

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch Horizon Europe projects from CORDIS."""

        page = 1

        while True:
            params = self._build_params(page)

            try:
                resp = requests.get(self.BASE_URL, params=params, timeout=60)
                resp.raise_for_status()

                # CORDIS returns HTML with embedded JSON or XML
                # For simplicity, we'll parse the JSON API endpoint
                data = self._parse_response(resp.text)

            except Exception as e:
                print(f"  Error fetching CORDIS data (page {page}): {e}")
                break

            if not data:
                break

            for project in data:
                yield self._parse_project(project)

            page += 1

            if self._total_count and (page * self.page_size) >= self._total_count:
                break

            time.sleep(self.rate_limit_ms / 1000)

    def _build_params(self, page: int) -> Dict[str, Any]:
        """Build search parameters."""
        return {
            'q': ' '.join(self.keywords) if self.keywords else '*',
            'p': page,
            'num': self.page_size,
            'srt': 'relevance',
            'format': 'json',
            'type': 'project',
            'programme': self.programme,
        }

    def _parse_response(self, html: str) -> List[Dict]:
        """Parse CORDIS response (placeholder - actual implementation depends on API format)."""
        # Note: CORDIS API format may vary; this is a simplified placeholder
        # Real implementation would parse the actual response format
        try:
            import json
            # Try to extract JSON from response
            return json.loads(html).get('results', [])
        except:
            return []

    def _parse_project(self, project: Dict[str, Any]) -> Grant:
        """Parse CORDIS project into Grant format."""

        return Grant(
            id=project.get('rcn', project.get('id', '')),
            title=project.get('title', ''),
            abstract=project.get('objective', ''),
            amount=float(project.get('totalCost', 0) or 0),
            start_date=self.parse_date(project.get('startDate')),
            end_date=self.parse_date(project.get('endDate')),
            institution=project.get('coordinator', {}).get('name', ''),
            state=project.get('coordinator', {}).get('country', ''),
            pi_name='',
            program=project.get('programme', ''),
            source_type='horizon_europe',
            metadata={
                'rcn': project.get('rcn', ''),
                'acronym': project.get('acronym', ''),
                'programme': project.get('programme', ''),
                'funding_scheme': project.get('fundingScheme', ''),
                'ec_contribution': project.get('ecContribution', 0),
                'status': project.get('status', ''),
            }
        )

    def get_total_count(self) -> Optional[int]:
        return self._total_count


class UKRISource(DataSource):
    """
    Fetch UK Research and Innovation (UKRI) grants.

    UKRI encompasses:
    - AHRC (Arts and Humanities)
    - BBSRC (Biotechnology and Biological Sciences)
    - EPSRC (Engineering and Physical Sciences)
    - ESRC (Economic and Social)
    - MRC (Medical)
    - NERC (Natural Environment)
    - STFC (Science and Technology Facilities)
    - Innovate UK
    - Research England

    API: https://gtr.ukri.org/resources/GtR-2-API-v1.7.5.pdf
    """

    BASE_URL = "https://gtr.ukri.org/gtr/api"

    def __init__(self, config: dict):
        super().__init__(config)

        ukri_config = config.get('ukri', {})

        self.keywords = ukri_config.get('keywords', [])
        self.funders = ukri_config.get('funders', [])  # e.g., ["NERC", "MRC"]
        self.from_year = ukri_config.get('from_year', 2020)

        self.rate_limit_ms = ukri_config.get('rate_limit_ms', 200)
        self.page_size = ukri_config.get('page_size', 100)

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch UKRI projects."""

        page = 1

        while True:
            url = f"{self.BASE_URL}/projects"
            params = {
                'p': page,
                's': self.page_size,
            }

            # Add keyword search
            if self.keywords:
                params['q'] = ' '.join(self.keywords)

            # Add funder filter
            if self.funders:
                params['f.fu.org.n'] = '|'.join(self.funders)

            try:
                resp = requests.get(
                    url,
                    params=params,
                    headers={'Accept': 'application/json'},
                    timeout=60
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"  Error fetching UKRI data (page {page}): {e}")
                break

            projects = data.get('project', [])
            if not projects:
                break

            # Update total
            if self._total_count is None:
                self._total_count = data.get('totalSize', 0)

            for project in projects:
                yield self._parse_project(project)

            page += 1

            if page * self.page_size >= self._total_count:
                break

            time.sleep(self.rate_limit_ms / 1000)

    def _parse_project(self, project: Dict[str, Any]) -> Grant:
        """Parse UKRI project into Grant format."""

        # Extract funder
        fund = project.get('fund', {})
        funder = fund.get('funder', {}).get('name', '')

        # Extract lead organization
        participants = project.get('participantValues', {}).get('participant', [])
        lead_org = ''
        for p in participants:
            if p.get('role') == 'LEAD_ORG':
                lead_org = p.get('organisationName', '')
                break

        return Grant(
            id=project.get('id', ''),
            title=project.get('title', ''),
            abstract=project.get('abstractText', ''),
            amount=float(fund.get('valuePounds', 0) or 0),
            start_date=self.parse_date(project.get('identifiers', {}).get('start')),
            end_date=self.parse_date(project.get('identifiers', {}).get('end')),
            institution=lead_org,
            state='UK',
            pi_name='',
            program=funder,
            source_type='ukri',
            metadata={
                'funder': funder,
                'grant_category': project.get('grantCategory', ''),
                'status': project.get('status', ''),
                'research_topics': [t.get('text', '') for t in project.get('researchTopics', {}).get('researchTopic', [])],
            }
        )

    def get_total_count(self) -> Optional[int]:
        return self._total_count


class ARCSource(DataSource):
    """
    Fetch Australian Research Council grants.

    ARC provides funding through:
    - Discovery Projects
    - Linkage Projects
    - Future Fellowships
    - Centres of Excellence

    Data: https://dataportal.arc.gov.au/
    """

    BASE_URL = "https://dataportal.arc.gov.au/NCGP/API"

    def __init__(self, config: dict):
        super().__init__(config)

        arc_config = config.get('arc', {})

        self.keywords = arc_config.get('keywords', [])
        self.schemes = arc_config.get('schemes', [])  # e.g., ["DP", "LP", "FF"]
        self.from_year = arc_config.get('from_year', 2020)

        self.rate_limit_ms = arc_config.get('rate_limit_ms', 500)
        self.page_size = arc_config.get('page_size', 100)

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch ARC grants."""
        # Note: ARC data portal API format varies
        # This is a placeholder implementation

        url = f"{self.BASE_URL}/grants"
        params = {
            'limit': self.page_size,
            'offset': 0,
        }

        if self.keywords:
            params['keywords'] = ','.join(self.keywords)

        if self.schemes:
            params['scheme'] = ','.join(self.schemes)

        if self.from_year:
            params['from_year'] = self.from_year

        try:
            resp = requests.get(url, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            for grant in data.get('grants', []):
                yield self._parse_grant(grant)

        except Exception as e:
            print(f"  Error fetching ARC data: {e}")

    def _parse_grant(self, grant: Dict[str, Any]) -> Grant:
        """Parse ARC grant into Grant format."""

        return Grant(
            id=grant.get('project_id', ''),
            title=grant.get('title', ''),
            abstract=grant.get('summary', ''),
            amount=float(grant.get('funding_amount', 0) or 0),
            start_date=self.parse_date(grant.get('start_date')),
            end_date=self.parse_date(grant.get('end_date')),
            institution=grant.get('administering_organisation', ''),
            state=grant.get('state', ''),
            pi_name=grant.get('chief_investigator', ''),
            program=grant.get('scheme', ''),
            source_type='arc',
            metadata={
                'scheme': grant.get('scheme', ''),
                'for_codes': grant.get('for_codes', []),
                'seo_codes': grant.get('seo_codes', []),
            }
        )

    def get_total_count(self) -> Optional[int]:
        return self._total_count
