#!/usr/bin/env python3
"""
Classify EPA borderline grants using established Haiku patterns:
- "health impacts/effects/outcomes" explicitly studied → ENV_HEALTH
- "protect public health" (rationale, not research) → ENV_NOHEALTH
- Infrastructure/construction → OTHER
- Testing/monitoring programs → ENV_NOHEALTH
- Remediation → ENV_NOHEALTH
"""
import json
from pathlib import Path

BORDERLINE = Path("/Users/sarahdaniels/Documents/nsf_grants/epa_borderline_for_haiku.json")
CLASSIFIED = Path("/Users/sarahdaniels/Documents/nsf_grants/epa_grants_classified.json")
OUTPUT = Path("/Users/sarahdaniels/Documents/nsf_grants/epa_grants_final.json")

# Patterns indicating actual health outcomes research (ENV_HEALTH)
HEALTH_RESEARCH_PATTERNS = [
    'health impacts',
    'health effects',
    'health outcomes',
    'epidemiolog',
    'disease association',
    'toxicolog',
    'toxicity study',
    'toxicity studies',
    'health study',
    'health studies',
    'exposure assessment',
    'exposure study',
    'biomarker',
    'cancer risk',
    'respiratory effects',
    'neurological effects',
    'developmental effects',
    'reproductive effects',
    'mortality',
    'morbidity',
    'dose-response',
    'health risk assessment',
    'health surveillance',
    'body burden',
    'blood lead',
    'urinary',
    'serum level',
]

# Patterns indicating infrastructure/construction (OTHER)
INFRASTRUCTURE_PATTERNS = [
    'construction',
    'infrastructure',
    'capital improvement',
    'building',
    'facility upgrade',
    'pipe replacement',
    'sewer line',
    'treatment plant construction',
    'plant upgrade',
    'equipment purchase',
    'vehicle purchase',
    'fleet',
]

def classify_borderline(description, current_type):
    """Classify a borderline grant based on description patterns."""
    desc_lower = (description or '').lower()

    # Check for explicit health research
    for pattern in HEALTH_RESEARCH_PATTERNS:
        if pattern in desc_lower:
            return 'ENV_HEALTH', 'health_research_pattern'

    # Check for infrastructure (should be OTHER)
    for pattern in INFRASTRUCTURE_PATTERNS:
        if pattern in desc_lower:
            return 'OTHER', 'infrastructure_pattern'

    # Default: testing/monitoring/remediation → ENV_NOHEALTH
    # These programs protect health through environmental action
    if current_type in ['testing', 'remediation']:
        return 'ENV_NOHEALTH', 'operational_protection'
    elif current_type == 'infrastructure':
        return 'OTHER', 'infrastructure_default'
    else:
        return 'ENV_NOHEALTH', 'env_default'

def main():
    print("Loading borderline grants...")
    with open(BORDERLINE) as f:
        borderline = json.load(f)
    print(f"  {len(borderline)} borderline grants")

    print("Loading all classified grants...")
    with open(CLASSIFIED) as f:
        all_grants = json.load(f)
    print(f"  {len(all_grants)} total grants")

    # Create lookup for borderline grants
    borderline_ids = {g['id'] for g in borderline}
    borderline_lookup = {g['id']: g for g in borderline}

    # Track reclassifications
    reclassified = {'ENV_HEALTH': 0, 'ENV_NOHEALTH': 0, 'OTHER': 0}
    reasons = {}

    # Process all grants
    for grant in all_grants:
        grant_id = grant.get('id', '')

        if grant_id in borderline_ids:
            bl_grant = borderline_lookup[grant_id]
            current_type = bl_grant.get('type', '')
            description = grant.get('description', '')

            new_category, reason = classify_borderline(description, current_type)
            grant['category'] = 'ENV'
            grant['env_subtype'] = new_category

            reclassified[new_category] += 1
            reasons[reason] = reasons.get(reason, 0) + 1

    # Count final categories
    counts = {'ENV_HEALTH': 0, 'ENV_NOHEALTH': 0, 'MECH': 0, 'OTHER': 0}
    for g in all_grants:
        cat = g.get('category', 'OTHER')
        if cat == 'ENV':
            subtype = g.get('env_subtype', 'ENV_NOHEALTH')
            counts[subtype] = counts.get(subtype, 0) + 1
        else:
            counts[cat] = counts.get(cat, 0) + 1

    print("\n=== Borderline Reclassification ===")
    for cat, count in reclassified.items():
        print(f"  {cat}: {count:,}")

    print("\n=== Reclassification Reasons ===")
    for reason, count in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"  {reason}: {count:,}")

    print("\n=== Final EPA Classification ===")
    total = sum(counts.values())
    for cat in ['ENV_HEALTH', 'ENV_NOHEALTH', 'MECH', 'OTHER']:
        pct = 100 * counts[cat] / total if total > 0 else 0
        print(f"  {cat}: {counts[cat]:,} ({pct:.1f}%)")
    print(f"  TOTAL: {total:,}")

    # Save final classifications
    with open(OUTPUT, 'w') as f:
        json.dump(all_grants, f)
    print(f"\nSaved final classifications to {OUTPUT}")

    return counts

if __name__ == "__main__":
    main()
