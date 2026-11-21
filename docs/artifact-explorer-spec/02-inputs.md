> **Audience**: Builders of research-artifact viewers.
> **Source of truth for**: What the explorer accepts, how it gates inputs, and how it locates
> files inside them.

# 2. Inputs

## 2.1 Accepted inputs and usage errors

| Input | Required | Notes |
|-------|----------|-------|
| Artifact directory | Mode A, C | An `evaluable-artifact/v3` or `/v2` directory in the on-disk shape of JR §2.3.1 |
| Sealed run directory | Mode B | A run directory `<base>/runs/<run-id>/` as defined in JR §6.1–§6.3 |
| Unsealed outputs directory | Mode C only | §2.7 |
| Publication-approval record | no (OPTIONAL feature, §4.8) | a file, named explicitly; modes B and C only (naming one in mode A is a usage error) |
| Separate reference-check result | no (OPTIONAL feature, §4.9) | a file, named explicitly |
| Output directory | always | Where the site is written (§5.2) |

The explorer MUST be given every input path explicitly. It MUST NOT discover "the latest run", a
run inside the artifact, or an artifact next to a run (JR §6.8).

Usage errors, detected before anything is written:

- no input, or both an artifact directory and a sealed run (§1.2);
- an output directory that equals, contains, or lies inside an input directory (I1);
- an input path that does not exist or is not a directory;
- a named input file (publication-approval record, separate reference-check result) that does
  not exist or is not a regular file; a file that exists but is rejected by §4.8 or §4.9 is a
  build warning, not a usage error;
- a publication-approval record in mode A (§4.8 needs a run);
- an output path that is, or lies under, a symbolic link: once the path is made absolute, no
  component of it, from the root down, may be a symbolic link (§6.1);
- in mode C, an outputs directory that equals or lies inside the artifact directory (the
  artifact would then contain the analysis of itself; the reverse, an outputs directory that
  contains the artifact directory, is allowed);
- an output directory that exists and is not empty, unless the caller passes an explicit option
  to replace it (the tool then replaces it only after a successful build, per exit `3` below).
  An existing empty directory is used as is.

Exit statuses of a conforming command-line tool:

| Code | Meaning |
|------|---------|
| `0` | Site written. Build warnings (§3.2) do not change the code. |
| `2` | Usage error, format-gate rejection (§2.2), run-gate rejection (§2.4), or a hash mismatch found while reading or copying a run file (§4.6). The output directory MUST be left exactly as it was before the build (absent, empty, or with its previous content): a rejection found after writing has begun is handled by writing to a staging directory and renaming on success, or by undoing every write. |
| `3` | Unexpected failure while building. The output directory may hold a partial site; the tool SHOULD write to a sibling temporary directory and rename on success so that it does not. |

## 2.2 Format gate

The explorer applies JR §2.2 rule 1 unchanged: it reads the artifact through the
[Artifact Reader](../artifact-reader-spec/README.md), reads `evaluable-artifact/v3` and
`evaluable-artifact/v2` natively, and reads any other or missing `format_version`, and a missing
or unparsable `manifest.yml`, with the reader's repairs, adding each reader warning as a build
warning (§3.2). Only a reader rejection (Reader §5) is a gate rejection (exit `2`).

- `sdk_version` is copied into `identity` (§3.3) and MUST NOT change behavior (JR §2.2 rule 2).
- `producer`, `origin`, and other producer extensions are opaque: copied for display, never
  interpreted, except `origin.kind` and `origin.evidence_cap`, which only the paper-origin banner
  of §5.5 uses. Every other `origin` key is shown verbatim on Provenance (§5.4.5).
- A v2 artifact has no contributions; `contributions` is `[]` and the Contributions section
  says that no declaration was provided (I3).

## 2.3 Reading the artifact

The explorer reads the artifact in the on-disk shape of **JR §2.3.1**, including its index
location rule (`paths.<name>`, else the default file name), its top-level-key rule, the
contributions-only-through-`paths.contributions` rule (SDK §5.2), the references-export
exception, and the research-agent metadata rule. A `paths.<name>` whose value is `null` counts as
not declared (JR §3.2 allows `null` for an index with no entries); a value that is neither a
string nor `null` also counts as not declared and adds a warning. It reads these files beyond
the JR §2.3 table:

