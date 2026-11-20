# Containerized no-mount reproduction bundle

Status: Successful

Reproduce: implement the specs referenced by experiment `containerized-no-mount-reproduction-bundle` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Created and validated a no-mount container reproduction bundle.

Build command used:

```bash
docker build -t benford-repro:latest -f Dockerfile .
```

Validation command used:

```bash
docker run --rm benford-repro:latest python3 scripts/run_all.py --mode full --clean-smoke
```

The no-mount container run passed the digit/provenance/p-value tests, downloaded the pinned World Bank population CSV, verified SHA-256 `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`, generated tables/figures, and passed the offline deterministic smoke rerun. Key reproduced metrics: 17,195 analyzed rows, 0 excluded rows, first-digit MAD `0.007314647983807111` (`acceptable conformity`), second-digit MAD `0.004058150935433028`, negative-control MAD `0.0602555206731196` (`nonconformity`). Offline numeric output hashes were stable across two reruns.

## Lessons
- A slim Python image with only `numpy`, `pandas`, and `matplotlib` is sufficient; SciPy is optional and the existing fallback test passes when it is absent.
- The existing `run_all.py` orchestrator is already suitable as the container entry command because it performs tests, provenance validation, analysis, figure generation, and offline smoke checking.
- No bind mount is needed: copying only `scripts/`, `tests/`, and `README.md` into the image is enough for the end-to-end validation; data/results/figures are created inside the container at runtime.
- The provenance gate remains the critical first empirical step: the container run fetched the pinned URL and verified checksum/schema/row count before analysis.
