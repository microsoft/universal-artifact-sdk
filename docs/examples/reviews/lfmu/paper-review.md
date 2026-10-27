> [!WARNING]
> **Experimental, AI-generated example. No human judgement.** This review was produced
> automatically by an experimental reference implementation of the judge/reviewer
> specification. No person reviewed, edited, or endorsed it. It does not represent the
> opinion of the SDK maintainers, Microsoft, or any reviewer, and it is not an assessment of
> the paper or its authors. It may contain errors. It is published only to show what the
> tool's output looks like.

# Academic Review Draft

> **AI-generated draft** by `reference-reviewer` - a human reviewer must verify, edit, and own the submitted review.

**Submission:** paper
**Venue profile:** `generic-computing/v2`

## Human-owned assessment

- Overall recommendation: unset
- Criterion scores: unset
- Reviewer confidence: unset

These belong to the human reviewer; the tool never sets them. Venue scales: scores human-owned; confidence human-owned.

## Contribution summary

The paper proposes LFSSD, a variant of Selective Synaptic Dampening (SSD) that replaces the diagonal of the Fisher information matrix with the gradient of the squared l2 norm of the model output, a sensitivity estimate taken from Aljundi et al. (2018). SSD's parameter-selection and dampening rule is otherwise kept. As a result, unlearning needs neither retraining nor labels, only the unlabelled forget samples. Experiments cover full-class, subclass, random-sample and face unlearning on ResNet and ViT models, with comparisons to SSD, retraining and other baselines.

## Contributions

1. **Loss-Free Selective Synaptic Dampening (LFSSD) unlearning method.** An extension of Selective Synaptic Dampening that unlearns without retraining and without loss or ground-truth labels, requiring only the unlabelled forget samples at forgetting time.
   *Claim support: unresolved · Significance: unassessed · Originality: contested*
2. **Output-norm gradient sensitivity replacing Fisher information importance.** Parameter importance in SSD is estimated from the gradient of the squared l2 norm of the model output, a sensitivity measure from continual learning, instead of the Fisher information diagonal.
   *Claim support: unresolved · Significance: unassessed · Originality: unresolved*
3. **Empirical evaluation on ResNet18 and Vision Transformer.** Evaluation of LFSSD across full-class, subclass, and random forgetting on CIFAR and face data, comparing against retraining, finetuning, and state-of-the-art unlearning baselines.
   *Claim support: unresolved · Significance: unassessed · Originality: unassessed*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: Loss-Free Selective Synaptic Dampening (LFSSD) unlearning method

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- LFSSD is positioned as an extension of SSD that swaps the Fisher-diagonal importance for the output-norm sensitivity of Aljundi et al. (2018). Both components are prior work, so the novelty lies in combining them and in the label-free setting it enables.
- The authors present LFSSD as an extension of their own SSD that borrows MAS-style sensitivity from continual learning. The novelty claimed is the transfer to unlearning and the label-free setting, not a new importance estimator.
- The authors present originality as a novel extension of their own SSD, transferring the Aljundi et al. sensitivity measure to unlearning. They claim a 'first' that is qualified as 'to the best of our knowledge'.
- The 'first label-free, retraining-free' claim is hedged in the introduction but stated unhedged in the conclusion. The paper also cites zero-shot unlearning without explaining how it differs in data or label requirements.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/4392-6820, paper:chars/6820-7514

Paper’s wording: “Therefore, we propose a novel extension of SSD that does not require access to the loss or ground truth labels, which we refer to as Loss-Free Selective Synaptic Dampening (LFSSD).”

### Contribution 2: Output-norm gradient sensitivity replacing Fisher information importance

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The authors present the advance as combining two existing pieces: SSD (their own prior method) and the Memory Aware Synapses sensitivity measure (Aljundi et al.). The novelty is the application of that measure to unlearning, not a new importance measure.
- The output-norm sensitivity measure is explicitly taken from Aljundi et al. (2018); the new element is its use as a replacement for the FIM in SSD.
- The output-norm sensitivity substitution is explicitly borrowed from continual learning. Its originality is limited to applying it in the unlearning setting.
- The importance estimator itself is credited to Aljundi et al. (2018), so it is not novel. The novelty is its application within SSD for unlearning.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/4392-6820

Paper’s wording: “substituting the diagonal of the Fisher information matrix for the gradient of the l2 norm of the model output to approximate sensitivity”

### Contribution 3: Empirical evaluation on ResNet18 and Vision Transformer

**Claim support: unresolved**
- No claims are linked to this contribution.
- The appendix tables broadly support the claim that LFSSD is competitive with SSD and the other baselines. However, LFSSD's forget-set (Df) accuracy sometimes diverges substantially from the retrained model in both directions.
- Within the reported benchmarks, LFSSD is broadly comparable to SSD and the other baselines, supporting 'competitive'. However, 'equally effective as Fisher information' and 'robust' overstate mixed results.
- Tables support the claim that LFSSD is competitive with SSD in class unlearning. For example, on ViT lamp LFSSD reaches Df 0.00 where SSD leaves 36.89.
- Some results depart from the retrain reference, so the claim that LFSSD's scores are 'similar to that of a model trained on only Dr' needs qualifying. In subclass unlearning LFSSD sometimes over-forgets (RN sea Df 18.06 vs retrain 91.47). LFSSD's α is also tuned per task while SSD's values are reused from prior work.
- The 'competitive with SOTA' claim is broadly supported across full-class, subclass, random and face tasks. However, ViT subclass forgetting is mixed, and the 'equally effective as Fisher' wording overstates this.
- Sources: paper:chars/7514-23701, paper:chars/4392-6820, paper:chars/1165-4392, paper:chars/6820-7514

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “We evaluate our method in a range of experiments using ResNet18 and Vision Transformer. Results show our label-free method is competitive with existing state-of-the-art approaches.”

