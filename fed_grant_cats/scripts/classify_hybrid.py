#!/usr/bin/env python3
"""
Hybrid classification: keyword-based with confidence scoring.
High-confidence = keep as-is; Low-confidence = flagged for review.
"""
import json
from pathlib import Path

UNCLASSIFIED = Path("/Users/sarahdaniels/Documents/nsf_grants/unclassified_full.json")
HAIKU_CLASSIFIED = Path("/Users/sarahdaniels/Documents/nsf_grants/haiku_classified_full.json")
OUTPUT = Path("/Users/sarahdaniels/Documents/nsf_grants/all_grants_classified.json")
AMBIGUOUS_OUTPUT = Path("/Users/sarahdaniels/Documents/nsf_grants/ambiguous_grants.json")

# Environmental keywords
ENV_KEYWORDS = [
    'environmental', 'pollution', 'pollutant', 'contamination', 'exposure',
    'climate', 'climate change', 'global warming', 'greenhouse', 'carbon',
    'ecosystem', 'ecological', 'biodiversity', 'habitat', 'conservation',
    'water quality', 'air quality', 'soil', 'sediment', 'groundwater',
    'ocean', 'marine', 'coastal', 'aquatic', 'freshwater', 'wetland',
    'forest', 'wildfire', 'drought', 'flood', 'hurricane', 'tornado',
    'atmosphere', 'atmospheric', 'ozone', 'aerosol', 'particulate',
    'toxic', 'toxicology', 'pesticide', 'herbicide', 'heavy metal',
    'pfas', 'microplastic', 'plastic pollution', 'waste', 'landfill',
    'renewable energy', 'solar', 'wind energy', 'sustainability',
    'endangered species', 'invasive species', 'wildlife', 'migration',
    'coral reef', 'glacier', 'ice sheet', 'permafrost', 'sea level',
    'weather', 'meteorology', 'precipitation', 'temperature change',
    'land use', 'deforestation', 'urbanization', 'agriculture impact',
    'drinking water', 'wastewater', 'stormwater', 'runoff',
    'environmental health', 'environmental justice', 'air pollution',
    'water pollution', 'soil contamination', 'chemical exposure'
]

# Biological mechanism keywords
MECH_KEYWORDS = [
    'mechanism', 'pathway', 'signaling', 'signal transduction',
    'molecular', 'cellular', 'cell', 'protein', 'enzyme', 'receptor',
    'gene', 'genetic', 'genome', 'genomic', 'transcription', 'translation',
    'dna', 'rna', 'mrna', 'mutation', 'expression', 'regulation',
    'metabolism', 'metabolic', 'mitochondria', 'atp',
    'immune', 'immunity', 'inflammation', 'cytokine', 'antibody',
    'neuron', 'neural', 'synapse', 'neurotransmitter', 'brain',
    'disease mechanism', 'pathogen', 'infection', 'viral', 'bacterial',
    'cancer', 'tumor', 'oncogene', 'apoptosis', 'cell death',
    'stem cell', 'differentiation', 'development', 'embryo',
    'hormone', 'endocrine', 'insulin', 'glucose',
    'membrane', 'ion channel', 'transporter',
    'oxidative stress', 'antioxidant', 'reactive oxygen',
    'circadian', 'biological clock', 'homeostasis',
    'epigenetic', 'methylation', 'histone',
    'microbiome', 'gut bacteria', 'symbiosis',
    'biochemistry', 'biophysics', 'structural biology'
]

