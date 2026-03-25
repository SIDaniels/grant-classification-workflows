import csv
import os
import json
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

def get_env_subgroup(row):
    for key in ['Environmental_Subgroup', 'Env_Subgroup']:
        if key in row and row[key]:
            return row[key]
    return "Other"

# Collect data
category_data = []
subfield_data = []

disease_order = [
    "ALS", "Biodefense", "Breast Cancer", "Liver Disease",
    "Contraception Reproduction", "Parkinsons", "Colorectal Cancer", "Lung Cancer"
]

files = [f for f in os.listdir(base_path) if f.endswith('_combined.csv')]

for filename in files:
    filepath = os.path.join(base_path, filename)
    disease = filename.replace("_combined.csv", "").replace("_", " ")

    totals = {'mechanistic': 0, 'environmental': 0, 'everything_else': 0}
    env_subgroups = defaultdict(float)

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = get_tag(row)
            amount = get_amount(row)

            if 'Mechanistic' in tag:
                totals['mechanistic'] += amount
            elif 'Environmental' in tag:
                totals['environmental'] += amount
                subgroup = get_env_subgroup(row)
                env_subgroups[subgroup] += amount
            else:
                totals['everything_else'] += amount

    total = sum(totals.values())

    category_data.append({
        'disease': disease,
        'total': int(total),
        'mechanistic': int(totals['mechanistic']),
        'environmental': int(totals['environmental']),
        'everything_else': int(totals['everything_else']),
        'mech_pct': round(totals['mechanistic'] / total * 100, 1) if total else 0,
        'env_pct': round(totals['environmental'] / total * 100, 1) if total else 0,
        'ee_pct': round(totals['everything_else'] / total * 100, 1) if total else 0
    })

    # Add subfield data
    for subgroup, amount in env_subgroups.items():
        if amount > 0:
            subfield_data.append({
                'disease': disease,
                'subfield': subgroup,
                'amount': int(amount)
            })

# Sort category_data by disease_order
category_data.sort(key=lambda x: disease_order.index(x['disease']) if x['disease'] in disease_order else 99)

# Calculate grand totals
grand_totals = {
    'total': sum(d['total'] for d in category_data),
    'mechanistic': sum(d['mechanistic'] for d in category_data),
    'environmental': sum(d['environmental'] for d in category_data),
    'everything_else': sum(d['everything_else'] for d in category_data)
}

output = {
    'category_data': category_data,
    'subfield_data': subfield_data,
    'grand_totals': grand_totals
}

# Write to JSON
output_path = "/Users/sarahdaniels/Documents/grant_categorization/viz_data_dollars.json"
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print("Updated viz_data_dollars.json")
print(f"\nGrand Totals:")
print(f"  Total: ${grand_totals['total']/1e6:,.1f}M")
print(f"  Biological Mechanisms: ${grand_totals['mechanistic']/1e6:,.1f}M ({grand_totals['mechanistic']/grand_totals['total']*100:.1f}%)")
print(f"  Clinical: ${grand_totals['everything_else']/1e6:,.1f}M ({grand_totals['everything_else']/grand_totals['total']*100:.1f}%)")
print(f"  Environmental: ${grand_totals['environmental']/1e6:,.1f}M ({grand_totals['environmental']/grand_totals['total']*100:.1f}%)")

print("\nBy Disease:")
for d in category_data:
    print(f"  {d['disease']:25} ${d['total']/1e6:6.1f}M  Mech:{d['mech_pct']:4.1f}%  Env:{d['env_pct']:4.1f}%  Clin:{d['ee_pct']:4.1f}%")
