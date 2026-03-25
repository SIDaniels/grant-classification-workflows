"""
Classifier modules for categorizing grants.

Available classifiers:
  - keyword: Fast keyword-based classification
  - llm: LLM-powered classification (Claude)
  - hybrid: Combined keyword + LLM with confidence routing
  - crosswalk: Stage-based crosswalk analysis
"""

from .keyword import KeywordClassifier
from .crosswalk import CrosswalkAnalyzer, CrosswalkConfig, get_crosswalk

# Registry of classifiers
CLASSIFIERS = {
    'keyword': KeywordClassifier,
}

# Lazy imports for optional classifiers
def _get_llm_classifier():
    from .llm import LLMClassifier
    return LLMClassifier

def _get_hybrid_classifier():
    from .hybrid import HybridClassifier
    return HybridClassifier


LAZY_CLASSIFIERS = {
    'llm': _get_llm_classifier,
    'hybrid': _get_hybrid_classifier,
}


def get_classifier(classifier_type: str, config: dict):
    """Factory function to create a classifier from config."""
    if classifier_type in CLASSIFIERS:
        return CLASSIFIERS[classifier_type](config)
    elif classifier_type in LAZY_CLASSIFIERS:
        try:
            classifier_class = LAZY_CLASSIFIERS[classifier_type]()
            return classifier_class(config)
        except ImportError as e:
            raise ImportError(
                f"Classifier '{classifier_type}' requires additional dependencies. "
                f"Install them with: pip install grant-classifier[{classifier_type}]"
            ) from e
    else:
        all_classifiers = list(CLASSIFIERS.keys()) + list(LAZY_CLASSIFIERS.keys())
        raise ValueError(f"Unknown classifier: {classifier_type}. Available: {all_classifiers}")


__all__ = [
    'KeywordClassifier',
    'CrosswalkAnalyzer',
    'CrosswalkConfig',
    'get_crosswalk',
    'get_classifier',
]
