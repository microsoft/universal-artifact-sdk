# Reflection

No prior completed runs or lessons were provided. Initial planning lessons: keep dataset provenance first-class and fail closed on checksum/schema mismatch; isolate significant-digit extraction behind tests before computing any empirical claim; reuse one shared scoring path for real data and controls; interpret chi-square cautiously due to large N and temporal/cross-sectional dependence; generate figures only from recorded result tables so the paper remains auditable.

## Dataset provenance and checksum gate
- The pinned GitHub raw URL currently resolves to the expected byte-for-byte artifact, so provenance can be made deterministic after the one network download.
- A pure-stdlib Python validator is sufficient for this gate; optional package versions are recorded when installed but not required.
- Testing the validation function directly catches schema/row-count/checksum regressions cheaply, while an explicit wrong-hash CLI run confirms operational fail-closed behavior.
- The row-count check should remain coupled to the immutable commit URL; if the source URL changes, both checksum and expected row count should be intentionally updated together.

## Tested significant-digit extraction library
Use `Decimal(str(value))` plus fixed-point formatting to keep one normalization path for integers, decimals below one, powers of ten, and scientific notation. Preserve reason-coded exclusions (`zero`, `missing_or_blank`, `non_finite`) so later Benford analysis can report skipped rows transparently. When importing a dataclass module via `importlib.util.module_from_spec`, register it in `sys.modules` before `exec_module`; otherwise postponed annotations can break dataclass processing.

## Primary first-digit Benford conformity analysis
- Provenance gating is essential and cheap: the script fails closed on checksum, schema, or row-count mismatch before any empirical claim is generated.
- The real population dataset conforms acceptably by first-digit MAD but not perfectly; digit 1 is lower than Benford expectation and digit 5 is higher.
- The large-N chi-square is sensitive even for visually/moderately small deviations, so MAD/Nigrini classification is the clearer conformity summary for this artifact.
- The fixed-seed uniform one-order-of-magnitude control produced strong nonconformity, confirming that the scoring path discriminates rather than trivially accepting all numeric inputs.
- Keeping figures generated from recorded CSV result tables makes the artifact auditable.

## Second-digit generalized Benford analysis
- The pinned dataset gate is fast and should remain the first step; it verified checksum, schema, and row count before analysis.
- The second-digit result is stronger than the first-digit result by MAD: second-digit MAD is about 0.00406, while the first-digit MAD is about 0.00731.
- Explicitly recording the one-significant-digit convention avoids ambiguity in second-digit analyses. In this dataset, no rows required that convention.
- The same scoring path continues to discriminate: the fixed-seed single-order-of-magnitude control is clearly non-Benford by MAD.

## Deterministic uniform one-order negative control
- A one-order uniform control is strongly rejected by the same first-digit scoring path used for the real population data, supporting the discriminating-power claim.
- The pinned provenance gate is cheap enough to keep at the start of every run and fail closed before producing empirical claims.
- The real World Bank population data remains in the acceptable MAD conformity range, while the deterministic control is far into nonconformity, making the contrast clear and reproducible.
- Keeping the scoring path in a single shared function (`score_first_digits`) reduces risk that the control and real-data analyses are inadvertently incomparable.

## Positive log-uniform synthetic control
- A six-order log-uniform control with the same retained-row count as the real dataset produces very low first-digit MAD under the existing scoring path.
- Keeping the dataset provenance gate at the start is cheap and preserves consistency with the primary analysis, even for a synthetic-control validation.
- The positive control complements the existing one-order uniform negative control: one fails clearly, while this Benford-like generator is classified as close conformity.
- A focused standalone reproducer can validate this result from a clean Python container with only `numpy` installed.

## Country-only sensitivity analysis excluding aggregate World Bank series
- Reusing the same scoring functions for full-panel and country-only panels avoids introducing analysis-path differences during robustness checks.
- The pinned checksum gate remains valuable even for sensitivity scripts: it ensures the static aggregate-code filter is applied to the exact dataset it documents.
- The country-only filter is explicit and reproducible, but its main limitation is that it uses a documented static aggregate-code list rather than a separately checksummed World Bank metadata file. A future version should vendor or pin metadata for classification provenance.
- Aggregate exclusion changed the first-digit MAD only slightly, from 0.007315 to 0.007368, preserving the acceptable-conformity interpretation.

