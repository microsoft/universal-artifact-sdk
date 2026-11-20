# NOTES — provenance, scrubbing and decisions

> **Audience**: reviewers and maintainers of this example. **Source of truth for**: where this artifact
> came from, what was removed or changed and why, and open questions.

## Provenance

* Derived from a real run of an autonomous research agent (July 2026): an empirical check of Benford's
  law on World Bank population data, packaged as an `evaluable-artifact/v2` submission with 23
  experiments, 23 claims and 23 results.
* This version is a **spec-artifact** (`artifact_kind: spec-artifact`): every piece of code (18 shipped
  Python/shell files plus 3 programs that were embedded inline or base64-encoded in run commands) is
  replaced by a Markdown specification under `specs/` that is detailed enough to re-implement the code and
  reproduce the numeric outputs. Data is provided as a download recipe (`DATA.md`), not as files.
* `reference-outputs/` holds the original run's numeric outputs (one copy of each), laid out at the
  workspace-relative path where the implementation writes them (`output_path` in `results.yml`).
  `reports/` holds the agent's per-experiment narrative reports and run records, scrubbed.

## Contents

| Path | What |
|---|---|
| `manifest.yml`, `claims.yml`, `results.yml`, `datasets.yml` | v3 metadata (see below) |
| `specs/` | 25 module/test specs + `common.md` + `README.md` (index, dependency graph, environment, layout, quirks) |
| `experiments/<slug>/README.md` | per-experiment pointer: specs, check, command, data, outputs |
| `reference-outputs/` | 41 numeric/text outputs + 3 main figures (oracle references) |
| `reports/` | 23 scrubbed experiment reports, `research-brief.md` (the original research brief), `run-records/` |
| `paper.tex` | paper source, completed from the evidence (see *Paper completed from evidence*) |
| `paper.pdf` | the paper built from `paper.tex` (6 pages) |
| `references.bib` | bibliography of `paper.tex` (registered as `paper.references_export`) |
| `reflection.md` | the agent's reflection, scrubbed |
| `DATA.md` | data download/verification recipe |

## Decisions

1. **`has_runnable_experiments: false`.** No code ships, so nothing can run until the specs are
   implemented. The SDK would derive `true` from the 23 active experiments; it is set to `false` on purpose
   and `artifact_kind: spec-artifact` signals why.
2. **`implementation`** on every experiment: `kind: spec`, `spec` = main spec, `check` = command that exits 0
   iff the implementation exists and its specified unit tests pass (`python -m py_compile …` for
   experiments whose code has no unit tests). Experiments that need several modules list the others in an
   extension field `implementation.additional_specs` (not part of the v3 schema).
3. **`run.command`** is the plain command run from the workspace root after implementing (no container,
   no base64). Where the original command ran prerequisite steps, they are kept
   (e.g. `validate_provenance.py && analyze_benford.py`). The `dataset-provenance-and-checksum-gate`
   command keeps the original negative check (a wrong expected hash must exit non-zero).
4. **Inline programs became files**: `scripts/negative_control_oneliner.py`,
   `scripts/metadata_filter_oneliner.py`, `scripts/reproduce_positive_control_standalone.py`,
   `scripts/year_block_plot_inline.py`, and the root `significant_digits.py`/`test_significant_digits.py`
   (which the original created through a heredoc). Their outputs were moved to non-colliding paths
   where the original wrote into throw-away container directories; two now also save their printed JSON.
5. **`containerized-no-mount-reproduction-bundle`** and **`ci-smoke-test-…`** originally ran a locally
   built image. The image is replaced by the environment spec in `specs/README.md` §3; the commands run
   the same driver/script directly.
6. **`uses_data`** is declared where a script reads the population CSV from a file. Omitted for experiments
   that need no data (unit tests, the appendix renderer) and for scripts that download the CSV into memory
   (`negative_control_oneliner.py`, `second_digit_pvalue_residuals.py`,
   `reproduce_positive_control_standalone.py`, the metadata one-liner). The metadata dataset is declared in
   `datasets.yml` but not in `uses_data`, because its recorded hash can no longer be reproduced (see `DATA.md`).
