> **Audience**: Builders of the bridge from Universal Artifact SDK artifacts to the
> [AEBench](https://github.com/AEBench/AEBench) artifact-evaluation benchmark, and AEBench case
> authors who refine its output.
> **Source of truth for**: How an artifact becomes an AEBench case bundle: applicability by
> artifact kind, the task view, `case.toml` fields, the generated task instructions, reference
> values and tolerances, the four oracle phases, and what is left to a human.

# AEBench Writer — Specification

**Spec ID:** `aebench-writer/v1` · **Status:** DRAFT · **Input:** the read model of the
[Artifact Reader](../artifact-reader-spec/README.md) · **Output:** an AEBench case bundle as
defined by AEBench's [`docs/howtos/add_case.md`](https://github.com/AEBench/AEBench/blob/main/docs/howtos/add_case.md)
(checked against AEBench commit `0e93841`)

AEBench evaluates an AI agent on artifact evaluation: the agent receives an artifact and
instructions, works in an isolated workspace, and an oracle scores what it leaves behind in four
phases (`env_setup`, `artifact_build`, `benchmark_prep`, `experiment_runs`). The writer turns an SDK
artifact into such a case **mechanically**, so every artifact the SDK can describe can be put in
front of AEBench without hand-authoring a case. The writer drafts; a human (the case author)
refines. Everything the writer cannot decide is listed for that human (§9).

Example. The Benford example artifact ([`examples/benford-e2e/artifact/`](../../examples/benford-e2e/artifact/))
is a `spec-artifact`: it ships specs instead of code, a download recipe instead of data, and
reference outputs. The writer produces a case whose task tells the agent to implement the specs,
fetch and verify the World Bank population CSV, and run the experiments. The oracle then checks
that the data hash matches, the specified unit tests pass, and the regenerated numbers (row
counts, digit counts, MAD and chi-square values) equal the reference outputs. The output is in
[`examples/benford-e2e/aebench-case/`](../../examples/benford-e2e/aebench-case/).

## 1. Inputs and options

| Input | Required | Meaning |
|-------|----------|---------|
| Artifact | yes | Read through the Artifact Reader. Reader warnings are carried into §9. |
| `case_id` | yes | AEBench case id, e.g. `uas_benford_population`. AEBench's convention is `<venue><yy>_<name>`; artifacts without a venue use the prefix `uas_`. |
| `paper_url` | yes | Absolute `https` URL of the paper (AEBench requires `[paper] url` and `sha256`). The writer computes `sha256` over the artifact's paper of record (Reader §8 `paper.of_record`), whatever its format, and records the URL as given without fetching it, so the URL must serve exactly those bytes; point
it at the paper of record at a pinned commit (for example a raw-file URL). If no paper of record resolves to a file, the writer writes no case and says so in `WRITER-REPORT.md`. |
| `upstream` | no | Where AEBench fetches the artifact instead of the bundled task view (§3): `git` (`url`, full commit `ref`, optional `subdir` when the artifact is a subdirectory of the repository) or `archive` (`url` or `path`). Default: none (the task view ships in the bundle). |
| `timeout_ms` | no | Agent time budget. Default: 4 hours (`14400000`), AEBench's recommendation. |
| `float_tolerance` | no | Default relative tolerance for non-integer numbers (§6). Default `1e-9`. |

The writer never writes inside the artifact (Reader §7.2).

## 2. Applicability

| Artifact kind (Reader §6) | Writer output |
|---------------------------|---------------|
| `full-artifact` | Case: run the shipped code. |
| `spec-artifact` | Case: implement the specs, then run. |
| `paper+evidence` | **No case.** `WRITER-REPORT.md` states that the artifact has nothing to execute. AEBench scores execution; such artifacts are evaluated by the judge and reviewer. |
| `paper-only` | **No case**, as above. |

An experiment whose `disposition.status` is not `active` (SPEC §2.2.2) is excluded. If no active
experiment remains, the result is "no case" with that reason.

## 3. Task view

The agent must reproduce the results, not copy them. The **task view** is the artifact minus the
files that hold the answers:

- **Withheld:** every file that is the resolved `evidence` of a result the oracle compares (§6),
  and any file under a directory whose every file is withheld.
- **Kept:** everything else, including the paper, specs, `claims.yml`, `results.yml`, and
  `datasets.yml`. The paper still reports the numbers; §7.4 explains why the oracle re-executes
  rather than trusting outputs left in the workspace.

Without an `upstream`, the writer copies the task view into the case's `artifact/` directory
(AEBench `artifact_mode = "local"`). With an `upstream`, AEBench fetches the whole artifact, so the
withheld files **are** in the agent's workspace; `artifact/` then holds only `AEBENCH_TASK.md`, laid
over the fetched artifact (AEBench `artifact_mode = "overlay"`, `overlay_artifact = true`), and the
oracle's re-execution (§7.4) is what keeps copied answers from passing. In both cases the writer
lists the withheld paths in `withheld.txt` (one artifact-relative path per line; lines starting with
`#` are comments). An AEBench option to exclude paths from a fetched upstream would close this gap. Copying is acceptable here because the task
view excludes large data by construction: data are `external` datasets fetched by the agent
(Reader §7.2). AEBench itself always works on its own copy, since the agent writes into it.

The writer adds one file to the task view: `AEBENCH_TASK.md`, the generated instructions (§5).

## 4. `case.toml`

| `case.toml` key | Value |
|-----------------|-------|
| `id`, `run.id` | `case_id` |
| `case_brief.core_claim` | The artifact `title`, then "Reproduce claims" and the IDs of the claims whose results the oracle compares (when none is compared: "Re-execute the experiments; no result is compared automatically."), e.g. `"First- and second-digit Benford conformity of World Bank population figures. Reproduce claims C1, C3, C4, C5, C6, C7, C8."` |
| `case_brief.acceptable_evidence` | One sentence per compared result: `"<result id> (<claim ids>): <output_path> matches the reference within tolerance."` |
| `case_brief.allowed_tolerance` | The tolerance rules of §6 in one sentence, e.g. `"Integers, booleans, and hashes exact; other numbers within relative 1e-9."` |
| `run.instructions.path` | `AEBENCH_TASK.md`, or `<subdir>/AEBENCH_TASK.md` for a `git` upstream with `subdir` (the overlay then places the file at that path) |
| `run.instructions.required_evidence` | One line per compared result: `"Leave <output_path> as written by <run.command>."`, then `"Leave the implementation and its tests in place; the oracle re-runs them."` |
| `run.runtime` | `mode = "docker"`, `image = "aebench-agent:latest"`, `timeout_ms`, `gpu` = `true` iff any environment declares a GPU in `hardware`, `interactive = false` |
| `run.artifact_requirements` | `docker = false`, `compose = false` (SDK experiments run inside the agent's container) |
| `run.prompt.profile` | `artifact-eval-v1` |
| `oracle` | `expected_score = 4`, `placeholder = false`; every `phase_targets` entry `"local"` |
| `upstream` | No `upstream` option: `artifact_mode = "local"`. Otherwise `source_type` and `url`/`ref`/`path` from the option, `artifact_mode = "overlay"`, `overlay_artifact = true`, and `notes = "artifact subdirectory: <subdir>"` when `subdir` is given (AEBench's `[upstream]` table accepts no other keys). |
| `paper` | `url` = `paper_url`; `sha256` of the paper of record; `title` = artifact `title` |

## 5. Generated task instructions (`AEBENCH_TASK.md`)

A Markdown file with these sections, in order, generated from the read model. Text in quotes is
fixed wording; the rest is filled from the artifact.

1. **Goal.** "Reproduce the results of this research artifact." The artifact title and the
   compared claims' statements, one per line with their IDs.
2. **What you are given.** For a `spec-artifact`: "This artifact contains no code. Each experiment
   lists a specification that defines exactly what its code must do. Implement each specification
   at the paths it names." For a `full-artifact`: "Run the shipped code as each experiment
   declares." Then the paper path.
3. **Data.** For each dataset used by an included experiment: its `id`, `uri`, `sha256`, `access`,
   `license`, and the path to place it at (the experiment's `uses_data[].at`, else
   `data/<last segment of uri>`); a dataset used at several paths lists every placement. "Verify the SHA-256 before use. Do not commit downloaded data to
   the artifact's history." Datasets with `access` other than `public` are listed with "Obtain
   access as described in `datasets.yml`; if you cannot, report it and continue."
4. **Experiments.** In dependency order (`depends_on`; ties by declaration order): slug, spec
   path (spec-artifact), `run.entrypoint`, `implementation.check` if any, and `run.command`.
5. **Outputs to leave.** The `required_evidence` lines of §4.
6. **Rules.** "Do not write into `reference-outputs/` or any of these withheld paths: …" followed
   by the withheld paths of §3, one per line (the agent cannot see the case's `withheld.txt`).
   Then: "Do not hard-code results taken from the paper; the oracle re-runs your code and compares
   what it produces."

## 6. Reference values

A result belongs to an included experiment when its `produced_by` names one; a result without
`produced_by` belongs to all of them. A result whose `produced_by` names an excluded or unknown
experiment is not compared. When IDs or slugs repeat, the first record wins. A result whose evidence
yields no kept value (§6.2) is not compared and its evidence is not withheld. For each such result, the writer extracts **reference values** when all of
these hold: the result's `evidence` resolves; its extension is `.json` or `.csv`; and its
`output_path` (§6.1) is set. Otherwise the result is listed in §9 as "not compared
automatically".

### 6.1 `output_path`

`output_path` is an optional result field: the workspace-relative path where running the
experiment writes this result's evidence. `evidence` is the shipped reference copy. When
`output_path` is absent and the artifact kind is `full-artifact`, the writer uses `evidence`
itself; for a `spec-artifact` it does not guess.

### 6.2 Extraction

- **JSON.** Every leaf reached from the root through objects and arrays, keyed by its JSON Pointer
  (RFC 6901), e.g. `/first_digit/mad`.
- **CSV.** The header row names the columns; each later row is keyed by its first column's value,
  which is a key, not a compared value; every other cell is keyed `<first-column value>/<column
  name>`, e.g. `3/observed_count`. When two rows share a first-column value, the first wins. A cell
  that parses as a number is a number; otherwise a string.

Kept leaves: numbers, booleans, and strings that are 32–128 lowercase hex digits (hashes). Dropped
leaves: other strings, `null`, and any leaf whose key contains `path`, `dir`, `file`, `time`,
`date`, `host`, `user`, `version`, `duration`, `elapsed`, or `seconds` (case-insensitive) — values that legitimately
differ between environments. The match is a case-insensitive substring test on the whole key
(so `/dir_count` is dropped too). Also dropped: every key that matches a pattern in the result's
`volatile` list (SPEC §2.3), which records what the artifact's author knows does not reproduce byte
for byte. A `volatile` that is not a list of strings is ignored with the reader's `RD-FIELD-TYPE`
warning. Dropped keys are listed in §9, each with its reason (name rule or `volatile`), so the case
author can restore any that matter.

### 6.3 Tolerances

| Value | Rule |
|-------|------|
| Boolean, hash string, integer (a JSON integer, or a CSV cell without `.`/`e`) | Exact. |
| Other number | `abs(observed - reference) <= float_tolerance * max(1, abs(reference))`. |

A claim validator of kind `builtin` named `numeric_close` (SPEC §3.2) whose `input.result` is a
compared result overrides the float rule for that result's float values with its
`params.rel_tol` and `params.abs_tol`: `abs(observed - reference) <= max(rel_tol * abs(reference),
abs_tol)` (an absent one is 0). Reference values are written to `refs/reference-values.json`:

```json
{"R3": {"output_path": "results/summary.json",
        "values": {"/first_digit/mad": {"value": 0.00412, "rule": "float", "tolerance": 1e-9},
                   "/first_digit/n": {"value": 17195, "rule": "exact"}}}}
```

## 7. Oracle phases

The writer emits `oracles/common.py` and one module per phase, using AEBench's
`CaseOracle*Base` classes and checks. Every check name starts with the SDK object it comes from
(`dataset:`, `experiment:`, `result:`), so a failed check points back to the artifact. Artifact-relative
paths in checks (entrypoints, dataset placements, `output_path`, `run.working_dir`, the scratch
root) are taken relative to the artifact's location in the workspace: the workspace root, or
`<subdir>` for a `git` upstream with `subdir`.

### 7.1 `env_setup`

- `env:python3_version` — `python3` version ≥ 3.10 (AEBench's floor).
- For each environment (SPEC §2.5) with a pinned image digest: an **optional** check that notes
  the digest; AEBench runs in its own image, so a mismatch does not fail the phase.
- `instructions:AEBENCH_TASK.md` — the instructions file exists in the workspace.

Checks that come from no SDK object use the prefixes `env:` and `instructions:`; environment digest
notes use `environment:<name>:image_digest`.

### 7.2 `artifact_build`

For each included experiment:

- `experiment:<slug>:entrypoint` — `run.entrypoint` exists (when declared);
- `experiment:<slug>:check` — `implementation.check` exits 0 within 600 s when run from the
  workspace root (when declared). This is where a `spec-artifact`'s specified unit tests run.

`implementation.check` is an optional experiment field: a command that exits 0 if and only if the
implementation is in place and its specified tests pass.

### 7.3 `benchmark_prep`

For each `external` dataset used by an included experiment: `dataset:<id>` — the file at the
placement path of §5 item 3 exists and its SHA-256 equals `location.sha256`. One check per dataset
covers **every** placement; it fails if any placement is missing or differs. A dataset without a
`sha256` gets an existence check only, listed in §9.

### 7.4 `experiment_runs`

The oracle **re-executes** before comparing, so that numbers copied from the paper cannot pass:

1. Copy the workspace to a scratch directory, excluding every `output_path` of a compared result
   and every withheld path (§3).
2. In dependency order, run each included experiment's `run.command` in the scratch copy, from
   `run.working_dir` when declared, else the scratch root, with the experiment's `run.env`. A non-zero exit fails `experiment:<slug>:run`.
3. For each compared result, `result:<id>` reads `output_path` (relative to the scratch root) in
   the scratch directory, extracts
   values as in §6.2, and compares each reference value under its rule. Missing keys fail; extra
   keys are ignored. The failure message lists up to 10 mismatches as
   `<key>: observed <x>, reference <y>`.

An experiment whose `expected_runtime` exceeds the remaining oracle budget (reference value: one
hour) is not re-executed; its `experiment:<slug>:run` check passes with the message
"not re-executed: expected_runtime exceeds budget". Runs share the one-hour budget: each run's
timeout is the budget remaining when it starts, and once the budget is spent the remaining runs
fail. `expected_runtime` is a number of seconds or a string `<number><unit>`
with unit `s`, `m`, `h`, or `d`; an unparsable value counts as fitting the budget. A skipped
experiment's results are compared on the files the agent left, and §9 records
the weaker guarantee.

The phase passes when every `experiment:*:run` and `result:*` check passes. AEBench's
`phase_count` score therefore gives 4 only when every compared result reproduces. AEBench's
oracle report keeps only phase-level status, so every generated check also appends one JSON line
`{phase, check, ok, message}` to `aebench-writer-checks.jsonl` in the oracle output directory.

## 8. Evaluation record

After the AEBench run, the runner (or a post-step) writes `evaluation-record.yml` (Reader §7.3) in
the run's output directory with `evaluator.type: aebench`, `config: {case, agent, model}`,
`outcome: {score, expected_score, results_passed, results_compared}`, and the artifact's content
digest. The writer emits `evaluation-record.template.yml` with the `artifact` block already filled,
so the record refers to the exact artifact bytes the case was built from.

## 9. Left to the case author

The writer writes `WRITER-NOTES.md` listing, in this order:

1. Reader warnings (Reader §4), verbatim.
2. Results not compared automatically, with the reason (non-JSON/CSV evidence, no `output_path`,
   unresolved evidence), and their claims' validator `instructions` or `success_criteria` so the
   author can write a check by hand.
3. Dropped keys per result (§6.2).
4. Datasets without `sha256`, non-public datasets, experiments not re-executed (§7.4).
5. Claims with no compared result.

The case author refines tolerances, adds hand-written checks, and removes this file when done.

## 10. Bundle layout

```text
<case_id>/
├── case.toml
├── artifact/                       # task view (§3), unless an upstream is used
│   └── AEBENCH_TASK.md             # §5
├── refs/
│   ├── reference-values.json       # §6
│   └── datasets.json               # {"_generated", "datasets": [{id, path, sha256}]} for §7.3
├── oracles/
│   ├── common.py                   # extraction and comparison helpers (§6.2, §6.3)
│   ├── env_setup.py
│   ├── artifact_build.py
│   ├── benchmark_prep.py
│   └── experiment_runs.py
├── withheld.txt                    # §3, always written
├── evaluation-record.template.yml  # §8
└── WRITER-NOTES.md                 # §9
```

Every generated file carries the marker "Generated by aebench-writer/v1 from `<artifact id>`
(`<content digest>`)": as a comment in TOML, Python, YAML, and `withheld.txt`; as an HTML comment
on the first line of Markdown; and as a top-level `"_generated"` key in JSON, so
`refs/datasets.json` is `{"_generated": …, "datasets": [{id, path, sha256}]}`.

## 11. Conformance

Using the Artifact Reader base fixture (Reader §9) with `out/r1.json` = `{"n": 10, "mad": 0.5,
"ok": true, "path": "/tmp/x"}` and `R1.output_path: out/r1.json`:

| ID | Input | Expected |
|----|-------|----------|
| W1 | Base fixture | Case written. `refs/reference-values.json` has `R1` with `/n` exact 10, `/mad` float 0.5, `/ok` exact true; `/path` dropped and listed in `WRITER-NOTES.md`. `withheld.txt` lists `out/r1.json`; `artifact/out/r1.json` absent. |
| W2 | W1's case, workspace where `run.py` writes `{"n": 10, "mad": 0.5000000001, "ok": true}` | `experiment_runs` passes. |
| W3 | As W2 with `"n": 11` | `result:R1` fails with `/n: observed 11, reference 10`. |
| W4 | As W2, but `run.py` only copies a pre-made `out/r1.json` that the scratch copy lacks | `experiment:e1:run` or `result:R1` fails. |
| W5 | Reader RD15 (spec-artifact) without `output_path` | Case written; `R1` listed as not compared; `experiment_runs` has no `result:` checks. |
| W6 | Reader RD4 (`paper+evidence`) | No case; `WRITER-REPORT.md` gives the reason. |
| W7 | Base fixture plus an `external` dataset with `sha256` used by `e1` at `data/x.csv` | `benchmark_prep` has `dataset:<id>` checking `data/x.csv` against the hash. |
| W8 | Any | The artifact's bytes are unchanged; every generated file has the marker. |
| W9 | Base fixture with `out/r1.json` = `{"n": 10, "steps": [{"elapsed_s": 1.5, "rows": 7}], "fig": {"sha256": "<64 hex>", "bytes": 120}}` and `R1.volatile: ["/fig/*"]` | `R1` compares `/n` and `/steps/0/rows` only. `WRITER-NOTES.md` lists `/steps/0/elapsed_s` (name rule) and `/fig/sha256`, `/fig/bytes` (`volatile`). |
