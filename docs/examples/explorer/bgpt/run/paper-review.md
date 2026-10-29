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

The paper presents bGPT, a hierarchical Transformer trained with next-byte prediction, and applies it both to conventional media (text, images, audio) and to native binary tasks framed as digital-world simulation: ABC-to-MIDI data conversion (algorithm simulation) and CPU state modelling (hardware simulation). It reports classification and bits-per-byte results against modality-specific baselines, cross-modal pre-training comparisons, and near-perfect results on the conversion and CPU tasks. The authors describe the architecture as adapted from prior hierarchical work and position the contribution around native binary data.

## Contributions

1. **bGPT: next byte prediction model for digital world simulation.** Introduces bGPT, a model that applies next byte prediction directly to native binary data to process digital media and simulate algorithms and hardware within a single unified byte-sequence framework.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unresolved*
2. **Hierarchical patch-based Transformer architecture with generative and classification objectives.** bGPT segments byte sequences into fixed-size patches, using a linear projection, a patch-level decoder and a byte-level decoder, trained with next byte prediction and then adapted to classification.
   *Claim support: unresolved · Significance: unassessed · Originality: contested*
3. **CPU States dataset for hardware behaviour modelling.** Introduces a 2.1-million-instance synthetic dataset pairing memory blocks of machine instructions with sequences of 16-byte CPU register states, for modelling simplified CPU behaviour.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unresolved*
4. **Algorithm and hardware simulation via byte modelling.** Frames ABC-to-MIDI data conversion and CPU state modelling as byte-level generative tasks, showing byte models can simulate algorithms and hardware with scaling behaviour.
   *Claim support (inferred links): contested · Significance: supported · Originality: unresolved*
5. **Modality-agnostic digital media processing and cross-modal transfer.** Shows bGPT handles text, audio and image files as raw bytes without modality-specific design and analyses cross-modal knowledge transfer between pre-training and fine-tuning modalities.
   *Claim support: unresolved · Significance: unassessed · Originality: contested*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: bGPT: next byte prediction model for digital world simulation

**Claim support (inferred links): contested**
- Linked claims:
  - C1 (inferred by the reviewer, not declared by the authors): It has almost flawlessly replicated the process of converting symbolic music data, achieving a low error rate of 0.0011 bits per byte in converting ABC notat…
  - C2 (inferred by the reviewer, not declared by the authors): In addition, bGPT demonstrates exceptional capabilities in simulating CPU behaviour, with an accuracy exceeding 99.99% in executing various operations.
- The headline simulation claims (C1, C2) are reported numerically, but the absence of baselines and the very simple CPU make the 'emergent' and 'digital world simulator' framing stronger than the evidence.
- Sources: paper:chars/30472-31335, paper:chars/34448-36748, paper:chars/36748-38535

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The authors acknowledge byte-level multimodal models, citing ByteFormer and MegaByte, and say their architecture adapts prior hierarchical designs. bGPT's novelty therefore lies in its application scope (native binary data and simulation), not in the model.
- Overall bGPT novelty claim: byte modelling of media is prior work per the authors; claimed gap is native binary data and digital-world simulation.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7775-10479, paper:chars/10851-15278

Paper’s wording: “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”

### Contribution 2: Hierarchical patch-based Transformer architecture with generative and classification objectives

**Claim support: unresolved**
- No claims are linked to this contribution.
- The paper describes the architecture and both training objectives, but does not ablate patch size or the hierarchical design against a flat byte model.
- Sources: paper:chars/21690-22666

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- The authors frame bGPT as an introduction of next-byte prediction for digital-world simulation, yet their own background credits ByteFormer, MegaByte and MambaByte with byte-level modelling across modalities and states that the architecture is inspired by prior hierarchical work. On the paper's own account, the novelty lies in task framing and evaluation scope, not in the model.
- The architecture is explicitly derivative of prior hierarchical/patch work, so novelty rests on the application framing, not on the architecture.
- The architecture is author-acknowledged as an adaptation of prior hierarchical byte models; originality rests on application scope, not the model.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7775-10479, paper:chars/10851-15278, paper:chars/172-1238

Paper’s wording: “We start by present- ing its hierarchical Transformer framework, which segments byte sequences into patches to manage computational effi- ciency. Subsequently, we present the training objectives of bGPT, including generative modelling and classification.”

### Contribution 3: CPU States dataset for hardware behaviour modelling

**Claim support (inferred links): contested**
- Linked claims:
  - C2 (inferred by the reviewer, not declared by the authors): In addition, bGPT demonstrates exceptional capabilities in simulating CPU behaviour, with an accuracy exceeding 99.99% in executing various operations.
- CPU 99.99% accuracy is byte-wise over states on a simplified, jump-free synthetic ISA with no simple baseline; 'beyond memorization' and 'real comprehension' are not established.
- Sources: paper:chars/34448-36748, paper:chars/40096-79998

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The CPU States dataset is a new, explicitly simplified synthetic benchmark. It could become a reusable resource for learned-emulation research, though its utility is limited by deliberate design choices.
- The CPU States dataset is a new synthetic benchmark. It is clearly specified but deliberately simplified, and the authors acknowledge that it excludes jumps and real CPUs.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/18456-21674, paper:chars/36748-38535

Paper’s wording: “For CPU state modelling, we introduce the CPU States dataset (with 2.1 million instances), offering a simplified representation of CPU behaviour for ease of data collec- tion and evaluation.”

### Contribution 4: Algorithm and hardware simulation via byte modelling

**Claim support (inferred links): contested**
- Linked claims:
  - C1 (inferred by the reviewer, not declared by the authors): It has almost flawlessly replicated the process of converting symbolic music data, achieving a low error rate of 0.0011 bits per byte in converting ABC notat…
  - C2 (inferred by the reviewer, not declared by the authors): In addition, bGPT demonstrates exceptional capabilities in simulating CPU behaviour, with an accuracy exceeding 99.99% in executing various operations.
- The simulation results are measured, but there is no baseline, and the reported decision protocol limits what the numbers show. The 99.99% figure is byte-wise accuracy under teacher-forced, conditioned prediction, not rollout correctness.
- ABC→MIDI 0.0011 BPB is a teacher-forced likelihood; 'almost flawlessly replicated' conversion needs generation-level correctness.
- The 'emergent abilities' claim rests on a loss jump in a single run. The evidence offered, the 'linear and smooth nature of BPB', is in tension with the reported discontinuity.
- 'Emergent abilities' and 'strong scalability' rest on three data scales of one 110M model and a loss-curve jump, which the paper itself defends only via BPB smoothness.
- The 'emergent abilities' summary (C1, C2) rests on a loss jump around epoch 11 at a single data scale, which does not establish emergence with scale.
- Sources: paper:chars/30472-31335, paper:chars/34448-36748, paper:chars/31335-34448

**Significance: supported**
- Framing byte-level next-token prediction as simulation of algorithms and hardware (ABC→MIDI conversion, CPU state modelling) is an interesting, underexplored task direction.
- The most distinctive contribution is framing algorithm and hardware simulation as byte-level generative modelling. The reported results are strong: BPBmidi of 0.0011 for ABC→MIDI and 99.99% CPU-state accuracy.
- Sources: paper:chars/1238-5446, paper:chars/18456-21674, paper:chars/31335-34448, paper:chars/34448-36748