<details><summary>What the authors say is original (6 statements)</summary>

Authors' stated position:
- [claims] “ABSTRACT We present a machine unlearning approach that is both retraining- and label-free.”
- [claims] “Thus, we present an extension to the Selective Synaptic Dampening algorithm, substituting the diagonal of the Fisher information matrix for the gradient of the l2 norm of the model output to approximate sensitivity.”
- [claims] “Therefore, we propose a novel extension of SSD that does not require access to the loss or ground truth labels, which we refer to as Loss-Free Selective Synaptic Dampening (LFSSD).”
- [claims; positioned against Aljundi et al.,
2018] “Here, we show this new approach to dampening important parameters is equally effective as Fisher information, without relying on labelled data.”
- [claims; positioned against Feb 2024, ICLR 2024, Aljundi et al.,
2018] “To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only the unlabelled forget samples at forgetting time. 1 arXiv:2402.19308v1 [cs.LG] 29 Feb 2024 Accepted as a Tiny Paper at ICLR 2024 (Preprint) Table 1: Full- (class lamp) and subclass (lamp is part of electrical devices) unlearning with α =10, λ =1 on Cifar100/20.”
- [claims] “In this work, we presented a novel extension of existing literature that is the first retraining free machine unlearning method to require only the unlabelled input samples for the forget set.”

</details>


## Reasons to accept

1. **LFSSD is positioned as an extension of SSD that swaps the Fisher-diagonal importance for the output-norm sensitivity of Aljundi et al. (2018). Both components are prior work, so the novelty lies in combining them and in the label-free setting it enables.**
   The paper attributes the estimator to prior work rather than claiming it as new. This is consistent with an 'extension' framing. Whether the estimator has truly not been used in unlearning before is author-reported and not verified here.
   Evidence status: inference.
   Reasoning: The authors say the importance estimator comes from Aljundi et al. They also say the SSD selection rule (Eq. 1) is reused. The original element is therefore the transfer of this estimator into unlearning, which removes the need for labels. This is a modest but clearly stated delta, appropriate to a tiny-paper scope.
   Source `paper:chars/1165-4392`: Such importance estimation has been shown to be effective in continual learning (Aljundi et al.,
2018), yet it has not been applied in unlearning.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)

2. **The authors present LFSSD as an extension of their own SSD that borrows MAS-style sensitivity from continual learning. The novelty claimed is the transfer to unlearning and the label-free setting, not a new importance estimator.**
   The novelty is incremental but clearly positioned. The 'first' claim is hedged by 'to the best of our knowledge'.
   Evidence status: inference.
   Reasoning: The first quote concedes that the estimator comes from prior work, so the originality lies in combining it with SSD and in the resulting label-free capability. That framing is consistent across the paper. Whether no prior retraining-free label-free method exists (e.g., relative to the authors' account of zero-shot unlearning, Chundawat et al. 2023b) is author-reported and was not verified here.
   Source `paper:chars/1165-4392`: Such importance estimation has been shown to be effective in continual learning (Aljundi et al.,
2018), yet it has not been applied in unlearning.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.

3. **The paper proposes LFSSD, a variant of Selective Synaptic Dampening (SSD) that replaces Fisher-information importance with the gradient of the squared l2 norm of the model output. This makes unlearning both retraining-free and label-free.**
   This is a simple, practically motivated tiny-paper contribution. It addresses settings where labels are unavailable, such as copyrighted-data catalogues and semi-supervised models.
   Evidence status: observation.
   Reasoning: The abstract and introduction state the substitution directly. They also state the practical benefit: only unlabelled forget samples are needed at forgetting time.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.

4. **Tiny paper proposing LFSSD: SSD with Fisher-diagonal importance replaced by the gradient magnitude of the squared l2 norm of the model output, so unlearning needs neither retraining nor labels.**
   The contribution is a targeted, simple substitution within an existing algorithm, appropriate to the tiny-paper format.
   Evidence status: observation.
   Reasoning: The quotes state the single method change and its source.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)

## Originality

The originality is incremental but clearly positioned. The authors credit the importance estimator to prior continual-learning work (Aljundi et al., 2018) and reuse the SSD selection rule. The new element is moving this estimator into unlearning and the label-free capability that follows. This is a modest, honestly attributed change that suits a tiny-paper scope. The claim to be the first retraining-free, label-free method is hedged in the introduction ('to the best of our knowledge') but stated without the hedge in the conclusion. The paper also cites zero-shot machine unlearning (Chundawat et al., 2023b) only within a list of retraining-based methods and never says how its label or data requirements differ. The primacy claim therefore cannot yet be checked against the paper's own citations. This review has not verified that cited work.

## Likely impact

Practitioners who must remove data whose labels are unavailable could benefit, for example in copyrighted-data catalogues or semi-supervised models. The method is simple, lightweight and easy to adopt for anyone already using SSD. Several factors may limit its influence. The method is a small change to an existing algorithm. Its results are competitive rather than uniformly equal to SSD. Most importantly, it is unclear how α would be chosen in a truly label-free deployment, since the per-task tuning described appears to depend on accuracy on Dr and a retrained reference. If those require labels, the practical label-free benefit is qualified, although the importance estimate itself remains label-free.

## Decision-critical concerns