| File | Located by | Shape | Used for |
|------|------------|-------|----------|
| Figures index | `paths.figures` (no default) | top-level `figures`: list of `{id, number?, path, caption?, page?, claims?}` (JR §3.6.1) | §3.11 figures; `claims` links are labeled as paper-adapter suggestions |
| Exhibits index | `paths.exhibits`, else `exhibits.yml` | SDK §2.3.1 | §3.8 |
| README | probe (§2.6) | Markdown or text | §3.13 |

**Malformed content is reported, not fatal.** When an index other than `manifest.yml` is
declared but missing, or is read (because it is declared or exists at its default file name)
and fails path safety (§2.5), does not parse, or lacks its top-level list, the explorer uses an
empty list and adds a build warning (§3.2) naming the file. An index that is
**not declared** and absent at its default file name is simply empty, with no warning: absence
is not a defect (I3). A list element that is not a
mapping is skipped with a warning. Contribution loading additionally produces the contribution
diagnostics of the JR §2.3.1 contributions table; §3.5 says which list the site shows.

**Duplicate IDs.** When two records of one collection share an `id` (or an experiment `slug`),
both are kept in declaration order and a warning names the duplicate. Every lookup by that ID —
cross-references, joins (§4.4), and routes (§5.3) — resolves to the **first** record. Derived
cross-reference lists (§3) are filled on the first record only; a later duplicate keeps its
copied fields and has empty derived lists.

Unknown fields on any record are preserved in the data document (§3.1) and never interpreted.
YAML values are projected into JSON by the rule in §3.1.

**YAML reading.** Every YAML file is read as UTF-8 (a leading byte-order mark is ignored) under
the YAML 1.2 core schema, as the SDK bindings read it (SDK §5): `yes`, `no`, `on`, `off`,
dates, and timestamps are strings, never booleans or date values. A mapping that repeats a key is
a parse error. A `manifest.yml` that is not valid UTF-8 or does not parse is read as absent
(Reader §3.1 case C, a build warning); any other index that is not valid UTF-8 or does not parse is a malformed index
(a build warning, above).

## 2.4 Run gate (mode B)

1. The explorer MUST run JR §6.7 **consumer validation** on the run directory before reading
   anything else in it. Any failure is a run-gate rejection (exit `2`) whose message lists every
   failed rule. There is no flag to bypass it (I9). JR §6.3 fixes key order and separators for
   the `input_digest` serialization but not how non-ASCII characters are written; until it
   does, the explorer accepts the digest when it matches either the serialization with non-ASCII
   characters written literally (UTF-8) or the one with each of them escaped as `\uXXXX`
   (lower-case hex digits, UTF-16 surrogate pairs above U+FFFF). For ASCII-only paths the two
   coincide.
2. The run is then read **only** through files listed in the manifest's `inputs` (under
   `snapshot/`) and `outputs`. A file present in the directory but not listed is never read.
3. **Artifact-informed scope** (`scope: artifact-informed`): the artifact is
   `snapshot/artifact/`. It passes the format gate (§2.2) like any artifact; a rejection there is
   a run-gate rejection.
4. **Paper-only scope** (`scope: paper-only`): there is no artifact. The explorer builds the core
   document from an **empty artifact**: `identity.id` and `identity.title` are `null`,
   `identity.origin`, `format_version`, `sdk_version`, and `producer` are `null`, `identity.extra`
   is `{}`, `display_title` follows the chain of §3.3 from the snapshot paper, every collection is
   empty, and `paper` is the manifest's `paper`
   file (§3.10). The overlay (§4) carries everything the run has. The site states that the input
   was a paper without an artifact.
5. **Judge-only runs.** JR §1.2 and §6.4 define a judge-only invocation as an ordinary sealed
   run with scope `artifact-informed` whose `paper_review` stage (and every other reviewer stage)
   is `not-requested`. It is gated and read exactly like any other mode-B run; nothing in this
   specification distinguishes it except how the review part of the overlay is presented (§4.3).
   The explorer's test for "judge-only" is the one of §4.1 (`judge_only`).
6. **Unreadable outputs.** A JSON file listed in `outputs` that §4 reads, and that is not valid
   UTF-8 JSON or not a JSON object, is a run-gate rejection (exit `2`) even though its hash
   matches: a sealed run is never rendered with part of its analysis missing (I9). A JSON object
   that lacks the key §4 reads from it, such as the status object `{status, reason}` that JR §6.2
   writes for a stage that did not run, is valid: each key read from it takes its default
   (`null` or `[]`). In mode C a file that does not parse is skipped with a warning (§2.7).

