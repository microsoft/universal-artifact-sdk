# Spec: `scripts/ci_figure_generation_smoke.sh` — CI smoke test for table-driven figures

> **Audience**: implementers. **Source of truth for**: experiment
> `ci-smoke-test-for-table-driven-figure-generation`. Bash, run from the workspace root.

`set -euo pipefail`; `PYTHON_BIN="${PYTHON_BIN:-python3}"`. Steps (any failure → non-zero exit):

1. `$PYTHON_BIN -m pip install --quiet --no-cache-dir numpy pandas matplotlib`
2. `$PYTHON_BIN scripts/validate_provenance.py`
3. `$PYTHON_BIN scripts/analyze_benford.py`
4. `$PYTHON_BIN scripts/generate_required_figures_from_tables.py`
5. Inline Python check of `figures/figure_generation_manifest.json`:
   * file exists (`missing manifest: <path>`), `status == "ok"` (`manifest status is not ok: …`);
   * `generated_figures` is a list of exactly 4 (`expected 4 generated figures, found N`);
   * for each entry: resolve `path` (relative → against cwd); must exist
     (`manifest figure missing on disk: …`), size > 0 (`figure is empty: …`), `bytes` equals size
     (`manifest byte count mismatch …`), `sha256` equals file digest (`manifest SHA-256 mismatch …`);
   * the set of basenames ⊇ `{first_digit_benford.png, first_digit_benford.pdf,
     second_digit_benford.png, second_digit_benford.pdf}` (`manifest missing expected figures: …`);
   * print `{"status": "ok", "manifest": "<path>", "verified_figures": [sorted names]}` (indent 2).

Oracle: exit code 0 and the printed status `ok` with the four names. Reference outputs are those of
`generate_required_figures_from_tables.md`.
