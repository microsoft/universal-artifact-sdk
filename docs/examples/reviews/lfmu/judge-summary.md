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

The paper adapter automatically extracted **10** claims and **79** reported numbers.
Every number is linked to at least one claim.
7 claims cite no reported number, so the judge marks them `unverifiable`.
Extraction is heuristic and can be wrong: a claim may be a table row read as text. The
reviewer's analysis of the paper's broader claims is in [`review-draft.md`](review-draft.md).

| Claim | Statement | Evidence (paper) | Reported value | Judge verdict |
|-------|-----------|------------------|----------------|---------------|
| claim-2 | LFSSD produces scores similar to a model retrained on only Dr and is competitive with SSD. | R1: p.2, “76.39±0.00”; R2: p.2, “72.89±0.34”; R4: p.2, “90.10±0.19”; R6: p.2, “0.00±0.00”; R10: p.2, “95.60±0.00”; R13: p.2, “81.81±0.19”; R14: p.2, “95.77±0.00”; R15: p.2, “94.69±0.13”; R17: p.2, “22.95±4.72”; R19: p.2, “34.55±8.62”; R28: p.5, “0.00”; R42: p.5, “0.00±0.00”; R51: p.5, “76.38±0.00”; R58: p.5, “0.00±0.00”; R65: p.5, “76.39±0.00”; R66: p.5, “72.89±0.34”; R70: p.5, “76.08±0.00”; R71: p.5, “76.36±0.00”; R79: p.5, “72.90±0.45”; R90: p.5, “72.83±0.42”; R102: p.5, “72.83±0.54”; R121: p.5, “90.19±0.00”; R129: p.5, “90.10±0.19”; R133: p.5, “89.06±0.00”; R134: p.5, “89.03±0.00”; R138: p.5, “36.89±0.00”; R139: p.5, “95.60±0.00”; R146: p.5, “90.02±0.22”; R162: p.5, “90.07±0.09”; R168: p.5, “94.70±0.00”; R192: p.6, “0.00±0.00”; R232: p.6, “81.46±0.3”; R258: p.6, “95.73±0.00”; R259: p.6, “94.71±0.14”; R278: p.6, “95.71±0.00”; R295: p.6, “95.54±0.00”; R301: p.6, “95.50±0.00”; R313: p.6, “95.59±0.00”; R318: p.6, “95.64±0.00”; R337: p.5, “72.94±0.82”; R357: p.5, “81.81±0.19”; R359: p.5, “81.51±0.19”; R361: p.5, “79.58±0.00”; R362: p.5, “81.54±0.00”; R364: p.5, “22.95±4.72”; R368: p.5, “0.00±0.00”; R369: p.5, “7.29±0.00”; R379: p.5, “81.50±0.2”; R395: p.5, “81.54±0.24”; R397: p.5, “81.48±0.27”; R398: p.5, “81.46±0.26”; R433: p.5, “95.69±0.00”; R438: p.5, “95.54±0.00”; R454: p.5, “95.77±0.00”; R455: p.5, “94.69±0.13”; R459: p.5, “95.68±0.00”; R461: p.5, “34.55±8.62”; R465: p.5, “14.58±0.00”; R466: p.5, “24.05±0.00”; R474: p.5, “94.60±0.13”; R478: p.5, “95.51±0.00”; R479: p.5, “95.66±0.00”; R493: p.5, “95.73±0.00”; R494: p.5, “94.61±0.13”; R511: p.5, “95.67±0.00”; R516: p.5, “95.57±0.00”; R533: p.7, “90.16±0.23” | 76.39, 72.89, 90.1, 0.0, 95.6, 81.81, 95.77, 94.69, 22.95, 34.55, 0.0, 0.0, 76.38, 0.0, 76.39, 72.89, 76.08, 76.36, 72.9, 72.83, 72.83, 90.19, 90.1, 89.06, 89.03, 36.89, 95.6, 90.02, 90.07, 94.7, 0.0, 81.46, 95.73, 94.71, 95.71, 95.54, 95.5, 95.59, 95.64, 72.94, 81.81, 81.51, 79.58, 81.54, 22.95, 0.0, 7.29, 81.5, 81.54, 81.48, 81.46, 95.69, 95.54, 95.77, 94.69, 95.68, 34.55, 14.58, 24.05, 94.6, 95.51, 95.66, 95.73, 94.61, 95.67, 95.57, 90.16 | advisory: claim claim-2: attest[provenance] — provenance: 67 input(s) resolve to shipped, non-empty evidence. |
| claim-3 | Loss-free sensitivity-based parameter dampening is as effective as Fisher information without labelled data. |  |  | unverifiable: claim claim-3: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-11 | Face unlearning results on PINS for LFSSD vs baselines. | R6: p.2, “0.00±0.00”; R28: p.5, “0.00”; R39: p.5, “98.42±0.13”; R40: p.5, “98.15±0.20”; R42: p.5, “0.00±0.00”; R49: p.5, “1.11±0.01”; R50: p.5, “0.38±0.58”; R58: p.5, “0.00±0.00”; R192: p.6, “0.00±0.00”; R368: p.5, “0.00±0.00” | 0.0, 0.0, 98.42, 98.15, 0.0, 1.11, 0.38, 0.0, 0.0, 0.0 | advisory: claim claim-11: attest[provenance] — provenance: 10 input(s) resolve to shipped, non-empty evidence. |
| claim-8 | LFSSD performance drops sharply at too aggressive/conservative alpha but has a wide well-performing plateau. | R26: p.5, “26.60”; R33: p.5, “29.40”; R557: p.4, “16.87”; R558: p.4, “74.72”; R559: p.4, “75.67”; R560: p.4, “76.10”; R561: p.4, “76.32”; R562: p.4, “71.88” | 26.6, 29.4, 16.87, 74.72, 75.67, 76.1, 76.32, 71.88 | advisory: claim claim-8: attest[provenance] — provenance: 8 input(s) resolve to shipped, non-empty evidence. |
| claim-9 | LFSSD has similar compute time to SSD. |  |  | unverifiable: claim claim-9: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-4 | LFSSD is the first retraining-free unlearning method requiring only unlabelled forget samples. |  |  | unverifiable: claim claim-4: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-5 | LFSSD is lightweight, robust and more practically useful than predecessors. |  |  | unverifiable: claim claim-5: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-7 | Like SSD, LFSSD depends on choosing alpha and lambda to balance forgetting and performance. |  |  | unverifiable: claim claim-7: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-10 | Retraining-based methods cost O(N·b_retain·p), much larger than SSD/LFSSD. |  |  | unverifiable: claim claim-10: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-6 | Evaluation uses ResNet18 and Vision Transformer. |  |  | unverifiable: claim claim-6: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |

