# Environmental Exposure Classification Methodology

## Overview

This document describes the process used to classify NIH grants into Environmental Exposure research vs. other categories. The goal is to identify grants studying environmental factors (chemicals, lifestyle, microbiome, etc.) as **risk factors for disease**, distinct from mechanistic research or interventions.

## Classification Categories

| Category | Code | Description |
|----------|------|-------------|
| Environmental Exposure | ENV | Studies environmental factors as RISK FACTORS for disease outcomes |
| Not Environmental | NOT | Mechanisms, genetics, interventions, treatments, infrastructure, training |

## Environmental Subgroups

| Subgroup | Description | Examples |
|----------|-------------|----------|
| Chemicals | Pollutants, toxicants, drugs | PFAS, pesticides, dioxins, air pollution, heavy metals |
| Smoking | Tobacco, nicotine, e-cigarettes | Cigarette smoke exposure, secondhand smoke, vaping |
| Diet_Obesity_Nutrition | Dietary factors, obesity as risk | High-fat diet, fructose, caloric intake, nutritional deficiencies |
| Alcohol | Alcohol consumption as risk | Binge drinking, chronic alcohol use, fetal alcohol |
| Microbiome | Microbial communities as disease modifiers | Gut microbiome dysbiosis, skin microbiome, oral microbiome |
| Infection | Infectious agents as disease risk | Viral hepatitis → cancer, H. pylori → gastric cancer |
| Radiation | Ionizing/non-ionizing radiation | UV exposure, radon, radiation therapy side effects |
| Gene_Environment | Gene-environment interactions | Genetic susceptibility to environmental toxicants |
| Other | Other environmental factors | Stress, noise, housing conditions |

## Classification Criteria (Refined v2)

### ENV - Include grants that:

1. **Study exposure → disease/health outcome relationships**
   - Epidemiological studies of environmental exposures
   - Cohort studies tracking exposure and disease incidence
   - Case-control studies of environmental risk factors

2. **Measure environmental exposures as independent variables**
   - Biomonitoring of chemical exposures
   - Assessment of dietary patterns and disease risk
   - Microbiome composition associated with health outcomes

3. **Investigate exposure-related biological effects (upstream of mechanism)**
   - DNA damage from environmental toxicants
   - Epigenetic changes from early-life exposures
   - Microbiome alterations from diet/antibiotics

### NOT - Exclude grants that:

1. **Study molecular mechanisms without exposure context**
   - Pure cell biology or biochemistry
   - Protein structure/function studies
   - Genetic pathway analysis
   - ❌ "JNK targets in hepatotoxicity" - mechanism study
   - ❌ "LPCAT3 in adipose remodeling" - mechanism study

2. **Develop or test interventions/treatments**
   - Smoking cessation programs (intervention, not exposure study)
   - Weight loss trials (intervention)
   - Probiotic supplementation trials (intervention)
   - ❌ "Culturally-Tailored Smoking Cessation Intervention" - intervention
   - ❌ "Role of probiotic L. reuteri in anti-tumor immunity" - intervention

3. **Administrative, training, or infrastructure grants**
   - Conference/symposium grants
   - Training grants (T32, K awards)
   - Core facilities
   - ❌ "Division of Chemical Toxicology Symposia" - conference
   - ❌ "Leadership, Planning and Evaluation" - administrative

4. **Study disease mechanisms in exposure-induced models**
   - Using alcohol model to study liver fibrosis mechanisms
   - Using HFD mice to study metabolic pathways
   - ❌ "Role of alcohol-adapted Kupffer cells" - mechanism using alcohol model

5. **Drug development or therapeutic studies**
   - Preclinical drug testing
   - Treatment cardiotoxicity (studying drug as treatment, not exposure)
   - ❌ "Novel therapeutics for obesity" - treatment development

## Key Distinctions

### Exposure Study vs. Mechanism Study

