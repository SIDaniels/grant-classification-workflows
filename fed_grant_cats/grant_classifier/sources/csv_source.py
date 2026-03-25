"""
CSV file data source adapter.

Allows loading grants from any CSV file with configurable column mapping.
"""

import csv
from pathlib import Path
from typing import Iterator, Optional, Dict, Any
from .base import DataSource, Grant


class CSVSource(DataSource):
    """
    Load grants from a CSV file.

    Supports flexible column mapping for different CSV formats.
    """

    def __init__(self, config: dict):
        super().__init__(config)

        csv_config = config.get('csv', {})

        self.path = Path(csv_config.get('path', ''))

        # Column name mappings (CSV column -> standard field)
        self.id_col = csv_config.get('id_column', 'id')
        self.title_col = csv_config.get('title_column', 'title')
        self.abstract_col = csv_config.get('abstract_column', 'abstract')
        self.amount_col = csv_config.get('amount_column', 'amount')
        self.start_date_col = csv_config.get('start_date_column', 'start_date')
        self.end_date_col = csv_config.get('end_date_column', 'end_date')
        self.institution_col = csv_config.get('institution_column', 'institution')
        self.state_col = csv_config.get('state_column', 'state')
        self.pi_col = csv_config.get('pi_column', 'pi_name')
        self.program_col = csv_config.get('program_column', 'program')

        # Additional metadata columns to preserve
        self.metadata_cols = csv_config.get('metadata_columns', [])

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Read grants from CSV file."""

        if not self.path or not self.path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.path}")

        with open(self.path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)

            count = 0
            for row in reader:
                yield self._parse_row(row)
                count += 1

            self._total_count = count

    def _parse_row(self, row: Dict[str, str]) -> Grant:
        """Parse a CSV row into a standardized Grant."""

        # Safely get values with fallback
        def get(col, default=''):
            return row.get(col, default) or default

        # Parse amount
        amount_str = get(self.amount_col, '0')
        try:
            # Handle currency formatting ($1,234.56)
            amount = float(amount_str.replace('$', '').replace(',', ''))
        except ValueError:
            amount = 0.0

        # Collect metadata
        metadata = {}
        for col in self.metadata_cols:
            if col in row:
                metadata[col] = row[col]

        return Grant(
            id=get(self.id_col),
            title=get(self.title_col),
            abstract=get(self.abstract_col),
            amount=amount,
            start_date=self.parse_date(get(self.start_date_col)),
            end_date=self.parse_date(get(self.end_date_col)),
            institution=get(self.institution_col),
            state=get(self.state_col),
            pi_name=get(self.pi_col),
            program=get(self.program_col),
            source_type='csv',
            metadata=metadata,
        )

    def get_total_count(self) -> Optional[int]:
        return self._total_count


class JSONSource(DataSource):
    """
    Load grants from a JSON file.

    Expects an array of grant objects or a dict with a 'grants' key.
    """

    def __init__(self, config: dict):
        super().__init__(config)

        json_config = config.get('json', {})
        self.path = Path(json_config.get('path', ''))
        self.grants_key = json_config.get('grants_key', None)  # Key containing grants array

        self._total_count = None

    def fetch(self) -> Iterator[Grant]:
        """Read grants from JSON file."""
        import json as json_lib

        if not self.path or not self.path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.path}")

        with open(self.path, 'r', encoding='utf-8') as f:
            data = json_lib.load(f)

        # Handle dict with grants key vs direct array
        if isinstance(data, dict) and self.grants_key:
            grants = data.get(self.grants_key, [])
        elif isinstance(data, list):
            grants = data
        else:
            grants = data.get('grants', data.get('results', []))

        self._total_count = len(grants)

        for raw in grants:
            yield Grant.from_dict(raw)

    def get_total_count(self) -> Optional[int]:
        return self._total_count
