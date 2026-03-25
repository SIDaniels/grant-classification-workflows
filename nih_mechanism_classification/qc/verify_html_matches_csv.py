import csv
import os
import re
from collections import defaultdict

base_path = "/Users/sarahdaniels/Documents/grant_categorization/combined_categories"

def get_tag(row):
    for key in ['Combined_Tag', 'Tag']:
        if key in row and row[key]:
            return row[key]
    return ""

def get_amount(row):
    for key in ['Amount_numeric', 'Amount']:
        if key in row and row[key]:
            try:
                val = str(row[key]).replace(',', '').replace('$', '')
                return float(val)
            except:
                pass
    return 0

# Calculate totals from CSVs
csv_totals = defaultdict(lambda: {'mechanistic': 0, 'environmental': 0, 'clinical': 0, 'total': 0})

disease_map = {
    "ALS": "ALS",
    "Biodefense": "Biodefense",
    "Breast Cancer": "Breast Cancer",
    "Colorectal Cancer": "Colorectal Cancer",
    "Contraception Reproduction": "Contraception",
    "Liver Disease": "Liver Disease",
    "Lung Cancer": "Lung Cancer",
    "Parkinsons": "Parkinson's"
}

files = [f for f in os.listdir(base_path) if f.endswith('_combined.csv')]

for filename in files:
    filepath = os.path.join(base_path, filename)
    disease_raw = filename.replace("_combined.csv", "").replace("_", " ")
    disease = disease_map.get(disease_raw, disease_raw)

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = get_tag(row)
            amount = get_amount(row)

            csv_totals[disease]['total'] += amount
            if 'Mechanistic' in tag:
                csv_totals[disease]['mechanistic'] += amount
            elif 'Environmental' in tag:
                csv_totals[disease]['environmental'] += amount
            else:
                csv_totals[disease]['clinical'] += amount

# Extract totals from HTML
with open('viz_sankey_with_heatmap.html', 'r') as f:
    html = f.read()

# Parse categoryData from HTML
html_totals = {}
pattern = r'\{ disease: "([^"]+)", total: (\d+), mechanistic: (\d+), environmental: (\d+), everything_else: (\d+) \}'
matches = re.findall(pattern, html)

for match in matches:
    disease, total, mech, env, clin = match
    html_totals[disease] = {
        'total': int(total),
        'mechanistic': int(mech),
        'environmental': int(env),
        'clinical': int(clin)
    }

# Compare
print("="*80)
print("VERIFICATION: CSV TOTALS vs HTML TOTALS")
print("="*80)
print(f"\n{'Disease':<25} {'Category':<15} {'CSV':>15} {'HTML':>15} {'Match':>8}")
print("-"*80)

all_match = True
for disease in sorted(csv_totals.keys()):
    csv = csv_totals[disease]
    html = html_totals.get(disease, {})

    for cat in ['total', 'mechanistic', 'environmental', 'clinical']:
        csv_val = int(csv[cat])
        html_key = 'clinical' if cat == 'clinical' else cat
        html_val = html.get(html_key, 0)

        match = "✓" if csv_val == html_val else "✗"
        if csv_val != html_val:
            all_match = False
            diff = csv_val - html_val
            print(f"{disease:<25} {cat:<15} ${csv_val/1e6:>12.2f}M ${html_val/1e6:>12.2f}M {match:>8} (diff: ${diff/1e6:.2f}M)")
        else:
            print(f"{disease:<25} {cat:<15} ${csv_val/1e6:>12.2f}M ${html_val/1e6:>12.2f}M {match:>8}")

# Grand totals
print("\n" + "="*80)
print("GRAND TOTALS")
print("="*80)

csv_grand = {
    'total': sum(d['total'] for d in csv_totals.values()),
    'mechanistic': sum(d['mechanistic'] for d in csv_totals.values()),
    'environmental': sum(d['environmental'] for d in csv_totals.values()),
    'clinical': sum(d['clinical'] for d in csv_totals.values())
}

html_grand = {
    'total': sum(d['total'] for d in html_totals.values()),
    'mechanistic': sum(d['mechanistic'] for d in html_totals.values()),
    'environmental': sum(d['environmental'] for d in html_totals.values()),
    'clinical': sum(d['clinical'] for d in html_totals.values())
}

for cat in ['total', 'mechanistic', 'environmental', 'clinical']:
    csv_val = csv_grand[cat]
    html_val = html_grand[cat]
    match = "✓" if csv_val == html_val else "✗"
    print(f"{cat:<15} CSV: ${csv_val/1e6:>10.2f}M  HTML: ${html_val/1e6:>10.2f}M  {match}")

print("\n" + "="*80)
if all_match:
    print("ALL DATA MATCHES PERFECTLY ✓")
else:
    print("SOME MISMATCHES FOUND - SEE ABOVE ✗")
print("="*80)
