# Under the Clouds

**NASA NISAR surface-change intelligence — Jatoi and Muzaffargarh, Pakistan**

Under the Clouds is a bilingual (English / Urdu) interactive web demonstration that investigates changes visible to radar when optical observations are absent or obscured. It combines exploratory **NASA NISAR** change candidates with **Sentinel-2**, **Copernicus Global Flood Monitoring (GFM)** and **JRC Global Surface Water** reference checks.

> **Not a confirmed flood map or operational flood warning system.** Radar change does not by itself establish flooding. Our independent checks did not confirm the Jatoi change candidates as flood extent.

## Live demonstration

This is a static website with no build tooling required. Open the published GitHub Pages URL once deployed, or run locally:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000` in a browser. The basemap and Leaflet library require internet access; research data are bundled in `data/`.

## What we measured

| Result | Finding | Interpretation |
|---|---:|---|
| Jatoi exploratory radar-change clusters | 290 | Stable candidate polygons, **not flood extent** |
| Jatoi candidate grid pixels | 5,679 | Approx. 0.568 km² on 10 m grid |
| Optical screening of Jatoi candidates | 4,759 / 5,679 (83.8%) | Spatial coverage of the Sep 4 optical comparison; **not** daily cloud availability |
| Optical water indications among screened candidates | 0 | Does not prove flooding was impossible |
| Overlap of Jatoi candidates with Aug 27 GFM flood-reference pixels | 0 | Reference and radar-acquisition dates differ |
| Separate July–August Case 2 holdout | 60.98% recall; 0.110% precision; ROC AUC 0.651 | Insufficient for reliable flood detection |

### Blind Days — 17 June to 13 November 2026

Sentinel-2 optical coverage was screened over a 150-day window, with **80% minimum AOI coverage and 80% clear-area thresholds**. These SCL-based classifications are preliminary and need independent cloud-mask quality assurance.

- **56** optical-usable observation dates
- **12** optical-obstructed observation dates
- **82** dates with **no Sentinel-2 observation** (these are **not** necessarily cloudy)
- **2 known study NISAR passes**: 12 August and 5 September (inventory **not** complete)

The interactive dated calendar is based on `data/calendar.json`; `data/blind_days_summary.json` contains the aggregate counts. These are **not** the same metric as the 83.8% optical screening coverage.

## What the application does

- Interactive maps of Jatoi and a separate exploratory Muzaffargarh case
- Radar-change candidate overlays with scientific caveats
- Reference data comparisons and validation statistics
- Dated optical-coverage calendar with known NISAR study markers
- Field-verification candidate CSV export; coordinates are **polygon centroids, not verified flood or breach coordinates**
- English and Urdu views

## Method and reproducibility

Read [METHOD.md](METHOD.md) for methodology, data limitations and the difference between candidate mapping and flood validation. The project includes derived GeoJSON, CSV and evidence JSON files for the front end, not the complete original satellite scene archive or every Colab processing notebook.

## Data and acknowledgments

- NASA / ISRO — **NISAR** L-band radar GCOV data
- ESA / European Commission Copernicus — **Sentinel-2** imagery
- Copernicus — **Global Flood Monitoring (GFM)** reference detections
- European Commission Joint Research Centre — **Global Surface Water** historical-water context
- OpenStreetMap contributors — street basemap; Esri — imagery basemap
- Leaflet contributors — mapping library

Original satellite and reference products retain their respective licenses and usage terms. This repository provides derived research outputs, not ownership of those source products.

## AI assistance disclosure

**ChatGPT (OpenAI) and Claude (Anthropic)** assisted with code drafting, debugging, documentation and framing. Satellite processing, scientific validation, outputs and uncertainty remain the team's responsibility. Verify the exact tools used by each team member before submission; this disclosure is based on the project's stated workflow.

## What we do *not* claim

- No validated flood extent, calibrated flood alert, or field-confirmed inundation
- No high flood-detection accuracy: the separate Case 2 test had very low precision
- No complete inventory of NISAR acquisitions across the study window
- No claim that a day without Sentinel-2 imagery was cloud-covered
- No proof that radar changes are agricultural or flood-related without independent evidence

## Submission

See [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) and [DEMO_SCRIPT_30_SECONDS.md](DEMO_SCRIPT_30_SECONDS.md). **Confirm event-specific deadlines and video limits with the actual event organizers and submission portal.**
