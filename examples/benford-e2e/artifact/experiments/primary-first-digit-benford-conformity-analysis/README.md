# Experiment `primary-first-digit-benford-conformity-analysis`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/analyze_benford.md`](../../specs/analyze_benford.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py`
* Run (from the workspace root): `python scripts/validate_provenance.py && python scripts/analyze_benford.py`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/summary.json` — reference copy [`reference-outputs/results/summary.json`](../../reference-outputs/results/summary.json).
* Narrative report of the original run: [`reports/primary-first-digit-benford-conformity-analysis.md`](../../reports/primary-first-digit-benford-conformity-analysis.md).
