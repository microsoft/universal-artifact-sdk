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

The paper proposes LFSSD, a variant of Selective Synaptic Dampening (SSD) for machine unlearning. It replaces SSD's Fisher-information importance estimate with the gradient of the squared l2 norm of the model output, a sensitivity measure from Aljundi et al. (2018). As a result, the method needs neither retraining nor labels for the forget samples. The selection and dampening rule of SSD is otherwise unchanged. The method is evaluated on ResNet18 and ViT across class, subclass, random-sample and face unlearning, with SSD, retraining and other baselines as comparisons.

## Contributions

1. **Loss-Free Selective Synaptic Dampening (LFSSD) method.** An extension of Selective Synaptic Dampening that replaces Fisher-information parameter importance with the gradient of the squared l2 norm of the model output, removing the need for loss or ground-truth labels.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unresolved*
2. **Retraining- and label-free unlearning needing only unlabelled forget samples.** The first retraining-free unlearning method that requires only unlabelled forget-set inputs at forgetting time, without long-term storage of the retain set, labels, or forget-set loss.
   *Claim support (inferred links): unassessed · Significance: supported · Originality: unresolved*
3. **Empirical evaluation against retraining and SSD baselines.** Experiments on ResNet18 and Vision Transformer across full-class, subclass, random and face unlearning show LFSSD yields scores similar to a retrained model and competitive with SSD.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unresolved*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: Loss-Free Selective Synaptic Dampening (LFSSD) method

