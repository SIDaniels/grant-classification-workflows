# NIH Grant Classification: Mechanism Definitions Memory File

**Created:** March 28, 2026
**Purpose:** Complete reference for mechanism classification patterns to ensure reproducibility

---

## Overview

This file contains the authoritative definitions for classifying NIH grants by mechanism of harm. These patterns are used for regex-based keyword matching on PROJECT_TITLE and ABSTRACT_TEXT fields.

---

## 11 Mechanism Categories (MECH_*)

### 1. MECH_RECEPTOR_SIGNALING
**Description:** Cell signaling pathways and receptor-mediated effects

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| signaling | 81.7% | `r'\bsignaling\b'` |
| receptor | 33.6% | `r'\breceptor\b'` |
| kinase | 24.7% | `r'\bkinase\b'` |
| pathway | 17.9% | `r'\bpathway\b'` |
| phosphorylation | 15.9% | `r'phosphorylation'` |

**Additional patterns:**
- `r'signal\s+transduction'`
- `r'mapk|erk\s+pathway'`
- `r'akt|pi3k'`
- `r'wnt\s+pathway'`
- `r'notch\s+pathway'`
- `r'hedgehog'`
- `r'tyrosine\s+kinase'`
- `r'gpcr|g.?protein'`

---

### 2. MECH_INFLAMMATION
**Description:** Inflammatory responses and cytokine-mediated effects

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| immune | 50.6% | `r'\bimmune\b'` |
| inflammatory | 48.2% | `r'inflamm'` |
| inflammation | 42.5% | `r'inflamm'` |
| cytokine | 16.8% | `r'cytokine'` |
| macrophage | 16.6% | `r'macrophage'` |

**Additional patterns:**
- `r'interleukin|\bil-\d'`
- `r'\btnf\b|tumor\s+necrosis'`
- `r'nf.?kb|nf.?kappa'`
- `r'prostaglandin'`
- `r'cox-2|cyclooxygenase'`
- `r'inflammasome'`
- `r'nlrp3'`

---

### 3. MECH_IMMUNE_DYSFUNCTION
**Description:** Immune system dysregulation, autoimmunity, immunotoxicity

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| immune | 73.4% | `r'immune\s+(dysfunction|suppress|deficien|response|system)'` |
| t cell | 34.9% | `r't\s*cell|t-cell'` |
| autoimmune | 34.1% | `r'autoimmun'` |
| inflammation | 25.9% | (overlaps with MECH_INFLAMMATION) |
| antibody | 12.9% | `r'antibody'` |

**Additional patterns:**
- `r'immunotoxic'`
- `r'b\s*cell|b-cell'`
- `r'natural\s+killer|nk\s+cell'`
- `r'immunoglobulin'`
- `r'immunodeficien'`
- `r'lymphocyte'`

---

### 4. MECH_MICROBIOME
**Description:** Gut microbiome, dysbiosis, microbiota effects

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| microbiome | 69.5% | `r'microbiome'` |
| gut | 41.1% | `r'\bgut\b'` |
| microbiota | 38.2% | `r'microbiota'` |
| bacteria | 22.5% | `r'bacteria'` |
| intestinal | 14.9% | `r'intestinal'` |

**Additional patterns:**
- `r'dysbiosis'`
- `r'gut.?brain'`
- `r'intestinal\s+flora'`
- `r'probiotic'`
- `r'prebiotic'`
- `r'commensal'`
- `r'fecal\s+microb'`

---

### 5. MECH_SENESCENCE_CELL_DEATH
**Description:** Cellular senescence, apoptosis, autophagy, aging

**Note:** This is a combined category from separate MECH_CELL_DEATH and MECH_SENESCENCE

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| cell death | 37.0% | `r'cell\s+death'` |
| apoptosis | 29.9% | `r'apoptosis|apoptotic'` |
| senescence | 16.9% | `r'senescen'` |
| autophagy | 12.7% | `r'autophagy'` |
| aging | 11.6% | `r'\baging\b'` |

**Additional patterns:**
- `r'necrosis'`
- `r'pyroptosis'`
- `r'ferroptosis'`
- `r'programmed\s+cell\s+death'`
- `r'caspase'`
- `r'bcl-2|bcl2'`
- `r'telomere'`
- `r'replicative\s+aging'`
- `r'sasp\b'`
- `r'p16|p21'`

---

### 6. MECH_EPIGENETIC
**Description:** Epigenetic modifications, gene expression regulation

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| epigenetic | 51.5% | `r'epigenetic'` |
| gene expression | 30.9% | `r'gene\s+expression'` |
| chromatin | 24.7% | `r'chromatin'` |
| methylation | 22.1% | `r'methylation'` |
| histone | 20.6% | `r'histone'` |

**Additional patterns:**
- `r'dna\s+methylation'`
- `r'mirna|microrna'`
- `r'non.?coding\s+rna'`
- `r'imprint'`
- `r'dnmt'`
- `r'transcription'`
- `r'acetylation'`

---

