import re
import csv
import os
from collections import Counter

# Clinical context patterns - if these appear, the grant is probably Clinical, not Mechanistic
clinical_context = [
    r"behavioral therapy", r"dialectical", r"counseling", r"quality of life",
    r"self-management", r"mindfulness", r"coping", r"psychosocial",
    r"palliative care", r"caregiver", r"patient-reported", r"adherence",
    r"health literacy", r"survivorship", r"navigator", r"support group",
    r"exercise intervention", r"physical activity intervention",
    r"cognitive behavioral", r"anxiety in", r"depression in",
    r"augmented reality", r"virtual reality.*training", r"telemedicine",
    # Added to prevent false positives
    r"care pathway", r"policy pathway", r"treatment pathway",
    r"molecular epidemiol", r"epidemiolog", r"population.?based",
    r"patient outcome", r"clinical outcome", r"health outcome",
    r"shared decision", r"patient education", r"health disparit",
    r"community.?based", r"implementation science", r"dissemination",
    r"\bcore\b", r"administrative core", r"coordinating center",
]

# Strong mechanistic keywords - these indicate true mechanistic research
# Organized by subcategory with more specific patterns
mechanistic_keywords = [
    # Neurodegeneration - mechanism-focused, not patient interventions
    (r"alpha.?synuclein", "synuclein"),
    (r"\bsynuclein\b", "synuclein"),
    (r"lewy bod", "lewy"),
    (r"motor neuron disease|motor neuron degeneration", "motor neuron"),
    (r"dopaminergic neuron", "dopaminergic"),
    (r"TDP-?43", "TDP-43"),
    (r"C9orf72", "C9orf72"),
    (r"amyloid.?(beta|plaque|aggregat|pathol)", "amyloid"),
    (r"tauopathy|tau aggregat|tau phosphoryl", "tauopathy"),
    (r"protein aggregat", "aggregation"),
    (r"neuroprotect\w+ (mechanism|pathway|strateg)", "neuroprotection"),
    (r"proteinopathy", "proteinopathy"),

    # Tumor Biology - mechanism-focused
    (r"tumor (microenviron|suppress|progress|initiat|heterogen)", "tumor"),
    (r"tumor-?stroma", "tumor"),
    (r"tumour", "tumour"),
    (r"metasta\w+ (mechan|pathway|process|cascade|coloniz)", "metastasis"),
    (r"oncogen\w+ (signal|driv|transform|activ)", "oncogene"),
    (r"carcinogen\w+ (mechan|pathway|induc)", "carcinogenesis"),
    (r"angiogenesis", "angiogenesis"),
    (r"\bEMT\b", "EMT"),
    (r"cancer cell (migrat|invas|proliferat|signal|metabol)", "cancer cell"),
    (r"tumor.?suppress", "tumor suppressor"),

    # Immune/Inflammatory - mechanism-focused
    (r"immun\w+ (response|pathway|mechan|signal|regulat|evasion)", "immune"),
    (r"inflammat\w+ (pathway|signal|mechan|response|mediator)", "inflammatory"),
    (r"cytokine (signal|storm|releas|product|network)", "cytokine"),
    (r"\bT.?cell (exhaust|dysfunct|signal|activ|receptor|response)", "T-cell"),
    (r"macrophage (polariz|activ|infiltrat|signal|phenotype)", "macrophage"),
    (r"neutrophil (infiltrat|extracellular|recruit|function)", "neutrophil"),
    (r"antibod\w+ (engineer|therap|develop|target)", "antibody"),
    (r"interferon (signal|pathway|response|induc)", "interferon"),
    (r"checkpoint inhibit", "checkpoint"),
    (r"\bCAR[- ]?T\b", "CAR-T"),  # Require word boundary or hyphen, not just CART
    (r"immunotherapy mechan", "immunotherapy"),

    # Microbial Pathogenesis
    (r"pathogen (evolut|adapt|virulence|host)", "pathogen"),
    (r"virulence (factor|mechan|gene|regulat)", "virulence"),
    (r"viral (replicat|entry|assembly|pathogen)", "viral"),
    (r"host.?pathogen (interact|interface|dynamic)", "host-pathogen"),

    # Genetics/Genomics - mechanism-focused
    (r"genom\w+ (instabil|integr|edit|regulat|variat)", "genomic"),
    (r"epigenet\w+ (regulat|modif|mechan|reprogram)", "epigenetic"),
    (r"transcriptom\w+ (regulat|analys|profil|dysregulat)", "transcriptomic"),
    (r"CRISPR", "CRISPR"),
    (r"gene expression (regulat|reprogram|control|dysregulat)", "gene expression"),
    (r"chromatin (remodel|modif|regulat|access)", "chromatin"),

    # Metabolic
    (r"mitochondri\w+ (dysfunct|biogen|metabol|DNA|signal)", "mitochondrial"),
    (r"glycoly\w+ (pathway|switch|regulat|metabol)", "glycolysis"),
    (r"oxidative stress (mechan|pathway|induc|response)", "oxidative stress"),
    (r"ferroptosis", "ferroptosis"),

    # Reproductive/Developmental - mechanism-focused
    (r"embryo\w+ (develop|pattern|signal|morphogen)", "embryonic"),
    (r"oocyte (matur|quality|develop|aging)", "oocyte"),
    (r"meiosis|meiotic", "meiosis"),
    (r"gametogen", "gametogenesis"),
    (r"fetal (develop|program|growth)", "fetal development"),

    # Additional molecular/cellular mechanisms (with context)
    (r"transcriptional regulat", "transcriptional"),
    (r"post.?transcription", "transcriptional"),
    (r"spliced? isoform", "splicing"),
    (r"RNA.?binding protein", "RNA-binding"),
    (r"molecular (mechanism|pathway|basis)", "molecular"),
    (r"signal(ing|ling) pathway", "signaling"),
    (r"stem.?like phenotype", "stem-like"),
    (r"mammary gland develop", "developmental"),
    (r"ion channel regulat", "ion channel"),
    (r"mitophagy", "mitophagy"),

    # Specific kinases and genes - added from spot check
    (r"LRRK2|leucine.?rich repeat kinase", "LRRK2"),
    (r"\bBMP\b.*(signal|pathway|role)", "BMP signaling"),
    (r"\bFGF\b.*(signal|pathway|role)", "FGF signaling"),
    (r"\bWnt\b.*(signal|pathway)", "Wnt signaling"),
    (r"\bNotch\b.*(signal|pathway)", "Notch signaling"),
    (r"APOBEC3", "APOBEC3"),
    (r"extracellular matrix.*(invas|metasta|remodel|degrad)", "ECM"),
    (r"(invas|metasta).*extracellular matrix", "ECM"),
    (r"\bkinase\b.*(signal|pathway|phosphoryl|activ)", "kinase"),
    (r"receptor.?tyrosine kinase", "RTK"),
    (r"protein kinase", "kinase"),
    (r"cell cycle (regulat|checkpoint|control|arrest)", "cell cycle"),
    (r"apoptosis|apoptotic (pathway|signal|mechan)", "apoptosis"),
    (r"autophagy", "autophagy"),
    (r"DNA damage (response|repair|signal)", "DNA damage"),
    (r"DNA repair (mechan|pathway)", "DNA repair"),
    (r"ubiquitin", "ubiquitin"),
    (r"proteasome", "proteasome"),
    (r"endoplasmic reticulum stress", "ER stress"),
    (r"\bUPR\b|unfolded protein response", "UPR"),
    (r"cellular senescence", "senescence"),
    (r"cell death (mechan|pathway)", "cell death"),
    (r"necroptosis", "necroptosis"),
    (r"pyroptosis", "pyroptosis"),
]

