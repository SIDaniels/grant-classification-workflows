# NIH Disease Classification: Molecular vs Environmental vs Clinical

**Output:** [engineeredresilience.org/evidence/methods/nih](https://www.engineeredresilience.org/evidence/methods/nih)

## Goal

Show that **environmental factors research gets only ~3.4% of NIH funding** across 8 disease areas—even for diseases where environmental exposures are known major risk factors (like lung cancer and smoking, or Parkinson's and pesticides).

**Time period:** FY2022-2024 grants from NIH Reporter

---

## The Four Categories

Every grant is classified into one of these categories:

| Category | What it means | Examples |
|----------|---------------|----------|
| **Strictly_Environmental** | Studies an environmental EXPOSURE as the main focus | "PFAS exposure and thyroid cancer risk", "Gut microbiome in Parkinson's" |
| **Mechanistic_Pathogenesis** | Studies molecular/cellular MECHANISMS | "Role of KRAS in lung cancer", "DNA repair pathways" |
| **Strictly_Genetic** | Studies inherited genetic risk (GWAS, germline) | "Familial breast cancer mutations", "Genetic susceptibility loci" |
| **Everything_else** | Infrastructure, clinical trials, behavioral interventions | "Cancer center core", "Smoking cessation trial", "Screening program" |

**The key question:** Is the grant studying the EXPOSURE or the MECHANISM?
- "Arsenic exposure and cancer risk" → **Environmental** (exposure is the focus)
- "How arsenic damages DNA" → **Mechanistic** (mechanism is the focus)

---

## The Actual Process (Play-by-Play)

### Step 1: Downloaded NIH grants by disease area

Went to [NIH Reporter](https://reporter.nih.gov) and searched for each disease. Exported to CSV with these fields:
- `APPLICATION_ID` — Unique grant identifier
- `PROJECT_TITLE` — Grant title
- `PROJECT_TERMS` — MeSH-like keywords (e.g., "cancer; smoking; DNA damage")
- `TOTAL_COST` — Funding amount

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

**The challenge:** How do you distinguish "environmental" from "mechanistic" research when many grants mention both?
- "Role of arsenic in oxidative stress" — Is that environmental (arsenic) or mechanistic (oxidative stress)?
- "Gut microbiome and colorectal cancer" — Environmental exposure or mechanism study?

**First attempt (failed):** Used Claude Haiku (a faster/cheaper AI model) for classification. It was too aggressive and confidently misclassified edge cases. Many mechanism studies got tagged as environmental because they mentioned an exposure.

**What worked:** Switched to Claude Sonnet (more capable AI model) with a strict decision tree that checks categories IN ORDER:

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

The order matters! Infrastructure and clinical grants get filtered out first, before we even ask "environmental or mechanistic?"

### Step 3: Ran classification on each disease file

Used `classify_by_exposure.py` which sends batches of grants to Claude Sonnet via the Anthropic API.

**Important:** Classification required both PROJECT_TITLE and PROJECT_TERMS. Titles alone were too ambiguous.

Each disease area needed QC. Found systematic errors:
- "Everything_else → Mechanistic" was the most common fix (grants studying pathways got missed)
- Had to search for keywords like "kinase", "pathway", "signaling" in Everything_else and reclassify
- Microbiome studies stayed Environmental even when studying mechanisms (policy decision)

See `scripts/classification_guide.md` for the full 1300-line decision tree with lessons learned from each disease.

### Step 4: QC and iteration (this took a while)

For each disease area:
1. Run initial classification
2. Sample 20-50 grants from each category and review
3. Find systematic errors (e.g., all "kinase" studies were in Everything_else)
4. Update the decision tree with new rules
5. Re-run or manually fix

**Common error patterns:**
- Grants with "role of [protein]" or "mechanism of" got tagged Everything_else → should be Mechanistic
- Grants with "targeting [protein]" got tagged Genetic → should be Mechanistic
- Smoking cessation *interventions* got tagged Environmental → should be Everything_else
- Microbiome grants studying mechanisms were borderline → decided to keep as Environmental

### Step 5: Generated Sankey data

Once classifications were stable, aggregated counts and funding by disease × category:

```bash
python scripts/regenerate_viz_data.py
```

**Output:** `data/sankey_full_data_v2.json`

### Step 6: Built the D3.js visualization

The Sankey diagram shows funding flowing from diseases (left) to research categories (right). Band width = funding amount.

**Output:** `visualization/viz_sankey_with_heatmap.html`

---

## Requirements

To **view the visualization**: Just open the HTML file in a browser. No dependencies needed.

To **run classification scripts**:
```bash
pip install pandas anthropic

# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-key-here"
```

---

## File Structure

```
nih_disease_classification/
├── data/
│   ├── ALS_combined.csv                    # Classified grants (has Category column)
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
│   ├── classification_guide.md             # Full decision tree (1300 lines)
│   ├── environmental_classification_methodology.md
│   ├── classify_by_exposure.py             # Main classification script
│   ├── classify_mechanistic_final.py       # Mechanistic subgroup classifier
│   ├── classify_clinical_final.py          # Clinical subgroup classifier
│   └── regenerate_viz_data.py              # Generate Sankey JSON from CSVs
│
├── visualization/
│   ├── viz_sankey_with_heatmap.html        # Main Sankey diagram
│   └── nih_disease_funding_widget.html     # Alternative widget version
│
└── exploratory_mechanistic/                # Experimental (not in final viz)
    ├── sankey_exposure_mechanism.json
    └── ENV_Sankey_ExposureMechanism.html
```

---

## To Reproduce

### 1. Download grants from NIH Reporter

Go to [reporter.nih.gov](https://reporter.nih.gov):
1. Search for a disease (e.g., "lung cancer")
2. Filter by fiscal year (we used FY2022-2024)
3. Export as CSV
4. Make sure to include: APPLICATION_ID, PROJECT_TITLE, PROJECT_TERMS, TOTAL_COST

### 2. Classify grants

```bash
python scripts/classify_by_exposure.py data/Lung_Cancer.csv
```

This adds a `Category` column to each row with one of: Strictly_Genetic, Strictly_Environmental, Mechanistic_Pathogenesis, or Everything_else.

**Note:** This requires an Anthropic API key and will make API calls to Claude Sonnet.

### 3. QC the results

Sample 20-50 grants from each category and verify. Look for:
- Mechanism studies in Everything_else (search for "kinase", "pathway", "signaling")
- Intervention studies in Environmental (search for "cessation", "intervention", "trial")

### 4. Regenerate visualization data

```bash
python scripts/regenerate_viz_data.py
```

This reads all `*_combined.csv` files and creates `sankey_full_data_v2.json`.

### 5. View the Sankey

```bash
open visualization/viz_sankey_with_heatmap.html
```

Or just double-click the HTML file to open in your browser.

---

## What Worked and What Didn't

### Worked
- **Decision tree with strict ordering** — Check infrastructure first, then clinical, then environmental, then mechanistic. Order matters.
- **Claude Sonnet** — Followed the logic consistently and handled edge cases better than Haiku
- **PROJECT_TERMS + PROJECT_TITLE** — Titles alone were ambiguous; PROJECT_TERMS gave enough context
- **Iterative QC** — Sample → find errors → update rules → re-run

### Didn't Work
- **Claude Haiku** — Too aggressive, confidently wrong on edge cases. Would tag mechanism studies as environmental if they mentioned any exposure.
- **Single-pass classification** — Tried to classify all 4 categories at once. Errors cascaded. Two-pass (high-level first, then subgroups) was more reliable.
- **Titles alone** — "Targeting EGFR in lung cancer" could be mechanistic or clinical. Needed PROJECT_TERMS.
- **Trusting the first run** — Every disease area had systematic errors that required manual review.

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

The `exploratory_mechanistic/` folder contains an experimental attempt to further subcategorize environmental grants by mechanism (oxidative stress, inflammation, etc.). This was not used in the final visualization.