1. **The appendix tables broadly support the claim that LFSSD is competitive with SSD and the other baselines. However, LFSSD's forget-set (Df) accuracy sometimes diverges substantially from the retrained model in both directions.**
   The headline claim that LFSSD is 'equally effective as Fisher information' holds on average but not uniformly across settings.
   Evidence status: inference.
   Reasoning: The authors set similarity to the retrained model as the success criterion. In ViT subclass 'sea', LFSSD's Df accuracy is 20.83 versus 95.12 for the retrained model, which is over-forgetting by that criterion. In ViT subclass 'baby', MIA is 1.6 for LFSSD versus 77.37 for retraining.
   Source `paper:chars/4392-6820`: Similarity to the retrained model is necessary, as ”over-forgetting” can
lead to the Streisand effect
   Source `paper:chars/7514-23701`: Df 96.44±0.00 93.23±1.09 85.45±4.47 46.66±17.88 38.76±7.36 94.10±0.00 86.81±0.00
   Source `paper:chars/7514-23701`: Df 99.22±0.00 95.12±0.81 89.17±4.17 25.97±14.01 21.42±8.5 97.05±0.00 20.83±0.00
   - **Why this affects the decision:** The claim of matching SSD/Fisher effectiveness is central to the contribution.
   - **Actionable revision:** Report an aggregate distance-to-retrain metric across tasks for both SSD and LFSSD. Discuss the over-forgetting cases explicitly.
   - **What would resolve it:** A summary showing LFSSD's gap to retrain is comparable to SSD's, or a scoped claim.

2. **The primacy claim is hedged in the introduction but stated unhedged in the results and conclusion. It also sits beside a citation of 'Zero-shot machine unlearning' (Chundawat 2023b) that is never contrasted.**
   I have not inspected the cited work; any difference from it is unresolved.
   Evidence status: inference.
   Reasoning: The introduction qualifies the claim with 'To the best of our knowledge', but the conclusion drops that hedge. The paper cites a zero-shot unlearning method only within a group of retraining-based approaches. It never says how that method's data requirements differ, for example whether it needs class labels. Without that comparison, the primacy claim cannot be checked against the paper's own citations.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.
   Source `paper:chars/6820-7514`: is the first retraining free
machine unlearning method to require only the unlabelled input samples for the forget set
   Source `paper:chars/7514-23701`: Zero-shot machine
unlearning. IEEE Transactions on Information Forensics and Security, 2023b.
   - **Why this affects the decision:** Primacy is the paper's headline originality claim.
   - **Actionable revision:** Add one sentence explaining what Chundawat 2023b and FisherForgetting require (labels, retain data, retraining). Restore the hedge in the conclusion.
   - **What would resolve it:** An explicit comparison showing that the prior zero-shot method needs labels or retraining.

3. **Within the reported benchmarks, LFSSD is broadly comparable to SSD and the other baselines, supporting 'competitive'. However, 'equally effective as Fisher information' and 'robust' overstate mixed results.**
   The wording of the central empirical claim is stronger than the tables show.
   Evidence status: inference.
   Reasoning: In the ViT MR subclass row, LFSSD's Df is 31.42 versus SSD's 6.68. In the ViT Rkt class row, LFSSD's MIA is 10.60 versus SSD's 1.80. LFSSD wins in some other cells (e.g. ViT sea subclass), so the results are mixed rather than equivalent. No aggregate or statistical comparison is given, and per-task alpha was tuned.
   Source `paper:chars/1165-4392`: is equally effective as Fisher information, without relying on labelled data
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   Source `paper:chars/7514-23701`: MIA 94.40±0.00 3.23±0.00 19.00±0.09 0.03±0.00 1.00±0.01 1.80±0.00 10.60±0.00
   Source `paper:chars/6820-7514`: LFSSD is lightweight, robust and more practically useful than its predecessors
   - **Why this affects the decision:** The paper's value rests on matching SSD without labels, so this claim needs calibration.
   - **Actionable revision:** Report averaged Dr, Df, and MIA gaps (or |metric − retrain|) for LFSSD versus SSD per setting. Soften 'equally effective'/'robust' to 'competitive, with case-dependent differences', and discuss the ViT failure cases.
   - **What would resolve it:** An aggregate table showing small mean gaps, or revised wording that matches the results.

4. **Some results depart from the retrain reference, so the claim that LFSSD's scores are 'similar to that of a model trained on only Dr' needs qualifying. In subclass unlearning LFSSD sometimes over-forgets (RN sea Df 18.06 vs retrain 91.47). LFSSD's α is also tuned per task while SSD's values are reused from prior work.**
   The overall 'similar to retrain' framing should be scoped to the settings where it holds.
   Evidence status: inference.
   Reasoning: Where the retrain reference retains the subclass, driving Df to 18% is over-forgetting, which the paper itself says risks the Streisand effect. Separately, tuning α only for LFSSD may favor it in the SSD comparison.
   Source `paper:chars/7514-23701`: Df 96.27±0.00 91.47±1.92 82.69±7.17 75.13±4.12 46.78±8.55 75.35±0.00 18.06±0.00
   Source `paper:chars/4392-6820`: The results show that LFSSD produces scores similar to that of a model trained
on only Dr
   Source `paper:chars/7514-23701`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   - **Why this affects the decision:** These gaps affect how strongly the competitiveness claim is supported.
   - **Actionable revision:** Qualify the 'similar to retrain' claim for subclass settings, and report SSD under the same α search used for LFSSD.
   - **What would resolve it:** Revised wording plus a table comparing SSD and LFSSD under matched tuning.

## Questions for the authors

1. **Hyperparameters were chosen per unlearning task, and the alpha sensitivity is sharp at its extremes. Setting alpha without labels or a retrained reference is unaddressed.**
   Question: in a truly label-free deployment, how would alpha be selected?
   Evidence status: inference.
   Reasoning: Alpha differs by task (10, 5, 3.5), and alpha=1 collapses Dr accuracy to 16.87%. Tuning against Dr accuracy and a retrain reference needs labelled data, which may conflict with the label-free motivation.
   Source `paper:chars/7514-23701`: We pick one value per