### 7. MECH_OXIDATIVE_MITOCHONDRIAL
**Description:** Oxidative stress, ROS, mitochondrial dysfunction

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| mitochondria | 19.6% | `r'mitochondri'` |
| oxidative stress | 19.6% | `r'oxidative\s+stress'` |
| ROS | 12.9% | `r'\bros\b'` |
| metabolism | 12.2% | (not used - too broad) |
| oxidative | 10.0% | (captured by oxidative stress) |

**Additional patterns:**
- `r'reactive\s+oxygen'`
- `r'antioxidant'`
- `r'free\s+radical'`
- `r'lipid\s+peroxidation'`
- `r'glutathione'`
- `r'nrf2'`
- `r'redox'`
- `r'electron\s+transport'`
- `r'atp\s+production'`

---

### 8. MECH_BARRIER_DISRUPTION
**Description:** Blood-brain barrier, gut barrier, epithelial barrier integrity

**Note:** This category was NOT in the original classify_grants.py - it was added later

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| barrier | 95.4% | `r'\bbarrier\b'` |
| blood-brain | 71.1% | `r'blood.?brain'` |
| permeability | 15.0% | `r'permeability'` |
| endothelial | 10.6% | `r'endothelial'` |
| tight junction | 7.1% | `r'tight\s+junction'` |

**Additional patterns:**
- `r'intestinal\s+barrier'`
- `r'epithelial\s+barrier'`
- `r'vascular\s+barrier'`
- `r'bbb\b'` (blood-brain barrier)
- `r'gut\s+barrier'`
- `r'leaky\s+gut'`

---

### 9. MECH_ENDOCRINE
**Description:** Endocrine disruption, hormone signaling

**KNOWN ISSUE:** Current patterns require "disrupt" language (environmental health focus) and miss 99% of insulin/diabetes grants

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| estrogen | 41.5% | `r'\bestrogen\b'` |
| hormone | 40.4% | `r'\bhormone\b'` |
| androgen | 32.1% | `r'\bandrogen\b'` |
| receptor | 20.0% | (overlaps with MECH_RECEPTOR_SIGNALING) |
| thyroid | 10.1% | `r'\bthyroid\b'` |

**Current patterns (environmental focus):**
- `r'endocrine\s+disrupt'`
- `r'hormone\s+disrupt'`
- `r'estrogen\s+(receptor|disrupt|mimic)'`
- `r'androgen\s+(receptor|disrupt)'`
- `r'thyroid\s+(disrupt|hormone)'`
- `r'steroid\s+hormone'`
- `r'hormone\s+receptor'`

**MISSING patterns (needed for biotech context):**
- `r'\binsulin\b'` - 99% miss rate
- `r'\bdiabetes|diabetic\b'` - 99% miss rate
- `r'\bpituitary|adrenal|hypothalam'` - 94% miss rate
- `r'\bcortisol|glucocorticoid\b'` - 92% miss rate
- `r'\bgrowth\s+hormone\b'`

---

### 10. MECH_NEURODEGENERATION
**Description:** Neurodegenerative diseases, neurotoxicity

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| alzheimer | 53.9% | `r'alzheimer'` |
| dementia | 19.4% | `r'dementia'` |
| tau | 16.9% | `r'\btau\b'` |
| parkinson | 11.5% | `r'parkinson'` |
| amyloid | 10.9% | `r'amyloid'` |

**Additional patterns:**
- `r'neurodegenerat'`
- `r'neurotoxic'`
- `r'dopamine.{0,20}(loss|degenerat|neuron)'`
- `r'alpha.?synuclein'`
- `r'tauopathy'`
- `r'huntington'`
- `r'als\b|amyotrophic'`
- `r'lewy\s+bod'`
- `r'cognitive\s+decline'`

---

### 11. MECH_DNA_DAMAGE
**Description:** DNA damage, mutagenesis, genotoxicity

**Keywords (with frequency from validation):**
| Keyword | Frequency | Pattern |
|---------|-----------|---------|
| dna damage | 36.9% | `r'dna\s+damage'` |
| dna repair | 26.6% | `r'dna\s+repair'` |
| mutation | 14.7% | `r'\bmutation\b'` |
| genome | 12.7% | (not used - too broad) |
| cancer | 11.9% | (not used - captured elsewhere) |

**Additional patterns:**
- `r'mutagenesis|mutagen'`
- `r'genotoxic'`
- `r'double.?strand\s+break'`
- `r'nucleotide\s+excision'`
- `r'base\s+excision'`
- `r'mismatch\s+repair'`
- `r'chromosom.{0,10}aberration'`
- `r'genome\s+instability'`
- `r'dna\s+integrity'`

---

## 15 Exposure Categories (EXP_*)

### Chemical Exposures

