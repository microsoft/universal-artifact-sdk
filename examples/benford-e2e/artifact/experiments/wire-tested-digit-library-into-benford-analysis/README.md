# Experiment `wire-tested-digit-library-into-benford-analysis`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_all.md`](../../specs/run_all.md), [`specs/digits.md`](../../specs/digits.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py && python tests/test_p_values.py`
* Run (from the workspace root): `python scripts/run_all.py --mode full --clean-smoke`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/run_all_manifest.json` — reference copy [`reference-outputs/results/run_all_manifest.json`](../../reference-outputs/results/run_all_manifest.json).
* Narrative report of the original run: [`reports/wire-tested-digit-library-into-benford-analysis.md`](../../reports/wire-tested-digit-library-into-benford-analysis.md).
