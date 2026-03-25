# Grant Classification Workflow

You are a grant classification expert. For each grant, read the title and terms carefully and classify using the decision tree below.

## Input
CSV file: $ARGUMENTS
Required columns: PROJECT_TITLE, PROJECT_TERMS (or Abstract)

## Classification Process

For EACH grant, apply this decision tree IN ORDER:

### Step 1: Infrastructure/Administrative?
If the grant is for cores, training, conferences, administrative supplements → **Everything_else**

### Step 2: Clinical Intervention?
If testing a treatment, running a clinical trial, behavioral intervention, cessation program → **Everything_else**

### Step 3: Environmental Exposure Focus?
Is the PRIMARY FOCUS on an environmental exposure or its effects?
- Microbiome/gut bacteria as exposure (even if studying mechanisms)
- Obesity/diet as risk factor or exposure
- PFAS, chemicals, pesticides, air pollution
- Smoking/tobacco/vaping as exposure
- Gene-environment interactions
- Prenatal/in utero exposures

If YES → **Strictly_Environmental_or_Gene-Environment**

### Step 4: Molecular/Cellular Mechanism?
Is the PRIMARY FOCUS on understanding HOW something works at molecular/cellular level?
- Studying protein function, signaling pathways
- "Role of [protein] in..."
- Drug resistance mechanisms
- Metastasis, EMT, ferroptosis, autophagy
- Tumor microenvironment biology
- DNA repair mechanisms

If YES → **Mechanistic_Pathogenesis**

### Step 5: Pure Genetic Risk?
GWAS, germline mutations, hereditary syndromes, genetic risk (WITHOUT studying function) → **Strictly_Genetic**

### Step 6: Default
Everything else → **Everything_else**

## Critical Distinctions

| Scenario | Category |
|----------|----------|
| "Role of obesity in tumor progression" (studying mechanism) | Mechanistic |
| "Obesity as risk factor for breast cancer" (exposure focus) | Environmental |
| "Microbiome effects on cancer" (any microbiome study) | Environmental |
| "KRAS mutation function" (studying mechanism) | Mechanistic |
| "KRAS mutations and cancer risk" (genetic risk) | Genetic |
| "Testing microbiome intervention" (clinical trial) | Everything_else |

## Output Format

Create a CSV with:
- All original columns
- Category: one of the four categories
- Environmental_Subgroup: (if Environmental) one of: Smoking, Chemicals, Microbiome, Diet_Obesity_Nutrition, Alcohol, Infection, Radiation, Gene_Environment, Circadian_Sleep, Other
- Confidence: High/Medium/Low
- Rationale: Brief reason for classification

## Batch Processing

1. Load the input CSV
2. For each grant:
   - Read title and terms
   - Apply decision tree
   - Assign category and rationale
3. Save classified CSV
4. Generate summary statistics
5. Flag Low confidence grants for manual review

## Important Notes

- When in doubt between Environmental and Mechanistic, ask: "Is the EXPOSURE the focus, or is the MECHANISM the focus?"
- Microbiome is ALWAYS Environmental per project rules, even when studying mechanisms
- Interventions testing treatments are ALWAYS Everything_else, even if studying mechanisms
