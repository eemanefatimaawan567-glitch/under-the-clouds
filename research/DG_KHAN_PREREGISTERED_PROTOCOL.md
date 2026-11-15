# DG Khan July 2026 — pre-registered independent-event evaluation protocol

**Status:** REGISTERED BEFORE ACCESSING THE JULY FLOOD-REFERENCE PIXEL LABELS, BEFORE DOWNLOADING/PROCESSING THE TWO DG KHAN H5 PRODUCTS, AND BEFORE RUNNING THE MODEL ON THIS EVENT. **This is a prospective analysis protocol, not performed validation.** Date of registration: **15 November 2026 (Pakistan Standard Time)**. Git history of this file documents the registration commit.

## Goal and lock
Evaluate transfer of a **frozen, corrected-linear-power-to-dB, Jatoi-derived** NISAR radar change screen to a **separate DG Khan July flash-flood episode**, without optimising thresholds, model weights, JRC cutoff, study footprint or date window against DG Khan flood labels. This is a diagnostic study and **not a validated emergency detection system**.

### Grounded event context
Contemporary reporting dated **8 July 2026** documents hill-torrent floodwater entering villages near DG Khan (e.g. Vadore, Chat Sarkani, Bela, Bada). Sources:
- Dawn (8 July): https://www.dawn.com/news/2013685
- Express Tribune (8 July): https://tribune.com.pk/story/2617062/flash-floods-hit-dg-khan-villages

Such reports establish a regional flooding episode, **not exact geolocated 20 m flood labels**. Specific named affected settlements must be geolocated from reliable evidence and checked against the AOI; if outside, the test is **not an event validation**. A 19 July pass may be too late to observe transient floods.

## Pre-chosen primary scenes (same mode)
- **Before:** `NISAR_L2_PR_GCOV_023_164_D_073_4005_DHDH_A_20260625T140417_20260625T140451_P05023_N_F_J_001` — 25 June 2026.
- **After:** `NISAR_L2_PR_GCOV_025_164_D_073_4005_DHDH_A_20260719T140415_20260719T140450_P05023_N_F_J_001` — 19 July 2026.
- Track 164; frame 73; descending; `4005_DHDH_A` acquisition family.
- **Proposed bounding box:** [70.10, 29.90, 70.50, 30.25] longitude/latitude (WGS84). Prior ASF catalogue polygon intersections showed full AOI geometry overlap for both scenes; **per-pixel validity is UNTESTED**. This rectangle is a *search window*, not necessarily a geolocated affected-area footprint.

**Primary gate:** If confirmed flood time/place did not overlap the post-image acquisition and mutually valid radar grid, this pair cannot yield a meaningful negative flood-detection result; classify as **temporal/spatially non-observable** rather than a false negative.

## Exploratory alternative (NOT pooled with the primary test)
An ASF catalogue result dated **7 July 2026** exists at track 164/frame 73 but is `2005_QPDH_A`, versus 25 June `4005_DHDH_A`. Polarization availability, incidence angle, acquisition mode, product resolution, noise calibration and geometry must be verified first. **Do not treat the modes as automatically comparable or claim both HH/HV are present.** If common radiometrically comparable channels are unavailable, mark **UNSUPPORTED MIXED-MODE**, do not create quantitative change thresholds. Even if harmonizable, report only as an explicitly exploratory sensitivity experiment **separate from the same-mode primary evaluation**, with comparison limitations.

## Frozen algorithm before external labels
**Preprocessing:** inspect GCOV product metadata and actual band names; only convert calibrated *linear power backscatter* to dB as `10*log10(power)`, mask nonpositive/invalid/quality-failed pixels. Co-register without extrapolating. Verify common native grid, geolocation, calibration and expected polarization. Use the same **Jatoi focused 20 m mapping** definition and its known quality constraints, applied without modification to DG Khan:
- Aggregate aligned valid 10 m cells into complete 2×2 blocks on 20 m output grid. If common data cannot support this, record **not executable** (do not silently resample and call it the frozen method).
- Exclude invalid radar pixels; apply JRC occurrence **≥25%** historical-water exclusion to the same cell-selection logic, using a date-independent JRC layer. This cutoff is a project sensitivity choice, **not ground truth**.
- **Class 1** post-image HH `<= -18 dB` without a qualifying drop.
- **Class 2 (change-supported research candidate)** post HH `<= -18 dB` AND `post_HH - before_HH <= -3 dB`.
- **Class 0** eligible cells not selected; **255** excluded/invalid.
- No threshold tuning, selection budget retuning, machine-learning retraining, or filtering based on the external reference.
- Important: the original 290-cluster 10 m dual-HH/HV map is a **different algorithm and footprint**. Do **not** interchange it with this frozen 20 m HH screen. The separately reported 47–48% GFM reference-agreement ML models are **not deployed or tested** by this protocol.

## Independent reference and evaluability
Use independently acquired, timestamped DG Khan flood extent and **explicit reference coverage**, preferably GFM or an official EMS/UNOSAT/PDMA delineation. Before scoring:
1. Confirm coverage includes the matched radar-valid AOI and the documented event location.
2. Confirm acquisition/assessment date and labeling convention are appropriate for the radar post-pass; where flood receded before 19 July, declare **temporal non-observability** instead of interpreting a missing water indication as a model miss.
3. Reproject event reference and its observed/no-data mask to matching grid **without inventing labels**; preserve unknown as unknown. Use reference-covered valid cells only.
4. Report date lag, provenance and likely radar/optical class mismatch. Satellite flood estimates are *not* independent field-survey truth.

### Predefined outcomes
- **Evaluable:** same-mode quality/radiometry pass, documented event overlaps the common grid *and post-scene time*, and reference extent plus no-data masks are available. Compute TP/FP/FN/TN, prevalence, precision, recall, F1, eligible sample size, no-data counts, and candidate area; compare to baselines on identical common cells. Label metrics **satellite-reference agreement**, not true field-detection accuracy.
- **Non-evaluable / inconclusive:** no spatially/temporally valid flood evidence, event recedes before post scene, inadequate reference mask, or inadequate radar valid pixels. Publish no skill score. Retain audit of available evidence.
- **Unsupported cross-mode:** alternative 7 July imagery cannot be made radiometrically comparable without unplanned assumptions. No merged quantitative validation.
- **Unexpected very few flood labels / severe imbalance:** show prevalence and confusion counts; do not celebrate a high accuracy number dominated by negatives.

## Current dataset readiness (at registration)
- ASF lookup surfaced 67 total DG Khan/Dadu candidate scenes, including the above DG Khan pair. Team-run polygon-footprint test reported 100% polygon AOI overlap, not verified usable radar coverage.
- EODC GFM collection metadata returned HTTP 200. Item search, direct items and date-filtered items **failed with upstream Bad Gateway**. **No GFM independent reference data obtained.**
- Neither primary H5 pair nor frozen algorithm has been run on DG Khan. No external-event performance results currently exist.
- **Do not confuse this protocol with post-hoc validation, and do not claim the event has been tested.**

## Reporting policy
Run experimental processing on a **separate branch**; preserve failing/inconclusive outcomes and commit original IDs, code, timestamps and reproducible outputs. Only merge a report to README's Experimental follow-up once actual results exist. Prioritise submitting the official Space Apps project before any expensive experiment.
