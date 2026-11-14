# Method and limitations

## Important: focused Jatoi subset added after the earlier map study

The **new focused study** covers approximately **70.75–70.82°E, 29.59–29.65°N** using NASA–ISRO NISAR GCOV HH/HV images from **12 August and 5 September 2026** (track 164 / frame 73). After same-grid comparison and connected-component filtering it has **125 candidate clusters and 1,753 pixels (17.53 ha)**. These are unverified radar-change candidates. The existing dashboard map and the region described below use an **earlier and geographically distinct** Jatoi footprint with **290 clusters and 5,679 pixels**. Their counts must not be combined or replaced.

For the new study, the retrieved Copernicus GFM sample on **4 September 2026** included **100 readable entries but only two unique satellite-derived observations**, after removing 98 duplicate raster/time records. GFM covered **1,737 / 1,753** candidate pixels, of which **100** overlapped GFM flood flags; **1,637** covered candidates had no overlap and **16** lacked coverage. This is cross-date satellite agreement, **not confirmed flood extent or a precision/recall/F1 evaluation**. The available search sample may not be exhaustive. [Data summary](data/focused_jatoi_gfm_20260904.json).

## Study regions and observations

**Jatoi** is the primary case, around longitude 70.77–70.90° E, latitude 29.47–29.59° N. Two same-mode NISAR L-band GCOV observations (12 August and 5 September 2026; track 164, descending, 4005_DHDH_A) support the exploratory change-candidate map. Derived cluster polygons are in `data/jatoi_clusters.geojson` (290 features). Total candidate area is 5,679 × 100 m² = 0.5679 km², assuming a 10 m analysis grid.

**Muzaffargarh** is a separate exploratory case using a different observation pair / processing workflow. Its candidate polygons must not be presented as validated flood extent or directly compared as a matched experiment.

## Optical screening and reference comparison

Sentinel-2 on 4 September 2026 provided optical screening of 4,759 of the 5,679 Jatoi candidate pixels (83.8% of candidate pixels). No water indication was found in those screened candidate pixels under the project test; 920 candidates lacked this optical screening. This is *spatial* coverage for that comparison, not percent of cloud-free days.

The 27 August 2026 Copernicus GFM flood-reference detection map had zero overlap with the 5,679 Jatoi radar candidates. Acquisition dates differ; GFM is a separate satellite-derived estimate rather than surveyed ground truth. Lack of overlap is evidence against labeling the candidates as flood but does not prove absence of flood everywhere.

## Separate Case 2

A second same-mode July 7 to August 24 2026 comparison was tested using an August 27 GFM reference and a NW-training / SE-testing spatial split. Reported testing confusion matrix: TP=50, FP=45,478, FN=32, TN=59,530. Recall=60.98%, precision=0.1098%, F1=0.2193%, ROC AUC=0.6505. The reference was satellite-derived, only 3 days after the late NISAR acquisition, and pixels are spatially correlated; the resulting values do not establish generalizable flood-detection accuracy.

## Daily optical-availability calendar (preliminary)

Dates: 17 June–13 November 2026 inclusive (150 days). Daily records in `data/calendar.json` were produced from Sentinel-2 SCL-based classifications with an 80% AOI coverage criterion and an 80% clear-fraction criterion. Classification output: 56 usable observations, 12 obstructed observations, 82 days without Sentinel-2 acquisition in the filtered dataset. Missing acquisition is not evidence of clouds. Exact SCL class handling and unusually high reported clear fractions deserve a separate QA before strong cloud-obstruction claims. The two shown NISAR dates are **known study passes only**, not a complete inventory.

## Scientific scope

Candidate locations are leads for field verification, **not** flood detections or surveyed ground truth. This research prototype is not suitable for disaster-response decisions without independent validation.
