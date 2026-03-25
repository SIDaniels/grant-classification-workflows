"""
Hybrid classifier combining keyword and LLM approaches.

Strategy:
1. First pass: Fast keyword classification
2. Route high-confidence results to output
3. Route low-confidence/ambiguous to LLM for refinement
4. Flag edge cases for human review

This balances accuracy with cost/speed.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from collections import defaultdict

from .keyword import KeywordClassifier, ClassificationResult
from .llm import LLMClassifier, LLMClassificationResult


@dataclass
class HybridResult:
    """Result from hybrid classification."""
    grant_id: str
    primary_category: str
    confidence: float
    method_used: str  # 'keyword', 'llm', or 'human_review'

    # From keyword classifier
    keyword_category: Optional[str] = None
    keyword_confidence: Optional[float] = None

    # From LLM classifier (if used)
    llm_category: Optional[str] = None
    llm_confidence: Optional[float] = None
    llm_reasoning: Optional[str] = None

    # Human review
    needs_human_review: bool = False
    review_reason: Optional[str] = None
    human_category: Optional[str] = None

    # Additional metadata
    entities: List[str] = field(default_factory=list)


class HybridClassifier:
    """
    Two-stage classifier: keyword first, LLM for uncertain cases.

    Configuration:
    - keyword_confidence_threshold: Above this, trust keyword result (default: 0.7)
    - llm_confidence_threshold: Below this, flag for human review (default: 0.6)
    - use_llm: Whether to use LLM at all (can disable for cost savings)
    - max_llm_fraction: Maximum fraction of grants to send to LLM (default: 0.3)
    """

    def __init__(self, config: dict):
        """
        Initialize hybrid classifier.

        Expected config:
        {
            'keyword': { ... keyword classifier config ... },
            'llm': { ... llm classifier config ... },
            'keyword_confidence_threshold': 0.7,
            'llm_confidence_threshold': 0.6,
            'use_llm': True,
            'max_llm_fraction': 0.3,
        }
        """
        self.config = config

        # Initialize keyword classifier
        keyword_config = config.get('keyword', {})
        if 'categories' not in keyword_config and 'categories' in config:
            keyword_config['categories'] = config['categories']
        self.keyword_classifier = KeywordClassifier(keyword_config)

        # Initialize LLM classifier (lazy)
        self.llm_classifier = None
        self.use_llm = config.get('use_llm', True)

        # Thresholds
        self.keyword_threshold = config.get('keyword_confidence_threshold', 0.7)
        self.llm_threshold = config.get('llm_confidence_threshold', 0.6)
        self.max_llm_fraction = config.get('max_llm_fraction', 0.3)

    def _get_llm_classifier(self) -> LLMClassifier:
        """Lazy initialization of LLM classifier."""
        if self.llm_classifier is None:
            llm_config = self.config.get('llm', {})
            if 'categories' not in llm_config and 'categories' in self.config:
                llm_config['categories'] = self.config['categories']
            self.llm_classifier = LLMClassifier(llm_config)
        return self.llm_classifier

    def classify(self, grant_id: str, title: str, abstract: str) -> HybridResult:
        """
        Classify a single grant using hybrid approach.
        """
        # Stage 1: Keyword classification
        kw_result = self.keyword_classifier.classify(grant_id, title, abstract)

        result = HybridResult(
            grant_id=grant_id,
            primary_category=kw_result.primary_category or 'UNKNOWN',
            confidence=kw_result.confidence,
            method_used='keyword',
            keyword_category=kw_result.primary_category,
            keyword_confidence=kw_result.confidence,
        )

        # High confidence keyword match: use it
        if kw_result.confidence >= self.keyword_threshold and not kw_result.needs_review:
            return result

        # Stage 2: LLM classification for uncertain cases
        if self.use_llm:
            try:
                llm_classifier = self._get_llm_classifier()
                llm_result = llm_classifier.classify(grant_id, title, abstract)

                result.llm_category = llm_result.primary_category
                result.llm_confidence = llm_result.confidence
                result.llm_reasoning = llm_result.reasoning
                result.entities = llm_result.entities_mentioned

                # Trust LLM if confidence is good
                if llm_result.confidence >= self.llm_threshold:
                    result.primary_category = llm_result.primary_category
                    result.confidence = llm_result.confidence
                    result.method_used = 'llm'
                else:
                    # LLM also uncertain: flag for human review
                    result.needs_human_review = True
                    result.review_reason = f"Both classifiers uncertain (kw={kw_result.confidence:.2f}, llm={llm_result.confidence:.2f})"
                    result.method_used = 'human_review'

            except Exception as e:
                # LLM failed, flag for review
                result.needs_human_review = True
                result.review_reason = f"LLM error: {str(e)}"
        else:
            # No LLM, flag uncertain cases for review
            if kw_result.confidence < self.keyword_threshold or kw_result.needs_review:
                result.needs_human_review = True
                result.review_reason = kw_result.review_reason or "Low keyword confidence"

        return result

    def classify_batch(
        self,
        grants: List[Dict[str, Any]],
        id_field: str = 'id',
        title_field: str = 'title',
        abstract_field: str = 'abstract',
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> List[HybridResult]:
        """
        Classify batch with intelligent LLM routing.

        First does keyword pass on all grants, then routes uncertain ones to LLM.
        Respects max_llm_fraction to control costs.
        """
        total = len(grants)
        results: Dict[str, HybridResult] = {}

        # Stage 1: Keyword classification for all
        if progress_callback:
            progress_callback(0, total, "Keyword classification")

        uncertain_grants = []

        for i, grant in enumerate(grants):
            grant_id = str(grant.get(id_field, f"grant_{i}"))
            title = grant.get(title_field, '')
            abstract = grant.get(abstract_field, '')

            kw_result = self.keyword_classifier.classify(grant_id, title, abstract)

            result = HybridResult(
                grant_id=grant_id,
                primary_category=kw_result.primary_category or 'UNKNOWN',
                confidence=kw_result.confidence,
                method_used='keyword',
                keyword_category=kw_result.primary_category,
                keyword_confidence=kw_result.confidence,
            )

            # Route uncertain cases for LLM
            if kw_result.confidence < self.keyword_threshold or kw_result.needs_review:
                uncertain_grants.append((grant, result))

            results[grant_id] = result

            if progress_callback and (i + 1) % 100 == 0:
                progress_callback(i + 1, total, "Keyword classification")

        # Stage 2: LLM for uncertain cases (respecting budget)
        if self.use_llm and uncertain_grants:
            max_llm = int(total * self.max_llm_fraction)
            llm_batch = uncertain_grants[:max_llm]
            remaining = uncertain_grants[max_llm:]

            if progress_callback:
                progress_callback(0, len(llm_batch), "LLM classification")

            try:
                llm_classifier = self._get_llm_classifier()

                for i, (grant, result) in enumerate(llm_batch):
                    grant_id = str(grant.get(id_field, ''))
                    title = grant.get(title_field, '')
                    abstract = grant.get(abstract_field, '')

                    llm_result = llm_classifier.classify(grant_id, title, abstract)

                    result.llm_category = llm_result.primary_category
                    result.llm_confidence = llm_result.confidence
                    result.llm_reasoning = llm_result.reasoning
                    result.entities = llm_result.entities_mentioned

                    if llm_result.confidence >= self.llm_threshold:
                        result.primary_category = llm_result.primary_category
                        result.confidence = llm_result.confidence
                        result.method_used = 'llm'
                    else:
                        result.needs_human_review = True
                        result.review_reason = "Both classifiers uncertain"
                        result.method_used = 'human_review'

                    if progress_callback and (i + 1) % 10 == 0:
                        progress_callback(i + 1, len(llm_batch), "LLM classification")

            except Exception as e:
                # Mark all LLM batch for review on error
                for grant, result in llm_batch:
                    result.needs_human_review = True
                    result.review_reason = f"LLM error: {str(e)}"

            # Mark remaining (over budget) for review
            for grant, result in remaining:
                result.needs_human_review = True
                result.review_reason = "Over LLM budget, needs manual review"
        else:
            # No LLM: mark all uncertain for review
            for grant, result in uncertain_grants:
                result.needs_human_review = True
                result.review_reason = "LLM disabled, needs manual review"

        # Return in original order
        return [results[str(g.get(id_field, f"grant_{i}"))] for i, g in enumerate(grants)]

    def apply_human_review(self, result: HybridResult, category: str) -> HybridResult:
        """Apply human review decision to a result."""
        result.human_category = category
        result.primary_category = category
        result.confidence = 1.0  # Human review is authoritative
        result.method_used = 'human_review'
        result.needs_human_review = False
        return result

    def summary(self, results: List[HybridResult]) -> Dict[str, Any]:
        """Generate summary statistics."""
        total = len(results)
        if total == 0:
            return {'total': 0}

        by_category = defaultdict(int)
        by_method = defaultdict(int)
        needs_review = 0
        confidence_sum = 0.0

        for r in results:
            by_category[r.primary_category] += 1
            by_method[r.method_used] += 1
            if r.needs_human_review:
                needs_review += 1
            confidence_sum += r.confidence

        return {
            'total': total,
            'by_category': dict(by_category),
            'by_method': dict(by_method),
            'needs_human_review': needs_review,
            'needs_review_pct': needs_review / total * 100,
            'avg_confidence': confidence_sum / total,
            'keyword_only': by_method.get('keyword', 0),
            'llm_used': by_method.get('llm', 0),
            'llm_usage_pct': by_method.get('llm', 0) / total * 100 if total > 0 else 0,
        }

    def export_for_review(self, results: List[HybridResult]) -> List[Dict[str, Any]]:
        """Export items needing human review in a format suitable for review UI/spreadsheet."""
        review_items = []

        for r in results:
            if r.needs_human_review:
                review_items.append({
                    'grant_id': r.grant_id,
                    'suggested_category': r.primary_category,
                    'keyword_category': r.keyword_category,
                    'keyword_confidence': r.keyword_confidence,
                    'llm_category': r.llm_category,
                    'llm_confidence': r.llm_confidence,
                    'llm_reasoning': r.llm_reasoning,
                    'review_reason': r.review_reason,
                    'entities': r.entities,
                    # Leave blank for human to fill
                    'human_category': '',
                    'notes': '',
                })

        return review_items
