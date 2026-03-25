"""
LLM-based grant classifier using Claude.

For high-accuracy classification when keyword matching is insufficient.
Supports batch processing with rate limiting and retry logic.
"""

import json
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class LLMClassificationResult:
    """Result from LLM classification."""
    grant_id: str
    primary_category: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    subcategory: Optional[str] = None
    entities_mentioned: List[str] = field(default_factory=list)
    raw_response: Optional[str] = None
    error: Optional[str] = None


class LLMClassifier:
    """
    Classify grants using Claude or other LLMs.

    Features:
    - Configurable prompts and categories
    - Batch processing with concurrency
    - Rate limiting and retry logic
    - Structured output parsing
    """

    def __init__(self, config: dict):
        """
        Initialize from config.

        Expected config structure:
        {
            'api_key': 'sk-...' or use ANTHROPIC_API_KEY env var,
            'model': 'claude-3-haiku-20240307',  # or sonnet/opus
            'categories': [
                {'name': 'CAT1', 'description': 'what it means'},
                ...
            ],
            'system_prompt': 'optional custom system prompt',
            'max_tokens': 500,
            'temperature': 0.0,
            'rate_limit_rpm': 60,  # requests per minute
            'max_retries': 3,
            'batch_size': 10,  # concurrent requests
        }
        """
        self.config = config

        # Get API key
        import os
        self.api_key = config.get('api_key') or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Set 'api_key' in config or ANTHROPIC_API_KEY env var.")

        self.model = config.get('model', 'claude-3-haiku-20240307')
        self.max_tokens = config.get('max_tokens', 500)
        self.temperature = config.get('temperature', 0.0)

        # Rate limiting
        self.rate_limit_rpm = config.get('rate_limit_rpm', 60)
        self._request_times: List[float] = []

        # Retry settings
        self.max_retries = config.get('max_retries', 3)
        self.batch_size = config.get('batch_size', 10)

        # Build prompt from categories
        self.categories = config.get('categories', [])
        self.system_prompt = config.get('system_prompt') or self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build classification system prompt from categories."""
        categories_desc = "\n".join(
            f"- {cat['name']}: {cat.get('description', '')}"
            for cat in self.categories
        )

        return f"""You are a grant classification expert. Classify research grants into the following categories:

{categories_desc}

For each grant, provide:
1. The primary category (one of the category names above)
2. Your confidence level (0.0 to 1.0)
3. Brief reasoning (1-2 sentences)
4. Key entities mentioned (chemicals, diseases, methods, etc.)

Respond in JSON format:
{{
  "category": "CATEGORY_NAME",
  "confidence": 0.85,
  "reasoning": "Brief explanation",
  "entities": ["entity1", "entity2"]
}}

