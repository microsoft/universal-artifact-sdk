# Judge summary

> [!WARNING]
> **Experimental, AI-generated example. No human judgement.** This review was produced
> automatically by an experimental reference implementation of the judge/reviewer
> specification. No person reviewed, edited, or endorsed it. It does not represent the
> opinion of the SDK maintainers, Microsoft, or any reviewer, and it is not an assessment of
> the paper or its authors. It may contain errors. It is published only to show what the
> tool's output looks like.

> **Auto-generated** from `judge.json`, `artifact/claims.yml`, and `artifact/results.yml` by
> the example publication script. Not a spec-defined output; `judge.json` is authoritative.

**Overall rubric:** PARTIAL. **Badges:** available = unverifiable, functional = unverifiable, results_reproduced = unverifiable.

The judge checks structure and claim-to-evidence links deterministically. It does not
judge whether the science is right. This artifact was converted from the paper alone, so
the only evidence is the paper itself (`attest`): the judge can confirm each claim points
to a number the paper reports, not that the number is correct.

## Claims and their evidence

The paper adapter automatically extracted **1** claim and **556** reported numbers.
Only 1 of those numbers is linked to a claim; the rest are recorded in `artifact/results.yml` without one.
Extraction is heuristic and can be wrong: a claim may be a table row read as text. The
reviewer's analysis of the paper's broader claims is in [`review-draft.md`](review-draft.md).

| Claim | Statement | Evidence (paper) | Reported value | Judge verdict |
|-------|-----------|------------------|----------------|---------------|
| C1 | ResNet18 Vision Transformer data metric baseline retrain LFSSD SSD baseline retrain LFSSD SSD Cifar100 Dr 76.39±0.00 72.89±0.34 76.36 76.08 88.84±0.00 90.10±0.19 89.03 89.06 Df 70.49±0.00 0.00±0.00 0.00 0.00 97.22±0.00 0.00±0.00 0.00 36.89 | R1: p.2, “76.39±0.00” | 76.39 | advisory: claim C1: attest[provenance] — provenance: 1 input(s) resolve to shipped, non-empty evidence. |

## All judge checks

`unassessable` and `unverifiable` mostly mean the paper-only artifact has nothing to
check (no code, traces, or checksums); they are coverage notes, not failures.

### verified (3)

| Check | Finding |
|-------|---------|
| `structure/paper` | paper present at paper.pdf. |
| `provenance/generated-marker` | manifest.yml carries its generated marker. |
| `provenance/claims` | authored input claims.yml present and ledgered. |

### advisory (2)

| Check | Finding |
|-------|---------|
| `claim_validators/C1.v1` | claim C1: attest[provenance] — provenance: 1 input(s) resolve to shipped, non-empty evidence. |
| `assessments/citation_integrity` | citation integrity: all 1 exported reference(s) carry an existence-checkable identifier (DOI/arXiv/URL). Advisory — supportiveness is an inspection question. |

### unverifiable (3)

| Check | Finding |
|-------|---------|
| `structure/readme` | no standalone usage doc declared — documentation completeness is unassessable (usage guidance is expected in the paper and experiment dirs). |
| `structure/dependencies` | no dependencies declared — Functional reproducibility is at risk. |
| `provenance/reflection` | optional input reflection.md not shipped — nothing to audit (coverage note). |

### unassessable (9)

| Check | Finding |
|-------|---------|
| `structure/experiments` | no experiments registered — the artifact runs nothing (paper-origin / described-only); reproduction is unassessable, not a failure. |
| `paper_consistency/unassessable` | harvested 556 reported number(s) from paper.pdf (pypdf, 7 page(s)), but the artifact declares no shipped evidence to cross-check against (paper-origin / described-only) — paper↔data consistency is unassessable, not a failure. |
| `provenance/checksums` | No SHA256SUMS declaration; shipped checksum integrity unassessed. |
| `assessments/execution_authenticity` | execution authenticity is unassessable: no trace was declared, so whether the reported work actually ran cannot be judged (coverage note, not a failure). |
| `assessments/execution_authenticity/provenance_journal` | provenance journal is unassessable: no journal.yml was declared, so the narrated edit history cannot be reviewed (optional; coverage note, not a failure). |
| `assessments/trace_report_faithfulness` | trace-report faithfulness is unassessable: no trace was declared to reconcile against the paper's account (coverage note, not a failure). |
| `assessments/related_work_validity` | related-work validity is unassessable: a paper was read (from pdf) but no related-work section could be located to analyze (coverage note, not a failure). A future SDK related_work_export would remove the extraction ambiguity. |
| `assessments/limitation_transparency` | limitation transparency is unassessable: no reflection.md was shipped (optional; coverage note, not a failure). |
| `assessments/agent_faithfulness` | agent faithfulness is unassessable: no research-agent.md was shipped (optional; coverage note, not a failure). |

## Contribution declaration notes

- `contributions[0].supporting_claims` (warning): claim support not declared
- `contributions[1].supporting_claims` (warning): claim support not declared
- `contributions[2].supporting_claims` (warning): claim support not declared
