# Spec: `tests/test_p_values.py` — optional-SciPy p-value tests for `scripts/analyze_benford.py`

> **Audience**: implementers. **Source of truth for**: the optional-dependency p-value tests.

`ROOT` = parent of `tests/`. Helper `run_snippet(extra_pythonpath=None)` runs a fresh
`sys.executable -c SNIPPET` subprocess (cwd = `ROOT`, `check=True`, captured text output) with
`PYTHONPATH = [extra_pythonpath?] + [ROOT/scripts] + [existing PYTHONPATH?]` joined by `os.pathsep`,
and returns `json.loads(stdout)`. SNIPPET:

```python
import json
import analyze_benford as a
payload = {"method": a.PVALUE_METHOD, "note": a.PVALUE_NOTE,
           "p_zero": a.chi_square_p_value(0.0, 8),
           "scored_p": a.score_first_digits_from_values([10000, 20000, 30000, 40000])["p_value"]}
print(json.dumps(payload, sort_keys=True))
```

1. **scipy available**: if `method is None` (SciPy genuinely absent) assert `p_zero is None` and `note`
   truthy, return. Else assert `method == "scipy.stats.chi2.sf"`, `p_zero` within abs 1e-15 of 1.0,
   `scored_p is not None`, `note is None`.
2. **scipy import fails**: create a temporary directory containing a fake package `scipy/__init__.py`
   (comment only, no `stats` submodule), prepend it to PYTHONPATH → assert `method is None`,
   `p_zero is None`, `scored_p is None`, `"SciPy is not available" in note`.

`python tests/test_p_values.py` runs both and prints `p-value optional-dependency tests passed`.
Requires `analyze_benford` to import its SciPy dependency inside `try/except Exception` (see
`analyze_benford.md`).
