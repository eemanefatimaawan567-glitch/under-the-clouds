# Flood-evidence reliability upgrade — Terrapulse

**Research status:** a test protocol and runnable Colab notebook have been prepared, but **no revised accuracy/skill measurements have been obtained** from the original Drive GeoTIFFs. Do not change the website's existing validation statistics until the new analysis has run and the results have been checked.

## Intended capability
Distinguish **radar-change candidates** from **satellite-reference-supported potential flood** using radar-only features, with a third **uncertain / needs verification** state. GFM is a satellite-derived proxy, **not field ground truth**.

## Existing measured baseline (focused Jatoi)
- Focused footprint, different from the existing 290-cluster interactive map: **125 clusters / 1,753 pixels**.
- Candidate pixels with GFM coverage: **1,737**. Candidate/GFM overlap: **100** (5.757%).
- Full-area GFM reference prevalence: **19,918 / 462,341 = 4.308%**.
- Descriptive candidate enrichment over reference prevalence: **~1.34×**. **Not** statistically confirmed flood-detection skill.
- NISAR 12 Aug to 5 Sep 2026; GFM 4 Sep 2026, a cross-date mismatch.

## New validation experiment
A separate notebook, **Terrapulse_Jatoi_Flood_Validation_Upgrade.ipynb**, is supplied with the project handoff. It uses existing Drive outputs (no 14 GB original NISAR re-download):
- `jatoi/original_subset/jatoi_2026-09-05_original_HH_HV.tif`
- A **compatible co-registered** 12 Aug original HH/HV raster; if missing or mismatched the notebook **stops** and requests the correct file. Never substitute frame 74 as if it were aligned to frame 73.
- `jatoi/original_subset/jatoi_original_radar_clusters.geojson` (125-cluster baseline).
- `jatoi/original_subset/gfm_direct_validation/gfm_coverage_flood_on_nisar_grid.tif`, derived from the earlier Copernicus audit.

The code:
1. Verifies the two NISAR images and GFM have identical pixel-grid georeferencing and expected 1,753 / 1,737 / 100 counts.
2. Computes **NISAR-only** HH/HV before/after dB changes, post-image intensity, and local texture.
3. Aggregates 2×2 NISAR pixels to conservative 20 m comparison cells, retaining only fully covered consistent GFM-reference cells.
4. Assigns entire approximately 1 km spatial blocks to training or **held-out testing**, without selecting the split by its test performance.
5. Compares: **original 125-cluster mask**, fixed HH/HV −3 dB screen, and a regularized logistic model. Probability threshold is selected **on training data only**.
6. Saves a held-out result table, local prevalence baseline, precision/recall-like satellite-reference agreement, lift, and PR-AUC (model only). If insufficient spatially separate positive controls exist, **no score** is returned.
7. Records caveats: GFM date mismatch, uncertain product masks, 20 m approximate aggregation, spatial correlation and hand-selected geographic window.

## Method boundaries
Do not call any comparison **independent field validation**; the GFM proxy has its own errors and reference class imbalance. Hold out **different places and dates** before claiming generalizable flood detection. Spot-check Sentinel-2 cloud/water indicators on available matching dates, and obtain actual field or official damage reports for flood confirmation. Never publish the trained model as an operational alert without stronger validation.

## Outputs after executing in user's Colab
`/content/drive/MyDrive/UnderTheClouds/jatoi/original_subset/flood_validation_upgrade/`
- `spatial_holdout_results.csv`
- `test_block_summary.csv`
- `radar_flood_validation_report.json`
- `spatial_holdout_lift.png`

**Before execution:** none of these outputs, revised model scores, or improvement claims exist. An earlier 290-cluster map and this focused 125-cluster experiment must remain separate.

**Presentation-safe framing:** “We built and independently challenged an exploratory radar-change map. A more rigorous spatial-holdout flood-reference test is the next scientific validation step; a reliable flood detector is not yet demonstrated.”
