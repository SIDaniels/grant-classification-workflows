# Federal Agency Comparison: NIH vs EPA vs NSF

**Output:** [engineeredresilience.org/evidence/funding](https://www.engineeredresilience.org/evidence/funding)

## Goal

Show that **less than 1% of NIH funding goes to environmental health research**—and EPA/NSF don't fill the gap.

**The question:** Across all federal funding, who studies how environmental exposures cause disease?

**Time period:** Cumulative agency budgets (historical totals)

---

## The Three Categories

| Category | What it means | Examples |
|----------|---------------|----------|
| **Environmental Health** | Studies how exposures cause disease | "PFAS and thyroid cancer", "Lead neurotoxicity mechanisms" |
| **Monitoring & Remediation** | Detection, cleanup, regulatory compliance | "Water quality sensors", "Superfund site remediation" |
| **All Other Research** | Everything else | "Clinical trials", "Basic cell biology", "Behavioral studies" |

**Key insight:** EPA does "environmental stuff" but mostly monitoring/cleanup—not health research. That's why they don't fill the gap.

---

## The Actual Process (Play-by-Play)

### Step 1: Pulled grant data from each agency

Each agency has different data sources:

| Agency | Source | Method |
|--------|--------|--------|
| NIH | [NIH Reporter](https://reporter.nih.gov) | Manual export (their API has limitations) |
| EPA | [USAspending.gov](https://usaspending.gov) | API via `scripts/grant_classifier/sources/usaspending.py` |
| NSF | [NSF Awards API](https://nsf.gov/awardsearch) | API via `scripts/pull_all_nsf_grants.py` |

**NIH:** Manually searched for environmental health terms on NIH Reporter and exported. Tedious but necessary because their API doesn't support complex queries well.

**EPA:** Used the USAspending.gov API to get all EPA grants. Found that most EPA funding goes to monitoring/remediation, not health research.

**NSF:** Used the NSF Awards API to pull grants with environmental/health keywords. NSF has very little health research overall.

### Step 2: Built the classification system

**Approach:** Hybrid keyword + LLM classifier

1. **Keyword pass first** (~70% of grants)
   - "PFAS toxicity" → Environmental Health
   - "water quality monitoring" → Monitoring/Remediation
   - "clinical trial" → Other

2. **LLM for ambiguous cases** (~30% of grants)
   - Sent borderline grants to Claude Sonnet (Anthropic's AI model)
   - "Environmental factors in cancer progression" — exposure or mechanism?
   - LLM reads title + abstract and decides

**Why hybrid?** Pure keywords miss nuance. Pure LLM is slow and expensive. Hybrid gets best of both.

### Step 3: Iterated on categories

**Original attempt:** Binary (Environmental Health vs. Not)
- Problem: Lumped monitoring with health research

**Final categories:** Split EPA's work into "Monitoring & Remediation" vs. "Environmental Health"

This made the gap clearer: EPA does environmental monitoring, but not health research.

### Step 4: Aggregated funding totals

| Agency | Total Budget | Env Health | % |
|--------|--------------|------------|---|
| NIH | $167.5B | $1.0B | <1% |
| EPA | $4.3B | $0.3B | ~8% |
| NSF | $8.6B | $0.1B | ~1% |

### Step 5: Built the Sankey diagram

D3.js visualization showing funding flows. Band width = funding amount.

**Output:** `visualization/sankey_mini.html`

---

## Requirements

To **view the visualization**: Just open the HTML file in a browser. No dependencies needed.

To **run classification scripts**:
```bash
pip install pandas anthropic requests

# Set your Anthropic API key (for LLM classification)
export ANTHROPIC_API_KEY="your-key-here"
```

---

## File Structure

```
federal_agency_comparison/
├── data/
│   ├── NIH_NSF_EPA.csv                 # Historical funding by agency
│   ├── epa_grants_classified.csv       # Sample of classified EPA grants
│   └── nsf_grants_classified.csv       # Sample of classified NSF grants
│
├── scripts/
│   ├── pull_all_nsf_grants.py          # Fetch NSF data via API
│   ├── pull_nsf_fast.py                # Parallel version (faster)
│   ├── classify_all_grants.py          # Batch classification driver
│   ├── classify_batch.py               # Single batch classification
│   ├── classify_hybrid.py              # Hybrid keyword+LLM classifier
│   ├── classify_epa_borderline.py      # EPA edge cases
│   ├── create_classification_batches.py
│   │
│   └── grant_classifier/               # The classifier module
│       ├── __init__.py
│       ├── cli.py                      # Command-line interface
│       ├── classifiers/
│       │   ├── keyword.py              # Keyword-based classification
│       │   ├── llm.py                  # LLM-based classification
│       │   └── hybrid.py               # Combined approach
│       ├── sources/
│       │   ├── nih_reporter.py         # NIH Reporter API
│       │   ├── nsf.py                  # NSF Awards API
│       │   └── usaspending.py          # USAspending API (EPA)
│       └── configs/
│
└── visualization/
    └── sankey_mini.html                # D3.js Sankey diagram
```

---

## To Reproduce

### 1. Pull NSF grants

```bash
python scripts/pull_all_nsf_grants.py --keywords "environmental health,toxicology,pollution" --output data/nsf_raw.csv
```

### 2. Pull EPA grants

```bash
python scripts/grant_classifier/sources/usaspending.py --agency EPA --output data/epa_raw.csv
```

### 3. Pull NIH grants

Go to [reporter.nih.gov](https://reporter.nih.gov), search for environmental health terms, and export as CSV.

### 4. Classify grants

```bash
# Hybrid classifier (keyword first, then LLM for ambiguous)
python scripts/classify_hybrid.py --input data/epa_raw.csv --output data/epa_classified.csv
```

**Note:** LLM classification requires an Anthropic API key.

### 5. Aggregate and visualize

The Sankey data is hardcoded in `visualization/sankey_mini.html`. To update:
1. Sum funding by agency × category from your classified files
2. Edit the `data` object in the HTML file

```bash
open visualization/sankey_mini.html
```

---

## What Worked and What Didn't

### Worked
- **Hybrid keyword + LLM** — Keywords for obvious cases, LLM for nuance
- **Claude Sonnet** — Followed classification instructions well
- **Separating monitoring from health** — Made EPA's role clear

### Didn't Work
- **Claude Haiku** — Too aggressive, misclassified edge cases (same problem as disease classification)
- **Pure keyword matching** — Missed too many nuanced cases
- **NIH Reporter API** — Limited query support, had to do manual exports
- **Expecting EPA to fill the gap** — They focus on regulatory compliance, not mechanism discovery

---

## Key Finding

**Less than 1% of NIH funding** ($1.0B of $167.5B) studies how chemical pollutants cause disease.

| Agency | Role | Gap |
|--------|------|-----|
| NIH | Health research | Almost no environmental health |
| EPA | Environmental agency | Monitoring/cleanup, not health research |
| NSF | Basic science | Minimal health focus |

**The gap:** No single federal agency systematically bridges environmental exposures → molecular mechanisms → druggable targets.