| ENV (Exposure Study) | NOT (Mechanism Study) |
|---------------------|----------------------|
| "Air pollution and children's asthma risk" | "Inflammatory pathways in asthma" |
| "Alcohol consumption and breast cancer incidence" | "How alcohol activates oncogenic pathways" |
| "Gut microbiome composition in IBD patients" | "Microbial metabolites activate immune cells" |
| "Pesticide exposure and Parkinson's risk" | "Alpha-synuclein aggregation mechanisms" |

### Exposure Study vs. Intervention Study

| ENV (Exposure Study) | NOT (Intervention Study) |
|---------------------|-------------------------|
| "Smoking and lung cancer risk" | "Smoking cessation trial" |
| "Diet patterns and diabetes risk" | "Weight loss intervention efficacy" |
| "Microbiome dysbiosis in disease" | "Probiotic supplementation trial" |

## Classification Method

### Approach: LLM Classification with Claude Haiku

Due to high volume (29,373 candidates), regex classification was replaced with LLM-based classification using Claude Haiku for accuracy.

### Prompt Template (v2 - Refined)

```
Classify each grant as "ENV" or "NOT":

ENV = Studies environmental exposures as RISK FACTORS for disease:
  - Epidemiology of chemical/pollution/smoking/diet/microbiome exposures
  - Exposure-disease relationship studies
  - Biomonitoring and exposure assessment
  - Gene-environment interactions

NOT = Everything else, including:
  - Molecular mechanisms (even if exposure-related model)
  - Interventions and treatments (cessation programs, weight loss, probiotics)
  - Administrative/conference/training grants
  - Drug development and therapeutics
  - Pure genetics without environmental component

Key test: Is the PRIMARY FOCUS on measuring/understanding an environmental EXPOSURE and its relationship to health, or is it about mechanisms/treatments/infrastructure?

Examples:
- "Alcohol and breast cancer risk in women" → ENV (exposure-outcome study)
- "Mechanisms of alcohol-induced liver fibrosis" → NOT (mechanism study)
- "Smoking cessation intervention for veterans" → NOT (intervention)
- "PFAS exposure and thyroid disease" → ENV (exposure-outcome study)
- "Annual Conference on Chemical Toxicology" → NOT (conference)

Return ONLY a JSON object: {"grant_id": "ENV" or "NOT", ...}
```

## Validation Results

### Quality Check (n=20 random sample)

| Category | Correct | Borderline | Wrong |
|----------|---------|------------|-------|
| ENV (10) | 7 | 2 | 1 |
| NOT (10) | 8 | 2 | 0 |
| **Total** | **75%** | **20%** | **5%** |

### Common Errors Found

1. **Conference/symposium grants classified as ENV** - Fixed by adding explicit exclusion in prompt
2. **Intervention studies classified as ENV** - Fixed by emphasizing cessation/treatment exclusion
3. **Mechanism studies using exposure models classified as ENV** - Fixed by clarifying "mechanism using model" vs "exposure study"

## Process

### Step 1: Initial Candidate Selection (Regex)
Used broad keyword matching to identify 29,373 potential environmental grants from 500K+ total grants.

### Step 2: Batch Preparation
Created 588 batch files (50 grants each) with APPLICATION_ID, PROJECT_TITLE, and PROJECT_TERMS.

### Step 3: LLM Classification
Processed batches using Claude Haiku subagents (5 parallel batches at a time).

### Step 4: Quality Verification
Sampled classified grants to verify accuracy and refine criteria.

### Step 5: Output Generation
Generated final CSV/JSON with confirmed environmental grants and subgroup assignments.

## Final Results (100% Complete)

| Metric | Value |
|--------|-------|
| Grants Classified | 29,331 |
| ENV | 8,444 (28.8%) |
| NOT | 20,887 (71.2%) |

### Funding by Subgroup

