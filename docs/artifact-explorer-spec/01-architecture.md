> **Audience**: Builders of research-artifact viewers.
> **Source of truth for**: The explorer's pipeline, build modes, and global invariants.

# 1. Architecture and invariants

## 1.1 Pipeline

```text
 artifact dir ─┐                                      ┌─ data.json        (§3, §4)
               ├─▶ gate (§2) ─▶ assemble (§3) ─▶ emit ┼─ assets/…         (artifact files, §5.2)
 sealed run ───┘        └──── run overlay (§4) ───┘    ├─ run/…            (run files, §4.6)
                                                       └─ index.html + app (§5)
```

1. **Gate.** Check the inputs (§2): the artifact format gate, and, when a run is given, the run
   gate (JR §6.7 consumer validation). A failed gate produces no site.
2. **Assemble.** Read the artifact into the data document `artifact-explorer/data/v1` (§3). Every
   value is either copied from an input, derived by a rule in §3, or `null`/empty.
3. **Overlay.** If a run was given, read it into the `evaluation` block and attach per-claim and
   per-contribution cross-references (§4). The core of the document (§3) does not depend on it.
4. **Emit.** Write `data.json`, copy every referenced input file into the output, and write the
   viewer application (§5). The application reads only `data.json` and the copied files.

The data document is the **contract** between the builder and the viewer. Builder and viewer may
be built independently; a viewer conforms if it renders any valid data document as §5 requires.

## 1.2 Build modes

| Mode | Inputs | Artifact read from | `evaluation` |
|------|--------|--------------------|--------------|
| **A. Artifact** | an artifact directory | that directory | `null` |
| **B. Sealed run** | a sealed run directory | the run's `snapshot/artifact/` (artifact-informed scope), or a synthetic paper-only artifact (§2.4.2) | the run (§4) |
| **C. Unsealed preview** (OPTIONAL) | an artifact directory and an unsealed outputs directory, with an explicit opt-in flag | the artifact directory | the outputs, marked `sealed: false` (§4.7) |

Supplying both an artifact directory and a sealed run is a usage error (§2.1): in mode B the run's
own snapshot is the artifact, so a second artifact could disagree with what was reviewed.

A conforming command-line tool exposes at least `build <artifact> --out <dir>` (mode A) and
`build --run <run-dir> --out <dir>` (mode B). Option names are *reference values
(non-normative)*; behavior is normative.

## 1.3 Output

The output directory holds only files written by this build (a clean build MAY first remove it
when the caller explicitly asks). Its layout is in §5.2. The site is complete without the inputs:
after the build, the inputs may be deleted and the site still renders everything it shows.

## 1.4 Global invariants

| ID | Invariant |
|----|-----------|
| I1 | **Inputs are read-only.** The explorer never creates, modifies, or deletes anything under the artifact directory or the run directory. The output directory MUST NOT equal, contain, or lie inside either input. |
| I2 | **No evaluation.** The explorer computes no verdict, mode verdict, rubric, badge, score, recommendation, confidence, or qualification. Every such value it shows is copied verbatim from a run, with its source. |
| I3 | **Absence is not a negative.** A missing optional file, empty list, or `null` field is rendered as "not provided" (or a section-specific equivalent), never as a failure, a zero, or a missing contribution. |
| I4 | **Attribution.** Every value that did not come from the artifact's authors — a judge finding, a reviewer finding, a link inferred by a tool, a paper-adapter extraction — is shown with the tool or role that produced it (§4.5, §5.6). Inferred links are never presented as declared. |
| I5 | **Determinism.** The same inputs and options give a byte-identical `data.json` apart from `generated_at`, and the same set of copied files with identical bytes. Ordering never depends on file-system enumeration order or hash-map iteration order. |
| I6 | **Static and offline.** Neither the build nor the site makes a network request. Every URL in the data document and site is relative to the site root. The site works when served by any static HTTP server. |
| I7 | **Containment.** Only regular files inside an input root are read or copied, through the path rules of §6.1. |
| I8 | **Human-owned values stay unset.** Recommendation, scores, confidence, and contribution qualification are shown exactly as the run has them, which for a conforming run is "unset" (JR §6.5, I4 there). The explorer offers no control that sets them. |
| I9 | **Fail closed on runs.** A run that fails JR §6.7 consumer validation produces no site (mode B). The explorer never "repairs" or partially renders an invalid sealed run. |
| I10 | **Neutrality.** No behavior depends on the venue, field, model vendor, or artifact producer, except as recorded in the inputs and displayed verbatim. |

## 1.5 Versioning

The data document carries `"schema": "artifact-explorer/data/v1"`. Adding an optional key is a
minor change within v1; viewers MUST ignore unknown keys. Removing a key, changing a type, or
changing a key's meaning requires `data/v2`. A viewer given a document with an unknown major
`schema` MUST show an error instead of rendering.
