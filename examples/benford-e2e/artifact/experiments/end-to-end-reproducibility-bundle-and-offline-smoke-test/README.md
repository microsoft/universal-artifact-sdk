# Experiment `end-to-end-reproducibility-bundle-and-offline-smoke-test`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_all.md`](../../specs/run_all.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py && python tests/test_p_values.py`
* Run (from the workspace root): `python scripts/run_all.py --mode full --clean-smoke`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/offline_smoke_report.json` — reference copy [`reference-outputs/results/offline_smoke_report.json`](../../reference-outputs/results/offline_smoke_report.json).
* Narrative report of the original run: [`reports/end-to-end-reproducibility-bundle-and-offline-smoke-test.md`](../../reports/end-to-end-reproducibility-bundle-and-offline-smoke-test.md).
