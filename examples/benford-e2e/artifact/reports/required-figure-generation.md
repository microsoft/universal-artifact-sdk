# Required figure generation

Status: Completed

Reproduce: implement the specs referenced by experiment `required-figure-generation` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Completed the smallest concrete validation for required Benford figure generation.

What was added/run:
- Added `scripts/generate_required_figures_from_tables.py`, a table-driven plotting script that validates recorded CSV tables and generates the required PNG and PDF figures without re-reading raw data.
- Ran the full validation chain: digit tests, provenance-gate tests, pinned dataset download/checksum validation, primary analysis, and table-driven figure generation.
- Re-ran the figure-generation script and confirmed stable hashes for all four figure files.

Key validation outputs:
- Dataset provenance gate passed: SHA-256 `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`, row count `17195`, schema match true.
- First-digit MAD: `0.007314647983807111` (`acceptable conformity`), chi-square `100.16554215204238` with `8` dof.
- Second-digit MAD: `0.004058150935433028`, chi-square `49.27746805969423` with `9` dof.
- Negative-control first-digit MAD: `0.0602555206731196` (`nonconformity`).

Generated required figures:
- `figures/first_digit_benford.png` — SHA-256 `a70db6c77fb3e75b5f3310d045b2cb410f5b6cea857be7f194423512797f33c6`
- `figures/first_digit_benford.pdf` — SHA-256 `ad90b4c3b35713a55553dda8969bc5e8d9f6a4acf3f293d59433959e14b561d7`
- `figures/second_digit_benford.png` — SHA-256 `548ad33c1ed8ca2d4a412f584f04185b6aa19c4ecb5d1f23a145b6b5b1383a4d`
- `figures/second_digit_benford.pdf` — SHA-256 `8f3412ccab142824ea9160f599206a059b42a89eb9f6e734cb7096df1e720655`

## Lessons
- Generating figures from recorded CSV result tables makes the paper artifact more auditable than plotting directly from raw data inside the analysis script.
- Validating the theoretical `benford_proportion` and `abs_deviation` columns inside the plotting script catches stale or corrupted result tables while still avoiding recomputation of empirical analysis.
- Matplotlib PDF outputs are not hash-stable by default because metadata can vary; setting fixed PDF metadata made rerun hashes deterministic.
- Keeping both legacy analysis figures and explicitly named required publication figures is useful: the new `*_benford.{png,pdf}` files satisfy the requested output names, while existing `figure1_*`/`figure2_*` remain backward-compatible.
