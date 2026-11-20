# Experiment `required-figure-generation`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/generate_required_figures_from_tables.md`](../../specs/generate_required_figures_from_tables.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py`
* Run (from the workspace root): `python scripts/validate_provenance.py && python scripts/analyze_benford.py && python scripts/generate_required_figures_from_tables.py`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `figures/figure_generation_manifest.json` — reference copy [`reference-outputs/figures/figure_generation_manifest.json`](../../reference-outputs/figures/figure_generation_manifest.json).
* Narrative report of the original run: [`reports/required-figure-generation.md`](../../reports/required-figure-generation.md).
