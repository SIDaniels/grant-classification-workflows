# Federal Agency Comparison: NIH vs EPA vs NSF

**Output:** [engineeredresilience.org/evidence/funding](https://www.engineeredresilience.org/evidence/funding)

## Goal

Show that **less than 1% of NIH funding goes to environmental health research**—and EPA/NSF don't fill the gap. The result: No single federal agency systematically bridges environmental exposures to druggable molecular targets.

---

## The Actual Process (Play-by-Play)

### Step 1: Pulled grant data from each agency

Each agency has different data sources and APIs:

| Agency | Source | Method |
|--------|--------|--------|
| NIH | [NIH Reporter](https://reporter.nih.gov) | Manual export (their API is limited) |
| EPA | [USAspending.gov](https://usaspending.gov) | API via `sources/usaspending.py` |
| NSF | [NSF Awards API](https://nsf.gov/awardsearch) | API via `pull_all_nsf_grants.py` |

**NIH:** Manually searched for environmental health terms on NIH Reporter and exported. This was tedious but necessary because their API doesn't support complex queries well.

**EPA:** Used the USAspending.gov API to get all EPA grants. Most EPA funding goes to monitoring/remediation, not health research.

**NSF:** Used the NSF Awards API to pull grants with environmental/health keywords. NSF has very little health research overall.

### Step 2: Built the classification system

**The question:** Does this grant study how environmental exposures cause disease (environmental health)? Or is it monitoring, remediation, basic research, or clinical?

**Approach:** Hybrid keyword + LLM classifier

1. **Keyword pass first** — Fast, catches ~70% of obvious cases
   - "PFAS toxicity" → Environmental Health
   - "water quality monitoring" → Monitoring/Remediation
   - "clinical trial" → Other

2. **LLM for ambiguous cases** — Sent borderline grants to Sonnet
   - "Environmental factors in cancer progression" — Is that exposure or mechanism?
   - LLM reads the full title + abstract and decides

**What worked:**
- Keyword-first was fast and accurate for obvious cases
- Sonnet handled nuanced distinctions well
- Two-stage approach (keyword → LLM) was efficient

**What didn't work:**
- Haiku was too aggressive—would tag mechanism studies as environmental if they mentioned any pollutant
- Pure keyword matching missed nuanced cases
- NSF abstracts were often too vague to classify confidently

### Step 3: Iterated on classification

Had to refine the categories several times:

**Original attempt:** Binary (Environmental Health vs. Not)
- Problem: Didn't distinguish monitoring from health research

**Final categories:**
```
Environmental Health      — Studying how exposures cause disease
Monitoring & Remediation  — Detection, cleanup, regulatory compliance
All Other Research        — Everything else
```

EPA is mostly Monitoring & Remediation. That's why even though EPA "does environmental stuff," they're not filling the gap in understanding how pollutants cause disease.

### Step 4: Aggregated funding totals

Summed funding by agency × category:

| Agency | Total | Env Health | % |
|--------|-------|------------|---|
| NIH | $167.5B | $1.0B | <1% |
| EPA | $4.3B | $0.3B | ~8% |
| NSF | $8.6B | $0.1B | ~1% |

**The gap:** NIH is the health research agency, but <1% goes to environmental health. EPA focuses on regulatory science, not therapeutic discovery.

### Step 5: Built the Sankey diagram

Used D3.js to show the funding flows visually. The width of each band represents funding amount.

**Output:** `visualization/sankey_mini.html`

---

## File Structure

```
federal_agency_comparison/
├── data/
│   ├── NIH_NSF_EPA.csv                 # Historical funding by agency
│   ├── epa_grants_classified.csv       # EPA grants with categories
│   └── nsf_grants_classified.csv       # NSF grants with categories
│
├── scripts/
│   ├── pull_all_nsf_grants.py          # Fetch NSF data via API
│   ├── pull_nsf_fast.py                # Faster NSF fetch (parallel)
│   ├── classify_all_grants.py          # Batch classification driver
│   ├── classify_batch.py               # Single batch classification
│   ├── classify_hybrid.py              # Hybrid keyword+LLM classifier
│   ├── classify_epa_borderline.py      # EPA edge case handling
│   ├── create_classification_batches.py # Split large files into batches
│   │
│   └── grant_classifier/               # The classifier module
│       ├── __init__.py
│       ├── cli.py                      # Command-line interface
│       ├── classifiers/                # keyword.py, llm.py, hybrid.py
│       ├── sources/                    # nih_reporter.py, nsf.py, usaspending.py
│       ├── configs/                    # Classification configs
│       └── output/                     # Classification results
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

Go to [reporter.nih.gov](https://reporter.nih.gov), search for environmental health terms, export as CSV.

### 4. Classify grants

```bash
# Keyword pass first (fast)
python scripts/classify_hybrid.py --input data/epa_raw.csv --output data/epa_classified.csv

# Or full batch processing
python scripts/classify_all_grants.py --input data/ --output data/classified/
```

### 5. Aggregate and visualize

Sum funding by agency × category, then update the data in `visualization/sankey_mini.html`.

```bash
open visualization/sankey_mini.html
```

---

## What Worked and What Didn't

### ✅ Worked
- **Hybrid keyword + LLM** — Keywords caught obvious cases, LLM handled nuance
- **Sonnet for classification** — Followed instructions well, understood context
- **Separating monitoring from health** — Key insight that EPA does "environmental" but not "health"

### ❌ Didn't work
- **Haiku for classification** — Too aggressive, same problem as NIH disease classification
- **Pure keyword matching** — Missed too many nuanced cases
- **NIH Reporter API** — Limited, had to do manual exports
- **Expecting EPA to fill the gap** — They focus on regulatory compliance, not mechanism discovery

---

## Key Finding

**Less than 1% of NIH funding** ($1.0B of $167.5B) studies how chemical pollutants cause disease.

- NIH: Health agency, but almost no environmental health
- EPA: Environmental agency, but focused on monitoring/cleanup, not health research
- NSF: Basic science, minimal health focus

**The gap:** No single agency systematically bridges environmental exposures → molecular mechanisms → druggable targets.
