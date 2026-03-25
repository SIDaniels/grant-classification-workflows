# Grant Classification Workflows

Two workflows for classifying research grants by mechanism of harm and exposure type.

**Note:** This repo contains the **classification workflows** (scripts, methodology, prompts). For the **classified data and gap analysis**, see the [envirotox repo](https://github.com/SIDaniels/envirotox).

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW 1: NIH Mechanism Classification         │
├─────────────────────────────────────────────────────────────────────┤
│  Input: NIH Reporter grant exports                                   │
│  Output: Grants classified by mechanism (mito, inflammation, etc.)   │
│  Method: Claude + decision tree prompts                              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW 2: Federal Grant Categorization         │
├─────────────────────────────────────────────────────────────────────┤
│  Input: NIH, EPA, NSF grant data                                     │
│  Output: Grants classified by therapeutic category                   │
│  Method: Hybrid keyword + LLM classifier                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
grant_classification_workflows/
├── README.md
│
├── nih_mechanism_classification/     # Workflow 1: NIH by mechanism
│   ├── methodology/                  # Classification guides & decision trees
│   │   ├── classification_guide.md
│   │   ├── environmental_classification_methodology.md
│   │   ├── mechanistic_subcategory_methodology.md
│   │   └── GapAnalysis_Methodology.md
│   ├── scripts/                      # Core classification scripts
│   │   ├── classify_by_exposure.py
│   │   ├── classify_mechanistic_final.py
│   │   ├── classify_clinical_final.py
│   │   └── classify_all_mechanistic.py
│   └── qc/                           # Quality control & validation
│       ├── spot_check_comprehensive.py
│       ├── manual_sample_review.py
│       └── fix_miscategorized_v2.py
│
├── fed_grant_cats/                   # Workflow 2: Multi-agency (NIH/EPA/NSF)
│   ├── grant_classifier/             # Python classifier module
│   │   ├── classifiers/              # Classification strategies
│   │   │   ├── keyword.py            # Keyword-based classification
│   │   │   ├── llm.py                # LLM-based classification
│   │   │   ├── hybrid.py             # Combined approach
│   │   │   └── crosswalk.py          # Mechanism crosswalk
│   │   ├── sources/                  # Data source connectors
│   │   │   ├── nih_reporter.py       # NIH Reporter API
│   │   │   ├── nsf.py                # NSF Awards API
│   │   │   ├── usaspending.py        # USAspending (EPA)
│   │   │   └── grants_gov.py         # Grants.gov
│   │   └── cli.py                    # Command-line interface
│   ├── scripts/                      # Batch processing scripts
│   │   ├── classify_all_grants.py
│   │   ├── pull_all_nsf_grants.py
│   │   └── classify_batch.py
│   └── README.md
│
├── claude_commands/                  # Claude Code slash commands
│   ├── classify-grants.md            # /classify-grants workflow
│   └── qc-grants.md                  # /qc-grants workflow
│
└── sample_data/                      # Example inputs/outputs
    ├── nih/
    │   └── sample_mechanism_classified.csv
    └── federal/
        ├── sample_epa_grants.csv
        └── sample_nsf_grants.csv
```

---

## Workflow 1: NIH Mechanism Classification

### Purpose
Classify NIH environmental health grants by their **mechanism of harm** (e.g., oxidative stress, inflammation, epigenetic changes).

### Data Flow

```
NIH Reporter Export (.csv)
         │
         ▼
┌─────────────────────────┐
│  Step 1: High-Level     │
│  Classification         │
│  ├── Environmental      │
│  ├── Mechanistic        │
│  ├── Genetic            │
│  └── Everything_else    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Step 2: Subgroup       │
│  Classification         │
│  ├── Mitochondrial      │
│  ├── Inflammation       │
│  ├── Epigenetic         │
│  ├── DNA Damage         │
│  └── ...                │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Step 3: QC & Fixes     │
│  ├── Spot check sample  │
│  ├── Fix edge cases     │
│  └── Manual review      │
└───────────┬─────────────┘
            │
            ▼
    Classified Grants CSV
```

### How to Run

1. **Get NIH data** from [reporter.nih.gov](https://reporter.nih.gov)
   - Search for environmental health terms
   - Export as CSV

2. **Run high-level classification:**
   ```bash
   python nih_mechanism_classification/scripts/classify_by_exposure.py input.csv
   ```

3. **Run mechanism subclassification:**
   ```bash
   python nih_mechanism_classification/scripts/classify_mechanistic_final.py input.csv
   ```

4. **QC the results:**
   ```bash
   python nih_mechanism_classification/qc/spot_check_comprehensive.py output.csv
   ```

### Classification Categories

**High-Level:**
| Category | Description |
|----------|-------------|
| Strictly_Environmental | Focus on environmental exposure |
| Mechanistic_Pathogenesis | Focus on molecular/cellular mechanisms |
| Strictly_Genetic | Focus on genetic risk (GWAS, germline) |
| Everything_else | Infrastructure, clinical trials, etc. |

**Mechanism Subgroups:**
- Mitochondrial_Dysfunction
- Inflammation_Pathway
- Epigenetic_Changes
- DNA_Repair_Damage
- Endocrine_Hormonal
- Senescence_Aging
- Microbiome
- ... (see methodology docs for full list)

---

## Workflow 2: Federal Grant Categorization (NIH/EPA/NSF)

### Purpose
Classify grants from multiple federal agencies by **therapeutic category** to identify research gaps.

### Data Sources

| Agency | Source | Connector |
|--------|--------|-----------|
| NIH | NIH Reporter API | `sources/nih_reporter.py` |
| NSF | NSF Awards API | `sources/nsf.py` |
| EPA | USAspending.gov | `sources/usaspending.py` |

### Classification Strategies

The `grant_classifier` module supports three approaches:

1. **Keyword** (`classifiers/keyword.py`)
   - Fast, rule-based matching
   - Good for clear categories

2. **LLM** (`classifiers/llm.py`)
   - Uses Claude for nuanced classification
   - Better for ambiguous grants

3. **Hybrid** (`classifiers/hybrid.py`)
   - Keyword first, LLM for uncertain cases
   - Best balance of speed and accuracy

### How to Run

1. **Pull grant data:**
   ```bash
   # NSF grants
   python fed_grant_cats/scripts/pull_all_nsf_grants.py

   # EPA grants (via USAspending)
   # See sources/usaspending.py for API setup
   ```

2. **Classify grants:**
   ```bash
   python fed_grant_cats/grant_classifier/cli.py \
     --input grants.csv \
     --strategy hybrid \
     --output classified.csv
   ```

3. **Batch processing:**
   ```bash
   python fed_grant_cats/scripts/classify_batch.py \
     --input-dir ./raw_grants \
     --output-dir ./classified
   ```

---

## Claude Commands

These are [Claude Code](https://claude.com/code) slash commands used during development.

### `/classify-grants`
Runs the full classification workflow on a CSV file.

**Usage:**
```
/classify-grants path/to/grants.csv
```

**What it does:**
1. Reads the CSV
2. Applies the decision tree (see `claude_commands/classify-grants.md`)
3. Outputs classified CSV with Category, Subgroup, Confidence, Rationale

### `/qc-grants`
Quality-checks classified grants.

**Usage:**
```
/qc-grants path/to/classified.csv
```

---

## Decision Tree (High-Level)

```
For each grant:
│
├─► Is it infrastructure/admin (cores, training, conferences)?
│   └─► YES → Everything_else
│
├─► Is it a clinical intervention (trial, treatment, cessation)?
│   └─► YES → Everything_else
│
├─► Is the PRIMARY focus on an environmental EXPOSURE?
│   │   (chemicals, PFAS, microbiome, diet, smoking, pollution)
│   └─► YES → Strictly_Environmental
│
├─► Is the PRIMARY focus on molecular/cellular MECHANISMS?
│   │   (protein function, signaling, pathways, DNA repair)
│   └─► YES → Mechanistic_Pathogenesis
│
├─► Is it pure genetic risk (GWAS, germline, hereditary)?
│   └─► YES → Strictly_Genetic
│
└─► DEFAULT → Everything_else
```

---

## Sample Data

The `sample_data/` folder contains small excerpts showing input/output formats:

| File | Description |
|------|-------------|
| `nih/sample_mechanism_classified.csv` | NIH grants classified by mechanism |
| `federal/sample_epa_grants.csv` | Raw EPA grants |
| `federal/sample_nsf_grants.csv` | Raw NSF grants |

---

## Related Repos

- **[envirotox](https://github.com/SIDaniels/envirotox)** — Classified grant data and gap analysis results
- **[dgoodwin208/orchestrator](https://github.com/dgoodwin208/orchestrator)** — Toxicant assessments

---

## Lessons Learned: What Worked and What Didn't

### What Worked ✅

**1. Decision Tree + Sonnet**
- Clear hierarchical decision tree (infrastructure → clinical → environmental → mechanistic → genetic)
- Claude Sonnet followed the logic consistently
- Explicit "when in doubt" rules reduced ambiguity

**2. Hybrid Keyword + LLM**
- Keyword-first classification caught ~70% of grants quickly
- LLM only needed for genuinely ambiguous cases
- Saved significant API costs

**3. Iterative QC with Spot Checks**
- Running `spot_check_comprehensive.py` on random samples caught systematic errors
- Manual review of edge cases improved the decision tree
- Fixes were applied programmatically with `fix_miscategorized_v2.py`

**4. Exposure-First Framing**
- Asking "Is the EXPOSURE the focus?" before "Is the MECHANISM the focus?" reduced misclassification
- Microbiome studies were always tagged Environmental (per project rules) even when mechanistic

### What Didn't Work ❌

**1. Haiku for Classification**
- Haiku was too aggressive with classification — would confidently misclassify edge cases
- Didn't follow the decision tree as reliably as Sonnet
- Example: Would classify mechanistic studies as Environmental if they mentioned any chemical
- **Recommendation:** Use Haiku only for simple keyword extraction, not nuanced classification

**2. Single-Pass Classification**
- Initial approach: classify everything in one pass
- Problem: High-level errors cascaded into subgroup errors
- **Fix:** Two-pass approach (high-level first, then subgroups)

**3. Over-Reliance on Titles**
- Titles alone were insufficient for borderline cases
- PROJECT_TERMS (MeSH-like keywords) significantly improved accuracy
- Abstracts helped but weren't always available

**4. Batching Without Progress Tracking**
- Early batches had no checkpointing
- API failures meant re-running entire batches
- **Fix:** Added `classifications_progress.json` for resumability

### Edge Cases That Required Special Handling

| Scenario | Initial Classification | Correct Classification | Fix |
|----------|----------------------|----------------------|-----|
| "Role of obesity in tumor progression" | Environmental | Mechanistic | Check if studying mechanism vs. exposure |
| Microbiome mechanism studies | Mechanistic | Environmental | Project rule: microbiome always Environmental |
| Drug resistance mechanisms | Everything_else | Mechanistic | Added to decision tree explicitly |
| Prenatal exposure effects | Mechanistic | Environmental | Exposure focus takes precedence |

### Cost & Performance Notes

| Model | Speed | Accuracy | Cost | Recommendation |
|-------|-------|----------|------|----------------|
| Sonnet | ~2 sec/grant | ~95% | $$ | Use for classification |
| Haiku | ~0.5 sec/grant | ~75% | $ | Use only for keyword extraction |
| Keyword-only | Instant | ~70% | Free | Good first pass |
| Hybrid | ~1 sec/grant | ~92% | $ | Best balance |

---

## Data Sources

| Data | URL |
|------|-----|
| NIH Reporter | [reporter.nih.gov](https://reporter.nih.gov) |
| NSF Awards | [nsf.gov/awardsearch](https://www.nsf.gov/awardsearch/) |
| USAspending | [usaspending.gov](https://www.usaspending.gov) |
| Grants.gov | [grants.gov](https://www.grants.gov) |
