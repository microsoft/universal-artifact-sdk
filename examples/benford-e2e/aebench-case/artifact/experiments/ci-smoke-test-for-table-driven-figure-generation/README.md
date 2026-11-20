# Experiment `ci-smoke-test-for-table-driven-figure-generation`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/ci_figure_generation_smoke.md`](../../specs/ci_figure_generation_smoke.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `bash -n scripts/ci_figure_generation_smoke.sh && python tests/test_digits.py && python tests/test_provenance_gate.py`
* Run (from the workspace root): `bash scripts/ci_figure_generation_smoke.sh`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `figures/figure_generation_manifest.json` — reference copy [`reference-outputs/figures/figure_generation_manifest.json`](../../reference-outputs/figures/figure_generation_manifest.json).
* Narrative report of the original run: [`reports/ci-smoke-test-for-table-driven-figure-generation.md`](../../reports/ci-smoke-test-for-table-driven-figure-generation.md).