| Subgroup | Grants | Funding |
|----------|--------|---------|
| Chemicals | 1,113 | $609M |
| Microbiome | 1,037 | $465M |
| Diet/Obesity/Nutrition | 921 | $453M |
| Smoking | 470 | $279M |
| Alcohol | 356 | $134M |
| Other | 178 | $116M |
| Gene-Environment | 45 | $31M |
| Infection | 57 | $24M |
| Radiation | 39 | $21M |

## Files Generated

- `haiku_classifications.json` - Raw classification results
- `environmental_grants_classified.csv` - Confirmed ENV grants with details
- `environmental_grants_classified.json` - Same in JSON format
- `env_grant_ids.json` - List of ENV grant IDs
- `classification_batches/batch_*.json` - Input batch files

## Limitations

1. **Subgroup assignment from regex, not LLM** - Subgroups were pre-assigned during candidate selection, not verified by LLM
2. **Title/terms only** - Classification based on title and project terms, not full abstract
3. **Single-label** - Each grant gets one classification; some may span categories
4. **Partial completion** - 42% of candidates classified; full dataset would be more representative

## Exposure → Mechanism of Harm Mapping

### Overview

Secondary analysis mapping environmental exposures to molecular mechanisms of harm (rather than disease outcomes). Uses PHR (Public Health Relevance) abstracts and PROJECT_TERMS for mechanism detection.

### Data Source

- **Total ENV Grants**: 8,735 (FY2022-2025)
- **Grants with identifiable exposure-mechanism links**: 6,281 (72%)
- **Data fields used**: PROJECT_TITLE, PHR, PROJECT_TERMS

### Exposure Categories

Exposures organized into two groups with vertical separation in visualization:

**Chemical Exposures (9 categories)**

| Category | Grants | Keywords |
|----------|--------|----------|
| Heavy_Metals | 2,347 | arsenic, lead, cadmium, mercury, chromium, manganese, nickel, fluoride, nitrate |
| Air_Pollution | 1,087 | PM2.5, ozone, diesel, wildfire smoke, ultrafine particles |
| Radiation | 606 | UV, radon, ionizing, radioactive |
| PAHs_Dioxins_PCBs | 286 | polycyclic aromatic, benzo[a]pyrene, dioxin, PCB, TCDD |
| Pesticides | 279 | organophosphate, glyphosate, chlorpyrifos, DDT |
| PFAS | 265 | PFOA, PFOS, perfluorinated, forever chemicals |
| Phthalates_BPA | 174 | bisphenol, plasticizer, TBBPA |
| Solvents | 160 | TCE, benzene, toluene, formaldehyde |
| Flame_Retardants | 96 | PBDE, polybrominated, organohalogen |

**Lifestyle/Biological Exposures (7 categories)**

| Category | Grants | Keywords |
|----------|--------|----------|
| Diet_Nutrition | 4,085 | obesity, fasting, vitamin, nutrient, high-fat diet |
| Tobacco_Smoke | 1,708 | cigarette, nicotine, vaping, e-cigarette |
| Viral_Infection | 1,649 | HIV, HCV, influenza, COVID |
| Alcohol | 1,641 | ethanol, drinking, alcoholism |
| Bacterial_Infection | 1,608 | tuberculosis, H. pylori, microbiome |
| Drugs_Medications | 1,220 | opioid, pharmaceutical, cannabis |
| Hypoxia | 215 | low oxygen, ischemia |

**Excluded from analysis**: Psychosocial_Stress, Noise, Sleep_Circadian (lifestyle factors without clear molecular mechanisms)

### Mechanisms of Harm (16 categories)

