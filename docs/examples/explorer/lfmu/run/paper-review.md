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

The paper proposes Label-Free Selective Synaptic Dampening (LFSSD), an extension of the authors' Selective Synaptic Dampening (SSD) method for retraining-free machine unlearning. LFSSD replaces SSD's Fisher-information-diagonal parameter importance with the output-sensitivity estimate from Aljundi et al. (2018), the gradient of the squared l2 norm of the model output. Because this estimate needs no labels or loss, only unlabelled forget samples are needed at forgetting time, given importance over the full training data computed once beforehand. The method is evaluated against SSD and a retrain reference on class, subclass, and random-sample unlearning with ResNet and ViT models on CIFAR benchmarks.

## Contributions

1. **Loss-Free Selective Synaptic Dampening (LFSSD) unlearning method.** An extension of Selective Synaptic Dampening that replaces Fisher-information-based parameter importance with the gradient of the squared l2 norm of the model output. This removes the need for the loss or ground-truth labels while keeping unlearning retraining-free.
   *Claim support: unresolved · Significance: unassessed · Originality: unresolved*
2. **First retraining-free unlearning requiring only unlabelled forget samples.** Machine unlearning that needs neither retraining nor labels. At forgetting time it requires only the unlabelled forget-set inputs, without long-term storage of the retain dataset.
   *Claim support: unresolved · Significance: supported · Originality: contested*
3. **Output-sensitivity importance estimation applied to unlearning.** Introduces into unlearning the output-sensitivity parameter-importance estimate previously used in continual learning (Memory Aware Synapses).
   *Claim support: unresolved · Significance: unassessed · Originality: unresolved*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: Loss-Free Selective Synaptic Dampening (LFSSD) unlearning method

**Claim support: unresolved**
- No claims are linked to this contribution.
- Across the reported benchmarks, LFSSD is broadly competitive with SSD. It sometimes improves on SSD's ViT failure cases, which supports the competitiveness claim.
- The empirical results across ResNet18 and ViT, multiple tasks, and multiple baselines broadly support the claim that LFSSD is competitive with SSD.
- The results tables support the claim that LFSSD is competitive with SSD. In some ViT settings LFSSD forgets more completely than SSD, but subclass forget accuracy varies from SSD and from retraining.
- The claim of being 'equally effective as Fisher information' is not uniform: ViT subclass results show sizable deviations from retrain on Df.
- None of the candidate contributions has linked supporting claims. The empirical support comes from Tables 1 and 3–7, which compare LFSSD with SSD and baselines across 10 runs.
- Sources: paper:chars/7514-23701, paper:chars/1165-4392

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The authors present LFSSD as an extension of their prior SSD method. The only change is that the Fisher-diagonal importance term is replaced with the Memory Aware Synapses output-sensitivity estimate from Aljundi et al. (2018). The novelty is therefore a component substitution, and the authors describe it as such.
- The paper calls LFSSD 'a novel extension of SSD', which matches its stated positioning as a modification of SSD.
- The authors frame LFSSD as an extension that combines their prior SSD with an importance estimator they attribute to Aljundi et al. (2018). The novelty lies in this combination and its application to unlearning, not in a new estimator.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/284-1165, paper:chars/4392-6820, paper:chars/1165-4392

Paper’s wording: “Therefore, we propose a novel extension of SSD that does not require access to the loss or ground truth labels, which we refer to as Loss-Free Selective Synaptic Dampening (LFSSD).”

### Contribution 2: First retraining-free unlearning requiring only unlabelled forget samples

**Claim support: unresolved**
- No claims are linked to this contribution.
- The 'first label-free' contribution has no linked supporting claims. The paper does substantiate that the method needs only unlabelled forget inputs at forgetting time, by noting that importance over D is computed once beforehand.
- The label-free claim is substantiated by construction, since Eq. 3 uses no labels. However, all experiments use labelled datasets, and the motivating label-free scenarios (catalogues, semi-supervised models) are not evaluated.
- Computing importance over D still requires the training inputs once, which tempers the 'only unlabelled forget samples' framing.
- Sources: paper:chars/4392-6820, paper:chars/7514-23701

**Significance: supported**
- Removing label and retain-set dependence is practically useful, and the authors motivate concrete label-free scenarios.
- Sources: paper:chars/7514-23701

**Originality: contested**
- The 'first' claim for retraining-free unlearning with unlabelled forget samples is hedged with 'to the best of our knowledge'. The paper does not discuss zero-shot or other data-light unlearning methods to show they need labels.
- The primacy claim ('first retraining-free method requiring only unlabelled forget samples') is hedged with 'to the best of our knowledge'. However, the related-work coverage behind it is very brief and does not address label-free or zero-shot unlearning work beyond what is cited.
- The 'first' claim depends on storing a precomputed importance over D. The label-free requirement applies only at forgetting time, since computing the D importance needs access to the full data.
- The claim that LFSSD is 'the first' retraining-free method needing only unlabelled forget samples is hedged with 'to the best of our knowledge'. The paper's related-work coverage is brief, so this priority claim is unverified.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/4392-6820

Paper’s wording: “To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only the unlabelled forget samples at forgetting time.”

