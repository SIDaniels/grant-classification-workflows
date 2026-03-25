# NIH Disease Funding Visualization

Reproduces: [engineeredresilience.org/evidence/methods/nih](https://www.engineeredresilience.org/evidence/methods/nih)

## What This Shows

An interactive Sankey diagram showing NIH funding flow across 8 disease areas to 3 research focus categories:
- **Molecular Mechanisms** (~$3.3B) — biological pathways, genetic factors, protein function
- **Clinical Research and Other** (~$2.9B) — clinical trials, screening, training grants
- **Environmental Factors** (~$225.9M) — environmental exposures as disease risk factors

**Key Finding:** Environmental factors research receives only ~3.4% of funding, even for diseases where environmental exposures are major risk factors.

## Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SOURCE DATA                                  │
├─────────────────────────────────────────────────────────────────────┤
│  NIH Reporter exports for 8 disease areas:                          │
│  Breast Cancer, Colorectal Cancer, Lung Cancer, ALS,                │
│  Parkinson's, Liver Disease, Contraception, Biodefense              │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CLASSIFICATION                                  │
├─────────────────────────────────────────────────────────────────────┤
│  Each grant classified into:                                         │
│  ├── Strictly_Environmental                                          │
│  ├── Mechanistic_Pathogenesis                                        │
│  ├── Strictly_Genetic                                                │
│  └── Everything_else (clinical, infrastructure)                      │
│                                                                      │
│  Using: nih_mechanism_classification/ workflow                       │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AGGREGATION                                     │
├─────────────────────────────────────────────────────────────────────┤
│  regenerate_viz_data.py → sankey_full_data_v2.json                  │
│  Aggregates grant counts and funding by disease × category          │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      VISUALIZATION                                   │
├─────────────────────────────────────────────────────────────────────┤
│  nih_disease_funding_widget.html — Bar chart by disease             │
│  viz_sankey_with_heatmap.html — Sankey + heatmap                    │
│  ENV_Sankey_FullGap_v2.html — Gap analysis view                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Files

```
nih_disease_viz/
├── regenerate_viz_data.py           # Script to generate JSON from CSVs
├── data/
│   ├── sankey_full_data_v2.json     # Aggregated data for Sankey
│   ├── viz_data_dollars.json        # Funding amounts
│   └── disease_grants/              # Source: classified grants by disease
│       ├── ALS_combined.csv
│       ├── Biodefense_combined.csv
│       ├── Breast_Cancer_combined.csv
│       ├── Colorectal_Cancer_combined.csv
│       ├── Contraception_Reproduction_combined.csv
│       ├── Liver_Disease_combined.csv
│       ├── Lung_Cancer_combined.csv
│       └── Parkinsons_combined.csv
└── visualization/
    ├── nih_disease_funding_widget.html  # Bar chart widget
    ├── viz_sankey_with_heatmap.html     # Sankey + heatmap
    └── ENV_Sankey_FullGap_v2.html       # Gap analysis Sankey
```

## How to Reproduce

### 1. Get NIH disease grants

Download from [NIH Reporter](https://reporter.nih.gov) for each disease area:
- Search: "Breast Cancer", "ALS", etc.
- Export as CSV

### 2. Classify the grants

Use the `nih_mechanism_classification/` workflow:
```bash
python nih_mechanism_classification/scripts/classify_by_exposure.py Breast_Cancer.csv
```

This classifies each grant as:
- `Strictly_Environmental` — exposure focus
- `Mechanistic_Pathogenesis` — mechanism focus
- `Strictly_Genetic` — genetic risk focus
- `Everything_else` — clinical, infrastructure

### 3. Regenerate the visualization data

```bash
python regenerate_viz_data.py
```

This reads the `*_combined.csv` files and outputs:
- `sankey_full_data_v2.json` — for the Sankey diagram
- `viz_data_dollars.json` — funding amounts

### 4. View locally

```bash
open visualization/viz_sankey_with_heatmap.html
# Or serve with Python
python -m http.server 8000
```

## Disease Areas Covered

| Disease | Grants | Total Funding | Env % |
|---------|--------|---------------|-------|
| Breast Cancer | ~2,500 | $800M | 2.1% |
| Lung Cancer | ~1,800 | $600M | 4.3% |
| Colorectal Cancer | ~900 | $300M | 1.8% |
| ALS | ~400 | $150M | 3.2% |
| Parkinson's | ~600 | $200M | 5.1% |
| Liver Disease | ~1,200 | $400M | 4.8% |
| Contraception | ~500 | $180M | 2.5% |
| Biodefense | ~800 | $350M | 1.2% |

## Classification Schema

```
For each grant:
│
├─► Infrastructure/admin? → Everything_else
├─► Clinical intervention? → Everything_else
├─► Environmental exposure focus? → Strictly_Environmental
├─► Molecular mechanism focus? → Mechanistic_Pathogenesis
├─► Genetic risk only? → Strictly_Genetic
└─► Default → Everything_else
```

See `nih_mechanism_classification/methodology/` for full decision tree.