| Mechanism | Grants | Description |
|-----------|--------|-------------|
| Signaling_Disruption | 3,639 | Altered cellular signaling pathways |
| Inflammation | 2,524 | Inflammatory response activation |
| Microbiome_Disruption | 2,174 | Gut/tissue microbiome alterations |
| Receptor_Activation | 1,590 | Receptor binding and activation |
| Immune_Dysfunction | 1,155 | Immune system impairment |
| Epigenetic_Changes | 1,105 | DNA methylation, histone modification |
| Oxidative_Stress | 972 | ROS, free radical damage |
| Senescence | 782 | Cellular aging |
| Neurodegeneration | 611 | Neuronal damage/death |
| Cell_Death | 567 | Apoptosis, necrosis |
| Barrier_Disruption | 527 | Epithelial/BBB compromise |
| Endocrine_Disruption | 521 | Hormone signaling interference |
| DNA_Damage | 480 | Mutagenesis, genotoxicity |
| Mitochondrial_Dysfunction | 309 | Metabolic/energy disruption |
| Metabolic_Disruption | 231 | Metabolic pathway alterations |
| Protein_Stress | 166 | Protein misfolding, aggregation |

### Top Exposure-Mechanism Links

| Link | Grants |
|------|--------|
| Diet_Nutrition → Signaling_Disruption | 1,867 |
| Bacterial_Infection → Microbiome_Disruption | 1,349 |
| Diet_Nutrition → Inflammation | 1,209 |
| Diet_Nutrition → Microbiome_Disruption | 1,197 |
| Heavy_Metals → Signaling_Disruption | 1,111 |
| Bacterial_Infection → Inflammation | 887 |
| Viral_Infection → Inflammation | 743 |
| Heavy_Metals → Inflammation | 707 |

### Visualization

Interactive Sankey diagram showing flows from exposures to mechanisms:
- **File**: `ENV_Sankey_ExposureMechanism.html`
- **Features**: Click-to-highlight, info panel with connection details
- **Color coding**: Blue (chemical), Green (lifestyle), Orange (mechanisms)

### Files Generated

- `sankey_exposure_mechanism.json` - Exposure-mechanism link data
- `ENV_Sankey_ExposureMechanism.html` - Interactive Sankey visualization
- `env_grants_8735.csv` - Combined ENV grants with PHR (FY2022-2025)

## Subgroup Classification (Corrected - 2026-02-16)

### Problem with Original Approach

The original regex-based subgroup classification had ~66% accuracy due to:
1. **Priority ordering** - "Chemicals" was checked first with broad patterns, catching 60% of grants
2. **Over-broad patterns** - Terms like "environmental exposure", "contaminant" matched everything
3. **Keyword overlap** - "smoke" matched both wildfire smoke and tobacco smoke

### Corrected Methodology

**Key Changes:**
1. Check specific categories FIRST (Smoking, Alcohol, Infection, etc.) before catch-all Chemicals
2. Remove over-broad patterns from Chemicals category
3. Use stricter pattern matching (e.g., "radiation exposure" not just "radiation")

**Check Order:**
```
1. Smoking       → tobacco, cigarette, nicotine, vaping
2. Alcohol       → alcohol, ethanol, fetal alcohol, AUD
3. Infection     → viral/bacterial infection, HIV, hepatitis, COVID, pathogen
4. Diet/Obesity  → obesity, dietary, nutrition, metabolic syndrome, vitamin
5. Microbiome    → microbiome, microbiota, gut bacteria, dysbiosis, probiotic
6. Radiation     → radiation exposure, UV radiation, radon, radioactive
7. Gene_Env      → gene-environment interaction, GxE
8. Chemicals     → PFAS, pesticide, lead, mercury, air pollution, PM2.5, PCB (LAST)
9. Other         → default if no match
```

### Corrected Subgroup Distribution (n=8,735)

| Subgroup | Count | % |
|----------|-------|---|
| Diet_Obesity_Nutrition | 2,527 | 28.9% |
| Smoking | 1,590 | 18.2% |
| Chemicals | 1,468 | 16.8% |
| Infection | 906 | 10.4% |
| Alcohol | 752 | 8.6% |
| Microbiome | 739 | 8.5% |
| Other | 498 | 5.7% |
| Gene_Environment | 155 | 1.8% |
| Radiation | 100 | 1.1% |

### Validation Results

| Metric | Original | Corrected |
|--------|----------|-----------|
| ✅ Correct | 66.5% | **88-89%** |
| ⚠️ Questionable | 21.5% | 6-8% |
| ❌ Wrong | 12.0% | **3-5%** |

