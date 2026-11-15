#!/usr/bin/env python3
"""Discover dated EODC Global Flood Monitoring (GFM) scenes for DG Khan.
Discovery only: NEVER interprets catalogue scene counts as flood confirmation.
Run in Google Colab after: pip install pystac-client pandas shapely
"""
from pathlib import Path
import json
import pandas as pd
from pystac_client import Client

ROOT = Path("/content/drive/MyDrive/UnderTheClouds/jatoi/original_subset/flood_validation_upgrade")
ROOT.mkdir(parents=True, exist_ok=True)
OUTPUT = ROOT / "DG_KHAN_2026_GFM_CATALOG_DISCOVERY.csv"
BBOX = [70.10, 29.90, 70.50, 30.25]
INTERVAL = "2026-06-25/2026-07-21"
CATALOGUES = ["https://catalogue.services.eodc.eu",
              "https://stac.eodc.eu/api/v1"]  # fallback can fail

found = []
connected = False
last_error = None
for endpoint in CATALOGUES:
    try:
        catalog = Client.open(endpoint)
        collections = list(catalog.get_collections())
        candidates = [c.id for c in collections
                      if "gfm" in c.id.lower() or
                         "global flood" in (c.title or "").lower()]
        print("Connected:", endpoint, "Potential GFM collections:", candidates)
        connected = True
        if not candidates:
            print("No known GFM collection ID found; inspect catalog collections.")
            continue
        for collection in candidates:
            try:
                items = catalog.search(collections=[collection], bbox=BBOX,
                                       datetime=INTERVAL, max_items=300)
                for it in items.items():
                    assets = {name: asset.href for name, asset in it.assets.items()}
                    found.append({
                        "endpoint":endpoint,
                        "collection":collection,
                        "scene_id":it.id,
                        "datetime":str(it.datetime),
                        "assets": ",".join(assets),
                        "asset_hrefs":json.dumps(assets),
                        "bbox":str(it.bbox),
                    })
            except Exception as e:
                print("Collection search failed:", collection, repr(e)[:250])
        if found:
            break
    except Exception as e:
        last_error = repr(e)
        print("Endpoint unavailable:", endpoint, last_error[:250])

if found:
    df = pd.DataFrame(found).drop_duplicates(subset=["collection","scene_id"])
    df.to_csv(OUTPUT,index=False)
    print("GFM catalogue items:",len(df), "Saved:",OUTPUT)
    print(df[["datetime","scene_id","assets"]].head(30).to_string(index=False))
else:
    print("NO CONFIRMED REFERENCE ITEMS. This is NOT evidence of no flood.")
    if not connected:
        print("Catalogue connection failed:",last_error)
    pd.DataFrame(columns=["endpoint","collection","scene_id","datetime",
                          "assets","asset_hrefs","bbox"]).to_csv(OUTPUT,index=False)
