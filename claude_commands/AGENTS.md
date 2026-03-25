# Grant Categorization Project

## Project Overview

This project classifies NIH, DOE, and EPA research grants into four categories based on their research focus:
- **Strictly_Genetic** - Inherited genetics, germline mutations, GWAS
- **Strictly_Environmental_or_Gene-Environment** - Environmental exposures, lifestyle factors, gene-environment interactions
- **Mechanistic_Pathogenesis** - Molecular/cellular mechanisms of disease
- **Everything_else** - Clinical trials, behavioral interventions, infrastructure

## Key Files

- `classification_guide.md` - Complete decision rules and lessons learned
- `biotech_grants_categorized.csv` - Biotechnology grants with categories
- `disease_by_exposures/` - Grants organized by exposure type
- `external_grants_DOE_EPA.csv` - Non-NIH grants

## Data Sources

- NIH RePORTER (FY2022-2025)
- DOE SBIR grants
- EPA environmental grants
- SBIR data (`sbir_data/`)

## Classification Workflow

1. Load grant data (CSV with Title, Abstract, Funding info)
2. Apply decision tree from `classification_guide.md`
3. Tag Environmental grants with one of 10 subgroups
4. Run QC searches to catch misclassifications
5. Manual review of flagged grants
6. Generate visualizations

## Slash Commands

- `/classify-grants [file.csv]` - Classify a new grant dataset
- `/qc-grants [file.csv]` - QC an already-classified dataset

## Common Patterns

### Always Mechanistic:
- "Role of [protein]"
- "Mechanism of [process]"
- "Targeting [protein]"
- Kinase/pathway/signaling studies

### Always Environmental:
- Microbiome/gut-brain studies
- Exposure epidemiology
- Gene-environment interactions

### Always Everything_else:
- Clinical trials
- Behavioral interventions
- Infrastructure/cores
- Training programs