### Contribution 3: Output-sensitivity importance estimation applied to unlearning

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The authors frame LFSSD as an extension that combines SSD with the MAS sensitivity estimate (Aljundi et al.). By their own account, the originality lies in this combination and in removing the need for labels, not in a new importance measure.
- The authors frame the work as a 'novel extension' that combines SSD with MAS importance (Aljundi et al.). Originality therefore lies in this combination and in the label-free setting, not in either component.
- The claim that output-sensitivity importance has not been applied in unlearning is author-asserted only.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/4392-6820

Paper’s wording: “Such importance estimation has been shown to be effective in continual learning (Aljundi et al., 2018), yet it has not been applied in unlearning.”

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

1. **The authors present LFSSD as an extension of their prior SSD method. The only change is that the Fisher-diagonal importance term is replaced with the Memory Aware Synapses output-sensitivity estimate from Aljundi et al. (2018). The novelty is therefore a component substitution, and the authors describe it as such.**
   This is an incremental but clearly positioned change that fits a tiny-paper format.
   Evidence status: inference.
   Reasoning: Both components are attributed to prior work: SSD to Foster et al. and the sensitivity estimator to Aljundi et al. The contribution is their combination and the label-free property it yields. The paper frames this honestly as an extension. The cited works' content is author-reported here and was not independently verified.
   Source `paper:chars/284-1165`: we present an extension to the Selective Synaptic Dampening algorithm,
substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)

2. **The authors frame LFSSD as an extension that combines SSD with the MAS sensitivity estimate (Aljundi et al.). By their own account, the originality lies in this combination and in removing the need for labels, not in a new importance measure.**
   The contribution is incremental but useful. Its value depends on the label-free setting being practically relevant.
   Evidence status: inference.
   Reasoning: Both components are cited prior work. The novelty is transferring the MAS estimate into SSD to make unlearning label-free. Whether MAS-style importance has truly never been used in unlearning is author-reported and was not verified here.
   Source `paper:chars/1165-4392`: Such importance estimation has been shown to be effective in continual learning (Aljundi et al.,
2018), yet it has not been applied in unlearning.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)

3. **LFSSD replaces the Fisher-based importance in Selective Synaptic Dampening with the gradient of the squared l2 norm of the model output. This makes retraining-free unlearning label-free.**
   The paper is a simple, clearly scoped modification that fits the tiny-paper format.
   Evidence status: observation.
   Reasoning: The quotes state the single methodological change directly.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity
   Source `paper:chars/4392-6820`: the gradient can be calculated over the squared l2 norm of
the output

4. **The paper proposes LFSSD, which modifies Selective Synaptic Dampening by replacing Fisher-based importance with gradients of the squared l2 norm of the model output. This makes retraining-free unlearning label-free.**
   This is a small, clearly scoped modification suited to the Tiny Paper format.
   Evidence status: observation.
   Reasoning: The abstract states the method directly.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity

## Originality

The contribution is incremental and the paper positions it honestly. It is a component substitution that brings a continual-learning importance estimator (Aljundi et al., 2018) into the SSD framework (Foster et al.), and both components are attributed to prior work. The originality lies in this combination and in the label-free property at forgetting time, not in a new importance measure. Two originality claims are not established by the paper itself. First, the statement that output-sensitivity importance 'has not been applied in unlearning' is an absence claim with no supporting survey, and we could not assess it. Second, the claim that LFSSD is the 'first retraining-free unlearning method to require only the unlabelled forget samples at forgetting time' is hedged with 'to the best of our knowledge'. It rests on a brief related-work discussion confined to the introduction, and it does not engage label- or data-light alternatives such as zero-shot unlearning, which is cited only in passing. The scope of 'first' should be stated precisely: the label-free property holds at forgetting time, while computing importance over D still requires the full training data, as SSD also does. If prior unlearning work has already used MAS-style importance, the novelty of the substitution would shrink further.

## Likely impact

Practitioners who must honour forget requests without ground-truth labels could benefit from a simple, retraining-free option. The paper's motivating examples are unlabelled catalogues and models trained with semi-supervised learning, where pseudo labels may be unreliable. Its simplicity suits the tiny-paper format and makes it easy to adopt within SSD-style pipelines. Several factors may limit its influence. The motivating label-free scenarios are not evaluated, and all experiments use labelled datasets. Selecting the dampening hyperparameter α appears to require measuring retain and forget accuracy, which needs labels, and this partly undercuts the label-free motivation in deployment. Finally, effectiveness relative to the retrain reference is uneven on subclass forgetting.

## Decision-critical concerns

1. **The claim that LFSSD is 'equally effective' as Fisher information is overstated. On subclass forgetting, LFSSD often deviates strongly from the retrain reference, and the hyperparameters differ between methods.**
   No aggregate metric of distance to retrain is reported, and no matched-hyperparameter comparison is given.
   Evidence status: inference.
   Reasoning: The paper says similarity to retrain is the objective. In the RN sea subclass case, LFSSD drives Df to 18.06 while retrain stays at 91.47, i.e. over-forgetting. In the ViT MR case, LFSSD leaves Df at 31.42 against 26.57 for retrain. SSD's alpha came from an Optuna search, while LFSSD used a separate grid. As a result, any differences mix the effect of the importance measure with the effect of tuning.
   Source `paper:chars/7514-23701`: Df 96.27±0.00 91.47±1.92 82.69±7.17 75.13±4.12 46.78±8.55 75.35±0.00 18.06±0.00
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   Source `paper:chars/7514-23701`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information
   - **Why this affects the decision:** The headline equivalence claim depends on this comparison.
   - **Actionable revision:** Report a summary of |Df − retrain Df| and |MIA − retrain MIA| per task for SSD and LFSSD. Also run SSD under the same alpha grid with lambda=1, or soften the 'equally effective' wording.
   - **What would resolve it:** A matched-tuning comparison showing comparable distance to retrain, or a revised claim.