unlearning task (e.g. full class, sub-class, random)
   Source `paper:chars/7514-23701`: 1 16.87% 0.00% 26.60
   Source `paper:chars/4392-6820`: A shared limitation with SSD is the reliance
on choosing α and λ values that balance forgetting and model performance.
   - **Why the answer matters:** If alpha selection requires labelled validation data, the practical label-free claim weakens. A label-free selection heuristic would strengthen it.
   - **Requested response:** Describe a label-free alpha selection procedure, or acknowledge that labelled validation is needed for tuning.
   - **Answer that would resolve it:** A procedure that uses no labels, or an explicit scope statement.

2. **SSD and LFSSD are reported with ±0.00 in Tables 5 and 6, while other unlearning methods show non-zero spread. The reported variance therefore does not reflect the same randomness for all methods.**
   The ±0.00 values suggest variance was computed only over stochastic components that SSD and LFSSD do not have.
   Evidence status: inference.
   Reasoning: In record 31 (Table 6, ViT lamp Df), SSD is 14.58±0.00 and LFSSD is 24.05±0.00, but the other methods have spreads of ±8.62, ±10.4 and ±7.05. Record 47 shows the same pattern for Table 5 ViT ED Df: SSD 53.53±0.00 and LFSSD 0.68±0.00, against ±0.22, ±3.75 and ±0.08 for the others. Zero spread suggests SSD and LFSSD were run deterministically on one fixed trained model, while the baselines varied across runs. If so, the error bars are not comparable. They also do not show how sensitive LFSSD is to the choice of original model, which matters when the margins are close.
   Source `review-record:visual/31`: In Table 6, ViT lamp Df shows SSD 14.58±0.00 and LFSSD 24.05±0.00. RN lamp Dr shows SSD 79.58 and LFSSD 81.54.
   Source `review-record:visual/47`: The rendered values match the extracted text. For example, the RN ED row reads 82.56±0.00 ... 83.19±0.00, and the ViT ED SSD Df value is 53.53±0.00.
   Source `paper:chars/22176-22253`: Df 89.58±0.00 34.55±8.62 16.90±10.4 8.23±7.05 0.59±1.45 14.58±0.00 24.05±0.00
   Source `paper:chars/19321-19395`: Df 95.03±0.00 0.00±0.00 0.28±0.22 4.14±3.75 0.03±0.08 53.53±0.00 0.68±0.00
   - **Why the answer matters:** Comparisons and significance against baselines depend on whether variance across trained models is captured.
   - **Requested response:** State what the ± values are computed over. Report SSD and LFSSD across several independently trained original models or seeds.
   - **Answer that would resolve it:** Per-seed results, or a clear statement of the protocol, with non-degenerate spread for SSD and LFSSD.

3. **Hyperparameters were chosen differently for the two methods. SSD's values come from prior Optuna tuning, while LFSSD's alpha comes from a separate per-task search, and the paper does not say which data split guided that search.**
   Table 2 shows strong sensitivity at the extremes of the alpha range (alpha=1 and alpha=50).
   Evidence status: observation.
   Reasoning: If alpha was selected using the test-time Df/Dr metrics, the comparison with SSD may be biased in LFSSD's favour.
   Source `paper:chars/7514-23701`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   - **Why the answer matters:** Selecting alpha on test metrics would weaken the competitiveness claim.
   - **Requested response:** State which data and which criterion were used to select alpha per task.
   - **Answer that would resolve it:** A description of the selection protocol showing it used held-out data.

## Decision synthesis

In favour: the contribution is simple, clearly motivated and honestly attributed. Across the appendix tables, LFSSD is broadly comparable to SSD and the other baselines on full-class, subclass, random and face tasks, which supports the claim that it is competitive. Against: several pieces of evidence matter most. (1) The wording of the central claims, 'equally effective as Fisher information', 'robust' and 'similar to a model trained on only Dr', goes beyond mixed per-setting results. In some subclass cells LFSSD over-forgets relative to the retrained model, which the paper itself treats as a Streisand-effect risk (e.g., ViT 'sea' Df 20.83 vs 95.12 retrained; RN 'sea' 18.06 vs 91.47). In other cells it forgets less than SSD (e.g., ViT mushroom Df 31.42 vs 6.68). (2) The two methods were tuned differently. SSD reuses α values from prior tuning, while LFSSD's α was chosen per task (10, 5, 3.5) through a simplified search whose guiding data split is not stated. Performance is sharply sensitive at the ends of the α range (α=1 drops Dr accuracy to 16.87%). (3) SSD and LFSSD are reported with ±0.00 while the other baselines show non-zero spread. This suggests, though it is not confirmed, that the two were run deterministically on one fixed model. If so, the error bars are not comparable and do not show sensitivity to the original model. Score-changing questions for the authors: how would α be selected without labels or a retrained reference? Which data guided the α search? What variance across trained models do SSD and LFSSD have? How does LFSSD differ from zero-shot unlearning (Chundawat et al., 2023b) in its requirements? Non-blocking improvements: restore the hedge on the primacy claim in the conclusion, soften the 'equally effective' and 'robust' wording, and limit the 'similar to retrain' framing to the settings where it holds.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The abstract states the problem, the mechanism, and the practical motivation in plain, compact prose.

**Writing-quality issues**

1. **The abstract's central result is vague: 'competitive with existing state-of-the-art approaches' gives no shape of the outcome or trade-off.**
   Readers cannot tell from the abstract whether the method matches SSD on retained accuracy, on forgetting, or on both.
   - **Suggested revision:** State the central result in one plain sentence in the abstract. For example, say that retained accuracy and attack scores match or approach SSD across the tasks, and name any task where they do not.

