"""
Data source adapters for fetching grants from various APIs and file formats.

Supported sources:
  - U.S. Federal:
    - nsf: NSF Awards API
    - nih_reporter: NIH RePORTER API
    - usaspending: USAspending.gov (EPA, DOE, USDA, etc.)
    - grants_gov: Grants.gov (opportunity listings)

  - International:
    - horizon_europe: EU Horizon Europe (CORDIS)
    - ukri: UK Research and Innovation
    - arc: Australian Research Council

  - Foundations:
    - gates: Gates Foundation
    - wellcome: Wellcome Trust

  - Academic/Literature:
    - openalex: OpenAlex (papers + funding)
    - pubmed: PubMed grants

  - File-based:
    - csv: Any CSV file
    - json: Any JSON file
"""

from .base import DataSource, Grant
from .nsf import NSFSource
from .nih_reporter import NIHReporterSource
from .usaspending import USAspendingSource
from .csv_source import CSVSource, JSONSource

# Lazy imports for optional sources (avoid import errors if deps missing)
def _get_grants_gov():
    from .grants_gov import GrantsGovSource
    return GrantsGovSource

def _get_openalex():
    from .openalex import OpenAlexSource
    return OpenAlexSource

def _get_horizon_europe():
    from .international import HorizonEuropeSource
    return HorizonEuropeSource

def _get_ukri():
    from .international import UKRISource
    return UKRISource


# Registry of available sources
SOURCES = {
    # U.S. Federal
    'nsf': NSFSource,
    'nih_reporter': NIHReporterSource,
    'usaspending': USAspendingSource,

    # File-based
    'csv': CSVSource,
    'json': JSONSource,
}

# Sources that require lazy loading (optional dependencies)
LAZY_SOURCES = {
    'grants_gov': _get_grants_gov,
    'openalex': _get_openalex,
    'horizon_europe': _get_horizon_europe,
    'ukri': _get_ukri,
}


def get_source(source_type: str, config: dict) -> DataSource:
    """Factory function to create a data source from config."""
    if source_type in SOURCES:
        return SOURCES[source_type](config)
    elif source_type in LAZY_SOURCES:
        try:
            source_class = LAZY_SOURCES[source_type]()
            return source_class(config)
        except ImportError as e:
            raise ImportError(
                f"Source '{source_type}' requires additional dependencies. "
                f"Install them with: pip install grant-classifier[{source_type}]"
            ) from e
    else:
        all_sources = list(SOURCES.keys()) + list(LAZY_SOURCES.keys())
        raise ValueError(f"Unknown source type: {source_type}. Available: {all_sources}")


def list_sources() -> dict:
    """List all available sources with their status."""
    result = {}
    for name in SOURCES:
        result[name] = {'available': True, 'type': 'core'}

    for name, loader in LAZY_SOURCES.items():
        try:
            loader()
            result[name] = {'available': True, 'type': 'optional'}
        except ImportError:
            result[name] = {'available': False, 'type': 'optional'}

    return result


__all__ = ['DataSource', 'Grant', 'get_source', 'list_sources', 'SOURCES']
