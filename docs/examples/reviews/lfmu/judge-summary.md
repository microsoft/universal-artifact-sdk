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

The paper adapter automatically extracted **9** claims and **54** reported numbers.
Every number is linked to at least one claim.
5 claims cite no reported number, so the judge marks them `unverifiable`.
Extraction is heuristic and can be wrong: a claim may be a table row read as text. The
reviewer's analysis of the paper's broader claims is in [`review-draft.md`](review-draft.md).

| Claim | Statement | Evidence (paper) | Reported value | Judge verdict |
|-------|-----------|------------------|----------------|---------------|
| claim-1 | LFSSD is competitive with state-of-the-art approaches such as SSD while producing scores similar to a model retrained on only Dr. | R1: p.2, “76.39±0.00”; R6: p.2, “0.00±0.00”; R28: p.5, “0.00”; R42: p.5, “0.00±0.00”; R51: p.5, “76.38±0.00”; R58: p.5, “0.00±0.00”; R65: p.5, “76.39±0.00”; R70: p.5, “76.08±0.00”; R71: p.5, “76.36±0.00”; R133: p.5, “89.06±0.00”; R134: p.5, “89.03±0.00”; R138: p.5, “36.89±0.00”; R192: p.6, “0.00±0.00”; R232: p.6, “81.46±0.3”; R359: p.5, “81.51±0.19”; R361: p.5, “79.58±0.00”; R362: p.5, “81.54±0.00”; R368: p.5, “0.00±0.00”; R369: p.5, “7.29±0.00”; R379: p.5, “81.50±0.2”; R395: p.5, “81.54±0.24”; R397: p.5, “81.48±0.27”; R398: p.5, “81.46±0.26”; R465: p.5, “14.58±0.00”; R466: p.5, “24.05±0.00” | 76.39, 0.0, 0.0, 0.0, 76.38, 0.0, 76.39, 76.08, 76.36, 89.06, 89.03, 36.89, 0.0, 81.46, 81.51, 79.58, 81.54, 0.0, 7.29, 81.5, 81.54, 81.48, 81.46, 14.58, 24.05 | advisory: claim claim-1: attest[provenance] — provenance: 25 input(s) resolve to shipped, non-empty evidence. |
| claim-9 | Face unlearning on PINS: LFSSD achieves 0% Df accuracy with Dr 98.15 and MIA 0.38. | R6: p.2, “0.00±0.00”; R28: p.5, “0.00”; R39: p.5, “98.42±0.13”; R40: p.5, “98.15±0.20”; R42: p.5, “0.00±0.00”; R49: p.5, “1.11±0.01”; R50: p.5, “0.38±0.58”; R58: p.5, “0.00±0.00”; R192: p.6, “0.00±0.00”; R368: p.5, “0.00±0.00” | 0.0, 0.0, 98.42, 98.15, 0.0, 1.11, 0.38, 0.0, 0.0, 0.0 | advisory: claim claim-9: attest[provenance] — provenance: 10 input(s) resolve to shipped, non-empty evidence. |
| claim-10 | Random sample unlearning on Cifar10: LFSSD remains close to retrain model. | R4: p.2, “90.10±0.19”; R34: p.5, “98.52±0.02”; R121: p.5, “90.19±0.00”; R129: p.5, “90.10±0.19”; R151: p.5, “94.88±0.00”; R162: p.5, “90.07±0.09”; R265: p.6, “95.03±0.00”; R302: p.6, “98.54±0.00”; R329: p.6, “94.85±0.13”; R532: p.7, “90.21±0.10”; R533: p.7, “90.16±0.23”; R535: p.7, “89.82±2.30”; R542: p.7, “94.94±2.89”; R549: p.7, “73.86±6.33”; R551: p.7, “98.61±0.08”; R556: p.7, “98.53±0.27”; R563: p.7, “99.52” | 90.1, 98.52, 90.19, 90.1, 94.88, 90.07, 95.03, 98.54, 94.85, 90.21, 90.16, 89.82, 94.94, 73.86, 98.61, 98.53, 99.52 | advisory: claim claim-10: attest[provenance] — provenance: 17 input(s) resolve to shipped, non-empty evidence. |
| claim-7 | LFSSD has the same complexity as SSD and similar compute time in practice, far below retraining methods. |  |  | unverifiable: claim claim-7: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-4 | LFSSD is the first retraining-free unlearning method requiring only unlabelled forget samples. |  |  | unverifiable: claim claim-4: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-5 | LFSSD is lightweight, robust and more practically useful than predecessors. |  |  | unverifiable: claim claim-5: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-8 | Alpha sensitivity: performance drops for too aggressive/conservative alpha but there is a wide plateau of good performance. | R26: p.5, “26.60”; R28: p.5, “0.00”; R33: p.5, “29.40”; R42: p.5, “0.00±0.00”; R557: p.4, “16.87”; R558: p.4, “74.72”; R559: p.4, “75.67”; R560: p.4, “76.10”; R561: p.4, “76.32”; R562: p.4, “71.88” | 26.6, 0.0, 29.4, 0.0, 16.87, 74.72, 75.67, 76.1, 76.32, 71.88 | advisory: claim claim-8: attest[provenance] — provenance: 10 input(s) resolve to shipped, non-empty evidence. |
| claim-6 | LFSSD shares SSD's limitation of needing alpha and lambda tuned to balance forgetting and performance. |  |  | unverifiable: claim claim-6: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-11 | Evaluation uses ResNet18 and ViT on full class, subclass and random forgetting with 10 repeated runs. |  |  | unverifiable: claim claim-11: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |

