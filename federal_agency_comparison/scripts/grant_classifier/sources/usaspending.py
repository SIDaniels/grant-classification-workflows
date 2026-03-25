"""
USAspending.gov API data source adapter.

Used primarily for EPA grants, but can fetch from any federal agency.
"""

import requests
import time
from typing import Iterator, Optional, Dict, Any, List
from datetime import datetime
from .base import DataSource, Grant


class USAspendingSource(DataSource):
    """
    Fetch grants from USAspending.gov API.

    API endpoint: https://api.usaspending.gov/api/v2/search/spending_by_award/

    Documentation: https://api.usaspending.gov/docs/endpoints
    """

    BASE_URL = "https://api.usaspending.gov/api/v2/search/spending_by_award/"

    # Award type codes for grants
    GRANT_AWARD_TYPES = ["02", "03", "04", "05"]  # Block grants, project grants, etc.

    def __init__(self, config: dict):
        super().__init__(config)

        usa_config = config.get('usaspending', {})

        self.agency_name = usa_config.get('agency', 'Environmental Protection Agency')
        self.start_date = usa_config.get('start_date', '2022-01-01')
        self.end_date = usa_config.get('end_date', '2025-12-31')
        self.rate_limit_ms = usa_config.get('rate_limit_ms', 200)
        self.page_size = usa_config.get('page_size', 100)

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch all grants from the specified agency."""

        page = 1

        while True:
            payload = self._build_payload(page)

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
                print(f"  Error fetching USAspending data (page {page}): {e}")
                break

            results = data.get('results', [])
            if not results:
                break

            # Store total count on first request
            if self._total_count is None:
                self._total_count = data.get('page_metadata', {}).get('total', 0)

            # Convert to Grant objects
            for raw in results:
                yield self._parse_grant(raw)

            # Check if we've fetched all
            if len(results) < self.page_size:
                break

            page += 1

            # Safety limit
            if page > 500:
                print("  Hit page safety limit (500)")
                break

            # Rate limiting
            time.sleep(self.rate_limit_ms / 1000)

    def _build_payload(self, page: int) -> Dict[str, Any]:
        """Build API request payload."""

        return {
            "filters": {
                "agencies": [{
                    "type": "awarding",
                    "tier": "toptier",
                    "name": self.agency_name
                }],
                "time_period": [{
                    "start_date": self.start_date,
                    "end_date": self.end_date
                }],
                "award_type_codes": self.GRANT_AWARD_TYPES
            },
            "fields": [
                "Award ID",
                "Recipient Name",
                "Award Amount",
                "Description",
                "Start Date",
                "End Date",
                "CFDA Number",
                "awarding_agency_name",
                "recipient_state_code",
                "prime_award_recipient_id"
            ],
            "limit": self.page_size,
            "page": page
        }

    def _parse_grant(self, raw: Dict[str, Any]) -> Grant:
        """Parse raw USAspending API response into standardized Grant."""

        return Grant(
            id=raw.get('Award ID', ''),
            title=raw.get('Description', '')[:200] if raw.get('Description') else '',  # Description as title
            abstract=raw.get('Description', ''),  # Full description as abstract
            amount=float(raw.get('Award Amount', 0) or 0),
            start_date=self.parse_date(raw.get('Start Date')),
            end_date=self.parse_date(raw.get('End Date')),
            institution=raw.get('Recipient Name', ''),
            state=raw.get('recipient_state_code', ''),
            pi_name='',  # Not available from USAspending
            program=raw.get('CFDA Number', ''),
            source_type='usaspending',
            metadata={
                'agency': raw.get('awarding_agency_name', ''),
                'cfda_number': raw.get('CFDA Number', ''),
                'recipient_id': raw.get('prime_award_recipient_id', ''),
            }
        )

    def get_total_count(self) -> Optional[int]:
        return self._total_count
