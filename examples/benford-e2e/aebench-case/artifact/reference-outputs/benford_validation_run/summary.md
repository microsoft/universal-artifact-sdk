# Benford World Bank Population Validation

Interpretation: **supports primary Benford conformity claim by MAD; chi-square is sensitive at this sample size; negative control is nonconforming**.

## Dataset provenance

- Source URL: `https://raw.githubusercontent.com/datasets/population/425fc447a53a26c767a15a7de60c4cc2478a0595/data/population.csv`
- Retrieval timestamp (UTC): `<redacted-timestamp>`
- SHA-256: `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`
- Data rows: `17195`
- Schema: `Country Name, Country Code, Year, Value`

## Results

- Rows analyzed: 17195 / 17195
- Rows excluded: 0 ({})
- First digit MAD: 0.007314648 (acceptable conformity); chi-square=100.165542, dof=8
- Second digit MAD: 0.004058151 (close conformity); chi-square=49.277468, dof=9
- Negative control first digit MAD: 0.060501070 (nonconformity); chi-square=7312.294283, dof=8

## Artifact files

- provenance_json: `provenance.json`
- summary_json: `summary.json`
- summary_markdown: `summary.md`
- first_digit_csv: `first_digit_results.csv`
- second_digit_csv: `second_digit_results.csv`
- negative_control_csv: `negative_control_first_digit_results.csv`
- figure1: `figure1_first_digit_benford.png`
- figure2: `figure2_second_digit_benford.png`
- downloaded_csv: `population.csv`