2. **The claim that the method is 'equally effective as Fisher information' is broadly supported for class unlearning. In subclass unlearning, however, LFSSD's forget-set accuracy is far from the retrain reference in several cases, so the paper does not show equal effectiveness there.**
   Results are mixed relative to SSD across subclass tasks.
   Evidence status: inference.
   Reasoning: For ViT 'sea' subclass, the retrain model keeps 95.12% forget-set accuracy, while LFSSD drops it to 20.83%. That is over-forgetting, which the paper itself warns about. For ViT 'MR', LFSSD and SSD differ in opposite directions from the retrain model.
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information
   Source `paper:chars/7514-23701`: Df 99.22±0.00 95.12±0.81 89.17±4.17 25.97±14.01 21.42±8.5 97.05±0.00 20.83±0.00
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   - **Why this affects the decision:** The 'equally effective' framing may overstate what the evidence supports.
   - **Actionable revision:** Qualify the claim by task type and discuss the subclass cases where LFSSD diverges from the retrain model, such as over-forgetting on 'sea'.
   - **What would resolve it:** Revised claim text plus an aggregate gap-to-retrain metric for each task.

3. **The primacy claim ('first retraining-free method requiring only unlabelled forget samples') is hedged with 'to the best of our knowledge'. However, the related-work coverage behind it is very brief and does not address label-free or zero-shot unlearning work beyond what is cited.**
   The claim also appears in the abstract framing and in the conclusion.
   Evidence status: inference.
   Reasoning: The related-work discussion is confined to a single combined introduction section. Without a broader survey of label-free or source-free unlearning, the 'first' claim cannot be checked from the paper alone.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.
   - **Why this affects the decision:** An overstated primacy claim weakens the originality case.
   - **Actionable revision:** Add a short survey of label-free, unsupervised and zero-shot unlearning methods. Either explicitly scope the claim (retraining-free + label-free + no retain data) or soften it.
   - **What would resolve it:** Citations to the nearest label-free unlearning works, with a stated difference from each.

4. **The claim of being 'equally effective as Fisher information' is not uniform: ViT subclass results show sizable deviations from retrain on Df.**
   Over-forgetting is flagged by the paper itself as risking the Streisand effect.
   Evidence status: inference.
   Reasoning: In the ViT subclass 'sea' row, retrain gives Df 95.12 but LFSSD gives 20.83. Since the paper itself treats closeness to retrain as the target, this indicates over-forgetting relative to SSD (97.05).
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information
   Source `paper:chars/7514-23701`: Df 96.44±0.00 93.23±1.09 85.45±4.47 46.66±17.88 38.76±7.36 94.10±0.00 86.81±0.00
   Source `paper:chars/7514-23701`: Df 99.22±0.00 95.12±0.81 89.17±4.17 25.97±14.01 21.42±8.5 97.05±0.00 20.83±0.00
   - **Why this affects the decision:** It qualifies the headline equivalence claim.
   - **Actionable revision:** Scope the claim and discuss the subclass cases where LFSSD diverges from retrain.
   - **What would resolve it:** Revised claim wording plus a discussion of these cases.

## Questions for the authors

1. **The α hyperparameter is tuned with retained or full data, and Table 2 shows sharp failures at extreme values. It is unclear how α would be chosen in a truly label-free deployment.**
   The authors acknowledge the limitation, but its interaction with the label-free claim is not discussed.
   Evidence status: inference.
   Reasoning: Choosing α requires measuring Dr and Df accuracy, and measuring accuracy requires labels. This partly undercuts the label-free motivation.
   Source `paper:chars/7514-23701`: 1 16.87% 0.00% 26.60
   Source `paper:chars/7514-23701`: 50 76.32% 71.88% 29.40
   Source `paper:chars/4392-6820`: A shared limitation with SSD is the reliance
on choosing α and λ values that balance forgetting and model performance.
   - **Why the answer matters:** It affects how practical the core claim is.
   - **Requested response:** Explain how α would be selected without labels, or show that a single default α transfers across datasets and models.
   - **Answer that would resolve it:** Results using a fixed α across all settings, or a label-free selection procedure.

2. **The 'first' claim depends on storing a precomputed importance over D. The label-free requirement applies only at forgetting time, since computing the D importance needs access to the full data.**
   The scope of 'first' needs to be stated precisely.
   Evidence status: inference.
   Reasoning: SSD also precomputes over D, so storage of D is not the difference. The difference is the label requirement. The paper does not discuss zero-shot unlearning (Chundawat 2023b, cited only in passing) as a label- or data-light alternative.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.
   Source `paper:chars/4392-6820`: Fisher information is calculated over D not Dr,
meaning this is only calculated once
   - **Why the answer matters:** If a prior method already meets the condition, the novelty framing must change.
   - **Requested response:** Clarify how the 'first' claim relates to zero-shot unlearning and other label-free methods.
   - **Answer that would resolve it:** An explicit comparison with the cited zero-shot work.

