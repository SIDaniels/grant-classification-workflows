import re
import csv
import os
import json
from collections import Counter, defaultdict

# IMPROVED Clinical/Everything_else subcategory patterns (v4)
patterns = {
    "Clinical Trials/Drug Dev": [
        r"phase [I1-4]+", r"phase \d", r"placebo", r"\bRCT\b", r"randomized",
        r"clinical trial", r"clinical study", r"pilot study", r"pilot trial",
        r"drug trial", r"therapeutic(?!.*target)", r"treatment trial",
        r"preclinical", r"lead optimization", r"drug develop", r"drug discovery",
        r"\binhibitor\b", r"agonist", r"antagonist",
        r"dosing", r"dose.?escalation", r"pharmacokinetic", r"efficacy trial",
        r"neoadjuvant", r"adjuvant therap",
        r"transplant", r"allograft", r"xenotransplant", r"graft",
        r"therapy for", r"treatment of", r"treatment for",
        r"first.?in.?human", r"safety study", r"tolerability",
        # v4 additions
        r"novel therap", r"novel treatment", r"new therap",
        r"chemotherapy", r"chemoprevent", r"immunotherapy(?!.*mechan)",
        r"targeted therapy", r"combination therapy"
    ],
    "Behavioral/Lifestyle": [
        r"behavio", r"lifestyle", r"exercise", r"physical activity", r"fitness",
        r"nutrition intervention", r"weight loss", r"weight management",
        r"smoking cessation", r"quit smoking", r"tobacco treatment",
        r"counseling", r"psychosocial", r"cognitive behavio", r"mindfulness",
        r"adherence", r"self.?management", r"self.?help", r"motivat",
        r"community.?based(?!.*trial)", r"peer", r"social support",
        r"survivorship", r"quality of life", r"patient.?report",
        r"prenatal care", r"maternal care", r"palliative",
        r"caregiver", r"family support", r"patient education",
        r"smoke.?free", r"healthy home", r"intervention program",
        # v4 additions
        r"survivor", r"distress", r"anxiety", r"depression",
        r"insomnia", r"sleep", r"fatigue", r"pain management",
        r"cognitive function", r"neurocognitive", r"well.?being"
    ],
    "Screening/Detection": [
        r"screen(?!ing marker)", r"early detection", r"early diagnosis",
        r"risk assessment", r"risk prediction", r"risk stratification",
        r"imaging(?!.*immun)", r"\bPET\b", r"\bMRI\b", r"\bCT scan",
        r"endoscop", r"colonoscop", r"mammogra", r"ultrasound",
        r"diagnostic(?!.*marker)", r"biomarker(?!.*develop)",
        r"tomosynthesis", r"radiomics?", r"liquid biops",
        r"elastography", r"tomography", r"spectroscop",
        r"point.?of.?care", r"\bPOC\b", r"rapid detection",
        r"biosensor", r"assay develop",
        # v4 additions
        r"monitoring.*therapy", r"therapy response", r"response to",
        r"characteriz.*cancer", r"high.?risk", r"density"
    ],
    "Epidemiology/Population": [
        r"epidemiol", r"\bcohort\b", r"population.?based", r"longitudinal study",
        r"incidence", r"prevalence", r"risk factor(?!.*screen)",
        r"etiology", r"registry", r"database study",
        r"geospatial", r"geographic", r"trends", r"surveillance study",
        r"natural history", r"outcomes research",
        r"never smoker", r"non.?smoker", r"case.?control",
        r"prospective study", r"retrospective", r"life.?course",
        r"birth outcome", r"pregnancy outcome",
        # v4 additions
        r"patient outcome", r"long.?term outcome", r"survival outcome",
        r"social network", r"built environment", r"environmental exposure"
    ],
    "Health Disparities/Access": [
        r"disparit", r"equit", r"inequit", r"underserved", r"minority health",
        r"health access", r"social determinant", r"socioeconomic",
        r"rural health", r"urban health", r"immigrant", r"african.?american",
        r"latino", r"hispanic", r"indigenous", r"native american",
        r"low.?income", r"uninsured", r"safety net", r"vulnerable",
        r"cultural", r"community health",
        # Added patterns
        r"communication modalit", r"returning.*results", r"genetic counseling",
        r"health literacy", r"patient.?provider", r"shared decision"
    ],
    "Training/Infrastructure": [
        r"\bcore\b", r"administrative", r"resource center", r"biobank", r"repository",
        r"consortium", r"network(?!.*neural)", r"center(?!.*disease)",
        r"clinical trials unit", r"\bCTU\b", r"coordinating center",
        r"training", r"mentor", r"career", r"fellowship", r"K\d\d\b", r"T32",
        r"loan repayment", r"scholar", r"pilot.*program", r"feasibility.*program",
        r"reference lab", r"bioinformatics resource", r"data.?sharing",
        # Added patterns
        r"community outreach", r"stakeholder", r"engagement",
        r"cancer control", r"cancer prevention", r"prevention program",
        r"leadership", r"\bSDMC\b", r"coordinating", r"IMPAACT",
        r"research program", r"shared resource"
    ],
    "Technology/Methods": [
        r"novel method", r"new method", r"novel approach", r"new approach",
        r"nanomedicine", r"nanoparticle", r"gene therapy",
        r"cell therapy", r"stem cell therap", r"iPSC", r"autologous cell",
        r"deep brain stimulation", r"\bDBS\b", r"neuromodulation",
        r"machine learning", r"artificial intelligence", r"\bAI\b",
        r"bioinformatic", r"computational model", r"mathematical model",
        r"sensor", r"device", r"wearable", r"mobile health", r"mHealth",
        r"decision.?tool", r"decision.?support",
        # Added patterns
        r"systems biology", r"statistical method", r"modeling",
        r"algorithm", r"software", r"platform",
        r"gene delivery", r"mRNA", r"nonviral", r"viral vector",
        r"preservation", r"cryopreserv", r"organ preserv",
        r"engineering", r"bioengineering", r"tissue engineer",
        r"\bEHR\b", r"electronic health record", r"smart"
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
            if 'Everything_else' in tag:
                title = get_title(row)
                amount = get_amount(row)
                subcat = classify_grant(title)
                disease_counts[subcat] += 1
                disease_dollars[subcat] += amount
        
        results_counts[disease] = dict(disease_counts)
        results_dollars[disease] = dict(disease_dollars)

# Print summary
print("=" * 90)
print("CLINICAL & OTHER SUBCATEGORY DISTRIBUTION (v2 - improved patterns)")
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

print("\n" + "=" * 90)
print("OVERALL DISTRIBUTION")
print("=" * 90)
total = sum(all_counts.values())
total_dollars = sum(all_dollars.values())
for cat in sorted(all_counts.keys(), key=lambda x: all_counts[x], reverse=True):
    count = all_counts[cat]
    dollar = all_dollars[cat]
    pct = 100 * count / total
    print(f"  {cat:24s}: {count:5d} ({pct:5.1f}%)  ${dollar/1e6:8.1f}M")

print(f"\n  TOTAL: {total} grants, ${total_dollars/1e6:.1f}M")
print(f"  'Other' rate: {100*all_counts['Other']/total:.1f}%")

# Export for visualization
export_data = {"by_disease": {}, "totals": dict(all_dollars)}
for disease in results_dollars:
    export_data["by_disease"][disease] = results_dollars[disease]

with open("/Users/sarahdaniels/Documents/grant_categorization/clinical_subfields.json", "w") as f:
    json.dump(export_data, f, indent=2)

print("\nExported to clinical_subfields.json")