2. **The conclusion asserts qualities ('robust', 'more practically useful') rather than showing them, and the main-text results paragraph is similarly evaluative.**
   Linking 'robust' to the alpha plateau in the sensitivity analysis would let the evidence carry the claim.
   - **Suggested revision:** Tie 'robust' to the sensitivity analysis explicitly (stable over a range of alpha values), or drop it. Qualify 'more practically useful' with the specific scenario, such as a label-free forget set.

3. **Table 1 uses abbreviations (Dr, Df, MIA) before or without a nearby definition, and does not tell readers which direction is better.**
   A one-line caption note would make Table 1 self-contained.
   - **Suggested revision:** Add to the Table 1 caption that Dr should be high and that Df and MIA should resemble the retrain column.

## Additional improvements (non-blocking)

1. **The 'competitive with SOTA' claim is broadly supported across full-class, subclass, random and face tasks. However, ViT subclass forgetting is mixed, and the 'equally effective as Fisher' wording overstates this.**
   LFSSD's alpha was tuned per task with a simplified search, which may also affect the comparison.
   Evidence status: inference.
   Reasoning: Across most rows, LFSSD's Dr and Df scores are close to SSD's. In some subclass cases, though, LFSSD leaves Df higher than SSD (ViT mushroom: 31.42 vs 6.68). This means LFSSD is competitive overall but not uniformly equal to SSD.
   Source `paper:chars/1165-4392`: Df 72.66±0.00 22.95±4.72 7.29 0.00 89.58±0.00 34.55±8.62 24.05 14.58
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   - **Suggested revision:** Soften 'equally effective' to 'competitive' and discuss the ViT subclass gaps.

2. **The output-norm sensitivity measure is explicitly taken from Aljundi et al. (2018); the new element is its use as a replacement for the FIM in SSD.**
   Attribution is appropriate and the candidate is not overstated.
   Evidence status: observation.
   Reasoning: The authors credit the estimator to prior work, so this candidate's novelty is limited to applying it in SSD.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018), which we now
introduce.
   - **Suggested revision:** None.

3. **The output-norm sensitivity substitution is explicitly borrowed from continual learning. Its originality is limited to applying it in the unlearning setting.**
   This contribution should not be credited as a new estimator. The authors do not claim it is one.
   Evidence status: observation.
   Reasoning: The authors directly attribute Eq. 3 to Aljundi et al.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018), which we now
introduce.
   - **Suggested revision:** None.

4. **LFSSD's α settings differ across experiments (α=10 for Cifar20 subclass, α=3.5 for Cifar10 random-sample). The paper describes only a simplified search with α in [1, 50] and λ=1 on CIFAR100 rocket. It is unclear how the per-task α was chosen without labels.**
   Table 6 uses LFSSD α=10, λ=1. Table 7 uses LFSSD α=3.5, λ=1. The documented sensitivity search covers α in [1, 50] with λ=1 on CIFAR100 rocket only.
   Evidence status: inference.
   Reasoning: Record 25 states that the LFSSD search kept λ=1 and varied α over [1, 50], reported for CIFAR100 rocket unlearning. Records 28 and 29 show LFSSD using α=10 in Table 6 and α=3.5 in Table 7. The deployed α therefore varies by task. The records do not show how 3.5 and 10 were picked for tasks other than the one in the sensitivity study. If the choice relied on labeled validation or comparison with a retrained model, the practical label-free setting is qualified, although the importance estimate itself remains loss-free.
   Source `review-record:visual/25`: The sensitivity analysis text says lambda is fixed at 1 with alpha values [1, 50], and refers to Table 2 on CIFAR100 rocket class unlearning.
   Source `review-record:visual/28`: Table 6 caption shows SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1, with MR defined as mushroom and Rkt as Rocket.
   Source `review-record:visual/29`: Table 7 caption shows SSD: α = 10, λ = 1; LFSSD: α = 3.5, λ = 1.
   Source `paper:chars/13295-13404`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   Source `paper:chars/20462-20585`: Table 6: Subclass unlearning on Cifar20. SSD: αRN = 10, αV iT = 25, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.
   Source `paper:chars/23104-23147`: SSD: α = 10 , λ = 1 ; LFSSD:
α = 3.5, λ = 1
   - **Suggested revision:** State the selection procedure and the signals used to choose α for each benchmark, and whether any labeled data or retrained-model reference was needed. Optionally, report results with a single fixed α across all tasks.

5. **The 'first label-free, retraining-free' claim is hedged in the introduction but stated unhedged in the conclusion. The paper also cites zero-shot unlearning without explaining how it differs in data or label requirements.**
   I have not inspected the cited work, so the actual difference is unverified.
   Evidence status: inference.
   Reasoning: The introduction says 'to the best of our knowledge', but the conclusion drops that hedge. Chundawat et al. 2023b (zero-shot unlearning) is grouped with retraining-based methods, but its label and data requirements are not discussed.
   Source `paper:chars/6820-7514`: is the first retraining free
machine unlearning method to require only the unlabelled input samples for the forget set
   Source `paper:chars/1165-4392`: (Chundawat et al.,
2023a;b; Graves et al., 2021; Tarun et al., 2023; Kurmanji et al., 2023)
   - **Suggested revision:** Add one sentence distinguishing LFSSD's requirements from zero-shot unlearning (Chundawat 2023b), and keep the hedge in the conclusion.

