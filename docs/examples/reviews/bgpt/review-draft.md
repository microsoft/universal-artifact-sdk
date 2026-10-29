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

The paper presents bGPT, a byte-level model trained with next-byte prediction and built on a hierarchical, patch-based Transformer adapted from prior work. It evaluates the model on media classification and generation for text, audio and images. It also evaluates the model on binary-native tasks that the authors describe as underexplored: ABC↔MIDI data conversion, framed as algorithm simulation, and CPU state modelling, framed as hardware simulation. For the latter, the authors introduce a CPU States dataset of 2.1 million instances, which they describe as a simplified representation of CPU behaviour.

## Contributions

1. **bGPT: next-byte-prediction model for digital world simulation.** Introduces bGPT, a generative model trained via next byte prediction on native binary data to model digital media and simulate algorithms and hardware, treating all data types as byte sequences in a unified framework.
   *Claim support (inferred links): unassessed · Significance: unassessed · Originality: contested*
2. **Hierarchical patch-based Transformer with generative and classification objectives.** bGPT segments byte sequences into fixed-size patches processed by a patch-level decoder and a byte-level decoder, trained with next-byte generative loss and then adapted to classification via pooled features.
   *Claim support (inferred links): unassessed · Significance: unassessed · Originality: unresolved*
3. **Modality-agnostic digital media modelling and cross-modal transfer.** bGPT performs byte-level generation and classification on text, audio and images comparably to specialized models without modality-specific design, and exhibits cross-modal knowledge transfer between pre-training and fine-tuning modalities.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unassessed*
4. **Algorithm simulation via ABC–MIDI data conversion.** bGPT learns to simulate and reverse a symbolic music conversion algorithm between text ABC notation and binary MIDI, achieving 0.0011 bits per byte for ABC-to-MIDI conversion.
   *Claim support (inferred links): contested · Significance: supported · Originality: unassessed*
5. **CPU States dataset for hardware behaviour modelling.** Introduces a 2.1-million-instance synthetic dataset of machine-instruction memory blocks paired with sequences of 16-byte CPU register states for evaluating CPU behaviour simulation.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unresolved*
6. **Near-perfect CPU state simulation with emergent scaling behaviour.** bGPT predicts CPU register state updates from machine instructions with over 99.99% accuracy, showing strong data scalability and an emergent jump in capability.
   *Claim support (inferred links): contested · Significance: supported · Originality: unassessed*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: bGPT: next-byte-prediction model for digital world simulation

