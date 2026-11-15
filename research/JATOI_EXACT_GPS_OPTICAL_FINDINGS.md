# Exact-GPS optical cross-check — research observation, not flood confirmation

The team ran the separate Earth Engine Sentinel-2 SR Harmonized optical audit over **ten preselected interior GPS candidate centres** within Jatoi. The results recorded in [CSV](../../data/jatoi_gps_sentinel2_crosscheck_2026.csv) are transcribed from the user's executed Colab output. The selection rule used a 60 m radius around candidate centres; clear fraction is a sample-level summary, not field-survey evidence. Acquisition dates varied: before 5 or 10 August 2026, after 4, 9, or 11 September 2026. Original scene IDs and local QA statistics remain in the team's Google Drive `independent_optical_audit/selected_sentinel2_scene_qa.csv` (not published in this repository).

**Result:** All ten selected before/after pairs had reported local clear fraction 1.0. **None establishes independently confirmed *new* inundation.** This is not evidence of zero floods.

- **JATOI_01** (29.644212, 70.759943) is the strongest water-like after-scene example: August 5 MNDWI **0.3873** and SCL water fraction **0**; September 11 MNDWI **0.6790** and SCL water fraction **1.0**. Its before-scene MNDWI was already positive, so an unambiguously dry pre-event baseline is absent. This is an **optical water-like change signal, not field-confirmed new flooding**.
- The remaining nine centres have SCL water fraction 0 in both selected samples. MNDWI values vary and sometimes remain positive; these are mixed or ambiguous optics, not verified no-flood labels.
- The September scenes are days after September 4 GFM and up to September 11; transient floods may occur between acquisitions and clear-time samples may miss them.
- Point-centre 60m samples are **not polygon-wide delineations**, Sentinel-2 SCL water can fail on turbid waters and mixed pixels, and the MNDWI cutoff was heuristic and not independently calibrated.
- These data do **not** justify operational flood alerts, flood-damage claims, accuracy against field ground truth, or an external event generalization claim.

**Independent second-event validation remains NOT TESTED.** A DG Khan pre/post scene pair was found in ASF catalogue (25 June and 19 July, same track/frame/mode) and preliminary polygon footprint checks passed. Valid radar pixels, dated independent flood labels and transfer evaluation have not been established. The original radar GeoTIFF was later [uploaded to GitHub](TERRAPULSE_HH_CHANGE_CANDIDATES_20m%20.tif). See [the reproducible optical and second-event audit](FLOOD_VALIDATION_EVIDENCE_AUDIT.md).
