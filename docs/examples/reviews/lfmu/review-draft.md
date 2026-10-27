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

This Tiny Paper proposes LFSSD, an extension of Selective Synaptic Dampening (SSD) for machine unlearning. It replaces SSD's Fisher-information-diagonal importance estimate with the gradient of the l2 norm of the model output, the sensitivity measure of Aljundi et al. (2018). As a result, forgetting needs neither retraining nor labels for the forget samples. The method is evaluated against SSD and other baselines on class, subclass, and face-unlearning tasks with ResNet and ViT models.

## Contributions

1. **Loss-Free Selective Synaptic Dampening (LFSSD) unlearning method.** An extension of SSD that replaces Fisher-information parameter importance with the gradient of the squared l2 norm of model output, removing the need for loss or ground-truth labels.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unresolved*
2. **First retraining-free unlearning needing only unlabelled forget samples.** LFSSD unlearns without retraining and without labels, requiring only unlabelled forget-set inputs at forgetting time, so the retain dataset need not be stored long-term.
   *Claim support (inferred links): unassessed · Significance: supported · Originality: unresolved*
3. **Applying sensitivity-based importance from continual learning to unlearning.** Output-sensitivity parameter importance from Memory Aware Synapses is applied to machine unlearning for the first time and shown to be as effective as Fisher information.
   *Claim support (inferred links): unassessed · Significance: supported · Originality: unresolved*
4. **Empirical evaluation on ResNet18 and Vision Transformer.** LFSSD is evaluated on full-class, subclass and random forgetting across CIFAR and face datasets, performing competitively with SSD and other state-of-the-art methods.
   *Claim support (inferred links): supported · Significance: unassessed · Originality: unassessed*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: Loss-Free Selective Synaptic Dampening (LFSSD) unlearning method

**Claim support (inferred links): contested**
- Linked claims (inferred by the reviewer, not declared by the authors):
  - C1: ResNet18 Vision Transformer data metric baseline retrain LFSSD SSD baseline retrain LFSSD SSD Cifar100 Dr 76.39±0.00 72.89±0.34 76.36 76.08 88.84±0.00 90.10±…
- The claim that the method is 'equally effective as Fisher information' is uneven in subclass unlearning. LFSSD Df deviates substantially from retrain in several cases, so 'equally effective' should be scoped.
- Sources: paper:chars/1165-4392, paper:chars/7514-23701

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- LFSSD is positioned by the authors as an extension of their own SSD, swapping Fisher importance for the MAS-style output-sensitivity importance. The novelty is a targeted combination of two existing components rather than a new mechanism.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/4392-6820

Paper’s wording: “Therefore, we propose a novel extension of SSD that does not require access to the loss or ground truth labels, which we refer to as Loss-Free Selective Synaptic Dampening (LFSSD).”

### Contribution 2: First retraining-free unlearning needing only unlabelled forget samples

**Claim support (inferred links): unassessed**
- Linked claims (inferred by the reviewer, not declared by the authors):
  - C1: ResNet18 Vision Transformer data metric baseline retrain LFSSD SSD baseline retrain LFSSD SSD Cifar100 Dr 76.39±0.00 72.89±0.34 76.36 76.08 88.84±0.00 90.10±…
- No grounded finding addressed this.

**Significance: supported**
- Removing label and retain-set storage needs is practically motivated, and the method's cost matches SSD's.
- Sources: paper:chars/7514-23701

**Originality: unresolved**
- The 'first retraining-free method requiring only unlabelled forget samples' claim is hedged in the introduction. The conclusion restates it without the hedge, and the paper cites zero-shot unlearning (Chundawat et al. 2023b) without distinguishing it.
- The 'first' primacy claim depends on a 'retraining-free' qualifier, but the paper does not discuss the cited zero-shot unlearning work. That work may also avoid needing labelled retain data.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/6820-7514

Paper’s wording: “To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only the unlabelled forget samples at forgetting time.”

### Contribution 3: Applying sensitivity-based importance from continual learning to unlearning

**Claim support (inferred links): unassessed**
- Linked claims (inferred by the reviewer, not declared by the authors):
  - C1: ResNet18 Vision Transformer data metric baseline retrain LFSSD SSD baseline retrain LFSSD SSD Cifar100 Dr 76.39±0.00 72.89±0.34 76.36 76.08 88.84±0.00 90.10±…
- No grounded finding addressed this.

**Significance: supported**
- Label-free, retraining-free unlearning has plausible practical uses that the paper names: copyrighted data catalogues and semi-supervised models.
- Sources: paper:chars/7514-23701

**Originality: unresolved**
- The authors frame the work as a 'novel extension' of their own SSD that borrows importance estimation from continual learning (Aljundi et al.). The novelty is therefore a combination and transfer of two existing ideas, not a new importance measure.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392

Paper’s wording: “Such importance estimation has been shown to be effective in continual learning (Aljundi et al., 2018), yet it has not been applied in unlearning.”

### Contribution 4: Empirical evaluation on ResNet18 and Vision Transformer

**Claim support (inferred links): supported**
- Linked claims (inferred by the reviewer, not declared by the authors):
  - C1: ResNet18 Vision Transformer data metric baseline retrain LFSSD SSD baseline retrain LFSSD SSD Cifar100 Dr 76.39±0.00 72.89±0.34 76.36 76.08 88.84±0.00 90.10±…
- In full-class unlearning, LFSSD matches or exceeds SSD in retaining Dr accuracy while driving Df to 0. On ViT lamp, SSD leaves 36.89% Df while LFSSD reaches 0.00.
- The tables support the claim that LFSSD is competitive with SSD and retraining baselines on full-class forgetting. Subclass results are mixed.
- Sources: paper:chars/1165-4392

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “Results show our label-free method is competitive with existing state-of-the-art approaches.”

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

- contributions[0].supporting_claims: claim support not declared
- contributions[1].supporting_claims: claim support not declared
- contributions[2].supporting_claims: claim support not declared
- contributions[3].supporting_claims: claim support not declared