def classify_grant(title, abstract):
    """Classify with confidence score."""
    text = f"{title} {abstract}".lower()

    env_hits = [kw for kw in ENV_KEYWORDS if kw.lower() in text]
    mech_hits = [kw for kw in MECH_KEYWORDS if kw.lower() in text]

    env_score = len(env_hits)
    mech_score = len(mech_hits)
    total_hits = env_score + mech_score

    # Determine category
    if env_score > mech_score and env_score >= 2:
        category = "ENV"
        confidence = min(1.0, env_score / 5)  # 5+ hits = full confidence
    elif mech_score > env_score and mech_score >= 2:
        category = "MECH"
        confidence = min(1.0, mech_score / 5)
    elif env_score >= 2:
        category = "ENV"
        confidence = 0.5 if mech_score > 0 else min(1.0, env_score / 5)
    elif mech_score >= 2:
        category = "MECH"
        confidence = 0.5 if env_score > 0 else min(1.0, mech_score / 5)
    elif env_score == 1 and mech_score == 0:
        category = "ENV"
        confidence = 0.3
    elif mech_score == 1 and env_score == 0:
        category = "MECH"
        confidence = 0.3
    else:
        category = "OTHER"
        confidence = 0.8 if total_hits == 0 else 0.4  # No hits = likely truly OTHER

    # Lower confidence if scores are close
    if env_score > 0 and mech_score > 0:
        ratio = min(env_score, mech_score) / max(env_score, mech_score)
        if ratio > 0.5:  # Scores within 2x of each other
            confidence *= 0.7

    return {
        'category': category,
        'confidence': round(confidence, 2),
        'env_score': env_score,
        'mech_score': mech_score,
        'env_keywords': env_hits[:5],
        'mech_keywords': mech_hits[:5],
        'method': 'keyword'
    }

def main():
    # Load unclassified
    print("Loading unclassified grants...")
    with open(UNCLASSIFIED) as f:
        unclassified = json.load(f)
    print(f"  {len(unclassified)} unclassified grants")

    # Load existing Haiku classifications
    print("Loading existing Haiku classifications...")
    with open(HAIKU_CLASSIFIED) as f:
        haiku_classified = json.load(f)
    print(f"  {len(haiku_classified)} already classified by Haiku")

    # Classify remaining grants
    print("\nClassifying with keywords...")
    keyword_results = []
    ambiguous = []

    for g in unclassified:
        grant_id = g.get('id', '')
        title = g.get('title', '')
        abstract = g.get('abstractText', '') or ''

        result = classify_grant(title, abstract)
        result['id'] = grant_id
        result['title'] = title

        keyword_results.append(result)

        if result['confidence'] < 0.5:
            ambiguous.append({
                'id': grant_id,
                'title': title,
                'abstract': abstract[:500],
                'assigned': result['category'],
                'confidence': result['confidence'],
                'env_score': result['env_score'],
                'mech_score': result['mech_score']
            })

    # Merge all results
    all_classified = []

    # Add Haiku results (mark as high confidence)
    for g in haiku_classified:
        g['method'] = 'haiku'
        g['confidence'] = 0.95
        all_classified.append(g)

    # Add keyword results
    all_classified.extend(keyword_results)

    # Stats
    print("\n=== Classification Results ===")

    counts = {'ENV': 0, 'MECH': 0, 'OTHER': 0}
    high_conf = {'ENV': 0, 'MECH': 0, 'OTHER': 0}

    for r in all_classified:
        cat = r.get('category', 'OTHER')
        counts[cat] = counts.get(cat, 0) + 1
        if r.get('confidence', 0) >= 0.5:
            high_conf[cat] = high_conf.get(cat, 0) + 1

    total = len(all_classified)
    for cat in ['ENV', 'MECH', 'OTHER']:
        pct = 100 * counts[cat] / total
        print(f"  {cat}: {counts[cat]:,} ({pct:.1f}%) - {high_conf[cat]:,} high-confidence")
    print(f"  TOTAL: {total:,}")
    print(f"\n  Ambiguous (conf < 0.5): {len(ambiguous):,}")

    # Save
    with open(OUTPUT, 'w') as f:
        json.dump(all_classified, f)
    print(f"\nSaved all classifications to {OUTPUT}")

    with open(AMBIGUOUS_OUTPUT, 'w') as f:
        json.dump(ambiguous, f, indent=2)
    print(f"Saved {len(ambiguous)} ambiguous grants to {AMBIGUOUS_OUTPUT}")

if __name__ == "__main__":
    main()
