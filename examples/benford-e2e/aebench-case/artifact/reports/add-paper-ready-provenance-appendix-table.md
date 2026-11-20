# Add paper-ready provenance appendix table

Status: Completed

Reproduce: implement the specs referenced by experiment `add-paper-ready-provenance-appendix-table` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete validation for the provenance-appendix experiment. Added `scripts/render_provenance_appendix.py`, which reads only `results/provenance.json` and `results/summary.json` and emits stable Markdown and LaTeX appendix tables.

Generated artifacts:
- `results/provenance_appendix.md`
- `results/provenance_appendix.tex`
- `provenance_appendix_experiment_run.md`
- `provenance_appendix_experiment_run.json`

Validation performed:
- Renderer produced 15 table rows.
- Reran renderer and verified byte-stable output hashes.
- Checked the Markdown table contains JSON-derived source URL, SHA-256, retrieval timestamp, row counts, exclusions, first-digit MAD/classification, and negative-control MAD/classification.
- Deterministic output hashes: Markdown `37a2d25ef2717babac5e6a0fd7f60cd1d163f5c129745884c56780edeeb0f3eb`; LaTeX `6c1e43da8cece111e60306ad4d54d0ec3fb338253a65d1c755d624b5f8cd0a6c`.

## Lessons
- A provenance appendix should be generated from recorded JSON artifacts rather than recomputing analysis, keeping the paper table auditable and deterministic.
- The appendix table benefits from including both checksum/source metadata and headline analysis/conformity values, because it links external-data provenance to the empirical claim in one compact place.
- Byte-stable regeneration is easy to test by hashing Markdown and LaTeX before and after rerunning the renderer.