## 2.5 Path safety

Every path read from an input — index pointers, `evidence`, `path`, `directory`,
`location.path`, `sample.path`, `paper.pdf`/`source`, figure `path`, Markdown image targets,
reviewer citation targets — is untrusted. The explorer applies the JR §2.4 rejection rules (absolute,
drive or backslash form, `.`/`..` segments, resolving outside the input root, symbolic link) with
the artifact directory (or run directory, for run files) as the root. A rejected path is
**unresolved**: the data document records `null` for the asset with a build warning, and the
site shows the declared path as text, marked unavailable. A rejected path is never a crash and
never copied. See also §6.1.

**Markdown link and image targets** are URL references, not SDK declarations, so they are first
normalized: a target that has a URI scheme (for example `https:`, `mailto:`) or starts with `/`
or `//` is external and never resolved; otherwise the `?query` and `#fragment` are removed,
the rest is percent-decoded, joined to the directory of the Markdown file, and `.` and `..`
segments are removed as in RFC 3986 §5.2.4. The result must then be a path inside the input root
that passes the rules above (a target that climbs above the root is rejected). So `./fig.png`
and `a/../fig.png` resolve, and `../../etc/x` does not. Declared paths in SDK index files are
**not** normalized: JR §2.4 rejects `.` and `..` segments there.

## 2.6 Discovery probes

The SDK declares most files explicitly; a few conventional files are found by probing fixed names
at the artifact root. Probes are used **only** when the SDK provides no declaration for the same
role, and the first existing regular file in the list wins. The lists are normative, so that two
conforming explorers find the same files.

| Role | Declared by | Probe order when undeclared |
|------|-------------|------------------------------|
| Paper PDF | `paper.pdf` (SDK §2.6) | `paper.pdf`, `main.pdf` |
| Paper source | `paper.source` (SDK §2.6) | `paper.tex`, `paper.md`, `main.tex`, `main.md` |
| README | — (the SDK declares none) | `README.md`, `README.txt`, `readme.md` |
| Reflection | fixed name `reflection.md` (SDK §5) | — |
| Figure images (OPTIONAL, §3.11) | `paths.figures` / `paths.exhibits` | image files at any depth that sit under a directory named `figures`, `figure`, `fig`, `plots`, or `images`, or under a declared experiment `directory`, or whose file name starts with `fig`/`figure` followed by a digit or separator (only when §3.11 item 3 allows it: no figures index is declared, and no exhibits index is declared but missing or unreadable, or lists a figure) |

A declared path that does not resolve, or that resolves to a file that does not parse, is **not**
replaced by a probe: the declaration wins and is
shown as unresolved (§2.5), so a broken declaration stays visible.

## 2.7 Unsealed preview (mode C, OPTIONAL)

Some published examples ship a run's output files without the seal (`manifest.json` and
`snapshot/`), next to a copy of the artifact. An explorer MAY render such a pair if, and only if,
the caller passes an explicit opt-in flag naming the outputs directory. Then:

1. The artifact directory is gated as in mode A.
2. The explorer reads only these files from the outputs directory, each optional:
   `run.json`, `judge.json`, `findings.json`, `contributions.json`,
   `artifact-reconciliation.json`, `review-draft.md`, `paper-review.md`, `reference-check.json`,
   `evidence-packet.json` (read for §4.6.2 only), `visual-coverage.json`, and
   `artifact-visual-coverage.json` (§4.3).
   Each is parsed as JR §6 defines it; a file that does not parse is skipped with a warning.
   This list is closed: no other file in the outputs directory is parsed. The only other files
   mode C touches are those named by `review-output:` citations and by visual-record
   `image_path` values, which are copied (never parsed) under the rule of §4.7.
3. `evaluation.run.sealed` is `false`, and every key of `evaluation.run` is filled by the table
   of §4.7: the manifest-only fields are `null`, and `stages` is
   `run.json.input_provenance.stages` when present, else `{}` (every stage shown as unknown).
4. Every page of the site shows the banner of §5.5: the analysis is unsealed and could have been
   altered after it was produced.
5. Without the opt-in flag, an outputs directory without a valid seal is a run-gate rejection.
