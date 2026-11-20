# Experiment `pinned-world-bank-metadata-filter`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/validate_metadata_filter.md`](../../specs/validate_metadata_filter.md), [`specs/metadata_filter_oneliner.md`](../../specs/metadata_filter_oneliner.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python -m py_compile scripts/validate_metadata_filter.py scripts/metadata_filter_oneliner.py`
* Run (from the workspace root): `python scripts/validate_metadata_filter.py --population-path data/population.csv --on-metadata-drift embedded && python scripts/metadata_filter_oneliner.py --on-metadata-drift embedded`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/metadata_country_only_summary.json` — reference copy [`reference-outputs/results/metadata_country_only_summary.json`](../../reference-outputs/results/metadata_country_only_summary.json).
* Narrative report of the original run: [`reports/pinned-world-bank-metadata-filter.md`](../../reports/pinned-world-bank-metadata-filter.md).