| Category | Key Patterns |
|----------|--------------|
| EXP_HEAVY_METALS | `lead`, `mercury`, `arsenic`, `cadmium`, `chromium` |
| EXP_AIR_POLLUTION | `air pollut`, `particulate`, `pm2.5`, `ozone`, `diesel exhaust` |
| EXP_PFAS | `pfas`, `pfoa`, `pfos`, `perfluor` |
| EXP_PESTICIDES | `pesticide`, `herbicide`, `insecticide`, `organophosphate` |
| EXP_RADIATION | `radiation`, `uv`, `radon`, `ionizing` |
| EXP_PHTHALATES_BPA | `phthalate`, `bpa`, `bisphenol`, `plasticizer` |
| EXP_SOLVENTS | `solvent`, `benzene`, `toluene`, `trichloroethylene` |
| EXP_PAHS_DIOXINS_PCBS | `pah`, `dioxin`, `pcb`, `polychlorinated`, `polycyclic aromatic` |
| EXP_FLAME_RETARDANTS | `flame retardant`, `pbde`, `brominated` |

### Lifestyle/Behavioral Exposures

| Category | Key Patterns |
|----------|--------------|
| EXP_DIET_NUTRITION | `diet`, `nutrition`, `obesity`, `vitamin`, `nutrient` |
| EXP_TOBACCO_SMOKE | `tobacco`, `smoking`, `cigarette`, `nicotine` |
| EXP_DRUGS_MEDICATIONS | `drug toxicity`, `adverse drug`, `substance abuse`, `overdose` |
| EXP_BACTERIAL_INFECTION | `bacteria`, `infection`, `sepsis`, `pathogen` |
| EXP_ALCOHOL | `alcohol`, `ethanol`, `drinking` |
| EXP_VIRAL_INFECTION | `virus`, `viral infection`, `hepatitis`, `hiv` |

---

## Toxicant-Mechanism Matrix

Evidence scores: Strong (+++), Moderate (++), Weak (+), None (-)

| Toxicant | Oxidative | Inflammation | DNA Damage | Epigenetic | Endocrine | Microbiome |
|----------|-----------|--------------|------------|------------|-----------|------------|
| Heavy Metals | +++ | ++ | +++ | ++ | ++ | + |
| Air Pollution | +++ | +++ | ++ | ++ | + | + |
| PFAS | + | ++ | + | ++ | +++ | ++ |
| Pesticides | +++ | ++ | ++ | ++ | +++ | ++ |
| Radiation | +++ | ++ | +++ | + | + | - |
| Phthalates/BPA | + | + | + | ++ | +++ | + |
| Solvents | +++ | + | ++ | + | + | - |
| PAHs/Dioxins | +++ | ++ | +++ | +++ | ++ | + |
| Flame Retardants | ++ | + | + | ++ | +++ | + |
| Tobacco | +++ | +++ | +++ | +++ | + | ++ |

---

## Known Issues and Limitations

### CRITICAL
1. **MECH_ENDOCRINE undercounting** - 99% miss rate on insulin/diabetes (environmental focus only)
2. **Mechanism column mismatch** - Original script that created MECH_* columns is lost

### HIGH
3. **32% over-classification** - 14,262 biotech grants tagged with ALL 3 subfields
4. **No ground truth validation** - Manual review not performed

### MEDIUM
5. **Regex word boundary bugs** - Some patterns missing `\b`
6. **"treatment" too broad** - Catches "treatment group" in methods

### LOW
7. **Missing categories** - No protein folding, stem cell, circadian mechanisms

---

## File Locations

| File | Path |
|------|------|
| Exposure classification script | `classification/classify_grants.py` |
| Reconstructed mechanism script | `classification/classify_grants_mechanisms_reconstructed.py` |
| Biotech subfield script | `classification/classify_biotech_subfields.py` |
| Merged data | `~/Documents/grant_categorization/shared/raw_data/reporter/merged/` |

---

## Validation Methodology

Patterns were inferred by:
1. Loading grants with existing MECH_* = 1 tags
2. Sampling 500 tagged grants per category
3. Calculating keyword frequency in title + abstract
4. Inferring patterns from high-frequency terms (>50% = primary, 20-50% = secondary)
5. Validating against known patterns from classify_grants.py where names matched

---

## Usage

```python
import re
import pandas as pd

# Example: Check if grant matches MECH_INFLAMMATION
inflammation_patterns = [
    re.compile(r'inflamm', re.IGNORECASE),
    re.compile(r'\bimmune\b', re.IGNORECASE),
    re.compile(r'cytokine', re.IGNORECASE),
]

def classify_inflammation(text):
    if pd.isna(text):
        return 0
    for pattern in inflammation_patterns:
        if pattern.search(str(text)):
            return 1
    return 0

df['MECH_INFLAMMATION'] = (df['PROJECT_TITLE'].fillna('') + ' ' +
                           df['ABSTRACT_TEXT'].fillna('')).apply(classify_inflammation)
```

---

## Reproducibility Checklist

- [ ] All 11 MECH_* patterns documented above
- [ ] All 15 EXP_* patterns documented above
- [ ] Known issues documented
- [ ] Validation methodology documented
- [ ] File locations documented
- [ ] Usage examples provided
