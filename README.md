# Grant Classification Workflows

Workflows for classifying federal research grants to identify funding gaps in environmental health research.

**Related:** For the **classified data and gap analysis results**, see the [envirotox repo](https://github.com/SIDaniels/envirotox).

---

## Why Two Different Analyses?

This repo contains two separate analyses that answer different questions:

| Analysis | Question | Finding |
|----------|----------|---------|
| **NIH Disease Classification** | Within NIH disease-specific research, how much studies environmental factors vs. molecular mechanisms? | **3.4%** goes to environmental factors |
| **Federal Agency Comparison** | Across ALL federal funding (NIH + EPA + NSF), who studies how environmental exposures cause disease? | **<1%** of NIH's total budget |

**They're measuring different things:**
- The **disease analysis** looks at ~8,700 grants across 8 diseases (FY2022-2024) and asks: "Is this grant studying the exposure or the mechanism?"
- The **federal comparison** looks at total agency budgets and asks: "How much goes to environmental health research overall?"

Both show the same gap: environmental health research is underfunded.

---

## Quick Start

### Just want to see the visualizations?

```bash
# NIH Disease Classification Sankey
open nih_disease_classification/visualization/viz_sankey_with_heatmap.html

# Federal Agency Comparison Sankey
open federal_agency_comparison/visualization/sankey_mini.html
```

### Want to reproduce the analysis?

See the README in each folder:
- `nih_disease_classification/README.md` — Full workflow for disease classification
- `federal_agency_comparison/README.md` — Full workflow for agency comparison

---

## Folder Structure

```
grant_classification_workflows/
│
├── nih_disease_classification/          # Disease-level analysis
│   ├── README.md                        # Start here
│   ├── data/                            # 8 disease CSVs + Sankey JSON
│   ├── scripts/                         # Classification scripts
│   └── visualization/                   # D3.js Sankey diagram
│
└── federal_agency_comparison/           # Agency-level analysis
    ├── README.md                        # Start here
    ├── data/                            # Agency funding data
    ├── scripts/                         # Classifier module
    └── visualization/                   # Agency comparison Sankey
```

---

## Key Concepts (for newcomers)

### What's "Sonnet" and "Haiku"?

These are [Claude AI models](https://www.anthropic.com/claude) by Anthropic:
- **Claude Sonnet** — More capable, follows complex instructions well. Used for grant classification.
- **Claude Haiku** — Faster and cheaper, but we found it too aggressive for nuanced classification tasks.

### What's PROJECT_TERMS?

A field in NIH Reporter exports that contains MeSH-like keywords describing the grant. Example: `"cancer, lung; smoking; carcinogen; DNA damage"`. This gives more context than the title alone.

### What's a Sankey diagram?

A flow diagram where the width of each band represents quantity (in our case, funding dollars). It shows how funding flows from sources (diseases or agencies) to categories (environmental, mechanistic, etc.).

---

## Requirements

To **view the visualizations**: Just open the HTML files in a browser. No dependencies needed.

To **run the classification scripts**:
- Python 3.8+
- pandas
- An [Anthropic API key](https://console.anthropic.com/) (for LLM classification)

```bash
pip install pandas anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Data Sources

| Source | URL | Used For |
|--------|-----|----------|
| NIH Reporter | [reporter.nih.gov](https://reporter.nih.gov) | NIH grant data (manual export) |
| NSF Awards | [nsf.gov/awardsearch](https://www.nsf.gov/awardsearch/) | NSF grant data (API) |
| USAspending | [usaspending.gov](https://www.usaspending.gov) | EPA grant data (API) |

---

## Key Findings

### NIH Disease Classification (FY2022-2024)

Across 8 disease areas (~8,700 grants, $6.6B):

| Category | Funding | % |
|----------|---------|---|
| Molecular Mechanisms | $3.3B | 50% |
| Clinical & Other | $2.9B | 44% |
| Environmental Factors | $225.9M | **3.4%** |

### Federal Agency Comparison (cumulative)

| Agency | Total Budget | Env Health Research | % |
|--------|--------------|---------------------|---|
| NIH | $167.5B | $1.0B | <1% |
| EPA | $4.3B | $0.3B | ~8% |
| NSF | $8.6B | $0.1B | ~1% |

**The gap:** No single federal agency systematically bridges environmental exposures → molecular mechanisms → druggable targets.

---

## What Worked and What Didn't

### Worked
- **Decision tree with strict ordering** — Check categories in a specific order to avoid ambiguity
- **Claude Sonnet** — Followed complex instructions consistently
- **Hybrid keyword + LLM** — Keywords for obvious cases, LLM for ambiguous ones
- **Iterative QC** — Every disease area had errors that required manual review

### Didn't Work
- **Claude Haiku** — Too aggressive, confidently misclassified edge cases
- **Titles alone** — Needed PROJECT_TERMS for context
- **Single-pass classification** — Two-pass (high-level then subgroups) was more reliable
