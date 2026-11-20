# Second-digit p-value and residual diagnostics

Status: Completed

Reproduce: implement the specs referenced by experiment `second-digit-p-value-and-residual-diagnostics` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Created and ran the smallest concrete validation under the workspace root.

The validation script downloads the pinned World Bank population CSV, verifies SHA-256, schema, and row count before analysis, then computes the second significant digit distribution, generalized-Benford expected proportions, chi-square statistic, pure-Python chi-square survival-function p-value, and standardized residuals for all digits 0–9.

Key results:
- Dataset rows verified: 17,195
- Analyzed rows: 17,195
- Excluded rows: 0
- Second-digit MAD: 0.004058150935433028
- Chi-square: 49.27746805969423
- Degrees of freedom: 9
- p-value: 1.472389888615024e-07
- Largest absolute standardized residual: digit 0, residual 5.557610312342366

Interpretation: the second-digit MAD remains small/practically conforming, but the large-N chi-square p-value is very small. Residual diagnostics show the rejection is driven most strongly by excess second digit `0`, followed by deficits for digits `5` and `4`.

## Lessons
- A pure-Python regularized upper incomplete gamma implementation is sufficient here, avoiding a SciPy dependency while making the p-value reproducible from the recorded chi-square and dof.
- Reporting standardized residuals materially improves interpretability: the global chi-square result is not opaque, and digit `0` is clearly the dominant contributor.
- The provenance gate remains cheap and should stay before all empirical claims: checksum, schema, and row-count validation passed before computing diagnostics.
- The generated JSON and Markdown intentionally include a retrieval timestamp, so numeric outputs are deterministic while provenance files update timestamp metadata on rerun.
