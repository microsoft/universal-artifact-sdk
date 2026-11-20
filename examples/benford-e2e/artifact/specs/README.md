# Specifications index — Benford's-law analysis of World Bank population data

> **Audience**: an implementer who must re-create the code of this artifact from these specs alone
> (no original code ships). **Source of truth for**: the module list, dependency graph, environment,
> workspace layout, experiment → command mapping and known quirks. Shared definitions (constants,
> summation semantics, file formats, digit-extraction variants) live in [`common.md`](common.md).

**Goal**: following these specs, a competent implementer produces CSV/JSON outputs whose numbers are
byte-identical to the original run (modulo paths, timestamps and software-version strings). Figures
are specified by content (data, axes, labels, file names); byte-identical PNG/PDF is not expected.
Where the original code was inconsistent, the specs reproduce the inconsistency on purpose — see
[Known quirks](#known-quirks). The specs never read anything under `reference-outputs/` (that folder
may be withheld from the workspace).

## 1. Spec index

| Spec | File the implementer creates | Kind |
|---|---|---|
| [common.md](common.md) | — | shared definitions |
| [digits.md](digits.md) | `scripts/digits.py` | library (DIGITS-DECIMAL) |
| [validate_provenance.md](validate_provenance.md) | `scripts/validate_provenance.py` | library + CLI (download & checksum gate) |
| [analyze_benford.md](analyze_benford.md) | `scripts/analyze_benford.py` | library + CLI (core analysis) |
| [run_negative_control_validation.md](run_negative_control_validation.md) | `scripts/run_negative_control_validation.py` | CLI |
| [run_positive_control_validation.md](run_positive_control_validation.md) | `scripts/run_positive_control_validation.py` | CLI |
| [reproduce_positive_control_standalone.md](reproduce_positive_control_standalone.md) | `scripts/reproduce_positive_control_standalone.py` | standalone CLI (was base64-inline) |
| [run_country_only_sensitivity.md](run_country_only_sensitivity.md) | `scripts/run_country_only_sensitivity.py` | CLI |
| [validate_metadata_filter.md](validate_metadata_filter.md) | `scripts/validate_metadata_filter.py` | standalone CLI |
| [metadata_filter_oneliner.md](metadata_filter_oneliner.md) | `scripts/metadata_filter_oneliner.py` | standalone CLI (was base64-inline) |
| [run_year_block_robustness.md](run_year_block_robustness.md) | `scripts/run_year_block_robustness.py` | CLI |
| [plot_year_block_mad.md](plot_year_block_mad.md) | `scripts/plot_year_block_mad.py` | CLI (figure from CSV) |
| [year_block_plot_inline.md](year_block_plot_inline.md) | `scripts/year_block_plot_inline.py` | standalone CLI (was heredoc-inline) |
| [generate_required_figures_from_tables.md](generate_required_figures_from_tables.md) | `scripts/generate_required_figures_from_tables.py` | CLI (figures from CSV) |
| [ci_figure_generation_smoke.md](ci_figure_generation_smoke.md) | `scripts/ci_figure_generation_smoke.sh` | bash |
| [render_provenance_appendix.md](render_provenance_appendix.md) | `scripts/render_provenance_appendix.py` | CLI |
| [run_all.md](run_all.md) | `scripts/run_all.py` | driver |
| [negative_control_oneliner.md](negative_control_oneliner.md) | `scripts/negative_control_oneliner.py` | standalone CLI (was `python -c` inline) |
| [negative_control_validation.md](negative_control_validation.md) | `negative_control_validation.py` | standalone CLI (root) |
| [second_digit_pvalue_residuals.md](second_digit_pvalue_residuals.md) | `second_digit_pvalue_residuals.py` | standalone CLI (root) |
| [run_benford_validation.md](run_benford_validation.md) | `run_benford_validation.py` | standalone CLI (root) |
| [significant_digits.md](significant_digits.md) | `significant_digits.py` | standalone library (root, DIGITS-NORMALIZE) |
| [test_significant_digits.md](test_significant_digits.md) | `test_significant_digits.py` | unit tests (root) |
| [test_digits.md](test_digits.md) | `tests/test_digits.py` | unit tests |
| [test_provenance_gate.md](test_provenance_gate.md) | `tests/test_provenance_gate.py` | unit tests |
| [test_p_values.md](test_p_values.md) | `tests/test_p_values.py` | unit tests |

