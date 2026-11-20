# CI smoke test for table-driven figure generation

Status: Successful

Reproduce: implement the specs referenced by experiment `ci-smoke-test-for-table-driven-figure-generation` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete CI-style validation for table-driven figure generation.

What ran:
- `python3 scripts/run_all.py --mode full --clean-smoke`
- `scripts/ci_figure_generation_smoke.sh`

Result: passed.

The new smoke script installs `numpy`, `pandas`, and `matplotlib`, verifies/downloads the pinned dataset, runs the Benford analysis to produce result tables, regenerates required publication figures from those tables only, and then validates the figure manifest and outputs.

Key observed outputs:
- Dataset rows: `17195`
- Dataset SHA-256: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`
- First-digit MAD: `0.007314647983807111` (`acceptable conformity`)
- Second-digit MAD: `0.004058150935433028`
- Negative-control MAD: `0.0602555206731196` (`nonconformity`)
- Required figure manifest: `figures/figure_generation_manifest.json`
- Verified required figures:
  - `first_digit_benford.png` — 56145 bytes
  - `first_digit_benford.pdf` — 15832 bytes
  - `second_digit_benford.png` — 55151 bytes
  - `second_digit_benford.pdf` — 16400 bytes

## Lessons
- The existing table-driven figure generator already validates result-table schema and closed-form Benford columns; the smallest useful CI smoke layer is therefore a wrapper that checks dependency installation, pipeline ordering, manifest presence, and concrete file integrity.
- Validating manifest byte counts and SHA-256 values catches more failure modes than merely checking that four files exist.
- Keeping the smoke test under `scripts/` satisfies the artifact-local constraint while making it directly callable from a future GitHub Actions workflow.
- A real repository CI workflow was not added outside `` because the instruction constrained created artifacts to that directory; the included shell script is the CI job body.
