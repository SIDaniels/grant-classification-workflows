# NIH Disease Classification: Molecular vs Environmental vs Clinical

**Output:** [engineeredresilience.org/evidence/methods/nih](https://www.engineeredresilience.org/evidence/methods/nih)

## Goal

Show that **environmental factors research gets only ~3.4% of NIH funding** across 8 disease areas—even for diseases where environmental exposures are known major risk factors (like lung cancer and smoking, or Parkinson's and pesticides).

---

## The Actual Process (Play-by-Play)

### Step 1: Downloaded NIH grants by disease area

Went to [NIH Reporter](https://reporter.nih.gov) and searched for each disease. Exported to CSV with these fields: APPLICATION_ID, PROJECT_TITLE, PROJECT_TERMS, TOTAL_COST, etc.

| Disease | File | Grants |
|---------|------|--------|
| ALS | `ALS_combined.csv` | ~400 |
| Biodefense | `Biodefense_combined.csv` | ~800 |
| Breast Cancer | `Breast_Cancer_combined.csv` | ~2,500 |
| Colorectal Cancer | `Colorectal_Cancer_combined.csv` | ~900 |
| Contraception | `Contraception_Reproduction_combined.csv` | ~500 |
| Liver Disease | `Liver_Disease_combined.csv` | ~1,200 |
| Lung Cancer | `Lung_Cancer_combined.csv` | ~1,800 |
| Parkinson's | `Parkinsons_combined.csv` | ~600 |

### Step 2: Built the classification system (iterated many times)

**The challenge:** How do you distinguish "environmental" from "mechanistic" research when many grants mention both? For example:
- "Role of arsenic in oxidative stress" — Is that environmental (arsenic exposure) or mechanistic (oxidative stress pathway)?
- "Gut microbiome and colorectal cancer" — Environmental exposure or mechanism study?

**First attempt (failed):** Used Haiku for classification. It was too aggressive and confidently misclassified edge cases. Many mechanism studies got tagged as environmental because they mentioned an exposure.

**What worked:** Switched to Sonnet with a strict decision tree that prioritizes categories in order:

```
For each grant, check IN ORDER:

1. Infrastructure/admin (cores, training, conferences)?
   → Everything_else (stop here)

2. Clinical intervention (trial, treatment, cessation)?
   → Everything_else (stop here)

3. PRIMARY focus on environmental EXPOSURE?
   (chemicals, PFAS, microbiome, diet, smoking, pollution)
   → Strictly_Environmental (stop here)

4. PRIMARY focus on molecular/cellular MECHANISM?
   (protein function, signaling, pathways)
   → Mechanistic_Pathogenesis (stop here)

5. Pure genetic risk (GWAS, germline)?
   → Strictly_Genetic (stop here)

6. Default → Everything_else
```

**The key insight:** Ask "Is the EXPOSURE the focus, or is the MECHANISM the focus?"
- "Arsenic exposure and cancer risk" → Environmental (studying the exposure)
- "How arsenic damages DNA" → Mechanistic (studying the mechanism)
- "Arsenic-induced oxidative stress pathway" → Mechanistic (mechanism is the focus)

### Step 3: Ran classification on each disease file

Used `classify_by_exposure.py` which sends batches to Claude Sonnet. Required PROJECT_TITLE *and* PROJECT_TERMS for accuracy—titles alone weren't enough context.

Each disease area needed QC. Found systematic errors:
- "Everything_else → Mechanistic" was the most common fix (grants studying pathways got missed)
- Had to search for mechanistic keywords like "kinase", "pathway", "signaling" in Everything_else
- Microbiome studies stayed Environmental even when studying mechanisms (policy decision)

See `classification_guide.md` for the full 1300-line decision tree with lessons learned from each disease area.

### Step 4: QC and iteration (this took a while)

For each disease area, I had to:
1. Run initial classification
2. Sample and review results
3. Find systematic errors (e.g., all "kinase" studies were in Everything_else)
4. Update the decision tree with new rules
5. Re-run or manually fix

**Common error patterns across diseases:**
- Grants with "role of [protein]" or "mechanism of" got tagged Everything_else → should be Mechanistic
- Grants with "targeting [protein]" got tagged Genetic → should be Mechanistic
- Smoking cessation *interventions* got tagged Environmental → should be Everything_else
- Microbiome grants studying mechanisms were borderline → decided to keep as Environmental

### Step 5: Generated Sankey data

Once classifications were stable, aggregated counts and funding by disease × category.

```bash
python scripts/regenerate_viz_data.py
```

**Output:** `data/sankey_full_data_v2.json`

### Step 6: Built the D3.js visualization

Used a Sankey diagram to show flow from diseases → research categories. The visual makes the funding gap obvious.

**Output:** `visualization/viz_sankey_with_heatmap.html`

---

## File Structure

```
nih_disease_classification/
├── data/
│   ├── ALS_combined.csv                    # Classified grants (with Category column)
│   ├── Breast_Cancer_combined.csv
│   ├── Colorectal_Cancer_combined.csv
│   ├── Lung_Cancer_combined.csv
│   ├── Parkinsons_combined.csv
│   ├── Liver_Disease_combined.csv
│   ├── Biodefense_combined.csv
│   ├── Contraception_Reproduction_combined.csv
│   ├── sankey_full_data_v2.json            # Aggregated data for Sankey
│   └── viz_data_dollars.json               # Funding amounts
│
├── scripts/
│   ├── classification_guide.md             # ⭐ THE BIG ONE: Full decision tree (1300 lines)
│   │                                       #    with lessons learned from each disease
│   ├── environmental_classification_methodology.md  # ENV/NOT classification criteria
│   ├── classify_by_exposure.py             # Main classification script
│   ├── classify_mechanistic_final.py       # Mechanistic subgroup classifier
│   ├── classify_clinical_final.py          # Clinical subgroup classifier
│   ├── classify-grants.md                  # Claude Code slash command
│   ├── qc-grants.md                        # QC slash command
│   └── regenerate_viz_data.py              # Generate Sankey JSON from CSVs
│
├── visualization/
│   ├── viz_sankey_with_heatmap.html        # ⭐ Main Sankey diagram
│   └── nih_disease_funding_widget.html     # Alternative widget version
│
└── exploratory_mechanistic/                # ⚠️ EXPLORATORY (not in final viz)
    ├── sankey_exposure_mechanism.json      # Tried: Exposure → Mechanism mapping
    ├── sankey_chem_mechanism.json          # Tried: Chemical → Mechanism mapping
    ├── ENV_Sankey_ExposureMechanism.html   # Visualization attempt
    └── ENV_Sankey_ChemMechanism.html       # Visualization attempt
```

---

## To Reproduce

### 1. Download grants from NIH Reporter

Go to [reporter.nih.gov](https://reporter.nih.gov), search for a disease (e.g., "lung cancer"), filter by fiscal year, and export as CSV. Make sure you include:
- APPLICATION_ID
- PROJECT_TITLE
- PROJECT_TERMS
- TOTAL_COST (or AWARD_AMOUNT)

### 2. Classify grants

Option A — Python script:
```bash
python scripts/classify_by_exposure.py data/Lung_Cancer.csv
```

Option B — Claude Code slash command:
```
/classify-grants data/Lung_Cancer.csv
```

This adds a `Category` column to each row: Strictly_Genetic, Strictly_Environmental, Mechanistic_Pathogenesis, or Everything_else.

### 3. QC the results

Sample 20-50 grants from each category and verify. Look for:
- Mechanism studies in Everything_else (search for "kinase", "pathway", "signaling")
- Intervention studies in Environmental (search for "cessation", "intervention", "trial")
- Use `qc-grants.md` slash command to help

### 4. Regenerate visualization data

```bash
python scripts/regenerate_viz_data.py
```

This reads all `*_combined.csv` files and creates `sankey_full_data_v2.json`.

### 5. View the Sankey

```bash
open visualization/viz_sankey_with_heatmap.html
```

---

## What Worked and What Didn't

### ✅ Worked
- **Decision tree with strict ordering** — Check infrastructure first, then clinical, then environmental, then mechanistic. Order matters.
- **Sonnet (not Haiku)** — Sonnet followed the logic consistently and handled edge cases better
- **PROJECT_TERMS + PROJECT_TITLE** — Titles alone were ambiguous; PROJECT_TERMS gave enough context
- **Iterative QC** — Sample → find errors → update rules → re-run

### ❌ Didn't work
- **Haiku** — Too aggressive, confidently wrong on edge cases. Would tag mechanism studies as environmental if they mentioned any exposure.
- **Single-pass classification** — Tried to classify all 4 categories at once. Errors cascaded. Two-pass (high-level first, then subgroups) was more reliable.
- **Titles alone** — "Targeting EGFR in lung cancer" could be mechanistic or clinical. Needed PROJECT_TERMS.
- **Trusting the first run** — Every disease area had systematic errors that required manual review and fixes.

---

## Key Finding

**Environmental factors research gets only ~3.4% of funding** ($225.9M of $6.6B) across these 8 disease areas:

| Category | Funding | % |
|----------|---------|---|
| Molecular Mechanisms | $3.3B | 50% |
| Clinical & Other | $2.9B | 44% |
| Environmental Factors | $225.9M | **3.4%** |

---

## Exploratory: Mechanistic Subcategorization

⚠️ **Note:** The `exploratory_mechanistic/` folder contains an exploratory attempt to further subcategorize environmental grants by mechanism (oxidative stress, inflammation, etc.). This was experimental and not used in the final visualization.

Files:
- `sankey_exposure_mechanism.json` — Exposure → Mechanism mapping
- `ENV_Sankey_ExposureMechanism.html` — Visualization attempt
