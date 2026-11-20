# Experiment `plot-temporal-robustness-diagnostics`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/plot_year_block_mad.md`](../../specs/plot_year_block_mad.md), [`specs/year_block_plot_inline.md`](../../specs/year_block_plot_inline.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python -m py_compile scripts/plot_year_block_mad.py scripts/year_block_plot_inline.py`
* Run (from the workspace root): `python scripts/plot_year_block_mad.py && python scripts/year_block_plot_inline.py`
* Input data: `wb-population` at `results/year_block_inline/data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `figures/year_block_mad_manifest.json` — reference copy [`reference-outputs/figures/year_block_mad_manifest.json`](../../reference-outputs/figures/year_block_mad_manifest.json).
* Narrative report of the original run: [`reports/plot-temporal-robustness-diagnostics.md`](../../reports/plot-temporal-robustness-diagnostics.md).
