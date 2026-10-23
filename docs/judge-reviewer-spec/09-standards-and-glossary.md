> **Audience**: Anyone reading or implementing this specification.
> **Source of truth for**: The published standards every check and verdict is grounded in, and
> the meaning of the specification's terms.

# 9. Standards and glossary

## 9.1 Grounding standards

Every finding's `grounded_in` field (§4.2) and every review criterion (§5.2, §7.4) cites one or
more of these IDs. A check that cannot be traced to at least one of them does not belong in a
conforming core; put it in an extension (§7.5).

| ID | Source | Kind | Used for |
|----|--------|------|----------|
| S1 | ACM, *Artifact Review and Badging*, Version 1.1. <https://www.acm.org/publications/policies/artifact-review-and-badging-current> | Policy | Verdict vocabulary; Available, Functional, and Results Reproduced badges (§4.8); structural expectations (§4.5.1); integrity (§4.5.4). |
| S2 | NISO RP-31-2021, *Reproducibility Badging and Definitions*. <https://www.niso.org/standards-committees/reproducibility-badging> | Recommended practice | Repeatable / reproducible / replicable terminology; the reproduction tier (§4.1, §4.9). |
| S3 | Pineau et al., *The Machine Learning Reproducibility Checklist*. <https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf> | Community checklist | Inventory of what must be shipped: model, data, code, compute, claims (§4.5). |
| S4 | NeurIPS reviewer guidelines and review form. <https://neurips.cc/> | Venue review form | Soundness, presentation, contribution, originality, significance, limitations (§5.4, §5.12, §5.13). |
| S5 | ACL Rolling Review reviewer guidelines. <https://aclrollingreview.org/reviewerguidelines> | Venue review form | Soundness, excitement, reproducibility, and ethics axes (§5.2.1). |
| S6 | ACM SIGPLAN, *Review of Conference Papers* policy. <https://www.sigplan.org/Resources/Policies/Review/> | Policy | Acceptance criteria, including "sufficient information to reproduce" (§4.5.3, §5.2.1). |
| S7 | Blackburn, Hauswirth, Berger, Hicks, Krishnamurthi, *SIGPLAN Empirical Evaluation Checklist*. <https://www.sigplan.org/Resources/EmpiricalEvaluation/> | Community checklist | Claims supported by adequate evidence; honest reporting of negative results (§4.5.2, §4.5.5). |
| S8 | Community tutorials on how to review papers (for example, conference-hosted reviewer-training material). | **Secondary** | Heuristics for the advisory reviewer only. MUST NOT ground a verdict. |

Rules:

- Verdict-producing findings (anything other than `advisory`) MUST cite at least one of S1–S7.
- If a standard is revised, the specification is versioned; a tool MUST NOT silently re-ground a
  check against a different revision.
- Public artifact-evaluation committees for many venues publish per-badge checklists derived
  from S1. These are suitable test material for the `structure` check and the badge profile.

## 9.2 Glossary