## Reasons to accept

1. **LFSSD is positioned as an extension of SSD that swaps Fisher-based importance for the output-sensitivity importance of Aljundi et al. (2018). The novelty is a targeted, clearly stated substitution rather than a new algorithm.**
   The novelty is combinational. Neither cited work was independently inspected.
   Evidence status: inference.
   Reasoning: The authors credit both parts of the method to prior work: the dampening rule comes from SSD and the importance estimator comes from Aljundi et al. The original element is combining them so that unlearning needs no labels. This is honest framing of an incremental but useful idea, and it suits a tiny-paper format.
   Source `paper:chars/284-1165`: we present an extension to the Selective Synaptic Dampening algorithm,
substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)

2. **This Tiny Paper extends SSD. It replaces the Fisher-diagonal importance with the gradient of the squared l2 norm of the model output, a MAS-style sensitivity measure, so unlearning becomes both retraining-free and label-free.**
   The change is simple and practically motivated. It removes the need for labels at forget time.
   Evidence status: observation.
   Reasoning: The authors state the method directly. It is a single-component substitution inside SSD.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)

3. **The paper proposes LFSSD, an extension of SSD. It replaces the Fisher-based parameter importance with the gradient of the squared l2 norm of the model output, so unlearning needs neither labels nor retraining.**
   The modification is simple and well targeted, which suits a tiny-paper format.
   Evidence status: observation.
   Reasoning: The abstract states the substitution directly. This substitution removes the dependence on labels.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity

4. **The paper proposes LFSSD, a variant of Selective Synaptic Dampening (SSD) for machine unlearning. It replaces the Fisher-information importance estimate with the gradient of the squared l2 norm of the model output, so no labels or loss are needed at forgetting time.**
   This is a simple and well-scoped change that suits the tiny-paper format.
   Evidence status: observation.
   Reasoning: The abstract states that the method is a substitution of the importance estimator inside SSD.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity

## Originality

The contribution is combinational. The authors credit the dampening rule to SSD and the importance estimator to Aljundi et al. (2018). The new element is pairing them so that unlearning becomes label-free. This framing is honest, and the scope is appropriate for a tiny paper, but the contribution is incremental rather than a new algorithm. The paper hedges its claim to be the first retraining-free method needing only unlabelled forget samples in the introduction, but not in the conclusion. That claim is checked against only two retraining-free methods, Golatkar et al. and SSD. Zero-shot unlearning (Chundawat et al. 2023b) is cited but not contrasted on its label requirements. The statement that output-sensitivity importance 'has not been applied in unlearning' is an absence claim that the paper does not support with a survey. Whether that claim holds was not assessed here. The 'require only' framing also leaves out that importances computed over the full dataset D must be precomputed and stored.

## Likely impact

Practitioners who must forget data without reliable labels may benefit. The appendix names copyright catalogues and models trained with semi-supervised learning, where pseudo-labels may be untrustworthy. A drop-in, label-free variant of SSD lowers the operational barrier to retraining-free unlearning. Several factors may limit influence. The change is a single-component substitution. Its effectiveness is uneven in subclass settings. Like SSD, it depends on choosing α and λ. Privacy is evaluated only with an entropy-based membership inference attack, which offers limited assurance for regulatory use. The motivating use cases are argued only briefly, and mostly in the appendix.

## Decision-critical concerns

1. **The tables broadly support 'competitive with SSD' on class unlearning. They do not uniformly support 'equally effective as Fisher information', because subclass results are mixed.**
   The class-level results look good. The subclass results diverge in both directions.
   Evidence status: inference.
   Reasoning: In ViT subclass MR, LFSSD leaves Df at 31.42 versus 6.68 for SSD. Both methods are deterministic, so each configuration is a single result. No aggregate comparison is given.
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   - **Why this affects the decision:** How strong the central empirical claim is depends on this.
   - **Actionable revision:** Add an aggregate per-task summary for SSD and LFSSD covering the Df gap to retrain, the Dr drop and the MIA gap. Alternatively, soften 'equally effective' to 'competitive'.
   - **What would resolve it:** An aggregated table showing comparable gaps, or a revised claim scope.

2. **The tables broadly support 'competitive with SSD' for full-class unlearning. Results are mixed for subclass unlearning, which undercuts the claim of being 'equally effective'.**
   Full-class results such as ViT lamp (LFSSD Df 0.00 vs SSD 36.89) favour LFSSD. Subclass results are task dependent.
   Evidence status: inference.
   Reasoning: In the ViT subclass rows, LFSSD's Df differs from SSD's in both directions, and both differ from retrain. 'Equally effective' is therefore not uniformly supported.
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   Source `paper:chars/7514-23701`: Df 96.44±0.00 93.23±1.09 85.45±4.47 46.66±17.88 38.76±7.36 94.10±0.00 86.81±0.00
   - **Why this affects the decision:** The main claim is stated too strongly.
   - **Actionable revision:** Scope the claim per task, and add an aggregate measure such as average distance to retrain, per task.
   - **What would resolve it:** An aggregate comparison by task, plus a softened claim.

3. **The tables broadly support LFSSD being competitive with SSD. However, the claim that it is 'equally effective as Fisher information' is not uniform across settings: ViT subclass Df is high for several classes.**
   Class-forgetting results look strong. Subclass results under ViT are mixed.
   Evidence status: inference.
   Reasoning: In the ViT subclass rows, LFSSD's Df accuracy exceeds SSD's in some cases. The quoted MR row shows 31.42 for LFSSD versus 6.68 for SSD. The table also uses per-task α values. Together this suggests the method is comparable on average rather than equivalent in every setting.
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information
   Source `paper:chars/7514-23701`: Df 96.44±0.00 93.23±1.09 85.45±4.47 46.66±17.88 38.76±7.36 94.10±0.00 86.81±0.00
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   - **Why this affects the decision:** The headline equivalence claim drives how significant the contribution appears.
   - **Actionable revision:** Soften the claim to 'competitive', and summarise where LFSSD underperforms SSD (for example, ViT subclass forgetting).
   - **What would resolve it:** Revised wording, plus aggregated per-setting comparisons that acknowledge the gaps.

