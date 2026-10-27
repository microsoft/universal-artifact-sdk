> **Audience**: Builders of research-artifact evaluation tools.
> **Source of truth for**: The paper adapter, which produces a paper-origin `evaluable-artifact/v3`
> artifact from a bare paper, and its output layout.

# 3. Paper adapter

## 3.1 Purpose

Many papers come with no artifact. The adapter turns a paper into a **paper-origin** artifact so
the same judge and reviewer pipeline can run on it. The adapter MUST be **honest about what a
paper alone can show**: every result it emits is capped at `attested`, meaning "the paper
reports this". It never claims anything was re-executed or re-analyzed.

The adapter is OPTIONAL for conformance (§8). A tool that reviews paper files directly in
`paper-only` scope does not need it.

## 3.2 Inputs and output layout

- **Input:** a paper (PDF or source), plus an optional bibliography file.
- **Output:** a new directory (the caller names it; it MUST NOT exist yet or MUST be empty, except
  that re-running into a directory this adapter produced is allowed, §3.8) containing a valid
  `evaluable-artifact/v3` artifact (§2.2). Because the output is an ordinary artifact, consumers
  read it through §2.3 like any other; nothing below requires an adapter-aware consumer except
  the `origin` block (§3.3).
- **Schema conformance (MUST, no exceptions):** the logical artifact model, that is the manifest
  together with every index it names loaded into the corresponding top-level collection
  (`results`, `claims`, `contributions`, …), validates against the public SDK v3 JSON Schema
  (SDK §5, §8) and passes the SDK's relational rules. Every rule below is chosen so that this
  holds: no required field is ever `null` or absent, and no optional field is written as `null`
  where the schema types it as a string (omit it instead).

**SDK relational rules.** The SDK defines its relational (structural, beyond-schema) rules in
SDK §7 (the *Structural* row of the validation-split table), SDK §8.1 (schema validation
followed by "relational and filesystem invariants": references, cycles, safe paths,
generated/authored collisions, warning policy), SDK §2.4.2 (contribution shape, support,
evidence, and bibliography links), SDK §3.5 (`attest` validator shape), and SDK §5 (safe
relative paths). The adapter's output exercises only this subset, which is what A3 (§8.4)
checks:

| # | Rule (source) | How the adapter output satisfies it |
|---|---------------|-------------------------------------|
| SR1 | Every `Result.validates` entry names a declared claim ID (SDK §7, referential integrity) | links are made only to emitted claims (§3.5) |
| SR2 | `Result.produced_by`, when present, names a declared experiment (SDK §7) | `produced_by` is omitted; `experiments: []` |
| SR3 | A validator is well-formed for its `kind` (SDK §7); an `attest` validator carries `checks` from `provenance`, `integrity`, `ethics`, `citations_exist` and lists its `inputs` (SDK §3.5) | exactly one `{kind: attest, checks: provenance, inputs: [...]}` per claim (§3.5) |
| SR4 | `gated_by` names a validator on the same claim (SDK §7) | one validator `v1`, whose `inputs` name emitted Results; no `gated_by` |
| SR5 | `validation_mode` is a legal enum value (SDK §3.1, §7) | always `attest` |
| SR6 | Every producer-declared path (`evidence`, `paper.*`, `paths.*`) is a safe relative path that does not collide with a generated file (SDK §5, §7) | `paper.pdf` and the fixed index names of the layout below |
| SR7 | Contribution IDs are unique; `supporting_claims` name declared claims; no `established`/qualification field; locator offsets are non-negative with `char_end ≥ char_start` (SDK §2.4.2) | §3.6.4 |
| SR8 | Bibliography identities cited by contributions resolve against `paper.references_export` when that export resolves (SDK §2.4.2, §2.6) | contributions cite no references; the export is written only with `paper_references.yml` (§3.6.2) |
| SR9 | The evidence inventory is computed and consistent with the declarations (SDK §5.1) | stated explicitly (below) |

The rules for experiments, datasets, traces, research agents, claim `tested_by`, and disposition
links (SDK §7) are vacuous for this output, because it declares none of those objects.

**Extension fields.** SDK objects are open: unknown fields survive open and write (SDK §2.4.2)
and the v3 schema does not restrict additional properties of a Result or its locators. The
adapter uses SDK fields wherever one exists (`validation_mode: attest` is the Result's evidential
mode, SDK §2.3, §3.1) and writes exactly these **tool extension fields**, which SDK validators
ignore and consumers of this specification read as defined here: `Result.reported_value` (§3.4
step 4) and, inside the paper locator `locators.paper` (an SDK locator, whose content the SDK
leaves open), `quote`, `page`, `section`, `context`, and `token_class` (§3.4). When enrichment
ran (§3.7), the adapter also writes `inferred_supporting_claims` and
`provenance.claim_link_sources` on contributions, and MAY add fields to the claims it proposes.
No other extension field is written. A consumer MUST NOT rely on a field named `mode` on a Result; if an
older producer wrote one, it is ignored.