## Temporal robustness by predeclared year blocks
- The pinned provenance gate remains cheap enough to run at the start of this robustness check.
- Reusing the shared scoring function avoided creating a second analysis path for the temporal diagnostic.
- Temporal robustness is broadly supportive: three of four blocks are acceptable by MAD, and the early 1960-1979 block is marginal rather than nonconforming.
- The block-level chi-square diagnostics should be interpreted cautiously due to temporal/cross-sectional dependence and large sample sizes.

## Required figure generation
- Generating figures from recorded CSV result tables makes the paper artifact more auditable than plotting directly from raw data inside the analysis script.
- Validating the theoretical `benford_proportion` and `abs_deviation` columns inside the plotting script catches stale or corrupted result tables while still avoiding recomputation of empirical analysis.
- Matplotlib PDF outputs are not hash-stable by default because metadata can vary; setting fixed PDF metadata made rerun hashes deterministic.
- Keeping both legacy analysis figures and explicitly named required publication figures is useful: the new `*_benford.{png,pdf}` files satisfy the requested output names, while existing `figure1_*`/`figure2_*` remain backward-compatible.

## End-to-end reproducibility bundle and offline smoke test
- A single orchestrator is useful even for a small study because it prevents reviewers from having to infer the correct order of tests, provenance validation, analysis, and figure generation.
- The provenance JSON intentionally contains a retrieval timestamp, so the deterministic smoke test should compare stable numeric outputs rather than timestamped provenance.
- Re-running analysis twice into the same offline-smoke output directory gives byte-identical numeric hashes because output paths embedded in `summary.json` remain stable.
- Keeping required figures generated from recorded CSV tables preserves auditability: figures can be refreshed without silently recomputing empirical numbers.

## Significant-digit extraction unit tests
A minimal pure-stdlib validation is enough to support the digit-extraction success criterion before running any empirical Benford scoring. Using `Decimal(str(value))` with fixed-point formatting provides one normalization path for integers, decimals below one, negatives, and scientific notation. Returning a structured result with `excluded_reason` makes exclusion counting explicit and testable.

## Benford conformity analysis tables and figures
- The provenance gate remains cheap and effective: checksum, schema, and row-count validation completed before empirical claims were produced.
- The primary population data supports the Benford conformity claim by MAD/Nigrini criteria, while the large-N chi-square is sensitive to modest deviations and should be interpreted cautiously.
- The fixed-seed one-order uniform negative control strongly failed the same scoring path, supporting discriminating power.
- Generating publication figures from recorded result tables, followed by an offline smoke test, gives an auditable path from verified data to figures and summary outputs.

## Negative-control discrimination check
- The checksum/schema/row-count gate is fast enough to include even in this smallest validation and protects the external-input claim.
- Using the exact retained-row count from the verified dataset avoids a hidden sample-size mismatch between real data and control.
- A single-order uniform control is strongly non-Benford under the shared first-digit scoring function, supporting the experiment's negative-control hypothesis.

## Wire tested digit library into Benford analysis
Use `python3` in this environment: the initial `python ...` invocation failed because no unversioned `python` executable is on PATH. Once launched with `python3`, the orchestrator uses `sys.executable` for all child steps. The full validation remains small: it completed in about 5.3 seconds here, including network download, figure generation, and two offline numeric reruns. The checksum gate is cheap enough to run before every empirical claim, and the negative-control result confirms the shared scoring path discriminates rather than accepting arbitrary numeric data.

## Add negative-control validation
The smallest validation is sufficient for Success Criterion 4 because it keeps the checksum/schema/row-count gate before all analysis and then reuses exactly one scoring function for real and synthetic values. The control result is deterministic with NumPy seed `20260717`. The observed control MAD (`0.0602555`) is far from the threshold, so the conclusion is not sensitive to numerical rounding. A compact independent Docker reproducer using only `python:3.11` plus `numpy` reproduces the same key numbers from the pinned URL.

## Add exact chi-square p-values with optional SciPy dependency
- The optional dependency can be tested without uninstalling packages by shadowing `scipy` with a fake package on `PYTHONPATH`; this exercises the import-failure fallback while preserving the rest of the Python environment.
- Adding p-values does not alter the MAD-based conformity conclusion: first digit remains acceptable conformity and the uniform one-order control remains nonconforming.
- Very large chi-square statistics can underflow to `0.0` in SciPy's double-precision survival function; this is acceptable here as a conventional numerical p-value report, but should be described as effectively zero rather than exactly mathematically zero.