4. **The claim that LFSSD is 'equally effective' as Fisher-based SSD is mixed in subclass unlearning. In some cases LFSSD leaves notably more forget-set accuracy than SSD.**
   Results also vary across individual classes, which weakens a blanket claim of equivalence.
   Evidence status: observation.
   Reasoning: In the ViT mushroom subclass case, LFSSD forget-set accuracy is 31.42 versus 6.68 for SSD. In the ViT baby case, LFSSD gives 86.81 against a retrain value of 93.23. These are cases where the two methods diverge.
   Source `paper:chars/7514-23701`: Df 97.05±0.00 26.57±6.41 15.71±12.13 13.01±9.11 0.20±0.36 6.68±0.00 31.42±0.00
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information
   - **Why this affects the decision:** The headline equivalence claim should match the evidence.
   - **Actionable revision:** Qualify 'equally effective' to the full-class setting. Briefly discuss the subclass discrepancies against SSD and the retrain reference.
   - **What would resolve it:** Revised wording, or an aggregate comparison by task showing parity with SSD.

## Questions for the authors

1. **The 'first retraining-free unlearning method to require only the unlabelled forget samples' claim is hedged with 'to the best of our knowledge'. However, the related work cites only one other retraining-free method, Golatkar et al.**
   The paper cites zero-shot unlearning (Chundawat 2023b), but only within the fine-tuning group. Its data and label requirements are not contrasted with LFSSD.
   Evidence status: inference.
   Reasoning: The priority claim is checked against only two retraining-free methods, both described as Fisher- and label-based. The related-work coverage is too narrow to fully support a 'first' claim.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.
   Source `paper:chars/1165-4392`: FisherForgetting from Golatkar et al. (2020) or Selective Synaptic Dampening (SSD) from Foster
et al. (2023)
   - **Why the answer matters:** The headline novelty depends on this priority claim.
   - **Requested response:** Contrast LFSSD's data and label requirements with the cited zero-shot unlearning method and any other label-free approaches.
   - **Answer that would resolve it:** An explicit comparison of requirements showing that no prior method needs only unlabelled forget samples.

2. **The 'first label-free, retraining-free' claim is hedged, but it rests on a short related-work paragraph. The paper itself cites zero-shot unlearning (Chundawat 2023b) without explaining how its own label requirement differs.**
   The priority claim is central to the headline. Its scope should be stated precisely.
   Evidence status: inference.
   Reasoning: The paper groups Chundawat 2023b (which it cites as 'Zero-shot machine unlearning') with the retraining-based methods. It never states that method's label requirements, so the distinction behind the priority claim is not made explicit.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.
   Source `paper:chars/1165-4392`: Chundawat et al.,
2023a;b
   - **Why the answer matters:** If a prior method is also label-free and retraining-free, the 'first' claim must be narrowed.
   - **Requested response:** Add one or two sentences stating, for each cited retraining-free or zero-shot method, whether it needs labels at forgetting time.
   - **Answer that would resolve it:** An explicit comparison showing that the requirements of the cited methods differ from those of LFSSD.

3. **The ten reported repetitions cannot show variability for (LF)SSD, because the method is described as deterministic and its spread is reported as ±0.00.**
   Zero variance for LFSSD across 10 runs suggests the same original model was reused in every run.
   Evidence status: inference.
   Reasoning: Table 1's caption states that (LF)SSD is deterministic and that '±0.0' is omitted. The appendix states that runs are repeated 10 times with mean and standard deviation reported, and Table 4 shows LFSSD values such as 75.67±0.00. Together these premises imply the repetitions vary something that does not affect LFSSD or SSD, such as baseline seeds, but not the trained model or data split. If so, the reported uncertainty covers only the baselines. Comparisons between LFSSD and stochastic baselines would then rest on single-model results for the proposed method.
   Source `review-record:visual/15`: The caption states α=10, λ=1 on Cifar100/20 and that ±0.0 is omitted. The LFSSD and SSD columns show values without ±.
   Source `review-record:visual/21`: Appendix Benchmarks paragraph reads 'Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables.'
   Source `review-record:visual/39`: Table 2 α=10 row: Dr 75.67%, Df 0.00%, MIA 0.00. Table 4 RN Rkt LFSSD: Dr 75.67±0.00, Df 0.00±0.00, MIA 0.00±0.00, caption LFSSD α = 10, λ = 1.
   Source `paper:chars/3752-3837`: unlearning with α =10,
λ =1 on Cifar100/20. (LF)SSD is deterministic, ’±0.0’ omitted.
   Source `paper:chars/10633-10734`: Runs are repeated 10 times for each method, with the mean and standard
deviation shown in the tables.
   Source `paper:chars/15219-15340`: Table 4: Class unlearning on Cifar100. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.
   - **Why the answer matters:** If every comparison uses one original model, the robustness of LFSSD's advantage or parity is not yet established.
   - **Requested response:** State what varies across the 10 repetitions. If feasible, report (LF)SSD results across several independently trained original models or forget/retain splits.
   - **Answer that would resolve it:** A clarification of the repetition protocol, plus non-zero-variance results across independently trained models showing the conclusions hold.

## Decision synthesis

