# TERRAPULSE: focused Jatoi HH change research audit
# Use Google Colab with original team Drive GeoTIFFs, not a hosted emergency pipeline.
from pathlib import Path
import json
import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from scipy.ndimage import distance_transform_edt, label as ndlabel
from rasterio.warp import transform as reproject_coords

BASE = Path("/content/drive/MyDrive/UnderTheClouds/jatoi/original_subset")
OUT = BASE / "flood_validation_upgrade"
OUT.mkdir(parents=True, exist_ok=True)
PRE = BASE / "jatoi_2026-08-12_original_HH_HV.tif"
POST = BASE / "jatoi_2026-09-05_original_HH_HV.tif"
JRC = BASE / "jrc_occurrence_on_nisar_grid.tif"
GFM = BASE / "gfm_direct_validation/gfm_coverage_flood_on_nisar_grid.tif"

def read_radar(path):
    with rasterio.open(path) as src:
        if src.count < 3:
            raise ValueError("Expected HH, HV, and NISAR quality mask")
        if "linear" not in str(src.descriptions[0]).lower():
            raise ValueError("Check original band calibration before dB conversion")
        hh = src.read(1).astype("float64")
        hv = src.read(2).astype("float64")
        mask = src.read(3) == 1
        good = mask & np.isfinite(hh) & np.isfinite(hv) & (hh > 0) & (hv > 0)
        meta = (src.shape, src.transform, src.crs)
        return hh, good, meta, src.profile.copy()

pre, pre_good, pre_meta, _ = read_radar(PRE)
post, post_good, post_meta, profile = read_radar(POST)
assert pre_meta == post_meta, "Misaligned NISAR rasters; STOP"
shape, geot, crs = pre_meta
assert shape == (676, 688), "Unexpected focused study footprint; STOP"
with rasterio.open(JRC) as src:
    assert (src.shape, src.transform, src.crs) == pre_meta
    occ = src.read(1).astype("float64")
    if src.nodata is not None:
        occ[occ == src.nodata] = np.nan
with rasterio.open(GFM) as src:
    assert (src.shape, src.transform, src.crs) == pre_meta
    cov = src.read(1)
    flood = src.read(2)

height, width = shape
assert height % 2 == 0 and width % 2 == 0
h, w = height // 2, width // 2
def b2(a):
    return a.reshape(h, 2, w, 2).transpose(0, 2, 1, 3)

# Correct for original *linear power* GCOV band descriptions.
pre_db = np.full(shape, np.nan, dtype="float64")
post_db = np.full(shape, np.nan, dtype="float64")
pre_db[pre_good] = 10 * np.log10(pre[pre_good])
post_db[post_good] = 10 * np.log10(post[post_good])
radar_quality = b2(pre_good & post_good).all(axis=(2,3))
pre20 = b2(pre_db).mean(axis=(2,3))
post20 = b2(post_db).mean(axis=(2,3))
occ4 = b2(occ)
jrc_valid = np.isfinite(occ4).all(axis=(2,3)) & (occ4.min(axis=(2,3)) >= 0) & (occ4.max(axis=(2,3)) <= 100)
# 25% is a historical-observation sensitivity exclusion, NOT permanent-water truth.
jrc_keep = jrc_valid & ~(occ4 >= 25).any(axis=(2,3))
eligible = radar_quality & jrc_keep
assert np.isfinite(pre20[eligible]).all() and np.isfinite(post20[eligible]).all()

# 0 = no selected HH signal, 1 = post HH darkness, 2 = darkness + HH change;
# 255 = excluded/invalid. These are NOT ground-confirmed flood labels.
layer = np.full((h,w), 255, dtype="uint8")
layer[eligible] = 0
water_like = eligible & (post20 <= -18)
change_supported = water_like & ((post20 - pre20) <= -3)
layer[water_like] = 1
layer[change_supported] = 2

