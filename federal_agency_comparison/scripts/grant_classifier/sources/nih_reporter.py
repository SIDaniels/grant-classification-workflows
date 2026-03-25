"""
NIH RePORTER API data source adapter.
"""

import requests
import time
from typing import Iterator, Optional, Dict, Any
from datetime import datetime
from .base import DataSource, Grant


class NIHReporterSource(DataSource):
    """
    Fetch grants from NIH RePORTER API.

    API endpoint: https://api.reporter.nih.gov/v2/projects/search

    Documentation: https://api.reporter.nih.gov/
    """

    BASE_URL = "https://api.reporter.nih.gov/v2/projects/search"

    def __init__(self, config: dict):
        super().__init__(config)

        nih_config = config.get('nih_reporter', {})

        self.fiscal_years = nih_config.get('fiscal_years', [2024])
        self.include_active = nih_config.get('include_active', True)
        self.rate_limit_ms = nih_config.get('rate_limit_ms', 200)
        self.page_size = nih_config.get('page_size', 500)

        # Optional filters
        self.agencies = nih_config.get('agencies', None)  # e.g., ["NIEHS", "NCI"]
        self.keywords = nih_config.get('keywords', None)  # Pre-filter by keywords

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch all grants matching criteria."""

        offset = 0

        while True:
            # Build search criteria
            criteria = self._build_criteria()

            payload = {
                "criteria": criteria,
                "offset": offset,
                "limit": self.page_size,
                "sort_field": "project_start_date",
                "sort_order": "desc"
            }

            # Fetch page
            try:
                resp = requests.post(
                    self.BASE_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=60
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"  Error fetching NIH data (offset {offset}): {e}")
                break

            results = data.get('results', [])
            if not results:
                break

            # Store total count
            if self._total_count is None:
                self._total_count = data.get('meta', {}).get('total', 0)

            # Convert to Grant objects
            for raw in results:
                yield self._parse_grant(raw)

            # Check if we've fetched all
            offset += len(results)
            if offset >= self._total_count:
                break

            # Rate limiting
            time.sleep(self.rate_limit_ms / 1000)

    def _build_criteria(self) -> Dict[str, Any]:
        """Build search criteria for NIH API."""

        criteria = {
            "fiscal_years": self.fiscal_years,
            "include_active_projects": self.include_active,
        }

        if self.agencies:
            criteria["agencies"] = self.agencies

        if self.keywords:
            # Use advanced text search
            criteria["advanced_text_search"] = {
                "operator": "or",
                "search_field": "all",
                "search_text": " ".join(self.keywords)
            }

        return criteria

    def _parse_grant(self, raw: Dict[str, Any]) -> Grant:
        """Parse raw NIH API response into standardized Grant."""

        # Principal investigator info
        pi_profile = raw.get('principal_investigators', [{}])[0] if raw.get('principal_investigators') else {}
        pi_name = f"{pi_profile.get('first_name', '')} {pi_profile.get('last_name', '')}".strip()

        # Organization info
        org = raw.get('organization', {})

        # Project dates
        start_date = self.parse_date(raw.get('project_start_date'))
        end_date = self.parse_date(raw.get('project_end_date'))

        return Grant(
            id=raw.get('project_num', raw.get('appl_id', '')),
            title=raw.get('project_title', ''),
            abstract=raw.get('abstract_text', '') or raw.get('phr_text', ''),
            amount=float(raw.get('award_amount', 0) or 0),
            start_date=start_date,
            end_date=end_date,
            institution=org.get('org_name', ''),
            state=org.get('org_state', ''),
            pi_name=pi_name,
            program=raw.get('activity_code', ''),
            source_type='nih_reporter',
            metadata={
                'institute': raw.get('agency_ic_admin', {}).get('abbreviation', ''),
                'activity_code': raw.get('activity_code', ''),
                'funding_mechanism': raw.get('funding_mechanism', ''),
                'study_section': raw.get('study_section', {}).get('name', ''),
                'project_terms': raw.get('terms', ''),
                'is_active': raw.get('is_active', False),
            }
        )

    def get_total_count(self) -> Optional[int]:
        return self._total_count