**Originality: unresolved**
- Framing algorithm and hardware simulation (ABC→MIDI conversion, CPU state prediction) as byte-level generative tasks is the paper's most distinctive contribution relative to the byte models it cites. Those works are described as targeting language, media or malware.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7775-10479, paper:chars/18456-21674

Paper’s wording: “In summary, bGPT demonstrates strong scalability on native binary data with emergent abilities in data conversion and CPU state modelling”

### Contribution 5: Modality-agnostic digital media processing and cross-modal transfer

**Claim support: unresolved**
- No claims are linked to this contribution.
- The abstract says bGPT 'matches specialized models', but Table 3 shows a gap of roughly 10 points to ViT on CIFAR-10. The baseline numbers are also taken from studies with different pre-training.
- The abstract says bGPT 'matches specialized models', but Table 3 shows notable gaps, especially on CIFAR-10. The authors themselves describe these gaps.
- Sources: paper:chars/172-1238, paper:chars/25015-30472, paper:chars/23408-25015

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- The modality-agnostic transfer claim is novel mainly as analysis. The authors themselves report that bGPT trails specialized baselines, and that text transfer is negative.
- The cross-modal transfer analysis is a modest but informative contribution. However, the 'modality-agnostic' claim is weakened by the negative transfer the authors report from text.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/25015-30472, paper:chars/172-1238

Paper’s wording: “Our experiments demonstrate the effectiveness of bGPT in modelling digital media data, which showcases modality-agnostic knowledge transfer.”

<details><summary>What the authors say is original (3 statements)</summary>

Authors' stated position:
- [claims, builds on] “Inspired by the success of next token prediction in natural lan- guage processing, we introduce bGPT, a model with next byte prediction to simulate the digi- tal world. bGPT matches specialized models in performance across various modalities, including text, audio, and images, and offers new possibil- ities for predicting, simulating, and diagnosing algorithm or hardware behaviour.”
- [claims; positioned against Raff et al., 2018, Guo et al., 2019] “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”
- [claims, builds on] “Conclusions In this paper, we present bGPT as a versatile simulator for the digital world, extending deep learning to binary data processing via next byte prediction.”

</details>


## Reasons to accept

1. **Framing byte-level next-token prediction as simulation of algorithms and hardware (ABC→MIDI conversion, CPU state modelling) is an interesting, underexplored task direction.**
   Value lies in the task framing and testbeds rather than architecture.
   Evidence status: inference.
   Reasoning: The paper positions these as underexplored binary-native tasks; framing them as generative byte modelling gives a concrete testbed beyond media data, which is the main source of likely impact.
   Source `paper:chars/1238-5446`: underexplored tasks intrinsic to binary-native operations,
including data conversion and CPU state modelling, which
represent algorithm and hardware simulation, respectively.
   Source `paper:chars/18456-21674`: This necessitates the ability to simulate and
reverse-engineer the conversion algorithm1

2. **Framing algorithm and hardware simulation (ABC→MIDI conversion, CPU state prediction) as byte-level generative tasks is the paper's most distinctive contribution relative to the byte models it cites. Those works are described as targeting language, media or malware.**
   This framing could seed a research line on learned emulators and format converters. Researchers in program analysis, reverse engineering and learned simulators are likely to build on it.
   Evidence status: inference.
   Reasoning: The related-work section attributes language, media or security tasks to prior byte models. It then presents conversion and CPU simulation as new evaluation targets. This makes the task framing the clearest original element on the authors' own account. Novelty is judged relative to author-reported prior work only.
   Source `paper:chars/7775-10479`: current research often neglects native bi-
nary data, focusing on narrow tasks and overlooking the
broader potential of byte models in digital world simulation.
   Source `paper:chars/18456-21674`: This necessitates the ability to simulate and
reverse-engineer the conversion algorithm

3. **The most distinctive contribution is framing algorithm and hardware simulation as byte-level generative modelling. The reported results are strong: BPBmidi of 0.0011 for ABC→MIDI and 99.99% CPU-state accuracy.**
   These results could plausibly influence work on learned emulators and reverse engineering.
   Evidence status: inference.
   Reasoning: Near-zero error on deterministic transforms indicates that the model learned the underlying procedures. This opens a less-studied application area for byte models, though only on narrow tasks.
   Source `paper:chars/31335-34448`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   Source `paper:chars/34448-36748`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%)

4. **The authors acknowledge byte-level multimodal models, citing ByteFormer and MegaByte, and say their architecture adapts prior hierarchical designs. bGPT's novelty therefore lies in its application scope (native binary data and simulation), not in the model.**
   Phrasing such as 'paradigm shift' and 'transcends traditional deep learning boundaries' exceeds what the background section concedes.
   Evidence status: inference.
   Reasoning: The authors place their difference in task scope. That differentiation is stated clearly, but it is author-reported and was not independently verified against the cited works.
   Source `paper:chars/7775-10479`: Despite progress, current research often neglects native bi-
nary data, focusing on narrow tasks and overlooking the
broader potential of byte models in digital world simulation.
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture

## Originality

On the authors' own account, the originality lies in task framing and evaluation scope, not in the model or objective. The background credits ByteFormer with processing raw image and audio bytes and MegaByte with modelling long byte sequences across modalities. It also states that bGPT adapts a hierarchical architecture from cited work. Framing ABC-to-MIDI conversion and CPU state prediction as byte-level generative simulation tasks is the most distinctive element relative to these works, which the paper describes as targeting language, media or narrower tasks. This differentiation is author-reported and has not been verified against the cited papers. The paper does not say concretely how bGPT's architecture differs from MegaByte, and phrasing such as 'we introduce bGPT', 'paradigm shift' and 'transcends traditional deep learning boundaries' goes beyond what the background concedes. The cross-modal transfer analysis is a useful empirical contribution, but it is novel mainly as analysis.

## Likely impact

The simulation testbeds could seed work on learned emulators, format converters and reverse engineering. Researchers in program analysis and learned simulators may build on the task framing. Several factors limit likely influence. The CPU is a simplified synthetic ISA that deliberately excludes jump instructions. Neither simulation task has a baseline. On the media benchmarks, bGPT trails the specialised models, by about 9.4 points on CIFAR-10 and about 2 points on text and audio. Mixed-modality pre-training slightly underperformed text-only pre-training on AG News, and transfer between text and other modalities was negative. Impact is therefore most plausible as a task and benchmark direction rather than as evidence that one byte model can replace specialised ones.

## Decision-critical concerns

1. **The abstract says bGPT 'matches specialized models', but Table 3 shows a gap of roughly 10 points to ViT on CIFAR-10. The baseline numbers are also taken from studies with different pre-training.**
   GPT2-small was retrained under matched settings, but ViT and AST were not.
   Evidence status: inference.
   Reasoning: A gap of 9.4 points on CIFAR-10 contradicts 'matches'. Because the ViT and AST numbers are copied from other studies, the comparison mixes training regimes and model resolutions.
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities
   Source `paper:chars/25015-30472`: with an accuracy of
88.69% against 98.13%
   Source `paper:chars/23408-25015`: their
results were taken from the original studies
   - **Why this affects the decision:** The headline claim of the paper is overstated.
   - **Actionable revision:** Either retrain ViT and AST under matched settings on 32x32 and 8kHz inputs, or rescope the abstract and conclusions to say 'competitive on text/audio, lagging on images'.
   - **What would resolve it:** A matched-setting baseline table, or revised claim wording.

