# Flood validation upgrade — evidence inventory and independent-event gate (15 Nov 2026)

> **Status: strengthened independent-evidence auditing, NOT increased flood-detection accuracy or proven second-event transfer.** Existing observations were re-analysed; this report makes no claim of a new NISAR processing run.

## 1. Original Jatoi map: source-level calibration verified
The archived **290-cluster / 5,679 candidate 10 m pixel / 0.5679 km²** map's original processing transcript applies `10 * np.log10` to positive radar power for HH/HV before thresholding. Cells 119–131 mosaic via linear power averaging and reconversion to dB. [Original source-code audit](JATOI_290_CLUSTER_SCALE_PROVENANCE.md).

That verifies **visible code logic**, not individual original source-product lineage or the presence of a flood. The **different** historical July–August Case 2 classifier metrics remain calibration-unverified.

## 2. Direct optical evidence: all ten Jatoi GPS research centres

Source: the team's [executed Earth Engine optical cross-check](../data/jatoi_gps_sentinel2_crosscheck_2026.csv), which records **60 m neighbourhood summaries** around ten preselected interior radar-change centres. This is a **separate focused research footprint**, not the original 290-cluster map.

| Descriptive check | Result |
|---|---:|
| Preselected research centres | 10 |
| Locally clear pre/post samples reported in CSV | 10 / 10 |
| Positive pre-scene MNDWI (above 0; *not necessarily water*) | 9 / 10 |
| Positive post-scene MNDWI | 8 / 10 |
| MNDWI increases vs decreases | 7 vs 3 |
| Median post-minus-pre MNDWI | +0.130216 |
| New after-scene Sentinel-2 SCL water indication, prior SCL none | 1 / 10 (JATOI_01) |
| Independently established **new inundation** | **0 / 10 established** |

JATOI_01 had pre-scene MNDWI **+0.3873** and post-scene **+0.679027**, with SCL water fraction changing 0→1. A positive baseline MNDWI and different acquisition dates prevent inference of definitely new floodwater. A positive MNDWI value does **not** imply confirmed water; non-water class also does **not** independently prove dry conditions. Nine other centres showed no post-scene SCL water indication. Clear before/after optical observations were not simultaneous with both NISAR dates, and a transient flood could have come and gone between observations.

This is **not** a random sample of 290 clusters or a population accuracy estimate. Per-target values, coordinates and dates are in the CSV. Recompute aggregates with `python research/recheck_jatoi_optical_evidence.py` (uses only the Python standard library).

## 3. External-event readiness: Dera Ghazi Khan, July 2026

The team ran ASF catalogue discovery and a Shapely footprint intersection check. User-run outputs report:

| Requirement | Status |
|---|---|
| NISAR before scene | **25 June 2026**, track 164, frame 73, descending `4005_DHDH_A` |
| NISAR after scene | **19 July 2026**, same track/frame/mode |
| Overlap with tested bounding box (70.10–70.50°E, 29.90–30.25°N) | **1.0** for both scene catalogue footprints |
| Scene geometries valid | Yes for both |
| Original H5 valid-pixel/quality-mask overlap | **Not checked** |
| Verified flood event inside the exact matched valid radar pixels | **Not checked** |
| Dated, independently usable flood reference (e.g. GFM) | **Not obtained**; EODC search returned `Bad Gateway` |
| Frozen Jatoi model run on DG Khan pixels | **Not done** |
| Second-event flood precision / recall | **Not measurable yet** |

**Important:** A footprint polygon fully covering a rectangular search area is **not** proof of usable NISAR radar pixels, independent flood reference coverage, or actual flooding throughout it. A 19 July post-scene could miss shorter-lived July floodwater even if local flooding reports exist.

**Independent-event evaluation prerequisites (do not change the model or thresholds after viewing reference):**
1. Verify unmodified source scene URLs/IDs, sensor product version, polarization, native calibration, per-pixel quality masks, grid and valid overlap; restrict evaluation to common valid pixels.
2. Verify flooding observations fell **inside** the radar-valid AOI and between scene dates; record flood occurrence and retreat dates.
3. Obtain an independently dated flood mask with coverage mask and class definitions; distinguish no observation from observed no flood, avoid evaluation where date mismatch makes inference invalid.
4. Freeze the Jatoi algorithm, numerical thresholds, JRC historical-water exclusion and candidate filtering. Apply **without retraining or inspecting DG Khan reference labels to tune parameters**.
5. Report TP, FP, FN, TN; reference prevalence; precision, recall and F1 **only if** a suitable reference exists; publish confusion map, spatial uncertainty and caveats. Record inconclusive evaluation honestly if the event is unobservable.

## 4. Honest validation interpretation

The earlier focused Jatoi GFM comparison found 100 GFM matches among 1,737 reference-covered radar candidates, **5.76% overlap** versus **4.31% GFM flood prevalence** (1.34× prevalence baseline). This is weak observational enrichment, *not* statistically validated skill or field confirmation. A separate corrected-scale same-region model achieved approximately 47–48% reference precision-like values on non-independent reused regional folds, not independent event accuracy. Do **not** mix these with the original 290-cluster map or the ten GPS optical test.

**Validated statement:** We performed source-level calibration checking, an auditable independent optical crosscheck on ten specific research-centre neighbourhoods, and verified geometric coverage of a potential separate NISAR event pair. **We have not validated new inundation or model transfer to a new flood event.**


## 5. User-executed DG Khan follow-up — 15 November 2026

See [the executed nine-site diagnostic and INCONCLUSIVE finding](DG_KHAN_EXECUTED_INCONCLUSIVE_RESULT.md). The team reported **36,841 common-valid 20m sample cells** and **240 HH-screen candidates** across nine fixed sites. It did **not** run JRC exclusion or obtain appropriate flood-reference labels. Earlier statements in this audit about "no model run" describe the state **before** this follow-up; they should not be treated as current. Result remains **INCONCLUSIVE**, with no validated precision/recall/F1 or independently established new inundation.
