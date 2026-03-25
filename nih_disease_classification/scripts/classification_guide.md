# Grant Classification Guide

## Overview

This document outlines the decision-making process for categorizing NIH grants into four groups based on their research focus. The classification system is designed to distinguish between genetic, environmental, mechanistic, and other types of cancer research.

---

## The Four Categories

### 1. Strictly_Genetic
Research focused purely on inherited genetics, germline mutations, genetic risk, or genetic sequencing without environmental or mechanistic components.

**Include:**
- Germline mutation studies
- Genetic risk variants (SNPs, polymorphisms)
- Familial cancer sequencing
- Genome-wide association studies (GWAS)
- Hereditary cancer syndromes
- Genetic ancestry and cancer risk
- Copy number variations, chromosomal abnormalities (when studying inheritance)

**Exclude:**
- Somatic mutations (these are Mechanistic)
- Studies mentioning both genetic AND environmental factors (these are Gene-Environment)
- Functional studies of how mutations cause disease (these are Mechanistic)

---

### 2. Strictly_Environmental_or_Gene-Environment
Research focused on environmental exposures, lifestyle factors, or the interaction between genes and environment.

**Environmental exposures include:**
- **Smoking/tobacco** - cigarettes, vaping, e-cigarettes, nicotine
- **Air pollution** - PM2.5, PM10, particulate matter, diesel exhaust
- **Occupational exposures** - asbestos, silica, coal dust, workplace chemicals
- **Metals** - arsenic, cadmium, chromium (Cr(VI)), beryllium, lead, nickel
- **Radiation** - radon, UV, ionizing radiation
- **Diet/nutrition** - when studying specific dietary exposures
- **Microbiome** - gut bacteria, fecal microbiota, gut-brain axis, enteric nervous system. **See dedicated Microbiome Classification Rules section below for detailed guidance.**
- **Circadian disruption** - shift work, sleep disruption (lifestyle)
- **Infections** - when studying pathogen as environmental exposure

**Gene-Environment includes:**
- Studies explicitly mentioning BOTH genetic and environmental contributions
- Biomarkers of exposure in smokers/exposed populations
- Exposome studies
- Smoke-free interventions (environmental modification)

**Key indicators:**
- "exposure," "exposome," "environmental"
- "smoking," "tobacco," "smoke-free"
- "occupational," "workplace"
- Specific chemical/metal names
- "radon," "asbestos," "pollution"
- "microbiome," "microbiota"
- "circadian," "shift work"

---

### 3. Mechanistic_Pathogenesis
Research focused on understanding HOW cancer develops, progresses, or responds to treatment at the molecular, cellular, or physiological level.

**Include:**

#### Signaling Pathways & Molecular Biology
- Kinases (EGFR, MET, ALK, CDK, PI3K, MAPK, JAK, etc.)
- Phosphatases (SHP2, PTEN, etc.)
- Transcription factors (NF-kB, STAT, YAP, NEUROD1, etc.)
- GTPases and GEFs (RAS, RAC, etc.)
- Any named protein/pathway being studied for its FUNCTION

#### Epigenetics
- Histone modifications (methylation, acetylation)
- Histone modifiers (SETD2, NSD2, NSD3, KAT5, KAT8/MOF, LSD1, CARM1, etc.)
- Chromatin remodeling (SMARCA2, SMARCA4, BAP1, etc.)
- DNA methylation mechanisms

#### Cell Biology
- Cell cycle regulation
- Apoptosis, ferroptosis, necroptosis, pyroptosis (cell death mechanisms)
- Autophagy, mitophagy
- Cellular plasticity, EMT (epithelial-mesenchymal transition)
- Cell state transitions
- Senescence
- Progenitor/stem cell biology

#### Tumor Biology
- Tumor microenvironment (TME)
- Tumor-immune interactions (mechanistic, not clinical immunotherapy trials)
- Metastasis mechanisms
- Angiogenesis
- Tumor heterogeneity (when studying mechanisms)
- Stromal interactions

#### Metabolism
- Cancer metabolism (Warburg effect, glutamine, serine, etc.)
- Metabolic vulnerabilities
- Oxidative stress, redox biology
- Ferroptosis (iron-dependent cell death)

#### Drug Resistance Mechanisms
- Molecular mechanisms of resistance
- Synthetic lethality studies
- Drug target mechanisms
- Resistance to targeted therapy, immunotherapy, chemotherapy

#### DNA Damage & Repair
- DNA damage response (DDR)
- Replication stress
- Chromosomal instability (when studying mechanisms)
- BRCA, PARP mechanisms

#### Immune Mechanisms
- Immune checkpoint mechanisms (PD-1/PD-L1, CTLA-4, etc. - when studying HOW they work)
- Tumor immune evasion
- Immunosuppressive mechanisms
- Cytokine/chemokine signaling

**Key phrases that indicate Mechanistic:**
- "mechanism," "mechanistic"
- "pathway," "signaling"
- "role of," "function of"
- "regulation," "modulation"
- "target," "targeting" (molecular targets)
- "resistance mechanism"
- "synthetic lethality"
- "tumor microenvironment"
- "plasticity," "EMT"
- "epigenetic"
- Named proteins/genes being studied functionally

---

### 4. Everything_else
Research that does not fit the above categories, typically clinical, epidemiological, behavioral, or infrastructure-focused.

**Include:**

#### Clinical Research
- Clinical trials (treatment trials, not mechanism studies)
- Screening programs and implementation
- Diagnostic test development/validation
- Biomarker implementation (clinical use, not discovery)
- Treatment outcomes studies
- Survivorship care

#### Epidemiology & Population Science
- Cancer incidence/prevalence studies
- Health disparities research (social determinants)
- Health equity interventions
- Population-based cohort studies

#### Behavioral Research
- Smoking cessation interventions
- Behavioral interventions
- Psychological interventions
- Patient communication/stigma
- Health beliefs and behaviors

#### Technology & Methods
- Imaging technology development
- AI/machine learning for clinical applications
- Radiotherapy planning/delivery
- Surgical techniques

#### Infrastructure
- Cancer center programs (P30 grants)
- Core facilities
- Training programs
- Conferences/workshops
- Administrative cores
- Biospecimen banks

---

## Decision Tree

```
1. Does the grant study environmental exposures or gene-environment interactions?
   YES → Strictly_Environmental_or_Gene-Environment
   NO → Continue

2. Does the grant study purely inherited genetic risk without functional/mechanistic components?
   YES → Strictly_Genetic
   NO → Continue

3. Does the grant study molecular/cellular MECHANISMS of cancer?
   (pathways, proteins, cell biology, resistance mechanisms, tumor biology)
   YES → Mechanistic_Pathogenesis
   NO → Continue

4. Default → Everything_else
   (clinical trials, screening, behavioral, epidemiology, infrastructure)
```

---

## Common Pitfalls & Edge Cases

### Words that DON'T always mean Mechanistic:
- **"Mechanism"** in behavioral context (e.g., "mechanism of behavior change") → Everything_else
- **"Pathway"** in care pathway context (e.g., "care pathway intervention") → Everything_else
- **"Target"** in population context (e.g., "target population for screening") → Everything_else
- **"Biomarker"** for clinical implementation → Everything_else (vs. biomarker discovery → could be Mechanistic)

### Words that DON'T always mean Genetic:
- **"Mutation"** when studying functional consequences → Mechanistic_Pathogenesis
- **"Genomic"** when studying tumor genomics for mechanisms → Mechanistic_Pathogenesis
- **"CRISPR"** when used as a tool for functional studies → Mechanistic_Pathogenesis

### Environmental vs. Mechanistic:
- Metal-induced cancer (studying the exposure) → Environmental
- Metal-induced DNA damage (studying the mechanism) → Could be either, lean Environmental if exposure is the focus
- **Microbiome studies → See dedicated Microbiome Classification Rules section below**

### Genetic vs. Mechanistic:
- Germline BRCA mutations and cancer risk → Strictly_Genetic
- How BRCA loss causes genomic instability → Mechanistic_Pathogenesis
- Somatic mutations in tumors → Mechanistic_Pathogenesis