2. **CPU 99.99% accuracy is byte-wise over states on a simplified, jump-free synthetic ISA with no simple baseline; 'beyond memorization' and 'real comprehension' are not established.**
   Abstract 'executing various operations' depends on this metric.
   Evidence status: inference.
   Reasoning: Byte-wise accuracy over 16-byte states, many unchanged between steps (e.g., PC increments, untouched registers), can be high even with errors; without a copy-previous-state baseline or per-sequence exact-match, 99.99% does not show execution fidelity.
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   Source `paper:chars/34448-36748`: suggesting an efficiency beyond sim-
ple memorization
   Source `paper:chars/40096-79998`: complex instructions like jump commands were deliberately excluded
   - **Why this affects the decision:** Headline claim C2 and the hardware-simulation contribution rest on it.
   - **Actionable revision:** Report a copy-previous-state baseline, accuracy on changed bytes only, full-state and full-program exact match, and per-instruction-type accuracy.
   - **What would resolve it:** Large margin over trivial baseline on changed bytes and high program-level exact match.

3. **The authors frame bGPT as an introduction of next-byte prediction for digital-world simulation, yet their own background credits ByteFormer, MegaByte and MambaByte with byte-level modelling across modalities and states that the architecture is inspired by prior hierarchical work. On the paper's own account, the novelty lies in task framing and evaluation scope, not in the model.**
   The paper should state explicitly how bGPT's architecture differs from MegaByte, as the authors themselves describe MegaByte. It should also position the contribution as framing, tasks and evaluation rather than as a new model. These author-reported descriptions of prior work were not independently verified.
   Evidence status: inference.
   Reasoning: The paper reports that MegaByte already performs multimodal byte-sequence modelling and that ByteFormer already processes raw image and audio bytes. It also says bGPT adapts a hierarchical architecture from cited work. Together, these statements indicate that the model and objective are not new according to the authors themselves. The abstract and introduction do not state this disclaimer. The claimed differentiation is limited to the 'native binary data' framing and the simulation tasks.
   Source `paper:chars/7775-10479`: MegaByte (Yu et al., 2023), on the other hand,
has been tested and proven to excel in modelling long byte
sequences across various modalities.
   Source `paper:chars/7775-10479`: ByteFormer (Horton
et al., 2023) directly handles raw byte sequences converted
from images and audio
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture
   Source `paper:chars/172-1238`: we introduce bGPT, a model
with next byte prediction to simulate the digi-
tal world.
   - **Why this affects the decision:** Originality credit depends on whether any architectural novelty is claimed. Without a stated delta, the contribution reduces to an empirical study.
   - **Actionable revision:** Add an explicit comparison (text or table) of bGPT against MegaByte, ByteFormer and MambaByte covering architecture, objective and tasks. Revise the abstract and introduction to state what is new.
   - **What would resolve it:** A stated architectural or training difference from MegaByte, or an explicit scope statement that the novelty lies in the task suite and analysis.

4. **The headline simulation claims (C1, C2) are reported numerically, but the absence of baselines and the very simple CPU make the 'emergent' and 'digital world simulator' framing stronger than the evidence.**
   The paper should report a trivial baseline that copies the previous state, which tests whether most bytes are unchanged between steps. It should also report per-state exact-match accuracy alongside byte-wise accuracy.
   Evidence status: inference.
   Reasoning: The accuracy figures are reported, but there is no comparison point. Without one, readers cannot tell whether 99.99% reflects difficulty or task simplicity. A plain byte Transformer or a copy-previous-state baseline would answer this. The conclusion acknowledges that the CPU is simplified. Byte-wise accuracy over largely unchanged register states may also be inflated.
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets,
we investigated its performance across different data scales
   Source `paper:chars/34448-36748`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%)
   Source `paper:chars/36748-38535`: our
CPU state modelling experiments focused solely on simpli-
fied CPUs, omitting the use of real modern CPUs
   Source `paper:chars/34448-36748`: indicating
an emergent ability in CPU state modelling
   - **Why this affects the decision:** Without these measures, the significance of the near-perfect simulation result is uncertain.
   - **Actionable revision:** Report a copy-previous-state baseline, per-state or per-program exact-match accuracy, and a standard non-hierarchical byte Transformer baseline.
   - **What would resolve it:** Exact-match accuracy that remains high and is well above the copy baseline.

## Questions for the authors

1. **The 'emergent abilities' summary (C1, C2) rests on a loss jump around epoch 11 at a single data scale, which does not establish emergence with scale.**
   The authors should clarify whether the jump is reproducible across random seeds. If it is not, 'emergent' should be removed from the abstract and conclusion.
   Evidence status: inference.
   Reasoning: The evidence is a training-dynamics jump within one run. The paper does not show a scale-dependent capability threshold, which is what the emergence framing implies.
   Source `paper:chars/34448-36748`: A significant improvement in the performance of bGPT5
occurred around epoch 11
   - **Why the answer matters:** If the jump does not replicate across seeds, the emergence claim should be dropped from the contribution.
   - **Requested response:** Report multiple seeds and the epoch at which the jump occurs for each data scale.
   - **Answer that would resolve it:** A consistent jump across seeds, and its absence at smaller scales.

2. **How is the MIDI to ABC result scored given that the conversion is lossy? Is the 0.0011 BPB on ABC to MIDI driven by deterministic header bytes, and how robust is it on held-out tunes?**
   Claim C1 depends on this.
   Evidence status: inference.
   Reasoning: BPB averages over all bytes, so a near-zero value may hide errors in note events. Exact-match or validity rates for the generated MIDI would show whether the conversion is actually 'near flawless'.
   Source `paper:chars/31335-34448`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   - **Why the answer matters:** If the exact-match rate for generated MIDI files is high, claim C1 holds.
   - **Requested response:** Report the rate of exactly correct MIDI files under greedy decoding.
   - **Answer that would resolve it:** File-level exact-match percentage on the evaluation split.

3. **Are CPU test programs disjoint from training, and is variance across seeds known for small accuracy differences (e.g., 85.26 vs 84.66 in Table 4)?**
   If differences fall within seed variance, cross-modal transfer claims weaken.
   Evidence status: inference.
   Reasoning: The 'content alignment over format' conclusion relies on a 0.6-point single-run difference.
   Source `paper:chars/25015-30472`: bGPTimage 0.3899 84.66
bGPTlibri 0.3900 85.26
   Source `paper:chars/21690-22666`: we avoided hyper-
parameter tuning and data augmentation in all evaluations.
   - **Why the answer matters:** Could change support for transfer claim.
   - **Requested response:** Report multi-seed means/std.
   - **Answer that would resolve it:** Std smaller than gaps.

## Decision synthesis

In favour: the paper opens an underexplored direction by treating algorithm and hardware simulation as byte-level generative modelling, and it reports striking numbers on these tasks (0.0011 BPB for ABC-to-MIDI; 99.97% and 99.99% CPU-state accuracy). Read cautiously, near-zero error on deterministic transforms suggests the model may have learned the underlying procedures. The media and transfer experiments are reported candidly, including negative results.

The most important concerns are about whether the evidence supports the headline claims.