6. **Hyperparameters change across tables: α_ViT is 25 in Table 6 but 10 in Tables 4 and 5, and LFSSD α is 5 in Table 5 but 10 in Table 4. This suggests the settings were tuned per experiment.**
   Per-setting α choices are visible in the captions, but the selection procedure is not stated alongside them.
   Evidence status: observation.
   Reasoning: Record 35 gives 'α_ViT = 25' for Table 6. Records 42 and 43 give α_ViT = 10, and LFSSD α of 10 in Table 4 versus 5 in Table 5. Setting-specific α values raise the question of how they were chosen. It is also unclear whether the baselines received a comparable tuning budget, and whether α was selected using forget or test metrics.
   Source `review-record:visual/35`: The captions render α and λ with subscripts (α_RN, α_ViT). The tables render calligraphic D_r and D_f.
   Source `review-record:visual/42`: Subscripts render properly: α_RN, α_ViT, and calligraphic D_r and D_f.
   Source `review-record:visual/43`: Caption reads: 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' The table rows use the classes ED, NS, people, veg and Veh2 for both RN and ViT.
   Source `paper:chars/20503-20535`: SSD: αRN = 10, αV iT = 25, λ = 1
   Source `paper:chars/15258-15313`: SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1.
   Source `paper:chars/17822-17991`: Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 5, λ = 1.
ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.
   - **Suggested revision:** Describe the α selection procedure and the tuning budget for baselines. Optionally add an α-sensitivity plot for LFSSD.

7. **The conclusion calls LFSSD 'robust', but robustness is only discussed for alpha. Privacy guarantees rest on a single entropy-based logistic-regression membership inference attack.**
   This matters most because the paper motivates the method with legal and privacy needs.
   Evidence status: inference.
   Reasoning: Robustness and practical usefulness are asserted rather than tested. A single weak attack does not establish forgetting in regulatory contexts.
   Source `paper:chars/6820-7514`: LFSSD is lightweight, robust and more practically useful than its predecessors.
   Source `paper:chars/7514-23701`: logistic regression is used to classify samples as seen or unseen for a
given model, based the entropy of the model outputs for that sample.
   - **Suggested revision:** Soften 'robust' or define it, and add a limitations sentence on the MIA's strength.

8. **Only one weak MIA is used (logistic regression on output entropy), and all tasks are small-scale, so the evidence of forgetting is limited.**
   This setup follows prior SSD evaluation, so it is consistent but limited.
   Evidence status: observation.
   Reasoning: The described MIA is simple, and stronger attacks could reveal residual information.
   Source `paper:chars/7514-23701`: logistic regression is used to classify samples as seen or unseen for a
given model, based the entropy of the model outputs for that sample
   - **Suggested revision:** Note the limitation, or add a stronger attack such as LiRA.

9. **The importance estimator itself is credited to Aljundi et al. (2018), so it is not novel. The novelty is its application within SSD for unlearning.**
   Reviewers should credit the transfer to unlearning, not the estimator itself.
   Evidence status: observation.
   Reasoning: The authors attribute the estimator to Aljundi et al. (2018), whose content is reported by the authors rather than verified here.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)
   - **Suggested revision:** None.

## Evidence to examine (advisory)

