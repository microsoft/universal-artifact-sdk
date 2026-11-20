# Experiment `country-only-sensitivity-analysis-excluding-aggregate-world-bank-series`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/run_country_only_sensitivity.md`](../../specs/run_country_only_sensitivity.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py`
* Run (from the workspace root): `python scripts/validate_provenance.py && python scripts/run_country_only_sensitivity.py`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/country_only_summary.json` — reference copy [`reference-outputs/results/country_only_summary.json`](../../reference-outputs/results/country_only_summary.json).
* Narrative report of the original run: [`reports/country-only-sensitivity-analysis-excluding-aggregate-world-bank-series.md`](../../reports/country-only-sensitivity-analysis-excluding-aggregate-world-bank-series.md).
