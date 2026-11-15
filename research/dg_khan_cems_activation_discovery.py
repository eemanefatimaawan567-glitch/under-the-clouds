#!/usr/bin/env python3
"""Find public Copernicus EMS Rapid Mapping activations for DG Khan July 2026.
Uses published public-activations endpoint, not the broken EODC GFM STAC backend.
Discovery ONLY. An activation is NOT a validated flood raster.
Requires: requests, shapely (both normally available in Colab).
"""
import csv
from datetime import datetime, timezone
from pathlib import Path
import requests
from shapely.geometry import box
from shapely import wkt

BASE="https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations-info/"
AOI=box(70.10,29.90,70.50,30.25)
OUT=Path("/content/drive/MyDrive/UnderTheClouds/jatoi/original_subset/flood_validation_upgrade")
OUT.mkdir(parents=True,exist_ok=True)
rows=[]
url=BASE+"?limit=100&offset=0"
seen=set()
pages=0
try:
    while url and url not in seen and pages<20:
        seen.add(url)
        resp=requests.get(url,timeout=40,headers={"Accept":"application/json"})
        resp.raise_for_status()
        data=resp.json()
        entries=data.get("results",[]) if isinstance(data,dict) else data
        if not isinstance(entries,list): raise ValueError("Unexpected response structure")
        print("Page",pages+1,"items",len(entries))
        for a in entries:
            countries=a.get("countries") or []
            country_text=" ".join((x.get("name","") if isinstance(x,dict) else str(x)) for x in countries)
            start=str(a.get("eventTime") or a.get("activationTime") or "")
            if "pakistan" not in country_text.lower() or not start.startswith("2026-07"):
                continue
            raw=a.get("extent")
            overlap="unknown"
            if isinstance(raw,str) and raw.strip():
                try:
                    overlap=bool(wkt.loads(raw).intersects(AOI))
                except Exception:
                    overlap="geometry parse failed"
            row={
                "activation":a.get("code") or a.get("activationCode") or a.get("id"),
                "eventTime":a.get("eventTime"),
                "activationTime":a.get("activationTime"),
                "countries":country_text,
                "geometry_intersects_DG_Khan_search_AOI":overlap,
                "reportLink":a.get("reportLink"),
                "productsPath":a.get("productsPath"),
                "aois":len(a.get("aois") or [])
            }
            rows.append(row)
        url=data.get("next") if isinstance(data,dict) else None
        pages+=1
except Exception as e:
    print("REQUEST FAILED; results may be incomplete:",repr(e))
print("\nPakistan July 2026 activations:",len(rows))
for row in rows:
    print(row)
path=OUT/"DG_KHAN_CEMS_ACTIVATION_DISCOVERY.csv"
with path.open("w",newline="",encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=["activation","eventTime","activationTime","countries",
        "geometry_intersects_DG_Khan_search_AOI","reportLink","productsPath","aois"])
    writer.writeheader()
    writer.writerows(rows)
print("Saved:",path)
print("LIMIT: No public activation match DOES NOT mean no flood occurred.")
