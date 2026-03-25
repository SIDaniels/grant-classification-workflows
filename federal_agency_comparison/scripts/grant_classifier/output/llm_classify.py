#!/usr/bin/env python3
"""
LLM-based grant classification for untagged biomining grants.
Uses Claude API via urllib (no external dependencies).
"""

import json
import os
import time
import urllib.request
import urllib.error

# Get API key from environment
API_KEY = os.environ.get('ANTHROPIC_API_KEY')
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable required")

# Define valid categories
MATERIALS = [
    "rare_earth", "critical_minerals", "coal_byproduct", "lithium",
    "general_mineral", "nickel", "uranium", "cobalt", "phosphate",
    "manganese", "copper", "battery_materials", "gold", "zinc"
]

TOPICS = [
    "extraction", "environmental", "separation_purification", "recycling",
    "fundamental_science", "characterization", "modeling_simulation",
    "exploration", "geochemistry", "materials_science", "process_development",
    "waste_valorization"
]


def call_claude(prompt: str) -> str:
    """Call Claude API using urllib."""
    url = "https://api.anthropic.com/v1/messages"

    data = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}]
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read())
        return result['content'][0]['text']


def classify_grant_materials(grant_id: str, description: str) -> dict:
    """Classify a grant by materials using Claude."""
    prompt = f"""Classify this biomining/mineral extraction research grant by the materials it studies.

Grant ID: {grant_id}
Description: {description}

Valid materials categories:
- rare_earth: Rare earth elements (lanthanides, REE, yttrium, scandium)
- critical_minerals: General critical/strategic minerals
- coal_byproduct: Coal ash, coal combustion residuals, acid mine drainage
- lithium: Lithium extraction/recovery
- general_mineral: Non-specific mineral processing
- nickel: Nickel extraction/recovery
- uranium: Uranium extraction/recovery
- cobalt: Cobalt extraction/recovery
- phosphate: Phosphate/phosphorus recovery
- manganese: Manganese extraction/recovery
- copper: Copper extraction/recovery
- battery_materials: General battery metals/materials
- gold: Gold extraction/recovery
- zinc: Zinc extraction/recovery

Return a JSON object with:
- "materials": list of applicable material categories (can be empty if none apply)
- "confidence": "high", "medium", or "low"
- "reasoning": brief explanation

If this grant doesn't involve specific mineral/metal materials extraction, return an empty materials list.
Return ONLY valid JSON, no other text."""

    try:
        response_text = call_claude(prompt)
        # Try to extract JSON from response
        text = response_text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)
        # Validate materials
        result['materials'] = [m for m in result.get('materials', []) if m in MATERIALS]
        return result
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        return {"materials": [], "confidence": "low", "reasoning": f"Parse error: {e}"}


def classify_grant_topics(grant_id: str, description: str) -> dict:
    """Classify a grant by research topics using Claude."""
    prompt = f"""Classify this biomining/mineral extraction research grant by its research topics.

Grant ID: {grant_id}
Description: {description}

Valid topic categories:
- extraction: Metal extraction, leaching, dissolution processes
- environmental: Environmental remediation, contamination, cleanup
- separation_purification: Separation chemistry, purification, selective recovery
- recycling: E-waste recycling, battery recycling, material recovery from waste
- fundamental_science: Basic research, mechanistic studies, theory
- characterization: Analytical methods, sensing, detection, measurement
- modeling_simulation: Computational modeling, simulation, machine learning
- exploration: Prospecting, resource discovery, geological surveys
- geochemistry: Geochemical processes, mineral formation, weathering
- materials_science: Material properties, synthesis, novel materials
- process_development: Scale-up, pilot plants, industrial processes
- waste_valorization: Converting waste streams to valuable products

Return a JSON object with:
- "topics": list of applicable topic categories (can be empty if none apply)
- "confidence": "high", "medium", or "low"
- "reasoning": brief explanation

Return ONLY valid JSON, no other text."""

    try:
        response_text = call_claude(prompt)
        # Try to extract JSON from response
        text = response_text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)
        # Validate topics
        result['topics'] = [t for t in result.get('topics', []) if t in TOPICS]
        return result
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        return {"topics": [], "confidence": "low", "reasoning": f"Parse error: {e}"}


def process_batch(grants: list, classify_func: callable, field_name: str) -> dict:
    """Process a batch of grants and return classifications."""
    results = {}
    total = len(grants)

    for i, grant in enumerate(grants):
        grant_id = grant['id']
        description = grant.get('description', '')

        print(f"  [{i+1}/{total}] Processing {grant_id}...")

        try:
            result = classify_func(grant_id, description)
            results[grant_id] = result

            if result.get(field_name):
                print(f"    → {result[field_name]} ({result.get('confidence', 'unknown')})")
            else:
                print(f"    → No {field_name} identified")

        except urllib.error.HTTPError as e:
            print(f"    → HTTP Error: {e.code}")
            results[grant_id] = {field_name: [], "confidence": "low", "reasoning": str(e)}
        except Exception as e:
            print(f"    → Error: {e}")
            results[grant_id] = {field_name: [], "confidence": "low", "reasoning": str(e)}

        # Rate limiting
        time.sleep(0.5)

    return results


def main():
    # Load untagged grants
    with open('untagged_materials.json') as f:
        untagged_materials = json.load(f)
    with open('untagged_topics.json') as f:
        untagged_topics = json.load(f)

    print(f"Grants without materials tags: {len(untagged_materials)}")
    print(f"Grants without topics tags: {len(untagged_topics)}")

    # Process materials
    print("\n=== CLASSIFYING MATERIALS ===")
    materials_results = process_batch(untagged_materials, classify_grant_materials, 'materials')

    with open('llm_materials_results.json', 'w') as f:
        json.dump(materials_results, f, indent=2)
    print(f"\nSaved materials results to llm_materials_results.json")

    # Process topics
    print("\n=== CLASSIFYING TOPICS ===")
    topics_results = process_batch(untagged_topics, classify_grant_topics, 'topics')

    with open('llm_topics_results.json', 'w') as f:
        json.dump(topics_results, f, indent=2)
    print(f"\nSaved topics results to llm_topics_results.json")

    # Summary
    materials_classified = sum(1 for r in materials_results.values() if r.get('materials'))
    topics_classified = sum(1 for r in topics_results.values() if r.get('topics'))

    print("\n=== SUMMARY ===")
    print(f"Materials: {materials_classified}/{len(untagged_materials)} grants classified")
    print(f"Topics: {topics_classified}/{len(untagged_topics)} grants classified")


if __name__ == '__main__':
    main()
