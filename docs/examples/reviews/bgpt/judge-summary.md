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

The paper adapter automatically extracted **18** claims and **36** reported numbers.
Every number is linked to at least one claim.
8 claims cite no reported number, so the judge marks them `unverifiable`.
Extraction is heuristic and can be wrong: a claim may be a table row read as text. The
reviewer's analysis of the paper's broader claims is in [`review-draft.md`](review-draft.md).

| Claim | Statement | Evidence (paper) | Reported value | Judge verdict |
|-------|-----------|------------------|----------------|---------------|
| claim-1 | bGPT achieves 0.0011 BPB on MIDI when converting ABC notation to MIDI, near-perfect. | R65: p.8, “0.0011”; R69: p.0, “0.2381” | 0.0011, 0.2381 | advisory: claim claim-1: attest[provenance] — provenance: 2 input(s) resolve to shipped, non-empty evidence. |
| claim-2 | bGPT simulates CPU behaviour with accuracy exceeding 99.99%. | R2: p.1, “99.99%”; R70: p.0, “99.9702” | 99.99, 99.9702 | advisory: claim claim-2: attest[provenance] — provenance: 2 input(s) resolve to shipped, non-empty evidence. |
| claim-3 | bGPT matches specialized models across text, audio and images. |  |  | unverifiable: claim claim-3: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-4 | bGPTwiki gets 1.0639 BPB and 92.49% on AG News vs GPT2-small 0.9237 BPB and 94.50%. | R9: p.6, “92.43”; R10: p.6, “1.0639”; R11: p.6, “92.49”; R40: p.6, “0.9237”; R41: p.6, “94.50”; R44: p.6, “1.0639”; R45: p.6, “92.49%”; R46: p.6, “0.9237” | 92.43, 1.0639, 92.49, 0.9237, 94.5, 1.0639, 92.49, 0.9237 | advisory: claim claim-4: attest[provenance] — provenance: 8 input(s) resolve to shipped, non-empty evidence. |
| claim-5 | bGPTlibri reaches 96.03% on Speech Commands v2 vs AST 98.11%. | R48: p.6, “96.03%”; R71: p.6, “96.03”; R72: p.6, “98.11” | 96.03, 96.03, 98.11 | advisory: claim claim-5: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| claim-15 | CPU state modelling BPB drops sharply from bGPT4 to bGPT5 with diminishing returns beyond. | R60: p.7, “0.6924”; R61: p.7, “27.2404”; R62: p.7, “0.0969” | 0.6924, 27.2404, 0.0969 | advisory: claim claim-15: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| claim-16 | bGPT5 shows a sudden improvement around epoch 11, an emergent ability in CPU modelling. |  |  | unverifiable: claim claim-16: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-6 | bGPTimage lags ViT on CIFAR-10 (88.69% vs 98.13%). | R50: p.?, “88.69%”; R73: p.0, “88.69”; R74: p.0, “98.13” | 88.69, 88.69, 98.13 | advisory: claim claim-6: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| claim-18 | bGPT is effective in digital media modelling with modality-agnostic knowledge transfer. |  |  | unverifiable: claim claim-18: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-10 | On spectrogram Speech Commands, bGPTlibri achieves higher accuracy than bGPTimage, showing content alignment matters over format. | R5: p.6, “84.74”; R55: p.7, “80.74”; R57: p.7, “84.66”; R59: p.7, “85.26” | 84.74, 80.74, 84.66, 85.26 | advisory: claim claim-10: attest[provenance] — provenance: 4 input(s) resolve to shipped, non-empty evidence. |
| claim-13 | BPB for both conversion directions decreases significantly with data scale. | R75: p.8, “0.2796”; R76: p.8, “0.1751”; R77: p.8, “0.1341”; R78: p.8, “1.1227”; R79: p.8, “0.1763”; R80: p.8, “0.0789” | 0.2796, 0.1751, 0.1341, 1.1227, 0.1763, 0.0789 | advisory: claim claim-13: attest[provenance] — provenance: 6 input(s) resolve to shipped, non-empty evidence. |
| claim-7 | Pre-training matched to the fine-tuning domain yields better downstream performance. |  |  | unverifiable: claim claim-7: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-8 | Mixed-modality pre-trained models perform around the average of single-modality models. | R34: p.6, “1.0935”; R35: p.6, “91.75”; R52: p.6, “1.0935” | 1.0935, 91.75, 1.0935 | advisory: claim claim-8: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| claim-9 | Cross-modal fine-tuning shows positive transfer between audio and images but negative transfer between text and other modalities. |  |  | unverifiable: claim claim-9: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-12 | Larger data scale gives lower starting loss and faster convergence in data conversion. |  |  | unverifiable: claim claim-12: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-11 | bGPTimage and bGPTlibri have closely matched BPB on spectrograms. | R56: p.7, “0.3899”; R58: p.7, “0.3900” | 0.3899, 0.39 | advisory: claim claim-11: attest[provenance] — provenance: 2 input(s) resolve to shipped, non-empty evidence. |
| claim-14 | BPB for ABC is consistently higher than MIDI in both directions. |  |  | unverifiable: claim claim-14: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| claim-19 | Models are 110M parameters trained without hyperparameter tuning or data augmentation. |  |  | unverifiable: claim claim-19: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |

