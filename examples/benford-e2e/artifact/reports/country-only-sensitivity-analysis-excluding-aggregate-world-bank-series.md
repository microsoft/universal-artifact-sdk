# Country-only sensitivity analysis excluding aggregate World Bank series

Status: Successful

Reproduce: implement the specs referenced by experiment `country-only-sensitivity-analysis-excluding-aggregate-world-bank-series` in `manifest.yml` (see `specs/README.md` §5) and run that experiment's `run.command`.

## Summary
Implemented and ran the smallest concrete validation for the country-only sensitivity experiment.

Key results:
- Dataset checksum/schema/row-count gate passed: SHA-256 `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`, 17,195 rows.
- Removed 48 aggregate World Bank codes, totaling 3,120 rows.
- Country/territory-only panel: 217 unique codes, 14,075 analyzed rows, 0 exclusions.
- Full panel first-digit MAD: 0.007314647984, chi-square: 100.165542152042, class: acceptable conformity.
- Country-only first-digit MAD: 0.007368305780, chi-square: 95.276359140189, class: acceptable conformity.
- Full panel second-digit MAD: 0.004058150935, chi-square: 49.277468059694.
- Country-only second-digit MAD: 0.004879224846, chi-square: 50.421191070937.

Conclusion: excluding World Bank aggregate region/income/world series does not materially change the first-digit conclusion; country-only data remains in Nigrini's acceptable conformity range. The second-digit generalized Benford MAD remains small. This supports the robustness claim that the main Benford conformity finding is not driven solely by aggregate World Bank entries.

## Lessons
- Reusing the same scoring functions for full-panel and country-only panels avoids introducing analysis-path differences during robustness checks.
- The pinned checksum gate remains valuable even for sensitivity scripts: it ensures the static aggregate-code filter is applied to the exact dataset it documents.
- The country-only filter is explicit and reproducible, but its main limitation is that it uses a documented static aggregate-code list rather than a separately checksummed World Bank metadata file. A future version should vendor or pin metadata for classification provenance.
- Aggregate exclusion changed the first-digit MAD only slightly, from 0.007315 to 0.007368, preserving the acceptable-conformity interpretation.