3. **The claim that output-sensitivity importance 'has not been applied in unlearning' is an absence claim. The paper gives no survey to support it.**
   If prior unlearning work already used MAS-style importance, the originality of the substitution itself would shrink.
   Evidence status: unassessed.
   Reasoning: This is an absence assertion, and I cannot verify it from the paper alone.
   Source `paper:chars/1165-4392`: yet it has not been applied in unlearning.
   - **Why the answer matters:** Determines whether the substitution is itself novel.
   - **Requested response:** State what search supports this claim, or cite the closest unlearning work that uses MAS-style importance.
   - **Answer that would resolve it:** A literature check showing no prior use, or a stated distinction from any prior use found.

## Decision synthesis

On the positive side, the method is a clearly scoped, cleanly motivated modification. The label-free property holds by construction, since the importance estimate uses no labels and the training set can be discarded after a one-time importance computation. The comparison with SSD broadly supports comparable behaviour on class unlearning. On the negative side, the evidence that matters most concerns the central claim that the new importance estimate is 'equally effective as Fisher information'. In subclass unlearning, LFSSD's forget-set accuracy departs substantially from the retrain reference in several cases. For ViT 'sea', retrain keeps about 95% forget accuracy while LFSSD drops it to about 21%. For ResNet 'sea', the figures are about 91% for retrain versus about 18% for LFSSD. This is the over-forgetting the paper itself warns about. For ViT 'mushroom', LFSSD and SSD deviate from retrain in opposite directions. No aggregate distance-to-retrain metric is reported. SSD and LFSSD were also tuned with different procedures and different per-setting α values (for example α = 10, 5, and 3.5 for LFSSD across settings). The sensitivity analysis covers only CIFAR100 rocket-class unlearning, so differences may mix the effect of the importance measure with the effect of tuning. Score-changing questions for the authors: (1) How were α values chosen for each setting, and would a single α (e.g., 10) work across all benchmarks? (2) Can the comparison be repeated under matched hyperparameter tuning, with a summary metric of distance to retrain? (3) How should α be chosen in a genuinely label-free deployment? (4) Can the 'first' and 'not applied in unlearning' claims be scoped precisely and supported with broader related work, including zero-shot and data-free unlearning? Non-blocking improvements: evaluate a scenario with noisy or pseudo labels to support the practical motivation, and restate the effectiveness claim to distinguish class from subclass results.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The abstract is compact and clear about the problem, the specific change to SSD, and why it matters, which suits a short-format paper.

**Writing-quality issues**

1. **The central result is stated only as 'competitive'. Neither the abstract nor the main text gives one plain sentence on how LFSSD compares with SSD, including where it does better or worse.**
   The tables show a mixed pattern that a reader would benefit from seeing summarised in words.
   - **Suggested revision:** Add one plain sentence to the abstract or results stating where LFSSD matches, exceeds, or falls short of SSD, for example full-class versus subclass forgetting.

2. **Key notation and terms in Table 1 (Dr, Df, MIA, Cifar20 subclass) are defined only later in Section 2 or the appendix. Figure 1 is never referenced in the text.**
   The order of definitions forces readers to jump ahead to interpret the main table.
   - **Suggested revision:** Define Dr, Df, and MIA, and explain what a good value looks like, in the Table 1 caption. Also reference Figure 1 from the Methods section.

3. **The conclusion describes the method as 'robust and more practically useful' without pointing to the evidence for robustness. The paper itself reports that performance depends on choosing alpha.**
   The appendix sensitivity analysis could support the robustness claim if it were linked to it.
   - **Suggested revision:** Point the robustness claim to the sensitivity analysis in Table 2. Specify robust to what, for example a wide range of alpha values, and keep the hyperparameter limitation alongside it.

4. **The practical scenarios that motivate label-free unlearning appear only in the appendix. The introduction motivates the problem only abstractly, with labels that 'may not always be available'.**
   Readers of the main text alone get little guidance on when to use this method.
   - **Suggested revision:** Add one sentence to the introduction naming the main label-free scenarios.

## Additional improvements (non-blocking)

1. **The paper calls LFSSD 'a novel extension of SSD', which matches its stated positioning as a modification of SSD.**
   The framing is consistent with the abstract and conclusion.
   Evidence status: observation.
   Reasoning: The claim is scoped as an extension of SSD, so it does not overclaim.
   Source `paper:chars/1165-4392`: Therefore, we propose a novel extension of SSD that does not require access to the loss
or ground truth labels
   - **Suggested revision:** None.

2. **The 'first label-free' contribution has no linked supporting claims. The paper does substantiate that the method needs only unlabelled forget inputs at forgetting time, by noting that importance over D is computed once beforehand.**
   The mechanism is supported. Primacy remains unverified.
   Evidence status: observation.
   Reasoning: Because importance over D is computed once and the train set can then be discarded, only unlabelled Df inputs are needed at forgetting time. This supports the mechanism part of the claim, but not the primacy part.
   Source `paper:chars/4392-6820`: meaning this is only calculated once, and then the train-set may be discarded after.
   - **Suggested revision:** None.