## 2. Module dependency graph

```
scripts/digits.py ─────────────┬──────────────► scripts/analyze_benford.py ──┬─► scripts/run_country_only_sensitivity.py
scripts/validate_provenance.py ┤                                             └─► scripts/run_year_block_robustness.py
                               ├──────────────► scripts/run_negative_control_validation.py
                               └──────────────► scripts/run_positive_control_validation.py
(Python imports; scripts insert scripts/ at the front of sys.path)

File-level data flow (reads outputs of):
  data/population.csv            ◄── validate_provenance.py (download + gate)
  results/{first,second}_digit_table.csv ──► generate_required_figures_from_tables.py ──► figures/*benford.{png,pdf}
  results/year_block_robustness.csv ──► plot_year_block_mad.py ──► figures/year_block_mad.{png,_manifest.json}
  results/provenance.json + results/summary.json ──► render_provenance_appendix.py
Subprocess drivers:
  run_all.py ──► tests/test_digits.py, tests/test_provenance_gate.py, tests/test_p_values.py,
                 validate_provenance.py, analyze_benford.py, generate_required_figures_from_tables.py
  ci_figure_generation_smoke.sh ──► validate_provenance.py, analyze_benford.py, generate_required_figures_from_tables.py
Tests:
  tests/test_digits.py ► digits.py; tests/test_provenance_gate.py ► validate_provenance.py;
  tests/test_p_values.py ► analyze_benford.py; test_significant_digits.py ► significant_digits.py
Self-contained (no project imports): validate_metadata_filter.py, metadata_filter_oneliner.py,
  negative_control_oneliner.py, reproduce_positive_control_standalone.py, year_block_plot_inline.py,
  negative_control_validation.py, second_digit_pvalue_residuals.py, run_benford_validation.py,
  significant_digits.py
```

## 3. Environment

* **Python**: 3.11 recommended (the experiments ran in `python:3.11` containers; the host that
  produced some outputs had 3.10.12). Any Python ≥ 3.10 works **provided** float sums are written as
  explicit loops where a spec says SEQ-SUM (Python ≥ 3.12 changed built-in `sum()` — `common.md` §5).
* **Packages (as recorded)**: numpy 2.2.6, pandas 2.3.3, matplotlib 3.10.8, requests 2.33.1.
  SciPy: version not recorded; any recent version (only `scipy.stats.chi2.sf` is used; p-values are
  compared with relative tolerance 1e-9). Standalone scripts use the standard library (+ numpy or
  matplotlib where stated).
* **Hardware**: CPU only; total runtime of all experiments is a few minutes; network access is needed
  for the pinned downloads (see `DATA.md`).
* **Determinism**: all randomness is seeded — `CONTROL_SEED = 20260717` (negative controls; numpy
  `default_rng` in `scripts/`, `random.Random` in `run_benford_validation.py`, numpy uniform floats in
  `negative_control_validation.py`), `POSITIVE_SEED = 424242` (positive control). Matplotlib uses the
  `Agg` backend.

## 4. Workspace layout produced by the implementation

All paths relative to the workspace root (= working directory of every command):

