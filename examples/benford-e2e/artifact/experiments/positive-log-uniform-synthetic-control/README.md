# Experiment `positive-log-uniform-synthetic-control`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_positive_control_validation.md`](../../specs/run_positive_control_validation.md), [`specs/reproduce_positive_control_standalone.md`](../../specs/reproduce_positive_control_standalone.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py && python -m py_compile scripts/reproduce_positive_control_standalone.py`
* Run (from the workspace root): `python scripts/run_positive_control_validation.py && python scripts/reproduce_positive_control_standalone.py`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/positive_control_summary.json` — reference copy [`reference-outputs/results/positive_control_summary.json`](../../reference-outputs/results/positive_control_summary.json).
* Narrative report of the original run: [`reports/positive-log-uniform-synthetic-control.md`](../../reports/positive-log-uniform-synthetic-control.md).
