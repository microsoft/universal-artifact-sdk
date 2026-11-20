# Experiment `containerized-no-mount-reproduction-bundle`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_all.md`](../../specs/run_all.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py && python tests/test_p_values.py`
* Run (from the workspace root): `python scripts/run_all.py --mode full --clean-smoke`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Narrative report of the original run: [`reports/containerized-no-mount-reproduction-bundle.md`](../../reports/containerized-no-mount-reproduction-bundle.md).