1. **CPU accuracy.** The 99.99% figure is byte-wise over 16-byte states, many of which may be unchanged between steps. There is no copy-previous-state baseline and no per-state exact-match accuracy, so the number may not show execution fidelity. Claims of going 'beyond memorization' are not established.
2. **ABC-to-MIDI scoring.** BPB averages over all bytes and could be dominated by deterministic header bytes. Exact-match or validity rates on held-out tunes would show whether the conversion is truly near-flawless.
3. **Emergence.** The 'emergent ability' claim rests on a loss jump around epoch 11 within a single run at one data scale. That is not a scale-dependent threshold.
4. **'Matches specialized models'.** The abstract's claim conflicts with Table 3, which shows bGPT trailing on all three benchmarks. The ViT and AST numbers are also taken from original studies with different training regimes; only GPT2-small was retrained under matched settings.
5. **Novelty positioning.** The abstract and introduction do not acknowledge that, by the authors' own description, the model and objective have precedents.

Score-changing questions for the authors:
- Are the CPU test programs disjoint from the training programs?
- How is the lossy MIDI-to-ABC direction scored?
- Is the epoch-11 jump reproducible across random seeds?
- Do small differences such as 85.26 vs 84.66 in Table 4 exceed seed variance? The 'content alignment over format' conclusion relies on this single-run gap.

Non-blocking improvements:
- Temper the abstract wording.
- State the architectural differences from MegaByte and ByteFormer.
- Analyse whether the bGPT_mix shortfall on AG News reflects a smaller share of text data or interference between modalities.

The weight a reviewer gives these points depends mainly on whether baselines and exact-match metrics for the simulation tasks can be supplied.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The abstract states its headline results concretely and gives a reader the core idea in plain terms.

**Writing-quality issues**

1. **The abstract's CPU accuracy and conversion figures are not given the scope a reader needs: the CPU is a simplified synthetic one and 0.0011 BPB is a per-byte loss, not an 'error rate'.**
   The body is candid about simplification; the abstract should match it.
   - **Suggested revision:** In the abstract, describe 0.0011 as bits-per-byte loss (not error rate), state that CPU accuracy is per-byte on a simplified synthetic CPU, and if available add a whole-sequence exact-match rate.

2. **Rigor is sometimes asserted with adjectives rather than shown, notably 'emergent ability' and 'real comprehension' claims.**
   Similar intensifiers ('exceptional', 'impressively low', 'potent') appear in reported results.
   - **Suggested revision:** Replace 'real comprehension' with a description of what was measured, or add a breakdown (e.g., accuracy by instruction type or program length) that demonstrates it.

3. **Numbers are reported to four decimal places, and the main media takeaway (byte models trail specialists, especially on images) is softened as 'on par'.**
   The image-gap disclosure is valuable and should be kept, stated plainly in the summary.
   - **Suggested revision:** Round table values to meaningful precision and state a one-sentence practitioner takeaway: competitive on text/audio, notably behind on images.

4. **Table 1 'Total Bytes (GB)' values appear to be binary gibibytes rather than decimal gigabytes.**
   The values are internally consistent, but the unit label understates the decimal byte count by about 7%. This does not affect the paper's conclusions.
   - **Suggested revision:** Relabel the column as GiB or convert the values to decimal GB.

## Additional improvements (non-blocking)

1. **Table 3 values, which match the text, show bGPT trailing the modality-specific baselines on all three benchmarks. The gap is largest on CIFAR-10.**
   The roughly 9.4-point CIFAR-10 gap is much larger than the gaps on text (about 2 points) and audio (about 2 points).
   Evidence status: inference.
   Reasoning: The confirmed record shows the paper's own reported figures: AG News 92.49% vs 94.50% and BPB 1.0639 vs 0.9237, CIFAR-10 88.69% vs 98.13%, and Speech Commands 96.03% vs 98.11%. Because the rendered table agrees with the body text, these numbers are the paper's stated results. They limit how strongly any claim of competitiveness with specialised models can be made, especially for images.
   Source `review-record:visual/49`: Metrics labeled BPB and Acc (%); values such as 1.0639/92.49, 3.1234/88.69, 1.4818/96.03, baselines 0.9237/94.50, 98.13, 98.11.
   Source `paper:chars/25826-25993`: bGPTwiki
achieved a score of 1.0639 BPB and an accuracy of 92.49%
on AG News, which, while not quite at the level of GPT2-
small, scored 0.9237 BPB and 94.50% accuracy
   - **Suggested revision:** Phrase cross-modal performance claims in the abstract and conclusion in proportion to the per-modality gaps in Table 3. Consider discussing why the gap is larger for images.

2. **The architecture is explicitly derivative of prior hierarchical/patch work, so novelty rests on the application framing, not on the architecture.**
   The paper does not state concretely how bGPT differs from MegaByte or ByteFormer beyond the choice of tasks.
   Evidence status: inference.
   Reasoning: The authors say they adapt the architecture from prior work. They also report that MegaByte already models bytes across modalities. Architectural originality is therefore limited by their own account, and the remaining difference is the focus on native binary data and simulation. We have not verified MegaByte's content directly.
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture
   Source `paper:chars/7775-10479`: MegaByte (Yu et al., 2023), on the other hand,
has been tested and proven to excel in modelling long byte
sequences across various modalities.
   - **Suggested revision:** Add an explicit architectural and task-level comparison against MegaByte and ByteFormer.

3. **The modality-agnostic transfer claim is novel mainly as analysis. The authors themselves report that bGPT trails specialized baselines, and that text transfer is negative.**
   The abstract wording should be tempered to reflect the reported gaps.
   Evidence status: inference.
   Reasoning: The abstract's 'matches' wording conflicts with the reported ten-point gap on CIFAR-10 and with the negative transfer from text. The cross-modal analysis is still a useful empirical contribution.
   Source `paper:chars/25015-30472`: bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%
   Source `paper:chars/25015-30472`: negative trans-
fer is observed when transitioning between text and other
modalities
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities
   - **Suggested revision:** Revise the abstract to say 'approaches' and note the image gap.

4. **The architecture is author-acknowledged as an adaptation of prior hierarchical byte models; originality rests on application scope, not the model.**
   Contribution framing 'we introduce bGPT' should clarify architectural deltas vs MegaByte/ByteFormer.
   Evidence status: observation.
   Reasoning: Authors state the architecture is adapted, and describe MegaByte (author-reported) as already modelling bytes across modalities; the paper does not state how bGPT's architecture differs. Difference not independently verified.
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture
   Source `paper:chars/7775-10479`: MegaByte (Yu et al., 2023), on the other hand,
has been tested and proven to excel in modelling long byte
sequences across various modalities.
   - **Suggested revision:** State explicitly what (if anything) differs from MegaByte's patch design; otherwise frame as reuse.

5. **Mixed-modality pre-training (bGPT_mix) underperforms text-only bGPT_wiki on AG News. This bears on claims of cross-modal benefit.**
   The paper reports the gap but does not show whether it reflects a reduced share of text data or genuine interference between modalities.
   Evidence status: inference.
   Reasoning: The confirmed records show that bGPT_mix includes ImageNet, LibriSpeech, and Wikipedia. On AG News it scores 1.0935 BPB and 91.75% accuracy, compared with 1.0639 BPB and 92.49% for bGPT_wiki. Adding modalities therefore did not help, and slightly hurt, in-domain text performance. The paper states this comparison itself.
   Source `review-record:visual/47`: Caption names GPT2-small on AG News, ViT-B/16 on CIFAR-10, AST on Speech Commands v2; bGPT_signal = ImageNet+LibriSpeech, bGPT_mix = ImageNet, LibriSpeech, Wikipedia.
   Source `review-record:visual/50`: bGPT_mix row shows 1.0935 BPB and 91.75 Acc on AG News, lower than bGPT_wiki's bold 92.49.
   Source `paper:chars/23083-23186`: bGPTsignal