```
scripts/   digits.py validate_provenance.py analyze_benford.py run_negative_control_validation.py
           run_positive_control_validation.py reproduce_positive_control_standalone.py
           run_country_only_sensitivity.py validate_metadata_filter.py metadata_filter_oneliner.py
           run_year_block_robustness.py plot_year_block_mad.py year_block_plot_inline.py
           generate_required_figures_from_tables.py ci_figure_generation_smoke.sh
           render_provenance_appendix.py run_all.py negative_control_oneliner.py
tests/     test_digits.py test_provenance_gate.py test_p_values.py
./         negative_control_validation.py second_digit_pvalue_residuals.py run_benford_validation.py
           significant_digits.py test_significant_digits.py
data/      population.csv (pinned), world_bank_country_metadata.json, population_metadata_filter.csv
results/   provenance.json summary.json first_digit_table.csv second_digit_table.csv
           negative_control_validation_summary.json negative_control_first_digit_table.csv experiment_run.json
           negative_control_summary.json dataset_provenance.json negative_control_uniform_float_table.csv
           positive_control_summary.json positive_control_first_digit_table.csv positive_control_standalone/
           country_only_{summary.json,comparison.csv,first_digit_table.csv,second_digit_table.csv}
           metadata_{provenance.json,aggregate_codes.json,aggregate_codes.csv,country_only_summary.json,
                     country_only_comparison.csv,country_only_first_digit_table.csv,country_only_second_digit_table.csv}
           metadata_filter_oneliner.json negative_control_oneliner.json
           year_block_robustness.csv year_block_robustness_summary.json year_block_inline/
           offline_smoke/ offline_smoke_report.json run_all_manifest.json
           provenance_appendix.md provenance_appendix.tex
figures/   figure1_first_digit.png figure2_second_digit.png first_digit_benford.{png,pdf}
           second_digit_benford.{png,pdf} figure_generation_manifest.json
           year_block_mad.png year_block_mad_manifest.json offline_smoke/
benford_validation_run/   outputs of run_benford_validation.py --outdir benford_validation_run
second_digit_pvalue_residuals_{results.json,by_digit.csv,summary.md}   (root)
```

Each spec's **Outputs & oracle** section lists the exact files, compared fields and tolerances.

## 5. Experiments → commands

`run.command` values in `manifest.yml` (the implementer runs them after implementing). Unit-test
`check` commands are also listed in `manifest.yml`.

| Experiment | Command | Main spec(s) |
|---|---|---|
| dataset-provenance-and-checksum-gate | `python scripts/validate_provenance.py` (+ negative check with a wrong `--expected-sha256` must exit non-zero) | validate_provenance |
| tested-significant-digit-extraction-library | `python tests/test_digits.py && python tests/test_provenance_gate.py` | digits, test_digits |
| primary-first-digit-benford-conformity-analysis | `python scripts/validate_provenance.py && python scripts/analyze_benford.py` | analyze_benford |
| second-digit-generalized-benford-analysis | same as above | analyze_benford |
| deterministic-uniform-one-order-negative-control | `python scripts/run_negative_control_validation.py` | run_negative_control_validation |
| positive-log-uniform-synthetic-control | `python scripts/run_positive_control_validation.py && python scripts/reproduce_positive_control_standalone.py` | run_positive_control_validation, reproduce_positive_control_standalone |
| country-only-sensitivity-… | `python scripts/validate_provenance.py && python scripts/run_country_only_sensitivity.py` | run_country_only_sensitivity |
| temporal-robustness-by-predeclared-year-blocks | `python scripts/validate_provenance.py && python scripts/run_year_block_robustness.py` | run_year_block_robustness |
| required-figure-generation | `python scripts/validate_provenance.py && python scripts/analyze_benford.py && python scripts/generate_required_figures_from_tables.py` | generate_required_figures_from_tables |
| end-to-end-…, benford-conformity-analysis-tables-and-figures, wire-tested-digit-library-…, add-exact-chi-square-p-values-…, containerized-no-mount-reproduction-bundle | `python scripts/run_all.py --mode full --clean-smoke` | run_all |
| significant-digit-extraction-unit-tests | `python -m unittest discover -s . -p "test_significant_digits.py" -v` | significant_digits, test_significant_digits |
| negative-control-discrimination-check | `python negative_control_validation.py` | negative_control_validation |
| add-negative-control-validation | `python scripts/negative_control_oneliner.py` | negative_control_oneliner |
| add-paper-ready-provenance-appendix-table | `python scripts/render_provenance_appendix.py` | render_provenance_appendix |
| second-digit-p-value-and-residual-diagnostics | `python second_digit_pvalue_residuals.py` | second_digit_pvalue_residuals |
| pinned-world-bank-metadata-filter | `python scripts/validate_metadata_filter.py --on-metadata-drift embedded && python scripts/metadata_filter_oneliner.py --on-metadata-drift embedded` | validate_metadata_filter, metadata_filter_oneliner |
| plot-temporal-robustness-diagnostics | `python scripts/plot_year_block_mad.py && python scripts/year_block_plot_inline.py` | plot_year_block_mad, year_block_plot_inline |
| benford-world-bank-population-validation | `python run_benford_validation.py --outdir benford_validation_run` | run_benford_validation |
| ci-smoke-test-for-table-driven-figure-generation | `bash scripts/ci_figure_generation_smoke.sh` | ci_figure_generation_smoke |

