# DG Khan independent event — executed evidence report

**Execution outcome: `INCONCLUSIVE_REFERENCE_AND_EVENT_OBSERVABILITY_NOT_ESTABLISHED`**

**Source:** User-executed end-to-end DG Khan Colab notebook output provided on 15 November 2026. Values below transcribed from that reported output; raw generated CSV/JSON files remain in the team's Google Drive and **are not represented as uploaded to GitHub or independently re-executed here**.

## Acquisition and preprocessing

- NISAR L2 provisional GCOV pair **25 June 2026 → 19 July 2026**, descending track **164**, frame **73**, same `4005_DHDH_A` mode.
- Authenticated NASA Earthdata HDF5 **HTTP 206** streaming succeeded for both original products. Dataset bands `HHHH`, `HVHV`, `mask`, `numberOfLooks` available at 10 m `frequencyA`, EPSG:32642; observed linear units `1`.
- **Nine pre-selected spatial samples**, S01–S09, each **128×128 native 10 m** pixels, transformed into complete **2×2 blocks at 20 m**. Samples are study-grid sites, **not confirmed flooded locations**.
- Recorded common-valid **20 m cells: 36,841** across nine separate samples, out of 9×4,096=36,864 potential 20 m cells (23 cells unavailable). Nine samples are not one contiguous full-AOI flood mask.
- Applied pre-registered fixed HH thresholds to valid cells: **post HH ≤−18 dB** AND **post–pre HH ≤−3 dB**. The executed diagnostic did **not** apply the pre-registered JRC historical-water exclusion, so **it is not a full frozen-method external-event transfer**.

## Observed radar-change screening

| Diagnostic | User-run output |
|---|---:|
| Sample sites | 9 |
| Common-valid 20 m cells | **36,841** |
| Frozen-threshold radar-change candidate cells (without JRC exclusion) | **240** |
| Total flagged candidate-cell area, 240×400 m² | **0.096 km²** (not flood extent) |
| Candidate percentage of valid sampled cells | **0.6514%** (descriptive only) |
| Flood-confirmed pixels | **None established** |

Earlier central sample S05 contained **4,096 common-valid 20 m cells**, median pixelwise HH change **−3.229 dB**, **2,281** cells with a ≥3 dB decrease, **zero** cells with post HH ≤−18 dB, hence **zero candidates**. The post-scene minimum HH there was **−17.309 dB**. Other predefined samples contributed the aggregate count of 240 radar candidates; no mismatch is implied.

## Independent-sensor observations and location attempts

- OSM named-place queries: **6 returned candidate results**, **all UNVERIFIED as geolocations of July-flooded settlements**. In the initial run, Chat Sarkani, Shero Dasti, Bela, Bada, and Vadore searches returned no matches; at least one Kotani result was recorded. Do not treat OSM search matches as flood labels.
- Sentinel-2 locally sampled records: **126**. These are sensor observations, not ground-confirmed flood-class labels or a population-wide flood mask.
- Sentinel-1 catalogue records: **13**, availability evidence only.
- Google Earth Engine issue: **none recorded** in final notebook execution.
- EODC GFM STAC catalogue metadata was accessible but filtered item retrieval returned upstream `Bad Gateway`; separate CEMS public activation search reported no matching July-Pakistan records under the script's filter. Neither result establishes that no flooding occurred or that no other reference exists.

## Why the result is **inconclusive**, not a positive or negative flood-validation score

1. No spatially aligned, **date-matched verified flood / observed-not-flooded reference mask** was obtained for the nine sampled sites.
2. The sample sites were not proved to coincide with the reported July 2026 flooded villages.
3. The **19 July** radar acquisition may occur after the transient **7 July** hill-torrent flood receded, so absence of a radar-selected water-like pixel would not establish no flooding during the event.
4. The JRC ≥25% historical-occurrence exclusion was **not applied**; these numbers must not be called a fully frozen model transfer.
5. **TP, FP, FN, TN, precision, recall and F1 are undefined**, not zero.

**Scientific conclusion:** The independent-region follow-up successfully demonstrates authenticated access to real NISAR data, matched radiometric/grid screening, and auditable radar-change observations at nine preselected research sites. It **does not establish true inundation, flood-detection skill, or generalization to a second event**.

## Protocol and reproducibility

- [Pre-registered protocol](DG_KHAN_PREREGISTERED_PROTOCOL.md) — preserves test assumptions before label access; deliberately not retroactively revised after this run.
- Original in-Google-Drive outputs reported by the user:
  - `DG_KHAN_VALIDATION_RESULT.md` (1,545 bytes)
  - `nisar_frozen_9_samples.csv` (2,202 bytes)
  - `nisar_read_errors.csv` (17 bytes)
  - `sentinel1_available_scenes.csv` (2,257 bytes)
  - `sentinel2_local_observation_screen.csv` (16,733 bytes)
  - `settlement_geocoding_UNVERIFIED.csv` (685 bytes)
  - `validation_status.json` (1,627 bytes)
- Stored under `/content/drive/MyDrive/UnderTheClouds/jatoi/original_subset/flood_validation_upgrade/DG_KHAN_END_TO_END_2026/`.

**Provenance/context:** Regional flooding reports (not 20 m inundation ground truth): [Dawn, 8 July 2026](https://www.dawn.com/news/2013685) and [Express Tribune, 8 July 2026](https://tribune.com.pk/story/2617062/flash-floods-hit-dg-khan-villages). No field survey is claimed.