## All judge checks

`unassessable` and `unverifiable` mostly mean the paper-only artifact has nothing to
check (no code, traces, or checksums); they are coverage notes, not failures.

### verified (3)

| Check | Finding |
|-------|---------|
| `structure/paper` | paper present at paper.pdf. |
| `provenance/generated-marker` | manifest.yml carries its generated marker. |
| `provenance/claims` | authored input claims.yml present and ledgered. |

### advisory (4)

| Check | Finding |
|-------|---------|
| `claim_validators/claim-1.v1` | claim claim-1: attest[provenance] — provenance: 25 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-9.v1` | claim claim-9: attest[provenance] — provenance: 10 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-10.v1` | claim claim-10: attest[provenance] — provenance: 17 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-8.v1` | claim claim-8: attest[provenance] — provenance: 10 input(s) resolve to shipped, non-empty evidence. |

### unverifiable (8)

| Check | Finding |
|-------|---------|
| `structure/readme` | no standalone usage doc declared — documentation completeness is unassessable (usage guidance is expected in the paper and experiment dirs). |
| `structure/dependencies` | no dependencies declared — Functional reproducibility is at risk. |
| `claim_validators/claim-7.v1` | claim claim-7: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-4.v1` | claim claim-4: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-5.v1` | claim claim-5: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-6.v1` | claim claim-6: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-11.v1` | claim claim-11: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `provenance/reflection` | optional input reflection.md not shipped — nothing to audit (coverage note). |

### unassessable (10)

| Check | Finding |
|-------|---------|
| `structure/experiments` | no experiments registered — the artifact runs nothing (paper-origin / described-only); reproduction is unassessable, not a failure. |
| `paper_consistency/unassessable` | harvested 556 reported number(s) from paper.pdf (pypdf, 7 page(s)), but the artifact declares no shipped evidence to cross-check against (paper-origin / described-only) — paper↔data consistency is unassessable, not a failure. |
| `provenance/checksums` | No SHA256SUMS declaration; shipped checksum integrity unassessed. |
| `assessments/execution_authenticity` | execution authenticity is unassessable: no trace was declared, so whether the reported work actually ran cannot be judged (coverage note, not a failure). |
| `assessments/execution_authenticity/provenance_journal` | provenance journal is unassessable: no journal.yml was declared, so the narrated edit history cannot be reviewed (optional; coverage note, not a failure). |
| `assessments/trace_report_faithfulness` | trace-report faithfulness is unassessable: no trace was declared to reconcile against the paper's account (coverage note, not a failure). |
| `assessments/citation_integrity` | citation integrity is unassessable: no references export was shipped to check citations against (coverage note, not a failure). |
| `assessments/related_work_validity` | related-work validity is unassessable: a paper was read (from pdf) but no related-work section could be located to analyze (coverage note, not a failure). A future SDK related_work_export would remove the extraction ambiguity. |
| `assessments/limitation_transparency` | limitation transparency is unassessable: no reflection.md was shipped (optional; coverage note, not a failure). |
| `assessments/agent_faithfulness` | agent faithfulness is unassessable: no research-agent.md was shipped (optional; coverage note, not a failure). |
