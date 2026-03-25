import csv
import os
import random
import re
from collections import defaultdict

base_path = "/Users/sarahdaniels/Documents/grant_categorization/combined_categories"

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

# Collect all grants by category
mechanistic = []
clinical = []

files = [f for f in os.listdir(base_path) if f.endswith('_combined.csv')]

for filename in sorted(files):
    filepath = os.path.join(base_path, filename)
    disease = filename.replace("_combined.csv", "").replace("_", " ")

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = get_tag(row)
            title = get_title(row)
            amount = get_amount(row)

            if 'Mechanistic' in tag:
                mechanistic.append((disease, title, amount))
            elif 'Everything_else' in tag:
                clinical.append((disease, title, amount))

print("=" * 100)
print("MANUAL SAMPLE REVIEW")
print("=" * 100)
print(f"Total Mechanistic: {len(mechanistic):,} grants, ${sum(x[2] for x in mechanistic)/1e9:.2f}B")
print(f"Total Clinical: {len(clinical):,} grants, ${sum(x[2] for x in clinical)/1e9:.2f}B")

# Set seed for reproducibility
random.seed(123)

# Sample 100 from each for manual review
mech_sample = random.sample(mechanistic, 100)
clin_sample = random.sample(clinical, 100)

# Classify each based on title
# For mechanistic: check if it looks like clinical, infrastructure, or environmental
# For clinical: check if it looks like mechanistic

mech_issues = []
clin_issues = []

# Patterns for misclassification
clinical_patterns = [
    (r'phase [I1-4]+[ab]?\b', 'CLINICAL_TRIAL'),
    (r'clinical trial', 'CLINICAL_TRIAL'),
    (r'randomized.*trial', 'CLINICAL_TRIAL'),
    (r'randomized controlled', 'CLINICAL_TRIAL'),
    (r'patient.*outcome', 'CLINICAL_OUTCOME'),
    (r'treatment outcome', 'CLINICAL_OUTCOME'),
    (r'quality of life', 'CLINICAL'),
    (r'survivorship', 'CLINICAL'),
    (r'screening program', 'CLINICAL'),
    (r'diagnostic accuracy', 'CLINICAL'),
]

infra_patterns = [
    (r'pilot plant', 'INFRASTRUCTURE'),
    (r'repository', 'INFRASTRUCTURE'),
    (r'\bcore\b(?!.*protein)(?!.*pathway)(?!.*receptor)', 'INFRASTRUCTURE'),
    (r'coordinating center', 'INFRASTRUCTURE'),
    (r'leadership group', 'INFRASTRUCTURE'),
    (r'support service', 'INFRASTRUCTURE'),
    (r'training program', 'INFRASTRUCTURE'),
    (r'career development', 'INFRASTRUCTURE'),
    (r'data management center', 'INFRASTRUCTURE'),
]

env_patterns = [
    (r'environmental exposure', 'ENVIRONMENTAL'),
    (r'pollutant', 'ENVIRONMENTAL'),
    (r'pesticide exposure', 'ENVIRONMENTAL'),
    (r'smoking.*risk', 'ENVIRONMENTAL'),
    (r'diet.*risk', 'ENVIRONMENTAL'),
]

mech_patterns = [
    (r'signaling pathway', 'MECHANISTIC'),
    (r'molecular mechanism', 'MECHANISTIC'),
    (r'gene expression', 'MECHANISTIC'),
    (r'protein.*interaction', 'MECHANISTIC'),
    (r'knockout', 'MECHANISTIC'),
    (r'transgenic', 'MECHANISTIC'),
    (r'tumor microenvironment', 'MECHANISTIC'),
    (r'metastasis mechanism', 'MECHANISTIC'),
]

print(f"\n\n{'='*80}")
print("MECHANISTIC SAMPLE REVIEW (100 random grants)")
print(f"{'='*80}")

for disease, title, amount in sorted(mech_sample, key=lambda x: -x[2]):
    title_lower = title.lower()

    # Check for clinical patterns
    for pattern, reason in clinical_patterns:
        if re.search(pattern, title_lower, re.IGNORECASE):
            mech_issues.append((disease, title, amount, f'SHOULD_BE_CLINICAL: {reason}'))
            break
    else:
        # Check for infrastructure patterns
        for pattern, reason in infra_patterns:
            if re.search(pattern, title_lower, re.IGNORECASE):
                mech_issues.append((disease, title, amount, f'SHOULD_BE_INFRA: {reason}'))
                break
        else:
            # Check for environmental patterns
            for pattern, reason in env_patterns:
                if re.search(pattern, title_lower, re.IGNORECASE):
                    mech_issues.append((disease, title, amount, f'SHOULD_BE_ENV: {reason}'))
                    break

print(f"\nIssues found in Mechanistic sample: {len(mech_issues)} / 100")
print(f"Issue rate: {len(mech_issues)}%")
print(f"Projected issues in full Mechanistic: ~{int(len(mechanistic) * len(mech_issues) / 100):,} grants")

for disease, title, amount, issue in sorted(mech_issues, key=lambda x: -x[2]):
    print(f"\n[{disease}] ${amount/1e6:.2f}M - {issue}")
    print(f"  {title[:100]}")

print(f"\n\n{'='*80}")
print("CLINICAL SAMPLE REVIEW (100 random grants)")
print(f"{'='*80}")

for disease, title, amount in sorted(clin_sample, key=lambda x: -x[2]):
    title_lower = title.lower()

    # Check for mechanistic patterns (should not be in clinical)
    for pattern, reason in mech_patterns:
        if re.search(pattern, title_lower, re.IGNORECASE):
            clin_issues.append((disease, title, amount, f'SHOULD_BE_MECH: {reason}'))
            break
    else:
        # Check for environmental patterns
        for pattern, reason in env_patterns:
            if re.search(pattern, title_lower, re.IGNORECASE):
                clin_issues.append((disease, title, amount, f'SHOULD_BE_ENV: {reason}'))
                break

print(f"\nIssues found in Clinical sample: {len(clin_issues)} / 100")
print(f"Issue rate: {len(clin_issues)}%")
print(f"Projected issues in full Clinical: ~{int(len(clinical) * len(clin_issues) / 100):,} grants")

for disease, title, amount, issue in sorted(clin_issues, key=lambda x: -x[2]):
    print(f"\n[{disease}] ${amount/1e6:.2f}M - {issue}")
    print(f"  {title[:100]}")

# Also do a separate check for HIGH-DOLLAR grants (top 100 in each category)
print(f"\n\n{'='*80}")
print("HIGH-DOLLAR MECHANISTIC REVIEW (top 100 by amount)")
print(f"{'='*80}")

mech_top = sorted(mechanistic, key=lambda x: -x[2])[:100]
top_issues = []

for disease, title, amount in mech_top:
    title_lower = title.lower()

    for pattern, reason in clinical_patterns + infra_patterns:
        if re.search(pattern, title_lower, re.IGNORECASE):
            top_issues.append((disease, title, amount, reason))
            break

print(f"\nIssues in top 100 Mechanistic: {len(top_issues)}")
print(f"Total $ at risk: ${sum(x[2] for x in top_issues)/1e6:.1f}M")

for disease, title, amount, issue in top_issues:
    print(f"\n[{disease}] ${amount/1e6:.2f}M - {issue}")
    print(f"  {title[:100]}")
