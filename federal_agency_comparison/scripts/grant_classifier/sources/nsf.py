"""
NSF Awards API data source adapter.
"""

import requests
import time
from typing import Iterator, Optional, Dict, Any, List
from datetime import datetime
from .base import DataSource, Grant


class NSFSource(DataSource):
    """
    Fetch grants from NSF Awards Search API.

    API endpoint: https://api.nsf.gov/services/v1/awards.json

    Note: API has 10,000 result limit per query.
    We work around this by splitting queries by month.
    """

    BASE_URL = "https://api.nsf.gov/services/v1/awards.json"

    # Fields to request from NSF API
    DEFAULT_FIELDS = [
        "id", "title", "abstractText", "awardeeName", "awardeeCity",
        "awardeeStateCode", "estimatedTotalAmt", "fundsObligatedAmt",
        "startDate", "expDate", "fundProgramName", "primaryProgram",
        "pdPIName", "piEmail", "transType", "orgLongName", "divAbbr",
        "dirAbbr", "progEleCode", "cfdaNumber"
    ]

    def __init__(self, config: dict):
        super().__init__(config)

        nsf_config = config.get('nsf', {})
        date_range = nsf_config.get('date_range', {})

        self.start_date = date_range.get('start', '2022-01-01')
        self.end_date = date_range.get('end', '2025-12-31')
        self.rate_limit_ms = nsf_config.get('rate_limit_ms', 100)
        self.pagination_strategy = nsf_config.get('pagination_strategy', 'monthly')

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch all grants, splitting by month to avoid API limits."""

        # Parse date range
        start = datetime.strptime(self.start_date, '%Y-%m-%d')
        end = datetime.strptime(self.end_date, '%Y-%m-%d')

        # Generate month ranges
        current = start
        while current <= end:
            year = current.year
            month = current.month

            # Fetch this month
            for grant in self._fetch_month(year, month):
                yield grant

            # Move to next month
            if month == 12:
                current = datetime(year + 1, 1, 1)
            else:
                current = datetime(year, month + 1, 1)

    def _fetch_month(self, year: int, month: int) -> Iterator[Grant]:
        """Fetch all grants for a specific month."""

        # Calculate date range for this month
        date_start = f"{month:02d}/01/{year}"
        if month == 12:
            date_end = f"12/31/{year}"
        else:
            date_end = f"{month+1:02d}/01/{year}"

        offset = 0
        rpp = 25  # Results per page (NSF default max)

        while True:
            # Fetch page
            data = self._fetch_page(date_start, date_end, offset, rpp)
            if not data:
                break

            total = data['response']['metadata'].get('totalCount', 0)
            awards = data['response'].get('award', [])

            if not awards:
                break

            # Convert to Grant objects
            for raw in awards:
                yield self._parse_grant(raw)

            # Check if we've fetched all
            offset += rpp
            if offset >= min(total, 10000):  # API limit
                break

            # Rate limiting
            time.sleep(self.rate_limit_ms / 1000)

    def _fetch_page(self, date_start: str, date_end: str, offset: int, rpp: int) -> Optional[Dict]:
        """Fetch a single page of results."""

        params = {
            "dateStart": date_start,
            "dateEnd": date_end,
            "offset": offset,
            "rpp": rpp,
            "printFields": ",".join(self.DEFAULT_FIELDS)
        }

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"  Error fetching NSF data (offset {offset}): {e}")
            return None

    def _parse_grant(self, raw: Dict[str, Any]) -> Grant:
        """Parse raw NSF API response into standardized Grant."""

        # Handle list fields (NSF sometimes returns lists)
        def get_val(d, key, default=''):
            v = d.get(key, default)
            if isinstance(v, list):
                return '; '.join(str(x) for x in v)
            return v or default

        return Grant(
            id=get_val(raw, 'id'),
            title=get_val(raw, 'title'),
            abstract=get_val(raw, 'abstractText'),
            amount=float(get_val(raw, 'estimatedTotalAmt', 0) or 0),
            start_date=self.parse_date(get_val(raw, 'startDate')),
            end_date=self.parse_date(get_val(raw, 'expDate')),
            institution=get_val(raw, 'awardeeName'),
            state=get_val(raw, 'awardeeStateCode'),
            pi_name=get_val(raw, 'pdPIName'),
            program=get_val(raw, 'fundProgramName'),
            source_type='nsf',
            metadata={
                'directorate': get_val(raw, 'dirAbbr'),
                'division': get_val(raw, 'divAbbr'),
                'cfda_number': get_val(raw, 'cfdaNumber'),
                'transaction_type': get_val(raw, 'transType'),
            }
        )

    def get_total_count(self) -> Optional[int]:
        """Get total count (requires fetching first page of first month)."""
        return self._total_count
