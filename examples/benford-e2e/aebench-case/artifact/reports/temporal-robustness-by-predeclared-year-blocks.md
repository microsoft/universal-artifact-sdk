# Temporal robustness by predeclared year blocks

Status: Successful

Reproduce: implement the specs referenced by experiment `temporal-robustness-by-predeclared-year-blocks` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete temporal robustness validation under the workspace root.

Validation path:
- Reused the existing checksum/schema/row-count gate before analysis.
- Added `scripts/run_year_block_robustness.py`, which partitions verified rows into fixed blocks: 1960-1979, 1980-1999, 2000-2019, and 2020-2024.
- Reused the shared `score_first_digits_from_values` pipeline, including tested significant-digit extraction and Nigrini MAD classification.
- Wrote `results/year_block_robustness.csv` and `results/year_block_robustness_summary.json`.

Results:

| block | sample_size | first_digit_mad | chi_square | dof | classification |
|---|---:|---:|---:|---:|---|
| 1960-1979 | 5280 | 0.012916039293 | 94.334136121468 | 8 | marginally acceptable conformity |
| 1980-1999 | 5290 | 0.010819211214 | 76.827763466249 | 8 | acceptable conformity |
| 2000-2019 | 5300 | 0.008670439119 | 45.796834916742 | 8 | acceptable conformity |
| 2020-2024 | 1325 | 0.010652512951 | 24.785700518072 | 8 | acceptable conformity |

All blocks had zero excluded rows and positive analyzable sample size. The pooled first-digit conformity is not solely due to one period, though the earliest block is weaker and only marginally acceptable by Nigrini MAD. Chi-square values remain descriptive diagnostics because country-year population observations are temporally correlated rather than iid.

## Lessons
- The pinned provenance gate remains cheap enough to run at the start of this robustness check.
- Reusing the shared scoring function avoided creating a second analysis path for the temporal diagnostic.
- Temporal robustness is broadly supportive: three of four blocks are acceptable by MAD, and the early 1960-1979 block is marginal rather than nonconforming.
- The block-level chi-square diagnostics should be interpreted cautiously due to temporal/cross-sectional dependence and large sample sizes.