## All judge checks

`unassessable` and `unverifiable` mostly mean the paper-only artifact has nothing to
check (no code, traces, or checksums); they are coverage notes, not failures.

### verified (3)

| Check | Finding |
|-------|---------|
| `structure/paper` | paper present at paper.pdf. |
| `provenance/generated-marker` | manifest.yml carries its generated marker. |
| `provenance/claims` | authored input claims.yml present and ledgered. |

### advisory (10)

| Check | Finding |
|-------|---------|
| `claim_validators/claim-1.v1` | claim claim-1: attest[provenance] — provenance: 2 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-2.v1` | claim claim-2: attest[provenance] — provenance: 2 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-4.v1` | claim claim-4: attest[provenance] — provenance: 8 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-5.v1` | claim claim-5: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-15.v1` | claim claim-15: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-6.v1` | claim claim-6: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-10.v1` | claim claim-10: attest[provenance] — provenance: 4 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-13.v1` | claim claim-13: attest[provenance] — provenance: 6 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-8.v1` | claim claim-8: attest[provenance] — provenance: 3 input(s) resolve to shipped, non-empty evidence. |
| `claim_validators/claim-11.v1` | claim claim-11: attest[provenance] — provenance: 2 input(s) resolve to shipped, non-empty evidence. |

### unverifiable (12)

| Check | Finding |
|-------|---------|
| `structure/readme` | no standalone usage doc declared — documentation completeness is unassessable (usage guidance is expected in the paper and experiment dirs). |
| `structure/dependencies` | no dependencies declared — Functional reproducibility is at risk. |
| `claim_validators/claim-3.v1` | claim claim-3: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-16.v1` | claim claim-16: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-18.v1` | claim claim-18: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-7.v1` | claim claim-7: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-9.v1` | claim claim-9: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-12.v1` | claim claim-12: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-14.v1` | claim claim-14: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `claim_validators/claim-19.v1` | claim claim-19: attest[provenance] could not be established — no inputs declared to attest (integrity flag; never a silent pass). |
| `provenance/reflection` | optional input reflection.md not shipped — nothing to audit (coverage note). |
| `assessments/citation_integrity` | citation integrity: 51/58 exported reference(s) carry an existence-checkable identifier; 7 lack one, so their existence cannot be machine-verified (advisory flag, never a failure). |

### unassessable (9)

| Check | Finding |
|-------|---------|
| `structure/experiments` | no experiments registered — the artifact runs nothing (paper-origin / described-only); reproduction is unassessable, not a failure. |
| `paper_consistency/unassessable` | harvested 68 reported number(s) from paper.pdf (pypdf, 19 page(s)), but the artifact declares no shipped evidence to cross-check against (paper-origin / described-only) — paper↔data consistency is unassessable, not a failure. |
| `provenance/checksums` | No SHA256SUMS declaration; shipped checksum integrity unassessed. |
| `assessments/execution_authenticity` | execution authenticity is unassessable: no trace was declared, so whether the reported work actually ran cannot be judged (coverage note, not a failure). |
| `assessments/execution_authenticity/provenance_journal` | provenance journal is unassessable: no journal.yml was declared, so the narrated edit history cannot be reviewed (optional; coverage note, not a failure). |
| `assessments/trace_report_faithfulness` | trace-report faithfulness is unassessable: no trace was declared to reconcile against the paper's account (coverage note, not a failure). |
| `assessments/related_work_validity` | related-work validity is unassessable: a paper was read (from pdf) but no related-work section could be located to analyze (coverage note, not a failure). A future SDK related_work_export would remove the extraction ambiguity. |
| `assessments/limitation_transparency` | limitation transparency is unassessable: no reflection.md was shipped (optional; coverage note, not a failure). |
| `assessments/agent_faithfulness` | agent faithfulness is unassessable: no research-agent.md was shipped (optional; coverage note, not a failure). |

## Contribution declaration notes

- `contributions[3].supporting_claims` (warning): claim support not declared or inferred