3. **The label-free claim is substantiated by construction, since Eq. 3 uses no labels. However, all experiments use labelled datasets, and the motivating label-free scenarios (catalogues, semi-supervised models) are not evaluated.**
   Testing a scenario where labels are noisy or pseudo labels would strengthen the practical-impact claim.
   Evidence status: observation.
   Reasoning: The motivating scenario is described but not tested.
   Source `paper:chars/7514-23701`: Second, models that were trained with semi-supervised learning
could benefit from our method when we do not want to rely on the accuracy of pseudo labels.
   - **Suggested revision:** Add a pseudo-label comparison, e.g. SSD with noisy labels versus LFSSD.

4. **The plateau evidence comes from one setting, yet LFSSD uses α=10 on CIFAR100 and α=5 on CIFAR20.**
   The question is whether one α (e.g., 10) would work across all settings without per-dataset selection.
   Evidence status: inference.
   Reasoning: The Table 4 caption sets LFSSD α=10 and the Table 5 caption sets α=5. Both values fall inside the Table 2 plateau. Still, choosing different values per dataset suggests α was selected per setting. Readers cannot tell whether the plateau generalizes beyond the CIFAR100 rocket class.
   Source `review-record:visual/41`: At α=10, Table 2 shows Dr 75.67%, Df 0.00% and MIA 0.00. In Table 4, the RN Rkt LFSSD entries are 75.67±0.00, 0.00±0.00 and 0.00±0.00.
   Source `review-record:visual/43`: The Table 4 caption renders 'SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 10, λ = 1' with proper subscripts. The metric labels render as calligraphic D_r and D_f.
   Source `review-record:visual/45`: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' Rows list RN and ViT with classes ED, NS, people, veg, Veh2.
   Source `paper:chars/13643-13892`: A sensitivity analysis in Table 2 on CIFAR100 rocket class unlearning shows that there
is a significant drop off in performance when picking an alpha that is too aggressive or conservative
but the method has a wide plateau in which it performs well.
   Source `paper:chars/15219-15313`: Table 4: Class unlearning on Cifar100. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1.
   Source `paper:chars/17822-17991`: Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 5, λ = 1.
ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.
   - **Suggested revision:** State how α was chosen per dataset. Alternatively, report CIFAR20 and ViT results at a single shared α, or a brief sweep on at least one more setting.

5. **LFSSD's α changes across settings (α = 10 for Cifar20 subclass, α = 3.5 for Cifar10 random-sample), but the stated sensitivity search is described only for CIFAR100 rocket-class unlearning. The paper should say how α was chosen for each setting.**
   The per-setting hyperparameters are stated, but their selection protocol is not visible beyond the single-class sensitivity search.
   Evidence status: inference.
   Reasoning: Record visual/19 shows the sensitivity paragraph fixing λ = 1 and searching α over [1, 50], and it references CIFAR100 rocket-class unlearning. Records visual/29 and visual/30 show the Table 6 and Table 7 captions reporting different LFSSD α values (10 and 3.5). The SSD α values also differ by architecture in Table 6 (α_RN = 10, α_ViT = 25). The visible text does not say whether the per-setting α values came from the rocket-class search or from separate tuning on each benchmark. That affects how fairly the LFSSD and SSD comparisons were tuned. Matching captions confirm only what the pages state, not how the values were selected.
   Source `review-record:visual/19`: The sensitivity analysis paragraph states that lambda was fixed at 1 and alpha values [1, 50] were searched, and it references Table 2 on CIFAR100 rocket class unlearning.
   Source `review-record:visual/29`: Caption reads 'Table 6: Subclass unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1. MR: mushroom, Rkt: Rocket.'
   Source `review-record:visual/30`: Caption reads 'Random sample unlearning on Cifar10 (100 samples). SSD: α = 10, λ = 1; LFSSD: α = 3.5, λ = 1'.
   Source `paper:chars/13353-13403`: keeping lambda fixed at 1 and alpha values [1, 50]
   Source `paper:chars/20462-20585`: Table 6: Subclass unlearning on Cifar20. SSD: αRN = 10, αV iT = 25, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.
   Source `paper:chars/23044-23147`: Table 7: Random sample unlearning on Cifar10 (100 samples). SSD: α = 10 , λ = 1 ; LFSSD:
α = 3.5, λ = 1
   - **Suggested revision:** State the α selection procedure for each benchmark and architecture, including the data used for selection and whether SSD received equal tuning effort. Optionally, report sensitivity curves for the subclass and random-sample settings.

6. **The ±0.00 spreads in Table 4 raise the question of how many runs were aggregated for class unlearning.**
   If the ± reflects only a deterministic method on one model, it does not capture variance across seeds or trained models.
   Evidence status: inference.
   Reasoning: The Table 4 RN rocket LFSSD entries read 75.67±0.00, 0.00±0.00 and 0.00±0.00. These are identical to the single Table 2 α=10 values. A zero spread on Dr fits either a single run or a fully deterministic, retraining-free procedure applied to one fixed checkpoint. The supplied records state the number of repeats only for Table 3 (5 face IDs).
   Source `review-record:visual/41`: At α=10, Table 2 shows Dr 75.67%, Df 0.00% and MIA 0.00. In Table 4, the RN Rkt LFSSD entries are 75.67±0.00, 0.00±0.00 and 0.00±0.00.
   Source `paper:chars/13643-13892`: A sensitivity analysis in Table 2 on CIFAR100 rocket class unlearning shows that there