7. **Results**: each of the 23 results keeps its id, `produced_by` and `validates`. Where the experiment
   writes a machine-readable output, `evidence` is the reference copy under `reference-outputs/`, with
   `output_path` and `kind: metrics|table`. The other four results (R2, R11, R15, R19) have no output file
   from the code (unit-test transcripts, printed-only output, or a container-level check), so their
   evidence is the narrative report, `kind: artifact`. Each spec's **Oracle** table lists every
   compared file and tolerance, not only the primary one.
8. **Output de-duplication**: the source held up to four copies of some outputs (top-level copies, a
   `_verify` rerun, offline-smoke copies). One canonical copy is kept per output, chosen as the final state
   of the workspace (e.g. `results/first_digit_table.csv` is the LF pandas version written by `run_all.py`,
   not the CRLF copy that `run_negative_control_validation.py` writes before it). `specs/README.md` §5
   states which command produced each file. CSV and PNG reference files are byte-identical to the originals.

## Dropped (and why)

| Item | Reason |
|---|---|
| all `*.py`, `*.sh`, inline/base64 programs in run commands | code → specs |
| `Dockerfile`, container image names/ids | environment is specified in `specs/README.md` §3 |
| `data/population.csv`, `data/world_bank_country_metadata.json`, `data/population_metadata_filter.csv`, other CSV copies | data → recipe (`DATA.md`) |
| `journal.yml` | the 70-entry edit history only records the one-time import (23 experiments, 23 claims, 23 results, the reflection), with the original container/base64 run commands and harness identifiers in every entry; scrubbing them leaves nothing useful |
| `MANIFEST.json`, `.sdk/`, `SECURITY_AUDIT.md`, `security_audit_report.md`, `worker_report.md`, `__pycache__/` | harness internals / not part of the research artifact |
| `research_artifacts/ARTIFACT.md`, `README.md` of the code bundle | described the code bundle and container usage, which no longer ship |
| offline-smoke and no-SciPy duplicate tables/figures, legacy figures, PDF figures, `_verify` rerun, run logs, `*_experiment_run.md` notes | duplicates or harness notes (the JSON run records are kept in `reports/run-records/`) |

## Scrub rules applied (by category)

* **Harness / organisation names**: the producing harness name, its submission id (`id` →
  `benford-world-bank-population`), the harness-specific title prefix (→ plain title; brief renamed
  `reports/research-brief.md`), internal tool and model names — removed. `producer.harness` is
  `research-agent`.
* **Container images**: internal image name → `benford-repro`; image digests → `<redacted-image-id>`.
* **Absolute paths**: the container path prefix of the original run and the agent-output subdirectory
  prefix were removed, so paths are workspace-relative; other scratch paths → `<scratch-file>`.
* **Timestamps**: ISO-8601 timestamps in outputs and reports → `<redacted-timestamp>`.
* **Hosts**: the platform string (contains a cloud-provider kernel tag) → `<redacted-platform>`
  (`redacted-platform` inside the LaTeX appendix).
* **Run commands**: `docker run …`, base64 payloads and heredocs removed from run commands and from the
  `Reproduce:` lines of reports (replaced by a pointer to the specs).
* **Kept on purpose**: every number, hash of data/outputs, the pinned dataset URL, World Bank API URL,
  Python/package versions.
* **Model names in run records**: `reports/run-records/optional_scipy_pvalues_experiment_run.json`
  `proposedBy` → `<redacted-model>`.
* Scrubbing touched only path, timestamp, platform, image and proposer fields; numeric fields are unchanged.

## Known quirks

See `specs/README.md` → *Known quirks* (summation order, CSV dialects, four digit-extraction variants,
four different negative controls, a label variant, a file overwrite, relocated outputs, metadata drift).

## Open questions for the human reviewer

