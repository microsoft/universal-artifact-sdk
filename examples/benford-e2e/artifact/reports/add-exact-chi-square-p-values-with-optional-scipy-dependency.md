# Add exact chi-square p-values with optional SciPy dependency

Status: Successful

Reproduce: implement the specs referenced by experiment `add-exact-chi-square-p-values-with-optional-scipy-dependency` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete validation for optional chi-square p-values.

Validation passed:
- `python3 tests/test_p_values.py`
- `python3 scripts/run_all.py --mode pipeline-no-download --clean-smoke`
- A full `analyze_benford.py` run with a fake `scipy` shadow package first on `PYTHONPATH` to simulate SciPy absence.

With SciPy installed, `results/summary.json` now reports:
- `first_digit.p_value = 3.94917604502503e-18`
- `second_digit.p_value = 1.4723898886150244e-07`
- `negative_control.p_value = 0.0` (double-precision underflow for the very large negative-control chi-square)
- `p_value_calculation.method = "scipy.stats.chi2.sf"`

The simulated no-SciPy run at `results/no_scipy_validation/summary.json` completed successfully and wrote null p-values plus an explanatory fallback note. Primary MAD classifications and reproducibility smoke checks remain unchanged.

## Lessons
- The optional dependency can be tested without uninstalling packages by shadowing `scipy` with a fake package on `PYTHONPATH`; this exercises the import-failure fallback while preserving the rest of the Python environment.
- Adding p-values does not alter the MAD-based conformity conclusion: first digit remains acceptable conformity and the uniform one-order control remains nonconforming.
- Very large chi-square statistics can underflow to `0.0` in SciPy's double-precision survival function; this is acceptable here as a conventional numerical p-value report, but should be described as effectively zero rather than exactly mathematically zero.
