# Pinned World Bank metadata filter

Status: Completed

Reproduce: implement the specs referenced by experiment `pinned-world-bank-metadata-filter` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Completed a smallest concrete validation under the workspace root.

Key result: the metadata-driven filter is reproducible and checksum-gated, but it intentionally updates the prior static filter. The pinned World Bank metadata snapshot marks 47 population-present codes as aggregates via `region.value == Aggregates`; the previous static list had 48 codes. The only prior static code not marked as aggregate in the current metadata is `FCS`, so the metadata-driven sensitivity keeps `FCS` rather than carrying it forward unprovenanced.

Validated inputs:
- Population CSV SHA-256: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`; rows: 17,195.
- World Bank metadata JSON SHA-256: `d29d57f8adf954c5e2a1520a02fb2c7b45575d8db3bd327a9dff47d66914231c`; rows: 295.

Generated aggregate list:
- Codes present in population and marked aggregate by metadata: 47.
- Canonical JSON SHA-256: `18eb78dd7f7093e3dd9e26ae569875ef138f5cb3b2c2d7b1a402016aea1616c8`.
- Rows removed: 3,055.

Rerun sensitivity:
- Full panel first-digit MAD: `0.007314647983807111` (`acceptable conformity`); second-digit MAD: `0.004058150935433028`.
- Metadata country-only panel rows: 14,140; unique codes: 218.
- Metadata country-only first-digit MAD: `0.007540426519039584` (`acceptable conformity`); chi-square: `98.71453554721771` with 8 dof.
- Metadata country-only second-digit MAD: `0.004864316834289349`; chi-square: `50.29048197306566` with 9 dof.

Conclusion: the provenance-backed metadata filter preserves the acceptable first-digit Benford conclusion while making the filtering rule auditable. The old static filter is not exactly reproduced because `FCS` is no longer classified by the current checksum-pinned metadata snapshot.

## Lessons
- A live metadata API can still be made fail-closed by recording a checksum, but it is less stable than an immutable/vendored snapshot; future API changes will intentionally break this validation until reviewed.
- Current World Bank country metadata does not mark legacy population code `FCS` as an aggregate row, even though the old static filter did. Treating the checksum-pinned metadata as authoritative gives a clear, auditable intentional update rather than silently preserving a static exception.
- The country-only Benford conclusion is insensitive to this update: first-digit MAD remains in Nigrini's acceptable-conformity range.
- A pure-stdlib reproducer is sufficient for this validation because the values are integer population counts and only CSV/JSON/hash/math operations are needed.
