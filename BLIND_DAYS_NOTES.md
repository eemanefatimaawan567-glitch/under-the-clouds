# Blind Days — preliminary measured results

Jatoi, 2026-06-17 through 2026-11-13: 150 dates, of which 68 had Sentinel-2 observations (76 granules), 56 were optical-usable, 12 optical-obstructed, 82 had no Sentinel-2 observation, 0 insufficient coverage. AOI threshold 80%. Two known NISAR study acquisitions Aug 12 and Sep 5, not complete inventory.

**Caveats:** Cloud-screening results were supplied by the project owner from a Colab Earth Engine run; not independently reprocessed here. High clear fractions for several dates suggest validating SCL masking and mosaic logic before drawing broad conclusions. The visualization is **aggregate**, not a day-by-day timeline; `calendar.json` was not provided. 'No observation' is not 'cloudy'. These results are independent of 83.8% candidate-pixel optical screening on Sep 4.

## Date-specific timeline update
Uses exact user-generated `data/calendar.json` (150 records). JavaScript renders six month cards; click any date to inspect optical status, approximate clear-area percentage, and known study-pass marker. A missing Sentinel-2 observation is **not** classified as a cloud-obstructed observation. No new GEE requests are made.

Important: some SCL fractions are exactly 1.0, warranting independent optical QA before claiming a validated cloud climatology.
