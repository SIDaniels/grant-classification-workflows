#!/usr/bin/env python3
"""Fast NSF grant pull - processes by month, shows progress."""
import requests
import json
import csv
import sys
from pathlib import Path

BASE_URL = "https://api.nsf.gov/services/v1/awards.json"
OUTPUT_DIR = Path("/Users/sarahdaniels/Documents/nsf_grants")
FIELDS = ["id", "title", "abstractText", "awardeeName", "awardeeCity",
          "awardeeStateCode", "estimatedTotalAmt", "fundsObligatedAmt",
          "startDate", "expDate", "fundProgramName", "primaryProgram",
          "pdPIName", "piEmail", "transType", "orgLongName", "divAbbr",
          "dirAbbr", "progEleCode", "cfdaNumber"]

def fetch_page(start, end, offset=0):
    params = {
        "dateStart": start, "dateEnd": end,
        "offset": offset, "rpp": 25,
        "printFields": ",".join(FIELDS)
    }
    r = requests.get(BASE_URL, params=params, timeout=60)
    return r.json() if r.status_code == 200 else None

def fetch_month(year, month):
    start = f"{month:02d}/01/{year}"
    end = f"{month:02d}/28/{year}" if month != 12 else f"12/31/{year}"

    data = fetch_page(start, end, 0)
    if not data: return []

    total = min(data['response']['metadata']['totalCount'], 10000)
    grants = data['response'].get('award', [])

    offset = 25
    while offset < total:
        data = fetch_page(start, end, offset)
        if data:
            grants.extend(data['response'].get('award', []))
        offset += 25
        if offset % 100 == 0:
            print(f"    {offset}/{total}", flush=True)

    return grants

all_grants = []
for year in [2022, 2023, 2024, 2025]:
    print(f"=== {year} ===", flush=True)
    for month in range(1, 13):
        if year == 2025 and month > 2:
            break
        print(f"  {year}-{month:02d}...", end=" ", flush=True)
        grants = fetch_month(year, month)
        all_grants.extend(grants)
        print(f"{len(grants)} grants (total: {len(all_grants)})", flush=True)

print(f"\nTotal: {len(all_grants)} grants", flush=True)

# Save JSON
with open(OUTPUT_DIR / "nsf_grants_2022_2025.json", 'w') as f:
    json.dump(all_grants, f)
print("Saved JSON", flush=True)

# Save CSV
with open(OUTPUT_DIR / "nsf_grants_2022_2025.csv", 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
    w.writeheader()
    for g in all_grants:
        row = {k: ('; '.join(str(x) for x in v) if isinstance(v, list) else v)
               for k, v in g.items() if k in FIELDS}
        w.writerow(row)
print("Saved CSV", flush=True)

# Summary
print("\n=== By Directorate ===", flush=True)
dirs = {}
for g in all_grants:
    d = g.get('dirAbbr', 'UNK')
    dirs[d] = dirs.get(d, 0) + 1
for d, c in sorted(dirs.items(), key=lambda x: -x[1]):
    print(f"  {d}: {c:,}", flush=True)
