"""
Grants.gov API data source adapter.

Grants.gov lists federal grant opportunities (forecasts and current).
Note: This is for opportunity listings, not awarded grants.

API: https://www.grants.gov/web/grants/search-grants.html (REST API)
"""

import requests
import time
from typing import Iterator, Optional, Dict, Any, List
from datetime import datetime
from .base import DataSource, Grant


class GrantsGovSource(DataSource):
    """
    Fetch grant opportunities from Grants.gov.

    Note: Grants.gov lists opportunities, not awards. Use this to find
    active funding opportunities, not historical grant data.

    API endpoint: https://www.grants.gov/grantsws/rest/opportunities/search
    """

    BASE_URL = "https://www.grants.gov/grantsws/rest/opportunities/search"

    def __init__(self, config: dict):
        super().__init__(config)

        gg_config = config.get('grants_gov', {})

        # Search filters
        self.keywords = gg_config.get('keywords', [])
        self.agencies = gg_config.get('agencies', [])  # e.g., ["EPA", "NSF"]
        self.opportunity_status = gg_config.get('status', 'posted')  # posted, forecasted, closed
        self.funding_instrument = gg_config.get('funding_instrument', 'G')  # G=Grant, CA=Cooperative Agreement

        self.rate_limit_ms = gg_config.get('rate_limit_ms', 500)
        self.page_size = gg_config.get('page_size', 25)

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Fetch grant opportunities matching criteria."""

        start_record = 0

        while True:
            payload = self._build_payload(start_record)

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
                print(f"  Error fetching Grants.gov data (offset {start_record}): {e}")
                break

            # Parse response
            opp_search = data.get('oppHits', [])
            if not opp_search:
                break

            # Update total
            if self._total_count is None:
                self._total_count = data.get('totalHits', 0)

            for opp in opp_search:
                yield self._parse_opportunity(opp)

            # Check if done
            start_record += len(opp_search)
            if start_record >= self._total_count:
                break

            time.sleep(self.rate_limit_ms / 1000)

    def _build_payload(self, start_record: int) -> Dict[str, Any]:
        """Build search payload."""
        payload = {
            "startRecordNum": start_record,
            "rows": self.page_size,
            "sortBy": "openDate|desc",
        }

        if self.keywords:
            payload["keyword"] = " ".join(self.keywords)

        if self.agencies:
            payload["agency"] = self.agencies

        if self.opportunity_status:
            payload["oppStatuses"] = self.opportunity_status

        if self.funding_instrument:
            payload["fundingInstruments"] = self.funding_instrument

        return payload

    def _parse_opportunity(self, opp: Dict[str, Any]) -> Grant:
        """Parse Grants.gov opportunity into Grant format."""

        return Grant(
            id=opp.get('id', ''),
            title=opp.get('title', ''),
            abstract=opp.get('synopsis', {}).get('synopsisDesc', ''),
            amount=float(opp.get('awardCeiling', 0) or 0),  # Max award amount
            start_date=self.parse_date(opp.get('openDate')),
            end_date=self.parse_date(opp.get('closeDate')),
            institution='',  # Opportunities don't have recipients
            state='',
            pi_name='',
            program=opp.get('cfdaNumber', ''),
            source_type='grants_gov',
            metadata={
                'agency': opp.get('agency', ''),
                'opportunity_number': opp.get('number', ''),
                'opportunity_status': opp.get('oppStatus', ''),
                'funding_instrument': opp.get('fundingInstrument', ''),
                'award_floor': opp.get('awardFloor', 0),
                'estimated_funding': opp.get('estimatedFunding', 0),
                'is_forecast': opp.get('oppStatus') == 'forecasted',
            }
        )

    def get_total_count(self) -> Optional[int]:
        return self._total_count