combined the ImageNet and LibriSpeech datasets, while
bGPTmix integrated all three datasets.
   Source `paper:chars/26907-27073`: bGPTmix on
the AG News dataset, with a BPB of 1.0935 and accuracy of
91.75%, outperforms other variants but falls short of the per-

formance demonstrated by bGPTwiki
   - **Suggested revision:** Clarify whether the amount of text data or compute was matched between bGPT_mix and bGPT_wiki. If it was not, note this as a confound.

6. **The cross-modal transfer analysis is a modest but informative contribution. However, the 'modality-agnostic' claim is weakened by the negative transfer the authors report from text.**
   Novelty relative to ByteFormer and MegaByte transfer studies is not discussed.
   Evidence status: observation.
   Reasoning: Mixed results, plus a Table 4 BPB difference of 0.0001 between the image and audio models, do not support a general modality-agnostic transfer claim.
   Source `paper:chars/25015-30472`: negative trans-
fer is observed when transitioning between text and other
modalities
   - **Suggested revision:** Scope the transfer claim and report variance across seeds.

7. **The CPU States dataset is a new synthetic benchmark. It is clearly specified but deliberately simplified, and the authors acknowledge that it excludes jumps and real CPUs.**
   Evidence status: observation.
   Reasoning: The authors' candid scoping limits the dataset's impact, but it remains a reusable testbed.
   Source `paper:chars/36748-38535`: our
CPU state modelling experiments focused solely on simpli-
fied CPUs, omitting the use of real modern CPUs

8. **The stated preprocessing specifications in Section 4.1 match the per-file byte sizes reported in Table 1.**
   The header arithmetic shows the files are uncompressed fixed-length inputs, as described. This does not establish the correctness of any model results. Authors could briefly state the header-inclusive arithmetic in the Table 1 discussion so readers can check it.
   Evidence status: inference.
   Reasoning: The record quotes WAV at 8000 Hz, mono, 8-bit, trimmed to one second, and BMP at 32×32 RGB, 24-bit. It notes Table 1 mean sizes of about 8044 B for audio and 3126 B for images. The audio payload is 8000 Hz × 1 s × 1 byte = 8000 B, plus a standard 44 B WAV header, giving 8044 B. The image payload is 32 × 32 × 3 B = 3072 B, plus a 54 B BMP header, giving 3126 B. The data description therefore agrees internally with the reported statistics. This resolves one specific question: whether the byte-level input sizes follow from the stated formats.
   Source `review-record:visual/64`: Text states WAV, 8000 Hz sampling rate, mono, 8-bit depth, one-second lengths; BMP 32×32, RGB, 24-bit depth.
   Source `paper:chars/18196-18454`: Audio files were converted to WA V
format, with specifications including an 8000 Hz sampling
rate, mono channel, and 8-bit depth, each trimmed to one-
second lengths. Image data were set to BMP format with a
resolution of 32×32, RGB colour, and 24-bit depth.

9. **Limitations and dual-use risks (IP, reverse engineering) are acknowledged candidly.**
   Could link limitations back to softened abstract.
   Evidence status: observation.
   Reasoning: Direct statements of scope and risk.
   Source `paper:chars/36748-38535`: our
CPU state modelling experiments focused solely on simpli-
fied CPUs
   Source `paper:chars/38535-40096`: it poses a risk to
intellectual property
   - **Suggested revision:** Optional.

## Evidence to examine (advisory)

### Rendered formulas: Eq. (2) renders P_N = [b_{(N−1)S+1}, …, b_T, e, …, e] with an underbrace labelled S−(T mod S).

Scope: paper-only; analysis: visual; evidence status: inference.
The padding count S−(T mod S) correctly fills the last patch to S bytes when T mod S ≠ 0, which is consistent with the stated condition and definition.

- Source: `review-record:visual/0`
- Source: `paper:chars/12937-13031`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Eq. (3) renders E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N. Nearby text states that W_linear has shape (S × 257, H).

Scope: paper-only; analysis: visual; evidence status: inference.
A flattened S×257 one-hot patch multiplied by an (S×257, H) matrix yields an H-dimensional vector. This is consistent with the stated 257D encoding (256 byte values plus <eop>).

- Source: `review-record:visual/1`
- Source: `paper:chars/13936-14031`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: The page renders N = ⌈T/S⌉ and P_i = [b_{(i−1)S+1}, …, b_{iS}] for 1 ≤ i ≤ N.

Scope: paper-only; analysis: visual; evidence status: inference.
The ceiling function gives the correct number of patches, and the index ranges partition the sequence into S-byte patches.

- Source: `review-record:visual/2`
- Source: `paper:chars/11776-11818`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Captions: Figure 2 is a diagram labelled, from bottom to top: Byte Patches, Linear Projection Layer, Patch Embeds & Position Embeds (0, 1, 2, N), Patch-Level Transformer Decoder, Patch Features & Input Bytes, Byte-Level Transformer Decoder, and Output Bytes. Byte patches contain four bytes each, and <eop> padding is visible.

Scope: paper-only; analysis: visual; evidence status: inference.
The diagram matches the caption and the three components described in the text. The illustrative 4-byte patch is a schematic and does not conflict with the patch size of 16 used in the experiments.

- Source: `review-record:visual/3`
- Source: `paper:chars/12668-12863`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Units: The text states that each byte is one-hot encoded into a 257D vector covering all 256 byte values and an <eop> token.

Scope: paper-only; analysis: visual; evidence status: inference.
256 + 1 = 257, which is internally consistent.

- Source: `review-record:visual/7`
- Source: `paper:chars/13514-13612`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Sample counts: The CPU States row shows Total Files (Million) = 2.1, Total Bytes (GB) = 6.09, Mean File Size (Byte) = 3103 and GPU hours per Epoch = 36.

Scope: paper-only; analysis: visual; evidence status: inference.
The 2.1 million file count in the table matches the 2.1 million instances stated in the text.

- Source: `review-record:visual/8`
- Source: `paper:chars/20705-20794`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: The column headers are 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)' and 'GPU hours per Epoch'. The caption cites NVIDIA V100 GPU hours.

Scope: paper-only; analysis: visual; evidence status: inference.
The units in the column headers match the units described in the caption.

- Source: `review-record:visual/9`
- Source: `paper:chars/19668-19816`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: Approximate products of Total Files × Mean File Size agree with Total Bytes. Examples: Wikipedia 6.28M × 2237 ≈ 14.0e9; LibriSpeech 3.68M × 8044 ≈ 29.6e9 (27.57 GiB); CPU States 2.1M × 3103 ≈ 6.5e9 (6.09 GiB).

Scope: paper-only; analysis: visual; evidence status: inference.
The values are internally consistent if GB is read as binary gigabytes (GiB), allowing for rounding.

- Source: `review-record:visual/10`
- Source: `paper:chars/20328-20366`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Budgets: Table 2 lists Patch Size 16/16, Patch Length 512/512, Patch-Level Layers 12/12, Byte-Level Layers 3/3, Hidden Size 768/768, Epochs 32/32, Learning Rate 1e-04/1e-05 and Batch Size 16/1.

