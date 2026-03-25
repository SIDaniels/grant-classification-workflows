"""
Grant Classifier - A generalizable framework for classifying research grants.

Features:
- Multi-source data adapters (NSF, NIH, EPA, international, CSV/JSON)
- Modular classification (keyword, LLM, hybrid with human review)
- Crosswalk gap analysis for identifying underfunded research connections
- CLI for batch processing and pipeline execution

Quick start:
    from grant_classifier.sources import get_source
    from grant_classifier.classifiers import KeywordClassifier

    # Fetch grants
    source = get_source('nsf', {'keywords': ['environmental health']})
    grants = list(source.fetch())

    # Classify
    classifier = KeywordClassifier({'categories': [...]})
    results = classifier.classify_batch(grants)
"""

__version__ = '0.1.0'

from .sources import get_source, list_sources, DataSource, Grant
from .classifiers import KeywordClassifier, CrosswalkAnalyzer, get_classifier

__all__ = [
    'get_source',
    'list_sources',
    'DataSource',
    'Grant',
    'KeywordClassifier',
    'CrosswalkAnalyzer',
    'get_classifier',
]
