# Benford end-to-end example: artifact → AEBench evaluation

> **Audience**: anyone running an automated reproduction of an SDK artifact with
> [AEBench](https://github.com/AEBench/AEBench). **Source of truth for**: what this example
> contains and how to run it. The artifact format is defined in [`SPEC.md`](../../SPEC.md).
> This example also uses a few fields that a follow-up change adds to the specification:
> `artifact_kind` (manifest), `implementation` (experiments), and `output_path` and `volatile`
> (results). The same change adds the Artifact Reader and AEBench writer specifications that
> produced `aebench-case/`.

The research question is small and concrete: do the leading digits of the World Bank's
country-by-year population figures follow Benford's Law? The paper (`artifact/paper.pdf`)
answers it with 17,195 population values: the first-digit mean absolute deviation (MAD) is
0.0073, which is "acceptable conformity" by Nigrini's bands, while a deliberately non-Benford
control is rejected.

This example takes that study through the whole path:

1. **Artifact.** `artifact/` is an SDK artifact of kind `spec-artifact`. It ships **no code**:
   each of its 23 experiments has a specification in `artifact/specs/` that says exactly what the
   code must compute and which files it must write. Data is not shipped either; `artifact/DATA.md`
   gives the download URL and SHA-256 of the one input file. The original outputs are kept in
   `artifact/reference-outputs/` as evidence.
2. **Reader.** An Artifact Reader opens the directory read-only and classifies it
   (`spec-artifact`, evaluable, 0 warnings).
3. **Writer.** The AEBench writer turns it into the AEBench case in `aebench-case/`. The task
   the agent sees (`aebench-case/artifact/`) is the artifact **minus** the 16 reference output
   files that the oracle compares against; `aebench-case/artifact/AEBENCH_TASK.md` is the task
   statement.
4. **Agent.** An agent implements the specifications, downloads the data, and runs the
   experiments.
5. **Oracle.** AEBench's four oracle phases grade the workspace. The last phase deletes every
   compared output, re-runs every experiment in a clean copy, and compares the regenerated
   numbers with the reference values, so numbers copied from the paper cannot pass.

For how the SDK is used during research, a diagram of how the components connect, and step-by-step commands, see [`GUIDE.md`](GUIDE.md).

## Layout

| Path | What it is |
|------|------------|
| `artifact/` | The SDK artifact (paper, claims, results, datasets, specs, reference outputs). |
| `artifact/NOTES.md` | How the artifact was prepared, every number in the paper traced to its source file. |
| `aebench-case/` | Generated AEBench case (`case.toml`, task view, oracles, reference values). |
| `aebench-case/WRITER-NOTES.md` | What the writer could not decide; for the case author to refine. |

## Running it

From an AEBench checkout:

```bash
# Is the case well-formed?
aebench case validate path/to/examples/benford-e2e/aebench-case

# Grade a workspace in which an agent (or a person) has implemented the specs:
aebench case oracle path/to/examples/benford-e2e/aebench-case \
  --workspace-dir path/to/workspace --output-dir path/to/oracle-out
```

The oracle runs the experiments' commands with whatever `python3` is first on `PATH`, so run it
in the environment where the implementation's packages are installed (in a full AEBench run,
that is the agent's container). Besides AEBench's phase-level report, every individual check is
written to `oracle-out/aebench-writer-checks.jsonl`, e.g.
`{"phase": "experiment_runs", "check": "result:R3", "ok": true, ...}`.

## What has been verified

- The reader and the writer were each implemented twice from their specifications alone, by
  implementers who saw no other implementation; both passed every conformance test the
  specifications define.
- A separate implementer that saw only the task view (`aebench-case/artifact/`) implemented all
  23 experiments. Its first-digit MAD (0.007314647983807111), second-digit MAD
  (0.004058150935433028) and chi-square statistic (100.16554215204238) equal the reference values
  exactly. `aebench case oracle` on that workspace scores **4/4** (all 90 checks pass); on the
  unimplemented task view it scores 1/4 (only the environment phase passes).
- Not yet run: a full AEBench run with an agent in AEBench's container.

## Known gaps

- **Five results are not graded automatically.** R2, R11, R15, R17 and R19 have only a written
  report as evidence, so their claims need hand-written checks (listed in `WRITER-NOTES.md`).
- **Paper URL.** `case.toml` points at
  `https://raw.githubusercontent.com/microsoft/universal-artifact-sdk/main/examples/benford-e2e/artifact/paper.pdf`,
  which serves the same bytes as `artifact/paper.pdf` (SHA-256 checked).
- **Requests for AEBench** that would tighten the setup:
  1. an option to exclude paths from an `upstream` fetch, so withheld reference outputs never
     reach the agent when the artifact is fetched from git;
  2. per-check results in the oracle report (today only phase status is kept, hence the
     `aebench-writer-checks.jsonl` side file);
  3. emitting an `evaluation-record.yml` (defined in the Artifact Reader specification) after a
     run, so the result is tied to the exact artifact bytes; the writer leaves
     `evaluation-record.template.yml` for this.