**Claim support (inferred links): contested**
- Linked claims:
  - claim-2 (inferred by the paper adapter's extractor, not declared by the authors): LFSSD produces scores similar to a model retrained on only Dr and is competitive with SSD.
  - claim-3 (inferred by the paper adapter's extractor, not declared by the authors): Loss-free sensitivity-based parameter dampening is as effective as Fisher information without labelled data.
  - claim-11 (inferred by the paper adapter's extractor, not declared by the authors): Face unlearning results on PINS for LFSSD vs baselines.
  - claim-9 (inferred by the paper adapter's extractor, not declared by the authors): LFSSD has similar compute time to SSD.
- Across most tables, LFSSD's results track SSD and the retrained model. However, the claim that it is 'equally effective' is broader than the subclass results support.
- The claim of similar compute time to SSD is asserted, but no timing measurements are reported.
- Both the 'equally effective as Fisher' claim and the 'similar compute time' claim rest on informal assertion. No timing data or controlled head-to-head ablation is reported.
- Sources: paper:chars/1165-4392, paper:chars/7514-23701

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The method combines two existing components: SSD's dampening rule and the Memory Aware Synapses sensitivity estimator. The paper states this provenance openly. The novelty lies in this combination and in applying it to unlearning.
- The authors frame the originality as a transfer: the importance estimator comes from continual learning, and the claimed novelty is applying it to unlearning. They do not claim to have invented the estimator.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/4392-6820

Paper’s wording: “Therefore, we propose a novel extension of SSD that does not require access to the loss or ground truth labels, which we refer to as Loss-Free Selective Synaptic Dampening (LFSSD).”

### Contribution 2: Retraining- and label-free unlearning needing only unlabelled forget samples

**Claim support (inferred links): unassessed**
- Linked claims:
  - claim-2 (inferred by the paper adapter's extractor, not declared by the authors): LFSSD produces scores similar to a model retrained on only Dr and is competitive with SSD.
  - claim-3 (inferred by the paper adapter's extractor, not declared by the authors): Loss-free sensitivity-based parameter dampening is as effective as Fisher information without labelled data.
  - claim-11 (inferred by the paper adapter's extractor, not declared by the authors): Face unlearning results on PINS for LFSSD vs baselines.
  - claim-8 (inferred by the paper adapter's extractor, not declared by the authors): LFSSD performance drops sharply at too aggressive/conservative alpha but has a wide well-performing plateau.
  - claim-4 (inferred by the reviewer, not declared by the authors): LFSSD is the first retraining-free unlearning method requiring only unlabelled forget samples.
  - claim-5 (inferred by the reviewer, not declared by the authors): LFSSD is lightweight, robust and more practically useful than predecessors.
  - claim-10 (inferred by the reviewer, not declared by the authors): Retraining-based methods cost O(N·b_retain·p), much larger than SSD/LFSSD.
- No grounded finding addressed this.

**Significance: supported**
- Removing the label requirement has plausible practical utility. The paper names copyright catalogues and semi-supervised models as use cases, but neither scenario is evaluated.
- Removing the label requirement extends SSD-style unlearning to practical scenarios that the authors motivate.
- Sources: paper:chars/7514-23701

**Originality: unresolved**
- The primacy claim of being 'first retraining-free method requiring only unlabelled forget samples' is hedged with 'to the best of our knowledge'. However, the related-work discussion in this paper is brief, and the claim needs sharper scoping.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/1165-4392, paper:chars/4392-6820

Paper’s wording: “To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only the unlabelled forget samples at forgetting time.”

### Contribution 3: Empirical evaluation against retraining and SSD baselines

**Claim support (inferred links): contested**
- Linked claims:
  - claim-2 (inferred by the reviewer, not declared by the authors): LFSSD produces scores similar to a model retrained on only Dr and is competitive with SSD.
  - claim-11 (inferred by the reviewer, not declared by the authors): Face unlearning results on PINS for LFSSD vs baselines.
  - claim-6 (inferred by the reviewer, not declared by the authors): Evaluation uses ResNet18 and Vision Transformer.
  - claim-8 (inferred by the reviewer, not declared by the authors): LFSSD performance drops sharply at too aggressive/conservative alpha but has a wide well-performing plateau.
- LFSSD's results are broadly close to SSD and retrain, but it is not uniformly 'similar to retrain'. In several Cifar20 subclass cases, forget accuracy diverges markedly from retrain.
- Sources: paper:chars/7514-23701, paper:chars/4392-6820

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The empirical-evaluation contribution follows existing benchmark protocols, so it is not novel in itself. It serves as validation of the method.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7514-23701

Paper’s wording: “The results show that LFSSD produces scores similar to that of a model trained on only Dr, and is competitive with state-of-the-art methods such as SSD”

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

1. **The paper proposes LFSSD, a variant of Selective Synaptic Dampening that replaces Fisher-information importance with the gradient of the squared l2 output norm (from Aljundi et al., 2018). This makes unlearning both retraining-free and label-free.**
   This is a simple, clearly scoped tiny-paper contribution. Its value lies in removing the dependency on labels.
   Evidence status: observation.
   Reasoning: The quote states the single methodological change relative to SSD.
   Source `paper:chars/1165-4392`: LFSSD replaces the Fisher-based importance estimation with an approximation of the sensitivity of
the model to perturbations of each parameter

2. **The paper proposes LFSSD, a retraining-free unlearning method. It extends SSD by replacing Fisher-information importance with the gradient of the squared l2 norm of the model output, so labels are not needed.**
   This is a short Tiny Paper whose contribution is a simple, practical substitution inside an existing algorithm.
   Evidence status: observation.
   Reasoning: The abstract states the method and its distinguishing property directly.
   Source `paper:chars/284-1165`: We present a machine unlearning approach that is both retraining- and label-free.
   Source `paper:chars/284-1165`: substituting the diagonal of the Fisher information matrix for the gradient of the
l2 norm of the model output to approximate sensitivity

3. **The authors frame LFSSD as a focused extension of their own SSD method. It swaps the Fisher-based importance estimate for the output-norm sensitivity measure of Aljundi et al. (2018). The novelty claimed is the transfer of this measure into unlearning, not a new sensitivity measure.**
   The originality is incremental but stated honestly. The contribution fits the Tiny Paper format.
   Evidence status: inference.
   Reasoning: The paper attributes the importance measure to Aljundi et al. and attributes the dampening step to SSD. The original element is therefore their combination and the label-free use case. The paper states the difference from SSD clearly: the importance estimator changes and the selection/dampening rule stays the same. Whether the measure has truly never been applied to unlearning is an author-reported claim. I have not verified it against the literature.
   Source `paper:chars/1165-4392`: Such importance estimation has been shown to be effective in continual learning (Aljundi et al.,
2018), yet it has not been applied in unlearning.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)

4. **The tables broadly support the claim that LFSSD is competitive with SSD, retrain, and the other baselines across ResNet18 and ViT on class, subclass, random, and face unlearning.**
   The benchmark breadth is reasonable for the format.
   Evidence status: observation.
   Reasoning: On ViT lamp, LFSSD reaches 0.00 Df accuracy while SSD is left at 36.89. Retain (Dr) accuracy is close to baseline.
   Source `paper:chars/1165-4392`: Df 70.49±0.00 0.00±0.00 0.00 0.00 97.22±0.00 0.00±0.00 0.00 36.89
   Source `paper:chars/7514-23701`: Runs are repeated 10 times for each method

## Originality

The originality is incremental but honestly framed. The sensitivity measure is attributed to Aljundi et al. (2018), and the dampening procedure to the authors' prior SSD work. The new element is applying this measure to unlearning and the label-free use case this allows. The paper's statement that the measure has not been applied to unlearning is the authors' own claim. It was not verified against the literature for this review. The claim to be the 'first retraining-free method requiring only unlabelled forget samples' is hedged in the introduction ('To the best of our knowledge') but stated without the hedge in the conclusion. The related-work discussion is too brief to delimit this claim. In particular, it does not explain how LFSSD's label requirements differ from those of cited zero-shot unlearning work (Chundawat et al. 2023b). The primacy claim should be treated as unestablished until this comparison is made.

## Likely impact

Practitioners who must handle deletion requests where forget samples arrive without labels could benefit from this method. It keeps SSD's low cost and avoids retraining. Because the change is a simple substitution inside an existing algorithm, it is easy to adopt and to combine with other work on importance-based unlearning. Several factors may limit its influence. Performance depends strongly on α, which changes by task (3.5, 5 and 10). Selecting α appears to require evaluating labelled forget and retain accuracy, which is in tension with the label-free framing. The importance over the full training set D is precomputed, so the claim that the training set can be discarded depends on that one-time step. The privacy evidence rests on a single entropy-based membership inference attack.

## Decision-critical concerns

1. **The claim that LFSSD is 'equally effective as Fisher information' is broadly supported in class unlearning. However, ViT subclass results show cases where LFSSD's forget-set accuracy diverges from retrain behaviour.**
   Comparisons are reported per class without any aggregate measure such as average distance to retrain. This makes 'equally effective' and 'competitive' hard to assess.
   Evidence status: inference.
   Reasoning: In ViT subclass 'baby', retraining yields an MIA of 77.37 and SSD yields 77.20, while LFSSD yields 1.60. By the paper's own criterion of similarity to retrain, this is a mismatch. The results are therefore mixed, not uniformly equivalent.
   Source `paper:chars/1165-4392`: Here, we show this new approach to dampening
important parameters is equally effective as Fisher information, without relying on labelled data.
   Source `paper:chars/7514-23701`: Df 96.44±0.00 93.23±1.09 85.45±4.47 46.66±17.88 38.76±7.36 94.10±0.00 86.81±0.00
MIA 91.60±0.00 77.37±0.03 66.57±0.07 0.03±0.00 0.93±0.01 77.20±0.00 1.60±0.00
   - **Why this affects the decision:** The headline claim may be overstated.
   - **Actionable revision:** Report an aggregate gap-to-retrain metric (for Dr, Df and MIA) for SSD versus LFSSD per task. Qualify 'equally effective' where LFSSD diverges.
   - **What would resolve it:** A summary table showing comparable mean absolute deviation from retrain for LFSSD and SSD.

2. **The primacy claim ('first retraining-free method requiring only unlabelled forget samples') is hedged in the introduction. The conclusion repeats it without the hedge. The related-work discussion is too short to substantiate it, and it does not address other label-free or zero-shot unlearning work.**
   The primacy claim is central to the paper's significance argument, but the paper does not delimit it against nearby work.
   Evidence status: inference.
   Reasoning: The introduction qualifies the claim with 'To the best of our knowledge'; the conclusion asserts it categorically. The paper cites Chundawat et al. 2023b ('Zero-shot machine unlearning') only in a list of retraining-based methods. It does not explain how the label requirements of that work differ from LFSSD's. I have not inspected the cited works.
   Source `paper:chars/1165-4392`: To the best of our knowledge, LFSSD is the first retraining-free unlearning method to require only
the unlabelled forget samples at forgetting time.
   Source `paper:chars/6820-7514`: we presented a novel extension of existing literature that is the first retraining free
machine unlearning method to require only the unlabelled input samples for the forget set.
   - **Why this affects the decision:** If a prior label-free, retraining-free method exists, the headline novelty shrinks to the choice of estimator.
   - **Actionable revision:** Make the conclusion's primacy claim consistent with the hedged introduction. Add one or two sentences stating which existing retraining-free methods (e.g., FisherForgetting, SSD) require labels or loss, and how zero-shot or other label-free unlearning methods differ, such as by needing retraining or class labels.
   - **What would resolve it:** An explicit comparison table or paragraph covering the data and label requirements of each cited retraining-free method and of label-free alternatives.

3. **Hyperparameters were tuned on the evaluation tasks without a held-out protocol, and α varies by task. This undercuts the label-free practicality claim.**
   The values used differ by task: α=3.5, 5, and 10.
   Evidence status: inference.
   Reasoning: α=1 collapses Dr to 16.87% and α=50 fails to forget (Df 71.88%). Choosing α appears to require evaluating Df/Dr accuracy, which needs labels. That is in tension with the label-free framing.
   Source `paper:chars/7514-23701`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   Source `paper:chars/7514-23701`: 1 16.87% 0.00% 26.60
   Source `paper:chars/4392-6820`: A shared limitation with SSD is the reliance
on choosing α and λ values that balance forgetting and model performance.
   - **Why this affects the decision:** Practical label-freeness depends on whether α can be chosen without labels.
   - **Actionable revision:** State how α would be selected without labels at deployment time, or report results with a single fixed α across all tasks.
   - **What would resolve it:** A label-free selection rule, or fixed-α results that remain competitive.

4. **The 'equally effective' and 'robust' claims are weakened by ViT subclass results. In several rows LFSSD leaves substantial forget-set accuracy, in some cases far above retrain.**
   Mixed agreement with the retrain reference on the subclass ViT task.
   Evidence status: inference.
   Reasoning: For ViT baby, LFSSD Df stays near retrain (86.81 vs 93.23), yet its MIA is 1.60 against retrain's 77.37. So similarity to retrain is inconsistent across metrics. In other rows, such as MR, LFSSD Df is 31.42 while retrain is 26.57. This variability does not justify blanket claims of robustness and equivalence.
   Source `paper:chars/7514-23701`: Df 96.44±0.00 93.23±1.09 85.45±4.47 46.66±17.88 38.76±7.36 94.10±0.00 86.81±0.00
   Source `paper:chars/7514-23701`: MIA 91.60±0.00 77.37±0.03 66.57±0.07 0.03±0.00 0.93±0.01 77.20±0.00 1.60±0.00
   Source `paper:chars/6820-7514`: LFSSD is lightweight, robust and more practically useful than its predecessors.
   - **Why this affects the decision:** The central effectiveness claim is overstated as written.
   - **Actionable revision:** Qualify the claims of being 'equally effective' and 'robust'. Add a short discussion of the subclass/ViT cases where LFSSD diverges from retrain on Df or MIA.
   - **What would resolve it:** Revised wording, or an aggregate distance-to-retrain metric showing parity with SSD.

## Questions for the authors

1. **Hyperparameters were tuned differently for the two methods. SSD used values taken from prior work, while LFSSD's α was searched per task. The 'label-free' framing also leaves unclear how α is selected without labels.**
   The paper does not state how α would be chosen in a deployment where no labels are available.
   Evidence status: inference.
   Reasoning: The sensitivity table shows performance collapsing at α=1 and α=50. Choosing α appears to require evaluating Dr and Df accuracy, which needs labels. This could undercut the label-free claim in practice.
   Source `paper:chars/7514-23701`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   Source `paper:chars/7514-23701`: 1 16.87% 0.00% 26.60
   - **Why the answer matters:** If α selection requires labelled data, the label-free advantage weakens.
   - **Requested response:** Describe a label-free α selection procedure, or acknowledge the dependence on labels for tuning.
   - **Answer that would resolve it:** A label-free heuristic, or evidence that a fixed α transfers across datasets.

2. **Does computing importance over the full D still require labels or retained data access, and is a single MIA enough to support privacy claims?**
   If the authors confirm that D-importance is label-free and add a stronger attack (e.g., LiRA), confidence in the privacy claims rises.
   Evidence status: inference.
   Reasoning: Importance over D is precomputed, so the claim of no storage holds only if the precomputation is done once. The privacy evidence rests on a single entropy-based MIA.
   Source `paper:chars/4392-6820`: meaning this is only calculated once, and then the train-set may be discarded after.
   Source `paper:chars/7514-23701`: logistic regression is used to classify samples as seen or unseen for a
given model, based the entropy of the model outputs
   - **Why the answer matters:** Bears on how much privacy assurance and practicality the method actually provides.
   - **Requested response:** Clarify the requirements of the precomputation step. Optionally add a stronger membership inference attack.
   - **Answer that would resolve it:** A clarification, plus results under an additional attack.

## Decision synthesis

On the positive side, the contribution is clearly specified (Eq. 3), fits the Tiny Paper format, and is evaluated over a reasonable range of architectures and unlearning scenarios with repeated runs. In class unlearning the tables broadly support competitiveness with SSD and retraining. In some rows LFSSD forgets more completely than SSD while retain accuracy stays close to baseline; for example, on ViT lamp LFSSD reaches 0.00 forget accuracy against SSD's 36.89. On the negative side, the strongest wording ('equally effective as Fisher information', 'robust') goes beyond the evidence. The ViT subclass results are mixed. For 'baby', LFSSD's forget accuracy is close to retraining (86.81 vs 93.23), but its MIA is 1.60 against 77.37 for retraining and 77.20 for SSD, so its similarity to retraining is inconsistent across metrics. Results are reported per class without an aggregate distance-to-retrain measure. Hyperparameter handling is the most decision-relevant concern. LFSSD's α was searched per task with λ fixed at 1, while SSD's values came from prior work. The sensitivity sweep covers only CIFAR100 rocket: α=1 collapses retain accuracy to 16.87% and α=50 fails to forget. The paper does not describe a label-free way to choose α. Score-changing questions for the authors: (1) How would α be selected in deployment without labels, and was it tuned on evaluation outcomes? (2) Does computing importance over D require labels or retained data access beyond a one-time precomputation? (3) Can the privacy claims be supported with a stronger attack, such as LiRA? (4) How does LFSSD relate to prior label-free or zero-shot unlearning work, and is the primacy claim justified? Non-blocking improvements: soften 'equally effective' and discuss the ViT subclass cases; report an aggregate metric; extend the α/λ sensitivity analysis to other classes and to ViT; compare the importance rankings produced by the two measures; and document how the per-table α values were chosen.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The abstract states the problem, the method change, and the main result in plain, readable terms.

**Writing-quality issues**

1. **'Competitive' hides mixed results. The prose does not tell readers where LFSSD falls behind SSD or retraining.**
   Readers must decode the table themselves to see where LFSSD diverges from retraining.
   - **Suggested revision:** Add one or two sentences summarizing where LFSSD matches retraining and where it deviates, for example in subclass forget-set accuracy.

2. **The conclusion's claim that LFSSD is "robust and more practically useful than its predecessors" asserts qualities rather than demonstrating them.**
   The appendix sensitivity table could back a narrower claim, such as a wide plateau of good α values.
   - **Suggested revision:** Replace 'robust' with the specific demonstrated property, for example 'stable across α in [5,25] on the tested task', and cite Table 2.

3. **The appendix states "Figure 1: Loss-free parameter importance estimation as a replacement for the label-dependent pa-
rameter importance estimation of SSD resulting in the LFSSD method." However, the evidence does not show the main text cross-referencing Figure 1.**
   Figure placement was judged only from extracted text.
   - **Suggested revision:** Reference Figure 1 from Section 2, or move it there if page limits allow.

## Additional improvements (non-blocking)

1. **The LFSSD contribution's main claims are supported by the tables, with the subclass/ViT caveats noted above.**
   Partial support for the claims.
   Evidence status: inference.
   Reasoning: See the evaluation findings above.
   Source `paper:chars/4392-6820`: is competitive with state-of-the-art methods such as SSD, while being the first
method to require no labelled data and no retraining.
   - **Suggested revision:** None additional.

2. **The tables broadly support the claim of competitiveness with SSD. However, results are mixed for subclass forgetting on ViT, and only alpha is tuned, with lambda fixed at 1.**
   Consider softening 'equally effective' and briefly discussing the ViT subclass cases.
   Evidence status: observation.
   Reasoning: Several rows show LFSSD comparable to SSD or better on Dr. In some ViT subclass rows, though, the forget accuracy is far above the retrain value. In addition, the table shows a sharp Dr collapse at alpha=1. These observations support 'competitive' but not 'equally effective as Fisher information' in all settings.
   Source `paper:chars/1165-4392`: Df 72.66±0.00 22.95±4.72 7.29 0.00 89.58±0.00 34.55±8.62 24.05 14.58
   Source `paper:chars/7514-23701`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   - **Suggested revision:** Qualify the 'equally effective' wording and discuss the ViT subclass outliers.

3. **The substitution is clearly specified in Eq. 3, and the results tables use it. Evidence that the substitution itself drives success comes only from comparison with SSD.**
   A comparison of the importance rankings from the two measures would strengthen the claim.
   Evidence status: observation.
   Reasoning: The method is fully specified and was evaluated against its Fisher-based counterpart.
   Source `paper:chars/4392-6820`: Which we can calculate over D and Df and substitute into equation 1
   - **Suggested revision:** Optionally report the correlation between the Ω and FIM importances.

4. **The table captions report different SSD and LFSSD hyperparameters for each unlearning setting. The paper should explain how these values were chosen.**
   The α values differ across Tables 5–7 for both SSD and LFSSD. The paper does not describe the selection procedure in the quoted text.
   Evidence status: inference.
   Reasoning: The captions confirmed by the visual check list different values for each setting. LFSSD uses α = 5 for Cifar20 class unlearning (Table 5), α = 10 for Cifar20 subclass unlearning (Table 6) and α = 3.5 for Cifar10 random-sample unlearning (Table 7). SSD uses α_ViT = 10 in Table 5 and α_ViT = 25 in Table 6. These are reported settings, not errors. However, because α changes with the scenario, the comparisons depend on how each value was chosen. If α was tuned using forget-set or test outcomes, the reported trade-offs may be optimistic for practical use, where tuning per request may not be possible.
   Source `review-record:visual/36`: Caption: 'Subclass unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1. MR: mushroom, Rkt: Rocket.' The rows are RN/ViT × baby, lamp, MR, Rkt, sea.
   Source `review-record:visual/40`: The symbols render correctly as calligraphic D_r and D_f, and as α_RN, α_ViT, α = 3.5, and λ = 1.
   Source `review-record:visual/42`: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' The rows are labeled ED, NS, people, veg, and Veh2 for both RN and ViT.
   Source `paper:chars/20462-20585`: Table 6: Subclass unlearning on Cifar20. SSD: αRN = 10, αV iT = 25, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.
   Source `paper:chars/23044-23147`: Table 7: Random sample unlearning on Cifar10 (100 samples). SSD: α = 10 , λ = 1 ; LFSSD:
α = 3.5, λ = 1
   Source `paper:chars/17822-17991`: Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 5, λ = 1.
ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.
   - **Suggested revision:** State how α (and λ) were selected for each setting and which data were used for selection. Report sensitivity of the results to α, or results with a single shared α.

5. **The LFSSD hyperparameter evidence is narrow: λ is fixed at 1, and α sensitivity is shown for only one CIFAR100 class (rocket). The selected α = 10 is then reused across the class-unlearning results.**
   Tables 2 and 4 show that the sensitivity sweep is limited to one class with λ fixed. It is unclear whether α = 10 transfers to other forget classes and to ViT, or whether varying λ changes the retain/forget trade-off.
   Evidence status: inference.
   Reasoning: Record 28 states the search kept λ fixed at 1 and varied α over [1, 50]. Record 27 shows Table 2's sensitivity analysis covers only rocket-class unlearning with λ = 1. Record 31 shows Table 4 uses LFSSD α = 10, λ = 1 for multiple classes (mushroom, rocket) and both architectures. Together, these records suggest the robustness of α = 10 across classes, architectures and λ values is not shown in these tables.
   Source `review-record:visual/27`: Caption reads 'Sensitivity analysis for LFSSD parameter α with λ = 1 on CIFAR100 rocket class unlearning. LFSSD is deterministic, thus no ± reported.' Table rows α=1,5,10,25,50 show no ± values.
   Source `review-record:visual/28`: α values span 1 to 50 with λ fixed at 1.
   Source `review-record:visual/31`: Caption renders α_RN = 10, α_ViT = 10, λ = 1 for SSD; LFSSD: α = 10, λ = 1. Metric rows render as calligraphic D_r and D_f.
   Source `paper:chars/14433-14576`: Table 2: Sensitivity analysis for LFSSD parameter α with λ = 1 on CIFAR100 rocket class
unlearning. LFSSD is deterministic, thus no ± reported.
   Source `paper:chars/13295-13404`: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].
   Source `paper:chars/15219-15340`: Table 4: Class unlearning on Cifar100. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.
   - **Suggested revision:** Report the α sweep for at least one additional class and the ViT model, plus a small λ sweep. Alternatively, explicitly scope the robustness claim to the tested setting.

6. **The importance measure itself is borrowed from Aljundi et al. Its novelty lies only in being applied to unlearning, not in the measure.**
   The candidate contribution should not be credited as a new estimator.
   Evidence status: observation.
   Reasoning: The authors explicitly credit the source of the measure.
   Source `paper:chars/4392-6820`: We replace
the Fisher information with the sensitivity estimation from Aljundi et al. (2018)
   - **Suggested revision:** None.

7. **The empirical evaluation reuses the SSD/Chundawat protocol. This is appropriate for comparison but not a novelty in itself.**
   Using an established protocol aids comparability.
   Evidence status: observation.
   Reasoning: The evaluation protocol is inherited from prior work.
   Source `paper:chars/7514-23701`: We evaluate LFSSD in the same manner as Chundawat et al. (2023a); Foster et al.
(2023)
   - **Suggested revision:** None.

## Evidence to examine (advisory)

### Rendered formulas: Page 1 renders the set notation D, D_f, D_r with calligraphic D and subscripts, and the retained set as D_r = D \ D_f.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered inline formula matches the extracted text. The only differences are the dropped calligraphic font and subscripts, which are extraction noise.

- Source: `review-record:visual/0`
- Source: `paper:chars/1398-1497`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Rendered formulas: The abstract renders 'l_2 norm' with a subscript 2.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered text is consistent with the paper text. The flattened subscript is an extraction artifact.

- Source: `review-record:visual/1`
- Source: `paper:chars/927-981`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: captions (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/7`
- Source: `paper:chars/3674-3795`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/8`
- Source: `paper:chars/4788-4890`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/9`
- Source: `paper:chars/5750-5819`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: rendered formulas (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/10`
- Source: `paper:chars/5292-5356`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: units (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/11`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: sample counts (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/12`
- Source: `paper:chars/3796-3837`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: captions (paper:p.4)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/15`
- Source: `paper:chars/11866-11958`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Reviewer coverage limitation: rendered formulas (paper:p.4)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/17`
- Source: `paper:chars/12993-13088`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Reviewer coverage limitation: budgets (paper:p.4)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/18`
- Source: `paper:chars/13331-13404`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Reviewer coverage limitation: sample counts (paper:p.4)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/19`
- Source: `paper:chars/10633-10675`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Sample counts: Appendix Benchmarks paragraph reads 'Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables.'

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered repetition count matches the extracted text.

- Source: `review-record:visual/21`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Units: Text states 'D_r and D_f in the tables denote the accuracy on the respective subset of data in percent.'

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered unit (percent) for Dr/Df accuracy matches the paper text.

- Source: `review-record:visual/22`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Budgets: Text reads 'a model finetuned for 2 epochs on D_r'.

Scope: paper-only; analysis: visual; evidence status: inference.
Finetuning epoch budget rendered on the page matches the extracted text.

- Source: `review-record:visual/23`
- Source: `paper:chars/9926-9962`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Inline symbols render as calligraphic D with subscript r (𝒟_r) in the benchmark description and italic D_r, D_f later; no placeholder or broken glyphs visible.

Scope: paper-only; analysis: visual; evidence status: inference.
Inline math renders legibly and consistent with the text; the calligraphic vs italic D difference is typographic and does not alter meaning.

- Source: `review-record:visual/24`
- Source: `paper:chars/9883-9962`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Captions: Caption reads 'Sensitivity analysis for LFSSD parameter α with λ = 1 on CIFAR100 rocket class unlearning. LFSSD is deterministic, thus no ± reported.' Table rows α=1,5,10,25,50 show no ± values.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered caption matches the text, and the table indeed omits ±.

- Source: `review-record:visual/27`
- Source: `paper:chars/14433-14576`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Budgets: α values span 1 to 50 with λ fixed at 1.

Scope: paper-only; analysis: visual; evidence status: inference.
Tested α range and fixed λ match the described search.

- Source: `review-record:visual/28`
- Source: `paper:chars/13295-13404`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: Dr and Df accuracy columns use % signs; MIA has no unit.

Scope: paper-only; analysis: visual; evidence status: inference.
Percent units are consistent with the stated accuracy convention.

- Source: `review-record:visual/29`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Sample counts: Caption lists IDs 1,10,20,30,40 and says results are aggregated for 5 experiments.

Scope: paper-only; analysis: visual; evidence status: inference.
Five listed IDs correspond to the stated 5 experiments.

- Source: `review-record:visual/30`
- Source: `paper:chars/14760-14853`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Rendered formulas: Caption renders α_RN = 10, α_ViT = 10, λ = 1 for SSD; LFSSD: α = 10, λ = 1. Metric rows render as calligraphic D_r and D_f.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered subscripts are correct; the 'αV iT' text form is extraction noise.

- Source: `review-record:visual/31`
- Source: `paper:chars/15219-15340`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: captions (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/32`
- Source: `paper:chars/14649-14669`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: sample counts (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/33`
- Source: `paper:chars/10824-10904`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Sample counts: Table 7 caption reads 'Random sample unlearning on Cifar10 (100 samples).'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption's forget-set size matches the extracted text.

- Source: `review-record:visual/35`
- Source: `paper:chars/23044-23103`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: Caption: 'Subclass unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1. MR: mushroom, Rkt: Rocket.' The rows are RN/ViT × baby, lamp, MR, Rkt, sea.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption abbreviations match the row labels, and the hyperparameters match the text.

- Source: `review-record:visual/36`
- Source: `paper:chars/20462-20585`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: budgets (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/37`
- Source: `paper:chars/4178-4256`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: units (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/38`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: sample counts (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/39`
- Source: `paper:chars/10824-10991`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Rendered formulas: The symbols render correctly as calligraphic D_r and D_f, and as α_RN, α_ViT, α = 3.5, and λ = 1.

Scope: paper-only; analysis: visual; evidence status: inference.
The symbols are legible and not garbled. They match the extracted text.

- Source: `review-record:visual/40`
- Source: `paper:chars/23044-23147`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' The rows are labeled ED, NS, people, veg, and Veh2 for both RN and ViT.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption and abbreviations match the extracted text. Each abbreviation in the caption is used in the table rows.

- Source: `review-record:visual/42`
- Source: `paper:chars/17822-17991`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: rendered formulas (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/43`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: sample counts (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/44`
- Source: `paper:chars/10633-10734`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: units (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/45`
- Source: `paper:chars/10735-10823`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: budgets (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/46`
- Source: `paper:chars/13295-13404`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### claim-2: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/0`

### claim-3: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/1`

### claim-11: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/2`

### claim-8: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/3`

### claim-9: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/4`
- Source: `paper:chars/12946-12991`

### claim-4: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/5`

### claim-5: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/6`

### claim-7: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/7`

### claim-10: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/8`

### claim-6: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/9`

### Reviewer coverage limitation: budgets (artifact:figures/figure-1.png)

Scope: artifact-informed; analysis: visual; evidence status: unassessed.
Grounding failure: context, citation or readability. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:artifact-visual/0`
- Source: `paper:chars/12946-12991`
- Source: `artifact:figures/figure-1.png`
- Source: `review-output:visual-artifact/f4014155bd7c596b079acdcc9f55d7931f9b1f01fae0663c4c99175e6aa79298.png`

## Direct visual evidence (advisory)

- **agreement**, rendered page 1, rendered formulas: Page 1 renders the set notation D, D_f, D_r with calligraphic D and subscripts, and the retained set as D_r = D \ D_f.
  Paper quote: dataset D into a subset of data that needs to be forgotten Df , and the retained data Dr = D \ Df .. The rendered inline formula matches the extracted text. The only differences are the dropped calligraphic font and subscripts, which are extraction noise.
- **agreement**, rendered page 1, rendered formulas: The abstract renders 'l_2 norm' with a subscript 2.
  Paper quote: l2 norm of the model output to approximate sensitivity. The rendered text is consistent with the paper text. The flattened subscript is an extraction artifact.
- **agreement**, rendered page 3, sample counts: Appendix Benchmarks paragraph reads 'Runs are repeated 10 times for each method, with the mean and standard deviation shown in the tables.'
  Paper quote: Runs are repeated 10 times for each method, with the mean and standard
deviation shown in the tables.. Rendered repetition count matches the extracted text.
- **agreement**, rendered page 3, units: Text states 'D_r and D_f in the tables denote the accuracy on the respective subset of data in percent.'
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. Rendered unit (percent) for Dr/Df accuracy matches the paper text.
- **agreement**, rendered page 3, budgets: Text reads 'a model finetuned for 2 epochs on D_r'.
  Paper quote: a model finetuned for 2 epochs on Dr. Finetuning epoch budget rendered on the page matches the extracted text.
- **agreement**, rendered page 3, rendered formulas: Inline symbols render as calligraphic D with subscript r (𝒟_r) in the benchmark description and italic D_r, D_f later; no placeholder or broken glyphs visible.
  Paper quote: a model retrained from scratch
on only Dr, a model finetuned for 2 epochs on Dr. Inline math renders legibly and consistent with the text; the calligraphic vs italic D difference is typographic and does not alter meaning.
- **agreement**, rendered page 5, captions: Caption reads 'Sensitivity analysis for LFSSD parameter α with λ = 1 on CIFAR100 rocket class unlearning. LFSSD is deterministic, thus no ± reported.' Table rows α=1,5,10,25,50 show no ± values.
  Paper quote: Table 2: Sensitivity analysis for LFSSD parameter α with λ = 1 on CIFAR100 rocket class
unlearning. LFSSD is deterministic, thus no ± reported.. Rendered caption matches the text, and the table indeed omits ±.
- **agreement**, rendered page 5, budgets: α values span 1 to 50 with λ fixed at 1.
  Paper quote: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50].. Tested α range and fixed λ match the described search.
- **agreement**, rendered page 5, units: Dr and Df accuracy columns use % signs; MIA has no unit.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent.. Percent units are consistent with the stated accuracy convention.
- **agreement**, rendered page 5, sample counts: Caption lists IDs 1,10,20,30,40 and says results are aggregated for 5 experiments.
  Paper quote: One face unlearned per experiment [ID 1,10,20,30,40]
and results aggregated for 5 experiments. Five listed IDs correspond to the stated 5 experiments.
- **agreement**, rendered page 5, rendered formulas: Caption renders α_RN = 10, α_ViT = 10, λ = 1 for SSD; LFSSD: α = 10, λ = 1. Metric rows render as calligraphic D_r and D_f.
  Paper quote: Table 4: Class unlearning on Cifar100. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.. Rendered subscripts are correct; the 'αV iT' text form is extraction noise.
- **agreement**, rendered page 7, sample counts: Table 7 caption reads 'Random sample unlearning on Cifar10 (100 samples).'
  Paper quote: Table 7: Random sample unlearning on Cifar10 (100 samples).. The rendered caption's forget-set size matches the extracted text.
- **agreement**, rendered page 7, captions: Caption: 'Subclass unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 25, λ = 1; LFSSD: α = 10, λ = 1. MR: mushroom, Rkt: Rocket.' The rows are RN/ViT × baby, lamp, MR, Rkt, sea.
  Paper quote: Table 6: Subclass unlearning on Cifar20. SSD: αRN = 10, αV iT = 25, λ = 1; LFSSD: α = 10,
λ = 1. MR: mushroom, Rkt: Rocket.. The caption abbreviations match the row labels, and the hyperparameters match the text.
- **agreement**, rendered page 7, rendered formulas: The symbols render correctly as calligraphic D_r and D_f, and as α_RN, α_ViT, α = 3.5, and λ = 1.
  Paper quote: Table 7: Random sample unlearning on Cifar10 (100 samples). SSD: α = 10 , λ = 1 ; LFSSD:
α = 3.5, λ = 1. The symbols are legible and not garbled. They match the extracted text.
- **agreement**, rendered page 6, captions: Caption reads 'Table 5: Class unlearning on Cifar20. SSD: α_RN = 10, α_ViT = 10, λ = 1; LFSSD: α = 5, λ = 1. ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.' The rows are labeled ED, NS, people, veg, and Veh2 for both RN and ViT.
  Paper quote: Table 5: Class unlearning on Cifar20. SSD: αRN = 10, αV iT = 10, λ = 1; LFSSD: α = 5, λ = 1.
ED: electrical devices, NS: natural scenes, veg: vegetables, Veh2: vehicle2.. The rendered caption and abbreviations match the extracted text. Each abbreviation in the caption is used in the table rows.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 15 |
| Confirmed text-image mismatch (advisory) | 0 |
| Not applicable | 14 |
| Grounding failure: context, citation or readability | 0 |
| Missing or invalid confirmation | 7 |
| Conflicting assessments | 9 |
| Substantive uncertainty | 3 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.

### Human inspection needed

Conflicting assessments and substantive uncertainties are unconfirmed, not author-facing findings. Confirmed mismatches are advisory, not scientific proof.

- **Conflicting assessments**: `paper:p.2`, captions (visual audit observation index 7).
  Observation: The Table 1 caption states the hyperparameters 'α =10, λ =1 on Cifar100/20'. Its Cifar20 rows report LFSSD values of 81.54 / 7.29 / 3.40 (RN) and 95.68 / 24.05 / 5.80 (ViT).
  Paper quote: Table 1: Full- (class lamp) and subclass (lamp is part of electrical devices) unlearning with α =10,
λ =1 on Cifar100/20..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The Cifar20 rows match the Table 6 lamp subclass values exactly. Table 6 lists 'SSD: αRN = 10, αV iT = 25, λ = 1'. The Table 1 Cifar20 ViT SSD values (95.54, 14.58, 3.2) were therefore produced with α=25, not the α=10 stated in the caption.
  First assessment: mismatch. The Cifar20 rows match the Table 6 lamp subclass values exactly. Table 6 lists 'SSD: αRN = 10, αV iT = 25, λ = 1'. The Table 1 Cifar20 ViT SSD values (95.54, 14.58, 3.2) were therefore produced with α=25, not the α=10 stated in the caption.
  Second assessment: agreement. The rendered caption text matches the quote.

- **Substantive uncertainty**: `paper:p.2`, rendered_formulas (visual audit observation index 8).
  Observation: Equation 1 is rendered with an empty bracket '[]' as the importance symbol, for example '[]_{D_f,i} > α[]_{D,i}'. The following text also says '[]_{D_f,i} and []_{D_i}' and 'in place of [] and []_f'.
  Paper quote: Here, α and λ are hyper-parameters, and []Df,i and []Di are the ith element of the diagonal of
the FIM.
  Reason: Rendered formula requires human confirmation; an extraction difference alone is not an authoring defect.

- **Substantive uncertainty**: `paper:p.4`, sample_counts (visual audit observation index 19).
  Observation: Page 4 continues the sentence ending 'across repeated runs' about deterministic SSD/LFSSD having no standard deviation. No explicit run counts appear on this page.
  Paper quote: Runs are repeated 10 times for each method.
  Reason: The run count is stated on page 3. Table 7 later reports nonzero ± values for SSD and LFSSD in random forgetting. That cannot be reconciled from page 4 with the claim that deterministic methods have no standard deviation, possibly because forget samples vary across runs.

- **Conflicting assessments**: `paper:p.5`, captions (visual audit observation index 32).
  Observation: Table 4 RN Rkt LFSSD row reads Dr 75.67±0.00, Df 0.00±0.00, MIA 0.00±0.00; Table 2 α=10 row reads 75.67%, 0.00%, 0.00.
  Paper quote: 10 75.67% 0.00% 0.00.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The α=10 sensitivity row matches the rocket result in Table 4, which uses LFSSD α=10.
  First assessment: agreement. The α=10 sensitivity row matches the rocket result in Table 4, which uses LFSSD α=10.
  Second assessment: unresolved. A caption check cannot be grounded because the quote is table content rather than a caption. The values themselves do match the visible row.

- **Substantive uncertainty**: `paper:p.5`, sample_counts (visual audit observation index 33).
  Observation: SSD and LFSSD columns show ±0.00 for all entries; SSD RN baby Dr shows '44.05*±0.00' with an asterisk not explained on this page.
  Paper quote: Since SSD (and therefore LFSSD) is deterministic, there is no standard deviation.
  Reason: ±0.00 is consistent with determinism, but the meaning of the asterisk on 44.05 is not defined in the supplied text, so its interpretation cannot be confirmed.

- **Conflicting assessments**: `paper:p.7`, budgets (visual audit observation index 37).
  Observation: The RN lamp row shows LFSSD Dr 81.54, Df 7.29, MIA 3.40 and SSD Dr 79.58, Df 0.00, MIA 2.00. The ViT lamp row shows LFSSD Df 24.05 and SSD Df 14.58.
  Paper quote: Cifar20 Dr 82.61±0.00 81.81±0.19 81.54 79.58 95.77±0.00 94.69±0.13 95.68 95.54.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): These rendered values agree with Table 1's subclass lamp entries. One exception: Table 1 lists ViT SSD Dr as 95.54, which equals Table 6's ViT lamp SSD Dr of 95.54. Overall the values are consistent.
  First assessment: agreement. These rendered values agree with Table 1's subclass lamp entries. One exception: Table 1 lists ViT SSD Dr as 95.54, which equals Table 6's ViT lamp SSD Dr of 95.54. Overall the values are consistent.
  Second assessment: unresolved. The quoted row belongs to Table 1, which appears on another page, so this page cannot confirm it directly. The Table 6 lamp values on this page are numerically consistent with the quote, but they are not the same table row.

- **Conflicting assessments**: `paper:p.7`, units (visual audit observation index 38).
  Observation: The Dr and Df entries are shown as numbers with ± and no unit symbol. The values fall in the 0–100 range.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The appendix defines these values as percentages, and the values shown fit that scale.
  First assessment: agreement. The appendix defines these values as percentages, and the values shown fit that scale.
  Second assessment: unresolved. The statement is appendix text from a different page. This page has no element that states the units.

- **Conflicting assessments**: `paper:p.7`, sample_counts (visual audit observation index 39).
  Observation: In the SSD and LFSSD columns of Table 6, every entry shows ±0.00. In Table 7, the SSD and LFSSD columns show nonzero standard deviations, such as 88.68±3.36.
  Paper quote: Since SSD (and therefore LFSSD) is deterministic, there is no standard deviation

3Accepted as a Tiny Paper at ICLR 2024 (Preprint)

Approximate parameter importances.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Table 6 is consistent with determinism. The nonzero SSD and LFSSD standard deviations in Table 7 can plausibly come from random selection of the forget set across runs. That reason is not stated in the text.
  First assessment: agreement. Table 6 is consistent with determinism. The nonzero SSD and LFSSD standard deviations in Table 7 can plausibly come from random selection of the forget set across runs. That reason is not stated in the text.
  Second assessment: unresolved. The quote spans pages 3 and 4. No relevant element appears on this page.

- **Conflicting assessments**: `paper:p.6`, rendered_formulas (visual audit observation index 43).
  Observation: The caption's α_RN and α_ViT are rendered as proper subscripts. The table rows show 𝒟_r and 𝒟_f with calligraphic D and subscripts.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The formulas are rendered correctly. The extracted forms 'αV iT' and 'Dr' are extraction artifacts, not rendering defects.
  First assessment: agreement. The formulas are rendered correctly. The extracted forms 'αV iT' and 'Dr' are extraction artifacts, not rendering defects.
  Second assessment: unresolved. The quoted sentence's rendering is not on this page; only the D_r/D_f symbols in the table are visible, so the quote's rendering cannot be checked here.

- **Conflicting assessments**: `paper:p.6`, sample_counts (visual audit observation index 44).
  Observation: Baseline, SSD and LFSSD values show ±0.00. Retrain, finetune, teacher and amnesiac show nonzero standard deviations, such as 82.13±0.23 and 10.88±1.3.
  Paper quote: Runs are repeated 10 times for each method, with the mean and standard
deviation shown in the tables..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The ±0.00 values for SSD and LFSSD agree with their stated determinism. The page does not state the number of runs, so it cannot be checked visually beyond showing mean±std.
  First assessment: agreement. The ±0.00 values for SSD and LFSSD agree with their stated determinism. The page does not state the number of runs, so it cannot be checked visually beyond showing mean±std.
  Second assessment: unresolved. The mean±std format is consistent with the statement, but the number of runs (10) is not visible on this page, so the count cannot be verified.

- **Conflicting assessments**: `paper:p.6`, units (visual audit observation index 45).
  Observation: The table shows no unit symbols. 𝒟_r and 𝒟_f values range from 0 to 100, and MIA values are also on a 0–100 scale.
  Paper quote: Dr and Df in the tables denote the accuracy on the respective subset
of data in percent..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The value ranges are consistent with percentages as stated in the appendix.
  First assessment: agreement. The value ranges are consistent with percentages as stated in the appendix.
  Second assessment: unresolved. Values are consistent with percentages (0–100 range), but the table itself shows no explicit unit, so the unit claim is not directly confirmed by the image.

- **Conflicting assessments**: `paper:p.6`, budgets (visual audit observation index 46).
  Observation: The caption gives LFSSD α = 5 and λ = 1.
  Paper quote: For LFSSD we performed a simplified
hyperparameter search keeping lambda fixed at 1 and alpha values [1, 50]..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): An LFSSD setting of λ = 1 with α = 5 falls within the stated search range.
  First assessment: agreement. An LFSSD setting of λ = 1 with α = 5 falls within the stated search range.
  Second assessment: unresolved. The search-budget statement is on another page; this page only shows the chosen values (α=5 within [1,50], λ=1), which does not verify the search itself.



## Artifact evidence reconciliation (supplementary)

Literal checks of explicitly linked shipped evidence, not scientific validation. The independent paper assessment is unchanged.

- **unresolved**: claim-2 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-3 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-11 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-8 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-9 / . No declared result edge resolves.
  Paper: `paper:chars/12946-12991`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-4 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-5 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-7 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-10 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-6 / . No declared result edge resolves.
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
- artifact visual inspection: incomplete
- artifact checks: completed
- reference lookup: not-requested
- contribution review: completed

No submission code was executed.

**Coverage notes**

- Visual inspection incomplete: Image analysis is advisory; unmatched or omitted evidence is unassessed.
- Additional analysis diagnostics are retained in run.json (raw model responses omitted from this copy); incomplete coverage is not evidence of paper quality.