In favour: the idea is simple, clearly stated, and practically motivated. It removes the label requirement from a retraining-free method. Full-class results broadly support competitiveness with SSD, and in some cases favour LFSSD; for example, ViT lamp forget accuracy is 0.00 for LFSSD versus 36.89 for SSD. A single LFSSD setting (α=10, λ=1) is used across benchmarks, which may suggest some robustness of the defaults. Against: the headline claim that the approach is 'equally effective as Fisher information' is not uniformly supported. Subclass results diverge in both directions. In ViT mushroom, forget accuracy is 31.42 for LFSSD versus 6.68 for SSD. In ViT baby, LFSSD gives 86.81 against a retrain value of 93.23. No aggregate comparison is given. The questions most likely to change the assessment are: (1) whether the ten repetitions vary anything that affects (LF)SSD. The ±0.00 spreads, together with the description of the method as deterministic, suggest they may not, in which case comparisons with stochastic baselines rest on single-model results; and (2) how the priority claim differs from zero-shot unlearning and other label-free approaches. Non-blocking improvements: explain how hyperparameters were selected, especially the differing SSD (α=50, λ=0.1) and LFSSD (α=10, λ=1) settings in Table 3; hedge the conclusion's priority and 'robust' wording given the acknowledged α sensitivity; and move the practical motivation into the main text.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The abstract states the problem, the change made, and the outcome in plain language a non-specialist can follow.

**Writing-quality issues**

1. **The headline result is stated only as 'similar' and 'competitive'. The results text never gives the size of the differences, including the cases where forgetting is partial.**
   One plain sentence giving typical gaps to retraining and to SSD, plus the setting where agreement is weakest, would make the takeaway clear.
   - **Suggested revision:** State the central result in one plain sentence with typical magnitudes. Name the settings where forgetting is partial, keeping those results rather than softening them.

2. **The conclusion asserts that the method is 'robust' without pointing to evidence, and it drops the α/λ tuning limitation that the results section acknowledges.**
   Showing rather than asserting the robustness claim would better calibrate the framing.
   - **Suggested revision:** Replace 'robust' with a pointer to the sensitivity evidence, keep the α/λ limitation in the conclusion, and add one sentence on when a practitioner should prefer this method.

3. **Table 1 appears before the abbreviation MIA is defined. MIA is spelled out only in the results text of Section 2, and 'Streisand effect' is explained only by a parenthetical example.**
   Defining the metrics in the Table 1 caption would let the table stand on its own.
   - **Suggested revision:** In the Table 1 caption, define Dr, Df and MIA and say which direction counts as a good value. Explain 'over-forgetting' in plain words.

## Additional improvements (non-blocking)

1. **The claim to be the 'first retraining-free method requiring only unlabelled forget samples' is hedged in the introduction but unhedged in the conclusion. The method also still relies on importances computed over the full dataset D.**
   This is a framing precision issue.
   Evidence status: inference.
   Reasoning: The introduction hedges the claim, but the conclusion drops the hedge. The phrase 'require only' also omits the precomputed importances over D, which must be stored.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.
   Source `paper:chars/6820-7514`: the first retraining free
machine unlearning method to require only the unlabelled input samples for the forget set
   Source `paper:chars/4392-6820`: Fisher information is calculated over D not Dr,
meaning this is only calculated once, and then the train-set may be discarded after.
   - **Suggested revision:** Qualify the claim to note that precomputed full-data importances are needed, and keep the hedge in the conclusion.

2. **LFSSD uses one setting (α=10, λ=1) across benchmarks, while SSD uses α=50, λ=0.1 on the face-unlearning task in Table 3.**
   How the hyperparameters were selected affects how the face-unlearning comparison should be read.
   Evidence status: observation.
   Reasoning: The Table 3 caption gives different hyperparameters for SSD (α=50, λ=0.1) and LFSSD (α=10, λ=1). Tables 1 and 4 use α=10, λ=1 for LFSSD. This pattern could support a robustness claim for LFSSD's defaults. It also means the Table 3 comparison pits a possibly tuned SSD against untuned LFSSD, or the reverse. The captions do not say how either setting was chosen.
   Source `review-record:visual/43`: Captions render α = 50, λ = 0.1; α_RN = 10, α_ViT = 10 with proper subscripts; row labels render as calligraphic D_r, D_f.
   Source `review-record:visual/39`: Table 2 α=10 row: Dr 75.67%, Df 0.00%, MIA 0.00. Table 4 RN Rkt LFSSD: Dr 75.67±0.00, Df 0.00±0.00, MIA 0.00±0.00, caption LFSSD α = 10, λ = 1.
   Source `paper:chars/14882-14924`: SSD: α = 50, λ = 0.1; LFSSD:
α = 10, λ = 1
   Source `paper:chars/15219-15340`: Table 4: Class unlearning on Cifar100. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.
   - **Suggested revision:** Explain how the per-method hyperparameters were chosen. Optionally, report LFSSD with α=50, λ=0.1, or SSD with α=10, λ=1, on the Table 3 task.

3. **The claim that output-sensitivity importance 'has not been applied in unlearning' is an absence assertion with no supporting survey. The experiments support the method's use but not its historical primacy.**
   Hedging this statement would be prudent.

Coverage note: Literature not inspected.
   Evidence status: unassessed.
   Reasoning: The results show the substituted importance measure works. They cannot establish that no prior unlearning work used it.
   Source `paper:chars/1165-4392`: yet it has not been applied in unlearning
   - **Suggested revision:** Hedge the statement or cite a survey supporting it.

4. **The limitations section is brief. It acknowledges hyperparameter reliance, but the conclusion's 'robust and more practically useful' wording overreaches.**
   Evaluation relies on an entropy-based MIA only. That is a weak privacy guarantee for regulatory use cases.
   Evidence status: inference.
   Reasoning: Claiming robustness sits awkwardly with an acknowledged sensitivity to alpha.
   Source `paper:chars/4392-6820`: A shared limitation with SSD is the reliance
on choosing α and λ values
   Source `paper:chars/6820-7514`: LFSSD is lightweight, robust and more practically useful than its predecessors.
   - **Suggested revision:** Temper the robustness wording and note that the MIA metric gives limited guarantees.

5. **The practical motivation for label-free unlearning is plausible but only briefly argued.**
   Moving these scenarios into the main text would strengthen the significance argument.
   Evidence status: observation.
   Reasoning: The appendix gives two concrete use cases: copyright catalogues and models trained with semi-supervised learning.
   Source `paper:chars/7514-23701`: Second, models that were trained with semi-supervised learning
