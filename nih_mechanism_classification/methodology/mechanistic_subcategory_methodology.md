# Mechanistic Subcategory Classification Methodology

## Overview

This document describes the process used to classify NIH grants tagged as "Mechanistic_and_Genetic" into research focus subcategories. The goal was to create subcategories that would enable a heatmap visualization showing funding distribution across disease areas.

## Final Subcategories (8 categories + Other)

| Subcategory | Description | Total Funding |
|-------------|-------------|---------------|
| Microbial Pathogenesis | Infectious disease mechanisms, host-pathogen interactions | $1,131M |
| Immune/Inflammatory | Immune responses, inflammation, vaccines | $840M |
| Tumor Biology | Cancer mechanisms, metastasis, oncogenes | $649M |
| Other | Grants not matching specific patterns | $546M |
| Neurodegeneration | Neural death, protein aggregation, disease-specific mechanisms | $245M |
| Metabolic | Metabolism, lipids, mitochondria, energy | $160M |
| Genetics/Genomics | Genetic variants, epigenetics, gene expression | $142M |
| Reproductive/Developmental | Reproductive biology, fetal development, fertility | $111M |
| Biomarkers | Diagnostic/prognostic marker development | $19M |

## Process

### Step 1: Initial Sampling

Sampled ~100 mechanistic grant titles across disease areas to identify natural groupings:

```
grep "Mechanistic" [disease]_combined.csv | head -25 | cut -d',' -f7
```

**Observations:**
- Cancer grants heavily focused on tumor mechanisms
- Parkinson's/ALS dominated by neurodegeneration terms
- Biodefense mixed between pathogen and immune research
- Liver disease showed variety (metabolic, immune, tumor)

### Step 2: Initial Category Design

Started with 6 categories based on biological system/process:
1. Neurodegeneration
2. Tumor Biology
3. Immune/Inflammatory
4. Genetics/Genomics
5. Metabolic
6. Biomarkers

**Problem:** 39% of grants fell into "Other" - too many unclassified.

### Step 3: Added Disease-Specific Categories

Added 2 categories to capture disease-specific patterns:
- **Microbial Pathogenesis** - For Biodefense infectious disease research
- **Reproductive/Developmental** - For Contraception/Reproduction research

**Result:** "Other" dropped to 18%

### Step 4: Keyword Pattern Development

Developed regex patterns for each category. Example for Immune/Inflammatory:

```python
"Immune/Inflammatory": [
    r"immun", r"inflammat", r"neuroinflam", r"cytokine", r"interleukin",
    r"\bT.?cell", r"\bB.?cell", r"macrophage", r"neutrophil", r"lymphocyte",
    r"antibod", r"autoimmun", r"interferon", r"chemokine",
    r"checkpoint", r"\bPD-?1\b", r"\bPD-?L1\b", r"\bCD\d+",
    r"microglia", r"astrocyte", r"glial", r"myeloid", r"inflammasome",
    r"vaccine", r"vaccin", r"adjuvant"
]
```

### Step 5: Classification Logic

```python
def classify_grant(title, disease_area=""):
    scores = {}
    for category, keywords in patterns.items():
        score = sum(1 for kw in keywords if re.search(kw, title, re.IGNORECASE))
        if score > 0:
            scores[category] = score

    if not scores:
        # Default for neurodegenerative disease areas
        if disease_area in ["ALS", "Parkinsons"]:
            return "Neurodegeneration"
        return "Other"

    # Highest score wins
    return max(scores.items(), key=lambda x: x[1])[0]
```

## Issues Found and Fixed

### Issue 1: Disease Names Overriding Research Focus

**Problem:** Parkinson's showed 0 grants in Immune/Inflammatory, but manual inspection found grants like:
- "Immune System Aging in Parkinson's and Alzheimer's disease"
- "The Role of Myeloid Cells in Parkinson's Disease"
- "Alpha-Synuclein-Specific T cells in Parkinson's Disease Pathogenesis"

**Cause:** "parkinson" and "alzheimer" were in the Neurodegeneration keyword list, so any Parkinson's grant got classified as Neurodegeneration regardless of actual research focus.

**Fix:** Removed disease names (parkinson, alzheimer, ALS, huntington) from Neurodegeneration keywords. Instead, rely on mechanism-specific terms (synuclein, lewy, motor neuron, etc.) and use disease area as fallback only when NO keywords match.

**Result:** Parkinson's now shows 9 grants ($4.6M) in Immune/Inflammatory.

### Issue 2: Vaccine Grants Misclassified

**Problem:** Vaccine development grants in Biodefense were going to Microbial Pathogenesis because "influenza" or "COVID" matched, but vaccines are fundamentally about immune responses.

**Examples misclassified:**
- "Impact of repeated vaccination on the effectiveness of seasonal influenza vaccines"
- "A new mucosal adjuvant for augmenting influenza vaccines"

