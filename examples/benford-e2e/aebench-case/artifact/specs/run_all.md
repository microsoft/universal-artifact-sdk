# Spec: `scripts/run_all.py` — one-command reproducibility driver + offline smoke test

> **Audience**: implementers. **Source of truth for**: experiments
> `end-to-end-reproducibility-bundle-and-offline-smoke-test`,
> `benford-conformity-analysis-tables-and-figures`, `wire-tested-digit-library-into-benford-analysis`,
> `add-exact-chi-square-p-values-with-optional-scipy-dependency`,
> `containerized-no-mount-reproduction-bundle`. Standard library only (drives other scripts).

CLI: `python scripts/run_all.py [--mode full|offline-smoke|tests|pipeline-no-download] [--clean-smoke]`
(default `full`). All child processes run with `cwd` = workspace root, using `sys.executable`.

## Steps

`run_step(label, cmd)`: print `\n==> {label}\n$ {cmd joined by spaces}`, run with captured text output,
echo stdout/stderr, record `{label, command (list of str), returncode, elapsed_seconds (round 3)}`.
Non-zero return → `SystemExit(json.dumps({"status": "failed", "failed_step": result}, indent=2))`.

* **tests**: `tests/test_digits.py` ("digit extraction unit tests"), `tests/test_provenance_gate.py`
  ("provenance gate unit tests"), `tests/test_p_values.py` ("optional chi-square p-value tests").
* **full pipeline**: `scripts/validate_provenance.py` ("download and verify pinned dataset"; with
  `skip_download`: `--source-file data/population.csv`, label "re-verify cached pinned dataset without
  network"), `scripts/analyze_benford.py` ("primary Benford analysis and legacy figures"),
  `scripts/generate_required_figures_from_tables.py` ("required figures generated from recorded tables").
* **offline smoke**: requires `data/population.csv` (else `SystemExit("Cached verified data not found
  for offline smoke: …")`); create `results/offline_smoke/`, `figures/offline_smoke/`; run
  `scripts/analyze_benford.py --data data/population.csv --results-dir results/offline_smoke
  --figures-dir figures/offline_smoke` twice (labels "offline numeric rerun A/B from cached verified
  CSV"), hashing `first_digit_table.csv`, `second_digit_table.csv`, `summary.json` after each.
  `stable = hashes_a == hashes_b`. Write `results/offline_smoke_report.json` (JSON-STD):
  `{status: "ok"|"failed", description: "Offline smoke test: run analysis twice from cached verified CSV and compare numeric output SHA-256 hashes.",
  network_used: false, cached_data_path, cached_data_sha256, steps: [A, B],
  numeric_outputs: [the 3 names], hashes_first_rerun, hashes_second_rerun,
  stable_numeric_output_hashes, key_metrics: {analyzed_rows, excluded_rows, first_digit_mad,
  first_digit_classification, second_digit_mad, negative_control_mad, negative_control_classification}}`
  (key_metrics read from the smoke `summary.json`). Unstable → `SystemExit`.

## Modes

`--clean-smoke` first deletes `results/offline_smoke/` and `figures/offline_smoke/`.
`full` = tests + full pipeline + smoke; `tests` = tests; `pipeline-no-download` = tests + pipeline with
`skip_download` + smoke; `offline-smoke` = smoke only.
Finally write `results/run_all_manifest.json` (JSON-STD): `{status: "ok", mode, elapsed_seconds,
steps, offline_smoke (report or null), artifact_root}`; print it; exit 0.

## Oracle

| file | compared fields | tolerance |
|---|---|---|
| `results/offline_smoke_report.json` | `status` ok, `stable_numeric_output_hashes` true, `cached_data_sha256` = EXPECTED_SHA256, `key_metrics.*`, `hashes_first_rerun` (equal to the sha256 of the byte-identical reference tables/summary when the environment matches) | metrics: ints/labels exact, floats rel 1e-12; hashes informational |
| `results/run_all_manifest.json` | `status`, `mode`, list of step labels, every `returncode == 0` | exact |
| plus every output of `analyze_benford.md` and `generate_required_figures_from_tables.md` | as in those specs | — |

Note: the `summary.json` hash depends on the SciPy p-value bits and on `data_path` strings; only
`stable_numeric_output_hashes` is a hard requirement.