```text
<out>/
  manifest.yml              # REQUIRED  format_version, paper pointer, paths, evidence inventory, origin
  paper.<ext>               # REQUIRED  byte copy of the input paper (reference name: paper.pdf)
  claims.yml                # if ≥1 claim      top-level key `claims`
  results.yml               # if ≥1 result     top-level key `results`
  contributions.yml         # if ≥1 candidate  top-level key `contributions` (§3.6.4)
  figures.yml + figures/    # if ≥1 figure     top-level key `figures` (§3.6.1)
  paper_references.yml      # if ≥1 reference  top-level key `references` (§3.6.2)
  paper_related_work.yml    # if ≥1 statement  top-level key `related_work` (§3.6.3)
  GENERATION.md             # REQUIRED  human-readable account of how this artifact was produced
  .adapter/state.json       # OPTIONAL  implementation ledger (below)
```

**Manifest.** `format_version: evaluable-artifact/v3`; `sdk_version: artifact-sdk/v1` (always
written; the SDK's language-neutral contract id, SDK §8, not a package release number); `id`
(reference: the first 12 hex digits of the paper's SHA-256; never truncate it further in data);
`title`, a non-empty string, **never `null`**: the detected paper title, or, when none is
detected, the input paper file's name without its final extension (its *stem*, e.g. `paper` for
`paper.pdf`; if that is empty, the `id`); `experiments: []`; the `origin` block (§3.3); the paper pointer (SDK §2.6:
`paper.pdf` or `paper.source` naming the copied paper, and `paper.references_export` when
references were emitted); and `paths`, which names every emitted index **and nothing else**:

| `paths` key | Value when emitted |
|-------------|--------------------|
| `claims` | `claims.yml` |
| `results` | `results.yml` |
| `contributions` | `contributions.yml` (the only way consumers find it, §2.3.1) |
| `figures` | `figures.yml` |
| `paper_related_work` | `paper_related_work.yml` |

An index with no entries is **omitted**: no file and no `paths` key (a `null` value is also
acceptable to consumers). The `evidence_inventory` (SDK §5.1) is stated explicitly, never left
to defaults: `has_runnable_experiments: false`, `has_paper_source: true`,
`has_results`/`result_count`, `has_contributions`/`contribution_count`,
`has_citations_export`, `has_related_work_export`, every other `has_*` `false`, and, when
results exist, `evidence_kinds: [metrics]` (the SDK's Result `kind` vocabulary, SDK §2.3) and
`validation_modes: [attest]`.

**Generated markers.** Every YAML file the adapter writes carries a top-level `_generated`
string naming the adapter and stating that the content is generated and attested, never
reproduced. `GENERATION.md` begins with an equivalent marker line. Consumers ignore
`_generated` (§2.3.1).

**`GENERATION.md`** reports, at minimum: the adapter name/version, the text reader used, the
counts of results, claims, linked claims, contributions, figures, references and related-work
statements, numbers dropped as not result-shaped, whether LLM enrichment ran and its outcome
(§3.7), and the limitations of §3.6.1. Each count is read from the file the run actually wrote,
so `GENERATION.md` is written after every other output file (§3.7). The report also states:

- for claims, their source: `deterministic seed` (§3.5) or the enrichment extractor with its
  model label (§3.7);
- for figures, a status when none was written (§3.6.1);
- for references, `not split (unrecognized format)` when a references section was found but no
  entry could be split from it (§3.6.2);
- for enrichment, the outcome of each stage (§3.7).

**Ledger (optional, implementation-only).** An implementation MAY keep a ledger such as
`.adapter/state.json` recording `origin`, the paper id, the extractor stamp, the options that
shaped the output (§3.8), and `generated_files: {relative path → sha256}` for every file it
wrote. Consumers MUST NOT require
it. If present it is used only for §3.8. The adapter does not write `SHA256SUMS` or
`exhibits.yml`; a consumer that needs integrity data uses its own snapshot hashes (§2.5).

## 3.3 Origin block

The manifest MUST include an origin block so consumers can tell this artifact apart from one a
producer emitted:

```yaml
origin:
  kind: paper                     # paper-origin artifact
  evidence_cap: attested          # the strongest verdict any result here can earn
  extractor:
    tool: "<adapter name>/<version>"
    reader: "<text reader>"       # which PDF/source text reader produced the text
    llm: null                     # or an opaque label for the enrichment model, if §3.7 ran
    verifier: null                # or an opaque label for the verifier model, if §3.7 ran
```

`origin` is otherwise opaque to consumers (§2.3.1). The judge MUST respect `evidence_cap`. With
`evidence_cap: attested`, the reproduction tier is unreachable, a requested reproduction yields
`reproduce/deferred` `unassessable` (§4.5.6), and the rubric can be at most `PARTIAL`.

## 3.4 Result harvesting (deterministic)

The adapter extracts **result-shaped numbers** from the text source (§2.3.2). This subsection
is the reference rule. Harvest counts depend on the text reader and legitimately differ between
implementations, so conformance (§8.4) asserts only robust properties: no bare integers, no
duplicates under the dedup key, every result linked to its sentence, every result capped.

**0. Page furniture.** When the text source has pages (PDF), remove running headers and footers
from each page's text before anything else. Consider the first three and last three non-blank
lines of every page; normalize each by *collapse*, lowercasing, and replacing every digit run
with `#` (so `Smith et al. 7` and `Smith et al. 8` match). A normalized line that occurs in that
top-or-bottom band on at least 3 pages **and** on at least 30% of the pages (reference values) is
furniture, and every occurrence of it in a band is deleted, as is a band line consisting only of a
page number (`^\s*\d{1,4}\s*$` or `^\s*(page\s+)?\d{1,4}(\s+of\s+\d{1,4})?\s*$`, case-insensitive). Furniture tokens are not
harvested and not counted as dropped. Removal is local to harvesting: it never changes the
extracted text that other stages quote or the offsets of §2.8. A source without pages skips this
step. So a header `Proceedings of the Workshop on Parsing 2021` repeated on every page, or a
footer `Preprint v2.0, under review`, contributes no Result.

**1. Segmentation.** Split the text into sections at heading lines (§2.7); heading lines
themselves are not section text. Within each section's text, rejoin line-break hyphenation by
deleting every `-` that is immediately followed by a line break **together with that line break
and any spaces or tabs that begin the next line** (regular expression `-\r?\n[ \t]*` replaced by
the empty string, so `effi-` + line break + `cient` becomes `efficient`, never `effi cient`), then
*collapse* whitespace (§2.8), and split into
sentences at whitespace preceded by `.`, `!` or `?` and followed by an uppercase letter or `(`
(regular expression `(?<=[.!?])\s+(?=[A-Z(])`). A table row is treated as text: it becomes part
of whatever sentence the split produces. No other row segmentation is attempted.

**Bibliography entries are excluded by shape, not by section.** Before sentence splitting
(that is, on the section's lines, before hyphen removal and *collapse*), remove every *reference
entry*; its tokens are not harvested (they are counted as dropped). The section label is
deliberately **not** used: garbled or missing headings routinely file appendix tables under a
detected "References" heading, and those tables are results. Reference-entry rule (normative in
kind; the cue lists are reference values):

- **Indexed entry:** a line that begins with a bracketed index (`^\s*\[[^\]]{1,20}\]\s`, e.g.
  `[3]`, `[Smi21]`) starts an entry, which extends over the following lines up to, not including,
  the next such line, a blank line, or a heading (§2.7).
- **Unindexed entry line:** any other line that contains a DOI (`doi.org/`, `doi:`) or an arXiv
  identifier (`arXiv:\d{4}\.\d{4,5}`), or that contains a four-digit year (`(19|20)\d\d`)
  **and** a venue cue (`In Proceedings`, `Proc.`, `Conference on`, `Workshop on`,
  `Symposium on`, `Journal of`, `Transactions on`, `vol.`, `pp.`, `et al.`, `Press`,
  `arXiv preprint`), is removed by itself.

Entries are detected on lines because sentence splitting would cut an entry such as
`[3] B. Smith. Faster parsers achieve 12.5% gains. In Proceedings …` into fragments that no
longer look like a reference. Text under a "References" heading that is not a reference entry is
harvested like any other.

**2. Tokens.** In each sentence, find numeric tokens of these classes:

| Class | Shape (examples) | Kept |
|-------|------------------|------|
| `pm` | `N ± M`, `N +/- M`, `N \pm M`, with or without spaces (`76.39±0.00`, `76.39 ± 0.00`) | always |
| `percentage` | `N%` (`73.4%`) | always |
| `pvalue` | `p < 0.05`, `p=0.001` | always |
| `ratio` | `N` directly followed by `x`, `X`, or `×`, with **at most one space** between (`3.2×`, `3.2x`, `3.2 ×`, `12x`); the symbol must not be followed by a letter, digit, or `_`, nor by optional whitespace and a digit (so `3 x 3`, `1920×1080`, and `3xl` are not ratios) | always |
| `metric` | a plain number **with a radix point** (`0.912`, `81.0`, `0.00`) | only in a *metric sentence* |
| bare integer | a plain number **without a radix point and without a unit suffix** (`%`, `×`/`x`, `±`) (`2023`, `12`, `3`) | **never** (§8.4 A1, §8.7 E4) |

"Bare integer" is a property of the **source token**, not of its numeric value: `81.0` and
`0.00` are integer-valued but are `metric` tokens and are kept; `81` is a bare integer and is
dropped. A plain number is matched only when it is not part of a word, identifier, or larger
number (reference pattern `(?<![\w.\-])(\d+(?:\.\d+)?)(?![\w%])(?!\.\d)`).

**Raw token and value per class.** The *raw token* is the exact matched span of the source
sentence, trimmed at both ends, with inner whitespace kept as written:

| Class | Raw token (examples) | `reported_value` |
|-------|----------------------|------------------|
| `pm` | the whole `N ± M` span: `76.39±0.00`, `76.39 ± 0.00`, `0.5 +/- 0.1` | `N` (the centre value); the spread `M` is not a separate result and is not stored as a value |
| `percentage` | `73.4%` | `73.4` |
| `pvalue` | `p < 0.05`, `p=0.001` | the number |
| `ratio` | `3.2×`, `3.2 ×` (the span from `N` through the symbol) | `3.2` |
| `metric` | `0.912` | the number |

**Consumed spans.** Classes are matched in the order of the token table. A character span
matched by a `pm`, `percentage`, `pvalue`, or `ratio` token is *consumed*: no number inside it
is harvested again as a `metric` token. So `76.39±0.00` yields exactly one Result (raw
`76.39±0.00`, value `76.39`), never additional Results for `76.39` or `0.00`. Because the raw
token is part of the dedup key (step 3), `76.39±0.00` and `76.39 ± 0.00` in two different
sentences are two Results, and the same span written twice in one sentence is one.

A **metric sentence** contains a metric word (reference list, non-normative: accuracy, acc, F1,
F-score, AUROC, AUPRC, AUC, BLEU, ROUGE, METEOR, perplexity, PPL, precision, recall, mAP, IoU,
Dice, RMSE, MAE, MSE, PSNR, SSIM, error, loss, score, throughput, latency, speedup, reduction,
improvement, win rate, success rate, exact match, EM) or a result cue (reference list: achiev-,
outperform-, improv-, reduc-, increas-, decreas-, higher, lower, better, surpass-, gain(s),
demonstrat-, yield(s), attain(s), boost(s), exceed(s), beat(s), state-of-the-art, SOTA,
compared to/with, relative to, "we show", "results show"). Entries match whole words only (not
preceded or followed by a letter or digit). Entries written with two or more uppercase letters
(acronyms: F1, AUROC, AUPRC, AUC, BLEU, ROUGE, METEOR, PPL, mAP, IoU, RMSE, MAE, MSE, PSNR, SSIM,
EM, SOTA) match **case-sensitively, exactly as written**, so the ordinary words `map`, `Map`,
and `em` never make a metric sentence; every other entry matches case-insensitively
(`Accuracy`, `LOSS`).

Always skip a token that is a year (`19xx`/`20xx` without a radix point), that directly follows
a label word (Table, Figure, Fig., Section, Sec., Eq., Equation, Algorithm, Appendix), or that
is a list ordinal (`N.` or `N)` at sentence start or after `.!?:;`). Also always skip:

- **A section number.** A token of shape `\d{1,2}(\.\d{1,2}){0,3}\.?` that stands at the start
  of a sentence or directly after `.`, `!`, `?` or `:` and whitespace, and is followed by
  whitespace and a **title run**: the next word begins with an uppercase letter and is either all
  caps (at least three letters) or followed by at least one more word beginning with an uppercase
  letter among the next two words (one lowercase function word such as `of`, `and`, `versus`,
  `for` may sit between them). This catches a heading that the text reader glued into the
  surrounding prose: in `… as Table 3 shows. 2.4 Cross-Domain Robustness Analysis We compare
  …` the `2.4` is a section number, not a result; likewise `5 DISCUSSION` and `3. Method`
  (which are bare integers anyway). A heading on its own line never reaches this step (§2.7).
- **A name-and-version number.** A `metric` token that names a version of something rather than
  a measurement. A version number written with a `v` prefix (`v2.0`) or hyphen-joined to a name
  (`Lang-4.1`) never matches the plain-number pattern above, so it is already excluded. In
  addition, skip a `metric` token of shape `[1-9]\d?\.\d{1,2}` that directly follows (after one
  space) the word `version`, `ver.`, or `release`, or a **name word**: a *word* that begins with
  an uppercase letter and is not a metric word or result cue (lists above), unless the token is directly followed by another numeric token (a table row
  such as `Baseline 85.3 91.2` is kept). So `Solver 3.5 Lite`, `Python 3.12`, and `version 2.0`
  yield no Result, while `accuracy 0.912` and `Ours 0.85` (integer part 0) are unaffected. The rule accepts one known loss: a lone
  table cell such as `Baseline 85.3` with no neighbouring number is skipped.
  The class-`pm`, `percentage`, `pvalue`, and `ratio` tokens carry units and are never treated as
  versions. For this rule a **word** is a maximal run of letters, digits, hyphens, and
  apostrophes that is preceded by the start of the sentence, whitespace, or an opening
  punctuation mark (`(`, `[`, `{`, `"`, `'`, `“`, `‘`). So in `(Solver 3.5 Lite)` and
  `[Model 3.5]` the name word is `Model` and `3.5` is skipped.

**3. Dedup key.** Within one pass, a number is identified by (raw token, sentence); repeats are
dropped. Two passes are RECOMMENDED: a page-aware pass over per-page text (which yields page
numbers) and a full-text pass (which recovers numbers split across page boundaries). Their
outputs are merged and deduplicated by the key

```text
( round(value, 6), raw token, lowercase(collapse(context)) )
```

where `context` is the first 240 characters (reference value) of the sentence. A full-text
number gets a page when the first 20 characters of its context occur in exactly one page's text.

**4. Emission.** Results are numbered `R1, R2, …` in harvest order:

```yaml
- id: R12
  validates: [C3]                 # claim ids (§3.5); [] when unlinked
  kind: metrics                   # SDK Result kind (SDK §2.3)
  validation_mode: attest         # SDK evidential mode; the verdict ceiling (origin evidence_cap, §3.3)
  evidence: paper.pdf             # the copied paper file (relative path); the paper is the only source
  reported_value: 0.912           # tool extension field: the token's numeric value (table above)
  locators:
    paper:
      quote: "0.912"              # the raw source token
      token_class: metric         # tool extension: pm | percentage | pvalue | ratio | metric (step 2)
      page: 6                     # when known
      section: "results"          # detected section label, when known
      context: "Our model achieves an accuracy of 0.912 on the held-out split."
```

`produced_by` is **omitted** (no experiment exists; the schema types it as a string, so it is
never written as `null`). `evidence` is the manifest's paper pointer (`paper.pdf` or
`paper.source`), exactly as written there: the paper is the declared source of every
paper-origin result. Consumers MUST NOT treat a Result whose `evidence` equals the artifact's
declared paper file as **shipped evidence** of a result (§4.5.3): pointing at the paper says
"the paper reports this", which is attestation, not corroboration.

`quote` is the raw token and `context` is a **normalized excerpt** (§2.8): the *collapse*d
sentence, not a byte-exact substring of the PDF. A consumer that needs to find it in the paper
uses the *squash* procedure (§2.8). Result-shaped numbers that fail the rules above are counted
as dropped in `GENERATION.md`.

## 3.5 Headline claims

A **headline claim** is a sentence from a headline section (abstract, introduction, an explicit
contributions section, or the conclusion) that carries a harvested result token and either (a)
the token is `percentage`, `pm`, `pvalue`, or `ratio`, or (b) the sentence is in the authors'
voice ("we", "our", "us") or contains a metric word. Tokens that are citation markers (`[8]`),
labels (`Stage 3`, `H1`), symbol subscripts, or enumerators (`(2)`) never seed a claim.

**Table rows never seed a claim.** A *numeric word* is a whitespace-separated word that is, as a
whole, a number in the sense of the result tokens of §3.4: digits with an optional leading sign,
an optional radix point and fraction, an optional trailing `%`, and an optional `±` spread
(reference pattern `^[+\-−]?\d+(\.\d+)?%?(±\d+(\.\d+)?%?)?$`). A word that only contains a
digit (`F1`, `Lang-4.1`, `(Table`) is not a numeric word. A candidate sentence that contains a
run of **4 or more consecutive numeric words** (reference value) is rejected as a claim, because
adjacent numbers are table cells. The sentence still yields its Results (§3.4). So
"… Baseline 81.20±0.10 79.45±0.32 80.02 77.91 90.13±0.05 …" seeds no claim, while "Our method
improves accuracy from 71.2% to 84.5% and F1 from 0.61 to 0.78." is kept, because no two of its
numbers are adjacent.

Each distinct sentence (case-insensitive) yields at most one claim, numbered `C1, C2, …` in this
**normative order**: candidate sentences are sorted by section weight, descending, with a stable
sort (ties keep harvest order, i.e. position in the paper):

| Section of the seeding token | Weight |
|------------------------------|--------|
| abstract; contributions (an explicit contributions section, or a sentence in the `introduction` section or the `front` section (text before the first heading line, §2.7) that contains a contributions cue such as "our contributions", "we contribute", "in summary") | 1.0 |
| conclusion | 0.9 |
| introduction | 0.8 |

A sentence seeded by several tokens is placed by its first (highest-weight, earliest) token.
The weights are only an ordering device; they are not written to the output.

```yaml
- id: C3
  statement: "Our model achieves an accuracy of 0.912 on the held-out split."   # rejoin(context), §2.8
  kind: empirical
  measurability: measurable
  paper_ref: { quote: "0.912", page: 6, section: "abstract", context: "…" }
  validators:
    - { id: v1, kind: attest, checks: provenance, inputs: [R12] }   # its linked results
```

The claim `statement` is *rejoin*(context) (§2.8): the sentence with line-break hyphenation
removed for display (`evalua- tion` → `evaluation`). `paper_ref.quote` (the raw token) and
`paper_ref.context` (the *collapse*d sentence, §3.4) are left exactly as harvested.

**Edge direction.** The canonical claim↔result edge is **`Result.validates`** (SDK §2.3): a
result lists the claim ids it supports. A result is linked to a claim **only** when both come
from the **same sentence** (the Result's `context` and the claim's `paper_ref.context`, equal after removing all whitespace and lowercasing; if one is a
prefix of the other, the shorter must be at least 40 characters) **and** the result's
`reported_value` equals the claim's headline value within a relative tolerance of 1e-3
(reference value). Otherwise the result is unlinked. A wrong link is worse than a missing one.
An implementation MAY mirror the edge on the claim (e.g. `supported_by: [{result: R12}]`);
consumers MUST read `Result.validates`.

**Exactly one `attest` validator.** Every paper-origin claim carries `validators` with exactly
one entry, `{id: v1, kind: attest, checks: provenance, inputs: [...]}`, whose `inputs` are the
IDs of the Results that `validate` this claim, in Result order (`[]` when none is linked). No
other validator kind is ever synthesized, and no `stance` is written. The SDK semantics apply
unchanged (SDK §3.5, attest-as-verdict): the judge evaluates it as the claim's own `attest`
validator (§4.5.2), so a claim with linked results is `attested` (at most `PARTIAL` in roll-up,
never `verified`), and a claim with `inputs: []` fails the attest check and is `unverifiable`.
"The paper says so" is the strongest statement a paper-origin claim can earn.

## 3.6 Figures, references, related work, contributions

### 3.6.1 Figures (caption-anchored)

Figures are anchored on their captions, not on embedded images:

1. A **caption** is a text block on a PDF page whose text begins `Figure N` or `Fig. N`
   followed by `.` or `:` (case-insensitive; reference pattern
   `^(fig(ure)?\.?)\s*(\d+)\s*[.:]\s+`). Only the first caption for each number is used.
2. The figure **area** is the region **above** the caption, within the caption's column (both
   columns when the caption spans the page centre), bounded above by the nearest preceding
   caption or page header.
3. If an embedded raster image lies in that area, it is the figure (when a page has exactly one
   caption, an otherwise unused image anywhere on the page qualifies). Otherwise the area is
   **rendered** to a PNG (vector graphics). Reference values (non-normative): 160 dpi,
   at most 36 pt of whitespace between drawing and caption, minimum region 15 × 30 pt.
4. Each figure is written to `figures/figure-<N>.<ext>` and listed in `figures.yml`:

```yaml
figures:
  - id: figure-3
    number: 3
    path: figures/figure-3.png
    caption: "Figure 3: Accuracy versus training steps."
    page: 7
    claims: [C2]          # advisory: claims whose wording overlaps the caption (≥2 discriminating tokens)
```

**Limitation:** the method assumes captions sit **below** their figures; captions above a figure,
uncaptioned figures, and figures spanning pages are missed or mis-cropped. `GENERATION.md` MUST
state this limitation. The `claims` links are advisory and never become `validates` edges.

**Extraction status.** `GENERATION.md` reports the number of figures written. When it is 0, it
also states why, so that "no figures" is never confused with a failure:

| Status | Meaning |
|--------|---------|
| `renderer unavailable` | The implementation has no component that can read the page images and drawings of this source (for example, an optional PDF renderer is not installed). |
| `renderer failed` | The renderer was available but raised an error on this paper. |
| `no captions found` | Extraction ran and found no caption under rule 1. |

### 3.6.2 References

If a bibliography was supplied or a references section is detected, emit
`paper_references.yml` (`references:`) with one entry per reference: `id`, `raw`, and any `doi`,
`arxiv`, `isbn`, `url` found, and point `paper.references_export` at it. Omit the file if none
are found.

**Splitting a detected references section.** When the section's entries carry bracketed indexes
(`[1]`, `[Smi21]`), each index starts an entry. Otherwise the adapter splits the section's lines
as follows:

1. **Entry starts.** A line starts a new entry when it begins with any of these shapes
   (reference patterns, non-normative):
   - a number `N.` or `N)`, where the first is `1` and each next one is greater by one;
   - a surname-first author: a capitalized surname, a comma, and initials (`Adams, J.,`;
     `^[A-Z][\w'’\-]+(?: [A-Z][\w'’\-]+)*, (?:[A-Z]\.\s?)+`);
   - an initial-first author: initials, then a capitalized surname (`A. Author`,
     `J. K. Smith`; `^(?:[A-Z]\.\s?)+[A-Z][\w'’\-]+`);
   - a list of full author names followed, on this line or the next, by a year sentence
     (`Jane Smith and Ali Khan. 2020.`; the year sentence is `. ` then a year `(19|20)\d\d`,
     an optional lowercase letter, and `.`);
   - an organization name directly followed by a year sentence (`ExampleOrg. 2024.`).
2. **Continuations.** Every other line joins the current entry. A line also joins the current
   entry, whatever its shape, when the previous non-blank line ends with `,`, `-`, `and`, or
   `&`. Blank lines are not entry boundaries: text readers put blank lines both between entries and
   inside one entry that wraps across a column or page break. Lines before the first entry
   start belong to no entry.
3. **Validation.** An entry is kept only when it contains a four-digit year `(19|20)\d\d` or
   carries a DOI, an arXiv identifier, or a URL. When no entry is kept, the adapter writes no
   `paper_references.yml` and `GENERATION.md` reports `references: not split (unrecognized
   format)`. The adapter never emits the whole section as one entry. A single kept entry is a
   valid one-entry bibliography.
4. **IDs.** Kept entries get the IDs `1, 2, …` in order.

### 3.6.3 Related work

Emit `paper_related_work.yml` (`related_work:`) with positioning statements (sentences that
compare the paper to prior work), each with its quote, location, and any citation keys it
carries. Omit the file if none are found.

### 3.6.4 Contributions (source-only)

The adapter emits **candidate** contributions (SDK §2.4.2): advances the authors **state**, never
advances the adapter infers or judges. Candidates come from exactly one of two sources, applied
over the whole extracted text (§2.7; offsets as in §2.8):

1. **Explicit contribution list.** If the paper contains at least one list item under the rule
   below, the candidates are **those items and nothing else**. Advance sentences elsewhere ("we
   present X" in the abstract, introduction or conclusion) summarize the same advances and are
   not added.
2. **Advance sentences (fallback).** Only when the paper has **no** list item at all.

**List rule.** A *list cue* is a match of
`\bcontributions?(?:\s+(?:are|include|is))?(?:\s+as\s+follows)?\s*:` (case-insensitive), e.g.
"Our contributions are as follows:", "we make the following key contributions:". After the cue,
skip whitespace and an optional `\begin{itemize}` or `\begin{enumerate}` (with an optional
`[…]` argument). The text there MUST begin with an **item marker**, otherwise this cue yields no
list. Item markers (one *family* per list, fixed by the first marker):

| Family | Marker | Next marker of the family |
|--------|--------|---------------------------|
| parenthesized number | `(N)`, N of 1–2 digits | `(N+1)` |
| parenthesized roman | `(i)` … `(x)`, lowercase | the next roman numeral |
| number | `N.` or `N)` followed by whitespace | `N+1.` or `N+1)` |
| LaTeX item | `\item`, optionally `\item[…]` | `\item` |
| bullet | `•`, `▪`, `◦`, `●`, or (at a line start only) `-` or `*` followed by a space | the same character |

An item starts at its marker and ends at the earliest of:

- the next marker of the family. Numbered and roman markers are recognized anywhere in the text
  when preceded by whitespace (so an inline list "Our contributions are: (1) a parser; (2) a
  benchmark." has two items); bullet and `\item` markers only at a line start;
- a blank line;
- a line that begins with a LaTeX command other than `\item` (for example `\end{itemize}`);
- a heading line (§2.7);
- the end of the text.

The span is then trimmed at its end, in this order: trailing whitespace; a trailing word `and`
or `or` with the whitespace before it; one trailing `;` or `,` (so the item `(1) a parser; and`
ends at `parser`).
The list ends when an item ends for any reason other than the next marker; a later cue may
start another list. Each item gives one candidate:

- `paper_ref.quote` is the exact span `text[char_start:char_end]` from the marker through the
  trimmed end, and is never rewritten;
- `statement` is *rejoin*(quote) (§2.8) with the leading marker and its whitespace removed and
  emphasis markup unwrapped (`**T**`, `__T__`, `\textbf{T}`, `\emph{T}` → `T`). Line-break
  hyphenation is therefore gone from the statement (`We in- troduce` → `We introduce`) and kept
  in the quote.

An item that opens with a short title, either a bold run or a run of 3–90 characters without
`:` or `.` followed by `:` (`(2) Caption anchoring: we locate figures by …`), keeps that title
inside `statement`. No separate title field is emitted. A consumer MAY display the run before
the first `:` as the title and the rest as the summary.

**Advance-sentence rule (fallback).** A *cue* is a match, case-insensitive except that the verb
must not continue with a lowercase letter, of

```text
\b(?:we\s+(?:present|propose|introduce|design|develop|contribute)
   |(?:our|the)\s+(?:(?:main|key|primary|central|principal|core)\s+)?contributions?
    (?:\s+of\s+this\s+(?:paper|work|study))?\s+(?:are|include|is))
```

Only these present-tense forms are cues: "we presented", "we proposed", and "we have
introduced" are not, so a conclusion that restates the work in the past tense yields nothing.
The candidate span is the cue's sentence:

- **start:** after the last `.`, `!` or `?` followed by whitespace, or the last blank line,
  before the cue (or the text start), then past any lines consisting only of a LaTeX command.
  If the text between that start and the cue is longer than 200 characters, contains `\`, or
  is non-blank while the cue begins with an uppercase letter (the reader lost the preceding
  period), the span starts at the cue instead. A lead-in such as "In this paper, " is thus
  kept. **A sentence never spans a heading line (§2.7):** the start is never earlier than the
  first character after the nearest heading line that precedes the cue, so in A16 the quote
  begins `In this paper`, never `Introduction In this paper`;
- **end:** the first `.`, `!` or `?` after the cue that is followed by whitespace or the end of
  the text, or a `.` between two lowercase letters and an uppercase-then-lowercase pair (a
  sentence glued to the next: `systems.Our`), whichever comes first; otherwise the end of the
  text. The end is never later than the end of the line before the next heading line.

A sentence that matches `\blimitations?\b`, `\bnot\s+(yet\s+)?(been\s+)?completed\b`, or
`\bfuture\s+work\b` is not a candidate. `paper_ref.quote` is the exact span, and `statement` is
*rejoin*(quote).

**Dropping duplicates and restatements.** Candidates are considered in text order, and each is
kept or dropped against the candidates already kept:

1. A statement outside 25–2000 characters (reference values) is dropped.
2. Its *comparison key* is *rejoin*(statement), lowercased, with trailing spaces and `.!?;:`
   removed. A candidate whose key is contained in a kept key, or contains one, is dropped.
3. **Restatement (fallback candidates only).** The *object head* of an advance sentence is the
   text after its cue, lowercased; leading words from {a, an, the, our, this, these, its, new,
   novel, first} removed; then cut before the first `,`, `;`, `:`, `.`, `(`, or the first word in
   {that, which, who, for, to, with, and, in, on, of, by, using, called}; and kept to at most 5
   words, compared after *fold*. A candidate whose section label (§2.7) is `conclusion`, or that
   lies after the first conclusion heading, is dropped when its object head is non-empty and
   equals the object head of a kept candidate. For example, an introduction sentence "In this
   paper, we present Sieve, a compressor for sensor logs." (object head `sieve`) is kept; the
   conclusion sentence "In this paper we present Sieve, which shrinks logs before
   upload." has the same object head and is dropped; "We presented Sieve …" is not a cue at
   all.

Each kept candidate is emitted as:

```yaml
- id: contribution/<sha256>                    # SHA-256 of collapse(quote); full 64-hex digest, never truncated
  statement: "We introduce a caption-anchored figure extractor ..."   # rejoin, marker removed (above)
  supporting_claims: [C2]                     # only claims whose statement it contains (case-insensitive)
  paper_ref: { quote: "<exact span>", char_start: 1042, char_end: 1110 }
  provenance:
    kind: paper-extraction
    source: "paper:document"
    method: author-contribution-list-item/v1  # or explicit-author-advance-sentence/v1
    locator: { quote: "<exact span>", char_start: 1042, char_end: 1110 }
```

Rules: the `id` hashes the *collapse*d quote (UTF-8), not the display statement, so improving
the display normalization never changes an ID. `quote` is the exact slice
`text[char_start:char_end]` of the adapter's extracted text (§2.8); no `significance`,
`originality`, or qualification is ever emitted; `supporting_claims` is never inferred from
meaning, only from verbatim containment of the claim's `statement` in the contribution's
`statement`, case-insensitively (it is usually empty, which is a legal draft warning, §4.5.7).
Inferring support or assessing the advance is the reviewer's job (§5.13). The one exception is
optional enrichment: when it ran, the adapter adds the extractor's proposed links as
`inferred_supporting_claims`, kept apart from `supporting_claims` and attributed to the
extractor (§3.7).

## 3.7 Optional LLM enrichment

When an LLM provider is configured (§7.1), the adapter MAY run an enrichment pass:

1. An **extractor** prompt proposes claims, each with a quote and a reported value.
2. An independent **verifier** prompt, given only the paper text and one proposal, accepts or
   rejects it.
3. An accepted proposal is **bound** to a deterministic result only if the values agree within
   a tight relative tolerance (reference value: 1e-6) **and** the metric names corroborate.
   Unbound proposals become claims whose single `attest` validator has `inputs: []` (§3.5).
4. Every quote MUST be located in the paper text with the *squash* procedure (§2.8); proposals
   whose quote cannot be located are dropped.
5. The extractor MAY link each proposed claim to the contributions (§3.6.4) whose advance it
   substantiates. The adapter records these links by full contribution ID
   (`contribution/<64 hex>`). When the prompt names contributions by short labels, the adapter
   MUST map each label back to the full ID before it writes anything.

If enrichment fails for any reason, the adapter MUST keep the deterministic output and record
the failure in `GENERATION.md`. Enrichment MUST NOT raise `evidence_cap`.

**Stages and their outcomes.** Enrichment has two stages, `extract` (steps 1 and 5) and
`verify` (step 2). Each ends as `completed` or `failed: <reason>`. Enrichment *fails* when the
extract stage fails or yields no claim; the adapter then keeps the deterministic output. A
failed verify stage (for example, the verifier model is unavailable) does not discard the
extracted claims, but none of them counts as verified, and `GENERATION.md` MUST say that the
claims are unverified. A verify stage that returns no judgment for any proposal counts as
failed.

**Contribution links after enrichment.** When enrichment succeeds and `contributions.yml` was
generated in this run, the adapter rewrites `contributions.yml` against the new claims. It never
rewrites a file a human has edited (§3.8). For each contribution:

1. **Recompute `supporting_claims`** with the rule of §3.6.4 (verbatim, case-insensitive
   containment of a claim `statement` in the contribution `statement`). Entries that named
   claims which no longer exist disappear by construction.
2. **Add `inferred_supporting_claims`**: the IDs of the claims that the extractor linked to this
   contribution (step 5), in claim order, without IDs already in `supporting_claims`, without
   duplicates. Omit the key when the list is empty.
3. **Record the source** in `provenance.claim_link_sources`, an ordered list with one record per
   inferencer that added at least one link. Each record is
   `{kind: extractor-inference, method, model, claims}`, where `method` names the enrichment
   method and its version, `model` is the extractor's opaque model label (as in
   `origin.extractor.llm`, §3.3), and `claims` lists the claim IDs this source added to
   `inferred_supporting_claims` in step 2. Omit the key when no source added a link.

`supporting_claims` stays reserved for declared links and for links found deterministically.
`inferred_supporting_claims` and `claim_link_sources` are open extension fields: SDK records
are open (SDK §2.4.2), so they need no schema change. Example:

```yaml
- id: contribution/<sha256>
  statement: "We introduce a streaming parser for nested logs."
  supporting_claims: []
  inferred_supporting_claims: [claim-1, claim-2, claim-5]
  provenance:
    kind: paper-extraction
    method: explicit-author-advance-sentence/v1
    claim_link_sources:
      - { kind: extractor-inference, method: "<enrichment method>/v1", model: "<opaque>",
          claims: [claim-1, claim-2, claim-5] }
```

**Commit order.** The adapter writes the enriched `claims.yml`, the updated `results.yml`, the
rewritten `contributions.yml`, and the ledger together, and only once the outcome of every
stage is known. A run that ends with enrichment failed leaves the deterministic files in place.
`GENERATION.md` is written last, from the files as written (reloaded, never from an earlier
in-memory state), and the ledger is then refreshed to record its hash. It reports the claim
count of `claims.yml` with its source (`deterministic seed`, or the extractor with its model
label), and the outcome of each stage (`extract: completed`, `verify: failed: <reason>`, …).

## 3.8 Idempotency

Running the adapter twice on the same paper with the same options and adapter version MUST
produce byte-identical files, except for timestamps confined to `GENERATION.md` and
`.adapter/state.json`.

When re-running into its own earlier output, the adapter MUST NOT silently overwrite a
generated file that a human has since edited. In particular, if `contributions.yml` no longer
matches the hash the adapter recorded for it (its ledger, §3.2), the run fails with an input
error instead of overwriting the edit; an edited file is authored input, not generated output
(SDK §5.2).

**Re-runs with different options.** Every run regenerates its output from the paper. Nothing
carries over from an earlier run, so links never appear or vanish depending on what ran before.
The ledger records the options that shaped the output: whether enrichment was requested, and
the extractor and verifier model labels.

| Previous run | This run | Result |
|--------------|----------|--------|
| any | without enrichment | Deterministic output. No `inferred_supporting_claims` and no `claim_link_sources`. |
| any | with enrichment, which succeeds | Enriched output (§3.7). |
| any | with enrichment, which fails or yields no claim | Deterministic output; `GENERATION.md` records the failure (§3.7). |
| any, and `contributions.yml` edited since | any | Input error before anything is written. |
