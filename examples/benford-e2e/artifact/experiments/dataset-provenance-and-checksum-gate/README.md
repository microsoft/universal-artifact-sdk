# Experiment `dataset-provenance-and-checksum-gate`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/validate_provenance.md`](../../specs/validate_provenance.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_provenance_gate.py`
* Run (from the workspace root): `python scripts/validate_provenance.py && ! python scripts/validate_provenance.py --source-file data/population.csv --expected-sha256 0000000000000000000000000000000000000000000000000000000000000000`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/provenance.json` — reference copy [`reference-outputs/results/provenance.json`](../../reference-outputs/results/provenance.json).
* Narrative report of the original run: [`reports/dataset-provenance-and-checksum-gate.md`](../../reports/dataset-provenance-and-checksum-gate.md).
