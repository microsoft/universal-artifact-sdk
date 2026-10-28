> **Audience**: Builders of research-artifact viewers; security reviewers.
> **Source of truth for**: How the explorer handles untrusted artifacts and runs.

# 6. Security

Artifacts and runs are **untrusted**: they may come from anyone, and parts of them may be
produced by language models. A site built from them may be hosted on a shared domain. The
explorer therefore treats every input byte as data, never as code or as an instruction.

## 6.1 Path containment (build time)

- Every declared path passes §2.5 before it is opened. Containment is checked on the resolved
  path, and any path that is or traverses a symbolic link is rejected, so a link inside the
  artifact cannot make the explorer read or copy a file outside it.
- Only regular files are read or copied. Devices, sockets, FIFOs, and directories named as files
  are unresolved.
- Copy destinations are computed from the **validated relative path** under `assets/` or `run/`;
  the explorer never writes outside the output directory, whatever the input path contains.
- The output directory MUST NOT equal, contain, or lie inside an input (I1). The explorer MUST
  NOT follow a symbolic link at or inside the output directory when writing.
- Input size limits (per-file and total) are *reference values (non-normative)*; when a limit is
  hit the file is unresolved with a warning, never truncated silently.

## 6.2 Content sanitization (view time)

- All text from the inputs — statements, captions, finding summaries, YAML values, file names —
  is inserted as text, never as HTML.
- Markdown (README, reflection, drafts, Markdown evidence) is converted to HTML and then
  sanitized with an allow-list: no `<script>`, `<style>`, `<iframe>`, `<object>`, `<embed>`,
  `<form>`, or event-handler attributes; no `javascript:`, `vbscript:`, or `data:` URLs except
  `data:` images; no remote `src`. Raw HTML in Markdown is not interpreted: it is rendered as
  literal text (§3.1).
- SVG files are displayed only through `<img>` (which does not execute scripts), never inlined.
- Links to copied files use relative URLs. Every other link is an external link (§6.3).
- The site SHOULD ship a restrictive Content Security Policy (for example via a `<meta>` element)
  that allows scripts and styles only from the site itself and forbids network connections other
  than same-origin reads of the site's files.

## 6.3 No network

- The build makes no network request: no reference resolution, DOI lookup, model call, package
  download, or URL fetch. Values that would need one (reference checks, external dataset sizes)
  come only from the run or are absent.
- The site makes no network request beyond reading its own files. **External links** — `http:`,
  `https:`, and `mailto:` URLs in the inputs (dataset `uri`, reference `url`, DOIs written as
  `https://doi.org/…`, Markdown links) — are rendered as hyperlinks whose full target is visible
  beside the link text, carry `rel="noopener noreferrer"`, and are followed only when the reader
  clicks them. A URL with any other scheme is shown as text. Nothing external is ever loaded
  automatically (no remote images, frames, prefetch, or analytics).

## 6.4 Integrity

- In mode B, every run file the site shows has been hash-checked against the seal (§4.6), and
  the site shows the run's `input_digest` so a reader can tie what they see to a specific sealed
  run.
- The explorer does not verify the artifact's own `SHA256SUMS`; an implementation MAY show its
  presence. Integrity judgments belong to the judge (JR §4).
- The site never presents unsealed content (mode C) without the banner of §5.5.