out_tif = OUT / "TERRAPULSE_HH_CHANGE_CANDIDATES_20m.tif"
profile.update(driver="GTiff",count=1,dtype="uint8",height=h,width=w,
               transform=geot * Affine.scale(2,2),nodata=255,compress="deflate",tiled=False)
for item in ["blockxsize","blockysize","interleave","photometric","predictor"]:
    profile.pop(item,None)
with rasterio.open(out_tif,"w",**profile) as dst:
    dst.write(layer, 1)
    dst.set_band_description(1, "Unverified HH darkness/change research classes")
    dst.update_tags(class_0="No selected HH signal",class_1="Post HH dark only",
                    class_2="Post HH dark AND decrease >=3dB",
                    class_255="Invalid or JRC occurrence >=25pct",
                    warning="NOT confirmed new flooding")

# Original radar-quality boundary, NOT masked JRC boundary.
quality20 = radar_quality
dist_m = distance_transform_edt(np.pad(quality20, 1, constant_values=False),
          sampling=(20,20))[1:-1,1:-1]
v4 = b2(cov)
f4 = b2(flood)
gfm_valid = (v4 == 1).all(axis=(2,3)) & np.isin(f4,[0,1]).all(axis=(2,3)) & (f4.min(axis=(2,3)) == f4.max(axis=(2,3)))
gfm_pos = f4[:,:,0,0] == 1
zones = [("0-100m",dist_m <= 100),("100-300m",(dist_m > 100)&(dist_m <= 300)),
         ("300-500m",(dist_m > 300)&(dist_m <= 500)),(">500m",dist_m > 500)]
stats=[]
for name, zone in zones:
    pop = eligible & zone
    supported = pop & gfm_valid
    red = supported & (layer == 2)
    flagged = int(red.sum())
    matches = int((red & gfm_pos).sum())
    stats.append(dict(zone=name,eligible_cells=int(pop.sum()),
         change_candidates=int((pop & (layer == 2)).sum()),gfm_covered=int(supported.sum()),
         gfm_positive=int((supported & gfm_pos).sum()),flagged_in_gfm=flagged,
         gfm_matches=matches,reference_precision_like=matches/flagged if flagged else np.nan))
audit = pd.DataFrame(stats)
audit.to_csv(OUT/"TERRAPULSE_EDGE_GFM_AUDIT.csv",index=False)
print(audit.to_string(index=False))
print("Class-1 water-like only",int((layer==1).sum()),"Class-2 change-supported",int((layer==2).sum()),"Excluded",int((layer==255).sum()))

# GPS of interior connected red components; centroids not polygon boundaries.
component, ncomp = ndlabel((layer == 2)&(dist_m > 500),structure=np.ones((3,3),dtype="uint8"))
clusters=[]
for cid in range(1,ncomp+1):
    rr,cc = np.where(component == cid)
    if len(rr)<5: continue
    cx,cy = rasterio.transform.xy(geot * Affine.scale(2,2),float(rr.mean()),float(cc.mean()),offset="center")
    longitude,latitude = reproject_coords(crs,"EPSG:4326",[cx],[cy])
    clusters.append(dict(cells=len(rr),area_hectares=round(len(rr)*.04,2),
         latitude=round(float(latitude[0]),6),longitude=round(float(longitude[0]),6),
         min_quality_edge_distance_m=round(float(dist_m[rr,cc].min()),1),
         status="UNVERIFIED research candidate"))
coords = pd.DataFrame(clusters).sort_values("cells",ascending=False)
coords.to_csv(OUT/"TERRAPULSE_INTERIOR_CLUSTERS_GPS.csv",index=False)
print("Top ten interior components:")
print(coords.head(10).to_string(index=False))
print("Outputs:",out_tif, OUT/"TERRAPULSE_EDGE_GFM_AUDIT.csv", OUT/"TERRAPULSE_INTERIOR_CLUSTERS_GPS.csv")
print("This is NOT a field-validated flood-extent or loss assessment.")
