# Spec: `scripts/negative_control_oneliner.py` — inline negative-control cross-check

> **Audience**: implementers. **Source of truth for**: the one-line program executed by experiment
> `add-negative-control-validation` (originally a `python -c` string). numpy + stdlib.

No CLI flags. Additionally writes its printed object to `results/negative_control_oneliner.json`
(addition; the original only printed).

1. Download `PINNED_URL` (no timeout); `sha = sha256(raw)`;
   `rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))`; `assert sha == EXPECTED_SHA256`;
   `assert len(rows) == 17195`.
2. `probs = BENFORD1`. `score(vals)`: `c = Counter(int(str(v).strip()[0]) for v in vals)` (DIGITS-STR —
   assumes positive integers without leading zeros), `n = len(vals)`;
   `mad = SEQ-SUM_{d=1..9} |c.get(d,0)/n − p_d| / 9`; `chi_square = SEQ-SUM (c.get(d,0) − n p_d)²/(n p_d)`;
   returns `{n, mad, chi_square, counts}`.
3. `real = score([r["Value"] for r in rows])`; `rng = numpy.random.default_rng(20260717)`;
   `control = score(rng.integers(1000, 10000, size=real["n"], endpoint=False))`.
4. `out = {sha256, row_count, real_mad, control_mad, control_chi_square,
   control_classification: "nonconformity" if control_mad >= 0.015 else "not_nonconformity"}`;
   print `json.dumps(out, sort_keys=True, indent=2)`; write it (JSON-STD); then
   `assert control_mad >= 0.015` (non-zero exit otherwise).

## Oracle (no shipped reference file)

`row_count` 17195; `real_mad` rel 1e-12 of `0.007314647983807111`; `control_mad` rel 1e-12 of
`0.06025552067311963`; `control_chi_square` rel 1e-12 of `6978.557246295499`;
`control_classification` `nonconformity`; exit 0.