### Reviewer coverage limitation: captions (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/0`
- Source: `paper:chars/15647-15731`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: budgets (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/1`
- Source: `paper:chars/20462-20558`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: captions (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/2`
- Source: `paper:chars/20894-20978`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/3`
- Source: `paper:chars/4788-4890`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Rendered formulas: Equation 2 renders as f(x;θ+δ) − f(x;θ) ≈ Σ_i ∂f(x;θ)/∂θ_i δ_i. Equation 3 renders as Ω_i = (1/N) Σ_{k=1}^{N} ‖∂[l_2^2(f(x_k;θ))]/∂θ_i‖.

Scope: paper-only; analysis: visual; evidence status: inference.
Equation 3 uses the gradient magnitude of the squared l2 norm of the output, averaged over N samples. This matches the accompanying text.

- Source: `review-record:visual/4`
- Source: `paper:chars/5750-5819`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: units (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/5`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/8`
- Source: `paper:chars/1466-1497`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: rendered formulas (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/9`
- Source: `paper:chars/927-981`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Sample counts: Appendix Benchmarks paragraph reads 'Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables.'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered repeat count of 10 matches the extracted text.

- Source: `review-record:visual/15`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Units: Rendered text states 'D_r and D_f in the tables denote the accuracy on the respective subset of data in percent.'

Scope: paper-only; analysis: visual; evidence status: inference.
The unit (percent) for the Dr/Df accuracies is rendered consistently with the text.

- Source: `review-record:visual/16`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Budgets: Rendered text reads 'a model finetuned for 2 epochs on 𝒟_r'.

Scope: paper-only; analysis: visual; evidence status: inference.
The finetuning budget of 2 epochs matches the extracted text.

- Source: `review-record:visual/17`
- Source: `paper:chars/9926-9962`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Retain-set symbols render as calligraphic 𝒟_r with a subscript r. Later in the paragraph, D_r and D_f render as italic D with subscripts.

Scope: paper-only; analysis: visual; evidence status: inference.
The symbols render legibly. The calligraphic 𝒟 versus italic D styling difference is minor notation and does not change meaning.

- Source: `review-record:visual/18`
- Source: `paper:chars/9914-9962`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Captions: Figure 1 shows a 'Loss-free importance estimation' panel (surface plot, 'Approximate parameter importances label-free via output gradients') feeding a 'Selective Synaptic Dampening' panel (Protect generalization, Target forget set importance, Synapse selection (α), Synaptic dampening (λ)) and an 'Unlearned model' panel. Caption: 'Loss-free parameter importance estimation as a replacement for the label-dependent parameter importance estimation of SSD resulting in the LFSSD method.'

Scope: paper-only; analysis: visual; evidence status: inference.
The diagram's two stages match the caption and the method text: SSD uses α for selection and λ for dampening (Eq. 1).

- Source: `review-record:visual/21`
- Source: `paper:chars/11866-12030`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: The rendered formulas are O(b_full·p), O(b_forget·p), O(b_retain·p), b_retain ≈ b_full >> b_forget, and O(N·b_retain·p). The subscripts render correctly.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered notation is consistent with the text. The broken spacing in the extracted subscripts is extraction noise.

- Source: `review-record:visual/23`
- Source: `paper:chars/12474-12620`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Budgets: The text states that SSD computes gradients for D once and then performs one Df computation per forget request. LFSSD has the same complexity, and retraining methods scale as O(N·b_retain·p).

Scope: paper-only; analysis: visual; evidence status: inference.
The compute budget statements on this page are internally consistent with Section 2: D is computed once and the train set is discarded afterwards.

- Source: `review-record:visual/24`
- Source: `paper:chars/12817-12945`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Sample counts: The sensitivity analysis text says lambda is fixed at 1 with alpha values [1, 50], and refers to Table 2 on CIFAR100 rocket class unlearning.

Scope: paper-only; analysis: visual; evidence status: inference.
This matches the Table 2 caption (λ = 1, CIFAR100 rocket) and its α rows, which range from 1 to 50.

- Source: `review-record:visual/25`
- Source: `paper:chars/13295-13404`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Sample counts: Table 7 caption reads 'Random sample unlearning on Cifar10 (100 samples).'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered sample count matches the extracted caption.

- Source: `review-record:visual/27`
- Source: `paper:chars/23044-23103`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: Table 6 caption shows SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1, with MR defined as mushroom and Rkt as Rocket.

Scope: paper-only; analysis: visual; evidence status: inference.
The hyperparameters and abbreviations agree. The split 'V iT' is extraction noise.

- Source: `review-record:visual/28`
- Source: `paper:chars/20462-20585`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: Table 7 caption shows SSD: α = 10, λ = 1; LFSSD: α = 3.5, λ = 1.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered hyperparameters match the paper text.

- Source: `review-record:visual/29`
- Source: `paper:chars/23104-23147`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: units (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/30`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: In Table 6, ViT lamp Df shows SSD 14.58±0.00 and LFSSD 24.05±0.00. RN lamp Dr shows SSD 79.58 and LFSSD 81.54.

Scope: paper-only; analysis: visual; evidence status: inference.
These rendered values match the extracted table and are consistent with the Cifar20 rows of Table 1.

- Source: `review-record:visual/31`
- Source: `paper:chars/22176-22253`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: sample counts (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/32`
- Source: `paper:chars/10824-10956`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Rendered formulas: The captions render α and λ with subscripts (α_RN, α_ViT). The tables render calligraphic D_r and D_f.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered symbols are consistent with the notation used in the text.

- Source: `review-record:visual/35`
- Source: `paper:chars/20503-20535`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Sample counts: Table 3 caption states one face unlearned per experiment, IDs [1,10,20,30,40], with results aggregated over 5 experiments. Five IDs are listed.

Scope: paper-only; analysis: visual; evidence status: inference.
The five listed IDs match the stated count of 5 experiments.

- Source: `review-record:visual/36`
- Source: `paper:chars/14760-14881`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: units (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/37`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: captions (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/38`
- Source: `paper:chars/13353-13403`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: captions (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/39`
- Source: `paper:chars/3674-3795`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Rendered formulas: Subscripts render properly: α_RN, α_ViT, and calligraphic D_r and D_f.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendering matches the text. The "V iT" spacing in the paper quote is extraction noise, not an authoring defect.

- Source: `review-record:visual/42`
- Source: `paper:chars/15258-15313`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: Caption reads: 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' The table rows use the classes ED, NS, people, veg and Veh2 for both RN and ViT.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption matches the extracted text. Every abbreviation used in the class column is defined in the caption, except 'people', which is self-explanatory.

- Source: `review-record:visual/43`
- Source: `paper:chars/17822-17991`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: rendered formulas (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/44`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: units (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/45`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: sample counts (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/46`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Captions: The rendered values match the extracted text. For example, the RN ED row reads 82.56±0.00 ... 83.19±0.00, and the ViT ED SSD Df value is 53.53±0.00.

Scope: paper-only; analysis: visual; evidence status: inference.
The values I spot-checked in the rendered table match the extracted text.

- Source: `review-record:visual/47`
- Source: `paper:chars/19321-19395`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

## Direct visual evidence (advisory)

- **agreement**, rendered page 2, rendered formulas: Equation 2 renders as f(x;θ+δ) − f(x;θ) ≈ Σ_i ∂f(x;θ)/∂θ_i δ_i. Equation 3 renders as Ω_i = (1/N) Σ_{k=1}^{N} ‖∂[l_2^2(f(x_k;θ))]/∂θ_i‖.
  Paper quote: the gradient can be calculated over the squared l2 norm of
the output. Equation 3 uses the gradient magnitude of the squared l2 norm of the output, averaged over N samples. This matches the accompanying text.
- **agreement**, rendered page 3, sample counts: Appendix Benchmarks paragraph reads 'Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables.'
  Paper quote: Runs are repeated 10 times for each method, with the mean and standard
deviation shown in the tables.. The rendered repeat count of 10 matches the extracted text.
- **agreement**, rendered page 3, units: Rendered text states 'D_r and D_f in the tables denote the accuracy on the respective subset of data in percent.'
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. The unit (percent) for the Dr/Df accuracies is rendered consistently with the text.
- **agreement**, rendered page 3, budgets: Rendered text reads 'a model finetuned for 2 epochs on 𝒟_r'.
  Paper quote: a model finetuned for 2 epochs on Dr. The finetuning budget of 2 epochs matches the extracted text.
- **agreement**, rendered page 3, rendered formulas: Retain-set symbols render as calligraphic 𝒟_r with a subscript r. Later in the paragraph, D_r and D_f render as italic D with subscripts.
  Paper quote: on only Dr, a model finetuned for 2 epochs on Dr. The symbols render legibly. The calligraphic 𝒟 versus italic D styling difference is minor notation and does not change meaning.
- **agreement**, rendered page 4, captions: Figure 1 shows a 'Loss-free importance estimation' panel (surface plot, 'Approximate parameter importances label-free via output gradients') feeding a 'Selective Synaptic Dampening' panel (Protect generalization, Target forget set importance, Synapse selection (α), Synaptic dampening (λ)) and an 'Unlearned model' panel. Caption: 'Loss-free parameter importance estimation as a replacement for the label-dependent parameter importance estimation of SSD resulting in the LFSSD method.'
  Paper quote: Figure 1: Loss-free parameter importance estimation as a replacement for the label-dependent pa-
rameter importance estimation of SSD resulting in the LFSSD method.. The diagram's two stages match the caption and the method text: SSD uses α for selection and λ for dampening (Eq. 1).
- **agreement**, rendered page 4, rendered formulas: The rendered formulas are O(b_full·p), O(b_forget·p), O(b_retain·p), b_retain ≈ b_full >> b_forget, and O(N·b_retain·p). The subscripts render correctly.
  Paper quote: Similarly, the complexity
for the forget and retain set is O(bf orget· p) and O(bretain · p), respectively. Note that bretain ≈
bf ull>> bf orget.. The rendered notation is consistent with the text. The broken spacing in the extracted subscripts is extraction noise.
- **agreement**, rendered page 4, budgets: The text states that SSD computes gradients for D once and then performs one Df computation per forget request. LFSSD has the same complexity, and retraining methods scale as O(N·b_retain·p).
  Paper quote: LFSSD has the same complexity as SSD with the difference being that LFSSD calculates the norm
of the output instead of the loss.. The compute budget statements on this page are internally consistent with Section 2: D is computed once and the train set is discarded afterwards.
- **agreement**, rendered page 4, sample counts: The sensitivity analysis text says lambda is fixed at 1 with alpha values [1, 50], and refers to Table 2 on CIFAR100 rocket class unlearning.
  Paper quote: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].. This matches the Table 2 caption (λ = 1, CIFAR100 rocket) and its α rows, which range from 1 to 50.
- **agreement**, rendered page 7, sample counts: Table 7 caption reads 'Random sample unlearning on Cifar10 (100 samples).'
  Paper quote: Table 7: Random sample unlearning on Cifar10 (100 samples).. The rendered sample count matches the extracted caption.
- **agreement**, rendered page 7, captions: Table 6 caption shows SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1, with MR defined as mushroom and Rkt as Rocket.
  Paper quote: Table 6: Subclass unlearning on Cifar20. SSD: αRN = 10, αV iT = 25, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.. The hyperparameters and abbreviations agree. The split 'V iT' is extraction noise.
- **agreement**, rendered page 7, captions: Table 7 caption shows SSD: α = 10, λ = 1; LFSSD: α = 3.5, λ = 1.
  Paper quote: SSD: α = 10 , λ = 1 ; LFSSD:
α = 3.5, λ = 1. The rendered hyperparameters match the paper text.
- **agreement**, rendered page 7, captions: In Table 6, ViT lamp Df shows SSD 14.58±0.00 and LFSSD 24.05±0.00. RN lamp Dr shows SSD 79.58 and LFSSD 81.54.
  Paper quote: Df 89.58±0.00 34.55±8.62 16.90±10.4 8.23±7.05 0.59±1.45 14.58±0.00 24.05±0.00. These rendered values match the extracted table and are consistent with the Cifar20 rows of Table 1.
- **agreement**, rendered page 7, rendered formulas: The captions render α and λ with subscripts (α_RN, α_ViT). The tables render calligraphic D_r and D_f.
  Paper quote: SSD: αRN = 10, αV iT = 25, λ = 1. The rendered symbols are consistent with the notation used in the text.
- **agreement**, rendered page 5, sample counts: Table 3 caption states one face unlearned per experiment, IDs [1,10,20,30,40], with results aggregated over 5 experiments. Five IDs are listed.
  Paper quote: One face unlearned per experiment [ID 1,10,20,30,40]
and results aggregated for 5 experiments as in Foster et al. (2023).. The five listed IDs match the stated count of 5 experiments.
- **agreement**, rendered page 5, rendered formulas: Subscripts render properly: α_RN, α_ViT, and calligraphic D_r and D_f.
  Paper quote: SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1.. The rendering matches the text. The "V iT" spacing in the paper quote is extraction noise, not an authoring defect.
- **agreement**, rendered page 6, captions: Caption reads: 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' The table rows use the classes ED, NS, people, veg and Veh2 for both RN and ViT.
  Paper quote: Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 5, λ = 1.
ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.. The rendered caption matches the extracted text. Every abbreviation used in the class column is defined in the caption, except 'people', which is self-explanatory.
- **agreement**, rendered page 6, captions: The rendered values match the extracted text. For example, the RN ED row reads 82.56±0.00 ... 83.19±0.00, and the ViT ED SSD Df value is 53.53±0.00.
  Paper quote: Df 95.03±0.00 0.00±0.00 0.28±0.22 4.14±3.75 0.03±0.08 53.53±0.00 0.68±0.00. The values I spot-checked in the rendered table match the extracted text.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 18 |
| Confirmed text-image mismatch (advisory) | 0 |
| Not applicable | 17 |
| Grounding failure: context, citation or readability | 0 |
| Missing or invalid confirmation | 2 |
| Conflicting assessments | 11 |
| Substantive uncertainty | 2 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.