is a significant drop off in performance when picking an alpha that is too aggressive or conservative
but the method has a wide plateau in which it performs well.
   - **Suggested revision:** State the number of runs and the source of variance (seeds, models, forget sets) behind the ± values in Tables 4 and 5.

7. **The alpha sensitivity analysis is useful but shows sharp failure at the extremes. In addition, the alpha value changes per task (3.5, 5, 10).**
   The authors acknowledge this as a shared limitation with SSD.
   Evidence status: observation.
   Reasoning: With alpha=1, Dr accuracy collapses to 16.87%. Choosing alpha without access to retrain references is not discussed.
   Source `paper:chars/7514-23701`: 1 16.87% 0.00% 26.60
   - **Suggested revision:** Discuss how to choose alpha without a retrained reference model.

8. **Computing importance over D still requires the training inputs once, which tempers the 'only unlabelled forget samples' framing.**
   The stored importances must be retained.
   Evidence status: observation.
   Reasoning: The claim is valid at forgetting time only. Precomputation over D is still required.
   Source `paper:chars/4392-6820`: Fisher information is calculated over D not Dr,
meaning this is only calculated once, and then the train-set may be discarded after.
   - **Suggested revision:** State explicitly that importances over D are precomputed and stored.

9. **The conclusion calls LFSSD 'robust and more practically useful than its predecessors'. The supplied excerpts give no evidence for robustness beyond the α plateau, and the MIA evaluation is a simple entropy-based attack.**
   This is a wording and scope issue.
   Evidence status: inference.
   Reasoning: Strong privacy-related claims would need stronger attacks or more careful wording.
   Source `paper:chars/6820-7514`: LFSSD is lightweight, robust and more practically useful than its predecessors.
   Source `paper:chars/7514-23701`: logistic regression is used to classify samples as seen or unseen for a
given model, based the entropy of the model outputs for that sample
   - **Suggested revision:** Soften the 'robust' claim and note that the MIA is weak.

10. **The claim that output-sensitivity importance has not been applied in unlearning is author-asserted only.**
   The claim is plausible but unverified.
   Evidence status: observation.
   Reasoning: No supporting survey is given for this claim.
   Source `paper:chars/1165-4392`: yet it has not been applied in unlearning
   - **Suggested revision:** Soften the wording or cite a supporting survey.

## Evidence to examine (advisory)

### Rendered formulas: Introduction renders calligraphic set notation: 'D_r = D \ D_f' with subscripts r and f, and D_f, D_r used consistently in the paragraph.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered set-difference definition matches the extracted text. Lost subscripts and calligraphic font in the extraction are extraction noise.

- Source: `review-record:visual/0`
- Source: `paper:chars/1398-1497`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Rendered formulas: Abstract renders 'gradient of the l_2 norm of the model output' with a subscript 2 on l.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered l_2 matches the extracted 'l2'. The extraction only flattens the subscript.