## All judge checks

`unassessable` and `unverifiable` mostly mean the paper-only artifact has nothing to
check (no code, traces, or checksums); they are coverage notes, not failures.

### verified (3)

| Check | Finding |
|-------|---------|
| `structure/paper` | paper present at paper.pdf. |
| `provenance/generated-marker` | manifest.yml carries its generated marker. |
| `provenance/claims` | authored input claims.yml present and ledgered. |

### advisory (3)

| Check | Finding |
|-------|---------|
| `claim_validators/claim-2.v1` | claim claim-2: attest[provenance] — provenance: 67 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-11.v1` | claim claim-11: attest[provenance] — provenance: 10 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-8.v1` | claim claim-8: attest[provenance] — provenance: 8 input(s) resolve to shipped, non-empty evidence. |

### unverifiable (10)

| Check | Finding |
|-------|---------|
| `structure/readme` | no standalone usage doc declared — documentation completeness is unassessable (usage guidance is expected in the paper and experiment dirs). |
| `structure/dependencies` | no dependencies declared — Functional reproducibility is at risk. |
| `claim_validators/claim-3.v1` | claim claim-3: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-9.v1` | claim claim-9: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-4.v1` | claim claim-4: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-5.v1` | claim claim-5: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-7.v1` | claim claim-7: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-10.v1` | claim claim-10: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-6.v1` | claim claim-6: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
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
