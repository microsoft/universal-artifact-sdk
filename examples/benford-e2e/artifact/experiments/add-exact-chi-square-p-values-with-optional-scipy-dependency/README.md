# Experiment `add-exact-chi-square-p-values-with-optional-scipy-dependency`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_all.md`](../../specs/run_all.md), [`specs/analyze_benford.md`](../../specs/analyze_benford.md), [`specs/test_p_values.md`](../../specs/test_p_values.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py && python tests/test_p_values.py`
* Run (from the workspace root): `python scripts/run_all.py --mode full --clean-smoke`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/summary.json` — reference copy [`reference-outputs/results/summary.json`](../../reference-outputs/results/summary.json).
* Narrative report of the original run: [`reports/add-exact-chi-square-p-values-with-optional-scipy-dependency.md`](../../reports/add-exact-chi-square-p-values-with-optional-scipy-dependency.md).