- Source: `review-record:visual/1`
- Source: `paper:chars/844-982`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/7`
- Source: `paper:chars/4788-4931`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/8`
- Source: `paper:chars/5951-6043`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/9`
- Source: `paper:chars/844-982`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: captions (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/10`
- Source: `paper:chars/20462-20558`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: captions (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/11`
- Source: `paper:chars/15647-15731`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: units (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/12`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Captions: Figure 1 has two left-to-right stages labeled 'Loss-free importance estimation' and 'Selective Synaptic Dampening'. The dampening stage contains 'Protect generalization', 'Target forget set importance', 'Synapse selection (α)' and 'Synaptic dampening (λ)' boxes, and the pipeline ends at 'Unlearned model'.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption's description of loss-free importance estimation feeding into SSD to produce LFSSD matches the depicted pipeline.

- Source: `review-record:visual/16`
- Source: `paper:chars/11866-12030`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: The Resources paragraph renders O(b_full · p), O(b_forget · p), O(b_retain · p), and b_retain ≈ b_full >> b_forget, with subscripts displayed correctly.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered complexity expressions match the extracted text. The spacing in the extracted text, such as 'bf ull', is extraction noise and not an authoring defect.

- Source: `review-record:visual/17`
- Source: `paper:chars/12582-12620`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: The text renders O(N · b_retain · p) for retraining-based methods.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered expression agrees with the paper text.

- Source: `review-record:visual/18`
- Source: `paper:chars/13066-13133`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Budgets: The sensitivity analysis paragraph states that lambda was fixed at 1 and alpha values [1, 50] were searched, and it references Table 2 on CIFAR100 rocket class unlearning.

Scope: paper-only; analysis: visual; evidence status: inference.
The stated search range matches Table 2, which lists α values from 1 to 50 with λ = 1.

- Source: `review-record:visual/19`
- Source: `paper:chars/13353-13403`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Sample counts: Appendix Benchmarks paragraph reads: "Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables."

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered repeat count of 10 runs matches the supplied text.

- Source: `review-record:visual/23`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Budgets: Rendered text: "a model finetuned for 2 epochs on D_r" with calligraphic D and subscript r.

Scope: paper-only; analysis: visual; evidence status: inference.
The finetuning budget of 2 epochs matches. The extracted 'Dr' corresponds to the rendered calligraphic D with subscript r.

- Source: `review-record:visual/24`
- Source: `paper:chars/9926-9962`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Units: Rendered text: "D_r and D_f in the tables denote the accuracy on the respective subset of data in percent."

Scope: paper-only; analysis: visual; evidence status: inference.
The page states accuracy units as percent, consistent with the supplied text.

- Source: `review-record:visual/25`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Inline math renders as calligraphic \mathcal{D}_r in the Benchmarks sentences, and as italic D_r and D_f in the 'in the tables' sentence. No broken glyphs are visible.

Scope: paper-only; analysis: visual; evidence status: inference.
The symbols render legibly and correspond to the extracted Dr/Df. The calligraphic-versus-italic difference is typographic only.

- Source: `review-record:visual/26`
- Source: `paper:chars/10735-10803`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Captions: Caption reads 'Table 6: Subclass unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1. MR: mushroom, Rkt: Rocket.'

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered caption matches the extracted text; subscripts render correctly.

- Source: `review-record:visual/29`
- Source: `paper:chars/20462-20585`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Sample counts: Caption reads 'Random sample unlearning on Cifar10 (100 samples). SSD: α = 10, λ = 1; LFSSD: α = 3.5, λ = 1'.

Scope: paper-only; analysis: visual; evidence status: inference.
Sample count of 100 and hyperparameters match the text.

- Source: `review-record:visual/30`
- Source: `paper:chars/23044-23147`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: budgets (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/31`
- Source: `paper:chars/13295-13404`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: units (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/32`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: captions (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/33`
- Source: `paper:chars/10824-10904`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: captions (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/34`
- Source: `paper:chars/10824-10991`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: sample counts (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/35`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Rendered formulas: The metric column renders calligraphic D with subscripts r and f.

Scope: paper-only; analysis: visual; evidence status: inference.
The symbols render properly and are consistent with the notation defined in the text.

- Source: `review-record:visual/37`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Sample counts: Table 3 caption reads 'One face unlearned per experiment [ID 1,10,20,30,40] and results aggregated for 5 experiments'. Five IDs are listed.

Scope: paper-only; analysis: visual; evidence status: inference.
The five listed IDs match the stated count of 5 experiments.

- Source: `review-record:visual/38`
- Source: `paper:chars/14760-14881`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Budgets: Table 2 lists α values 1, 5, 10, 25, 50 with λ = 1 in the caption.

Scope: paper-only; analysis: visual; evidence status: inference.
The tested α values lie within [1, 50], and λ is fixed at 1, as stated.

- Source: `review-record:visual/39`
- Source: `paper:chars/13295-13404`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: The Dr and Df accuracy columns are shown with % signs. The MIA column has no unit.

Scope: paper-only; analysis: visual; evidence status: inference.
The percent units match the paper text.

- Source: `review-record:visual/40`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: At α=10, Table 2 shows Dr 75.67%, Df 0.00% and MIA 0.00. In Table 4, the RN Rkt LFSSD entries are 75.67±0.00, 0.00±0.00 and 0.00±0.00.

Scope: paper-only; analysis: visual; evidence status: inference.
The values are consistent across tables. The table shows drops at α=1 and α=50 and a plateau between them, matching the text.

- Source: `review-record:visual/41`
- Source: `paper:chars/13643-13892`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: captions (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/42`
- Source: `paper:chars/3966-4111`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Rendered formulas: The Table 4 caption renders 'SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 10, λ = 1' with proper subscripts. The metric labels render as calligraphic D_r and D_f.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendering matches the extracted text. The 'αV iT' spacing in the paper text is extraction noise.

- Source: `review-record:visual/43`
- Source: `paper:chars/15219-15313`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' Rows list RN and ViT with classes ED, NS, people, veg, Veh2.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption and its abbreviations match the extracted text and the row labels in the table.

- Source: `review-record:visual/45`
- Source: `paper:chars/17822-17991`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: budgets (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/46`
- Source: `paper:chars/13405-13513`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: units (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/47`
- Source: `paper:chars/10735-10904`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: rendered formulas (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Grounding failure: context, citation or readability. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/48`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: sample counts (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/49`
- Source: `paper:chars/10633-10675`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

## Direct visual evidence (advisory)

- **agreement**, rendered page 1, rendered formulas: Introduction renders calligraphic set notation: 'D_r = D \ D_f' with subscripts r and f, and D_f, D_r used consistently in the paragraph.
  Paper quote: dataset D into a subset of data that needs to be forgotten Df , and the retained data Dr = D \ Df .. The rendered set-difference definition matches the extracted text. Lost subscripts and calligraphic font in the extraction are extraction noise.
- **agreement**, rendered page 1, rendered formulas: Abstract renders 'gradient of the l_2 norm of the model output' with a subscript 2 on l.
  Paper quote: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity.. The rendered l_2 matches the extracted 'l2'. The extraction only flattens the subscript.
- **agreement**, rendered page 4, captions: Figure 1 has two left-to-right stages labeled 'Loss-free importance estimation' and 'Selective Synaptic Dampening'. The dampening stage contains 'Protect generalization', 'Target forget set importance', 'Synapse selection (α)' and 'Synaptic dampening (λ)' boxes, and the pipeline ends at 'Unlearned model'.
  Paper quote: Figure 1: Loss-free parameter importance estimation as a replacement for the label-dependent pa-
rameter importance estimation of SSD resulting in the LFSSD method.. The caption's description of loss-free importance estimation feeding into SSD to produce LFSSD matches the depicted pipeline.
- **agreement**, rendered page 4, rendered formulas: The Resources paragraph renders O(b_full · p), O(b_forget · p), O(b_retain · p), and b_retain ≈ b_full >> b_forget, with subscripts displayed correctly.
  Paper quote: Note that bretain ≈
bf ull>> bf orget.. The rendered complexity expressions match the extracted text. The spacing in the extracted text, such as 'bf ull', is extraction noise and not an authoring defect.
- **agreement**, rendered page 4, rendered formulas: The text renders O(N · b_retain · p) for retraining-based methods.
  Paper quote: generally on the order
of O(N · bretain · p), which is much larger.. The rendered expression agrees with the paper text.
- **agreement**, rendered page 4, budgets: The sensitivity analysis paragraph states that lambda was fixed at 1 and alpha values [1, 50] were searched, and it references Table 2 on CIFAR100 rocket class unlearning.
  Paper quote: keeping lambda fixed at 1 and alpha values [1, 50]. The stated search range matches Table 2, which lists α values from 1 to 50 with λ = 1.
- **agreement**, rendered page 3, sample counts: Appendix Benchmarks paragraph reads: "Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables."
  Paper quote: Runs are repeated 10 times for each method, with the mean and standard
deviation shown in the tables.. The rendered repeat count of 10 runs matches the supplied text.
- **agreement**, rendered page 3, budgets: Rendered text: "a model finetuned for 2 epochs on D_r" with calligraphic D and subscript r.
  Paper quote: a model finetuned for 2 epochs on Dr. The finetuning budget of 2 epochs matches. The extracted 'Dr' corresponds to the rendered calligraphic D with subscript r.
- **agreement**, rendered page 3, units: Rendered text: "D_r and D_f in the tables denote the accuracy on the respective subset of data in percent."
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. The page states accuracy units as percent, consistent with the supplied text.
- **agreement**, rendered page 3, rendered formulas: Inline math renders as calligraphic \mathcal{D}_r in the Benchmarks sentences, and as italic D_r and D_f in the 'in the tables' sentence. No broken glyphs are visible.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset. The symbols render legibly and correspond to the extracted Dr/Df. The calligraphic-versus-italic difference is typographic only.
- **agreement**, rendered page 7, captions: Caption reads 'Table 6: Subclass unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1. MR: mushroom, Rkt: Rocket.'
  Paper quote: Table 6: Subclass unlearning on Cifar20. SSD: αRN = 10, αV iT = 25, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.. Rendered caption matches the extracted text; subscripts render correctly.
- **agreement**, rendered page 7, sample counts: Caption reads 'Random sample unlearning on Cifar10 (100 samples). SSD: α = 10, λ = 1; LFSSD: α = 3.5, λ = 1'.
  Paper quote: Table 7: Random sample unlearning on Cifar10 (100 samples). SSD: α = 10 , λ = 1 ; LFSSD:
α = 3.5, λ = 1. Sample count of 100 and hyperparameters match the text.
- **agreement**, rendered page 7, rendered formulas: The metric column renders calligraphic D with subscripts r and f.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. The symbols render properly and are consistent with the notation defined in the text.
- **agreement**, rendered page 5, sample counts: Table 3 caption reads 'One face unlearned per experiment [ID 1,10,20,30,40] and results aggregated for 5 experiments'. Five IDs are listed.
  Paper quote: One face unlearned per experiment [ID 1,10,20,30,40]
and results aggregated for 5 experiments as in Foster et al. (2023).. The five listed IDs match the stated count of 5 experiments.
- **agreement**, rendered page 5, budgets: Table 2 lists α values 1, 5, 10, 25, 50 with λ = 1 in the caption.
  Paper quote: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].. The tested α values lie within [1, 50], and λ is fixed at 1, as stated.
- **agreement**, rendered page 5, units: The Dr and Df accuracy columns are shown with % signs. The MIA column has no unit.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. The percent units match the paper text.
- **agreement**, rendered page 5, captions: At α=10, Table 2 shows Dr 75.67%, Df 0.00% and MIA 0.00. In Table 4, the RN Rkt LFSSD entries are 75.67±0.00, 0.00±0.00 and 0.00±0.00.
  Paper quote: A sensitivity analysis in Table 2 on CIFAR100 rocket class unlearning shows that there
is a significant drop off in performance when picking an alpha that is too aggressive or conservative
but the method has a wide plateau in which it performs well.. The values are consistent across tables. The table shows drops at α=1 and α=50 and a plateau between them, matching the text.
- **agreement**, rendered page 5, rendered formulas: The Table 4 caption renders 'SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 10, λ = 1' with proper subscripts. The metric labels render as calligraphic D_r and D_f.
  Paper quote: Table 4: Class unlearning on Cifar100. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1.. The rendering matches the extracted text. The 'αV iT' spacing in the paper text is extraction noise.
- **agreement**, rendered page 6, captions: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' Rows list RN and ViT with classes ED, NS, people, veg, Veh2.
  Paper quote: Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 5, λ = 1.
ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.. The rendered caption and its abbreviations match the extracted text and the row labels in the table.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 19 |
| Confirmed text-image mismatch (advisory) | 0 |
| Not applicable | 16 |
| Grounding failure: context, citation or readability | 1 |
| Missing or invalid confirmation | 0 |
| Conflicting assessments | 11 |
| Substantive uncertainty | 4 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.


