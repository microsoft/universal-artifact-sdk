# Plot temporal robustness diagnostics

Status: Completed

Reproduce: implement the specs referenced by experiment `plot-temporal-robustness-diagnostics` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete validation for the temporal robustness diagnostic. Added `scripts/plot_year_block_mad.py`, which reads only `results/year_block_robustness.csv`, validates required columns and Nigrini MAD classifications, then renders `figures/year_block_mad.png` with threshold bands at 0.006, 0.012, and 0.015. Re-ran the year-block robustness script followed by the plotter successfully.

Observed block MADs: 1960-1979 = 0.012916 (marginally acceptable), 1980-1999 = 0.010819 (acceptable), 2000-2019 = 0.008670 (acceptable), 2020-2024 = 0.010653 (acceptable). The generated PNG SHA-256 is `476ca5dd725f304aeb6135d803e5c443194fb8f58b0a8bcba637a02e0cefe1ce`.

## Lessons
- A CSV-backed plotter keeps the diagnostic auditable: the figure is generated from recorded robustness results rather than silently recomputing empirical Benford scores.
- Validating classifications against Nigrini thresholds before plotting catches stale or corrupted `year_block_robustness.csv` rows.
- The temporal diagnostic is visually supportive: three of four blocks are acceptable by MAD, while the earliest block is marginally acceptable rather than nonconforming.
