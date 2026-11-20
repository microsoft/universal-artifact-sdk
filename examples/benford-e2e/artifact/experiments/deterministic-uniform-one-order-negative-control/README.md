# Experiment `deterministic-uniform-one-order-negative-control`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_negative_control_validation.md`](../../specs/run_negative_control_validation.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py`
* Run (from the workspace root): `python scripts/run_negative_control_validation.py`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/negative_control_validation_summary.json` — reference copy [`reference-outputs/results/negative_control_validation_summary.json`](../../reference-outputs/results/negative_control_validation_summary.json).
* Narrative report of the original run: [`reports/deterministic-uniform-one-order-negative-control.md`](../../reports/deterministic-uniform-one-order-negative-control.md).
