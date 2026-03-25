# Federal Funding Visualization (NIH/EPA/NSF)

Reproduces: [engineeredresilience.org/evidence/funding](https://www.engineeredresilience.org/evidence/funding)

## What This Shows

An interactive Sankey diagram showing how federal research funding flows from three agencies (NIH, EPA, NSF) to research categories:
- **All Other Research** — non-environmental
- **Monitoring & Remediation** — detection and cleanup
- **Environmental Health** — biological effects of pollutants

**Key Finding:** Less than 1% of NIH funding ($1.0B of $167.5B) studies how chemical pollutants cause disease.

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SOURCE DATA                                  │
├─────────────────────────────────────────────────────────────────────┤
│  NIH: NIH Reporter API → classified by mechanism                    │
│  EPA: USAspending.gov → classified by focus area                    │
│  NSF: NSF Awards API → classified by focus area                     │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AGGREGATION                                     │
├─────────────────────────────────────────────────────────────────────┤
│  data/NIH_NSF_EPA.csv — Historical funding by agency (FY1938-2025)  │
│  data/agency_grants/ — Classified grants by agency                  │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      VISUALIZATION                                   │
├─────────────────────────────────────────────────────────────────────┤
│  visualization/sankey_mini.html — D3.js Sankey diagram              │
│  visualization/funding_content.html — Page content wrapper          │
└─────────────────────────────────────────────────────────────────────┘
```

## Files

```
federal_funding_viz/
├── data/
│   ├── NIH_NSF_EPA.csv              # Historical funding by agency
│   └── agency_grants/
│       ├── epa_grants_sample.csv    # EPA classified grants (sample)
│       └── nsf_grants_sample.csv    # NSF classified grants (sample)
└── visualization/
    ├── sankey_mini.html             # D3.js Sankey diagram
    └── funding_content.html         # Page content
```

## How to Reproduce

### 1. Get the raw data

**NIH:**
```bash
# Use NIH Reporter API or download from reporter.nih.gov
# Classify using nih_mechanism_classification/ workflow
```

**EPA:**
```bash
# Use USAspending.gov API
python fed_grant_cats/grant_classifier/sources/usaspending.py
# Classify using fed_grant_cats/ workflow
```

**NSF:**
```bash
# Use NSF Awards API
python fed_grant_cats/scripts/pull_all_nsf_grants.py
# Classify using fed_grant_cats/ workflow
```

### 2. Aggregate funding totals

Sum funding by agency and category:
- Environmental Health
- Monitoring & Remediation
- All Other

### 3. Update the visualization

Edit `visualization/sankey_mini.html` with new funding totals in the `data` object.

### 4. View locally

```bash
open visualization/sankey_mini.html
# Or serve with Python
python -m http.server 8000
```

## Data Sources

| Agency | Source | Classification Method |
|--------|--------|----------------------|
| NIH | [reporter.nih.gov](https://reporter.nih.gov) | LLM + decision tree |
| EPA | [usaspending.gov](https://usaspending.gov) | Keyword + LLM hybrid |
| NSF | [nsf.gov/awardsearch](https://nsf.gov/awardsearch) | Keyword + LLM hybrid |