### Clinical vs. Mechanistic:
- "Mechanism-based therapy" → Check if studying the mechanism (Mechanistic) or testing the therapy (Everything_else)
- Drug resistance → If studying WHY resistance occurs (Mechanistic), if testing ways to overcome clinically (Everything_else)
- Immunotherapy → If studying immune mechanisms (Mechanistic), if running clinical trials (Everything_else)

---

## Microbiome Classification Rules

Microbiome grants require special consideration because they can fall into any of the three main categories depending on the research focus.

### Everything_else (Therapies & Technology)
Grants focused on **therapies, interventions, or technology development**:
- Fecal microbiota transplant (FMT) trials
- Probiotic/prebiotic interventions
- Microbiome-based therapeutics development
- Microbiome engineering technology
- Microbiome analysis platforms/methods
- Clinical trials testing microbiome interventions

**Key indicators:** "therapeutic," "therapy," "treatment," "probiotic," "FMT," "transplant," "intervention," "trial," "technology," "platform," "engineering"

### Mechanistic_Pathogenesis (Infection & Basic Biology)
Grants focused on **infection/pathogen interactions OR basic microbiome biology**:
- Host-pathogen-microbiome interactions
- Microbiome's role in colonization resistance
- Antimicrobial resistance mechanisms
- How microbiome affects pathogen virulence
- Basic microbiome biology (strain transmission, epithelial interactions)
- Microbiome regulation and modulation mechanisms
- Metabolite production and signaling

**Key indicators:** "infection," "pathogen," "colonization," "virulence," "antimicrobial," "C. difficile," "resistance," "transmission," "strain," "regulation," "modulation"

### Strictly_Environmental_or_Gene-Environment (Disease Outcomes)
Grants focused on **microbiome's impact on disease risk or outcomes**:
- Gut microbiome and cancer risk
- Microbiome and neurodegeneration (Parkinson's, Alzheimer's)
- Gut-brain axis in disease
- Gut-liver axis in liver disease
- Microbiome and metabolic disease (obesity, diabetes)
- Microbiome and inflammatory conditions
- Microbiome as a disease risk factor