Be consistent and precise. If a grant doesn't fit well, choose the closest match and lower your confidence."""

    def _call_api(self, title: str, abstract: str) -> str:
        """Make API call to Claude."""
        import urllib.request
        import urllib.error

        # Rate limiting
        self._enforce_rate_limit()

        prompt = f"""Classify this research grant:

Title: {title}

Abstract: {abstract}"""

        data = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "system": self.system_prompt,
            "messages": [{"role": "user", "content": prompt}]
        }

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read())
            return result['content'][0]['text']

    def _enforce_rate_limit(self):
        """Enforce rate limiting."""
        now = time.time()

        # Remove old timestamps
        self._request_times = [t for t in self._request_times if now - t < 60]

        # If at limit, wait
        if len(self._request_times) >= self.rate_limit_rpm:
            sleep_time = 60 - (now - self._request_times[0]) + 0.1
            if sleep_time > 0:
                time.sleep(sleep_time)

        self._request_times.append(time.time())

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from LLM."""
        try:
            # Try to extract JSON from response
            # Handle cases where response has extra text
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # Fallback: try to extract key fields
        return {
            'category': None,
            'confidence': 0.0,
            'reasoning': response,
            'entities': []
        }

    def classify(self, grant_id: str, title: str, abstract: str) -> LLMClassificationResult:
        """Classify a single grant."""
        for attempt in range(self.max_retries):
            try:
                response = self._call_api(title, abstract)
                parsed = self._parse_response(response)

                return LLMClassificationResult(
                    grant_id=grant_id,
                    primary_category=parsed.get('category', 'UNKNOWN'),
                    confidence=float(parsed.get('confidence', 0.0)),
                    reasoning=parsed.get('reasoning', ''),
                    entities_mentioned=parsed.get('entities', []),
                    raw_response=response,
                )

            except Exception as e:
                if attempt == self.max_retries - 1:
                    return LLMClassificationResult(
                        grant_id=grant_id,
                        primary_category='ERROR',
                        confidence=0.0,
                        reasoning='',
                        error=str(e),
                    )
                time.sleep(2 ** attempt)  # Exponential backoff

        # Should not reach here
        return LLMClassificationResult(
            grant_id=grant_id,
            primary_category='ERROR',
            confidence=0.0,
            reasoning='',
            error='Max retries exceeded',
        )

    def classify_batch(
        self,
        grants: List[Dict[str, Any]],
        id_field: str = 'id',
        title_field: str = 'title',
        abstract_field: str = 'abstract',
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> List[LLMClassificationResult]:
        """
        Classify a batch of grants with concurrent processing.

        Args:
            grants: List of grant dicts
            id_field: Key for grant ID
            title_field: Key for title
            abstract_field: Key for abstract
            progress_callback: Optional callback(completed, total)

        Returns:
            List of LLMClassificationResult
        """
        results = []
        total = len(grants)

        # Process in batches
        with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
            futures = {}

            for grant in grants:
                future = executor.submit(
                    self.classify,
                    grant_id=str(grant.get(id_field, '')),
                    title=grant.get(title_field, ''),
                    abstract=grant.get(abstract_field, ''),
                )
                futures[future] = grant.get(id_field)

            for i, future in enumerate(as_completed(futures)):
                result = future.result()
                results.append(result)

                if progress_callback:
                    progress_callback(i + 1, total)

        # Sort results by original order
        id_to_result = {r.grant_id: r for r in results}
        ordered_results = [
            id_to_result.get(str(g.get(id_field)), None)
            for g in grants
        ]

        return [r for r in ordered_results if r is not None]

    def summary(self, results: List[LLMClassificationResult]) -> Dict[str, Any]:
        """Generate summary statistics."""
        total = len(results)
        if total == 0:
            return {'total': 0}

        from collections import defaultdict

        by_category = defaultdict(int)
        confidence_sum = 0.0
        error_count = 0

        for r in results:
            by_category[r.primary_category] += 1
            confidence_sum += r.confidence
            if r.error:
                error_count += 1

        return {
            'total': total,
            'by_category': dict(by_category),
            'avg_confidence': confidence_sum / total,
            'error_count': error_count,
            'error_rate': error_count / total * 100,
        }


class MockLLMClassifier(LLMClassifier):
    """
    Mock classifier for testing without API calls.

    Uses simple keyword matching to simulate LLM behavior.
    """

    def __init__(self, config: dict):
        # Skip API key requirement
        self.config = config
        self.categories = config.get('categories', [])
        self.system_prompt = ""
        self.rate_limit_rpm = 1000
        self._request_times = []
        self.max_retries = 1
        self.batch_size = 100

    def _call_api(self, title: str, abstract: str) -> str:
        """Mock API call using keyword matching."""
        text = f"{title} {abstract}".lower()

        best_category = None
        best_score = 0

        for cat in self.categories:
            score = 0
            # Simple keyword matching from description
            desc_words = cat.get('description', '').lower().split()
            for word in desc_words:
                if len(word) > 3 and word in text:
                    score += 1

            if score > best_score:
                best_score = score
                best_category = cat['name']

        confidence = min(0.9, best_score * 0.2) if best_score > 0 else 0.3

        return json.dumps({
            'category': best_category or self.categories[0]['name'] if self.categories else 'UNKNOWN',
            'confidence': confidence,
            'reasoning': 'Mock classification based on keyword matching',
            'entities': []
        })
