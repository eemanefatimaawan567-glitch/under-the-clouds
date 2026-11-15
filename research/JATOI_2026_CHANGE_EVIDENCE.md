# Focused Jatoi radar-change experiment — 15 November 2026

> **Research-only potential-water / radar-change candidates; NOT field-confirmed new flooding, a flood-extent map or an emergency alert.**

## Exact scope
This experiment is **different from** the earlier web map (**290 clusters, 5,679 candidate 10 m pixels**) and the original focused change extraction (**125 clusters, 1,753 candidate 10 m pixels**). Do not merge the counts. Focused acquisition dates: NISAR **12 Aug** and **5 Sep 2026**, track **164**, frame **73**. GFM satellite reference: **4 Sep 2026**. Data were analyzed on an aligned **676 × 688** 10 m grid, with approximated 2 × 2 aggregation to 20 m cells.

## Radar calibration correction
The input TIFF bands are named `HHHH_linear` and `HVHV_linear`. Their values had incorrectly been treated as decibels in initial diagnostic notebooks. For **linear power backscatter** (verify GCOV source-calibration provenance), conversion is `10 * log10(linear_power)`. The previous rule `HH <= -18 dB` evaluated on unconverted linear values was invalid; corrected HH-only screening showed much higher satellite-reference sensitivity. Older notebook sections retained for audit history are NOT corrected-scale scores.

## Radar-only candidate layer (full valid Jatoi subset)
`TERRAPULSE_HH_CHANGE_CANDIDATES_20m.tif` was generated in the team's private Google Drive Colab environment and was **subsequently uploaded to GitHub** as [the verified binary GeoTIFF](TERRAPULSE_HH_CHANGE_CANDIDATES_20m%20.tif) (uploaded filename has an extra space before `.tif`). Class definitions:
- **0:** neither selected signal;
- **1:** post-date HH ≤ −18 dB, without HH drop ≥3 dB;
- **2:** post-date HH ≤ −18 dB AND post minus pre HH ≤ −3 dB — **change-supported research candidate**, not confirmed new inundation;
- **255:** radar-invalid or JRC historical occurrence ≥25% (exploratory exclusion; **not** a permanent-water definition).

Observed output: **14,034 class-1 cells; 2,503 class-2 cells; 941 excluded**. At 20 m × 20 m, class 2 is approximately **1.0012 km² of candidate area, not flood extent**. This output evaluates the broader radar-valid grid, **not just** reference-covered cells.

## Reference checks, same previously examined Jatoi region
Spatially held-out **1 km** test excluding JRC occurrence ≥25%: 34,394 evaluable 20 m cells, 2,310 GFM positives. Simple rule post HH ≤−18 dB AND HH drop ≥3 dB: **923 flagged, 438 GFM positive matches, 485 GFM negatives, 47.45% reference precision-like and 18.96% reference recall-like**. Because variants were inspected using the same holdout, these are **exploratory** results, not independent generalization.

### Corrected-scale machine-learning reference comparison
In **2 km GroupKFold with a 500 m train-cell exclusion zone**, JRC ≥25% excluded, using the **5% training selection-budget** setting:

| Method | GFM matches | Flagged | Reference precision-like | Reference recall-like |
|---|---:|---:|---:|---:|
| HH darkness ranking | 3,724 | 7,855 | 47.41% | 83.40% |
| Two-stage HH-gated logistic | 3,817 | 7,979 | 47.84% | 85.49% |
| Unrestricted six-feature logistic | 3,851 | 8,011 | **48.07%** | **86.25%** |

These are **pooled results from the scorable spatial folds** within one region. The training selection budgets do **not** enforce identical test flagged counts, and GFM labels are spatially correlated. Simpler and gated models are **not proven superior** to unrestricted logistic. Changing JRC filtering changes the evaluation population. The 25% cutoff was explored against this same reference, and is not a permanent-water truth label.

### Change-specific diagnostic on 1 km JRC-filtered test cells
- GFM-positive cells with HH drop ≥3 dB: **19.0%**, versus **4.2%** of GFM-negative cells.
- BOTH HH and HV drop ≥3 dB occurs in only **0.65%** of GFM-positive cells; requiring both drops is a poor high-recall rule.
- **645** GFM-positive test cells were newly HH-dark, **1,615** were HH-dark on both acquisition dates. These numbers do **not** prove that water was absent or present on 12 Aug.

### Radar quality-boundary audit (full candidate footprint)
| Distance to original radar-quality boundary | Eligible cells | Class-2 candidates | Rate |
|---|---:|---:|---:|
| ≤100m | 6,304 | 228 | 3.62% |
| 100–300m | 12,378 | 412 | 3.33% |
| 300–500m | 11,977 | 358 | 2.99% |
| >500m | 84,672 | 1,505 | 1.78% |

Agreement with GFM is **33.49%** (≤100 m) vs **43.91%** (>500 m) precision-like. Boundary-adjacent candidates should be **flagged for QA**, not erased based on this association alone. Lower interior prevalence and different geography may confound this comparison.

## Priority locations
The ten largest **interior** (more than 500m from original radar-quality boundary) connected candidate components appear in [the coordinates CSV](../data/jatoi_interior_change_candidates_2026.csv) and the [interactive review map](../candidate-review.html). Their centers are research targets; the site **does not display exact polygon boundaries** and does not claim confirmed floods.

## What remains unverified
- Independent clear, timestamped optical imagery / field confirmation at **exact candidate pixels**, especially the first three GPS centers.
- A demonstrably dry August baseline for the full flood event. Already-dark radar cells could represent earlier water or low-backscatter land.
- Acquisition calibration, geolocation, speckle, native GFM resolution and 1-day GFM/NISAR date mismatch.
- A genuinely independent **second event or geographic region** and uncertainty from independent flood-event samples.
- The actual research GeoTIFF **has now been committed**; see the linked binary above. The new report [optical + second-event audit](FLOOD_VALIDATION_EVIDENCE_AUDIT.md) does not establish new-event validation.

## Reproduce
Run the committed [Google Colab notebook](../research/Jatoi_Change_Validation_Colab.ipynb) using the original NISAR and JRC/GFM GeoTIFFs in your own Google Drive. It creates the rule-based raster and reference/edge audit. The separate advanced ML experiments were performed in an earlier team notebook; figures above are supplied as **user-run Colab results**, not re-executed on GitHub.

**Interpretation:** Radar evidence is promising for water-like surfaces and surface-change candidates, **not** validated operational flood alerts or verified newly inundated cropland.