Scope: paper-only; analysis: visual; evidence status: inference.
16 × 512 = 8192 bytes, which equals 8KB. The patch size and length match the text.

- Source: `review-record:visual/11`
- Source: `paper:chars/21970-22056`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Budgets: The largest mean file sizes are 8044 bytes for LibriSpeech and Speech Commands v2.

Scope: paper-only; analysis: visual; evidence status: inference.
8044 bytes is within the 8192-byte context. The audio specification of 8000 Hz, 8-bit, 1 s gives 8000 bytes plus a WAV header, which is consistent with 8044.

- Source: `review-record:visual/12`
- Source: `paper:chars/21970-22001`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: units (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/13`
- Source: `paper:chars/18363-18454`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: The CPU States mean file size is 3103 bytes.

Scope: paper-only; analysis: visual; evidence status: inference.
1024 bytes plus about 128 states × 16 bytes is roughly 3.1KB, which is consistent with the paper's average of 128 instructions.

- Source: `review-record:visual/14`
- Source: `paper:chars/20896-21048`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: The caption reads 'Hyperparameter settings for pre-training and fine-tuning.' The columns are Pre-training and Fine-tuning.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption matches the table content.

- Source: `review-record:visual/15`
- Source: `paper:chars/22396-22462`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: units (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/18`
- Source: `paper:chars/829-1076`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: sample counts (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/24`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: units (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/25`
- Source: `paper:chars/35098-35117`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: sample counts (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/26`
- Source: `paper:chars/35174-35329`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: axes (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/27`
- Source: `paper:chars/35331-35430`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: rendered formulas (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/28`
- Source: `paper:chars/33102-33160`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/31`
- Source: `paper:chars/67936-68096`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/32`
- Source: `paper:chars/69753-69985`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Reviewer coverage limitation: units (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Grounding failure: context, citation or readability. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/33`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Reviewer coverage limitation: sample counts (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/38`
- Source: `paper:chars/30886-30975`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: axes (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/39`
- Source: `paper:chars/31646-31709`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: axes (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/40`
- Source: `paper:chars/35331-35430`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: captions (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/41`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: sample counts (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/42`
- Source: `paper:chars/35044-35117`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: captions (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/43`
- Source: `paper:chars/29729-29801`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: rendered formulas (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/44`
- Source: `paper:chars/31203-31238`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: units (paper:p.7)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/45`
- Source: `paper:chars/32923-33012`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: Caption names GPT2-small on AG News, ViT-B/16 on CIFAR-10, AST on Speech Commands v2; bGPT_signal = ImageNet+LibriSpeech, bGPT_mix = ImageNet, LibriSpeech, Wikipedia.

Scope: paper-only; analysis: visual; evidence status: inference.
Caption composition of mixed models and baselines matches Sections 5.2 and 5.2.1.

- Source: `review-record:visual/47`
- Source: `paper:chars/23083-23186`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Sample counts: Column headers: AG News (4 classes), CIFAR-10 (10 classes), Speech Commands v2 (36 classes).

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered class counts match the extracted table text.

- Source: `review-record:visual/48`
- Source: `paper:chars/24561-24634`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Units: Metrics labeled BPB and Acc (%); values such as 1.0639/92.49, 3.1234/88.69, 1.4818/96.03, baselines 0.9237/94.50, 98.13, 98.11.

Scope: paper-only; analysis: visual; evidence status: inference.
Values and units in the rendered table agree with the body text, including 88.69% vs 98.13% and 96.03% vs 98.11%.

- Source: `review-record:visual/49`
- Source: `paper:chars/25826-25993`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Captions: bGPT_mix row shows 1.0935 BPB and 91.75 Acc on AG News, lower than bGPT_wiki's bold 92.49.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered numbers support the textual comparison.

- Source: `review-record:visual/50`
- Source: `paper:chars/26907-27073`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Units: Text reads 'transformed into 32×32 BMP spectrograms... converting 8KB audio files to 3KB images'.

Scope: paper-only; analysis: visual; evidence status: inference.
Consistent with Table 1 mean file sizes (8044 bytes audio, 3126 bytes images) and Section 4.1 32×32 resolution.

- Source: `review-record:visual/51`
- Source: `paper:chars/28540-28633`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Sample counts: Page 17 states that the dataset comprises 2.1 million entries for the training set and 21,000 entries for the evaluation set.

Scope: paper-only; analysis: visual; evidence status: inference.
The 2.1 million training count matches the Section 4.2 description, 'CPU States dataset (with 2.1 million instances)', and Table 1, 'CPU States (proposed) 2.1'.

- Source: `review-record:visual/55`
- Source: `paper:chars/75331-75450`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Units: The page describes 1KB memory blocks paired with 16-byte register-state sequences. It lists PC as 1 byte, ACC as 1 byte, IR as 4 bytes, and general-purpose registers as 10 bytes.

Scope: paper-only; analysis: visual; evidence status: inference.
The listed register sizes sum to 16 bytes (1+1+4+10). This matches the stated 16-byte state and the Section 4.2 description.

- Source: `review-record:visual/56`
- Source: `paper:chars/72023-72159`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Sample counts: The page says that instruction sequences vary 'in length from 1 to 256' and that there are 'over 516 million potential scenarios'.

Scope: paper-only; analysis: visual; evidence status: inference.
The 1–256 range matches Section 4.2. The figure of over 516 million scenarios also appears in Section 5.3.2.

- Source: `review-record:visual/57`
- Source: `paper:chars/21430-21510`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Units: Each instruction is shown in a four-byte format, OP ADDR1 ADDR2 ADDR3, with 1 byte per field.

Scope: paper-only; analysis: visual; evidence status: inference.
Four fields of 1 byte each total 4 bytes, which matches the 4-byte instruction register.

- Source: `review-record:visual/58`
- Source: `paper:chars/21303-21360`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Sample counts: The example program list shows 10 instructions ending with 'HLT', and the text refers to '10 instructions'.

Scope: paper-only; analysis: visual; evidence status: inference.
The visible program list contains 10 entries, and the last entry is HLT.

- Source: `review-record:visual/59`
- Source: `paper:chars/75731-75827`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Rendered formulas: Eq. (5) renders as \hat b_{i,j} = Decoder_byte(\hat E_i, b_{i,<j}), 1 ≤ j ≤ S, with hats and subscripts intact.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered formula matches the extracted text and the surrounding definition of a per-patch byte decoder.

- Source: `review-record:visual/61`
- Source: `paper:chars/15098-15146`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: Eq. (6) renders as L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,...,b_i;θ).

Scope: paper-only; analysis: visual; evidence status: inference.
Summation limits 1 to T−1 are consistent with predicting b_{i+1} for a length-T sequence; extraction garbling of Σ is noise.

- Source: `review-record:visual/62`
- Source: `paper:chars/15800-15858`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: Eq. (7) renders as L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B;θ).

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered cross-entropy form matches the text; K is defined as total number of categories.

- Source: `review-record:visual/63`
- Source: `paper:chars/16662-16704`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Units: Text states WAV, 8000 Hz sampling rate, mono, 8-bit depth, one-second lengths; BMP 32×32, RGB, 24-bit depth.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered units match extracted text and are consistent with Table 1 mean file sizes (~8044 B audio, 3126 B images).

- Source: `review-record:visual/64`
- Source: `paper:chars/18196-18454`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Reviewer coverage limitation: captions (paper:p.2)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/69`
- Source: `paper:chars/4825-5002`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Captions: Caption reads 'Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.' Score shows key signature of two sharps (D major), 3/4 time, tempo marking quarter = 120.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption matches the text. The two-sharp key and 3/4 meter are consistent with the ABC header 'M:3/4' and 'K:D'.

- Source: `review-record:visual/81`
- Source: `paper:chars/65157-65255`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Reviewer coverage limitation: sample counts (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/82`
- Source: `paper:chars/69986-70197`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Reviewer coverage limitation: units (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/83`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Captions: Sheet music with key signature of two sharps (D major), 3/4 time signature, chord symbols D, A, C, G/B, Bm, F#m, G; caption reads 'Figure 4. Sheet music example corresponding to the ABC notation of a folk tune in D major.'

Scope: paper-only; analysis: visual; evidence status: inference.
Two-sharp key signature and 3/4 meter match the caption and the ABC header K:D and M:3/4.

- Source: `review-record:visual/111`
- Source: `paper:chars/62105-62195`
- Source: `paper:p.14`
- Source: [`review-output:visual/page-14.png`](visual/page-14.png)

### Reviewer coverage limitation: axes (paper:p.14)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/112`
- Source: `paper:chars/62883-62949`
- Source: `paper:p.14`
- Source: [`review-output:visual/page-14.png`](visual/page-14.png)

### Reviewer coverage limitation: units (paper:p.14)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/113`
- Source: `paper:chars/63489-63552`
- Source: `paper:p.14`
- Source: [`review-output:visual/page-14.png`](visual/page-14.png)

### Reviewer coverage limitation: sample counts (paper:p.19)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/117`
- Source: `paper:chars/21049-21133`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Reviewer coverage limitation: sample counts (paper:p.19)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/118`
- Source: `paper:chars/21049-21133`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Reviewer coverage limitation: captions (paper:p.19)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/119`
- Source: `paper:chars/73809-73956`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Reviewer coverage limitation: sample counts (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/121`
- Source: `paper:chars/75731-75868`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

### Rendered formulas: The rendered register and ACC values match the extracted text exactly. Examples: J becomes 38 at step 2, ACC is 1 at step 3, E is 255 at step 4, and ACC is 0 at step 10.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered values are consistent with the supplied text. Each state reflects the effect of the previous IR, which is consistent with the shown progression.

- Source: `review-record:visual/122`
- Source: `paper:chars/77525-77564`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

### Reviewer coverage limitation: units (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/123`
- Source: `paper:chars/72539-72582`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

## Direct visual evidence (advisory)

- **agreement**, rendered page 3, rendered formulas: Eq. (2) renders P_N = [b_{(N−1)S+1}, …, b_T, e, …, e] with an underbrace labelled S−(T mod S).
  Paper quote: where e represents the <eop> (end-of-patch) token used to
pad the last patch PN to the size S.. The padding count S−(T mod S) correctly fills the last patch to S bytes when T mod S ≠ 0, which is consistent with the stated condition and definition.
- **agreement**, rendered page 3, rendered formulas: Eq. (3) renders E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N. Nearby text states that W_linear has shape (S × 257, H).
  Paper quote: where Wlinear is the weight matrix of the linear projection
layer with a shape of (S × 257, H).. A flattened S×257 one-hot patch multiplied by an (S×257, H) matrix yields an H-dimensional vector. This is consistent with the stated 257D encoding (256 byte values plus <eop>).
- **agreement**, rendered page 3, rendered formulas: The page renders N = ⌈T/S⌉ and P_i = [b_{(i−1)S+1}, …, b_{iS}] for 1 ≤ i ≤ N.
  Paper quote: where N = ⌈ T
S ⌉ is the number of patches. The ceiling function gives the correct number of patches, and the index ranges partition the sequence into S-byte patches.
- **agreement**, rendered page 3, captions: Figure 2 is a diagram labelled, from bottom to top: Byte Patches, Linear Projection Layer, Patch Embeds & Position Embeds (0, 1, 2, N), Patch-Level Transformer Decoder, Patch Features & Input Bytes, Byte-Level Transformer Decoder, and Output Bytes. Byte patches contain four bytes each, and <eop> padding is visible.
  Paper quote: Figure 2. bGPT segments byte sequences into patches, predicts
next patch features with a patch-level decoder, and reconstructs
bytes within patches using these features with a byte-level decoder.. The diagram matches the caption and the three components described in the text. The illustrative 4-byte patch is a schematic and does not conflict with the patch size of 16 used in the experiments.
- **agreement**, rendered page 3, units: The text states that each byte is one-hot encoded into a 257D vector covering all 256 byte values and an <eop> token.
  Paper quote: each byte is one-hot encoded into a 257D vector, including
all 256 byte values and an <eop> token.. 256 + 1 = 257, which is internally consistent.
- **agreement**, rendered page 5, sample counts: The CPU States row shows Total Files (Million) = 2.1, Total Bytes (GB) = 6.09, Mean File Size (Byte) = 3103 and GPU hours per Epoch = 36.
  Paper quote: For CPU state modelling, we introduce the CPU States
dataset (with 2.1 million instances). The 2.1 million file count in the table matches the 2.1 million instances stated in the text.
- **agreement**, rendered page 5, units: The column headers are 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)' and 'GPU hours per Epoch'. The caption cites NVIDIA V100 GPU hours.
  Paper quote: Details include
file counts in millions, dataset sizes in gigabytes, average file sizes in bytes, and the GPU hours required per epoch for training.. The units in the column headers match the units described in the caption.
- **agreement**, rendered page 5, units: Approximate products of Total Files × Mean File Size agree with Total Bytes. Examples: Wikipedia 6.28M × 2237 ≈ 14.0e9; LibriSpeech 3.68M × 8044 ≈ 29.6e9 (27.57 GiB); CPU States 2.1M × 3103 ≈ 6.5e9 (6.09 GiB).
  Paper quote: CPU States (proposed) 2.1 6.09 3103 36. The values are internally consistent if GB is read as binary gigabytes (GiB), allowing for rounding.
- **agreement**, rendered page 5, budgets: Table 2 lists Patch Size 16/16, Patch Length 512/512, Patch-Level Layers 12/12, Byte-Level Layers 3/3, Hidden Size 768/768, Epochs 32/32, Learning Rate 1e-04/1e-05 and Batch Size 16/1.
  Paper quote: supporting file sizes up to
8KB using a patch size of 16 and a sequence length of 512.. 16 × 512 = 8192 bytes, which equals 8KB. The patch size and length match the text.
- **agreement**, rendered page 5, budgets: The largest mean file sizes are 8044 bytes for LibriSpeech and Speech Commands v2.
  Paper quote: supporting file sizes up to
8KB. 8044 bytes is within the 8192-byte context. The audio specification of 8000 Hz, 8-bit, 1 s gives 8000 bytes plus a WAV header, which is consistent with 8044.
- **agreement**, rendered page 5, units: The CPU States mean file size is 3103 bytes.
  Paper quote: Each dataset instance contains a 1KB
memory block with varying numbers of machine instruc-
tions, followed by a sequence of 16-byte CPU register states.. 1024 bytes plus about 128 states × 16 bytes is roughly 3.1KB, which is consistent with the paper's average of 128 instructions.
- **agreement**, rendered page 5, captions: The caption reads 'Hyperparameter settings for pre-training and fine-tuning.' The columns are Pre-training and Fine-tuning.
  Paper quote: Table 2. Hyperparameter settings for pre-training and fine-tuning.. The caption matches the table content.
- **agreement**, rendered page 6, captions: Caption names GPT2-small on AG News, ViT-B/16 on CIFAR-10, AST on Speech Commands v2; bGPT_signal = ImageNet+LibriSpeech, bGPT_mix = ImageNet, LibriSpeech, Wikipedia.
  Paper quote: bGPTsignal
combined the ImageNet and LibriSpeech datasets, while
bGPTmix integrated all three datasets.. Caption composition of mixed models and baselines matches Sections 5.2 and 5.2.1.
- **agreement**, rendered page 6, sample counts: Column headers: AG News (4 classes), CIFAR-10 (10 classes), Speech Commands v2 (36 classes).
  Paper quote: AG News (4 classes) CIFAR-10 (10 classes) Speech Commands v2 (36 classes). Rendered class counts match the extracted table text.
- **agreement**, rendered page 6, units: Metrics labeled BPB and Acc (%); values such as 1.0639/92.49, 3.1234/88.69, 1.4818/96.03, baselines 0.9237/94.50, 98.13, 98.11.
  Paper quote: bGPTwiki
achieved a score of 1.0639 BPB and an accuracy of 92.49%
on AG News, which, while not quite at the level of GPT2-
small, scored 0.9237 BPB and 94.50% accuracy. Values and units in the rendered table agree with the body text, including 88.69% vs 98.13% and 96.03% vs 98.11%.
- **agreement**, rendered page 6, captions: bGPT_mix row shows 1.0935 BPB and 91.75 Acc on AG News, lower than bGPT_wiki's bold 92.49.
  Paper quote: bGPTmix on
the AG News dataset, with a BPB of 1.0935 and accuracy of
91.75%, outperforms other variants but falls short of the per-

formance demonstrated by bGPTwiki. Rendered numbers support the textual comparison.
- **agreement**, rendered page 6, units: Text reads 'transformed into 32×32 BMP spectrograms... converting 8KB audio files to 3KB images'.
  Paper quote: This process, converting 8KB audio files to
3KB images, inevitably leads to information loss.. Consistent with Table 1 mean file sizes (8044 bytes audio, 3126 bytes images) and Section 4.1 32×32 resolution.
- **agreement**, rendered page 17, sample counts: Page 17 states that the dataset comprises 2.1 million entries for the training set and 21,000 entries for the evaluation set.
  Paper quote: The dataset thus produced comprises 2.1 million entries for the training set and 21,000 entries for the evaluation set.. The 2.1 million training count matches the Section 4.2 description, 'CPU States dataset (with 2.1 million instances)', and Table 1, 'CPU States (proposed) 2.1'.
- **agreement**, rendered page 17, units: The page describes 1KB memory blocks paired with 16-byte register-state sequences. It lists PC as 1 byte, ACC as 1 byte, IR as 4 bytes, and general-purpose registers as 10 bytes.
  Paper quote: The dataset comprises entries of 1KB memory blocks, each paired with a subsequent 16-byte sequence representing the
CPU register states.. The listed register sizes sum to 16 bytes (1+1+4+10). This matches the stated 16-byte state and the Section 4.2 description.
- **agreement**, rendered page 17, sample counts: The page says that instruction sequences vary 'in length from 1 to 256' and that there are 'over 516 million potential scenarios'.
  Paper quote: Instances are generated by execut-
ing random sequences of 1 to 256 instructions. The 1–256 range matches Section 4.2. The figure of over 516 million scenarios also appears in Section 5.3.2.
- **agreement**, rendered page 17, units: Each instruction is shown in a four-byte format, OP ADDR1 ADDR2 ADDR3, with 1 byte per field.
  Paper quote: 4 bytes are allocated for the Instruc-
tion Register (IR). Four fields of 1 byte each total 4 bytes, which matches the 4-byte instruction register.
- **agreement**, rendered page 17, sample counts: The example program list shows 10 instructions ending with 'HLT', and the text refers to '10 instructions'.
  Paper quote: a randomly generated program for executing
10 instructions along with their corresponding states. The visible program list contains 10 entries, and the last entry is HLT.
- **agreement**, rendered page 4, rendered formulas: Eq. (5) renders as \hat b_{i,j} = Decoder_byte(\hat E_i, b_{i,<j}), 1 ≤ j ≤ S, with hats and subscripts intact.
  Paper quote: ˆbi,j = Decoderbyte( ˆEi, bi,<j), 1 ≤ j ≤ S, (5). Rendered formula matches the extracted text and the surrounding definition of a per-patch byte decoder.
- **agreement**, rendered page 4, rendered formulas: Eq. (6) renders as L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,...,b_i;θ).
  Paper quote: LGEN(θ) =−
T −1X

i=1

log p(bi+1|b1, b2, ..., bi; θ), (6). Summation limits 1 to T−1 are consistent with predicting b_{i+1} for a length-T sequence; extraction garbling of Σ is noise.
- **agreement**, rendered page 4, rendered formulas: Eq. (7) renders as L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B;θ).
  Paper quote: LCLF(θ) =−
KX

k=1

yk log p(yk|B; θ), (7). Rendered cross-entropy form matches the text; K is defined as total number of categories.
- **agreement**, rendered page 4, units: Text states WAV, 8000 Hz sampling rate, mono, 8-bit depth, one-second lengths; BMP 32×32, RGB, 24-bit depth.
  Paper quote: Audio files were converted to WA V
format, with specifications including an 8000 Hz sampling
rate, mono channel, and 8-bit depth, each trimmed to one-
second lengths. Image data were set to BMP format with a
resolution of 32×32, RGB colour, and 24-bit depth.. Rendered units match extracted text and are consistent with Table 1 mean file sizes (~8044 B audio, 3126 B images).
- **agreement**, rendered page 15, captions: Caption reads 'Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.' Score shows key signature of two sharps (D major), 3/4 time, tempo marking quarter = 120.
  Paper quote: Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.. The rendered caption matches the text. The two-sharp key and 3/4 meter are consistent with the ABC header 'M:3/4' and 'K:D'.
- **agreement**, rendered page 14, captions: Sheet music with key signature of two sharps (D major), 3/4 time signature, chord symbols D, A, C, G/B, Bm, F#m, G; caption reads 'Figure 4. Sheet music example corresponding to the ABC notation of a folk tune in D major.'
  Paper quote: Figure 4. Sheet music example corresponding to the ABC notation of a folk tune in D major.. Two-sharp key signature and 3/4 meter match the caption and the ABC header K:D and M:3/4.
- **agreement**, rendered page 18, rendered formulas: The rendered register and ACC values match the extracted text exactly. Examples: J becomes 38 at step 2, ACC is 1 at step 3, E is 255 at step 4, and ACC is 0 at step 10.
  Paper quote: State at step 10:
PC: 10
ACC: 0
IR: HLT. The rendered values are consistent with the supplied text. Each state reflects the effect of the previous IR, which is consistent with the shown progression.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 29 |
| Confirmed text-image mismatch (advisory) | 0 |
| Not applicable | 70 |
| Grounding failure: context, citation or readability | 1 |
| Missing or invalid confirmation | 19 |
| Conflicting assessments | 6 |
| Substantive uncertainty | 2 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.