## Add paper-ready provenance appendix table
- A provenance appendix should be generated from recorded JSON artifacts rather than recomputing analysis, keeping the paper table auditable and deterministic.
- The appendix table benefits from including both checksum/source metadata and headline analysis/conformity values, because it links external-data provenance to the empirical claim in one compact place.
- Byte-stable regeneration is easy to test by hashing Markdown and LaTeX before and after rerunning the renderer.

## Second-digit p-value and residual diagnostics
- A pure-Python regularized upper incomplete gamma implementation is sufficient here, avoiding a SciPy dependency while making the p-value reproducible from the recorded chi-square and dof.
- Reporting standardized residuals materially improves interpretability: the global chi-square result is not opaque, and digit `0` is clearly the dominant contributor.
- The provenance gate remains cheap and should stay before all empirical claims: checksum, schema, and row-count validation passed before computing diagnostics.
- The generated JSON and Markdown intentionally include a retrieval timestamp, so numeric outputs are deterministic while provenance files update timestamp metadata on rerun.

## Containerized no-mount reproduction bundle
- A slim Python image with only `numpy`, `pandas`, and `matplotlib` is sufficient; SciPy is optional and the existing fallback test passes when it is absent.
- The existing `run_all.py` orchestrator is already suitable as the container entry command because it performs tests, provenance validation, analysis, figure generation, and offline smoke checking.
- No bind mount is needed: copying only `scripts/`, `tests/`, and `README.md` into the image is enough for the end-to-end validation; data/results/figures are created inside the container at runtime.
- The provenance gate remains the critical first empirical step: the container run fetched the pinned URL and verified checksum/schema/row count before analysis.

## Pinned World Bank metadata filter
- A live metadata API can still be made fail-closed by recording a checksum, but it is less stable than an immutable/vendored snapshot; future API changes will intentionally break this validation until reviewed.
- Current World Bank country metadata does not mark legacy population code `FCS` as an aggregate row, even though the old static filter did. Treating the checksum-pinned metadata as authoritative gives a clear, auditable intentional update rather than silently preserving a static exception.
- The country-only Benford conclusion is insensitive to this update: first-digit MAD remains in Nigrini's acceptable-conformity range.
- A pure-stdlib reproducer is sufficient for this validation because the values are integer population counts and only CSV/JSON/hash/math operations are needed.

## Plot temporal robustness diagnostics
- A CSV-backed plotter keeps the diagnostic auditable: the figure is generated from recorded robustness results rather than silently recomputing empirical Benford scores.
- Validating classifications against Nigrini thresholds before plotting catches stale or corrupted `year_block_robustness.csv` rows.
- The temporal diagnostic is visually supportive: three of four blocks are acceptable by MAD, while the earliest block is marginally acceptable rather than nonconforming.

## Benford World Bank population validation
- Keep the checksum/schema/row-count gate before every empirical claim; it is cheap and protects the external-data provenance claim.
- A minimal stdlib-first script is sufficient for analysis and testing; only `matplotlib` is needed for required PNG figures.
- Returning reason-coded digit extraction exclusions makes data-quality reporting explicit; this dataset excluded zero rows.
- MAD/Nigrini classification is the clearest conformity summary here; chi-square should be reported but interpreted cautiously because large N makes modest deviations detectable.
- The same-size one-order uniform negative control strongly discriminates, supporting that the test is not trivially accepting arbitrary numeric inputs.

## CI smoke test for table-driven figure generation
- The existing table-driven figure generator already validates result-table schema and closed-form Benford columns; the smallest useful CI smoke layer is therefore a wrapper that checks dependency installation, pipeline ordering, manifest presence, and concrete file integrity.
- Validating manifest byte counts and SHA-256 values catches more failure modes than merely checking that four files exist.
- Keeping the smoke test under `scripts/` satisfies the artifact-local constraint while making it directly callable from a future GitHub Actions workflow.
- A real repository CI workflow was not added outside the artifact directory because the instruction constrained created artifacts to that directory; the included shell script is the CI job body.
