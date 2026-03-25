"""
Keyword-based grant classifier.

Fast, deterministic classification using keyword matching.
Suitable for high-volume processing and as a first-pass filter.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict
import re


@dataclass
class Category:
    """A classification category with keywords and rules."""
    name: str
    description: str = ""

    # Keywords that indicate this category
    keywords: List[str] = field(default_factory=list)

    # Patterns (regex) for more complex matching
    patterns: List[str] = field(default_factory=list)

    # Keywords in title are weighted higher
    title_weight: float = 2.0

    # Threshold score to assign this category
    threshold: float = 1.0

    # If true, presence of ANY keyword is sufficient
    any_match: bool = False

    # Subcategories (optional)
    subcategories: List['Category'] = field(default_factory=list)


@dataclass
class ClassificationResult:
    """Result of classifying a grant."""
    grant_id: str
    primary_category: Optional[str]
    confidence: float  # 0.0 to 1.0
    all_scores: Dict[str, float]
    matched_keywords: Dict[str, List[str]]
    subcategory: Optional[str] = None
    needs_review: bool = False
    review_reason: Optional[str] = None


class KeywordClassifier:
    """
    Classify grants using keyword matching.

    Features:
    - Configurable categories with keywords and patterns
    - Title vs abstract weighting
    - Confidence scoring
    - Subcategory support
    - Review flagging for ambiguous cases
    """

    def __init__(self, config: dict):
        """
        Initialize from config dict.

        Expected config structure:
        {
            'categories': [
                {
                    'name': 'category_name',
                    'description': 'what this category means',
                    'keywords': ['keyword1', 'keyword2'],
                    'patterns': ['regex1', 'regex2'],  # optional
                    'threshold': 1.0,  # optional
                    'subcategories': [...]  # optional
                },
                ...
            ],
            'review_threshold': 0.5,  # confidence below this flags for review
            'ambiguity_threshold': 0.2,  # if top two scores within this, flag
        }
        """
        self.categories: List[Category] = []
        self.review_threshold = config.get('review_threshold', 0.5)
        self.ambiguity_threshold = config.get('ambiguity_threshold', 0.2)

        # Parse categories from config
        for cat_config in config.get('categories', []):
            self.categories.append(self._parse_category(cat_config))

        # Pre-compile patterns
        self._compiled_patterns: Dict[str, List[re.Pattern]] = {}
        for cat in self.categories:
            if cat.patterns:
                self._compiled_patterns[cat.name] = [
                    re.compile(p, re.IGNORECASE) for p in cat.patterns
                ]

    def _parse_category(self, config: dict) -> Category:
        """Parse a category from config dict."""
        subcats = []
        for subcat_config in config.get('subcategories', []):
            subcats.append(self._parse_category(subcat_config))

        return Category(
            name=config['name'],
            description=config.get('description', ''),
            keywords=config.get('keywords', []),
            patterns=config.get('patterns', []),
            title_weight=config.get('title_weight', 2.0),
            threshold=config.get('threshold', 1.0),
            any_match=config.get('any_match', False),
            subcategories=subcats,
        )

    def classify(self, grant_id: str, title: str, abstract: str) -> ClassificationResult:
        """
        Classify a single grant.

        Returns ClassificationResult with category, confidence, and review flag.
        """
        title_lower = title.lower()
        abstract_lower = abstract.lower()
        full_text = f"{title_lower} {abstract_lower}"

        # Score each category
        scores: Dict[str, float] = {}
        matched: Dict[str, List[str]] = defaultdict(list)

        for category in self.categories:
            score, keywords = self._score_category(
                category, title_lower, abstract_lower, full_text
            )
            scores[category.name] = score
            if keywords:
                matched[category.name] = keywords

        # Determine primary category
        if not scores or max(scores.values()) == 0:
            return ClassificationResult(
                grant_id=grant_id,
                primary_category=None,
                confidence=0.0,
                all_scores=scores,
                matched_keywords=dict(matched),
                needs_review=True,
                review_reason="No category matched",
            )

        # Sort by score
        sorted_cats = sorted(scores.items(), key=lambda x: -x[1])
        top_cat, top_score = sorted_cats[0]

        # Calculate confidence (normalized score)
        max_possible = self._max_possible_score(
            next(c for c in self.categories if c.name == top_cat)
        )
        confidence = min(1.0, top_score / max_possible) if max_possible > 0 else 0.0

        # Check for ambiguity
        needs_review = False
        review_reason = None

        if confidence < self.review_threshold:
            needs_review = True
            review_reason = f"Low confidence ({confidence:.2f})"
        elif len(sorted_cats) > 1:
            second_score = sorted_cats[1][1]
            if top_score > 0 and (top_score - second_score) / top_score < self.ambiguity_threshold:
                needs_review = True
                review_reason = f"Ambiguous: {sorted_cats[0][0]} vs {sorted_cats[1][0]}"

        # Check subcategories
        subcategory = None
        top_category_obj = next(c for c in self.categories if c.name == top_cat)
        if top_category_obj.subcategories:
            subcategory = self._classify_subcategory(
                top_category_obj, title_lower, abstract_lower, full_text
            )

        return ClassificationResult(
            grant_id=grant_id,
            primary_category=top_cat,
            confidence=confidence,
            all_scores=scores,
            matched_keywords=dict(matched),
            subcategory=subcategory,
            needs_review=needs_review,
            review_reason=review_reason,
        )

    def _score_category(
        self,
        category: Category,
        title: str,
        abstract: str,
        full_text: str
    ) -> Tuple[float, List[str]]:
        """Score how well text matches a category."""
        score = 0.0
        matched_keywords = []

        # Keyword matching
        for keyword in category.keywords:
            kw_lower = keyword.lower()

            # Check title (weighted higher)
            if kw_lower in title:
                score += category.title_weight
                matched_keywords.append(f"{keyword} (title)")
            # Check abstract
            elif kw_lower in abstract:
                score += 1.0
                matched_keywords.append(keyword)

        # Pattern matching
        if category.name in self._compiled_patterns:
            for pattern in self._compiled_patterns[category.name]:
                if pattern.search(full_text):
                    score += 1.5
                    matched_keywords.append(f"pattern:{pattern.pattern}")

        # Apply threshold
        if category.any_match and matched_keywords:
            score = max(score, category.threshold)

        return score, matched_keywords

    def _max_possible_score(self, category: Category) -> float:
        """Calculate maximum possible score for a category."""
        # All keywords in title + all patterns
        return (
            len(category.keywords) * category.title_weight +
            len(category.patterns) * 1.5
        )

    def _classify_subcategory(
        self,
        parent: Category,
        title: str,
        abstract: str,
        full_text: str
    ) -> Optional[str]:
        """Classify into subcategory of parent."""
        best_subcat = None
        best_score = 0.0

        for subcat in parent.subcategories:
            score, _ = self._score_category(subcat, title, abstract, full_text)
            if score > best_score:
                best_score = score
                best_subcat = subcat.name

        return best_subcat

    def classify_batch(
        self,
        grants: List[Dict[str, Any]],
        id_field: str = 'id',
        title_field: str = 'title',
        abstract_field: str = 'abstract'
    ) -> List[ClassificationResult]:
        """
        Classify a batch of grants.

        Args:
            grants: List of grant dicts
            id_field: Key for grant ID
            title_field: Key for title
            abstract_field: Key for abstract

        Returns:
            List of ClassificationResult
        """
        results = []
        for grant in grants:
            result = self.classify(
                grant_id=str(grant.get(id_field, '')),
                title=grant.get(title_field, ''),
                abstract=grant.get(abstract_field, ''),
            )
            results.append(result)
        return results

    def summary(self, results: List[ClassificationResult]) -> Dict[str, Any]:
        """Generate summary statistics for classification results."""
        total = len(results)
        if total == 0:
            return {'total': 0}

        by_category = defaultdict(int)
        needs_review_count = 0
        confidence_sum = 0.0

        for r in results:
            if r.primary_category:
                by_category[r.primary_category] += 1
            else:
                by_category['unclassified'] += 1

            if r.needs_review:
                needs_review_count += 1

            confidence_sum += r.confidence

        return {
            'total': total,
            'by_category': dict(by_category),
            'needs_review': needs_review_count,
            'needs_review_pct': needs_review_count / total * 100,
            'avg_confidence': confidence_sum / total,
        }


# =============================================================================
# PRESET CLASSIFICATION SCHEMES
# =============================================================================

def get_environmental_health_categories() -> List[dict]:
    """
    Environmental health classification scheme.

    Based on the NIH/NSF environmental health grant analysis work.
    """
    return [
        {
            'name': 'ENV',
            'description': 'Environmental health research (exposure, toxicity, mechanism)',
            'keywords': [
                'environmental', 'exposure', 'pollutant', 'toxicant', 'contamination',
                'PFAS', 'phthalate', 'BPA', 'lead', 'mercury', 'arsenic', 'cadmium',
                'PM2.5', 'air pollution', 'pesticide', 'microplastic',
                'endocrine disrupt', 'neurotox', 'hepatotox', 'oxidative stress',
                'biomonitoring', 'environmental justice', 'health disparities',
            ],
            'threshold': 2.0,
            'subcategories': [
                {
                    'name': 'exposure',
                    'description': 'Research on chemical exposures and detection',
                    'keywords': ['exposure', 'biomonitoring', 'detection', 'contamination', 'measurement'],
                },
                {
                    'name': 'mechanism',
                    'description': 'Research on biological mechanisms of harm',
                    'keywords': ['mechanism', 'pathway', 'toxicity', 'disruption', 'damage'],
                },
                {
                    'name': 'intervention',
                    'description': 'Research on protective interventions',
                    'keywords': ['protection', 'prevention', 'treatment', 'intervention', 'therapy'],
                },
            ]
        },
        {
            'name': 'BIOTECH',
            'description': 'Biotechnology and methods development',
            'keywords': [
                'biosensor', 'sequencing', 'omics', 'proteomics', 'metabolomics',
                'imaging', 'spectroscopy', 'mass spectrometry', 'assay development',
                'high-throughput', 'bioinformatics', 'machine learning',
            ],
            'threshold': 2.0,
        },
        {
            'name': 'CLIMATE',
            'description': 'Climate and ecosystem research',
            'keywords': [
                'climate', 'ecosystem', 'carbon', 'greenhouse', 'biodiversity',
                'conservation', 'species', 'habitat', 'marine', 'forest',
                'atmospheric', 'ocean', 'warming', 'adaptation',
            ],
            'threshold': 2.0,
        },
        {
            'name': 'OTHER',
            'description': 'Other research not fitting above categories',
            'keywords': [],
            'threshold': 0.0,  # Catch-all
        },
    ]


def get_drug_development_categories() -> List[dict]:
    """Drug development classification scheme."""
    return [
        {
            'name': 'target_discovery',
            'description': 'Target identification and validation',
            'keywords': [
                'target identification', 'target validation', 'disease mechanism',
                'biomarker', 'genetic variant', 'driver mutation', 'therapeutic target',
            ],
        },
        {
            'name': 'lead_discovery',
            'description': 'Lead compound discovery and optimization',
            'keywords': [
                'lead compound', 'hit-to-lead', 'lead optimization', 'drug discovery',
                'screening', 'medicinal chemistry', 'SAR', 'structure-activity',
            ],
        },
        {
            'name': 'preclinical',
            'description': 'Preclinical development',
            'keywords': [
                'preclinical', 'animal model', 'pharmacokinetics', 'ADME',
                'toxicology study', 'IND-enabling', 'formulation',
            ],
        },
        {
            'name': 'clinical',
            'description': 'Clinical trials',
            'keywords': [
                'clinical trial', 'phase 1', 'phase 2', 'phase 3', 'phase I', 'phase II', 'phase III',
                'patient enrollment', 'efficacy', 'safety trial',
            ],
        },
    ]


CLASSIFICATION_PRESETS = {
    'environmental_health': get_environmental_health_categories,
    'drug_development': get_drug_development_categories,
}


def get_preset_config(name: str) -> dict:
    """Get a preset classification config by name."""
    if name not in CLASSIFICATION_PRESETS:
        raise ValueError(f"Unknown preset: {name}. Available: {list(CLASSIFICATION_PRESETS.keys())}")
    return {'categories': CLASSIFICATION_PRESETS[name]()}
