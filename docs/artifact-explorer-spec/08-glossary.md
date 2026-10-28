> **Audience**: Readers of this specification.
> **Source of truth for**: Terms specific to the explorer. Terms of the artifact format are
> defined in the SDK specification; terms of runs, findings, and verdicts in JR §9.2.

# 8. Glossary

| Term | Meaning |
|------|---------|
| **Artifact** | A directory in the `evaluable-artifact/v3` (or `/v2`) on-disk shape (SDK §5; JR §2.3.1). |
| **Asset reference** | `null` or `{path, url, kind}` naming an input file copied into the site (§3.1). |
| **Attribution** | The label naming the tool or role that produced a value the authors did not write (§5.6). |
| **Build warning** | A human-readable note in `data.json.warnings` about input the explorer could not use; never a judgment of the work (§3.2). |
| **Data document** | `data.json`, the `artifact-explorer/data/v1` object that is the contract between builder and viewer (§3). |
| **Declared link** | A claim listed in a contribution's `supporting_claims` (SDK §2.4.2). |
| **Display title** | The title shown in the site header: the paper source's title, else the PDF metadata title (labeled as such), else the manifest title, else the ID; its origin is recorded in `display_title_source` (§3.3). |
| **Judge-only run** | A sealed `artifact-informed` run in which every reviewer stage is `not-requested` (JR §1.2, §6.4); shown with a judge overlay and no review (§4.3). |
| **Page unknown** | A claim or figure page that is missing, not an integer, or less than 1; recorded as `null` and never rendered as a page number (§3.4). |
| **Explorer** | A tool conforming to this specification: builder, viewer, or both. |
| **Inferred link** | A claim listed in a contribution's `inferred_supporting_claims`, attributed through `provenance.claim_link_sources` (§3.5.1). |
| **Join** | A navigational cross-reference between a finding and a claim, result, contribution, or other finding, computed only from identifiers the run records (§4.4). |
| **Mode A / B / C** | Artifact only; sealed run; unsealed preview (§1.2). |
| **Overlay** | The `evaluation` block: a run's analysis, read verbatim and joined to the artifact (§4). |
| **Paper adapter** | A tool that turns a bare paper into a paper-origin artifact (JR §3). Its suggestions are labeled as such. |
| **Probe** | A fixed, ordered list of conventional file names tried when the artifact declares no file for a role (§2.6). |
| **Run gate** | JR §6.7 consumer validation, applied before anything in a run is read (§2.4). |
| **Sealed run** | A run directory whose `manifest.json` passes JR §6.7. |
| **Site** | The output directory: `index.html`, `data.json`, `assets/`, `run/`, and application files (§5.2). |
| **Unresolved** | A declared path or ID that does not resolve safely; shown as declared text, never as a failure of the work (§2.5). |
| **Viewer** | The client-side application that renders a data document (§5). |
