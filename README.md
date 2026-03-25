# Grant Classification Workflows

Workflows for classifying research grants and reproducing the funding gap visualizations.

**Related:** For the **classified data and gap analysis results**, see the [envirotox repo](https://github.com/SIDaniels/envirotox).

---

## What's In This Repo

Two workflows to reproduce two visualizations:

| Visualization | Folder | URL |
|---------------|--------|-----|
| NIH Disease Classification Sankey | `nih_disease_classification/` | [/evidence/methods/nih](https://www.engineeredresilience.org/evidence/methods/nih) |
| Federal Agency Comparison Sankey | `federal_agency_comparison/` | [/evidence/funding](https://www.engineeredresilience.org/evidence/funding) |

---

## Folder Structure

```
grant_classification_workflows/
│
├── nih_disease_classification/          # → /evidence/methods/nih
│   ├── README.md                        # ⭐ Start here
│   ├── data/
│   │   ├── ALS_combined.csv             # Classified grants by disease
│   │   ├── Breast_Cancer_combined.csv
│   │   ├── ...
│   │   └── sankey_full_data_v2.json     # Aggregated Sankey data
│   ├── scripts/
│   │   ├── classification_guide.md      # Full decision tree (1300 lines)
│   │   ├── classify_by_exposure.py      # Main classification script
│   │   └── regenerate_viz_data.py       # Generate Sankey JSON
│   ├── visualization/
│   │   └── viz_sankey_with_heatmap.html # Main Sankey diagram
│   └── exploratory_mechanistic/         # Experimental (not in final viz)
│
└── federal_agency_comparison/           # → /evidence/funding
    ├── README.md                        # ⭐ Start here
    ├── data/
    │   ├── NIH_NSF_EPA.csv              # Historical funding by agency
    │   └── *_grants_classified.csv      # Classified grants
    ├── scripts/
    │   ├── classify_hybrid.py           # Hybrid keyword+LLM classifier
    │   ├── pull_all_nsf_grants.py       # Fetch NSF data
    │   └── grant_classifier/            # Classifier module
    └── visualization/
        └── sankey_mini.html             # Agency comparison Sankey
```

---

## Quick Start

### NIH Disease Classification

Shows that **~3.4% of NIH funding** goes to environmental factors research across 8 disease areas.

```bash
cd nih_disease_classification

# View the visualization
open visualization/viz_sankey_with_heatmap.html

# Or regenerate from data
python scripts/regenerate_viz_data.py
```

See `nih_disease_classification/README.md` for the full workflow.

### Federal Agency Comparison

Shows that **<1% of NIH funding** goes to environmental health research—and EPA/NSF don't fill the gap.

```bash
cd federal_agency_comparison

# View the visualization
open visualization/sankey_mini.html
```

See `federal_agency_comparison/README.md` for the full workflow.

---

## Key Findings

### NIH Disease Classification

Across 8 disease areas (ALS, breast cancer, colorectal cancer, liver disease, lung cancer, Parkinson's, biodefense, contraception):

| Category | Funding | % |
|----------|---------|---|
| Molecular Mechanisms | $3.3B | 50% |
| Clinical & Other | $2.9B | 44% |
| Environmental Factors | $225.9M | **3.4%** |

### Federal Agency Comparison

| Agency | Total | Env Health | % |
|--------|-------|------------|---|
| NIH | $167.5B | $1.0B | <1% |
| EPA | $4.3B | $0.3B | ~8% |
| NSF | $8.6B | $0.1B | ~1% |

**The gap:** No single federal agency systematically bridges environmental exposures → molecular mechanisms → druggable targets.

---

## What Worked and What Didn't

### ✅ Worked
- **Decision tree with strict ordering** — Check infrastructure first, then clinical, then environmental, then mechanistic
- **Sonnet (not Haiku)** — Followed instructions consistently, handled edge cases
- **Hybrid keyword + LLM** — Keywords caught obvious cases, LLM handled nuance
- **Iterative QC** — Every disease area had systematic errors that required manual review

### ❌ Didn't Work
- **Haiku** — Too aggressive, confidently misclassified edge cases
- **Pure keyword matching** — Missed too many nuanced cases
- **Titles alone** — Needed PROJECT_TERMS for accuracy
- **Single-pass classification** — Errors cascaded; two-pass was more reliable

---

## Data Sources

| Source | URL |
|--------|-----|
| NIH Reporter | [reporter.nih.gov](https://reporter.nih.gov) |
| NSF Awards | [nsf.gov/awardsearch](https://www.nsf.gov/awardsearch/) |
| USAspending (EPA) | [usaspending.gov](https://www.usaspending.gov) |