**Key indicators:** "risk," "outcome," "progression," "disease," specific disease names (cancer, Parkinson's, diabetes, etc.), "gut-brain," "gut-liver"

### Decision Priority
When a grant matches multiple categories, apply in this order:
1. **Everything_else** - If it's testing a therapy or developing technology
2. **Mechanistic** - If it's studying infection/pathogens OR basic biology
3. **Environmental** - If it's studying disease outcomes (default for unclear cases)

---

## Quality Control Checks

After classification, verify by searching for:

1. **In Everything_else:** Should NOT contain many grants with:
   - Named kinases, phosphatases, transcription factors
   - "mechanism of," "pathway," "signaling"
   - EMT, plasticity, ferroptosis, autophagy
   - Resistance mechanisms

2. **In Strictly_Genetic:** Should NOT contain:
   - Environmental exposures
   - Functional mechanism studies
   - The word "environmental" or "exposure"

3. **In Mechanistic_Pathogenesis:** Should NOT contain:
   - Pure clinical trials without mechanism focus
   - Behavioral interventions
   - Screening implementation
   - Infrastructure/administrative grants

4. **In Strictly_Environmental:** Should contain:
   - Clear environmental exposures OR
   - Gene-environment interaction studies

---

## Smoking_Subgroup Tagging

In addition to the four main categories, grants should be tagged with a **Smoking_Subgroup** indicator (Yes/No) if they are related to smoking, tobacco, or nicotine.

### Tag as "Yes" if the grant mentions:
- smoking, smoker, smokers
- tobacco, cigarette, cigarettes
- nicotine
- vaping, vape, e-cigarette
- smoke-free, smokefree
- cessation (smoking/nicotine cessation)
- secondhand smoke, passive smoking

### Tag as "No" (exclude from smoking subgroup):
- "Never smokers" studies (studying lung cancer in people who never smoked)
- Studies where smoking is only mentioned as exclusion criteria
- General cancer studies that don't focus on smoking

### Search terms for QC:
```
smoking|tobacco|cigarette|nicotine|smoker|vaping|vape|e-cigarette|smoke-free|smokefree|cessation
```

---

## Lessons Learned from Lung Cancer Classification

### Common Misclassifications Found:

1. **Everything_else → Mechanistic_Pathogenesis** (most common error)
   - Grants studying named proteins, pathways, or mechanisms were often incorrectly tagged as "Everything_else"
   - Key fix: Search for protein names, "mechanism," "pathway," "resistance," "target"

2. **Strictly_Genetic → Mechanistic_Pathogenesis**
   - Grants studying FUNCTION of genes/mutations were incorrectly tagged as genetic
   - "Role of X in cancer" = Mechanistic (studying function)
   - "Mechanisms of mutations" = Mechanistic
   - "Targeting X" = Mechanistic
   - Key fix: Only tag as Strictly_Genetic if studying inherited risk, not functional consequences

3. **Strictly_Genetic → Strictly_Environmental**
   - Grants mentioning "environmental" factors were tagged as genetic
   - Key fix: Search Strictly_Genetic for "environmental," "exposure," "carcinogen"

4. **Missing Smoking_Subgroup tags**
   - Many smoking-related grants were not tagged
   - Key fix: Search all grants for smoking terms and verify tagging

### Recommended QC Workflow:
1. First pass: Apply initial classifications
2. Search Everything_else for mechanistic terms → reclassify
3. Search Strictly_Genetic for mechanistic terms (function, role, mechanism, targeting) → reclassify
4. Search Strictly_Genetic for environmental terms → reclassify
5. Search all categories for smoking terms → verify Smoking_Subgroup tag
6. Final verification of category counts

---

## Lessons Learned from ALS Classification

### Common Misclassifications Found:

1. **Everything_else → Mechanistic_Pathogenesis** (63 corrections)
   - ALS grants heavily feature protein aggregation studies (TDP-43, FUS, SOD1, C9orf72)
   - Key terms missed: "phase separation," "aggregation," "condensate," "pathogenic"
   - "Defining mechanisms underlying..." = Mechanistic
   - "Molecular basis of..." = Mechanistic

2. **Strictly_Genetic → Mechanistic_Pathogenesis** (24 corrections)
   - Grants with gene names but studying FUNCTION were misclassified
   - "Excitability dysfunction mechanisms" = Mechanistic (not genetic risk)
   - "Pathogenic mechanisms of mutations" = Mechanistic
   - "Regulation mechanism and functional genomics" = Mechanistic

3. **Strictly_Environmental → Mechanistic_Pathogenesis** (8 corrections)
   - "Toxicity" keyword triggered Environmental tag incorrectly
   - "Cell-type-specific toxicity of C9orf72" = Mechanistic (studying toxicity mechanism)
   - "Neurotoxicity of RNA metabolism dysfunction" = Mechanistic
   - Key fix: If studying HOW something causes toxicity, it's Mechanistic

4. **Strictly_Genetic → Everything_else** (3 corrections)
   - Gene therapy DEVELOPMENT is not genetic risk research
   - Imaging technology development is not genetic research
   - "Gene delivery for treatment" = Everything_else (therapeutic development)

5. **Strictly_Genetic → Strictly_Environmental** (1 correction)
   - "Exposome" studies should be Environmental
   - Key fix: Search for "exposome" in Genetic category

### ALS-Specific Keywords for Mechanistic:
- TDP-43, FUS, SOD1, C9orf72 (when studying function/mechanism)
- Phase separation, liquid-liquid phase separation
- Protein aggregation, aggregates
- Motor neuron degeneration mechanisms
- Nuclear pore complex
- RNA metabolism, RNA-binding proteins

---

## Lessons Learned from Colorectal Cancer Classification

### Common Misclassifications Found:

1. **Everything_else → Mechanistic_Pathogenesis** (101 corrections)
   - Many grants studying specific proteins/pathways were missed
   - Common patterns: "Role of [protein] in colorectal cancer"
   - Key proteins: KRAS, BRAF, p53, WNT, EGFR, APC
   - Metastasis mechanism studies often misclassified
   - Drug resistance mechanism studies often misclassified

2. **Strictly_Genetic → Mechanistic_Pathogenesis** (11 corrections)
   - "Defining the function of mutations" = Mechanistic
   - "DNA damage repair by [gene]" = Mechanistic (studying repair mechanism)
   - "Mechanistic studies of DNA mismatch repair" = Mechanistic
   - "Targeting [gene] mutations" = Mechanistic

3. **Strictly_Genetic → Everything_else** (12 corrections)
   - Core facilities (sequencing cores, data analysis cores)
   - Behavioral interventions for genetic testing
   - Clinical implementation of genetic testing
   - Clinical trials using genetic tests

4. **Strictly_Genetic → Strictly_Environmental** (2 corrections)
   - "Gene-environment interaction" studies = Environmental
   - "Gene x Environment" studies = Environmental

5. **Mechanistic_Pathogenesis → Everything_else** (7 corrections)
   - Core facilities were tagged as Mechanistic
   - Clinical trials were tagged as Mechanistic
   - Survivorship care studies were tagged as Mechanistic
   - Key fix: Search Mechanistic for "core," "clinical trial," "survivorship"

6. **Everything_else → Strictly_Environmental** (2 corrections)
   - "Environmental exposures and cancer risk" = Environmental
   - "Modifiable exposures" = Environmental

### Colorectal Cancer-Specific Keywords:

**Mechanistic indicators:**
- KRAS, BRAF, APC, p53/TP53, WNT, EGFR, MSI/MSS
- Metastasis, liver metastasis, peritoneal metastasis
- Drug resistance, chemoresistance
- Tumor microenvironment, stromal interactions
- Necroptosis, ferroptosis (cell death mechanisms)

**Environmental indicators (for Diet_Microbiome_Tag):**
- Microbiome, microbiota, gut bacteria
- Fusobacterium, Streptococcus gallolyticus
- Probiotic, prebiotic
- Diet, dietary, nutrition, obesity
- Colitis-associated cancer

### Additional QC Steps for Colorectal Cancer:
1. Check for microbiome/diet-related grants missing Diet_Microbiome_Tag
2. Search Environmental for "probiotic," "bacteria," "microbiome" → verify tag
3. Search Mechanistic for "core," "clinical trial" → move to Everything_else

---

## General Lessons Across Disease Types

### Most Common Error Pattern:
**Everything_else → Mechanistic_Pathogenesis**

This is consistently the most frequent misclassification across all disease types. Grants studying molecular mechanisms are often tagged as "Everything_else" because:
- The initial classifier may not recognize protein names
- "Role of" and "targeting" are strong mechanistic indicators often missed
- Resistance mechanisms are frequently missed

### Key Search Terms for QC (apply to all disease types):

**Search Everything_else for these → likely Mechanistic:**
```
role of|mechanism|pathway|signaling|kinase|inhibitor|target|resistance|
metasta|apoptosis|autophagy|ferroptosis|necroptosis|phosphat|ubiquitin|
degradation|aggregat|phase separation
```

**Search Strictly_Genetic for these → likely Mechanistic:**
```
mechanism|function|role of|targeting|pathogenic|pathophysiology
```

**Search Strictly_Genetic for these → likely Environmental:**
```
environment|exposure|exposome|gene-environment|gene x environment
```

**Search Mechanistic for these → likely Everything_else:**
```
core|clinical trial|phase i|phase ii|randomized|survivorship|
implementation|behavioral intervention
```

**Search Mechanistic for these → move to Environmental:**
```
microbiome|microbiota|gut-brain|gut brain|enteric|myenteric|prokaryote
```

**Search any category for these → verify subgroup tags:**
```
microbiome|microbiota|diet|dietary|smoking|tobacco|probiotic
```

---

## Lessons Learned from Parkinson's Disease Classification

### Overview
Parkinson's disease grants required **111 total corrections** out of 510 grants (22% error rate). The most common issues involved grants studying neural mechanisms, protein function, and circuit dynamics being incorrectly classified.

### Common Misclassifications Found:

#### 1. **Everything_else → Mechanistic_Pathogenesis** (74 corrections - most common)
Grants studying neural and molecular mechanisms were frequently misclassified. Key patterns:

- **"Role of [structure/protein]"** - e.g., "Role of subthalamic nucleus," "Role of LRRK2"
- **"Mechanism of [process]"** - e.g., "Mechanisms of Low-Dose Ketamine Treatment"
- **Circuit/network studies** - e.g., "Circuit Mechanisms of Attentional-Motor Interface"
- **"Pathophysiology"** - inherently mechanistic (e.g., "Pathophysiology of Basal Ganglia Disorders")
- **Named proteins with functional terms** - LRRK2, synuclein, PINK1, VPS35, GBA when studied functionally
- **Plasticity studies** - "Corticosubthalamic Plasticity," "Striatal Plasticity"
- **Omics studies** - proteomics, lipidomics, single-cell sequencing

**Key search terms for QC:**
```
role of|mechanism|pathophysiology|pathway|circuit|network dynamics|
plasticity|LRRK2|synuclein|PINK1|VPS35|GBA|dysfunction|
proteom|lipidom|single.cell|propagation|aggregation
```

#### 2. **Strictly_Genetic → Mechanistic_Pathogenesis** (9 corrections)
Grants studying the FUNCTION of genes/mutations were incorrectly tagged as purely genetic:

- "Mechanistic Analysis of Genetic Modifiers" = Mechanistic (explicit)
- "Functional Role of GPNMB in Pathogenesis" = Mechanistic (functional study)
- "Effect of GBA1 mutation on synaptic morphology" = Mechanistic (studying effect)
- "Crosstalk Between Nurr1...Regulation by Ligands" = Mechanistic (regulation)
- Proteomic studies = Mechanistic (even with genomic component)
- Mouse models studying mutation effects = Mechanistic

**Key distinction:**
- GWAS/SNP discovery → Strictly_Genetic
- Studying HOW mutations cause disease → Mechanistic_Pathogenesis

#### 3. **Strictly_Genetic → Everything_else** (9 corrections)
Clinical/therapeutic grants incorrectly tagged as genetic:

- **Gene therapy** = Everything_else (therapeutic intervention, not genetic research)
- **Prediction models** = Everything_else (clinical application)
- **Health disparities** = Everything_else (epidemiology)
- **Behavioral interventions** = Everything_else (even if genetics mentioned)
- **Clinical studies** = Everything_else

#### 4. **Mechanistic_Pathogenesis → Everything_else** (10 corrections)
Clinical/administrative grants incorrectly tagged as mechanistic:

- **Administrative/resource cores** - "Neuroimaging Resource Core"
- **Training/mentorship awards** - "Midcareer Development Award"
- **Behavioral interventions** - music therapy, exergaming, exercise programs
- **Clinical technology** - smartphone apps, telehealth, AR rehabilitation
- **Palliative care** - clinical care, not mechanism research
- **Home-use devices** - neurostimulation treatment devices

**Key search terms for QC:**
```
core|administrative|training|mentorship|career development|
rehabilitation|therapy|smartphone|telehealth|palliative|
exergaming|exercise intervention|music therapy
```

#### 5. **Strictly_Environmental → Other categories** (6 corrections)
- Behavioral interventions (exercise) incorrectly tagged as Environmental → Everything_else
- EEG diagnostic coding incorrectly tagged as Environmental → Everything_else
- Mechanism-focused toxicity studies are BORDERLINE (can stay Environmental if exposure is the focus)

### Parkinson's Disease-Specific Keywords:

**Mechanistic indicators:**
- LRRK2, alpha-synuclein, PINK1, Parkin, VPS35, GBA, DJ-1, ATP13A2, SYNJ1
- Dopaminergic neurons, substantia nigra, nigrostriatal, striatum, basal ganglia
- Lewy body/pathology, protein aggregation, propagation, spreading
- Mitophagy, autophagy, lysosomal dysfunction, mitochondrial dysfunction
- Circuit dynamics, network synchrony, neural correlates
- Synaptic plasticity, corticosubthalamic, neuroinflammation

**Clinical/Everything_else indicators:**
- Deep brain stimulation (DBS) optimization/programming (not mechanism)
- Rehabilitation, physical therapy, gait training, balance
- Cognitive training, behavioral intervention
- Biomarker validation, diagnostic accuracy
- Palliative care, caregiver support, quality of life
- Telemedicine, wearables, smartphone apps

**Environmental indicators:**
- Pesticide, herbicide, paraquat, rotenone, dieldrin
- PFAS, metal exposure, manganese, lead
- Pollutant, environmental exposure, occupational
- Microbiome (when studying as exposure source)
- Gene-environment interaction

### Key Takeaways for Parkinson's Disease:

1. **"Pathophysiology" = Mechanistic** - Always reclassify grants with "pathophysiology" in the title

2. **Circuit/network studies = Mechanistic** - Neural circuit dynamics, network synchrony, and circuit manipulation are mechanistic research

3. **Named proteins need context:**
   - LRRK2 + "function/role/mechanism/regulation" = Mechanistic
   - LRRK2 + "genetic risk/susceptibility" = Genetic
   - LRRK2 + "therapy/treatment" = Everything_else

4. **Administrative components don't change content:**
   - "Administrative Supplement to [Mechanistic study]" = Still Mechanistic
   - "Resource Core" = Everything_else (infrastructure)

5. **Environmental vs. Mechanistic for toxicity:**
   - "Pollutant-induced dysfunction" = Environmental (exposure is the focus)
   - "Mechanisms of toxicity" = Borderline, but can stay Environmental if studying the exposure

6. **Very few grants are truly Strictly_Genetic** - Only pure GWAS, gene discovery, and genetic susceptibility studies without functional components (ended with only 3 out of 510)

7. **IMPORTANT: Microbiome/Gut studies = Environmental, NOT Mechanistic**
   - Even if studying mechanisms of how microbiome affects disease, classify as Environmental
   - Microbiome is treated as an environmental/exposure factor
   - This includes: gut-brain axis, enteric nervous system, myenteric macrophages, gut permeability
   - Exception: Probiotic/microbiome-based therapeutics = Everything_else (intervention)

### Environmental Subcategories for Parkinson's Disease:

The 30 Environmental grants can be organized into 4 subcategories:

| Subcategory | Grants | Amount | Description |
|-------------|--------|--------|-------------|
| **Microbiome/Gut-Brain Axis** | 8 | $2,560,910 | Gut bacteria, enteric nervous system, gut-brain connections, myenteric macrophages |
| **Chemical Exposures** | 11 | $4,307,155 | Pesticides (pyrethroid, paraquat, rotenone), Metals (e-cigarette aerosol, metal-mediated redox), PFAS, General toxicants |
| **Air Pollution** | 1 | $2,296,059 | Atmospheric particulate matter |
| **Gene-Environment Interactions** | 10 | $4,132,483 | Broad gene x environment studies, multiple exposures, toxicant + genetic interaction |

**Chemical Exposures breakdown:**
- Pesticides: 5 grants ($2,397,444) - pyrethroids, paraquat, organophosphates
- Metals: 3 grants ($1,089,316) - e-cigarette metal mixtures, metal-mediated oxidation
- PFAS: 1 grant ($249,000) - per/polyfluoroalkyl substances
- General Toxicants: 2 grants ($571,395) - pollutant-induced dysfunction

**Keywords for Environmental subcategories:**
```
Microbiome: microbiome|microbiota|gut-brain|gut brain|enteric|myenteric|prokaryote|bacteria.*gut
Chemical: pesticide|pyrethroid|paraquat|rotenone|metal mixture|PFAS|perfluoro|toxicant|neurotoxic
Air_Pollution: particulate matter|PM2\.5|atmospheric pollut|air pollut
Gene_Environment: gene.environment|gene x environment|environmental and genetic
```

### QC Workflow for Parkinson's Disease:

1. Search Everything_else for: `role of|mechanism|pathophysiology|circuit|network|plasticity|LRRK2|synuclein|PINK1`
2. Search Strictly_Genetic for: `function|mechanism|effect|role|proteom|mouse model`
3. Search Mechanistic for: `core|administrative|rehabilitation|therapy|training|palliative|smartphone`
4. **Search Mechanistic for: `microbiome|microbiota|gut-brain|gut brain|enteric|myenteric` → move to Environmental**
5. Verify Environmental grants contain actual exposure terms
6. Check that Strictly_Genetic grants are pure genetics (GWAS, gene discovery) without functional studies

---

## Lessons Learned from Women's Health Classification

### Overview
Women's Health grants required extensive QC corrections across all categories. The dataset includes diverse research areas: breast/ovarian/cervical cancers, pregnancy/reproduction, maternal health, menopause, and sex-specific conditions. Key challenges involved distinguishing between lifestyle as exposure vs. lifestyle intervention, and handling mechanistic research with obesity/diet context.

### Common Misclassifications Found:

#### 1. **Everything_else → Mechanistic_Pathogenesis** (most common)
Grants studying molecular/cellular mechanisms were frequently missed:

- **Kinase studies** - Grants studying specific kinases (CDK4/6, JNK, ceramide kinase, PI3K, etc.) as mechanisms
- **Plasticity/EMT** - Lineage plasticity, epithelial-mesenchymal transition studies
- **Cell death mechanisms** - Ferroptosis, autophagy studies
- **Resistance mechanisms** - Drug resistance, chemoresistance mechanism studies
- **"Role of [X]"** pattern - Almost always mechanistic when X is a protein/hormone/pathway

**Key search terms for QC:**
```
kinase|plasticity|EMT|ferroptosis|autophagy|resistance|role of|mechanism|
signaling|pathway|tumor microenvironment|metastasis
```

#### 2. **Strictly_Environmental → Mechanistic_Pathogenesis**
Environmental tag incorrectly applied to grants studying mechanisms:

- **"Mechanistic Study"** in title - Explicit mechanistic research, not exposure
- **"Role of [protein]"** - Studying protein function, not environmental exposure
- **"Mechanisms of [condition]"** - Studying disease mechanisms
- **Neural circuit studies** - Alcohol/substance studies on circuit mechanisms
- **Matrix metalloproteinase function** - "Metalloproteinase" ≠ metal exposure

**Key distinction:**
- "Role of obesity in [mechanism]" = Mechanistic (studying the mechanism)
- "Obesity as exposure leading to [outcome]" = Environmental (studying exposure effect)

#### 3. **Strictly_Environmental → Everything_else** (behavioral interventions)
The word "lifestyle" triggered Environmental tag, but interventions should be Everything_else:

- **"Lifestyle Intervention"** - Behavioral intervention = Everything_else
- **"Dietary intervention"** - Intervention testing = Everything_else
- **"Cognitive-Behavioral Therapy"** - CBT for any condition = Everything_else
- **"App-based intervention"** - Technology interventions = Everything_else
- **"Web-based/Internet-assisted intervention"** - Digital health interventions = Everything_else
- **"Exercise training"** (as treatment) - Intervention study = Everything_else
- **"Therapy for [condition]"** - Therapy development = Everything_else
- **Health disparities research** - Social determinants = Everything_else

**Critical distinction:**
- Studying exercise as EXPOSURE → Environmental
- Testing exercise as INTERVENTION/TREATMENT → Everything_else
- Studying obesity effects → Environmental
- Testing diet intervention for obesity → Everything_else

**Key patterns that indicate Everything_else (not Environmental):**
```
intervention|therapy development|cognitive.behavioral|CBT|
app-based|web-based|internet-assisted|lifestyle intervention|
dietary intervention|exercise training|health disparit|health equit
```

#### 4. **Word Matching False Positives**
Several keywords caused incorrect Environmental classification:

- **"metalloproteinase"** matched "metal" → Not a metal exposure, it's a protein
- **"Leader cell"** matched "lead" → Not lead exposure, it's cell biology
- **"lifestyle"** in demographics context → Not lifestyle exposure study
- **"nonmetallic"** matched "metal" → Actually about NOT using metals
- **"genotoxic therapy"** matched "toxic" → Therapy development, not toxin exposure

**Lesson:** Use word boundaries in regex (`\blead\b` not just `lead`) and context checking.

#### 5. **Infrastructure/Administrative Grants in Environmental**
Grants incorrectly classified due to keyword matching:

- **Leadership Administrative Cores** - Should be Everything_else
- **Training programs** - Should be Everything_else
- **SCORE grants** - Infrastructure, should be Everything_else

### Women's Health-Specific Keywords:

**Mechanistic indicators:**
- Kinases: CDK4, CDK6, JNK, PI3K, ceramide kinase, hexokinase, LRRK2
- Cancer biology: EMT, plasticity, ferroptosis, metastasis, resistance
- Proteins: FSH, LH, estrogen receptor, BRCA (when studying function)
- Pathways: signaling, tumor microenvironment, cell death

**Environmental indicators (true exposures):**
- Prenatal exposures: PFAS, phthalates, air pollution, PM2.5
- Lifestyle exposures: alcohol use (as exposure), smoking, diet (as exposure)
- Occupational: radiation exposure, chemical exposure
- Microbiome: vaginal microbiome, gut microbiome (as environmental factor)
- Infections: HIV, HPV, CMV, STIs (as environmental exposure)

**Everything_else indicators:**
- Interventions: CBT, lifestyle intervention, exercise intervention
- Technology: app-based, web-based, smartphone, telehealth
- Clinical: therapy, treatment development, clinical trial
- Infrastructure: core, administrative, training, SCORE

### Key Takeaways for Women's Health:

1. **"Lifestyle" requires context** - Lifestyle as exposure = Environmental; Lifestyle intervention = Everything_else

2. **"Role of [X]"** = Almost always Mechanistic when X is a protein, hormone, or pathway

3. **"Mechanisms of [condition]"** = Mechanistic, not Environmental even if condition relates to exposure

4. **Behavioral interventions are not Environmental** - CBT, exercise training, dietary interventions testing efficacy belong in Everything_else

5. **Watch for false keyword matches** - metalloproteinase ≠ metal, Leader ≠ lead, genotoxic therapy ≠ toxin exposure

6. **Infection can be Environmental or Mechanistic:**
   - Studying infection as exposure/risk factor → Environmental
   - Studying mechanisms of infection → Mechanistic

7. **Drug/therapy development is Everything_else** - Even if studying mechanisms to develop the drug

### QC Workflow for Women's Health:

1. Search Environmental for: `intervention|therapy|CBT|app-based|web-based|lifestyle intervention|dietary intervention`
2. Search Environmental for: `role of|mechanism|metalloproteinase|function of|leader cell`
3. Search Everything_else for: `kinase|plasticity|EMT|ferroptosis|signaling|pathway|metastasis|resistance`
4. Search Strictly_Genetic for: `function|mechanism|role|targeting|pathogenesis`
5. Verify Environmental grants contain true exposure terms (not just "lifestyle" or "diet")
6. Check for administrative/core/training grants in Environmental → move to Everything_else

### Additional Lessons from Women's Health QC:

#### Treatment Toxicity vs Environmental Toxicity
**Critical distinction:** Treatment-induced toxicity is NOT environmental exposure.

Move to Everything_else:
- "doxorubicin-induced cardiotoxicity" → Treatment side effect study
- "anthracycline cardiac toxicity" → Treatment side effect study
- "chemotherapy-induced toxicity" → Treatment side effect study
- "radiotherapy-induced toxicity" → Treatment side effect study
- "ART toxicities" (antiretroviral therapy) → Treatment monitoring
- "gonadotoxic chemotherapy" → Treatment effect study

Keep in Environmental:
- "environmental toxicant exposure" → True environmental exposure
- "toxicant-induced neurodegeneration" → Studying effect of environmental toxin

**Pattern to identify treatment toxicity:**
```
doxorubicin|anthracycline|chemotherapy.induced|radiotherapy.induced|
ART toxicit|drug.induced.*toxic|treatment.induced
```

#### False Positives from "Lead" and Similar Words

| Word in Title | Actual Meaning | Correct Category |
|---------------|----------------|------------------|
| "Lead Academic Site" | Leadership role | Everything_else |
| "LAUNCH Program" | Training program | Everything_else |
| "lead to subsequent" | Causation verb | Context-dependent |
| "lead compound" | Drug candidate | Everything_else |
| "leader cell" | Cell biology term | Mechanistic |
| "lead exposure" | Metal exposure | Environmental |

**Lesson:** Always check context. Only `lead exposure` or `lead poisoning` = Environmental.

#### Intervention Patterns (Always Everything_else, not Environmental)

Even if title contains lifestyle/diet/exercise terms, these patterns indicate Everything_else:
```
intervention|program for|therapy for|training program|
on-a-chip|chip.*screening|GLP.*toxicology|
marker-guided development|wellness.*program|
telehealth|mHealth|app-based|web-based|smartphone
```

#### Environmental Subgroup Tagging Patterns

For categorizing Environmental grants into overlapping subgroups:

| Subgroup | Pattern |
|----------|---------|
| Obesity | `\bobes\|overweight\|adipos\|BMI\|body mass\|high.fat diet\|NAFLD` |
| Diet | `\bdiet(?!ary intervention)\|nutri\|food intake\|prebiotic\|fasting` |
| Alcohol | `\balcohol\|drinking\|FASD\|fetal alcohol\|AUD\|ethanol` |
| Smoking | `\bsmok\|tobacco\|cigarette\|nicotine\|vaping\|never smoker` |
| Air_Pollution | `air pollut\|PM2\.5\|PM10\|particulate\|wildfire\|O3\|ozone` |
| Chemicals | `PFAS\|phthalate\|pesticide\|PCB\|BPA\|PAH\|pollutant\|perfluoro` |
| Metals | `\blead exposure\|arsenic\|cadmium\|mercury\|heavy metal` |
| Microbiome | `microbiome\|microbiota\|gut bacteria\|vaginal bacteria\|lactobacillus` |
| Infection | `HIV\|HPV\|infection\|viral\|CMV\|chlamydia\|STI\|helminth` |
| Exercise | `exercise(?!.*intervention)\|physical activity(?!.*intervention)\|sedentary` |
| Prenatal | `prenatal\|maternal exposure\|in.utero\|gestational exposure\|fetal exposure` |
| Stress | `stress\|psychosocial\|adversity\|trauma\|adverse childhood` |
| Sleep | `sleep\|circadian\|shift work\|insomnia` |
| Gene_Environment | `gene.environment\|genetic and environmental\|GxE` |

---

## General Classification Principles (All Disease Areas)

### Decision Tree Summary

```
1. Is it infrastructure (core, admin, training, leadership)?
   → YES: Everything_else

2. Is it an intervention/therapy/treatment study?
   → YES: Everything_else

3. Is it studying MECHANISMS (molecular, cellular, pathway, signaling)?
   → YES: Mechanistic_Pathogenesis

4. Is it studying EXPOSURE effects (environmental, lifestyle, infection)?
   → YES: Strictly_Environmental_or_Gene-Environment

5. Is it pure genetics (GWAS, gene discovery, no function)?
   → YES: Strictly_Genetic

6. None of the above?
   → Everything_else
```

### Red Flags for Misclassification

| If you see... | Check if it should be... |
|---------------|--------------------------|
| "mechanism" in Environmental | Mechanistic |
| "role of [protein]" in Environmental | Mechanistic |
| "function of" in Environmental | Mechanistic |
| "intervention" in Environmental | Everything_else |
| "therapy" in Environmental | Everything_else |
| "program" in Environmental | Everything_else |
| "treatment toxicity" in Environmental | Everything_else |
| "kinase/pathway/signaling" in Everything_else | Mechanistic |
| "targeting [protein]" in Strictly_Genetic | Mechanistic |

---

## Lessons Learned from Breast Cancer Classification

### Overview
Breast cancer grants required extensive reclassification. Starting with 1,766 grants, the initial automatic classification significantly under-classified mechanistic research. Final counts: Mechanistic_Pathogenesis (860), Everything_else (854), Strictly_Environmental (39), Strictly_Genetic (13).

### Common Misclassifications Found:

#### 1. **Everything_else → Mechanistic_Pathogenesis** (most common - ~300 corrections)
Many grants studying molecular mechanisms were initially missed:

- **Metastasis studies** - "breast cancer metastasis," "brain metastasis," "bone colonization"
- **Resistance mechanisms** - "chemoresistance," "drug resistance," "therapy resistance," "overcoming resistance"
- **"Role of [X] in"** pattern - Almost always mechanistic when X is a protein/gene
- **"Targeting [X]"** pattern - Molecular targeting studies
- **"Function of [X]"** pattern - Functional studies
- **Tumor microenvironment** - TME, stromal, fibroblast, macrophage studies
- **Receptor studies** - ER, PR, HER2, triple-negative biology
- **DNA repair** - BRCA function, RAD51, homologous recombination
- **Nanotherapy/nanoparticle** - Drug delivery mechanism studies
- **Oncolytic virus** - Virus-based therapy mechanism studies

**Key search terms for QC:**
```
role of|function of|mechanism|targeting|metastasis|metastatic|
resistance|chemoresist|tumor microenvironment|TME|stromal|
receptor|BRCA|RAD51|DNA repair|nanoparticle|nanotherapy|
oncolytic|antibody.drug|bispecific|CAR.T|exosome
```

#### 2. **Strictly_Genetic → Mechanistic_Pathogenesis** (3 corrections)
Grants studying gene FUNCTION rather than genetic risk:

- "RAD51 paralog function in cancer predisposition and genome integrity" → Mechanistic (studying function)
- "Stalled replication fork repair in cancer predisposition" → Mechanistic (studying repair mechanism)
- "Defining the role of persistent DNA bridges in tumor-intrinsic immune activation" → Mechanistic (studying role/function)

**Key distinction:**
- BRCA mutations and cancer RISK → Strictly_Genetic
- BRCA FUNCTION in DNA repair → Mechanistic_Pathogenesis

#### 3. **Everything_else/Mechanistic → Strictly_Environmental** (9 corrections)
Grants with environmental exposure focus incorrectly classified:

- Gene-environment interaction studies (explicit mention of both)
- Environmental risk factor studies using adductomics
- Endocrine disruptor studies (in utero estrogenic disruption)
- Exposome studies

#### 4. **Strictly_Environmental → Mechanistic_Pathogenesis** (3 corrections)
Grants studying mechanisms incorrectly tagged as Environmental:

- "Chemotherapy-induced circadian master clock disruptions" → Mechanistic (studying mechanism of chemotherapy effect, not environmental circadian exposure)
- "Targeting RAGE in tumor and TME" → Mechanistic (targeting, TME - mechanistic keywords override obesity context)

**Key distinction:**
- Studying HOW chemotherapy disrupts circadian rhythm = Mechanistic
- Studying circadian disruption as lifestyle/environmental exposure = Environmental

#### 5. **Strictly_Environmental → Everything_else** (1 correction)
- "Breast cancer survivorship in the era of climate change" → Everything_else (survivorship study, not environmental exposure research)

### Breast Cancer-Specific Keywords:

**Mechanistic indicators:**
- Receptors: ER, PR, HER2, EGFR, triple-negative, TNBC
- DNA repair: BRCA1, BRCA2, RAD51, PARP, homologous recombination
- Proteins: p53, PIK3CA, CDK4/6, mTOR, Wnt, Notch
- TME: tumor microenvironment, stromal, CAF, macrophage, T-cell infiltration
- Metastasis: brain metastasis, bone metastasis, liver metastasis, invasion
- Resistance: chemoresistance, endocrine resistance, HER2 resistance
- Therapy mechanisms: nanotherapy, ADC, bispecific antibody, CAR-T, oncolytic

**Environmental indicators:**
- Diet/Obesity: obesity, adiposity, BMI, dietary, nutrition, lipid metabolism
- Microbiome: gut microbiome, microbiota, microbial metabolites
- Endocrine disruptors: BPA, phthalates, estrogenic chemicals
- Gene-environment: exposome, gene x environment

**Everything_else indicators:**
- Clinical: clinical trial, phase I/II/III, randomized, screening, mammography
- Survivorship: survivor, quality of life, cognitive function after treatment
- Disparities: health disparities, health equity, underserved
- Imaging: MRI, PET (when clinical application, not molecular imaging)
- Biomarker implementation: ctDNA for clinical use, liquid biopsy validation

### Environmental Subgroup Tagging for Breast Cancer:

The Environmental grants (39 total) are tagged with an **Environmental_Subgroup** column:

| Subgroup | Count | Description |
|----------|-------|-------------|
| Diet_Obesity_Nutrition | 18 | Obesity, dietary factors, lipid metabolism, nutrition studies |
| Microbiome | 7 | Gut microbiome, oral microbiome, microbial metabolites |
| Gene_Environment_Interaction | 6 | Explicit gene x environment studies, exposome |
| Circadian_Sleep | 3 | Circadian rhythm, sleep disruption (as exposure, not mechanism) |
| Endocrine_Disruptors_Chemicals | 3 | BPA, e-cigarettes, environmental chemicals |
| Occupational | 1 | Occupational and environmental exposures |
| Other | 1 | Adductomics, general environmental risk factors |

**Keywords for Environmental subcategories:**
```
Diet_Obesity_Nutrition: diet|dietary|nutrition|obesity|obese|adipos|fat|weight|lipid|metaboli
Microbiome: microbiome|microbiota|gut bacteria|microbial|oral microbiome
Gene_Environment_Interaction: gene.environment|exposome|genetic.+environment|environment.+genetic
Circadian_Sleep: circadian|sleep|shift work
Endocrine_Disruptors_Chemicals: endocrine disrupt|BPA|phthalate|e.cigarette|electronic cigarette
Occupational: occupational|workplace exposure
```

### Key Takeaways for Breast Cancer:

1. **"Targeting [protein]" = Mechanistic** - Even if it mentions therapy, molecular targeting studies are mechanistic

2. **Obesity context requires careful evaluation:**
   - "Role of obesity in tumor progression" = Mechanistic (studying mechanism)
   - "Obesity as risk factor for breast cancer" = Environmental (studying exposure)
   - "Obesity intervention for prevention" = Everything_else (intervention study)

3. **Chemotherapy-induced effects:**
   - Studying MECHANISM of chemo side effects = Mechanistic
   - Studying chemo as treatment = Everything_else
   - Managing chemo side effects clinically = Everything_else

4. **Receptor studies are almost always Mechanistic:**
   - ER/PR/HER2 mechanism studies = Mechanistic
   - ER/PR/HER2 clinical testing = Everything_else

5. **DNA repair genes need context:**
   - BRCA genetic risk/testing = Strictly_Genetic or Everything_else
   - BRCA function in repair = Mechanistic_Pathogenesis

6. **Circadian disruption:**
   - Shift work as exposure → Environmental
   - Chemotherapy disrupting circadian clock (mechanism) → Mechanistic

7. **Microbiome remains Environmental** even when studying mechanisms of how it affects breast cancer

### QC Workflow for Breast Cancer:

1. Search Everything_else for: `role of|function of|mechanism|targeting|metastasis|resistance|TME|tumor microenvironment|receptor|BRCA|RAD51|nanoparticle|oncolytic`
2. Search Strictly_Genetic for: `function|mechanism|role|targeting|repair|stability`
3. Search Environmental for: `chemotherapy-induced|targeting|role of|mechanism` → may need reclassification
4. Search Mechanistic for: `clinical trial|survivorship|screening|disparit` → move to Everything_else
5. Verify Environmental grants and apply Environmental_Subgroup tags
6. Check that Strictly_Genetic grants are pure genetics without functional studies

---

## Standardized Environmental Subgroups (All Disease Areas)

### Overview

After processing 9 disease areas (18,977 grants total), environmental subgroups have been standardized to use 10 consistent categories across all files. This ensures comparability and simplifies analysis.

### The 10 Standardized Subgroup Names

| Subgroup | Description | Total Grants |
|----------|-------------|--------------|
| **Diet_Obesity_Nutrition** | Diet, obesity, nutrition, physical activity, exercise, lifestyle factors | 245 |
| **Chemicals** | Toxins, pollutants, metals, air pollution, endocrine disruptors, occupational exposures, wildfire smoke, PM2.5 | 169 |
| **Smoking** | Tobacco, nicotine, cigarettes, vaping, e-cigarettes, cessation (overrides Chemicals for tobacco-related) | 138 |
| **Microbiome** | Gut microbiome, microbiota, dysbiosis, probiotics | 133 |
| **Other** | General environmental studies without specific exposure type | 123 |
| **Alcohol** | Alcohol consumption, alcohol exposure, fetal alcohol | 72 |
| **Infection** | Viral/bacterial exposures as environmental factors, zoonotic diseases, prions | 55 |
| **Radiation** | UV exposure, ionizing radiation, X-ray exposure | 28 |
| **Gene_Environment** | Gene-environment interactions, GxE studies | 7 |
| **Circadian_Sleep** | Circadian rhythm disruption, sleep disorders, shift work | 4 |

**Total: 974 Environmental grants with subgroups assigned**

### Priority Rules for Subgroup Assignment

When a grant could fit multiple subgroups, apply these priority rules:

1. **Smoking overrides Chemicals** - E-cigarette toxicity, tobacco carcinogens → Smoking (not Chemicals)
2. **Chemicals has high priority** - When chemical exposure is present alongside other factors
3. **Single subgroup per grant** - Each grant gets exactly one subgroup
4. **"Other" is the default** - Use only when no specific exposure type applies

### Subgroup Distribution by Disease Area

| Subgroup | ALS | Breast | Color | Lung | Parkin | Women | Biodef | Contra | Liver |
|----------|-----|--------|-------|------|--------|-------|--------|--------|-------|
| Diet_Obesity_Nutrition | - | 14 | 26 | 7 | 2 | 173 | - | 12 | 11 |
| Chemicals | 1 | 6 | 4 | 20 | 14 | 62 | 10 | 31 | 21 |
| Smoking | - | 1 | - | 121 | 2 | 13 | - | 1 | - |
| Microbiome | 1 | 3 | 26 | 6 | 8 | 51 | 1 | 13 | 24 |
| Alcohol | - | - | - | - | - | 54 | - | 7 | 11 |
| Infection | - | - | 3 | 1 | - | 26 | 21 | 2 | 2 |
| Radiation | - | - | 1 | - | - | 4 | 23 | - | - |
| Gene_Environment | - | - | - | - | - | 5 | - | - | 2 |
| Circadian_Sleep | - | - | - | - | - | 4 | - | - | - |
| Other | 1 | 6 | 8 | 10 | 4 | 39 | 29 | 23 | 3 |

### Keywords for Each Subgroup

```
Diet_Obesity_Nutrition:
  \bdiet\b|dietary|nutri|obesity|obese|BMI|body mass|overweight|
  physical activity|exercise|sedentary|calori|fat.*intake|fiber|
  mediterranean|food|eating|weight.*loss|adipos|lifestyle

Chemicals:
  chemical|pollut|toxic|metal|arsenic|cadmium|chromium|lead|mercury|nickel|
  endocrine disrupt|BPA|bisphenol|phthalate|PFAS|pesticide|herbicide|
  air quality|particulate|PM2\.5|occupational|workplace exposure|
  carcinogen|dioxin|benzene|formaldehyde|radon|asbestos|
  microplastic|xenobiotic|aflatoxin|VOC|volatile|wildfire|wood smoke

Smoking:
  smok|tobacco|nicotine|cigarette|vap(?:e|ing)|e-cig|nitrosamine|
  cessation.*tobacco|quit.*smok

Microbiome:
  microbi|gut flora|intestinal bacteria|dysbiosis|probiotic|prebiotic|
  fecal|commensal|colonic bacteria|antibiotic.*risk|bacteria.*derived

Alcohol:
  \balcohol\b|ethanol|drinking.*risk|alcohol.*consumption|alcohol.*exposure|
  fetal alcohol|prenatal alcohol

Infection:
  zoonotic|prion|CWD|virus.*exposure|infection.*risk|pathogen|
  transmissible|BSE|scrapie|infectious|viral.*transmission|\bHIV\b|\bHBV\b|\bHCV\b

Gene_Environment:
  gene.environment|gene.exposure|genetic.*environmental|GxE|
  susceptibility.*exposure|polymorphism.*exposure|G.x.E|gene x env

Circadian_Sleep:
  circadian|sleep.*disrupt|shift work|melatonin|clock gene

Radiation:
  \bradiation\b|UV.*exposure|ultraviolet|ionizing|X-ray.*exposure
```

### Naming Consolidation (Historical)

Previous non-standard names were consolidated:

| Old Name | New Standard Name |
|----------|-------------------|
| Chemicals_Metals | Chemicals |
| Obesity | Diet_Obesity_Nutrition |
| Lifestyle_Factors | Diet_Obesity_Nutrition |
| Infectious_Disease | Infection |
| Endocrine_Disruptors_Chemicals | Chemicals |
| Gene_Environment_Interaction | Gene_Environment |
| Occupational | Chemicals |
| Air_Pollution | Chemicals |
| Metals | Chemicals |

### Removed Subgroups

- **Prenatal** - Removed as standalone category; prenatal exposures are now classified by the exposure type (e.g., prenatal alcohol → Alcohol, prenatal chemicals → Chemicals)

---

## Summary: All Disease Areas Processed

### Final Grant Counts by Category

| Disease Area | Total | Mechanistic | Everything_else | Environmental | Genetic |
|--------------|-------|-------------|-----------------|---------------|---------|
| ALS | 301 | 219 (73%) | 63 (21%) | 3 (1%) | 16 (5%) |
| Breast Cancer | 1,766 | 869 (49%) | 854 (48%) | 30 (2%) | 13 (1%) |
| Colorectal Cancer | 790 | 330 (42%) | 376 (48%) | 68 (9%) | 16 (2%) |
| Lung Cancer | 1,169 | 486 (42%) | 474 (41%) | 165 (14%) | 44 (4%) |
| Parkinsons | 510 | 289 (57%) | 188 (37%) | 30 (6%) | 3 (1%) |
| Womens Health | 6,800 | 1,856 (27%) | 4,252 (63%) | 431 (6%) | 261 (4%) |
| Biodefense | 4,138 | 3,138 (76%) | 914 (22%) | 84 (2%) | 2 (0%) |
| Contraception/Reproduction | 1,596 | 460 (29%) | 1,043 (65%) | 89 (6%) | 4 (0%) |
| Liver Disease | 1,907 | 1,351 (71%) | 479 (25%) | 74 (4%) | 3 (0%) |
| **TOTAL** | **18,977** | **8,998 (47%)** | **8,643 (46%)** | **974 (5%)** | **362 (2%)** |

### Key Observations Across Disease Areas

1. **Environmental % varies by disease:**
   - Highest: Lung Cancer (14%) - driven by smoking research
   - Lowest: ALS (1%), Breast Cancer (2%), Biodefense (2%)

2. **Mechanistic vs Everything_else split:**
   - Biodefense highest Mechanistic (76%) - basic science focus
   - Contraception/Womens Health highest Everything_else (63-65%) - clinical/behavioral focus

3. **"Other" subgroup remains for:**
   - General environmental studies without specific exposure type
   - Multi-exposure studies that don't fit single category
   - Stress/psychosocial factors (kept in Other per decision)
   - Climate/heat exposures (kept in Other per decision)

### Quality Assurance Checklist

After classifying any disease area, verify:

- [ ] All Environmental grants have Environmental_Subgroup assigned
- [ ] Subgroup names match the 10 standardized names
- [ ] No duplicate subgroup names (e.g., both "Chemicals" and "Chemicals_Metals")
- [ ] Smoking grants take priority over Chemicals for tobacco-related studies
- [ ] Microbiome grants are in Environmental (not Mechanistic)
- [ ] Intervention studies are in Everything_else (not Environmental)
- [ ] "Role of" and "Mechanism of" studies are in Mechanistic (not Environmental)

---

## Lessons Learned from Liver Disease Classification

### Overview
Liver Disease grants (1,907 total) presented unique challenges due to the prevalence of hepatitis, alcohol-related liver disease, and metabolic conditions. Final counts: Mechanistic_Pathogenesis (1,351, 70.8%), Everything_else (479, 25.1%), Strictly_Environmental (74, 3.9%), Strictly_Genetic (3, 0.2%).

### Common Misclassifications Found:

#### 1. **Everything_else → Mechanistic_Pathogenesis** (most common)
Grants studying liver disease mechanisms were frequently missed:

- **Kinase studies** - Hexokinase, JNK, CDK, PI3K in liver disease
- **Plasticity/EMT** - Lineage plasticity, epithelial-mesenchymal transition in liver
- **Ferroptosis** - Iron-dependent cell death in liver injury
- **Stellate cell biology** - Hepatic stellate cell activation, fibrosis mechanisms
- **Viral mechanisms** - HBV/HCV replication, viral lifecycle, host-virus interactions

**Key search terms for QC:**
```
kinase|plasticity|EMT|ferroptosis|stellate|hepatocyte|fibrosis|
mechanism|signaling|pathway|HBV|HCV|viral replication
```

#### 2. **Drug-Induced Liver Injury (DILI)**
**Critical rule:** DILI studies are Mechanistic_Pathogenesis, NOT Environmental.
- Studying mechanisms of drug hepatotoxicity = Mechanistic
- These are not "environmental exposures" but drug metabolism/toxicity mechanisms

#### 3. **Microbiome Studies → Environmental**
All microbiome/gut-liver axis studies go to Environmental, even if studying mechanisms:

- Gut-liver axis interactions
- Microbiome-dependent metabolites (bile acids, etc.)
- Gut permeability and bacterial translocation
- Probiotic/prebiotic mechanism studies
- Fecal microbiota transplant research

**Microbiome is treated as an internal environmental exposure.**

#### 4. **Alcohol-Related Studies - Context Matters**
- **Alcohol mechanisms** (how alcohol damages liver) = Mechanistic
- **Alcohol exposure/risk studies** (epidemiology, phenotyping) = Environmental
- **Alcohol interventions** (treatment programs) = Everything_else

#### 5. **Obesity/Diet Studies - Context Matters**
- **Obesity mechanisms** (how obesity causes NAFLD) = Mechanistic
- **Obesity epidemiology** (cohort studies, risk factors) = Environmental
- **Diet interventions** (testing treatments) = Everything_else

### Liver Disease-Specific Keywords:

**Mechanistic indicators:**
- Hepatocyte, stellate cell, Kupffer cell, cholangiocyte
- Fibrosis, fibrogenesis, cirrhosis mechanisms
- HBV, HCV, viral replication, lifecycle, cccDNA
- NAFLD/NASH mechanisms, steatosis, lipotoxicity
- Cholestasis mechanisms, bile acid metabolism
- Drug metabolism, CYP450, hepatotoxicity mechanisms
- Regeneration, liver repair mechanisms

**Environmental indicators:**
- Microbiome, microbiota, gut-liver axis, gut bacteria
- Toxin exposure: aflatoxin, microcystin, arsenic, PFAS
- Prenatal/early life: maternal, fetal, developmental
- Alcohol phenotyping, drinking patterns
- Obesity cohorts, diet epidemiology
- Air pollution, particulate matter
- Gene-environment interaction studies
- Psychosocial stress, acculturative stress

**Everything_else indicators:**
- Clinical trial, randomized, phase I/II/III
- Biomarkers (clinical validation, not discovery)
- Disparities, health equity
- Transplant outcomes (clinical, not mechanism)
- Screening programs, surveillance
- Training, administrative, core facilities

### Environmental Subgroup Tagging for Liver Disease:

The 74 Environmental grants are tagged with overlapping subgroups:

| Subgroup | Count | Description |
|----------|-------|-------------|
| Microbiome | 33 | Gut-liver axis, gut bacteria, probiotics, fecal microbiota |
| Chemical_Toxin | 17 | Aflatoxin, arsenic, PFAS, flame retardants, VOCs, chemicals |
| Alcohol | 14 | Alcohol exposure/phenotyping (not mechanisms) |
| Prenatal_Early_Life | 13 | Maternal, fetal, early life exposures |
| Diet | 6 | Diet epidemiology, nutrition exposure |
| Obesity | 5 | Obesity cohorts, BMI risk studies |
| Psychosocial_Stress | 4 | Acculturative stress, social adversity |
| Gene_Environment | 3 | Gene x environment interaction studies |
| Air_Pollution | 1 | Particulate matter exposure |
| Viral_Exposure | 1 | HBV/HCV as environmental exposure |
| Other | 4 | General environmental liver disease |

**Keywords for Environmental subcategories:**
```
Microbiome: microbiome|microbiota|gut bacteria|gut-liver|gut liver axis|probiotic|prebiotic|fecal microb|intestinal permeability
Chemical_Toxin: toxin|aflatoxin|microcystin|arsenic|PFAS|flame retardant|cadmium|VOC|1,4-dioxane|organophosphate|endocrine disrupt
Prenatal_Early_Life: prenatal|maternal|early life|in.utero|gestational|fetal|developmental|neonatal
Alcohol: alcohol.*risk|alcohol.*phenotyp|drinking pattern|AUD risk
Obesity: obesity.*cohort|obesity.*epidemiol|BMI.*risk|childhood obesity
Diet: diet.*epidemiol|nutrition.*cohort|epidemiology of diet
Gene_Environment: gene.environment|genetic and environmental|genomic and environmental|GxE|nature and nurture
Psychosocial_Stress: psychosocial|acculturative stress|social adversity
Air_Pollution: air pollut|PM2\.5|PM10|particulate
```

### Key Takeaways for Liver Disease:

1. **HBV/HCV studies are usually Mechanistic** - Most study viral mechanisms, host-virus interactions, or antiviral mechanisms

2. **Microbiome = Environmental** - Even when studying HOW microbiome affects liver disease, classify as Environmental

3. **DILI = Mechanistic** - Drug-induced liver injury mechanism studies are mechanistic, not environmental

4. **Fibrosis context matters:**
   - Fibrosis mechanism studies = Mechanistic
   - Fibrosis as outcome of exposure = Environmental (if exposure is the focus)

5. **Very few grants are Strictly_Genetic** - Only 3 out of 1,907 (pure genetic risk/GWAS)

6. **Alcohol needs careful classification:**
   - Alcohol + mechanism keywords = Mechanistic
   - Alcohol + epidemiology/cohort = Environmental
   - Alcohol + intervention/treatment = Everything_else

### QC Workflow for Liver Disease:

1. Search Everything_else for: `kinase|plasticity|ferroptosis|stellate|hepatocyte|mechanism|signaling|HBV|HCV|fibrosis`
2. Search Mechanistic for: `microbiome|microbiota|gut-liver|gut bacteria` → move to Environmental
3. Search Environmental for: `mechanism|role of|function of|pathway` → may need to stay if exposure-focused
4. Verify alcohol grants are correctly distributed across categories
5. Apply Environmental_Subgroup tags to all Environmental grants
6. Check that Strictly_Genetic grants are pure genetics (should be very few)

---
