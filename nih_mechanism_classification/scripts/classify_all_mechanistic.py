import re
import csv
import os
from collections import Counter

# Keyword patterns
patterns = {
    "Neurodegeneration": [
        r"neurodegen", r"parkinson", r"alzheimer", r"huntington", r"\bALS\b", r"amyotrophic",
        r"dopamine", r"dopaminergic", r"alpha.?synuclein", r"synuclein", r"lewy", r"motor neuron",
        r"neural circuit", r"striatal", r"basal ganglia", r"substantia nigra",
        r"neuroprotect", r"neuronal death", r"cortical circuit", r"tauopathy",
        r"prion", r"aggregat", r"misfolded protein"
    ],
    "Tumor Biology": [
        r"tumor", r"tumour", r"cancer", r"metasta", r"carcinogen", r"oncogene", 
        r"carcinoma", r"adenocarcinoma", r"malignant", r"neoplasm",
        r"angiogenesis", r"epithelial.?mesenchymal", r"\bEMT\b", 
        r"\bKRAS\b", r"\bEGFR\b", r"chemoresist", r"drug.?resist", r"radioresist",
        r"cancer stem", r"tumor.?suppress", r"sarcoma", r"lymphoma", r"melanoma"
    ],
    "Immune/Inflammatory": [
        r"immun", r"inflammat", r"cytokine", r"interleukin", r"\bIL-\d+", 
        r"\bT.?cell", r"\bB.?cell", r"macrophage", r"neutrophil", r"lymphocyte",
        r"antibod", r"autoimmun", r"interferon", r"chemokine", r"\bCXCL", r"\bCCL\d",
        r"checkpoint", r"\bPD-?1\b", r"\bPD-?L1\b", r"\bCD\d+", 
        r"oncolytic", r"CAR-?T", r"dendritic", r"vaccine", r"pathogen"
    ],
    "Genetics/Genomics": [
        r"\bgenetic", r"genom", r"\bGWAS\b", r"variant", r"mutation", r"polymorphism",
        r"\bSNP\b", r"allele", r"hereditary", r"familial", r"inherited",
        r"epigenet", r"methylation", r"histone", r"chromatin", r"\bBRCA", 
        r"DNA repair", r"transcriptom", r"single.?cell", r"\bLRRK2\b",
        r"CRISPR", r"gene edit", r"gene therapy", r"gene expression"
    ],
    "Metabolic": [
        r"metabol", r"\blipid", r"fatty acid", r"\bglucose\b", r"\binsulin",
        r"mitochondri", r"glycoly", r"oxidative stress", r"\bredox\b",
        r"adipose", r"cholesterol", r"triglyceride", r"ferroptosis", r"\bNAD\b",
        r"energy metabolism", r"lipogenesis", r"ketone", r"gluconeogenesis"
    ],
    "Biomarkers": [
        r"biomarker", r"diagnostic marker", r"prognostic marker", r"early detection",
        r"liquid biops", r"circulating tumor", r"cell.?free DNA", r"\bctDNA\b",
        r"biosensor", r"screening marker"
    ]
}

def classify_grant(title):
    if not title:
        return "Other"
    title_lower = title.lower()
    scores = {}
    
    for category, keywords in patterns.items():
        score = 0
        for kw in keywords:
            if re.search(kw, title_lower, re.IGNORECASE):
                score += 1
        if score > 0:
            scores[category] = score
    
    if not scores:
        return "Other"
    
    return max(scores.items(), key=lambda x: x[1])[0]

def get_title(row):
    """Handle inconsistent column names"""
    for key in ['Project_Title', 'Project Title']:
        if key in row and row[key]:
            return row[key]
    return ""

def get_tag(row):
    """Handle tag column"""
    for key in ['Combined_Tag', 'Tag']:
        if key in row and row[key]:
            return row[key]
    return ""

# Process all combined files
base_path = "/Users/sarahdaniels/Documents/grant_categorization/combined_categories"
files = [f for f in os.listdir(base_path) if f.endswith('_combined.csv')]

results = {}
all_classifications = []

for filename in sorted(files):
    filepath = os.path.join(base_path, filename)
    disease = filename.replace("_combined.csv", "").replace("_", " ")
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        disease_counts = Counter()
        
        for row in reader:
            tag = get_tag(row)
            if 'Mechanistic' in tag:
                title = get_title(row)
                subcat = classify_grant(title)
                disease_counts[subcat] += 1
                all_classifications.append({
                    'disease': disease,
                    'title': title,
                    'subcategory': subcat
                })
        
        results[disease] = disease_counts

# Print summary
print("=" * 80)
print("MECHANISTIC SUBCATEGORY DISTRIBUTION BY DISEASE")
print("=" * 80)

all_counts = Counter()
for disease, counts in sorted(results.items()):
    total = sum(counts.values())
    print(f"\n{disease} ({total} grants):")
    for cat, count in counts.most_common():
        pct = 100 * count / total if total > 0 else 0
        print(f"  {cat:20s}: {count:4d} ({pct:5.1f}%)")
        all_counts[cat] += count

print("\n" + "=" * 80)
print("OVERALL DISTRIBUTION") 
print("=" * 80)
total = sum(all_counts.values())
for cat, count in all_counts.most_common():
    pct = 100 * count / total
    print(f"  {cat:20s}: {count:5d} ({pct:5.1f}%)")

print(f"\n  TOTAL: {total}")

# Show "Other" examples
print("\n" + "=" * 80)
print("SAMPLE 'OTHER' GRANTS (to refine patterns)")
print("=" * 80)
other_grants = [g for g in all_classifications if g['subcategory'] == 'Other' and g['title']]
for g in other_grants[:25]:
    print(f"[{g['disease'][:12]:12s}] {g['title'][:65]}")

# Show more detailed "Other" breakdown by disease
print("\n" + "=" * 80)
print("'OTHER' SAMPLES BY DISEASE AREA")
print("=" * 80)

for disease in ["Contraception Reproduction", "Biodefense", "Liver Disease"]:
    disease_others = [g for g in all_classifications if g['subcategory'] == 'Other' and disease in g['disease'] and g['title']][:10]
    print(f"\n{disease}:")
    for g in disease_others:
        print(f"  - {g['title'][:70]}")
