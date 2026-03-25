"""
Base classes for data source adapters.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator, Dict, Any, Optional, List
from datetime import datetime


@dataclass
class Grant:
    """Standardized grant representation across all data sources."""
    id: str
    title: str
    abstract: str = ""
    amount: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    institution: str = ""
    state: str = ""
    pi_name: str = ""
    program: str = ""

    # Source-specific metadata (preserved for downstream use)
    source_type: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Classification results (populated during classification)
    category: Optional[str] = None
    subtype: Optional[str] = None
    confidence: float = 0.0
    keyword_hits: Dict[str, List[str]] = field(default_factory=dict)
    classification_method: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'abstract': self.abstract[:1000] if self.abstract else "",
            'amount': self.amount,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'institution': self.institution,
            'state': self.state,
            'pi_name': self.pi_name,
            'program': self.program,
            'source_type': self.source_type,
            'category': self.category,
            'subtype': self.subtype,
            'confidence': self.confidence,
            'keyword_hits': self.keyword_hits,
            'classification_method': self.classification_method,
            'metadata': self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Grant':
        """Create from dictionary."""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            abstract=data.get('abstract', ''),
            amount=float(data.get('amount', 0)),
            start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
            institution=data.get('institution', ''),
            state=data.get('state', ''),
            pi_name=data.get('pi_name', ''),
            program=data.get('program', ''),
            source_type=data.get('source_type', ''),
            metadata=data.get('metadata', {}),
            category=data.get('category'),
            subtype=data.get('subtype'),
            confidence=float(data.get('confidence', 0)),
            keyword_hits=data.get('keyword_hits', {}),
            classification_method=data.get('classification_method', ''),
        )


class DataSource(ABC):
    """Abstract base class for all data source adapters."""

    def __init__(self, config: dict):
        """
        Initialize with source-specific configuration.

        Args:
            config: Source configuration from workflow YAML
        """
        self.config = config
        self.field_mapping = config.get('field_mapping', {})

    @abstractmethod
    def fetch(self) -> Iterator[Grant]:
        """
        Fetch grants from the data source.

        Yields:
            Grant objects in standardized format
        """
        pass

    @abstractmethod
    def get_total_count(self) -> Optional[int]:
        """
        Get total count of grants available (if known).

        Returns:
            Total count or None if unknown
        """
        pass

    def map_fields(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map source-specific fields to standard field names.

        Args:
            raw_data: Raw data from source with original field names

        Returns:
            Dictionary with standardized field names
        """
        mapped = {}
        for standard_name, source_name in self.field_mapping.items():
            if source_name in raw_data:
                mapped[standard_name] = raw_data[source_name]
        return mapped

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats to datetime."""
        if not date_str:
            return None

        formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%Y-%m-%dT%H:%M:%S',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return None
