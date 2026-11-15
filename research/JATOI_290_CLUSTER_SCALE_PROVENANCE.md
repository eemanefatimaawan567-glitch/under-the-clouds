# Archived Jatoi 290-cluster map — HH/HV dB source-code provenance audit

**15 Nov 2026 — source-level review (not a fresh re-execution of the original Colab).**

The original team's large archived notebook transcript (cells **114–131**, with final Cell 131 asserting 290 clusters and 5,679 pixels) was inspected. Unlike a separate later diagnostic notebook that mistakenly treated linear HH/HV values as dB, the **290-cluster map's visible generation pipeline does convert positive source HH and HV power to decibels before thresholding**.

Exact operations observed:

1. Frame-level preprocessing (August 12 and September 5, frames 73 and 74): select pixels with radar mask = 1 and finite positive HH and HV; set `hh_db[valid] = 10 * np.log10(hh[valid])` and `hv_db[valid] = 10 * np.log10(hv[valid])`. Output band descriptions `HH_dB` and `HV_dB`.
2. Cell 119 co-registers frame-73 and frame-74 sources at 10 m on a shared EPSG:32642 grid. Crucially, it computes `power = 10 ** (db / 10)`, reprojects and averages **in linear power**, and then writes `10 * np.log10(mean_power)` to mosaic `HH_dB` and `HV_dB` bands. This avoids a dB/power mixup during mosaicking.
3. Cell 120 subtracts the resulting **dB mosaics**: `hh_change = after_hh - before_hh`, likewise HV.
4. Cell 121 defines candidate rule: `hh_diff <= -3`, `hv_diff <= -2`, `before_hh > -15`, `after_hh <= -15`; minimum 9 contiguous 10 m pixels.
5. Cells 129–131 further impose matching frame identity between the dates, recluster, and construct exact cell polygons. Cell 131 **asserts** `len(features)==290` and `total_pixels==5679`. The rendered repository GeoJSON contains the 290-candidate layer. Surface area is `5679 × 100 m² = 0.5679 km²` **of exploratory candidate cells, not floodwater**.

**Finding:** The published 290 / 5,679 / 0.568 km² numbers are **source-code dB-conversion-verified**, *not* subject to the specific linear-as-dB bug identified in a distinct later workflow. This does **not** prove the input files actually matched every expected provenance record, that imagery quality was adequate, or that radar changes were caused by flooding. The source itself notes imperfect underlying source-file lineage.

**Scope boundary:** No equivalent independent processing provenance verification has yet been established for the distinct **July–August Case 2 six-rule/classifier** metrics. Those remain **calibration-unverified historical results** and cannot be replaced with corrected August–September values.

**Independent crosscheck:** The ten GPS centres from the **separate** corrected-scale focused Jatoi test were selected as the largest connected HH-change-supported components located more than 500 m from radar-quality edges. In the team-run Sentinel-2 check, most August before-scenes had *positive* MNDWI (not necessarily water), while September SCL showed no water except at the first target. Those samples do **not** prove newly flooded fields and should not be conflated with the earlier 290-cluster map's optical test.

**Source of this audit:** team's archived notebook transcript supplied in the project conversation, with cell comments 114–131 and downstream check 290 / 5679. No new original radar processing or model fit was run to produce this note.
