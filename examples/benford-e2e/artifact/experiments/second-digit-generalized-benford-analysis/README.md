# Experiment `second-digit-generalized-benford-analysis`

Code for this experiment is **not shipped**; it is supplied as specifications.

* Implement: [`specs/analyze_benford.md`](../../specs/analyze_benford.md) (shared definitions: [`specs/common.md`](../../specs/common.md)).
* Check: `python tests/test_digits.py && python tests/test_provenance_gate.py`
* Run (from the workspace root): `python scripts/validate_provenance.py && python scripts/analyze_benford.py`
* Input data: `wb-population` at `data/population.csv` (see [`DATA.md`](../../DATA.md)).
* Primary output: `results/second_digit_table.csv` — reference copy [`reference-outputs/results/second_digit_table.csv`](../../reference-outputs/results/second_digit_table.csv).
* Narrative report of the original run: [`reports/second-digit-generalized-benford-analysis.md`](../../reports/second-digit-generalized-benford-analysis.md).
