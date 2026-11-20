# Experiment `benford-world-bank-population-validation`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_benford_validation.md`](../../specs/run_benford_validation.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python -m py_compile run_benford_validation.py`
* Run (from the workspace root): `python run_benford_validation.py --outdir benford_validation_run`
* Input data: `wb-population` at `benford_validation_run/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `benford_validation_run/summary.json` — reference copy [`reference-outputs/benford_validation_run/summary.json`](../../reference-outputs/benford_validation_run/summary.json).
* Narrative report of the original run: [`reports/benford-world-bank-population-validation.md`](../../reports/benford-world-bank-population-validation.md).
