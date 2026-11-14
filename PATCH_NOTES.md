# Patch notes — current code and science status (15 Nov 2026)

These notes replace the older Option 2 freeze text which said Blind Days were not computed.

1. **Preserved**: interactive map, Jatoi/Muzaffargarh exploratory cases, bilingual UI, original statistics, field-verification CSV, existing validation tabs.
2. **Added**: separate focused Jatoi section (125 clusters, 1,753 pixels) and independent GFM evidence summary; it is *not* the older 290-cluster map layer.
3. **Added**: cinematic standalone `story.html`, chapter navigation, small short narration captions, and voice-over script.
4. **Now computed, preliminary**: 150-date Blind Days calendar, 56 usable/12 obstructed/82 without Sentinel-2 acquisitions, subject to SCL spot-check.
5. **Chance baseline check**: 19,918 / 462,341 = 4.31% GFM reference prevalence. Candidate overlap 100 / 1,737 = 5.76%, lift ≈1.34×. This is weak cross-date enrichment, not claimed flood detection skill.
6. **Scientific caveats**: 4 Sep GFM versus 5 Sep NISAR, reference is another satellite estimate, 500 STAC results sampled and deduplicated, study window manually selected, no ground-confirmed flood area, and no verified agricultural damage.

See `METHOD.md`, `README.md`, and `data/focused_jatoi_gfm_20260904.json` for reproducible counts and definitions.
