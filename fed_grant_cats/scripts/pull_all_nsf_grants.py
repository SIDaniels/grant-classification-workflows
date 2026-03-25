#!/usr/bin/env python3
"""
Pull ALL NSF grants from 2022-present.
Splits by month to avoid 10,000 result API limit.
"""

import requests
import json
import csv
import time
from datetime import datetime
from pathlib import Path

BASE_URL = "https://api.nsf.gov/services/v1/awards.json"
OUTPUT_DIR = Path("/Users/sarahdaniels/Documents/nsf_grants")
FIELDS = [
    "id", "title", "abstractText", "awardeeName", "awardeeCity",
    "awardeeStateCode", "estimatedTotalAmt", "fundsObligatedAmt",
    "startDate", "expDate", "fundProgramName", "primaryProgram",
    "pdPIName", "piEmail", "transType", "orgLongName", "divAbbr",
    "dirAbbr", "progEleCode", "cfdaNumber"
]

def fetch_grants(date_start, date_end, offset=0, rpp=25):
    """Fetch a page of grants from NSF API."""
    params = {
        "dateStart": date_start,
        "dateEnd": date_end,
        "offset": offset,
        "rpp": rpp,
        "printFields": ",".join(FIELDS)
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  Error fetching offset {offset}: {e}")
        return None

def fetch_month(year, month):
    """Fetch all grants for a specific month."""
    # Calculate date range
    date_start = f"{month:02d}/01/{year}"
    if month == 12:
        date_end = f"12/31/{year}"
    else:
        date_end = f"{month+1:02d}/01/{year}"

    grants = []
    offset = 0
    rpp = 25

    # First request to get total count
    data = fetch_grants(date_start, date_end, offset, rpp)
    if not data:
        return grants

    total = data['response']['metadata']['totalCount']
    print(f"  {year}-{month:02d}: {total} grants")

    # Collect all pages
    while offset < total and offset < 10000:
        if offset > 0:
            data = fetch_grants(date_start, date_end, offset, rpp)
            if not data:
                break

        awards = data['response'].get('award', [])
        grants.extend(awards)
        offset += rpp

        if offset % 500 == 0:
            print(f"    Fetched {offset}/{min(total, 10000)}...")

        time.sleep(0.1)  # Rate limiting

    return grants

def main():
    all_grants = []
    years = [2022, 2023, 2024, 2025]

    for year in years:
        print(f"\n=== Fetching {year} ===")
        for month in range(1, 13):
            # Skip future months
            if year == 2025 and month > 2:
                break

            grants = fetch_month(year, month)
            all_grants.extend(grants)
            print(f"    Running total: {len(all_grants)}")

    print(f"\n=== Total grants fetched: {len(all_grants)} ===")

    # Save to JSON
    json_path = OUTPUT_DIR / "nsf_grants_2022_2025.json"
    with open(json_path, 'w') as f:
        json.dump(all_grants, f)
    print(f"Saved JSON: {json_path}")

    # Save to CSV
    csv_path = OUTPUT_DIR / "nsf_grants_2022_2025.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
        writer.writeheader()
        for grant in all_grants:
            # Flatten any nested fields
            row = {}
            for field in FIELDS:
                val = grant.get(field, '')
                if isinstance(val, list):
                    val = '; '.join(str(v) for v in val)
                row[field] = val
            writer.writerow(row)
    print(f"Saved CSV: {csv_path}")

    # Print summary by directorate
    print("\n=== By Directorate ===")
    by_dir = {}
    for g in all_grants:
        d = g.get('dirAbbr', 'Unknown')
        by_dir[d] = by_dir.get(d, 0) + 1
    for d, c in sorted(by_dir.items(), key=lambda x: -x[1]):
        print(f"  {d}: {c:,}")

if __name__ == "__main__":
    main()