Validated with two independent spot checks (n=200 and n=300, different random seeds).

### Files Generated

- `env_grants_8735_subgroup_FINAL.csv` - Corrected subgroup classifications

## ENV Verification Pass (2026-02-16)

### Problem Identified

The original LLM classification (ENV vs NOT) had an estimated **~23% false positive rate**. Many grants were classified as ENV because they mentioned exposures but were actually:
- **Mechanism studies** - "Role of X in disease" or "Mechanism of exposure-induced Y"
- **Intervention studies** - Cessation programs, dietary interventions, probiotic trials
- **Infrastructure** - Core facilities, training grants, conferences

### Verification Methodology

Applied keyword-based verification to all 8,735 grants:

**ENV indicators (exposure research):**
- `exposure`, `exposed to`, `epidemiolog*`, `cohort study`, `case-control`
- `risk factor`, `health effect`, `health outcome`, `health impact`
- `carcinogen`, `toxic effect`, `toxicity`, `pollut*`, `contamin*`
- Specific exposures: `PFAS`, `pesticide`, `heavy metal`, `air pollution`, `PM2.5`

**NOT indicators (mechanism/intervention/infrastructure):**
- `mechanism of`, `mechanistic`, `signaling pathway`, `signal transduction`
- `intervention`, `cessation`, `treatment of`, `therapy for`, `therapeutic`
- `drug development`, `agonist`, `antagonist`, `inhibitor`
- `role of X in`, `function of` (mechanism framing)
- `training`, `conference`, `symposium`, `core facility`, `administrative`

**Decision Logic:**
1. If ENV_score >= 2 → Verified ENV
2. If NOT_score >= 2 AND ENV_score <= 1 → False Positive
3. If NOT_score >= 1 AND ENV_score = 0 → False Positive
4. If ENV_score >= 1 → Verified ENV
5. Default → Verified ENV (conservative)

### Verification Results

| Category | Count | % |
|----------|-------|---|
| ✅ Verified ENV | 6,752 | 77.3% |
| ❌ False Positives | 1,983 | 22.7% |

**False Positive Rates by Subgroup:**

| Subgroup | Original | Verified | FP Rate | Primary Issue |
|----------|----------|----------|---------|---------------|
| Diet_Obesity_Nutrition | 2,527 | 1,675 | 34% | Intervention studies |
| Microbiome | 739 | 424 | 43% | "Role of microbiome" mechanism studies |
| Infection | 906 | 606 | 33% | Mechanism studies with infection models |
| Smoking | 1,590 | 1,294 | 19% | Cessation interventions |
| Alcohol | 752 | 657 | 13% | Mechanism studies |
| **Chemicals** | **1,468** | **1,439** | **2%** | Almost all true exposure studies |
| Other | 498 | 428 | 14% | Mixed |
| Gene_Environment | 155 | 146 | 6% | Good accuracy |
| Radiation | 100 | 83 | 17% | Mechanism studies |

### Files Generated

- `env_grants_VERIFIED.csv` - 6,752 verified ENV grants
- `env_grants_FALSE_POSITIVES.csv` - 1,983 false positive grants (mechanism/intervention)

## Future Improvements

1. ~~Add subgroup verification pass with LLM~~ - Completed via corrected regex (89% accuracy)
2. Include abstract text for better classification accuracy
3. Add confidence scores to flag uncertain classifications
4. Develop disease-specific environmental exposure profiles
5. Expand mechanism detection with full abstract text

---
*Last updated: 2026-02-16*
*Classification model: Claude Haiku (ENV/NOT), Regex (Subgroups), Keyword (Verification)*
*Original candidates: 29,331 grants processed*
*LLM classified as ENV: 8,735 grants*
*Verified ENV (post-verification): 6,752 grants*
*False positives removed: 1,983 grants (23%)*
*Subgroup accuracy: 88-89%*
