# Experiment `temporal-robustness-by-predeclared-year-blocks`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_year_block_robustness.md`](../../specs/run_year_block_robustness.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py`
* Run (from the workspace root): `python scripts/validate_provenance.py && python scripts/run_year_block_robustness.py`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/year_block_robustness_summary.json` — reference copy [`reference-outputs/results/year_block_robustness_summary.json`](../../reference-outputs/results/year_block_robustness_summary.json).
* Narrative report of the original run: [`reports/temporal-robustness-by-predeclared-year-blocks.md`](../../reports/temporal-robustness-by-predeclared-year-blocks.md).
