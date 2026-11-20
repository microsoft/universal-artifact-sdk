# Dataset provenance and checksum gate

Status: Completed

Reproduce: implement the specs referenced by experiment `dataset-provenance-and-checksum-gate` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete validation under the workspace root.

Results:
- Unit tests passed: `tests/test_provenance_gate.py` prints `ok`.
- Pinned dataset downloaded and persisted to `data/population.csv`.
- SHA-256 verified exactly: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`.
- Data rows verified: `17195` data rows (`17196` file lines including header).
- Byte count recorded: `552112` bytes.
- Header/schema verified: `Country Name`, `Country Code`, `Year`, `Value`.
- Provenance written to `results/provenance.json` with source URL, UTC retrieval timestamp, checksum, row count, schema, attribution, and software versions.
- Fail-closed behavior validated by running the validator against the verified local CSV with an all-zero expected hash; it exited with code `1` and printed a loud checksum mismatch before analysis.

This completes the dataset provenance/checksum gate, not the downstream Benford digit analysis.

## Lessons
- The pinned GitHub raw URL currently resolves to the expected byte-for-byte artifact, so provenance can be made deterministic after the one network download.
- A pure-stdlib Python validator is sufficient for this gate; optional package versions are recorded when installed but not required.
- Testing the validation function directly catches schema/row-count/checksum regressions cheaply, while an explicit wrong-hash CLI run confirms operational fail-closed behavior.
- The row-count check should remain coupled to the immutable commit URL; if the source URL changes, both checksum and expected row count should be intentionally updated together.