The reference copy `results/no_scipy_validation/summary.json` was produced by
`python scripts/analyze_benford.py --results-dir results/no_scipy_validation --figures-dir figures/no_scipy_validation`
in an environment **without** SciPy (p-value fields `null`, note set; all other numbers identical).

**Run order** (later runs overwrite some files of earlier ones — the reference copies are the final
state): validate_provenance → analyze_benford → run_negative_control_validation (overwrites
`results/first_digit_table.csv` with a CRLF variant) → … → run_all (rewrites the canonical LF
`results/first_digit_table.csv`). Run `run_all.py` after `run_negative_control_validation.py` if you
want the canonical tables.

## Known quirks

These are faithful to the original artifact and **must be reproduced** to match the reference numbers:

1. **Three summation modes.** MADs are PAIRWISE-MEAN in pandas-based scripts (`analyze_benford`,
   country-only, year blocks, positive control), SEQ-MEAN in stdlib scripts, FSUM-MEAN where stated.
   Example: the integer negative control MAD is `0.0602555206731196` (pairwise) vs
   `0.06025552067311963` (sequential). Python ≥ 3.12 `sum()` is compensated — do not use it for SEQ-SUM.
2. **Two CSV dialects.** pandas tables (LF, `%.12f`) vs `csv` module tables (CRLF, repr floats or
   `%.12f` as stated per spec).
3. **Four digit-extraction variants** (`common.md` §7): one-significant-digit values get second digit
   `0` (DIGITS-DECIMAL), `None` (DIGITS-NORMALIZE) or are **excluded** (DIGITS-RESIDUAL); inline
   one-liners take `str(v)[0]`. On the pinned population data every variant yields the same digits
   (all 17,195 values have ≥ 2 significant digits, so nothing is excluded); the variants differ on
   synthetic controls and in the unit tests.
4. **Different negative controls.** `scripts/run_negative_control_validation.py` and
   `analyze_benford.py`: numpy integers (`[1000,10000)` resp. `[10000,100000)`, seed 20260717 — same
   first-digit counts); `negative_control_validation.py`: numpy **uniform floats** on `[1000, 9999)`;
   `run_benford_validation.py`: `random.Random(20260717).uniform(1, 10)` formatted `%.12f`. They
   therefore report different control MADs.
5. **Label quirk.** `negative_control_validation.py` uses `marginal conformity` instead of
   `marginally acceptable conformity`; `run_benford_validation.py` classifies the **second** digit
   with first-digit Nigrini cutoffs.
6. **File overwrite.** `run_negative_control_validation.py` overwrites `results/first_digit_table.csv`.
7. **Relocated outputs** (originals wrote into throw-away container dirs or collided with canonical
   files): `results/positive_control_standalone/`, `results/year_block_inline/`,
   `results/negative_control_uniform_float_table.csv`.
8. **Inline programs promoted to files.** Three programs originally shipped inside run commands
   (base64 / `python -c` / heredoc) are specified as `scripts/*_oneliner.py`,
   `scripts/reproduce_positive_control_standalone.py`, `scripts/year_block_plot_inline.py`; two of them
   additionally write their printed JSON to `results/` (marked "addition" in their specs).
9. **Metadata drift.** The World Bank country-metadata API is not immutable; the recorded
   `METADATA_SHA256` no longer reproduces. Specs embed the 47 aggregate codes and add
   `--on-metadata-drift embedded` (see `validate_metadata_filter.md`).
10. **Static vs metadata aggregate lists.** The country-only sensitivity uses a static list of 48
    codes; the metadata filter derives 47 (no `FCS`).
11. **Residual test exclusion.** `second_digit_pvalue_residuals.py` excludes values with < 2
    significant digits and uses its own incomplete-gamma p-value (no SciPy).