could benefit from our method when we do not want to rely on the accuracy of pseudo labels.
   - **Suggested revision:** Briefly mention these scenarios in the introduction.

## Evidence to examine (advisory)

### Captions: The diagram has three stages. The first is 'Loss-free importance estimation', shown as a 3D surface under 'Approximate parameter importances label-free via output gradients'. The second is 'Selective Synaptic Dampening', which contains 'Protect generalization' and 'Target forget set importance' boxes plus 'Synapse selection (α)' and 'Synaptic dampening (λ)' bars. The third is 'Unlearned model'. The caption below the diagram matches the extracted caption.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption describes replacing SSD's label-dependent importance estimation with a loss-free estimate, and the diagram shows that same pipeline. The α and λ labels match the Section 2 description of selection and dampening hyperparameters.

- Source: `review-record:visual/0`
- Source: `paper:chars/11866-12030`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Reviewer coverage limitation: rendered formulas (paper:p.4)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/2`
- Source: `paper:chars/12582-12620`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Reviewer coverage limitation: budgets (paper:p.4)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/3`
- Source: `paper:chars/12817-12945`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Reviewer coverage limitation: sample counts (paper:p.4)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/4`
- Source: `paper:chars/13353-13403`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: The page renders the set-difference definition D_r = D \ D_f with calligraphic D symbols and subscripts r and f.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered formula is consistent with the extracted text. The flattened subscripts in the extraction are extraction noise.

- Source: `review-record:visual/5`
- Source: `paper:chars/1398-1497`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Rendered formulas: The abstract renders 'l_2 norm of the model output' with a subscript 2 on l.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered l_2 notation is consistent with the extracted text and with the later description of the method using the l2 norm.

- Source: `review-record:visual/6`
- Source: `paper:chars/927-981`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/12`
- Source: `paper:chars/4788-4890`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/13`
- Source: `paper:chars/5992-6041`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Rendered formulas: Ω_i = (1/N) Σ_{k=1}^N ||∂[l_2^2(f(x_k;θ))]/∂θ_i||, which is the gradient of the squared l2 norm.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered formula uses the squared l2 norm, matching the text.

- Source: `review-record:visual/14`
- Source: `paper:chars/5750-5819`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Captions: The caption states α=10, λ=1 on Cifar100/20 and that ±0.0 is omitted. The LFSSD and SSD columns show values without ±.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption matches the table layout.

- Source: `review-record:visual/15`
- Source: `paper:chars/3752-3837`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: budgets (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/16`
- Source: `paper:chars/15647-15731`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: captions (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/17`
- Source: `paper:chars/20462-20535`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: units (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/18`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Sample counts: Appendix Benchmarks paragraph reads 'Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables.'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered run count matches the extracted text.

- Source: `review-record:visual/21`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Units: Text states D_r and D_f in the tables denote accuracy on the respective subset 'in percent'.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered unit (percent) for Dr/Df accuracy matches the extracted text.

- Source: `review-record:visual/22`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Budgets: Text reads 'a model finetuned for 2 epochs on D_r'.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered finetuning budget of 2 epochs matches the extracted text.

- Source: `review-record:visual/23`
- Source: `paper:chars/9926-9962`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Calligraphic D_r appears in 'retrained from scratch on only D_r' and 'finetuned ... on D_r'. Italic D_r and D_f appear in the table-description sentence. All subscripts render legibly.

Scope: paper-only; analysis: visual; evidence status: inference.
The symbols render properly. The calligraphic versus italic font difference is a stylistic inconsistency only and does not change the meaning.

- Source: `review-record:visual/24`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Reviewer coverage limitation: sample counts (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/27`
- Source: `paper:chars/23044-23103`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: captions (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/28`
- Source: `paper:chars/20462-20585`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: captions (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/29`
- Source: `paper:chars/3674-3795`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: units (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/30`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: rendered formulas (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/31`
- Source: `paper:chars/20508-20535`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: sample counts (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/32`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Sample counts: Table 3 caption states one face unlearned per experiment with IDs [1,10,20,30,40] and results aggregated for 5 experiments; table shows RN rows with ± values.

Scope: paper-only; analysis: visual; evidence status: inference.
Five listed IDs match the stated count of 5 experiments.

- Source: `review-record:visual/35`
- Source: `paper:chars/14760-14881`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: sample counts (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/36`
- Source: `paper:chars/10824-10956`
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
- Source: `paper:chars/13295-13404`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Budgets: Table 2 α=10 row: Dr 75.67%, Df 0.00%, MIA 0.00. Table 4 RN Rkt LFSSD: Dr 75.67±0.00, Df 0.00±0.00, MIA 0.00±0.00, caption LFSSD α = 10, λ = 1.

Scope: paper-only; analysis: visual; evidence status: inference.
Hyperparameter settings and rocket results are consistent across tables.

- Source: `review-record:visual/39`
- Source: `paper:chars/15219-15340`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: captions (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/40`
- Source: `paper:chars/4046-4111`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: sample counts (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/41`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Rendered formulas: Captions render α = 50, λ = 0.1; α_RN = 10, α_ViT = 10 with proper subscripts; row labels render as calligraphic D_r, D_f.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered symbols match the extracted text; garbled 'αV iT' is extraction noise.

- Source: `review-record:visual/43`
- Source: `paper:chars/14882-14924`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption and hyperparameters match the extracted text. The extracted text splits the subscript 'ViT' into 'V iT', which is extraction noise.

- Source: `review-record:visual/44`
- Source: `paper:chars/17822-17914`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: budgets (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/45`
- Source: `paper:chars/3674-3795`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: sample counts (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/46`
- Source: `paper:chars/10824-10904`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: units (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/47`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Rendered formulas: The metric column renders calligraphic 𝒟_r and 𝒟_f symbols, and the caption renders α and λ symbols properly.

Scope: paper-only; analysis: visual; evidence status: inference.
The symbols render correctly and match the notation used in the text.

- Source: `review-record:visual/49`
- Source: `paper:chars/10735-10803`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### C1: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/0`

## Direct visual evidence (advisory)

- **agreement**, rendered page 4, captions: The diagram has three stages. The first is 'Loss-free importance estimation', shown as a 3D surface under 'Approximate parameter importances label-free via output gradients'. The second is 'Selective Synaptic Dampening', which contains 'Protect generalization' and 'Target forget set importance' boxes plus 'Synapse selection (α)' and 'Synaptic dampening (λ)' bars. The third is 'Unlearned model'. The caption below the diagram matches the extracted caption.
  Paper quote: Figure 1: Loss-free parameter importance estimation as a replacement for the label-dependent pa-
rameter importance estimation of SSD resulting in the LFSSD method.. The caption describes replacing SSD's label-dependent importance estimation with a loss-free estimate, and the diagram shows that same pipeline. The α and λ labels match the Section 2 description of selection and dampening hyperparameters.
- **agreement**, rendered page 1, rendered formulas: The page renders the set-difference definition D_r = D \ D_f with calligraphic D symbols and subscripts r and f.
  Paper quote: dataset D into a subset of data that needs to be forgotten Df , and the retained data Dr = D \ Df .. The rendered formula is consistent with the extracted text. The flattened subscripts in the extraction are extraction noise.
- **agreement**, rendered page 1, rendered formulas: The abstract renders 'l_2 norm of the model output' with a subscript 2 on l.
  Paper quote: l2 norm of the model output to approximate sensitivity. The rendered l_2 notation is consistent with the extracted text and with the later description of the method using the l2 norm.
- **agreement**, rendered page 2, rendered formulas: Ω_i = (1/N) Σ_{k=1}^N ||∂[l_2^2(f(x_k;θ))]/∂θ_i||, which is the gradient of the squared l2 norm.
  Paper quote: the gradient can be calculated over the squared l2 norm of
the output. The rendered formula uses the squared l2 norm, matching the text.
- **agreement**, rendered page 2, captions: The caption states α=10, λ=1 on Cifar100/20 and that ±0.0 is omitted. The LFSSD and SSD columns show values without ±.
  Paper quote: unlearning with α =10,
λ =1 on Cifar100/20. (LF)SSD is deterministic, ’±0.0’ omitted.. The caption matches the table layout.
- **agreement**, rendered page 3, sample counts: Appendix Benchmarks paragraph reads 'Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables.'
  Paper quote: Runs are repeated 10 times for each method, with the mean and standard
deviation shown in the tables.. The rendered run count matches the extracted text.
- **agreement**, rendered page 3, units: Text states D_r and D_f in the tables denote accuracy on the respective subset 'in percent'.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. The rendered unit (percent) for Dr/Df accuracy matches the extracted text.
- **agreement**, rendered page 3, budgets: Text reads 'a model finetuned for 2 epochs on D_r'.
  Paper quote: a model finetuned for 2 epochs on Dr. The rendered finetuning budget of 2 epochs matches the extracted text.
- **agreement**, rendered page 3, rendered formulas: Calligraphic D_r appears in 'retrained from scratch on only D_r' and 'finetuned ... on D_r'. Italic D_r and D_f appear in the table-description sentence. All subscripts render legibly.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. The symbols render properly. The calligraphic versus italic font difference is a stylistic inconsistency only and does not change the meaning.
- **agreement**, rendered page 5, sample counts: Table 3 caption states one face unlearned per experiment with IDs [1,10,20,30,40] and results aggregated for 5 experiments; table shows RN rows with ± values.
  Paper quote: One face unlearned per experiment [ID 1,10,20,30,40]
and results aggregated for 5 experiments as in Foster et al. (2023).. Five listed IDs match the stated count of 5 experiments.
- **agreement**, rendered page 5, budgets: Table 2 α=10 row: Dr 75.67%, Df 0.00%, MIA 0.00. Table 4 RN Rkt LFSSD: Dr 75.67±0.00, Df 0.00±0.00, MIA 0.00±0.00, caption LFSSD α = 10, λ = 1.
  Paper quote: Table 4: Class unlearning on Cifar100. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.. Hyperparameter settings and rocket results are consistent across tables.
- **agreement**, rendered page 5, rendered formulas: Captions render α = 50, λ = 0.1; α_RN = 10, α_ViT = 10 with proper subscripts; row labels render as calligraphic D_r, D_f.
  Paper quote: SSD: α = 50, λ = 0.1; LFSSD:
α = 10, λ = 1. Rendered symbols match the extracted text; garbled 'αV iT' is extraction noise.
- **agreement**, rendered page 6, captions: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.'
  Paper quote: Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 5, λ = 1.. The rendered caption and hyperparameters match the extracted text. The extracted text splits the subscript 'ViT' into 'V iT', which is extraction noise.
- **agreement**, rendered page 6, rendered formulas: The metric column renders calligraphic 𝒟_r and 𝒟_f symbols, and the caption renders α and λ symbols properly.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset. The symbols render correctly and match the notation used in the text.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 14 |
| Confirmed text-image mismatch (advisory) | 0 |
| Not applicable | 14 |
| Grounding failure: context, citation or readability | 0 |
| Missing or invalid confirmation | 6 |
| Conflicting assessments | 12 |
| Substantive uncertainty | 4 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.

### Human inspection needed

Conflicting assessments and substantive uncertainties are unconfirmed, not author-facing findings. Confirmed mismatches are advisory, not scientific proof.

- **Substantive uncertainty**: `paper:p.2`, rendered_formulas (visual audit observation index 12).
  Observation: Equation 1 is rendered with empty bracket glyphs '[]' in the conditions and in β: '[]_{D_f,i} > α[]_{D,i}' and 'β = min(λ[]_{D,i}/[]_{D_f,i}, 1)'. No importance symbol (for example, a Fisher diagonal) appears inside the brackets.
  Paper quote: Here, α and λ are hyper-parameters, and []Df,i and []Di are the ith element of the diagonal of
the FIM.
  Reason: Rendered formula requires human confirmation; an extraction difference alone is not an authoring defect.

- **Substantive uncertainty**: `paper:p.2`, rendered_formulas (visual audit observation index 13).
  Observation: The text below Eq. 3 reads 'substitute into equation 1 in place of [] and []_f', using empty brackets instead of a named symbol.
  Paper quote: substitute into equation 1 in place of [] and []f.
  Reason: Rendered formula requires human confirmation; an extraction difference alone is not an authoring defect.

- **Conflicting assessments**: `paper:p.2`, budgets (visual audit observation index 16).
  Observation: The Cifar100 lamp row (ResNet18 Dr 76.39/72.89/76.36/76.08) and the Cifar20 row (LFSSD Df 7.29, SSD 0.00) match the appendix Tables 4 and 6.
  Paper quote: lamp Dr 76.39±0.00 72.89±0.34 64.01±0.63 74.76±0.19 73.52±0.48 76.08±0.00 76.36±0.00.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The page-2 values are consistent with the appendix tables.
  First assessment: agreement. The page-2 values are consistent with the appendix tables.
  Second assessment: unresolved. The quoted row comes from the appendix Table 4, which is not on this page. The overlapping values (76.39, 72.89, 76.08, 76.36) are consistent, but the full row cannot be checked here.

- **Conflicting assessments**: `paper:p.2`, captions (visual audit observation index 17).
  Observation: The caption gives α=10 for both Cifar100 and Cifar20, and the Cifar20 rows are reported under that setting. The Cifar20 rows match Table 6 (subclass).
  Paper quote: Table 6: Subclass unlearning on Cifar20. SSD: αRN = 10, αV iT = 25, λ = 1.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): SSD ViT used α=25 for Cifar20 subclass unlearning, which contradicts Table 1's blanket α=10.
  First assessment: mismatch. SSD ViT used α=25 for Cifar20 subclass unlearning, which contradicts Table 1's blanket α=10.
  Second assessment: unresolved. Table 6 is in the appendix and is not on this page, so its caption cannot be checked here.

- **Substantive uncertainty**: `paper:p.2`, units (visual audit observation index 18).
  Observation: Table 1 reports Dr, Df and MIA values with no unit shown.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent..
  Reason: The appendix gives Dr and Df in percent, but MIA's unit or scale is not stated.

- **Conflicting assessments**: `paper:p.7`, captions (visual audit observation index 29).
  Observation: Table 6 caption gives LFSSD α = 10, λ = 1 for Cifar20 subclass unlearning; the ViT lamp row shows LFSSD Df 24.05.
  Paper quote: Table 1: Full- (class lamp) and subclass (lamp is part of electrical devices) unlearning with α =10,
λ =1 on Cifar100/20..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Table 1 states SSD used α=10 for subclass, but Table 6 caption gives SSD α_ViT = 25 while reproducing the same ViT subclass SSD values (14.58, 95.54, 3.2) in Table 1; the stated SSD hyperparameters for these values are inconsistent between captions.
  First assessment: mismatch. Table 1 states SSD used α=10 for subclass, but Table 6 caption gives SSD α_ViT = 25 while reproducing the same ViT subclass SSD values (14.58, 95.54, 3.2) in Table 1; the stated SSD hyperparameters for these values are inconsistent between captions.
  Second assessment: unresolved. The Table 1 caption is on another page, so it cannot be checked from this image.

- **Conflicting assessments**: `paper:p.7`, units (visual audit observation index 30).
  Observation: Values shown as plain numbers with ± and no % sign; metrics Dr, Df, MIA.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Values lie in 0–100 consistent with percentages as stated in the appendix.
  First assessment: agreement. Values lie in 0–100 consistent with percentages as stated in the appendix.
  Second assessment: unresolved. The values fall within the 0–100 range, which is consistent with percentages. However, the page does not state the unit, and the definition is on another page.

- **Conflicting assessments**: `paper:p.7`, sample_counts (visual audit observation index 32).
  Observation: Table 7 SSD and LFSSD entries show nonzero std (e.g., 88.68±3.36, 89.82±2.30), while Table 6 SSD/LFSSD show ±0.00.
  Paper quote: Runs are repeated 10 times for each method, with the mean and standard
deviation shown in the tables..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Nonzero std for deterministic methods in random forgetting is plausible since forget sets vary across runs; consistent with repeated-run reporting.
  First assessment: agreement. Nonzero std for deterministic methods in random forgetting is plausible since forget sets vary across runs; consistent with repeated-run reporting.
  Second assessment: unresolved. The ± notation is consistent with reporting mean and standard deviation. The 10-run count is not visible on this page; it is stated elsewhere in the paper.

- **Conflicting assessments**: `paper:p.5`, sample_counts (visual audit observation index 36).
  Observation: Table 3 SSD and LFSSD columns show nonzero standard deviations (e.g., 98.42±0.13, 98.15±0.20, LFSSD MIA 0.38±0.58).
  Paper quote: Since SSD (and therefore LFSSD) is deterministic, there is no standard deviation

3Accepted as a Tiny Paper at ICLR 2024 (Preprint).
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Paper states deterministic methods have no std across repeated runs; nonzero std here plausibly reflects aggregation over 5 face IDs rather than repeated runs, but the table does not distinguish this, so the stated ± semantics are inconsistent with the general claim.
  First assessment: mismatch. Paper states deterministic methods have no std across repeated runs; nonzero std here plausibly reflects aggregation over 5 face IDs rather than repeated runs, but the table does not distinguish this, so the stated ± semantics are inconsistent with the general claim.
  Second assessment: unresolved. The quoted text is not on this page, so it cannot be checked here.

- **Conflicting assessments**: `paper:p.5`, units (visual audit observation index 37).
  Observation: Table 2 Dr and Df Accuracy shown with % signs; MIA column shown without units.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Accuracy columns rendered in percent, consistent with text.
  First assessment: agreement. Accuracy columns rendered in percent, consistent with text.
  Second assessment: unresolved. Table 2 agrees with the percent claim. Tables 3 and 4 do not show units, though their values are consistent with percentages. The defining sentence is not on this page, so the claim cannot be fully confirmed here.

- **Conflicting assessments**: `paper:p.5`, captions (visual audit observation index 38).
  Observation: Caption: λ = 1, CIFAR100 rocket class; α rows 1,5,10,25,50; values without ±.
  Paper quote: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50]..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Rendered α range and λ match text; no ± consistent with determinism claim.
  First assessment: agreement. Rendered α range and λ match text; no ± consistent with determinism claim.
  Second assessment: unresolved. Table 2 is consistent with λ fixed at 1 and α spanning 1 to 50. However, the search-procedure sentence itself is on another page, so whether this table fully represents that search cannot be confirmed here.

- **Conflicting assessments**: `paper:p.5`, captions (visual audit observation index 40).
  Observation: Table 4 RN/ViT lamp rows: RN LFSSD Dr 76.36, SSD 76.08; ViT SSD Df 36.89, LFSSD MIA 2.20.
  Paper quote: Df 70.49±0.00 0.00±0.00 0.00 0.00 97.22±0.00 0.00±0.00 0.00 36.89.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Lamp values on page 5 match Table 1 values.
  First assessment: agreement. Lamp values on page 5 match Table 1 values.
  Second assessment: unresolved. The quoted Table 1 row is not on this page. Related Table 4 values are consistent with it, but the row itself cannot be checked here.

- **Substantive uncertainty**: `paper:p.5`, sample_counts (visual audit observation index 41).
  Observation: RN baby SSD Dr shows '44.05*±0.00' with an asterisk; no footnote visible on page 5.
  Paper quote: (not grounded).
  Reason: Asterisk meaning is not explained in the supplied text or visible page, so its interpretation cannot be confirmed.

- **Conflicting assessments**: `paper:p.6`, budgets (visual audit observation index 45).
  Observation: The Table 5 caption shows LFSSD α = 5, λ = 1 for Cifar20 full-class unlearning.
  Paper quote: Table 1: Full- (class lamp) and subclass (lamp is part of electrical devices) unlearning with α =10,
λ =1 on Cifar100/20..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Table 5 uses α=5 for LFSSD on Cifar20 class unlearning. Table 1 states α=10 for Cifar100/20. However, Table 1's Cifar20 rows report subclass results, which match Table 6 (α=10), so this may not be a true conflict. It is noted as a hyperparameter inconsistency only if Table 1's α is read as covering Cifar20 class unlearning.
  First assessment: mismatch. Table 5 uses α=5 for LFSSD on Cifar20 class unlearning. Table 1 states α=10 for Cifar100/20. However, Table 1's Cifar20 rows report subclass results, which match Table 6 (α=10), so this may not be a true conflict. It is noted as a hyperparameter inconsistency only if Table 1's α is read as covering Cifar20 class unlearning.
  Second assessment: unresolved. Table 1 and its hyperparameter settings are not present on page 6, so they cannot be checked here.

- **Conflicting assessments**: `paper:p.6`, sample_counts (visual audit observation index 46).
  Observation: Rows show RN and ViT blocks, each with 5 classes (ED, NS, people, veg, Veh2) and 3 metrics (D_r, D_f, MIA). Deterministic SSD and LFSSD columns show ±0.00.
  Paper quote: Since SSD (and therefore LFSSD) is deterministic, there is no standard deviation.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The SSD and LFSSD columns all render ±0.00, which is consistent with the stated deterministic behavior.
  First assessment: agreement. The SSD and LFSSD columns all render ±0.00, which is consistent with the stated deterministic behavior.
  Second assessment: unresolved. The ±0.00 values are consistent with deterministic methods, but the page does not show run counts or state determinism, so the claim itself cannot be confirmed from this image.

- **Conflicting assessments**: `paper:p.6`, units (visual audit observation index 47).
  Observation: D_r and D_f values are in the 0–100 range with no % sign, e.g., RN ED D_r baseline 82.56±0.00 and LFSSD 83.19±0.00.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The values are consistent with percentages, and the rendered cells match the extracted values I spot-checked (e.g., ViT ED D_f SSD 53.53, ViT Veh2 MIA LFSSD 9.12).
  First assessment: agreement. The values are consistent with percentages, and the rendered cells match the extracted values I spot-checked (e.g., ViT ED D_f SSD 53.53, ViT Veh2 MIA LFSSD 9.12).
  Second assessment: unresolved. Values are compatible with percentages, but the table shows no explicit unit, so percent is not directly confirmed on this page.



## Artifact evidence reconciliation (supplementary)

Literal checks of explicitly linked shipped evidence, not scientific validation. The independent paper assessment is unchanged.

- **unresolved**: C1 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.

Only uniquely quoted, explicitly linked scalar numeric_close claims are compared.
Only explicit tabular metric/unit/context mappings are compared; other layouts remain unresolved. Semantic interpretation and causal validity need human review.
Producer narratives, code reads and numeric agreement are not reproduction.
Undeclared evidence is not missing content; packaging is not scientific criticism.

## Review scope and coverage

Selected scope: **artifact-informed**.
LLM provider: redacted-provider; model: redacted-model.

- contribution digest: completed
- visual inspection: incomplete
- visual integration: completed
- paper review: completed
- reproduction: not-requested
- artifact reconciliation: incomplete
- run evidence: incomplete
- artifact visual inspection: unavailable
- artifact checks: completed
- reference lookup: not-requested
- contribution review: completed

No submission code was executed.

**Coverage notes**

- Visual inspection incomplete: Image analysis is advisory; unmatched or omitted evidence is unassessed.
- Additional analysis diagnostics are retained in run.json (raw model responses omitted from this copy); incomplete coverage is not evidence of paper quality.
