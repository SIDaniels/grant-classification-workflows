#!/usr/bin/env python3
"""Create classification batches for NSF grants."""
import json
import os
from pathlib import Path

INPUT = Path("/Users/sarahdaniels/Documents/nsf_grants/nsf_grants_2022_2025.json")
OUTPUT_DIR = Path("/Users/sarahdaniels/Documents/nsf_grants/classification_batches")
BATCH_SIZE = 50

OUTPUT_DIR.mkdir(exist_ok=True)

# Load grants
with open(INPUT) as f:
    grants = json.load(f)

print(f"Loaded {len(grants)} grants")

# Create batches
batches = []
for i in range(0, len(grants), BATCH_SIZE):
    batch = []
    for g in grants[i:i+BATCH_SIZE]:
        # Truncate abstract to ~500 chars for efficiency
        abstract = g.get('abstractText', '') or ''
        if len(abstract) > 500:
            abstract = abstract[:500] + "..."

        batch.append({
            "id": g.get('id', ''),
            "title": g.get('title', ''),
            "abstract": abstract,
            "org": g.get('awardeeName', ''),
            "directorate": g.get('dirAbbr', ''),
            "program": g.get('fundProgramName', ''),
            "amount": g.get('estimatedTotalAmt', '')
        })
    batches.append(batch)

print(f"Created {len(batches)} batches")

# Save batches
for i, batch in enumerate(batches):
    path = OUTPUT_DIR / f"batch_{i:04d}.json"
    with open(path, 'w') as f:
        json.dump(batch, f, indent=2)

print(f"Saved to {OUTPUT_DIR}")