1. `implementation.additional_specs` is an extension field. Should multi-module experiments instead use
   one combined spec per experiment, or should the v3 schema let `spec` be a list?
2. Four results (R2, R11, R15, R19) have only narrative evidence. Should those experiments get a small
   machine-readable output (e.g. a JSON test summary) added to their specs so the oracle can check them?
3. The metadata experiment relies on an embedded code list because the API drifted. Is that acceptable for
   AEBench, or should the experiment be marked as only partly reproducible?
4. SciPy's version was not recorded; p-values are compared with relative tolerance 1e-9.

## Paper completed from evidence; number→source trace table

`paper.tex` was an unfinished draft (title, abstract, Introduction, Background and Related Work, Dataset
and Provenance; no bibliography, five unresolved `\cite` keys). It was completed from the evidence in
this artifact only (`reference-outputs/`, `results.yml`, and, for the narrative-only results R2, R11,
R15 and R19, their `reports/`). No result was recomputed.

**Added sections**: Methods (digit extraction; first/second-digit statistics; MAD with Nigrini bands;
chi-square and p-value method incl. the optional-SciPy path and the pure-Python cross-check; controls;
sensitivity analyses; reproducibility checks), Results (population data, controls, sensitivity,
reproducibility; Tables 2–3, Figures 1–3 from `reference-outputs/figures/*.png`), Threats to Validity
and Limitations, Conclusion, Artifact Availability (points to `specs/` and `DATA.md`), and the
bibliography (`references.bib`, style `ACM-Reference-Format`: the five original keys plus
`pearson1900`).

**Claim coverage**: C1, C17 → Dataset and Provenance / Methods §Reproducibility; C2, C11 → Methods
§Digit extraction, Results §Reproducibility; C3, C12, C22 → Results §Population data, Table 2,
Figure 1; C4, C18 → Results §Population data (second digits, residuals), Figure 2; C5, C13, C15 →
Results §Controls (all three negative-control variants reported); C6 → Results §Controls; C7, C20 →
Results §Sensitivity, Table 3; C8, C21 → Results §Sensitivity, Figure 3 (the marginal 1960–1979 block
is reported); C9, C10, C14, C16, C19, C23 → Methods/Results §Reproducibility. Chi-square rejection of
exact conformity (both digit positions) is reported alongside the MAD result.

**Edits to the existing text** (only where the draft was stronger than or inconsistent with the
evidence, plus typography):

| Where | Before | After | Why |
|---|---|---|---|
| Abstract | "Sensitivity checks excluding aggregate World Bank series and partitioning by year block preserve the main conclusion." | Aggregate exclusion leaves the first-digit class unchanged; three of four year blocks are acceptable and 1960–1979 is marginally acceptable. | `results/year_block_robustness.csv`: 1960–1979 is `marginally acceptable conformity`. |
| Introduction ¶3 | "The answers are affirmative." | Affirmative by the practical effect-size criterion, although large-sample chi-square tests reject exact conformity at both digit positions. | `results/summary.json`: first/second-digit `p_value` 3.9e-18 / 1.5e-7 (claim C18). |
| Background ¶3 | "below 0.015 as marginal conformity" | "below 0.015 as marginally acceptable conformity" | label used by the outputs (`year_block_mad_manifest.json`, `year_block_robustness.csv`). |
| Preamble | `\documentclass[sigconf]{acmart}` | `[sigconf,nonacm]`, `\setcopyright{none}`, `printacmref=false` | removes the template's placeholder conference, DOI and ISBN numbers, which are not evidence. |
| Typography | hashes in `\texttt{}`; Table 1 `{ll}` | `\hashtt{}` (seqsplit, breakable), URL breaks at hex digits, Table 1 `{@{}lp{0.68\columnwidth}@{}}`, `\emergencystretch` | hashes and URL overflowed into the other column; rendered text unchanged. |
| Labels | — | `\label` on the first three sections and both equations | cross-references from the new sections. |
| Abstract, Introduction | MAD and chi-square quoted to 9–12 decimals | MAD to 4 decimals, chi-square to 1 decimal (e.g. 0.0073, 100.2) | readability; same rounding as the rest of the prose (see *Precision*). |