**Fix:** Added "vaccine", "vaccin", "adjuvant" to Immune/Inflammatory keywords.

**Result:** Biodefense Immune/Inflammatory increased from 19.6% to 28.3% ($678M).

### Issue 3: Tie-Breaking Logic

**Problem:** When a grant matched multiple categories equally, the first alphabetically would win, which wasn't always appropriate.

**Example:** "Role of microglia in motor neuron degeneration"
- Matches Neurodegeneration: 1 (motor neuron)
- Matches Immune/Inflammatory: 1 (microglia)

**Decision:** Keep current behavior (highest score wins, ties go to first match). This is acceptable because:
1. Most grants have clear dominant focus
2. Edge cases are relatively rare
3. Adding complex tie-breaking rules risks over-fitting

## Validation

### Spot Checks Performed

1. **ALS immune grants:** Searched for immune keywords, found 124 mentions but only 13 classified as Immune - verified the others were primarily about neurodegeneration with immune as secondary focus.

2. **Cancer immunotherapy:** Verified grants about CAR-T, checkpoint inhibitors go to Immune when immune terms dominate.

3. **Biodefense vaccines:** Confirmed vaccine grants now classify as Immune.

### Final Distribution Validation

| Disease | Top Category | % | Makes Sense? |
|---------|-------------|---|--------------|
| ALS | Neurodegeneration | 82% | Yes - disease-specific mechanisms |
| Parkinson's | Neurodegeneration | 79% | Yes - with 3% immune now captured |
| Lung Cancer | Tumor Biology | 74% | Yes - cancer mechanisms |
| Breast Cancer | Tumor Biology | 78% | Yes |
| Biodefense | Microbial Pathogenesis | 50% | Yes - with 28% immune (vaccines) |
| Liver Disease | Other | 30% | Acceptable - diverse research |
| Contraception | Reproductive | 49% | Yes |

## Files Generated

- `classify_mechanistic_final.py` - Classification script
- `mechanistic_subfields.json` - Output data for visualization
- `viz_sankey_with_heatmap.html` - Interactive visualization

## Limitations

1. **Title-only classification:** Only uses grant titles, not abstracts. Some grants may be misclassified due to limited information.

2. **"Other" category:** 17% of grants don't match specific patterns. These are legitimate mechanistic research that doesn't fit neat categories.

3. **Single-label:** Each grant gets one category. Some grants span multiple areas (e.g., "Genetic regulation of immune response in cancer").

4. **Keyword sensitivity:** Classification depends on specific word choices in titles. Synonyms may be missed.

## Future Improvements

1. Use grant abstracts for more accurate classification
2. Implement multi-label classification for grants spanning categories
3. Add confidence scores to flag uncertain classifications
4. Develop disease-specific subcategories for more granular analysis

---

# Clinical & Other Subcategory Classification

## Final Subcategories (7 categories + Other)

| Subcategory | Description | Total Funding |
|-------------|-------------|---------------|
| Training/Infrastructure | Cores, CTUs, training grants, resources | $536M |
| Clinical Trials/Drug Dev | Phase trials, drug development, therapeutics | $318M |
| Screening/Detection | Early detection, imaging, diagnostics | $223M |
| Epidemiology/Population | Cohort studies, registries, trends | $120M |
| Behavioral/Lifestyle | Exercise, smoking cessation, counseling | $80M |
| Health Disparities/Access | Underserved populations, equity | $78M |
| Technology/Methods | Novel devices, AI, gene/cell therapy | $52M |
| Other | Unclassified (47%) | $1,150M |

## Key Differences from Mechanistic Classification

1. **Higher "Other" rate (47% vs 17%)** - Clinical category is inherently more heterogeneous
2. **Some grants may be miscategorized** - Basic research that belongs in Mechanistic
3. **Generic titles common** - "Project 1", "Core A" don't provide classifiable information

## Keyword Patterns

```python
"Clinical Trials/Drug Dev": [
    r"phase [I1-4]+", r"placebo", r"randomized", r"clinical trial",
    r"preclinical", r"therapeutic", r"inhibitor", r"efficacy"
],
"Behavioral/Lifestyle": [
    r"behavio", r"exercise", r"smoking cessation", r"counseling",
    r"adherence", r"self.?management", r"quality of life"
],
"Screening/Detection": [
    r"screen", r"early detection", r"imaging", r"PET", r"MRI",
    r"diagnostic", r"biomarker", r"mammogra"
],
"Training/Infrastructure": [
    r"core", r"administrative", r"CTU", r"training", r"mentor",
    r"pilot.*program", r"reference lab", r"consortium"
]
```

## Validation Notes

- Lung Cancer shows high Screening/Detection (18%) - appropriate given screening programs
- Biodefense shows high Training/Infrastructure (37%) - reflects CTU network
- Contraception shows high Other (64%) - many reproductive biology grants may belong in Mechanistic
- The "Other" category serves as a catch-all for truly heterogeneous research
