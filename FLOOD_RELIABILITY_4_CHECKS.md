# Terrapulse: four flood-reliability checks (experimental)

**Notebook availability:** The original historical `Terrapulse_Flood_Reliability_4_Checks.ipynb` is **not included in this repository**. For an actually committed, reproducible corrected-scale 20 m HH-change / radar-quality and GFM QA workflow, see [Jatoi_Change_Validation_Colab.ipynb](research/Jatoi_Change_Validation_Colab.ipynb). **It is a different workflow** and does not reproduce the four checks below. The four-check descriptions on this page are preserved as an earlier experimental protocol, not an executed or reproducible repository result. This copies and extends the previous audited Jatoi notebook; it does not overwrite the original investigation. All tests operate on **existing original_subset GeoTIFFs**, not a new 14 GB NISAR download.

1. **Simple HH baselines:** fixed post-acquisition HH ≤ −18 dB and a training-only Otsu HH cutoff vs the original candidate clusters and radar-only logistic model, on exactly the same original held-out cells.
2. **Permanent water:** optional JRC Global Surface Water occurrence 0–100 raster, filename `jrc_occurrence_on_nisar_grid.tif`, in `/content/drive/MyDrive/UnderTheClouds/jatoi/original_subset/`. **Must have exact same CRS, shape and affine transform** as NISAR pair. At preset occurrence ≥90%, reference cells are excluded from *evaluation* and (in the 2 km experiment) from **both training and testing**. If absent, the notebook explicitly **skips** these experiments; it never fabricates an empty permanent-water mask. Historical occurrence is not contemporaneous flood ground truth.
3. **2 km spatial groups, gap:** deterministic projected-coordinate groups, GroupKFold, with 500 m exclusion of train cells near each test fold; every fold is trained separately. Scores absent if too few positive controls; no new flood accuracy claims.
4. **Uncertainty:** block bootstrap 95% interval using whole spatial test blocks rather than treating adjacent 20 m cells as independent.

**Outputs** when run in Colab under `original_subset/flood_validation_upgrade/`: `hh_vs_logistic_original_holdout.csv`, `holdout_2km_folds.csv` (if sufficient positive folds), `block_bootstrap_95ci.csv` (if enough samples), `RELIABILITY_CHECKS_MANIFEST.json`.

### Before running
- Run the notebook from its first cell; confirm the original 125 clusters / 1,753 pixels and cross-date GFM reference 1,737 coverage / 100 overlap.
- To run the permanent-water control, export **JRC Global Surface Water occurrence**, not current optical water, as a GeoTIFF aligned to the NISAR grid. Missing mask is a limitation, not a reason to impute non-water.
- Never compare 12 Aug frame 74 with 5 Sep frame 73 unless both have been correctly co-registered to the exact same raster grid.

### Scientific interpretation
Any measured metrics are GFM-reference agreements on one manually chosen Jatoi footprint and one NISAR acquisition pair. GFM labels supervise the model; therefore this is **not independent ground-confirmed flood detection**. The notebook is delivered **unexecuted on the user's private satellite files**: no updated score exists until run in the user's Colab environment. Do not use these outputs for emergency response or relabel the older 290-cluster interactive map.


**Status clarification (15 Nov 2026):** The earlier protocol described unverified experimental processing and did not by itself establish that any existing Case 2 metrics used dB-converted radar input. The newer 25% JRC occurrence experiment is not a permanent-water (90%) control and the two cannot be treated as interchangeable. See [corrected-scale audit](research/JATOI_2026_CHANGE_EVIDENCE.md).