**Build**: `SOURCE_DATE_EPOCH=1763596800 FORCE_SOURCE_DATE=1 latexmk -pdf -interaction=nonstopmode
-halt-on-error paper.tex` (from a directory holding `paper.tex`, `references.bib` and the three PNGs
under `reference-outputs/figures/`). Result: 6 pages, 0 undefined references/citations, no `??`.

**Precision**: in the prose (abstract, introduction and the new sections) MAD is given to 4 decimals,
proportions to 3 decimals (shown as percentages with 1 decimal), chi-square to 1 decimal, p-values to
2 significant figures, and counts exactly. Tables 2–3 keep MAD to 6 decimals (at most 5 significant
digits) and show chi-square to 1 decimal.

**Writing-quality residual**: related work is limited to the five original sources plus Pearson (1900).

**Trace table.** Every number in the paper (the original sections and the new ones) maps to a recorded
value. Not listed: structural numbers (section, table, figure, equation and page numbers), citation
years and bibliographic data, digit labels (for example "digit 5"), constants of the Benford formulas
(Equations 1–3), the degrees-of-freedom formula `K−1`, the name "SHA-256", and layout values in the
LaTeX source. Each row was checked automatically against the source file with the stated rounding.

| # | Number in paper | Quantity | Source file (under `reference-outputs/`) | Field | Recorded value | Rounding |
|---:|---|---|---|---|---|---|
| 1 | 17,195 | data rows / analyzed rows / control sample sizes | `results/provenance.json` | `row_count` | `17195` | exact |
| 2 | 17,196 | file lines incl. header | `results/provenance.json` | `row_count` | `17195` | row_count + 1 header line |
| 3 | 552,112 | bytes | `results/provenance.json` | `byte_count` | `552112` | exact |
| 4 | 7d2dd6a1…088a | SHA-256 of input (printed in full) | `results/provenance.json` | `sha256` | `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a` | substring |
| 5 | 425fc447…0595 | pinned commit | `results/provenance.json` | `source_url` | `https://raw.githubusercontent.com/datasets/population/425fc447a53a2…` | substring |
| 6 | 0 (zero exclusions) | excluded rows | `results/summary.json` | `analysis.excluded_rows` | `0` | exact |
| 7 | 0 (no value lacks a 2nd digit) | values lacking second digit | `results/summary.json` | `second_digit.values_lacking_second_digit` | `0` | exact |
| 8 | 1960 | first year | `results/year_block_robustness_summary.json` | `dataset.year_min` | `1960` | exact |
| 9 | 2024 | last year | `results/year_block_robustness_summary.json` | `dataset.year_max` | `2024` | exact |
| 10 | 265 | distinct codes, full panel | `results/country_only_comparison.csv` | `unique_codes @ panel=full_verified_panel` | `265` | exact |
| 11 | 0.006 | Nigrini band close_conformity_lt | `figures/year_block_mad_manifest.json` | `thresholds.close_conformity_lt` | `0.006` | exact |
| 12 | 0.012 | Nigrini band acceptable_conformity_lt | `figures/year_block_mad_manifest.json` | `thresholds.acceptable_conformity_lt` | `0.012` | exact |
| 13 | 0.015 | Nigrini band marginally_acceptable_conformity_lt | `figures/year_block_mad_manifest.json` | `thresholds.marginally_acceptable_conformity_lt` | `0.015` | exact |
| 14 | 0.015 | predeclared negative-control criterion | `results/negative_control_summary.json` | `success_criterion` | `control MAD >= 0.015 and classified as nonconformity` | substring |
| 15 | 30.1% | Benford P(D1=1) | `results/first_digit_table.csv` | `benford_proportion @ digit=1` | `0.301029995664` | percent, 1 dp |
| 16 | 4.6% | Benford P(D1=9) | `results/first_digit_table.csv` | `benford_proportion @ digit=9` | `0.045757490561` | percent, 1 dp |
| 17 | 28.3% | observed share digit 1 | `results/first_digit_table.csv` | `observed_proportion @ digit=1` | `0.283454492585` | percent, 1 dp |
| 18 | 9.3% | observed share digit 5 | `results/first_digit_table.csv` | `observed_proportion @ digit=5` | `0.092759523117` | percent, 1 dp |
| 19 | 7.9% | Benford P(D1=5) | `results/first_digit_table.csv` | `benford_proportion @ digit=5` | `0.079181246048` | percent, 1 dp |
| 20 | 10.7% | observed share digit 4 | `results/first_digit_table.csv` | `observed_proportion @ digit=4` | `0.106833381797` | percent, 1 dp |
| 21 | 9.7% | Benford P(D1=4) | `results/first_digit_table.csv` | `benford_proportion @ digit=4` | `0.096910013008` | percent, 1 dp |
| 22 | 0.73 | abs deviation digit 2 (percentage points) | `results/first_digit_table.csv` | `abs_deviation @ digit=2` | `0.007263111338` | x100, 2 dp |
| 23 | 0.0073 | first-digit MAD (prose) | `results/summary.json` | `first_digit.mad` | `0.007314647983807111` | 4 dp |
| 24 | 0.007315 | first-digit MAD (Tables 2-3) | `results/summary.json` | `first_digit.mad` | `0.007314647983807111` | 6 dp |
| 25 | 100.2 | first-digit chi-square | `results/summary.json` | `first_digit.chi_square` | `100.16554215204238` | 1 dp |
| 26 | 8 | first-digit dof | `results/summary.json` | `first_digit.dof` | `8` | exact |
| 27 | 3.9e-18 | first-digit p-value | `results/summary.json` | `first_digit.p_value` | `3.94917604502503e-18` | 2 sig. fig. |
| 28 | acceptable conformity | first-digit class | `results/summary.json` | `first_digit.nigrini_classification` | `acceptable conformity` | label |
| 29 | 0.0041 | second-digit MAD (prose) | `results/summary.json` | `second_digit.mad` | `0.004058150935433028` | 4 dp |
| 30 | 0.004058 | second-digit MAD (Tables 2-3) | `results/summary.json` | `second_digit.mad` | `0.004058150935433028` | 6 dp |
| 31 | 49.3 | second-digit chi-square | `results/summary.json` | `second_digit.chi_square` | `49.27746805969423` | 1 dp |
| 32 | 9 | second-digit dof | `results/summary.json` | `second_digit.dof` | `9` | exact |
| 33 | 1.5e-7 | second-digit p-value | `results/summary.json` | `second_digit.p_value` | `1.4723898886150244e-07` | 2 sig. fig. |
| 34 | 1.5e-7 | second-digit p-value (library, agreement check) | `results/summary.json` | `second_digit.p_value` | `1.4723898886150244e-07` | 2 sig. fig. |
| 35 | 1.5e-7 | second-digit p-value (pure Python) | `second_digit_pvalue_residuals_results.json` | `analysis.p_value` | `1.472389888615024e-07` | 2 sig. fig. |
| 36 | 13.4% | observed share 2nd digit 0 | `results/second_digit_table.csv` | `observed_proportion @ digit=0` | `0.134341378308` | percent, 1 dp |
| 37 | 12.0% | Benford P(D2=0) | `results/second_digit_table.csv` | `benford_proportion @ digit=0` | `0.119679268597` | percent, 1 dp |
| 38 | +5.56 | standardized residual digit 0 | `second_digit_pvalue_residuals_by_digit.csv` | `standardized_residual @ digit=0` | `5.557610312342366` | 2 dp |
| 39 | -2.83 | standardized residual digit 5 | `second_digit_pvalue_residuals_by_digit.csv` | `standardized_residual @ digit=5` | `-2.829509328898171` | 2 dp |
| 40 | -2.16 | standardized residual digit 4 | `second_digit_pvalue_residuals_by_digit.csv` | `standardized_residual @ digit=4` | `-2.1622444382638566` | 2 dp |
| 41 | -1.53 | standardized residual digit 3 | `second_digit_pvalue_residuals_by_digit.csv` | `standardized_residual @ digit=3` | `-1.5333909658053555` | 2 dp |
| 42 | 0.74 | standardized residual digit 9 | `second_digit_pvalue_residuals_by_digit.csv` | `standardized_residual @ digit=9` | `0.7447178861996572` | 2 dp |
| 43 | 20260717 | negative-control seed | `results/negative_control_validation_summary.json` | `negative_control.control_seed` | `20260717` | exact |
| 44 | 1000 | integer control lower bound | `results/negative_control_validation_summary.json` | `negative_control.control_low_inclusive` | `1000` | exact |
| 45 | 10000 | integer control upper bound (exclusive) | `results/negative_control_validation_summary.json` | `negative_control.control_high_exclusive` | `10000` | exact |
| 46 | [10000,100000) | integer control range, main script | `results/summary.json` | `negative_control.description` | `Uniform random integers over one order of magnitude [10000, 100000)…` | substring |
| 47 | 0.0603 | integer control MAD (prose) | `results/summary.json` | `negative_control.first_digit_mad` | `0.0602555206731196` | 4 dp |
| 48 | 0.060256 | integer control MAD (Table 2) | `results/summary.json` | `negative_control.first_digit_mad` | `0.0602555206731196` | 6 dp |
| 49 | 6978.6 | integer control chi-square | `results/negative_control_validation_summary.json` | `negative_control.control_chi_square` | `6978.557246295499` | 1 dp |
| 50 | 0 (p underflows) | integer control p-value | `results/summary.json` | `negative_control.p_value` | `0.0` | exact |
| 51 | 11.1% | integer control share digit 1 | `results/negative_control_first_digit_table.csv` | `observed_proportion @ digit=1` | `0.110962489096` | percent, 1 dp |
| 52 | [1000,9999] | float control range | `results/negative_control_summary.json` | `control_distribution` | `uniform[1000.0, 9999.0]` | substring |
| 53 | 0.060889 | float control [1000,9999] MAD (Table 2) | `results/negative_control_summary.json` | `control_first_digit_mad` | `0.060888779695445226` | 6 dp |
| 54 | 0.0609 | float control [1000,9999] MAD (prose) | `results/negative_control_summary.json` | `control_first_digit_mad` | `0.060888779695445226` | 4 dp |
| 55 | 6897.7 | float control [1000,9999] chi-square | `results/negative_control_summary.json` | `control_chi_square` | `6897.74230178361` | 1 dp |
| 56 | [1,10) | float control range | `benford_validation_run/summary.json` | `analysis.negative_control.description` | `same-size fixed-seed uniform random values on [1, 10), scored throu…` | substring |
| 57 | 0.060501 | float control [1,10) MAD (Table 2) | `benford_validation_run/summary.json` | `analysis.negative_control.first_digit_mad` | `0.06050107008993974` | 6 dp |
| 58 | 0.0605 | float control [1,10) MAD (prose) | `benford_validation_run/summary.json` | `analysis.negative_control.first_digit_mad` | `0.06050107008993974` | 4 dp |
| 59 | 7312.3 | float control [1,10) chi-square | `benford_validation_run/summary.json` | `analysis.negative_control.chi_square` | `7312.294283374889` | 1 dp |
| 60 | 0 | log10 range min | `results/positive_control_summary.json` | `positive_control.generation_log10_min` | `0.0` | exact |
| 61 | 6 | log10 range max / orders of magnitude | `results/positive_control_summary.json` | `positive_control.generation_orders_of_magnitude` | `6.0` | exact |
| 62 | 424242 | positive-control seed | `results/positive_control_summary.json` | `positive_control.positive_control_seed` | `424242` | exact |
| 63 | 0.0016 | positive control MAD (prose) | `results/positive_control_summary.json` | `positive_control.positive_control_first_digit_mad` | `0.001620904667174733` | 4 dp |
| 64 | 0.001621 | positive control MAD (Table 2) | `results/positive_control_summary.json` | `positive_control.positive_control_first_digit_mad` | `0.001620904667174733` | 6 dp |
| 65 | 6.2 | positive control chi-square | `results/positive_control_summary.json` | `positive_control.positive_control_first_digit_chi_square` | `6.177076780388321` | 1 dp |
| 66 | 29.7% | positive control share digit 1 | `results/positive_control_first_digit_table.csv` | `observed_proportion @ digit=1` | `0.296946786857` | percent, 1 dp |
| 67 | 48 | static aggregate codes | `results/country_only_summary.json` | `filter.removed_unique_codes` | `48` | exact |
| 68 | 3,120 | rows removed (static) | `results/country_only_summary.json` | `filter.removed_rows` | `3120` | exact |
| 69 | 14,075 | country-only rows (static) | `results/country_only_summary.json` | `filter.country_only_rows` | `14075` | exact |
| 70 | 217 | country-only codes (static) | `results/country_only_summary.json` | `filter.country_only_unique_codes` | `217` | exact |
| 71 | 0.007368 | country-only first-digit MAD (Table 3) | `results/country_only_summary.json` | `country_only_panel.first_digit.mad` | `0.007368305779942078` | 6 dp |
| 72 | 0.0074 | country-only first-digit MAD (prose) | `results/country_only_summary.json` | `country_only_panel.first_digit.mad` | `0.007368305779942078` | 4 dp |
| 73 | 95.3 | country-only first-digit chi-square | `results/country_only_summary.json` | `country_only_panel.first_digit.chi_square` | `95.27635914018896` | 1 dp |
| 74 | 0.004879 | country-only second-digit MAD (Table 3) | `results/country_only_summary.json` | `country_only_panel.second_digit.mad` | `0.004879224846278068` | 6 dp |
| 75 | 0.0049 | country-only second-digit MAD (prose) | `results/country_only_summary.json` | `country_only_panel.second_digit.mad` | `0.004879224846278068` | 4 dp |
| 76 | 50.4 | country-only second-digit chi-square | `results/country_only_summary.json` | `country_only_panel.second_digit.chi_square` | `50.42119107093672` | 1 dp |
| 77 | 47 | metadata aggregate codes | `results/metadata_country_only_summary.json` | `filter.removed_unique_codes` | `47` | exact |
| 78 | 3,055 | rows removed (metadata) | `results/metadata_country_only_summary.json` | `filter.removed_rows` | `3055` | exact |
| 79 | 14,140 | country-only rows (metadata) | `results/metadata_country_only_summary.json` | `filter.country_only_rows` | `14140` | exact |
| 80 | 218 | country-only codes (metadata) | `results/metadata_country_only_summary.json` | `filter.country_only_unique_codes` | `218` | exact |
| 81 | 0.007540 | metadata panel first-digit MAD (Table 3) | `results/metadata_country_only_summary.json` | `metadata_country_only_panel.first_digit.mad` | `0.007540426519039584` | 6 dp |
| 82 | 0.0075 | metadata panel first-digit MAD (prose) | `results/metadata_country_only_summary.json` | `metadata_country_only_panel.first_digit.mad` | `0.007540426519039584` | 4 dp |
| 83 | 98.7 | metadata panel first-digit chi-square | `results/metadata_country_only_summary.json` | `metadata_country_only_panel.first_digit.chi_square` | `98.71453554721771` | 1 dp |
| 84 | 0.004864 | metadata panel second-digit MAD (Table 3) | `results/metadata_country_only_summary.json` | `metadata_country_only_panel.second_digit.mad` | `0.004864316834289349` | 6 dp |
| 85 | 0.0049 | metadata panel second-digit MAD (prose) | `results/metadata_country_only_summary.json` | `metadata_country_only_panel.second_digit.mad` | `0.004864316834289349` | 4 dp |
| 86 | 50.3 | metadata panel second-digit chi-square | `results/metadata_country_only_summary.json` | `metadata_country_only_panel.second_digit.chi_square` | `50.29048197306566` | 1 dp |
| 87 | 1960–1979 | year-block bounds | `results/year_block_robustness.csv` | `block @ block=1960-1979` | `1960-1979` | exact |
| 88 | 5,280 | rows 1960-1979 | `results/year_block_robustness.csv` | `sample_size @ block=1960-1979` | `5280` | exact |
| 89 | 0.012916 | first-digit MAD 1960-1979 (Table 3) | `results/year_block_robustness.csv` | `first_digit_mad @ block=1960-1979` | `0.012916039293` | 6 dp |
| 90 | 0.0129 | first-digit MAD 1960-1979 (prose) | `results/year_block_robustness.csv` | `first_digit_mad @ block=1960-1979` | `0.012916039293` | 4 dp |
| 91 | 1980–1999 | year-block bounds | `results/year_block_robustness.csv` | `block @ block=1980-1999` | `1980-1999` | exact |
| 92 | 5,290 | rows 1980-1999 | `results/year_block_robustness.csv` | `sample_size @ block=1980-1999` | `5290` | exact |
| 93 | 0.010819 | first-digit MAD 1980-1999 (Table 3) | `results/year_block_robustness.csv` | `first_digit_mad @ block=1980-1999` | `0.010819211214` | 6 dp |
| 94 | 2000–2019 | year-block bounds | `results/year_block_robustness.csv` | `block @ block=2000-2019` | `2000-2019` | exact |
| 95 | 5,300 | rows 2000-2019 | `results/year_block_robustness.csv` | `sample_size @ block=2000-2019` | `5300` | exact |
| 96 | 0.008670 | first-digit MAD 2000-2019 (Table 3) | `results/year_block_robustness.csv` | `first_digit_mad @ block=2000-2019` | `0.008670439119` | 6 dp |
| 97 | 2020–2024 | year-block bounds | `results/year_block_robustness.csv` | `block @ block=2020-2024` | `2020-2024` | exact |
| 98 | 1,325 | rows 2020-2024 | `results/year_block_robustness.csv` | `sample_size @ block=2020-2024` | `1325` | exact |
| 99 | 0.010653 | first-digit MAD 2020-2024 (Table 3) | `results/year_block_robustness.csv` | `first_digit_mad @ block=2020-2024` | `0.010652512951` | 6 dp |
| 100 | four / three of four | blocks; blocks in acceptable band | `results/year_block_robustness.csv` | `row count; nigrini_classification` | `4 rows; 3 'acceptable conformity'` | count |
| 101 | six | driver steps | `results/run_all_manifest.json` | `len(steps)` | `6` | count |
| 102 | two | offline reruns | `results/offline_smoke_report.json` | `hashes_first_rerun, hashes_second_rerun` | `2 hash sets` | count |
| 103 | 3 | numeric outputs compared | `results/offline_smoke_report.json` | `len(numeric_outputs)` | `3` | count |
| 104 | 5 | unit tests (independent suite) | `test_output.txt` | `'Ran N tests'` | `5` | exact |
| 105 | 3.10.12 | python version | `results/provenance.json` | `software_versions.python` | `3.10.12 (main, Jun 22 2026, 18:55:27) [GCC 11.4.0]` | prefix |
| 106 | 2.2.6 | numpy version | `results/provenance.json` | `software_versions.numpy` | `2.2.6` | prefix |
| 107 | 2.3.3 | pandas version | `results/provenance.json` | `software_versions.pandas` | `2.3.3` | prefix |
| 108 | 3.10.8 | matplotlib version | `results/provenance.json` | `software_versions.matplotlib` | `3.10.8` | prefix |
