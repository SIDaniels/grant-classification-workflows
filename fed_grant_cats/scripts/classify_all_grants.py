#!/usr/bin/env python3
"""
Classify all NSF grants using keyword matching.
Categories: ENV, MECH, OTHER
"""
import json
import csv
from pathlib import Path

INPUT = Path("/Users/sarahdaniels/Documents/nsf_grants/nsf_grants_2022_2025.json")
OUTPUT_CSV = Path("/Users/sarahdaniels/Documents/nsf_grants/nsf_grants_classified.csv")
OUTPUT_JSON = Path("/Users/sarahdaniels/Documents/nsf_grants/nsf_classifications.json")

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
    'drinking water', 'wastewater', 'stormwater', 'runoff'
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
    'microbiome', 'gut bacteria', 'symbiosis'
]

def classify_grant(title, abstract):
    """Classify a grant based on title and abstract keywords."""
    text = f"{title} {abstract}".lower()

    env_score = sum(1 for kw in ENV_KEYWORDS if kw.lower() in text)
    mech_score = sum(1 for kw in MECH_KEYWORDS if kw.lower() in text)

    if env_score > mech_score and env_score >= 2:
        return "ENV"
    elif mech_score > env_score and mech_score >= 2:
        return "MECH"
    elif env_score >= 2:
        return "ENV"
    elif mech_score >= 2:
        return "MECH"
    else:
        return "OTHER"

def main():
    print("Loading grants...")
    with open(INPUT) as f:
        grants = json.load(f)

    print(f"Classifying {len(grants)} grants...")

    classifications = {}
    results = []

    for g in grants:
        grant_id = g.get('id', '')
        title = g.get('title', '')
        abstract = g.get('abstractText', '') or ''

        category = classify_grant(title, abstract)
        classifications[grant_id] = category

        results.append({
            'id': grant_id,
            'title': title,
            'category': category,
            'awardeeName': g.get('awardeeName', ''),
            'awardeeStateCode': g.get('awardeeStateCode', ''),
            'estimatedTotalAmt': g.get('estimatedTotalAmt', ''),
            'startDate': g.get('startDate', ''),
            'expDate': g.get('expDate', ''),
            'fundProgramName': g.get('fundProgramName', ''),
            'dirAbbr': g.get('dirAbbr', ''),
            'abstractText': abstract[:1000] if abstract else ''
        })

    # Count categories
    counts = {}
    for cat in classifications.values():
        counts[cat] = counts.get(cat, 0) + 1

    print("\n=== Classification Results ===")
    for cat, count in sorted(counts.items()):
        pct = 100 * count / len(grants)
        print(f"  {cat}: {count:,} ({pct:.1f}%)")
    print(f"  TOTAL: {len(grants):,}")

    # Save JSON classifications
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(classifications, f)
    print(f"\nSaved classifications to {OUTPUT_JSON}")

    # Save CSV with all data
    fieldnames = ['id', 'title', 'category', 'awardeeName', 'awardeeStateCode',
                  'estimatedTotalAmt', 'startDate', 'expDate', 'fundProgramName',
                  'dirAbbr', 'abstractText']

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved classified grants to {OUTPUT_CSV}")

    # Summary by directorate
    print("\n=== By Directorate ===")
    dir_cats = {}
    for g in grants:
        d = g.get('dirAbbr', 'UNK')
        cat = classifications.get(g.get('id', ''), 'OTHER')
        key = (d, cat)
        dir_cats[key] = dir_cats.get(key, 0) + 1

    dirs = sorted(set(k[0] for k in dir_cats.keys()))
    for d in dirs:
        env = dir_cats.get((d, 'ENV'), 0)
        mech = dir_cats.get((d, 'MECH'), 0)
        other = dir_cats.get((d, 'OTHER'), 0)
        total = env + mech + other
        print(f"  {d}: ENV={env}, MECH={mech}, OTHER={other} (total={total})")

if __name__ == "__main__":
    main()
