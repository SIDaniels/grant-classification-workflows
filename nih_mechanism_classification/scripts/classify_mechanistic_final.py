import re
import csv
import os
import json
from collections import Counter, defaultdict

# REFINED keyword patterns - v3
# Key fixes:
# 1. Removed disease names from Neurodegeneration (parkinson, alzheimer, ALS)
# 2. Added "vaccine" to Immune/Inflammatory
# 3. Added neuroinflammation terms to Immune

patterns = {
    "Neurodegeneration": [
        r"neurodegen", r"neuroprotect", r"neuronal death", r"neuronal loss",
        r"dopaminergic", r"alpha.?synuclein", r"synuclein", r"lewy", r"motor neuron",
        r"striatal", r"basal ganglia", r"substantia nigra",
        r"cortical circuit", r"tauopathy",
        r"aggregat", r"misfolded protein", r"proteino?pathy",
        r"TDP-?43", r"C9orf72", r"FUS\b", r"SOD1", r"frontotemporal",
        r"ataxin", r"polyglutamine", r"amyloid", r"plaque"
    ],
    "Tumor Biology": [
        r"tumor", r"tumour", r"cancer", r"metasta", r"carcinogen", r"oncogene", 
        r"carcinoma", r"adenocarcinoma", r"malignant", r"neoplasm", r"neoplastic",
        r"angiogenesis", r"epithelial.?mesenchymal", r"\bEMT\b", 
        r"\bKRAS\b", r"\bEGFR\b", r"chemoresist", r"drug.?resist", r"radioresist",
        r"cancer stem", r"tumor.?suppress", r"sarcoma", r"lymphoma", r"melanoma",
        r"hepatocellular", r"glioma", r"glioblastoma"
    ],
    "Immune/Inflammatory": [
        r"immun", r"inflammat", r"neuroinflam", r"cytokine", r"interleukin", r"\bIL-\d+", 
        r"\bT.?cell", r"\bB.?cell", r"macrophage", r"neutrophil", r"lymphocyte",
        r"antibod", r"autoimmun", r"interferon", r"chemokine", r"\bCXCL", r"\bCCL\d",
        r"checkpoint", r"\bPD-?1\b", r"\bPD-?L1\b", r"\bCD\d+", 
        r"oncolytic", r"CAR-?T", r"dendritic", r"innate immun", r"adaptive immun",
        r"microglia", r"astrocyte", r"glial", r"myeloid", r"inflammasome", r"NK cell",
        r"vaccine", r"vaccin", r"adjuvant"  # ADDED: vaccine-related terms
    ],
    "Microbial Pathogenesis": [
        r"pathogen", r"virul", r"bacteri", r"viral", r"\bvirus\b", 
        r"infect(?!ion.*immun)", r"antimicrobial", r"antibiotic",
        r"tuberculosis", r"\bTB\b", r"malaria", r"\bHIV\b", r"hepatitis",
        r"SARS", r"COVID", r"coronavirus", r"influenza", r"ebola", r"zika",
        r"host.?pathogen", r"microbial", r"parasite", r"fungal",
        r"biofilm", r"secretion system", r"effector protein"
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
        r"energy metabolism", r"lipogenesis", r"ketone", r"gluconeogenesis",
        r"obesity", r"steatosis", r"NAFLD", r"NASH"
    ],
    "Reproductive/Developmental": [
        r"ovar", r"uter", r"placenta", r"embryo", r"fetal", r"fetus",
        r"pregnan", r"fertility", r"infertility", r"sperm", r"oocyte",
        r"meiosis", r"meiotic", r"gametogen", r"fertilization",
        r"decidual", r"endometri", r"preterm", r"gestation",
        r"reproductive", r"contracepti", r"menstrual", r"follicle",
        r"trophoblast", r"implantation"
    ],
    "Biomarkers": [
        r"biomarker", r"diagnostic marker", r"prognostic marker", r"early detection",
        r"liquid biops", r"circulating tumor", r"cell.?free DNA", r"\bctDNA\b",
        r"biosensor", r"screening marker"
    ]
}

def classify_grant(title, disease_area=""):
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
        # Default based on disease area if no keywords match
        if disease_area in ["ALS", "Parkinsons", "Parkinson's"]:
            return "Neurodegeneration"
        return "Other"
    
    return max(scores.items(), key=lambda x: x[1])[0]

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

# Process all files
base_path = "/Users/sarahdaniels/Documents/grant_categorization/combined_categories"
files = [f for f in os.listdir(base_path) if f.endswith('_combined.csv')]

results_counts = {}
results_dollars = {}

for filename in sorted(files):
    filepath = os.path.join(base_path, filename)
    disease = filename.replace("_combined.csv", "").replace("_", " ")
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        disease_counts = Counter()
        disease_dollars = defaultdict(float)
        
        for row in reader:
            tag = get_tag(row)
            if 'Mechanistic' in tag:
                title = get_title(row)
                amount = get_amount(row)
                subcat = classify_grant(title, disease)
                disease_counts[subcat] += 1
                disease_dollars[subcat] += amount
        
        results_counts[disease] = dict(disease_counts)
        results_dollars[disease] = dict(disease_dollars)

# Print summary
print("=" * 90)
print("MECHANISTIC SUBCATEGORY DISTRIBUTION (v3 - with vaccine fix)")
print("=" * 90)

all_counts = Counter()
all_dollars = defaultdict(float)

for disease in sorted(results_counts.keys()):
    counts = results_counts[disease]
    dollars = results_dollars[disease]
    total_grants = sum(counts.values())
    total_dollars = sum(dollars.values())
    
    print(f"\n{disease} ({total_grants} grants, ${total_dollars/1e6:.1f}M):")
    
    for cat in sorted(counts.keys(), key=lambda x: counts[x], reverse=True):
        count = counts[cat]
        dollar = dollars.get(cat, 0)
        pct = 100 * count / total_grants if total_grants > 0 else 0
        print(f"  {cat:24s}: {count:4d} ({pct:5.1f}%)  ${dollar/1e6:7.1f}M")
        all_counts[cat] += count
        all_dollars[cat] += dollar

print(f"\n'Other' rate: {100*all_counts['Other']/sum(all_counts.values()):.1f}%")

# Export for visualization
export_data = {"by_disease": {}, "totals": dict(all_dollars)}
for disease in results_dollars:
    export_data["by_disease"][disease] = results_dollars[disease]

with open("/Users/sarahdaniels/Documents/grant_categorization/mechanistic_subfields.json", "w") as f:
    json.dump(export_data, f, indent=2)

print("\nExported to mechanistic_subfields.json")