| Term | Meaning |
|------|---------|
| **Advisory** | Content that informs a human but never changes a verdict, the rubric, or a decision. All model output is advisory. |
| **Artifact** | A directory (or archive) in the `evaluable-artifact/v3` format (v2 remains readable): manifest, paper, claims, results, evidence, and optional environment, experiments, traces, reflection, and contributions. |
| **Artifact-informed scope** | A review run that also snapshots the artifact and runs the judge. Opposite of paper-only. |
| **Attested** | Supported only by the producer's statement or by the paper's own text, not by evidence the tool can check. The ceiling for paper-only artifacts (§3). |
| **Badge profile** | A mapping from the rubric and structure findings to ACM-style badges (§4.8). Display only. |
| **Bare integer** | A source token that is a plain number without a radix point and without a unit suffix (`2023`, `12`). A property of the token, not of its value: `81.0` is not a bare integer. Never harvested as a result (§3.4). |
| **Check** | A deterministic function from an artifact to a list of findings (§4.4). |
| **Claim** | A statement the paper makes, declared in `claims.yml`, with validators that link it to Results. A claim may be a `finding` or a `hypothesis`. |
| **Claim support** | One of the three contribution axes: whether a contribution is backed by claims, through declared `supporting_claims` or reviewer-inferred links, and how well those claims are settled (§5.13.3). |
| **Consumer** | Any tool that reads a sealed run. Must validate it first (§6.7). |
| **Contribution** | A candidate advance the paper puts forward (SDK §2.4.2), either declared in the artifact's `contributions.yml` or extracted from the paper's own text. The tool reviews contributions along three separate axes; it never decides whether one qualifies (§5.13). |
| **Contribution diagnostic** | A structural problem in the declared contributions (for example, an unresolved claim reference). Reported beside the findings, never as a finding, and never affects the rubric, badges, or exit code (§4.5.7). |
| **Critic** | The reviewer stage that deduplicates, merges, and ranks specialist findings (§5.6.2). |
| **Decision** | Accept/reject, a score, a confidence level, or a badge award by a human. The tool never makes one (I4). |
| **Evidence** | Files shipped in the artifact (or regenerated by a reproduction provider) that a Result points to. |
| **Evidence bundle** | The bounded, ID-addressed text the reviewer's models are allowed to see and cite (§5.3). |
| **Evidence-conditioned activation** | The rule that a check reports `unassessable` when its evidence was never declared and `unverifiable` when it was declared but does not resolve (I5, §4.3). |
| **Finding** | One unit of output with an ID, a verdict, a message, and evidence pointers (§4.2, §5.5). |
| **Gate** | An `attest` validator that another validator on the same claim names in `gated_by` (§4.5.2). |
| **Heading line** | A line of the text source recognized as a section heading: Markdown or LaTeX markup, a numbered title phrase (`2.4 Cross-Domain Robustness Analysis`, `5 DISCUSSION`), or a named heading. It opens a section and is not itself section text (§2.7). |
| **Headline number** | A reported number in the abstract, introduction, contributions, or conclusion, or in a sentence citing a figure or table (§4.5.3). |
| **Human-owned** | Fields reserved for a human reviewer: recommendation, scores, confidence, contribution qualification. Always `null`/"unset" in tool output. |
| **Integrity** | Shipped bytes match their declared hashes or pointers. Not authenticity, and not correctness. |
| **Mode verdict** | How strongly a claim was settled: `re-executed`, `re-analyzed`, `evidence-supported`, `attested`, or a negative value (§4.1). |
| **Negative result** | A tested hypothesis whose experiment failed or was abandoned, preserved with a rationale. Recognized, never penalized. |
| **Normalized excerpt** | A quote-like field the tool *produces* from extracted text (for example, a harvested result's *collapse*-normalized context sentence, §3.4) rather than locates in it. Consumers locate it with the *squash* procedure (§2.8). |
| **Originality** | One of the three contribution axes: the distinction a contribution claims over prior work, judged against the authors' stated position and the references actually inspected. Never `supported` without inspected prior work (§5.13.3). |
| **Pack** | Area or methodology criteria added to a review configuration (§5.2, §7.4). |
| **Page furniture** | Running headers, footers, and page numbers repeated in the top or bottom lines of many PDF pages; removed before harvesting only (§3.4 step 0). |
| **Paper-only scope** | A review of the paper alone; nothing from the artifact is read. The default. |
| **Producer** | Whoever built the artifact: authors, an agent, or a conversion tool. The tool treats all producers alike (I8). |
| **Profile** | A venue's review form and criteria (§5.2.1). |
| **Qualification** | The human decision whether a contribution qualifies as an advance. Always `null` in tool output (`human_qualification`); recorded, if at all, in a human sidecar (§5.13.4, §7.6). |
| **Quote** | An excerpt of the paper's *extracted* text, located by one of the procedures in §2.8. Evidence that the text exists in the paper, not a byte-exact copy of the PDF. |
| **Reference entry** | A bibliography entry recognized by its shape (an indexed line, or a line with a DOI, arXiv ID, or year plus venue cue), never by its section label. Its numbers are not harvested (§3.4). |
| **Rejoin** | The display normalization that removes line-break hyphenation (`evalua- tion` → `evaluation`) from claim and contribution statements; never applied to quotes (§2.8). |
| **Repair** | An edit a reproduction provider made to its copy of the artifact so an experiment could run. Always recorded and reported (§7.2). |
| **Reproduction provider** | A pluggable component that executes artifact experiments in a sandbox (§7.2). |
| **Result** | A declared, located number or output in `results.yml` that claims point to. |
| **Rubric** | The judge's overall outcome: `REPRODUCED`, `PARTIAL`, or `NOT_REPRODUCED` (§4.7). |
| **Run** | One sealed output directory with a manifest (§6). |
| **Scripted provider** | A deterministic test double for the LLM provider that returns fixed responses per call role (§7.1, §8.5.1). |
| **Sealed** | Every input and output file is hashed into a completed manifest, and the directory is never modified afterward. |
| **Significance** | One of the three contribution axes (`significance_and_relevance`): why the contribution matters and to whom, as anticipated or observed impact (§5.13.3). |
| **Snapshot** | The tool's private, hashed copy of its inputs inside the run (§2.5). |
| **Specialist** | One focused reviewer prompt role, such as soundness or presentation (§5.4). |
| **Stable ID** | A finding ID derived from content so re-runs on identical input produce identical IDs: a full SHA-256 content hash for reviewer findings, a short hash for judge-derived findings (§5.5). |
| **Stage** | A named step of a run with an explicit status (§6.4). |
| **Unassessable** | The needed evidence was never declared. A coverage note, not a defect. |
| **Unverifiable** | The evidence was declared but cannot be resolved or settled. Visible, blocks `REPRODUCED`, but not a failure. |
| **Validator** | A rule attached to a claim that decides whether a Result supports it (§4.6). |
