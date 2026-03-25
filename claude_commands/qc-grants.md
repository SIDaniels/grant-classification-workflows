# Grant Classification QC Workflow

You are a QC specialist for grant classification. Find and fix misclassified grants.

## Input
Classified CSV file: $ARGUMENTS (or ask user for file path)
Required columns: Category, Project_Title, Abstract/Terms

## QC Search Patterns

### Search Everything_else for Mechanistic errors:
```regex
role of|mechanism|pathway|signaling|kinase|inhibitor|target|resistance|
metasta|apoptosis|autophagy|ferroptosis|necroptosis|phosphat|ubiquitin|
degradation|aggregat|phase separation|plasticity|EMT
```
→ If matched: Likely should be **Mechanistic_Pathogenesis**

### Search Strictly_Genetic for Mechanistic errors:
```regex
mechanism|function|role of|targeting|pathogenic|pathophysiology
```
→ If matched: Likely should be **Mechanistic_Pathogenesis**

### Search Strictly_Genetic for Environmental errors:
```regex
environment|exposure|exposome|gene-environment|gene x environment
```
→ If matched: Likely should be **Environmental**

### Search Mechanistic for Everything_else errors:
```regex
core|clinical trial|phase i|phase ii|randomized|survivorship|
implementation|behavioral intervention|training|administrative
```
→ If matched: Likely should be **Everything_else**

### Search Mechanistic for Environmental errors:
```regex
microbiome|microbiota|gut-brain|gut brain|enteric|myenteric|prokaryote
```
→ If matched: Likely should be **Environmental**

### Search Environmental for Everything_else errors:
```regex
intervention|therapy|CBT|app-based|web-based|lifestyle intervention|
dietary intervention|treatment.induced|chemotherapy.induced
```
→ If matched: Likely should be **Everything_else**

### Search Environmental for Mechanistic errors:
```regex
role of|mechanism of|function of|metalloproteinase|leader cell|targeting
```
→ If matched: Review carefully - may be **Mechanistic**

## QC Workflow

1. Load the classified CSV
2. Run each search pattern against the appropriate category
3. Generate a REVIEW file listing potential misclassifications
4. For each flagged grant, show:
   - Current Category
   - Suggested Category
   - Matching keywords
   - Title/Abstract excerpt
5. Summarize:
   - Total grants reviewed
   - Potential errors by category
   - Error rate estimate

## False Positive Patterns

Ignore these matches (not misclassifications):
- "metalloproteinase" → NOT metal exposure (it's a protein)
- "Leader" in admin context → NOT lead exposure
- "mechanism of behavior change" → NOT mechanistic research
- "care pathway" → NOT molecular pathway

## Output

Generate:
1. `REVIEW_potential_errors.csv` - Flagged grants for manual review
2. `QC_summary.txt` - Statistics on potential errors
3. Optionally: Apply automatic corrections for high-confidence fixes