def has_clinical_context(title):
    """Check if title has clinical/behavioral context that overrides mechanistic keywords"""
    title_lower = title.lower()
    for pattern in clinical_context:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return True
    return False

def should_be_mechanistic(title):
    """Check if a title has strong mechanistic keywords without clinical context"""
    # First check for clinical context that would disqualify
    if has_clinical_context(title):
        return False, []

    title_lower = title.lower()
    matches = []
    for pattern, label in mechanistic_keywords:
        if re.search(pattern, title_lower, re.IGNORECASE):
            matches.append(label)

    # Require at least 1 strong match
    return len(matches) >= 1, matches

# Process each file
base_path = "/Users/sarahdaniels/Documents/grant_categorization/combined_categories"
files = [f for f in os.listdir(base_path) if f.endswith('_combined.csv')]

total_fixed = 0
fixes_by_disease = Counter()
all_fixes = []

for filename in sorted(files):
    filepath = os.path.join(base_path, filename)
    disease = filename.replace("_combined.csv", "").replace("_", " ")

    rows = []
    fieldnames = None
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    if 'Fix_Applied' not in fieldnames:
        fieldnames = list(fieldnames) + ['Fix_Applied']

    fixed_count = 0
    for row in rows:
        tag_key = 'Combined_Tag' if 'Combined_Tag' in row else 'Tag'
        if 'Everything_else' in row.get(tag_key, ''):
            title = row.get('Project_Title', row.get('Project Title', ''))
            should_fix, matches = should_be_mechanistic(title)
            if should_fix:
                row[tag_key] = 'Mechanistic_and_Genetic'
                row['Fix_Applied'] = f'Moved from Everything_else (matched: {matches[0]})'
                fixed_count += 1
                all_fixes.append((disease, title, matches[0]))

    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    if fixed_count > 0:
        print(f"{disease}: Fixed {fixed_count} grants")
        total_fixed += fixed_count
        fixes_by_disease[disease] = fixed_count

print(f"\nTotal fixed: {total_fixed} grants moved to Mechanistic")

# Show summary by keyword
print("\n" + "=" * 60)
print("SUMMARY BY MATCHING KEYWORD")
print("=" * 60)
keywords = Counter(f[2] for f in all_fixes)
for kw, count in keywords.most_common(15):
    print(f"  {kw:25s}: {count:4d} grants")
