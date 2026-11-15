#!/usr/bin/env python3
"""Recompute descriptive Sentinel-2 optical evidence; no flood-ground-truth claims."""
import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "jatoi_gps_sentinel2_crosscheck_2026.csv"
with SOURCE.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

required = ["before_MNDWI", "after_MNDWI", "before_SCL_water_fraction",
            "after_SCL_water_fraction", "local_clear_before",
            "local_clear_after", "new_inundation_confirmed"]
assert len(rows) == 10, "Expected the 10 preselected Jatoi research points"
assert len({r["target_id"] for r in rows}) == 10, "Duplicate target IDs"
for row in rows:
    for key in required[:-1]:
        float(row[key])
    assert row["new_inundation_confirmed"] == "not_established"

deltas = [float(r["after_MNDWI"]) - float(r["before_MNDWI"]) for r in rows]
before_positive = sum(float(r["before_MNDWI"]) > 0 for r in rows)
after_positive = sum(float(r["after_MNDWI"]) > 0 for r in rows)
scl_transitions = [r["target_id"] for r in rows
    if float(r["before_SCL_water_fraction"]) == 0
    and float(r["after_SCL_water_fraction"]) > 0]
all_clear = sum(float(r["local_clear_before"]) == 1 and
                float(r["local_clear_after"]) == 1 for r in rows)

print("Preselected optical research centres:", len(rows))
print("Reported locally clear before-and-after samples:", all_clear)
print("Positive MNDWI before / after:", before_positive, "/", after_positive)
print("MNDWI increased / decreased:", sum(d > 0 for d in deltas), "/",
      sum(d < 0 for d in deltas))
print("Median MNDWI change:", round(statistics.median(deltas), 6))
print("SCL 0 -> water transitions:", scl_transitions)
print("Independent new-flood confirmations: 0 established")
print("CAUTION: SCL and MNDWI are not independent field-survey truth.")