**Claim support (inferred links): unassessed**
- Linked claims:
  - claim-1 (inferred by the paper adapter's extractor, not declared by the authors): bGPT achieves 0.0011 BPB on MIDI when converting ABC notation to MIDI with 10^5 training examples, orders of magnitude better than bGPT3.
  - claim-2 (inferred by the paper adapter's extractor, not declared by the authors): bGPT5 and bGPT6 reach near-perfect CPU state modelling accuracy.
  - claim-3 (inferred by the paper adapter's extractor, not declared by the authors): bGPT matches specialized models across text, audio and images.
  - claim-5 (inferred by the paper adapter's extractor, not declared by the authors): bGPTlibri reaches 96.03% on Speech Commands v2 vs AST 98.11%.
  - claim-4 (inferred by the paper adapter's extractor, not declared by the authors): bGPTwiki gets 1.0639 BPB and 92.49% on AG News vs GPT2-small 0.9237 BPB and 94.50%.
  - claim-15 (inferred by the paper adapter's extractor, not declared by the authors): BPB for both conversion directions decreases significantly with data scale.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- Authors position bGPT as extending byte modelling to native binary data and digital-system simulation, while acknowledging ByteFormer, MegaByte and MambaByte already model bytes across modalities and that the architecture is inspired by prior hierarchical work.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7775-10479, paper:chars/10851-15278

Paper’s wording: “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”

### Contribution 2: Hierarchical patch-based Transformer with generative and classification objectives

**Claim support (inferred links): unassessed**
- Linked claims:
  - claim-1 (inferred by the paper adapter's extractor, not declared by the authors): bGPT achieves 0.0011 BPB on MIDI when converting ABC notation to MIDI with 10^5 training examples, orders of magnitude better than bGPT3.
  - claim-2 (inferred by the paper adapter's extractor, not declared by the authors): bGPT5 and bGPT6 reach near-perfect CPU state modelling accuracy.
  - claim-3 (inferred by the paper adapter's extractor, not declared by the authors): bGPT matches specialized models across text, audio and images.
  - claim-5 (inferred by the paper adapter's extractor, not declared by the authors): bGPTlibri reaches 96.03% on Speech Commands v2 vs AST 98.11%.
  - claim-4 (inferred by the paper adapter's extractor, not declared by the authors): bGPTwiki gets 1.0639 BPB and 92.49% on AG News vs GPT2-small 0.9237 BPB and 94.50%.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- How does bGPT's hierarchical patch architecture differ from MegaByte? The authors say the architecture is inspired by prior work and place their novelty in applying byte models to native binary data and simulation tasks, but they do not state the architectural difference.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/10851-15278, paper:chars/7775-10479

Paper’s wording: “We start by present- ing its hierarchical Transformer framework, which segments byte sequences into patches to manage computational effi- ciency. Subsequently, we present the training objectives of bGPT, including generative modelling and classification”

### Contribution 3: Modality-agnostic digital media modelling and cross-modal transfer

**Claim support (inferred links): contested**
- Linked claims:
  - claim-3 (inferred by the reviewer, not declared by the authors): bGPT matches specialized models across text, audio and images.
  - claim-4 (inferred by the reviewer, not declared by the authors): bGPTwiki gets 1.0639 BPB and 92.49% on AG News vs GPT2-small 0.9237 BPB and 94.50%.
  - claim-5 (inferred by the reviewer, not declared by the authors): bGPTlibri reaches 96.03% on Speech Commands v2 vs AST 98.11%.
  - claim-6 (inferred by the reviewer, not declared by the authors): bGPTimage lags ViT on CIFAR-10 (88.69% vs 98.13%).
  - claim-7 (inferred by the reviewer, not declared by the authors): Pre-training dataset matching the downstream task improves performance.
  - claim-8 (inferred by the reviewer, not declared by the authors): Mixed-modality pre-training yields performance near the average of single-modality models; bGPTmix gets 1.0935 BPB / 91.75% on AG News, below bGPTwiki.
  - claim-10 (inferred by the reviewer, not declared by the authors): Cross-modal fine-tuning shows positive transfer between audio and images over random init.
  - claim-13 (inferred by the reviewer, not declared by the authors): bGPTlibri achieves higher spectrogram accuracy than bGPTimage, showing content-aligned cross-modal transfer.
- The abstract says bGPT "matches" specialized models, but Table 3 shows clear gaps on every task, notably CIFAR-10 at 88.69% vs 98.13%.
- 'Matches specialized models' in the abstract is stronger than Table 3, which shows a ~9.4-point CIFAR-10 gap.
- Sources: paper:chars/172-1238, paper:chars/25015-30472, paper:chars/23408-25015

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “Our experiments demonstrate the effectiveness of bGPT in modelling digital media data, which showcases modality-agnostic knowledge transfer.”

### Contribution 4: Algorithm simulation via ABC–MIDI data conversion

**Claim support (inferred links): contested**
- Linked claims:
  - claim-1 (inferred by the reviewer, not declared by the authors): bGPT achieves 0.0011 BPB on MIDI when converting ABC notation to MIDI with 10^5 training examples, orders of magnitude better than bGPT3.
  - claim-14 (inferred by the reviewer, not declared by the authors): Larger data scale gives lower starting loss and faster convergence in data conversion.
  - claim-15 (inferred by the reviewer, not declared by the authors): BPB for both conversion directions decreases significantly with data scale.
- The ABC→MIDI result of 0.0011 BPB is supported by Table 5. The "almost flawlessly replicated" wording rests on BPB alone; the paper reports no exact-match conversion rate.
- Sources: paper:chars/31335-34448, paper:chars/172-1238

**Significance: supported**
- The algorithm and hardware simulation tasks are the most distinctive and potentially impactful part of the paper. They show near-perfect learned simulation of a format converter and of a toy CPU directly from bytes.
- Sources: paper:chars/31335-34448, paper:chars/34448-36748

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “It has almost flawlessly replicated the process of converting symbolic music data, achieving a low error rate of 0.0011 bits per byte in converting ABC notation to MIDI format.”

### Contribution 5: CPU States dataset for hardware behaviour modelling

**Claim support (inferred links): contested**
- Linked claims:
  - claim-2 (inferred by the paper adapter's extractor, not declared by the authors): bGPT5 and bGPT6 reach near-perfect CPU state modelling accuracy.
  - claim-18 (inferred by the paper adapter's extractor, not declared by the authors): bGPT5 shows a sudden improvement around epoch 11, an emergent ability in CPU state modelling.
- The 'emergent ability' and 'beyond memorization' claims for CPU modelling rest on a simplified, jump-free synthetic CPU without baselines.
- Sources: paper:chars/34448-36748, paper:chars/30472-31335

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The CPU States dataset is a new and openly specified resource. The authors acknowledge it is a simplified CPU without jumps.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/18456-21674, paper:chars/36748-38535

Paper’s wording: “For CPU state modelling, we introduce the CPU States dataset (with 2.1 million instances), offering a simplified representation of CPU behaviour for ease of data collec- tion and evaluation”

### Contribution 6: Near-perfect CPU state simulation with emergent scaling behaviour

**Claim support (inferred links): contested**
- Linked claims:
  - claim-2 (inferred by the reviewer, not declared by the authors): bGPT5 and bGPT6 reach near-perfect CPU state modelling accuracy.
  - claim-18 (inferred by the reviewer, not declared by the authors): bGPT5 shows a sudden improvement around epoch 11, an emergent ability in CPU state modelling.
- The CPU accuracy is byte-wise and teacher-forced, and both the emergence and the generalization arguments are weakly supported. bGPT5 and bGPT6 also have identical BPB, which complicates the "strong scalability" claim.
- Sources: paper:chars/34448-36748, paper:chars/31335-34448

**Significance: supported**
- Framing binary-format conversion and CPU-state prediction as byte-level simulation tasks is a distinctive agenda likely to interest byte-model, program-analysis and security researchers.
- Sources: paper:chars/1238-5446, paper:chars/31335-34448, paper:chars/34448-36748

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “We observe a strong scalability of bGPT in mod- elling native binary data and even signs of emergent abilities”

<details><summary>What the authors say is original (3 statements)</summary>

Authors' stated position:
- [claims, builds on] “Inspired by the success of next token prediction in natural lan- guage processing, we introduce bGPT, a model with next byte prediction to simulate the digi- tal world. bGPT matches specialized models in performance across various modalities, including text, audio, and images, and offers new possibil- ities for predicting, simulating, and diagnosing algorithm or hardware behaviour.”
- [claims; positioned against Raff et al., 2018, Guo et al., 2019] “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”
- [claims, builds on] “Conclusions In this paper, we present bGPT as a versatile simulator for the digital world, extending deep learning to binary data processing via next byte prediction.”

</details>

#### Contribution declaration checks (structural)

- Warning, contribution 4: claim support not declared or inferred.

## Reasons to accept

1. **Framing algorithm and hardware simulation (ABC→MIDI conversion, CPU state prediction) as next-byte prediction is a distinctive task framing. It could attract follow-up work on byte models, binary analysis and learned emulation.**
   Likely users include researchers working on byte models, security analysis and learned emulators.
   Evidence status: inference.
   Reasoning: The authors state that these tasks lack baselines and datasets. Within the paper's positioning, that makes the task framing the most original element and a plausible seed for new benchmarks.
   Source `paper:chars/18456-21674`: This necessitates the ability to simulate and
reverse-engineer the conversion algorithm
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets,

2. **The strongest reason to publish is the reframing of byte models as simulators of algorithms and hardware. Near-zero BPB on ABC→MIDI and >99.9% CPU-state accuracy make this an evocative demonstration.**
   This framing could open a line of work on learned emulation and reverse engineering, which is also discussed in the Impact section.
   Evidence status: inference.
   Reasoning: Learning a deterministic conversion program and an instruction-level state machine purely from bytes is a qualitatively different use of byte models from the media tasks emphasized in the related work. The scaling results suggest the capability is learnable.
   Source `paper:chars/31335-34448`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   Source `paper:chars/34448-36748`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%)

3. **The paper's scope is distinctive: it extends byte-level modelling from media files to algorithm and hardware simulation tasks.**
   One model is used for media classification and generation, ABC↔MIDI conversion, and CPU state prediction.
   Evidence status: inference.
   Reasoning: The authors evaluate the same byte model on binary-native simulation tasks, which they describe as underexplored. That scope makes the work a potentially impactful direction rather than only another media benchmark result.
   Source `paper:chars/1238-5446`: underexplored tasks intrinsic to binary-native operations,
including data conversion and CPU state modelling, which
represent algorithm and hardware simulation, respectively.

4. **The paper frames byte-level modelling of native binary data, including algorithm and hardware simulation, as an underexplored and potentially impactful direction. It provides concrete testbeds for this direction.**
   The likely impact rests on reframing byte models as simulators of algorithms and hardware, not only as media encoders.
   Evidence status: inference.
   Reasoning: The paper identifies a neglected data class. It then provides a new dataset and tasks (conversion, CPU simulation) that make that class studyable. This could seed follow-up work.
   Source `paper:chars/1238-5446`: These deep learning models, however, predominantly op-
erate within the realm of media data, overlooking the om-
nipresent native binary data in the digital world.
   Source `paper:chars/18456-21674`: For CPU state modelling, we introduce the CPU States
dataset (with 2.1 million instances)

## Originality

By the paper's own related-work section, byte-level modelling across modalities is not new. MegaByte is described as handling long byte sequences across modalities, ByteFormer as handling raw image and audio bytes, and bGPT's hierarchy as adapted from earlier work that includes Yu et al. (2023). The originality therefore appears to lie mainly in the task framing: algorithm and hardware simulation treated as next-byte prediction over native binary data, together with the accompanying CPU States dataset. The abstract presents bGPT as an introduced model, which reads broader than these concessions support. The architectural difference from MegaByte is not stated. The novelty of the CPU States dataset relative to prior work on learning program execution is not positioned, so its primacy cannot be judged from the paper. This assessment relies on the paper's own description of the cited works, which were not inspected independently.

## Likely impact

Researchers working on byte models, binary and security analysis, and learned emulation are the most likely to benefit. The paper supplies concrete testbeds in a space it says lacks baselines and datasets. Two results are evocative: near-zero BPB (0.0011) on ABC→MIDI conversion and above 99.9% byte-wise CPU-state accuracy. Together they suggest that deterministic conversion programs and simple state machines may be learnable from bytes, which could seed follow-up benchmarks. Several factors may limit this influence. The CPU task is simplified and appears to exclude control flow. The reported metrics (teacher-forced BPB and per-byte accuracy) may overstate functional correctness. No baselines are provided for the simulation tasks. On the media tasks, bGPT trails modality-specific models, so impact there is likely to be modest.

## Decision-critical concerns

1. **The abstract's claim that bGPT "matches specialized models" is overstated, given the paper's own CIFAR-10 gap (88.69% vs 98.13%).**
   Text and audio results come close to the baselines; image results do not.
   Evidence status: inference.
   Reasoning: The abstract claims parity across text, audio, and images, but the reported image result trails the baseline by a large margin. The ViT and AST numbers are copied from other studies, so the comparison is not controlled.
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities, including
text, audio, and images
   Source `paper:chars/25015-30472`: bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%
   Source `paper:chars/23408-25015`: ViT and AST
were pre-trained on ImageNet (Deng et al., 2009), and their
results were taken from the original studies.
   - **Why this affects the decision:** This is the headline modality-agnostic claim.
   - **Actionable revision:** Soften the abstract and conclusion wording, or report matched-setting image and audio baselines.
   - **What would resolve it:** Either revised claims or matched-setting baselines that show parity.

2. **The abstract's claim that bGPT "matches specialized models" is stronger than the results. The CIFAR-10 accuracy gap is large, and the image and audio baselines are taken from original studies rather than trained under matched conditions.**
   Results on text and audio are close to the baselines. Results on images are clearly worse.
   Evidence status: inference.
   Reasoning: A gap of nearly 10 points on CIFAR-10 contradicts "matches." Baselines copied from the original studies may differ in input resolution and pretraining. The comparison is therefore not controlled.
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities, including
text, audio, and images
   Source `paper:chars/25015-30472`: bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%
   Source `paper:chars/23408-25015`: ViT and AST
were pre-trained on ImageNet (Deng et al., 2009), and their
results were taken from the original studies.
   - **Why this affects the decision:** The headline claim in the abstract is overstated relative to Table 3.
   - **Actionable revision:** Revise the abstract and conclusion to say "competitive on text/audio, lagging on images". Report or justify the input conditions of the ViT/AST baselines.
   - **What would resolve it:** Either revised wording, or baselines evaluated at 32×32 inputs with comparable pretraining.

3. **C2 (>99.99% CPU accuracy) is reported, but the task excludes control flow. The per-byte metric may also be dominated by bytes that are trivially predictable.**
   The paper itself notes there are no baselines: 'Due to the lack of baseline models'.
   Evidence status: inference.
   Reasoning: The accuracy is computed per byte. Without jumps, PC increments deterministically, and IR is copied from the instruction memory. Most register bytes are also unchanged at each step. A copy-previous-state-plus-increment-PC baseline could therefore score very high. The 99.99% figure does not by itself show arithmetic simulation.
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   Source `paper:chars/18456-21674`: Within each state, 1
byte each is allocated for the Program Counter (PC) and
Accumulator (ACC), 4 bytes are allocated for the Instruc-
tion Register (IR)
   - **Why this affects the decision:** The paper's headline hardware-simulation claim depends on the metric reflecting non-trivial state updates.
   - **Actionable revision:** Report a trivial copy/increment baseline. Also report accuracy restricted to changed bytes (ACC and destination registers) and per-instruction-type accuracy, plus whole-state or whole-program exact match.
   - **What would resolve it:** A clear margin over the trivial baseline on changed bytes and on full-sequence exact match.

4. **The paper's related-work section credits ByteFormer and MegaByte with byte-level, cross-modality modelling. bGPT's originality therefore appears to lie in its native-binary-simulation framing and tasks, not in byte modelling or the patch architecture.**
   The abstract's framing of bGPT as an introduced model reads broader than the related-work concessions support.
   Evidence status: inference.
   Reasoning: The authors report that MegaByte already models long byte sequences across modalities and that ByteFormer handles image and audio bytes. They also say bGPT's hierarchy is adapted from prior work, including Yu et al. 2023. On their own positioning, the differentiator is native binary data and simulation tasks. The abstract nonetheless introduces bGPT as the model. The architectural difference from MegaByte is never stated. This review has not inspected the cited works.
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
   Source `paper:chars/7775-10479`: Despite progress, current research often neglects native bi-
nary data, focusing on narrow tasks
   Source `paper:chars/172-1238`: we introduce bGPT, a model
with next byte prediction to simulate the digi-
tal world.
   - **Why this affects the decision:** Originality credit depends on whether bGPT differs architecturally from MegaByte or only in the tasks it is applied to.
   - **Actionable revision:** Add an explicit comparison with MegaByte and ByteFormer covering architecture, objectives and tasks. State that the patch hierarchy is adopted from prior work.
   - **What would resolve it:** Either a stated technical difference from MegaByte, or an explicit scoping of the novelty to the binary-simulation tasks and the evaluation.

## Questions for the authors

1. **CPU-state accuracy jumps from 27.24% (10^4) to 99.97% (10^5). The definition of accuracy and the train/test separation for randomly generated programs need clarification.**
   Near-perfect CPU simulation is a central claim. Its strength depends on the metric granularity and on held-out novelty.
   Evidence status: inference.
   Reasoning: Table 6 shows bGPT4 at 0.6924/27.2404 and bGPT5/bGPT6 both at BPB 0.0969 with 99.97 and 99.99 accuracy. Instances are random programs of 1–256 instructions. A near-step change, followed by an identical BPB from 10^5 to 10^6, makes it important to know two things: what counts as a correct prediction (full state, per byte, or per register), and whether test programs or prefixes could overlap with training programs.
   Source `review-record:visual/44`: Table 6 shows bGPT4 0.6924/27.2404, bGPT5 0.0969/99.9702 and bGPT6 0.0969/99.9961.
   Source `review-record:visual/72`: Random instruction sequences 'varying in length from 1 to 256'; 'over 516 million potential scenarios'.
   Source `paper:chars/35044-35117`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%)
   Source `paper:chars/21430-21510`: Instances are generated by execut-
ing random sequences of 1 to 256 instructions
   - **Why the answer matters:** If accuracy is measured per byte, or if test programs overlap with training, the claim of learning CPU execution weakens substantially.
   - **Requested response:** Define the accuracy unit. Report the deduplication or overlap rate between train and test programs. Give accuracy by program length.
   - **Answer that would resolve it:** A metric definition, an overlap statistic, and a length-stratified accuracy table.

2. **Table 5 supports C1 (0.0011 BPB on ABC→MIDI). However, 'almost flawlessly replicated' rests on a teacher-forced likelihood, not on the correctness of generated conversions.**
   If exact matches are rare, the 'flawless' framing should be softened.
   Evidence status: inference.
   Reasoning: A near-zero BPB is consistent with flawless conversion. It does not show that generated MIDI files are byte-exact or valid.
   Source `paper:chars/31335-34448`: bGPT5 0.7362 0.0011 0.1341 0.0789
   Source `paper:chars/31335-34448`: While
BPBmidi evaluates data conversion, considering the com-
plete ABC byte sequence is given.
   - **Why the answer matters:** The answer determines whether the algorithm-simulation claim is substantiated beyond likelihood.
   - **Requested response:** Report the exact-match rate and validity rate of generated MIDI files on the test set.
   - **Answer that would resolve it:** A high rate of byte-exact generated MIDI files.

3. **The emergence claim rests on a training-curve jump around epoch 11. Is this robust across seeds, and could it reflect an optimization plateau rather than a scale-driven ability?**
   If the jump is seed-dependent, the emergence framing should be dropped.
   Evidence status: inference.
   Reasoning: A single run's loss jump within training is a different phenomenon from emergence with scale.
   Source `paper:chars/34448-36748`: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b, indicating
an emergent ability in CPU state modelling.
   - **Why the answer matters:** Multi-seed evidence would support the scalability and emergence claims made in the conclusion.
   - **Requested response:** Report multiple seeds and the timing of the jump.
   - **Answer that would resolve it:** A consistent jump across seeds, and an absent jump at the smaller data scale.

## Decision synthesis

On the positive side, the most important evidence is the reframing of byte models as simulators of algorithms and hardware. One model covers media and binary-native tasks, and the scaling results suggest that the simulation tasks are learnable. This framing, the new dataset and the testbeds are the paper's main contribution.

On the negative side, three issues matter most.

First, the abstract states that bGPT "matches specialized models" across text, audio and images. The paper's own Table 3 shows bGPT trailing on every task: about 2 points on text, about 2.1 points on audio and about 9.4 points on CIFAR-10 (88.69% vs 98.13%). The mixed model is lower still. In addition, the ViT and AST numbers are taken from the original studies rather than trained under matched conditions.

Second, the headline CPU result may be weaker than it appears. Accuracy is computed byte-wise, and the task lacks jumps. As a result, the PC likely increments deterministically, the IR is copied from instruction memory and most register bytes are unchanged at each step. A trivial copy-previous-state-plus-increment-PC baseline might therefore score highly, and such a baseline is not reported.

Third, the novelty is narrower than the abstract implies, given the paper's own account of MegaByte and ByteFormer.

Score-changing questions:
(a) How exactly is CPU-state accuracy defined (full state, per register or per byte)? How are train and test programs separated? The jump from 27.24% at 10^4 to 99.97% at 10^5, followed by identical BPB at 10^6, makes this important.
(b) Are generated MIDI outputs byte-exact or valid? 'Almost flawlessly replicated' currently rests on teacher-forced likelihood.
(c) Is the epoch-11 jump in bGPT5 robust across seeds? A jump within a single run's training is distinct from emergence with scale.

Non-blocking improvements:
- Scope the competitiveness claims to the reported gaps.
- Support 'beyond memorization' with a measured overlap analysis rather than combinatorial-space size alone.
- Position the CPU States dataset against prior execution-modelling work.
- Clarify whether the 16-byte patch size intentionally aligns with the 16-byte register state, and whether the CPU results depend on that alignment. This remains an open question, not an established defect.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The abstract states two concrete headline results in plain terms, which makes the central claim easy to locate.

**Writing-quality issues**

1. **The abstract's media claim says bGPT 'matches' specialized models. Section 5.2.2 reports a clear gap on CIFAR-10, so the plain-language headline overstates what the paper's own results show.**
   The image-classification shortfall is a legitimate partial result and should stay. It belongs in the headline sentence.
   - **Suggested revision:** Rephrase the abstract to say bGPT approaches specialized models on text and audio, and trails them on images (88.69% vs 98.13% on CIFAR-10).

2. **The abstract calls 0.0011 bits per byte an 'error rate'. Bits per byte is not introduced until Section 5.1 and is a likelihood measure, not an error rate, so non-specialists cannot interpret the headline number.**
   A plain gloss would make the strongest result legible.
   - **Suggested revision:** In the abstract, briefly explain BPB (e.g., average uncertainty per predicted byte, where 0 means perfect prediction) or report an interpretable conversion accuracy instead.

3. **The text reports 43 instruction variants, but Table 7 enumerates 44.**
   Table 7's enumerated address variants sum to 44, while the text states 43 variants across 21 instruction types.
   - **Suggested revision:** Reconcile the variant count between the text and Table 7. Either correct the number or state the counting convention, for example whether HLT's no-address form is counted.

4. **Accuracies are reported with four decimal places, and the text uses evaluative adjectives ('impressively', 'exceptional') that assert strength the reader could see from the numbers alone.**
   For readability, round to two decimal places and let the comparisons speak.
   - **Suggested revision:** Round Table 6 to sensible precision and replace evaluative adjectives with a comparison (e.g., 'roughly 200× lower than bGPT3').

5. **The text reports 99.9961% as 99.99%, which truncates rather than rounds the value.**
   This is a cosmetic inconsistency.
   - **Suggested revision:** Use a consistent rounding convention, or report the values at the same precision as the table.

## Additional improvements (non-blocking)

1. **Table 3 shows bGPT trailing modality-specific baselines on every task, with the largest gap on CIFAR-10. Claims of competitiveness should be scoped to match.**
   Gaps: 2.0 points (text), 2.1 points (audio), 9.4 points (image). The mixed model also degrades relative to the specialized model.
   Evidence status: inference.
   Reasoning: The rendered Table 3 values are bGPT_wiki 92.49 vs 94.50 (AG News), bGPT_libri 96.03 vs AST 98.11, and bGPT_image 88.69 vs ViT 98.13. bGPT_mix is lower still (1.0935 BPB, 91.75). The text openly states the AG News shortfall. These cells show a gap of roughly 9.4 points on image classification, which limits any claim that byte-level modelling matches native-modality models.
   Source `review-record:visual/55`: Rendered values include bGPT_wiki at 1.0639 BPB and 92.49%, the AG News baseline at 0.9237 and 94.50, bGPT_libri at 96.03, the AST baseline at 98.11, bGPT_image at 88.69, and the ViT baseline at 98.13. bGPT_mix is shown at 1.0935 and 91.75.
   Source `review-record:visual/53`: Column headers read 'AG News (4 classes)', 'CIFAR-10 (10 classes)', 'Speech Commands v2 (36 classes)'.
   Source `paper:chars/25826-25993`: bGPTwiki
achieved a score of 1.0639 BPB and an accuracy of 92.49%
on AG News, which, while not quite at the level of GPT2-
small, scored 0.9237 BPB and 94.50% accuracy
   Source `paper:chars/24561-24634`: AG News (4 classes) CIFAR-10 (10 classes) Speech Commands v2 (36 classes)
   - **Suggested revision:** State the per-modality gaps explicitly in the abstract or discussion, especially the CIFAR-10 gap. Discuss whether matched model size or compute explains the gaps.

2. **The CPU States dataset is proposed as new and is self-described as simplified. Its primacy relative to prior work on learning program execution is not positioned.**
   Positioning the dataset against prior work would strengthen the dataset claim.
   Evidence status: observation.
   Reasoning: The authors explicitly propose this dataset and describe it as simplified. Its originality against execution-modelling literature cannot be judged from the background section.
   Source `paper:chars/18456-21674`: we introduce the CPU States
dataset (with 2.1 million instances), offering a simplified
representation of CPU behaviour
   - **Suggested revision:** Cite and contrast prior datasets for neural program-execution or CPU simulation.

3. **The abstract says bGPT 'matches specialized models', but the paper's own results show gaps, most notably on CIFAR-10 (88.69% vs 98.13%).**
   Cross-modal transfer is a useful observation but should be framed alongside these gaps.
   Evidence status: observation.
   Reasoning: The paper's own results show bGPT trailing the baseline on CIFAR-10, so 'matches' overstates the outcome.
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities
   Source `paper:chars/25015-30472`: a noticeable difference
is seen with bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%.
   - **Suggested revision:** Revise the abstract to 'approaches' and note the per-modality gaps.

4. **The 'beyond simple memorization' claim rests on accuracy plus combinatorial-space size, not on a measured train/test overlap.**
   The numbers are correctly rendered. The conclusion drawn from them goes further than the evidence supports.
   Evidence status: inference.
   Reasoning: The rendered text supports this inference with three premises: 99.97% and 99.99% accuracy, an average of 128 instructions per test case, and over 516 million possible combinations. A large space of possible combinations does not show that test sequences, or their subsequences, are absent from training. Generalization therefore remains inferred rather than demonstrated.
   Source `review-record:visual/20`: Text states bGPT^5 and bGPT^6 reach 99.97% and 99.99% accuracy, average of 128 random instructions, over 516 million combinations.
   Source `paper:chars/35098-35329`: (99.97% and 99.99%), suggesting an efficiency beyond sim-
ple memorization, given that each test case contained an
average of 128 random instructions, and the vast potential
combinations of instruction scenarios (over 516 million).
   - **Suggested revision:** Report the train/test overlap at the sequence or n-gram level, or evaluate on held-out instruction lengths or compositions.

5. **The patch size matches the CPU register-state size (16 bytes). It is unclear whether this alignment is intentional and whether CPU-state results depend on it.**
   Patch boundaries may coincide with state boundaries in the CPU States data. This could favour patch-level prediction in a way that does not carry over to other byte formats.
   Evidence status: inference.
   Reasoning: Record 15 confirms that each CPU register state is 16 bytes (1+1+4+10). Record 14 confirms the patch size is 16. If the program prefix length is a multiple of 16, each patch holds exactly one machine state. That would make CPU modelling structurally easier than byte streams whose semantic units do not align with patches. The records do not show whether the prefix is aligned, so this stays a question.
   Source `review-record:visual/15`: The text allocates 1 byte for PC, 1 for ACC, 4 for IR, and 10 for general-purpose registers, giving 16-byte register states.
   Source `review-record:visual/14`: Table 2 shows Patch Size 16, Patch Length 512, Patch-Level Layers 12, Byte-Level Layers 3, Hidden Size 768, Epochs 32, Learning Rate 1e-04/1e-05, and Batch Size 16/1.
   Source `paper:chars/20994-21048`: followed by a sequence of 16-byte CPU register states.
   Source `paper:chars/21970-22056`: supporting file sizes up to
8KB using a patch size of 16 and a sequence length of 512.
   - **Suggested revision:** State whether the program and state boundaries are aligned to the 16-byte patch grid. If feasible, report CPU-state accuracy with a misaligned offset or a different patch size.

6. **Table 4 differences between bGPT_image and bGPT_libri are very small (BPB 0.3899 vs 0.3900; Acc 84.66 vs 85.26).**
   The bolding implies a meaningful ranking that the values alone do not establish.
   Evidence status: inference.
   Reasoning: The rendered rows show a 0.0001 BPB gap and a 0.6-point accuracy gap, and bold marks each as best. At this magnitude, run-to-run variance could reverse the ordering. Any cross-modal transfer conclusion drawn from which pretraining set wins is therefore fragile without a variability estimate.
   Source `review-record:visual/40`: Table 4 lists bGPTrandom 0.4052/80.74, bGPTimage 0.3899/84.66, bGPTlibri 0.3900/85.26; 0.3899 and 85.26 are bold.
   Source `paper:chars/29311-29356`: bGPTimage 0.3899 84.66
bGPTlibri 0.3900 85.26
   - **Suggested revision:** Report seed variance or confidence intervals for Table 4, or soften the ranking language.

7. **Fig. 3a plots loss against epochs, so 'lower starting loss and more rapid convergence' at larger data scale may reflect more optimizer steps per epoch.**
   The claim is accurately described, but its interpretation as faster convergence is confounded by the epoch-based x-axis.
   Evidence status: inference.
   Reasoning: The record confirms that the x-axis is Epoch (0–32) for the bGPT^3, bGPT^4 and bGPT^5 scales. It also confirms that larger-scale curves start lower and flatten sooner. With a fixed epoch count, an epoch at 10^5 samples contains about 100× more updates than an epoch at 10^3. The first plotted point therefore already reflects far more training. The visible ordering supports the textual description, but it does not separate a data-scale effect from a compute or step-count effect.
   Source `review-record:visual/41`: Panel (a) has an Epoch x-axis from 0 to 32 and a Loss y-axis from 0.2 to 1.2. Its legend lists bGPT3/4/5 Train and Eval. Loss curves start lower for larger scales.
   Source `paper:chars/33304-33402`: We observe a lower starting loss and a more rapid con-
vergence in Fig. 3a as the data scale grows
   - **Suggested revision:** Add a version of Fig. 3a plotted against training steps or tokens seen, or qualify the convergence claim.

8. **The 8KB context limit and the dataset file-size statistics raise the question of how files longer than 8KB are handled.**
   Table 1 reports means only. The share of files that exceed the context, and how they are treated, is not visible in these records.
   Evidence status: inference.
   Reasoning: Record 14 fixes the maximum input at 16×512 = 8192 bytes. Record 13 reports only mean file sizes, such as 2237 bytes for Wikipedia. A mean far below the cap does not rule out a tail of files above 8KB. Truncating or excluding those files would affect how the reported results should be interpreted.
   Source `review-record:visual/13`: Wikipedia shows 6.28M files, 13.67 GB, and a mean of 2237 bytes. CPU States shows 2.1M files, 6.09 GB, and a mean of 3103 bytes.
   Source `review-record:visual/14`: Table 2 shows Patch Size 16, Patch Length 512, Patch-Level Layers 12, Byte-Level Layers 3, Hidden Size 768, Epochs 32, Learning Rate 1e-04/1e-05, and Batch Size 16/1.
   Source `paper:chars/19917-19964`: Wikipedia (Wikimedia, 2022) 6.28 13.67 2237 107
   Source `paper:chars/21970-22056`: supporting file sizes up to
8KB using a patch size of 16 and a sequence length of 512.
   - **Suggested revision:** Report the fraction of files that exceed 8KB in each dataset, and state whether they are truncated, split, or excluded.

9. **The ABC↔MIDI task is positioned as novel because prior music models avoided raw MIDI bytes. This is a plausible, author-reported distinction that this review did not verify.**
   Evidence status: observation.
   Reasoning: The authors' positioning relative to Huang et al., Zeng et al., and Hsiao et al. is stated but was not independently verified.
   Source `paper:chars/31335-34448`: While previous
studies avoided direct MIDI modelling due to its binary

10. **The authors explicitly attribute the hierarchical patch architecture to prior work, so it should not be credited as a novel contribution.**
   The paper does not state any difference from MegaByte.
   Evidence status: observation.
   Reasoning: The authors say bGPT 'adapts' this architecture, which disclaims architectural originality.
   Source `paper:chars/10851-15278`: bGPT adapts a hierarchical Trans-
former architecture and segments a sequence of bytes
   - **Suggested revision:** State which components, if any, differ from the cited hierarchical models.

## Evidence to examine (advisory)

### Rendered formulas: Eq. (1) renders as 𝒫 = [P1, P2, ..., PN], followed by N = ⌈T/S⌉ and P_i = [b_{(i−1)S+1}, ..., b_{iS}] for 1 ≤ i ≤ N, with the condition T mod S ≠ 0.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered patch definition matches the extracted text, apart from extraction noise in subscripts and the ceiling notation.

- Source: `review-record:visual/0`
- Source: `paper:chars/11744-11774`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: P_N = [b_{(N−1)S+1}, ..., b_T, e, ..., e], with an underbrace labelled S−(T mod S).

Scope: paper-only; analysis: visual; evidence status: inference.
The number of padding tokens, S−(T mod S), fills the last patch to size S. This is consistent with the text.

- Source: `review-record:visual/1`
- Source: `paper:chars/12865-12927`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N. W_linear has shape (S × 257, H).

Scope: paper-only; analysis: visual; evidence status: inference.
A flattened S×257 one-hot patch multiplied by an (S×257, H) matrix produces a hidden-size-H vector. The dimensions are consistent.

- Source: `review-record:visual/2`
- Source: `paper:chars/13942-14030`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Units: Each byte is one-hot encoded into a 257D vector covering all 256 byte values plus an <eop> token.

Scope: paper-only; analysis: visual; evidence status: inference.
256 + 1 = 257, which is internally consistent.

- Source: `review-record:visual/3`
- Source: `paper:chars/13514-13611`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Ê_i = Decoder_patch(ℰ_{<i} ⊕ 𝒳_{<i}).

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered equation matches the text definitions of ℰ_{<i} and 𝒳_{<i}.

- Source: `review-record:visual/4`
- Source: `paper:chars/14439-14473`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Captions: The diagram shows Byte Patches, a Linear Projection Layer, Patch Embeds & Position Embeds (0, 1, 2, N), a Patch-Level Transformer Decoder, and a Byte-Level Transformer Decoder producing Output Bytes. Byte patches include <eop> padding.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption matches the depicted components.

- Source: `review-record:visual/5`
- Source: `paper:chars/12668-12863`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Reviewer coverage limitation: rendered formulas (paper:p.3)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/6`
- Source: `paper:chars/21970-22026`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Sample counts: Table 1 row 'CPU States (proposed)' shows Total Files (Million) = 2.1; body text says 'CPU States dataset (with 2.1 million instances)'.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered table count matches the in-text instance count and the Appendix B training-set size.

- Source: `review-record:visual/10`
- Source: `paper:chars/20705-20794`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: Column headers read 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)', 'GPU hours per Epoch'; the caption names millions, gigabytes, bytes, and V100 GPU hours.

Scope: paper-only; analysis: visual; evidence status: inference.
The header units match the caption.

- Source: `review-record:visual/11`
- Source: `paper:chars/19668-19816`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Reviewer coverage limitation: units (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/12`
- Source: `paper:chars/18363-18454`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Sample counts: Wikipedia shows 6.28M files, 13.67 GB, and a mean of 2237 bytes. CPU States shows 2.1M files, 6.09 GB, and a mean of 3103 bytes.

Scope: paper-only; analysis: visual; evidence status: inference.
Multiplying file count by mean size gives about 14.0e9 bytes for Wikipedia, or about 13.1 GiB. For CPU States it gives about 6.5e9 bytes, or about 6.07 GiB. Both are roughly consistent with the table totals, assuming GB is close to GiB. The rendered values match the extracted text.

- Source: `review-record:visual/13`
- Source: `paper:chars/19917-19964`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Budgets: Table 2 shows Patch Size 16, Patch Length 512, Patch-Level Layers 12, Byte-Level Layers 3, Hidden Size 768, Epochs 32, Learning Rate 1e-04/1e-05, and Batch Size 16/1.

Scope: paper-only; analysis: visual; evidence status: inference.
16 × 512 = 8192 bytes, which equals 8KB. This matches the stated maximum file size, and the values match the extracted Table 2.

- Source: `review-record:visual/14`
- Source: `paper:chars/21970-22056`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: The text allocates 1 byte for PC, 1 for ACC, 4 for IR, and 10 for general-purpose registers, giving 16-byte register states.

Scope: paper-only; analysis: visual; evidence status: inference.
1 + 1 + 4 + 10 = 16 bytes.

- Source: `review-record:visual/15`
- Source: `paper:chars/20994-21048`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: The Table 1 caption describes datasets and V100 GPU hours, and the GPU-hours column is present with values ranging from 1.1 to 107.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption matches the table content.

- Source: `review-record:visual/16`
- Source: `paper:chars/19554-19667`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Rendered formulas: Model names render with subscripts: bGPT_image, bGPT_wiki, bGPT_libri, bGPT_signal, bGPT_mix, bGPT_random.

Scope: paper-only; analysis: visual; evidence status: inference.
The page renders these names correctly as subscripts. The extracted text flattens them, which is extraction noise.

- Source: `review-record:visual/17`
- Source: `paper:chars/22928-23031`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Rendered formulas: Page renders BPB with subscripts (BPB_abc, BPB_midi) and model names with superscript scale exponents (bGPT^5, bGPT^3); extracted text shows these flattened as 'BPBabc', 'bGPT5'.

Scope: paper-only; analysis: visual; evidence status: inference.
Flattened sub/superscripts are extraction noise; the rendered notation matches the intended data-scale labels (10^3–10^6) and the Table 5 value 0.0011.

- Source: `review-record:visual/19`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Sample counts: Text states bGPT^5 and bGPT^6 reach 99.97% and 99.99% accuracy, average of 128 random instructions, over 516 million combinations.

Scope: paper-only; analysis: visual; evidence status: inference.
Consistent with Table 6 (99.9702, 99.9961), the 1–256 instruction range (mean ≈128), and Appendix B's 516 million figure.

- Source: `review-record:visual/20`
- Source: `paper:chars/35098-35329`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Units: Rendered text says notable BPB drop from bGPT^4 to bGPT^5 with diminishing returns beyond bGPT^5.

Scope: paper-only; analysis: visual; evidence status: inference.
Table 6 lists BPB 0.6924 → 0.0969 → 0.0969, consistent with the description.

- Source: `review-record:visual/21`
- Source: `paper:chars/34960-35043`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: units (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/25`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: units (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/26`
- Source: `paper:chars/35044-35117`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: captions (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/27`
- Source: `paper:chars/26238-26302`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Rendered formulas: Rendered: \hat{b}_{i,j} = Decoder_byte(\hat{E}_i, b_{i,<j}), 1 ≤ j ≤ S, labeled (5).

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered equation matches the extracted text, apart from subscript formatting.

- Source: `review-record:visual/32`
- Source: `paper:chars/15098-15146`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: Rendered: L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,...,b_i; θ), labeled (6).

Scope: paper-only; analysis: visual; evidence status: inference.
The summation limits run from i=1 to T−1, which is consistent with next-byte prediction over a sequence of length T. This matches the text.

- Source: `review-record:visual/33`
- Source: `paper:chars/15800-15858`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: Rendered: L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B; θ), labeled (7).

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered equation matches the extracted text. K is defined as the total number of categories.

- Source: `review-record:visual/34`
- Source: `paper:chars/16662-16704`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Units: Text reads: WAV format, 8000 Hz sampling rate, mono channel, 8-bit depth, one-second lengths; BMP images at 32×32 resolution, RGB colour, 24-bit depth.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered units match the text. They are also consistent with Table 1 mean file sizes: 8000 bytes of audio plus a WAV header gives about 8044 bytes, and 32×32×3 bytes plus a BMP header gives 3126 bytes.

- Source: `review-record:visual/35`
- Source: `paper:chars/18196-18454`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Sample counts: Table 4 lists bGPTrandom 0.4052/80.74, bGPTimage 0.3899/84.66, bGPTlibri 0.3900/85.26; 0.3899 and 85.26 are bold.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered values match the text. They also support the claims of closely matched BPB and higher accuracy for bGPTlibri.

- Source: `review-record:visual/40`
- Source: `paper:chars/29311-29356`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Axes: Panel (a) has an Epoch x-axis from 0 to 32 and a Loss y-axis from 0.2 to 1.2. Its legend lists bGPT3/4/5 Train and Eval. Loss curves start lower for larger scales.

Scope: paper-only; analysis: visual; evidence status: inference.
The axes and legend match the extracted figure text. The visual curve ordering is consistent with the claim about lower starting loss.

- Source: `review-record:visual/41`
- Source: `paper:chars/33304-33402`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Axes: Panel (b) has an Epoch x-axis from 0 to 32 and a Loss y-axis from 0.4 to 1.6. Its legend lists bGPT4/5/6. The orange (bGPT5) curve drops sharply between about epochs 10 and 12.

Scope: paper-only; analysis: visual; evidence status: inference.
The drop in the orange curve appears near epoch 11, consistent with the text.

- Source: `review-record:visual/42`
- Source: `paper:chars/35331-35430`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Sample counts: Table 5 shows bGPT5 with BPBmidi 0.0011 for ABC→MIDI. The full rows are 1.4319/0.2381/0.2796/1.1227, 0.9789/0.0202/0.1751/0.1763, and 0.7362/0.0011/0.1341/0.0789.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered values match the extracted table and the textual claim.

- Source: `review-record:visual/43`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Sample counts: Table 6 shows bGPT4 0.6924/27.2404, bGPT5 0.0969/99.9702 and bGPT6 0.0969/99.9961.

Scope: paper-only; analysis: visual; evidence status: inference.
The rounded accuracies match the table. The identical BPB values for bGPT5 and bGPT6 are consistent with the text's claim of diminishing returns.

- Source: `review-record:visual/44`
- Source: `paper:chars/35044-35117`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Rendered formulas: The text renders 10^3 (bGPT^3), 10^4, 10^5 and 10^6 with proper superscripts. The table model labels also use superscripts.

Scope: paper-only; analysis: visual; evidence status: inference.
The extracted text loses the superscripts, but the rendered page shows the powers of ten correctly. This is extraction noise, not an authoring defect.

- Source: `review-record:visual/45`
- Source: `paper:chars/30886-30975`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: The caption reads 'Training and evaluation loss curves for different data scales in bGPT performance across epochs.' The panels show train and eval curves per scale.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption is consistent with the panel content.

- Source: `review-record:visual/46`
- Source: `paper:chars/32225-32331`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: Diagram shows .wav, .bmp (cat images), .mid (piano roll), .abc, and .bin (CPU chip labeled 0) on the left, all feeding into a central 'bGPT' box. Outputs on the right are an audio waveform, a 'Cat' label, sheet music, and CPU chips labeled 1, 2, 3 … N.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered diagram shows several data types going into one model, including binary CPU states that progress from 0 to N. This matches the caption's description.

- Source: `review-record:visual/47`
- Source: `paper:chars/4825-5002`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Sample counts: Column headers read 'AG News (4 classes)', 'CIFAR-10 (10 classes)', 'Speech Commands v2 (36 classes)'.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered class counts match the extracted table header text.

- Source: `review-record:visual/53`
- Source: `paper:chars/24561-24634`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: captions (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/54`
- Source: `paper:chars/23083-23186`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Units: Rendered values include bGPT_wiki at 1.0639 BPB and 92.49%, the AG News baseline at 0.9237 and 94.50, bGPT_libri at 96.03, the AST baseline at 98.11, bGPT_image at 88.69, and the ViT baseline at 98.13. bGPT_mix is shown at 1.0935 and 91.75.

Scope: paper-only; analysis: visual; evidence status: inference.
The BPB and Acc (%) values cited in the text match the rendered table cells and their units.

- Source: `review-record:visual/55`
- Source: `paper:chars/25826-25993`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Units: The text reads '32×32 BMP spectrograms' and 'converting 8KB audio files to 3KB images'.

Scope: paper-only; analysis: visual; evidence status: inference.
The sizes are consistent with Table 1, which lists mean file sizes of 8044 bytes for Speech Commands v2 and 3126 bytes for CIFAR-10 BMP files.

- Source: `review-record:visual/56`
- Source: `paper:chars/28540-28633`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/66`
- Source: `paper:chars/67936-68096`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/67`
- Source: `paper:chars/65157-65255`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Reviewer coverage limitation: rendered formulas (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/68`
- Source: `paper:chars/69986-70197`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Units: Page states 1KB memory blocks, 16-byte register state; PC 1 byte, ACC 1 byte, IR 4 bytes, general-purpose 10 bytes (sums to 16).

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered byte allocations match Section 4.2 and sum to the stated 16-byte state.

- Source: `review-record:visual/70`
- Source: `paper:chars/21207-21429`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Reviewer coverage limitation: sample counts (paper:p.17)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/71`
- Source: `paper:chars/20705-20794`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Sample counts: Random instruction sequences 'varying in length from 1 to 256'; 'over 516 million potential scenarios'.

Scope: paper-only; analysis: visual; evidence status: inference.
Range matches Section 4.2; 516 million matches Section 5.3.2 ('over 516 million').

- Source: `review-record:visual/72`
- Source: `paper:chars/21430-21510`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Sample counts: Text says program executes 10 instructions; listed program contains 10 items ending in 'HLT'; step 0 shows PC: 0, ACC: 146, IR: HLT.

Scope: paper-only; analysis: visual; evidence status: inference.
Ten listed instructions match the stated count and the HLT-termination rule.

- Source: `review-record:visual/73`
- Source: `paper:chars/75731-75868`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Reviewer coverage limitation: captions (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/84`
- Source: `paper:chars/65157-65255`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Reviewer coverage limitation: sample counts (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/85`
- Source: `paper:chars/69986-70138`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Reviewer coverage limitation: rendered formulas (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Grounding failure: context, citation or readability. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/86`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Captions: The sheet music has a two-sharp key signature (D major) and a 3/4 time signature. It contains measures numbered 6, 10 and 14, with chord labels D, A, C, G/B, Bm, F#m and G. The caption reads 'Sheet music example corresponding to the ABC notation of a folk tune in D major.'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered key signature and the chord symbols match the caption and the ABC header (K:D, M:3/4).

- Source: `review-record:visual/108`
- Source: `paper:chars/62105-62195`
- Source: `paper:p.14`
- Source: [`review-output:visual/page-14.png`](visual/page-14.png)

### Reviewer coverage limitation: units (paper:p.14)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/109`
- Source: `paper:chars/63489-63552`
- Source: `paper:p.14`
- Source: [`review-output:visual/page-14.png`](visual/page-14.png)

### Reviewer coverage limitation: sample counts (paper:p.19)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/114`
- Source: `paper:chars/21049-21133`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Sample counts: The Address Variants column shows: HLT has 0. CLR, INC, DEC, SHL, SHR, ROL, ROR, and NOT each have 0, 1. PUSH, POP, and LOADI each have 1. SWAP has 1, 2. ADD, SUB, MUL, DIV, AND, OR, and XOR each have 1, 2, 3. MOV has 2.

Scope: paper-only; analysis: visual; evidence status: inference.
Summing the listed variants gives 1 + 8×2 + 3×1 + 2 + 7×3 + 1 = 44. The text states 43 variants. The text does not define a counting convention that would exclude one variant.

- Source: `review-record:visual/115`
- Source: `paper:chars/21092-21133`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Captions: The caption reads 'Table 7. Defined instruction set and the address variants of different instructions.' The page number is 19.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption, table content, and page location all match the in-text reference.

- Source: `review-record:visual/116`
- Source: `paper:chars/73809-73956`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Sample counts: The page shows 'State at step 1' through 'State at step 10'. The IR values are, in order: MUL J A, DIV I, MUL E D, ADD C, LOADI 86, MOV A H, AND D E, POP H, CLR, HLT. Each state lists PC, ACC, IR and ten registers, A through J.

Scope: paper-only; analysis: visual; evidence status: inference.
Ten steps are shown, one for each of the ten listed program instructions, and PC runs from 1 to 10. Each state has ten general-purpose registers (A–J), which matches 'An additional 10 bytes are allocated, emulating a range of registers (labelled A-J)'. The rendered values match the extracted text.

- Source: `review-record:visual/121`
- Source: `paper:chars/75731-75868`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

### Reviewer coverage limitation: rendered formulas (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/122`
- Source: `paper:chars/72539-72627`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

### claim-1: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/0`

### claim-2: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/1`

### claim-3: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/2`

### claim-5: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/3`

### claim-18: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/4`

### claim-4: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/5`

### claim-15: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/6`

### claim-13: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/7`

### claim-6: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/8`

### claim-7: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/9`

### claim-8: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/10`

### claim-10: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/11`

### claim-14: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/12`

### claim-11: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/13`

### claim-9: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/14`

### claim-12: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/15`

### claim-16: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/16`

### claim-20: comparison unresolved

Scope: artifact-informed; analysis: comparison; evidence status: unassessed.
No declared result edge resolves.

- Source: `review-record:comparison/17`

## Direct visual evidence (advisory)

- **agreement**, rendered page 3, rendered formulas: Eq. (1) renders as 𝒫 = [P1, P2, ..., PN], followed by N = ⌈T/S⌉ and P_i = [b_{(i−1)S+1}, ..., b_{iS}] for 1 ≤ i ≤ N, with the condition T mod S ≠ 0.
  Paper quote: P = [P1, P2, . . . , PN ], (1). The rendered patch definition matches the extracted text, apart from extraction noise in subscripts and the ceiling notation.
- **agreement**, rendered page 3, rendered formulas: P_N = [b_{(N−1)S+1}, ..., b_T, e, ..., e], with an underbrace labelled S−(T mod S).
  Paper quote: PN = [b(N −1)S+1, . . . , bT , e, . . . , e| {z }

S−(T mod S). The number of padding tokens, S−(T mod S), fills the last patch to size S. This is consistent with the text.
- **agreement**, rendered page 3, rendered formulas: E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N. W_linear has shape (S × 257, H).
  Paper quote: Wlinear is the weight matrix of the linear projection
layer with a shape of (S × 257, H). A flattened S×257 one-hot patch multiplied by an (S×257, H) matrix produces a hidden-size-H vector. The dimensions are consistent.
- **agreement**, rendered page 3, units: Each byte is one-hot encoded into a 257D vector covering all 256 byte values plus an <eop> token.
  Paper quote: each byte is one-hot encoded into a 257D vector, including
all 256 byte values and an <eop> token. 256 + 1 = 257, which is internally consistent.
- **agreement**, rendered page 3, rendered formulas: Ê_i = Decoder_patch(ℰ_{<i} ⊕ 𝒳_{<i}).
  Paper quote: ˆEi = Decoderpatch(E<i ⊕ X<i), (4). The rendered equation matches the text definitions of ℰ_{<i} and 𝒳_{<i}.
- **agreement**, rendered page 3, captions: The diagram shows Byte Patches, a Linear Projection Layer, Patch Embeds & Position Embeds (0, 1, 2, N), a Patch-Level Transformer Decoder, and a Byte-Level Transformer Decoder producing Output Bytes. Byte patches include <eop> padding.
  Paper quote: Figure 2. bGPT segments byte sequences into patches, predicts
next patch features with a patch-level decoder, and reconstructs
bytes within patches using these features with a byte-level decoder.. The caption matches the depicted components.
- **agreement**, rendered page 5, sample counts: Table 1 row 'CPU States (proposed)' shows Total Files (Million) = 2.1; body text says 'CPU States dataset (with 2.1 million instances)'.
  Paper quote: For CPU state modelling, we introduce the CPU States
dataset (with 2.1 million instances). The rendered table count matches the in-text instance count and the Appendix B training-set size.
- **agreement**, rendered page 5, units: Column headers read 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)', 'GPU hours per Epoch'; the caption names millions, gigabytes, bytes, and V100 GPU hours.
  Paper quote: Details include
file counts in millions, dataset sizes in gigabytes, average file sizes in bytes, and the GPU hours required per epoch for training.. The header units match the caption.
- **agreement**, rendered page 5, sample counts: Wikipedia shows 6.28M files, 13.67 GB, and a mean of 2237 bytes. CPU States shows 2.1M files, 6.09 GB, and a mean of 3103 bytes.
  Paper quote: Wikipedia (Wikimedia, 2022) 6.28 13.67 2237 107. Multiplying file count by mean size gives about 14.0e9 bytes for Wikipedia, or about 13.1 GiB. For CPU States it gives about 6.5e9 bytes, or about 6.07 GiB. Both are roughly consistent with the table totals, assuming GB is close to GiB. The rendered values match the extracted text.
- **agreement**, rendered page 5, budgets: Table 2 shows Patch Size 16, Patch Length 512, Patch-Level Layers 12, Byte-Level Layers 3, Hidden Size 768, Epochs 32, Learning Rate 1e-04/1e-05, and Batch Size 16/1.
  Paper quote: supporting file sizes up to
8KB using a patch size of 16 and a sequence length of 512.. 16 × 512 = 8192 bytes, which equals 8KB. This matches the stated maximum file size, and the values match the extracted Table 2.
- **agreement**, rendered page 5, units: The text allocates 1 byte for PC, 1 for ACC, 4 for IR, and 10 for general-purpose registers, giving 16-byte register states.
  Paper quote: followed by a sequence of 16-byte CPU register states.. 1 + 1 + 4 + 10 = 16 bytes.
- **agreement**, rendered page 5, captions: The Table 1 caption describes datasets and V100 GPU hours, and the GPU-hours column is present with values ranging from 1.1 to 107.
  Paper quote: Table 1. Overview of datasets for bGPT evaluation, with computational costs benchmarked in NVIDIA V100 GPU hours.. The caption matches the table content.
- **agreement**, rendered page 5, rendered formulas: Model names render with subscripts: bGPT_image, bGPT_wiki, bGPT_libri, bGPT_signal, bGPT_mix, bGPT_random.
  Paper quote: bGPT on diverse datasets like ImageNet ( bGPTimage),
Wikipedia (bGPTwiki), and LibriSpeech (bGPTlibri).. The page renders these names correctly as subscripts. The extracted text flattens them, which is extraction noise.
- **agreement**, rendered page 8, rendered formulas: Page renders BPB with subscripts (BPB_abc, BPB_midi) and model names with superscript scale exponents (bGPT^5, bGPT^3); extracted text shows these flattened as 'BPBabc', 'bGPT5'.
  Paper quote: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion. Flattened sub/superscripts are extraction noise; the rendered notation matches the intended data-scale labels (10^3–10^6) and the Table 5 value 0.0011.
- **agreement**, rendered page 8, sample counts: Text states bGPT^5 and bGPT^6 reach 99.97% and 99.99% accuracy, average of 128 random instructions, over 516 million combinations.
  Paper quote: (99.97% and 99.99%), suggesting an efficiency beyond sim-
ple memorization, given that each test case contained an
average of 128 random instructions, and the vast potential
combinations of instruction scenarios (over 516 million).. Consistent with Table 6 (99.9702, 99.9961), the 1–256 instruction range (mean ≈128), and Appendix B's 516 million figure.
- **agreement**, rendered page 8, units: Rendered text says notable BPB drop from bGPT^4 to bGPT^5 with diminishing returns beyond bGPT^5.
  Paper quote: with a notable BPB drop from bGPT4 to

bGPT5, but diminishing returns beyond bGPT5.. Table 6 lists BPB 0.6924 → 0.0969 → 0.0969, consistent with the description.
- **agreement**, rendered page 4, rendered formulas: Rendered: \hat{b}_{i,j} = Decoder_byte(\hat{E}_i, b_{i,<j}), 1 ≤ j ≤ S, labeled (5).
  Paper quote: ˆbi,j = Decoderbyte( ˆEi, bi,<j), 1 ≤ j ≤ S, (5). The rendered equation matches the extracted text, apart from subscript formatting.
- **agreement**, rendered page 4, rendered formulas: Rendered: L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,...,b_i; θ), labeled (6).
  Paper quote: LGEN(θ) =−
T −1X

i=1

log p(bi+1|b1, b2, ..., bi; θ), (6). The summation limits run from i=1 to T−1, which is consistent with next-byte prediction over a sequence of length T. This matches the text.
- **agreement**, rendered page 4, rendered formulas: Rendered: L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B; θ), labeled (7).
  Paper quote: LCLF(θ) =−
KX

k=1

yk log p(yk|B; θ), (7). The rendered equation matches the extracted text. K is defined as the total number of categories.
- **agreement**, rendered page 4, units: Text reads: WAV format, 8000 Hz sampling rate, mono channel, 8-bit depth, one-second lengths; BMP images at 32×32 resolution, RGB colour, 24-bit depth.
  Paper quote: Audio files were converted to WA V
format, with specifications including an 8000 Hz sampling
rate, mono channel, and 8-bit depth, each trimmed to one-
second lengths. Image data were set to BMP format with a
resolution of 32×32, RGB colour, and 24-bit depth.. The rendered units match the text. They are also consistent with Table 1 mean file sizes: 8000 bytes of audio plus a WAV header gives about 8044 bytes, and 32×32×3 bytes plus a BMP header gives 3126 bytes.
- **agreement**, rendered page 7, sample counts: Table 4 lists bGPTrandom 0.4052/80.74, bGPTimage 0.3899/84.66, bGPTlibri 0.3900/85.26; 0.3899 and 85.26 are bold.
  Paper quote: bGPTimage 0.3899 84.66
bGPTlibri 0.3900 85.26. The rendered values match the text. They also support the claims of closely matched BPB and higher accuracy for bGPTlibri.
- **agreement**, rendered page 7, axes: Panel (a) has an Epoch x-axis from 0 to 32 and a Loss y-axis from 0.2 to 1.2. Its legend lists bGPT3/4/5 Train and Eval. Loss curves start lower for larger scales.
  Paper quote: We observe a lower starting loss and a more rapid con-
vergence in Fig. 3a as the data scale grows. The axes and legend match the extracted figure text. The visual curve ordering is consistent with the claim about lower starting loss.
- **agreement**, rendered page 7, axes: Panel (b) has an Epoch x-axis from 0 to 32 and a Loss y-axis from 0.4 to 1.6. Its legend lists bGPT4/5/6. The orange (bGPT5) curve drops sharply between about epochs 10 and 12.
  Paper quote: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b. The drop in the orange curve appears near epoch 11, consistent with the text.
- **agreement**, rendered page 7, sample counts: Table 5 shows bGPT5 with BPBmidi 0.0011 for ABC→MIDI. The full rows are 1.4319/0.2381/0.2796/1.1227, 0.9789/0.0202/0.1751/0.1763, and 0.7362/0.0011/0.1341/0.0789.
  Paper quote: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion. The rendered values match the extracted table and the textual claim.
- **agreement**, rendered page 7, sample counts: Table 6 shows bGPT4 0.6924/27.2404, bGPT5 0.0969/99.9702 and bGPT6 0.0969/99.9961.
  Paper quote: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%). The rounded accuracies match the table. The identical BPB values for bGPT5 and bGPT6 are consistent with the text's claim of diminishing returns.
- **agreement**, rendered page 7, rendered formulas: The text renders 10^3 (bGPT^3), 10^4, 10^5 and 10^6 with proper superscripts. The table model labels also use superscripts.
  Paper quote: utilizing data scales ranging from 103
(bGPT3), 104 (bGPT4), 105 (bGPT5), to 106 (bGPT6).. The extracted text loses the superscripts, but the rendered page shows the powers of ten correctly. This is extraction noise, not an authoring defect.
- **agreement**, rendered page 7, captions: The caption reads 'Training and evaluation loss curves for different data scales in bGPT performance across epochs.' The panels show train and eval curves per scale.
  Paper quote: Figure 3. Training and evaluation loss curves for different data
scales in bGPT performance across epochs.. The caption is consistent with the panel content.
- **agreement**, rendered page 2, captions: Diagram shows .wav, .bmp (cat images), .mid (piano roll), .abc, and .bin (CPU chip labeled 0) on the left, all feeding into a central 'bGPT' box. Outputs on the right are an audio waveform, a 'Cat' label, sheet music, and CPU chips labeled 1, 2, 3 … N.
  Paper quote: Figure 1. The bGPT framework simulates digital systems through native binary data, and integrates diverse data types into a single model,
treating everything as a byte sequence.. The rendered diagram shows several data types going into one model, including binary CPU states that progress from 0 to N. This matches the caption's description.
- **agreement**, rendered page 6, sample counts: Column headers read 'AG News (4 classes)', 'CIFAR-10 (10 classes)', 'Speech Commands v2 (36 classes)'.
  Paper quote: AG News (4 classes) CIFAR-10 (10 classes) Speech Commands v2 (36 classes). The rendered class counts match the extracted table header text.
- **agreement**, rendered page 6, units: Rendered values include bGPT_wiki at 1.0639 BPB and 92.49%, the AG News baseline at 0.9237 and 94.50, bGPT_libri at 96.03, the AST baseline at 98.11, bGPT_image at 88.69, and the ViT baseline at 98.13. bGPT_mix is shown at 1.0935 and 91.75.
  Paper quote: bGPTwiki
achieved a score of 1.0639 BPB and an accuracy of 92.49%
on AG News, which, while not quite at the level of GPT2-
small, scored 0.9237 BPB and 94.50% accuracy. The BPB and Acc (%) values cited in the text match the rendered table cells and their units.
- **agreement**, rendered page 6, units: The text reads '32×32 BMP spectrograms' and 'converting 8KB audio files to 3KB images'.
  Paper quote: This process, converting 8KB audio files to
3KB images, inevitably leads to information loss.. The sizes are consistent with Table 1, which lists mean file sizes of 8044 bytes for Speech Commands v2 and 3126 bytes for CIFAR-10 BMP files.
- **agreement**, rendered page 17, units: Page states 1KB memory blocks, 16-byte register state; PC 1 byte, ACC 1 byte, IR 4 bytes, general-purpose 10 bytes (sums to 16).
  Paper quote: Within each state, 1
byte each is allocated for the Program Counter (PC) and
Accumulator (ACC), 4 bytes are allocated for the Instruc-
tion Register (IR), with an additional 10 bytes reserved for
general-purpose registers.. Rendered byte allocations match Section 4.2 and sum to the stated 16-byte state.
- **agreement**, rendered page 17, sample counts: Random instruction sequences 'varying in length from 1 to 256'; 'over 516 million potential scenarios'.
  Paper quote: Instances are generated by execut-
ing random sequences of 1 to 256 instructions. Range matches Section 4.2; 516 million matches Section 5.3.2 ('over 516 million').
- **agreement**, rendered page 17, sample counts: Text says program executes 10 instructions; listed program contains 10 items ending in 'HLT'; step 0 shows PC: 0, ACC: 146, IR: HLT.
  Paper quote: a randomly generated program for executing
10 instructions along with their corresponding states in human-readable form is provided below. Ten listed instructions match the stated count and the HLT-termination rule.
- **agreement**, rendered page 14, captions: The sheet music has a two-sharp key signature (D major) and a 3/4 time signature. It contains measures numbered 6, 10 and 14, with chord labels D, A, C, G/B, Bm, F#m and G. The caption reads 'Sheet music example corresponding to the ABC notation of a folk tune in D major.'
  Paper quote: Figure 4. Sheet music example corresponding to the ABC notation of a folk tune in D major.. The rendered key signature and the chord symbols match the caption and the ABC header (K:D, M:3/4).
- **mismatch**, rendered page 19, sample counts: The Address Variants column shows: HLT has 0. CLR, INC, DEC, SHL, SHR, ROL, ROR, and NOT each have 0, 1. PUSH, POP, and LOADI each have 1. SWAP has 1, 2. ADD, SUB, MUL, DIV, AND, OR, and XOR each have 1, 2, 3. MOV has 2.
  Paper quote: totaling 21 unique
types with 43 variants. Summing the listed variants gives 1 + 8×2 + 3×1 + 2 + 7×3 + 1 = 44. The text states 43 variants. The text does not define a counting convention that would exclude one variant.
- **agreement**, rendered page 19, captions: The caption reads 'Table 7. Defined instruction set and the address variants of different instructions.' The page number is 19.
  Paper quote: Table 7 (located on page 19) details the instruction set and the variants each instruction can have, depending on the values in
the address fields.. The caption, table content, and page location all match the in-text reference.
- **agreement**, rendered page 18, sample counts: The page shows 'State at step 1' through 'State at step 10'. The IR values are, in order: MUL J A, DIV I, MUL E D, ADD C, LOADI 86, MOV A H, AND D E, POP H, CLR, HLT. Each state lists PC, ACC, IR and ten registers, A through J.
  Paper quote: a randomly generated program for executing
10 instructions along with their corresponding states in human-readable form is provided below. Ten steps are shown, one for each of the ten listed program instructions, and PC runs from 1 to 10. Each state has ten general-purpose registers (A–J), which matches 'An additional 10 bytes are allocated, emulating a range of registers (labelled A-J)'. The rendered values match the extracted text.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 37 |
| Confirmed text-image mismatch (advisory) | 1 |
| Not applicable | 73 |
| Grounding failure: context, citation or readability | 1 |
| Missing or invalid confirmation | 3 |
| Conflicting assessments | 10 |
| Substantive uncertainty | 2 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.

### Human inspection needed

Conflicting assessments and substantive uncertainties are unconfirmed, not author-facing findings. Confirmed mismatches are advisory, not scientific proof.

- **Substantive uncertainty**: `paper:p.3`, rendered_formulas (visual audit observation index 6).
  Observation: The byte patches are drawn with 4 bytes per patch, for example 'f5 6b 85 98'. Some patches are only partially readable at this resolution.
  Paper quote: supporting file sizes up to
8KB using a patch size of 16.
  Reason: The illustration's 4-byte patch size differs from the configured patch size of 16. It is likely schematic, but the figure does not state that, so whether it is an intended simplification is uncertain.

- **Conflicting assessments**: `paper:p.5`, units (visual audit observation index 12).
  Observation: ImageNet and CIFAR-10 have a mean file size of 3126 bytes. LibriSpeech and Speech Commands v2 have 8044 bytes.
  Paper quote: Image data were set to BMP format with a
resolution of 32×32, RGB colour, and 24-bit depth..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): A 32×32×3-byte image is 3072 bytes, plus a BMP header of 54 bytes, which gives 3126. A one-second WAV at 8000 Hz and 8-bit depth is 8000 bytes plus a header, which gives 8044. Both values are consistent with the stated formats.
  First assessment: agreement. A 32×32×3-byte image is 3072 bytes, plus a BMP header of 54 bytes, which gives 3126. A one-second WAV at 8000 Hz and 8-bit depth is 8000 bytes plus a header, which gives 8044. Both values are consistent with the stated formats.
  Second assessment: unresolved. There is no relevant element on this page, so the claim cannot be checked against this image.

- **Conflicting assessments**: `paper:p.1`, units (visual audit observation index 25).
  Observation: Abstract states "achieving a low error rate of 0.0011 bits per byte in converting ABC notation to MIDI format."
  Paper quote: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The abstract's 0.0011 bits per byte matches the BPBmidi value for bGPT5 in ABC→MIDI reported in Section 5.3.1 and Table 5. The unit, bits per byte, is the BPB metric.
  First assessment: agreement. The abstract's 0.0011 bits per byte matches the BPBmidi value for bGPT5 in ABC→MIDI reported in Section 5.3.1 and Table 5. The unit, bits per byte, is the BPB metric.
  Second assessment: unresolved. The quoted passage and the Table 5 data are not on this page. The abstract's "0.0011 bits per byte" is consistent with BPB units. However, the page does not show the specific bGPT5/BPBmidi claim, so this comparison cannot be checked here.

- **Conflicting assessments**: `paper:p.1`, units (visual audit observation index 26).
  Observation: Abstract states that bGPT simulates CPU behaviour "with an accuracy exceeding 99.99% in executing various operations."
  Paper quote: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%).
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Table 6 lists bGPT6 at 99.9961%, which exceeds 99.99%. This is consistent with the abstract.
  First assessment: agreement. Table 6 lists bGPT6 at 99.9961%, which exceeds 99.99%. This is consistent with the abstract.
  Second assessment: unresolved. The quoted text and Table 6 appear on later pages that are not shown. Page 1 contains only a general 99.99% accuracy claim, not the per-model figures and units being checked.

- **Conflicting assessments**: `paper:p.1`, captions (visual audit observation index 27).
  Observation: Abstract states that bGPT matches specialized models across text, audio, and images.
  Paper quote: bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The page-1 wording matches the supplied abstract text, so the rendering agrees with the extraction. The CIFAR-10 gap reported later in the paper (88.69% vs 98.13%) qualifies this 'matches' claim. That is a substantive tension in the paper's content, not a rendering discrepancy.
  First assessment: agreement. The page-1 wording matches the supplied abstract text, so the rendering agrees with the extraction. The CIFAR-10 gap reported later in the paper (88.69% vs 98.13%) qualifies this 'matches' claim. That is a substantive tension in the paper's content, not a rendering discrepancy.
  Second assessment: unresolved. The relevant Table 3 caption and its results text are on pages 6 and 7, which are not shown. This page has no captioned element that could be compared with the quote.

- **Conflicting assessments**: `paper:p.6`, captions (visual audit observation index 54).
  Observation: The caption names GPT2-small/AG News, ViT-B/16/CIFAR-10, and AST/Speech Commands v2. It describes bGPT_signal as ImageNet+LibriSpeech and bGPT_mix as ImageNet+LibriSpeech+Wikipedia.
  Paper quote: bGPTsignal
combined the ImageNet and LibriSpeech datasets, while
bGPTmix integrated all three datasets..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The caption's descriptions of the pre-training mixtures match Section 5.2.
  First assessment: agreement. The caption's descriptions of the pre-training mixtures match Section 5.2.
  Second assessment: unresolved. The quoted sentence itself is not on this page, so it cannot be directly checked here. The caption shown is consistent with it, but that is related content, not the quoted text.

- **Conflicting assessments**: `paper:p.16`, captions (visual audit observation index 66).
  Observation: The Piano Roll bullet says a graphical interface is 'as shown in Fig. 1'.
  Paper quote: Piano Roll: A graphical interface in digital audio workstations (as shown in Fig. 1) where notes are displayed and
edited on a grid representing pitch and time..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): Figure 1's caption in the paper describes the bGPT framework: 'The bGPT framework simulates digital systems through native binary data...' It does not describe a piano-roll interface. The cross-reference therefore does not match that caption. Figure 1 may still contain a small piano-roll icon, but this page alone cannot confirm it.
  First assessment: mismatch. Figure 1's caption in the paper describes the bGPT framework: 'The bGPT framework simulates digital systems through native binary data...' It does not describe a piano-roll interface. The cross-reference therefore does not match that caption. Figure 1 may still contain a small piano-roll icon, but this page alone cannot confirm it.
  Second assessment: unresolved. The rendered text matches the quote. Whether Fig. 1 actually depicts a piano roll cannot be judged from this page alone. The paper's extracted Fig. 1 caption describes the bGPT framework, which suggests the cross-reference may be inaccurate, but the figure itself was not inspected here.

- **Conflicting assessments**: `paper:p.16`, captions (visual audit observation index 67).
  Observation: The text says the round-tripped tune was 'demonstrated in Fig, 4' and that its sheet music 'is shown in Fig. 5'.
  Paper quote: Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The page's references to Fig. 4 and Fig. 5 are consistent with the captions of those figures. The 'Fig,' comma is a typographic slip only.
  First assessment: agreement. The page's references to Fig. 4 and Fig. 5 are consistent with the captions of those figures. The 'Fig,' comma is a typographic slip only.
  Second assessment: unresolved. The Figure 5 caption is on a different page (page 15 per extraction), so this image cannot confirm or contradict it.

- **Conflicting assessments**: `paper:p.16`, rendered_formulas (visual audit observation index 68).
  Observation: The ABC block is rendered with X:1, L:1/8, M:3/4, K:D and tune lines that end with '|]'. The repeated sections are written out explicitly.
  Paper quote: One can observe that the ABC sequence and the musical score appear significantly longer than the original due to
the elimination of repeat signs in MIDI, requiring repeated sections to be explicitly written out..
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The rendered block contains no repeat signs, such as '::' or ':|', that appear in the original example. Its header matches the original's L:1/8, M:3/4 and K:D.
  First assessment: agreement. The rendered block contains no repeat signs, such as '::' or ':|', that appear in the original example. Its header matches the original's L:1/8, M:3/4 and K:D.
  Second assessment: unresolved. The text agrees with the quote, and the visible ABC block is consistent with written-out repeats. However, the comparison of length against the original ABC and the scores cannot be verified from this page alone.

- **Conflicting assessments**: `paper:p.14`, units (visual audit observation index 109).
  Observation: The ABC code block shows L:1/8 and M:3/4. The text describes 1/8 as the eighth-note unit length and 3/4 as the meter.
  Paper quote: In this context, 1/8 indicates that each note is an
eighth note.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The header values in the rendered code block match the explanatory text.
  First assessment: agreement. The header values in the rendered code block match the explanatory text.
  Second assessment: mismatch. L:1/8 sets the default unit length only. The visible ABC durations (3, 4, 2, /) and the varied note values in the rendered score contradict the claim that each note is an eighth note. The page itself also says the duration of notes is modified by numbers.

- **Conflicting assessments**: `paper:p.19`, sample_counts (visual audit observation index 114).
  Observation: Table 7 lists 21 instruction rows: HLT, CLR, INC, DEC, SHL, SHR, ROL, ROR, NOT, PUSH, POP, LOADI, SWAP, ADD, SUB, MUL, DIV, AND, OR, XOR, and MOV.
  Paper quote: These states include various instructions, totaling 21 unique
types with 43 variants.
  Reason: The image comparison was not consistently supported by the two assessments; human inspection is required. Proposed reasoning (not validated): The 21 rendered instruction types match the stated count of unique types.
  First assessment: agreement. The 21 rendered instruction types match the stated count of unique types.
  Second assessment: mismatch. The table matches the claim of 21 unique types. However, summing the listed address variants gives 44, not 43. The variant count therefore conflicts with the visible table.

- **Confirmed text-image mismatch (advisory)**: `paper:p.19`, sample_counts (visual audit observation index 115).
  Observation: The Address Variants column shows: HLT has 0. CLR, INC, DEC, SHL, SHR, ROL, ROR, and NOT each have 0, 1. PUSH, POP, and LOADI each have 1. SWAP has 1, 2. ADD, SUB, MUL, DIV, AND, OR, and XOR each have 1, 2, 3. MOV has 2.
  Paper quote: totaling 21 unique
types with 43 variants.
  Reason: Summing the listed variants gives 1 + 8×2 + 3×1 + 2 + 7×3 + 1 = 44. The text states 43 variants. The text does not define a counting convention that would exclude one variant.
  First assessment: mismatch. Summing the listed variants gives 1 + 8×2 + 3×1 + 2 + 7×3 + 1 = 44. The text states 43 variants. The text does not define a counting convention that would exclude one variant.
  Second assessment: mismatch. The type count of 21 agrees with the table. The stated 43 variants differs from the 44 variants enumerated in Table 7.

- **Substantive uncertainty**: `paper:p.18`, rendered_formulas (visual audit observation index 122).
  Observation: Each instruction's effect appears only in the following step's state. At step 1 (IR: MUL J A), J=2; at step 2, J=38 (19×2). At step 2 (IR: DIV I), ACC=146; at step 3, ACC=1. At step 5 (IR: LOADI 86), ACC=246; at step 6, ACC=86. At step 8 (IR: POP H), H=20; at step 9, H=86, although no PUSH appears in the program.
  Paper quote: Instruction Register (IR): Occupies 4 bytes, storing the currently executed instruction..
  Reason: The arithmetic is consistent if each state shows the IR before its effect is applied. That reading sits awkwardly with 'the CPU status post-execution of each instruction'. It is also unclear how POP H yields 86 with no prior PUSH; it may be an unstated stack initialization. The trace is readable, but its intended semantics are ambiguous.



## Artifact evidence reconciliation (supplementary)

Literal checks of explicitly linked shipped evidence, not scientific validation. The independent paper assessment is unchanged.

- **unresolved**: claim-1 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-2 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-3 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-5 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-18 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-4 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-15 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-13 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-6 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-7 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-8 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-10 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-14 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-11 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-9 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-12 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-16 / . No declared result edge resolves.
  Paper: `unresolved`; artifact: `unresolved`; locator: `{}`.
- **unresolved**: claim-20 / . No declared result edge resolves.
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
