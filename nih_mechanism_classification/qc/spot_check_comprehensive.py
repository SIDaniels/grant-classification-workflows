import csv
import os
import random
from collections import defaultdict, Counter

base_path = "/Users/sarahdaniels/Documents/grant_categorization/combined_categories"
files = [f for f in os.listdir(base_path) if f.endswith('_combined.csv')]

def get_title(row):
    for key in ['Project_Title', 'Project Title']:
        if key in row and row[key]:
            return row[key]
    return ""

def get_tag(row):
    for key in ['Combined_Tag', 'Tag']:
        if key in row and row[key]:
            return row[key]
    return ""

def get_amount(row):
    for key in ['Amount_numeric', 'Amount']:
        if key in row and row[key]:
            try:
                val = row[key].replace(',', '').replace('$', '')
                return float(val)
            except:
                pass
    return 0

# Collect all grants by disease and high-level category
all_grants = defaultdict(lambda: defaultdict(list))

for filename in sorted(files):
    filepath = os.path.join(base_path, filename)
    disease = filename.replace("_combined.csv", "").replace("_", " ")

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = get_tag(row)
            title = get_title(row)
            amount = get_amount(row)

            if 'Environmental' in tag:
                category = 'Environmental'
            elif 'Mechanistic' in tag:
                category = 'Mechanistic'
            elif 'Everything_else' in tag:
                category = 'Clinical'
            else:
                category = 'Unknown'

            all_grants[disease][category].append({
                'title': title,
                'amount': amount,
                'tag': tag
            })

print("=" * 100)
print("ITERATION 1: HIGH-LEVEL CATEGORIZATION SPOT CHECK")
print("=" * 100)

# Sample 5 grants from each category for each disease
random.seed(42)  # For reproducibility

for disease in sorted(all_grants.keys()):
    print(f"\n{'='*80}")
    print(f"DISEASE: {disease}")
    print(f"{'='*80}")

    for category in ['Environmental', 'Mechanistic', 'Clinical']:
        grants = all_grants[disease][category]
        if not grants:
            continue

        print(f"\n--- {category} ({len(grants)} grants) ---")

        # Sample up to 5 grants
        sample = random.sample(grants, min(5, len(grants)))

        for i, g in enumerate(sample, 1):
            title = g['title'][:100] + "..." if len(g['title']) > 100 else g['title']
            print(f"  {i}. [{g['tag']}] ${g['amount']/1e6:.2f}M")
            print(f"     {title}")

print("\n\n")
print("=" * 100)
print("LOOKING FOR POTENTIAL MISCLASSIFICATIONS")
print("=" * 100)

# Define keywords that might indicate wrong category
env_keywords = ['pollutant', 'exposure', 'pesticide', 'chemical', 'environmental',
                'air quality', 'water quality', 'toxicant', 'contamina', 'arsenic',
                'lead exposure', 'mercury', 'smoking', 'tobacco', 'cigarette',
                'diet', 'obesity', 'nutrition', 'microbiome', 'gut bacteria',
                'alcohol', 'radiation']

mech_keywords = ['signaling', 'pathway', 'kinase', 'receptor', 'gene expression',
                 'protein', 'molecular mechanism', 'cell cycle', 'apoptosis',
                 'tumor', 'metastasis', 'oncogene', 'mutation', 'transgenic',
                 'knockout', 'mouse model', 'in vitro', 'in vivo', 'cell line',
                 'transcription', 'epigenetic', 'chromatin', 'histone',
                 'mitochondria', 'metabolism', 'enzyme', 'substrate']

clinical_keywords = ['clinical trial', 'patient', 'randomized', 'placebo',
                     'treatment', 'therapy', 'intervention', 'outcome',
                     'quality of life', 'survivorship', 'screening', 'detection',
                     'diagnosis', 'prognosis', 'cohort study', 'epidemiol',
                     'training', 'career', 'fellowship', 'core', 'infrastructure']

def check_keywords(title, keywords):
    title_lower = title.lower()
    matches = [kw for kw in keywords if kw in title_lower]
    return matches

print("\n--- Potential Environmental grants in Mechanistic/Clinical ---")
misclass_count = 0
for disease in sorted(all_grants.keys()):
    for category in ['Mechanistic', 'Clinical']:
        for g in all_grants[disease][category]:
            matches = check_keywords(g['title'], env_keywords)
            if len(matches) >= 2:  # At least 2 environmental keywords
                print(f"\n[{disease}] [{category}] ${g['amount']/1e6:.2f}M")
                print(f"  Title: {g['title'][:120]}")
                print(f"  Env keywords: {matches}")
                misclass_count += 1

print(f"\nFound {misclass_count} potential environmental grants in wrong category")

print("\n--- Potential Mechanistic grants in Environmental/Clinical ---")
misclass_count = 0
for disease in sorted(all_grants.keys()):
    for category in ['Environmental', 'Clinical']:
        for g in all_grants[disease][category]:
            matches = check_keywords(g['title'], mech_keywords)
            if len(matches) >= 2:  # At least 2 mechanistic keywords
                print(f"\n[{disease}] [{category}] ${g['amount']/1e6:.2f}M")
                print(f"  Title: {g['title'][:120]}")
                print(f"  Mech keywords: {matches}")
                misclass_count += 1

print(f"\nFound {misclass_count} potential mechanistic grants in wrong category")

print("\n--- Potential Clinical grants in Environmental/Mechanistic ---")
misclass_count = 0
for disease in sorted(all_grants.keys()):
    for category in ['Environmental', 'Mechanistic']:
        for g in all_grants[disease][category]:
            matches = check_keywords(g['title'], clinical_keywords)
            if len(matches) >= 2:  # At least 2 clinical keywords
                print(f"\n[{disease}] [{category}] ${g['amount']/1e6:.2f}M")
                print(f"  Title: {g['title'][:120]}")
                print(f"  Clinical keywords: {matches}")
                misclass_count += 1

print(f"\nFound {misclass_count} potential clinical grants in wrong category")

print("\n\n")
print("=" * 100)
print("SUMMARY STATISTICS")
print("=" * 100)

total_grants = 0
total_dollars = 0
category_stats = defaultdict(lambda: {'count': 0, 'dollars': 0})

for disease in all_grants:
    for category in all_grants[disease]:
        for g in all_grants[disease][category]:
            total_grants += 1
            total_dollars += g['amount']
            category_stats[category]['count'] += 1
            category_stats[category]['dollars'] += g['amount']

print(f"\nTotal grants: {total_grants}")
print(f"Total funding: ${total_dollars/1e9:.2f}B")
print()

for cat in ['Environmental', 'Mechanistic', 'Clinical']:
    stats = category_stats[cat]
    print(f"{cat:15s}: {stats['count']:5d} grants ({100*stats['count']/total_grants:.1f}%)  ${stats['dollars']/1e9:.2f}B ({100*stats['dollars']/total_dollars:.1f}%)")
