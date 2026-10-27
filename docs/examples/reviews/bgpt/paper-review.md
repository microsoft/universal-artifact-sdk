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

The paper presents bGPT, a byte-level next-token prediction model that adapts a hierarchical Transformer architecture from prior work (e.g., MegaByte) and applies it across media modalities and to binary-native tasks. Beyond media classification and cross-modal transfer analyses, it introduces evaluations framed as algorithm simulation (ABC↔MIDI data conversion) and hardware simulation (CPU state modelling on a simplified instruction set). It reports low conditional BPB on conversion and near-perfect byte-wise accuracy on CPU state prediction, along with data-scaling trends.

## Contributions

1. **bGPT: next byte prediction model for digital world simulation.** Introduces bGPT, a model that applies next byte prediction to native binary data to process and simulate the digital world, including media files, algorithms and hardware.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: contested*
2. **Hierarchical patch-based Transformer architecture for byte sequences.** bGPT segments byte sequences into fixed-size patches, using a patch-level decoder to predict patch features and a byte-level decoder to reconstruct bytes, managing computational cost of long byte sequences.
   *Claim support: unresolved · Significance: unassessed · Originality: contested*
3. **Generative and classification training objectives for byte models.** bGPT is trained with next byte prediction for generative modelling and then adapted to classification by pooling patch features and training a classification head.
   *Claim support: unresolved · Significance: unassessed · Originality: contested*
4. **Unified byte-level modelling of text, audio and images.** A single byte model handles text, audio and image generation and classification without modality-specific designs, and exhibits cross-modal knowledge transfer.
   *Claim support: unresolved · Significance: unassessed · Originality: contested*
5. **Algorithm and hardware simulation via byte modelling.** Applies byte models to data conversion between ABC notation and MIDI and to CPU state modelling, showing scalability with data and signs of emergent abilities.
   *Claim support (inferred links): contested · Significance: supported · Originality: unresolved*
6. **CPU States dataset.** Introduces a 2.1-million-instance dataset of memory blocks of machine instructions paired with sequences of simplified CPU register states for modelling CPU behaviour.
   *Claim support: unresolved · Significance: supported · Originality: unassessed*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: bGPT: next byte prediction model for digital world simulation

**Claim support (inferred links): contested**
- Linked claims (inferred by the reviewer, not declared by the authors):
  - C1: It has almost flawlessly replicated the process of converting symbolic music data, achieving a low error rate of 0.0011 bits per byte in converting ABC notat…
  - C2: In addition, bGPT demonstrates exceptional capabilities in simulating CPU behaviour, with an accuracy exceeding 99.99% in executing various operations.
- The inferred supporting claims C1 and C2 are reported, but they only partly support the core bGPT contribution. They show learnability of a deterministic converter and a toy CPU, not general digital-world modelling.
- The reported numbers support C1 and C2 within narrow scope. However, the claim of an "emergent ability" rests on a single training run showing a loss jump around epoch 11.
- Sources: paper:chars/31335-34448, paper:chars/34448-36748, paper:chars/36748-38535

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- The authors acknowledge that the architecture is adapted from prior hierarchical models such as MegaByte. Their originality claim therefore rests on the task framing (native binary data and digital-world simulation), not on the model design.
- The main originality claim is bGPT as a byte model for native binary data and digital-world simulation. It is positioned against MalConv and DeepVSA, which the paper describes as narrow-task systems.
- The authors present bGPT as a new model, yet their own text says the hierarchical patch architecture is adapted from prior work and that byte models across modalities already exist. Novelty lies in breadth of evaluation, not the model.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/10851-15278, paper:chars/7775-10479, paper:chars/1238-5446

Paper’s wording: “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”

### Contribution 2: Hierarchical patch-based Transformer architecture for byte sequences

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- The paper's own background credits ByteFormer and MegaByte with multimodal byte modelling and says bGPT adapts MegaByte-style hierarchical patching. Its originality therefore rests on breadth of evaluation and native-binary simulation tasks, not on the architecture.
- The hierarchical patch architecture is presented as a contribution, but the authors themselves say they adapted it from prior work. It should not be credited as novel.
- The authors' stated novelty is the application to native binary data and digital-world simulation, not the architecture, which they say they adapt from prior hierarchical models.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7775-10479, paper:chars/10851-15278, paper:chars/1238-5446, paper:chars/38535-40096

Paper’s wording: “We start by present- ing its hierarchical Transformer framework, which segments byte sequences into patches to manage computational effi- ciency.”

### Contribution 3: Generative and classification training objectives for byte models

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- The training objectives are standard: next-byte NLL followed by a pooled classification head. They should not be credited as novel.
- The training objectives (next-byte NLL followed by a pooled classification head) are standard. The paper does not claim them as new.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/15278-16981

Paper’s wording: “Subsequently, we present the training objectives of bGPT, including generative modelling and classification.”

### Contribution 4: Unified byte-level modelling of text, audio and images

**Claim support: unresolved**
- No claims are linked to this contribution.
- The claim that bGPT "matches specialized models" is overstated for images. On CIFAR-10, bGPT trails ViT by about 9.4 points, and the authors themselves describe this as a noticeable difference.
- 'Matches specialized models' overstates the Table 3 results, especially on CIFAR-10.
- Sources: paper:chars/172-1238, paper:chars/25015-30472

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- The unified multimodal claim overlaps with prior byte models as the paper describes them. The cross-modal transfer analysis is the incremental addition.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7775-10479, paper:chars/25015-30472

Paper’s wording: “bGPT performs comparably to specialized models across di- verse datasets without modality-specific designs”

### Contribution 5: Algorithm and hardware simulation via byte modelling

**Claim support (inferred links): contested**
- Linked claims (inferred by the reviewer, not declared by the authors):
  - C1: It has almost flawlessly replicated the process of converting symbolic music data, achieving a low error rate of 0.0011 bits per byte in converting ABC notat…
  - C2: In addition, bGPT demonstrates exceptional capabilities in simulating CPU behaviour, with an accuracy exceeding 99.99% in executing various operations.
- The CPU and ABC→MIDI results (C1, C2) are reported numerically, but there are no baselines. The CPU task is a simplified, jump-free simulator, so 'exceptional' and 'hardware simulation' framing overreaches.
- The 99.99% CPU accuracy is a byte-wise score on a simplified, jump-free synthetic ISA with no baseline, so it does not establish the 'hardware simulation' claim as stated.
- The near-perfect ABC-to-MIDI (C1) and CPU (C2) results lack baselines and memorization controls. The CPU task is also deliberately simplified, which limits support for claims about 'simulating hardware'.
- Sources: paper:chars/30472-31335, paper:chars/40096-79998, paper:chars/34448-36748, paper:chars/36748-38535

**Significance: supported**
- Framing byte-level next-token prediction as simulation of algorithms and hardware is a distinctive, potentially impactful direction, supported by near-perfect results on two binary-native tasks.
- Framing byte models as simulators of algorithms and hardware (data conversion, CPU state modelling) is an interesting, underexplored task family with potential impact.
- Sources: paper:chars/1238-5446, paper:chars/34448-36748, paper:chars/31335-34448

**Originality: unresolved**
- The authors position data conversion and CPU simulation as underexplored tasks without prior baselines. This is the paper's most distinctive application.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/30472-31335, paper:chars/1238-5446

Paper’s wording: “excels in data conversion and CPU state modelling, demonstrating its potential for simulating various algorithms and hardware.”

### Contribution 6: CPU States dataset

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: supported**
- The CPU States dataset is a new, simple, controllable benchmark. Its utility is limited by the absence of control flow.
- Sources: paper:chars/18456-21674, paper:chars/40096-79998

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “For CPU state modelling, we introduce the CPU States dataset (with 2.1 million instances), offering a simplified representation of CPU behaviour for ease of data collec- tion and evaluation.”

<details><summary>What the authors say is original (3 statements)</summary>

Authors' stated position:
- [claims, builds on] “Inspired by the success of next token prediction in natural lan- guage processing, we introduce bGPT, a model with next byte prediction to simulate the digi- tal world. bGPT matches specialized models in performance across various modalities, including text, audio, and images, and offers new possibil- ities for predicting, simulating, and diagnosing algorithm or hardware behaviour.”
- [claims; positioned against Raff et al., 2018, Guo et al., 2019] “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”
- [claims, builds on] “Conclusions In this paper, we present bGPT as a versatile simulator for the digital world, extending deep learning to binary data processing via next byte prediction.”

</details>


## Reasons to accept

1. **Framing byte-level next-token prediction as simulation of algorithms and hardware is a distinctive, potentially impactful direction, supported by near-perfect results on two binary-native tasks.**
   The data-conversion and CPU tasks extend byte models beyond media modelling, which the paper says prior work treated narrowly.
   Evidence status: inference.
   Reasoning: The paper evaluates byte models on tasks that are defined at the byte level, not only on media. High reported accuracy on these tasks suggests the direction is viable and could interest the community.
   Source `paper:chars/1238-5446`: underexplored tasks intrinsic to binary-native operations,
including data conversion and CPU state modelling, which
represent algorithm and hardware simulation, respectively.
   Source `paper:chars/34448-36748`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%)

2. **The authors acknowledge that the architecture is adapted from prior hierarchical models such as MegaByte. Their originality claim therefore rests on the task framing (native binary data and digital-world simulation), not on the model design.**
   Framing byte models as simulators of conversion algorithms and CPU execution is a fresh empirical direction.
   Evidence status: inference.
   Reasoning: The first quote shows the architecture is adapted from cited prior work. The second places the claimed gap in the application scope. Together they indicate the novelty is the problem framing plus the evaluations on algorithm and hardware simulation. The paper reports MegaByte as tested on long byte sequences across modalities; I have not verified that cited work independently.
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture
   Source `paper:chars/7775-10479`: Despite progress, current research often neglects native bi-
nary data, focusing on narrow tasks and overlooking the
broader potential of byte models in digital world simulation.

3. **Framing byte models as simulators of algorithms and hardware (data conversion, CPU state modelling) is an interesting, underexplored task family with potential impact.**
   Value lies mainly in the task framing and the scaling evidence, not the architecture.
   Evidence status: inference.
   Reasoning: The paper defines a new evaluation setting beyond media modelling and reports clear data-scaling trends on it; this task framing is the most distinctive part of the work and could seed follow-up research.
   Source `paper:chars/1238-5446`: underexplored tasks intrinsic to binary-native operations,
including data conversion and CPU state modelling, which
represent algorithm and hardware simulation, respectively.
   Source `paper:chars/31335-34448`: BPB for both ABC to
MIDI and MIDI to ABC conversions decrease significantly.

4. **The authors position data conversion and CPU simulation as underexplored tasks without prior baselines. This is the paper's most distinctive application.**
   Likely to attract follow-up work in ML for systems, security, and program analysis.
   Evidence status: inference.
   Reasoning: If no comparable learned simulators exist, as the authors assert, this opens a new evaluation direction. Whether neural program-execution work exists that the paper does not cite remains unresolved and should be checked by the reviewer.
   Source `paper:chars/1238-5446`: underexplored tasks intrinsic to binary-native operations,
including data conversion and CPU state modelling
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets

## Originality

The authors themselves credit ByteFormer and MegaByte with byte-level modelling across modalities and describe bGPT's architecture as adapted from prior hierarchical models, so the architectural contribution is modest. The originality claim rests mainly on the task framing: treating byte models as simulators of conversion algorithms and CPU execution, which the paper positions as underexplored and without established baselines. That framing appears distinctive, though whether related neural program-execution work exists that is not cited remains unchecked and would sharpen the positioning. The unified multimodal aspect largely overlaps with the cited prior work; the cross-modal transfer analysis is the incremental addition there. The introduction's 'paradigm shift' language implies broader methodological novelty than the related-work section concedes.

## Likely impact

The binary-native simulation framing could seed follow-up work in ML for systems, program analysis, and security, and the data-conversion and CPU tasks may serve as starting points for new evaluation settings. Influence is likely limited by the current scope: the CPU task excludes jumps and control flow, both simulation tasks are acknowledged by the authors as not excessively complicated, train and test come from the same generator, and no baselines are provided. Without these, others may find it hard to use the reported numbers as reference points. On media tasks, the 'matches specialized models' framing is weakened by the reported CIFAR-10 gap (88.69% vs. 98.13% for ViT, with non-controlled comparison settings).

## Decision-critical concerns

1. **The CPU and ABC→MIDI results (C1, C2) are reported numerically, but there are no baselines. The CPU task is a simplified, jump-free simulator, so 'exceptional' and 'hardware simulation' framing overreaches.**
   The 99.99% figure is byte-wise, not per-program correctness.
   Evidence status: inference.
   Reasoning: Without a simple baseline, near-perfect numbers cannot be interpreted. Possible baselines include copying the previous state, or a standard byte-level Transformer without patching. Byte-wise accuracy over states where most register bytes remain unchanged may inflate accuracy. Excluding jumps also removes control flow, which narrows what is being simulated.
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets,
we investigated its performance across different data scales
   Source `paper:chars/40096-79998`: complex instructions like jump commands were deliberately excluded
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   - **Why this affects the decision:** The headline abstract claims rest on these numbers.
   - **Actionable revision:** Report three things: (1) a copy-previous-state baseline, (2) per-instruction and per-program exact-match accuracy, and (3) accuracy broken down by instruction type. Also scope the abstract claims to the simplified, jump-free CPU.
   - **What would resolve it:** Exact-match accuracy that clearly exceeds trivial baselines, plus revised claim wording.

2. **The paper's own background credits ByteFormer and MegaByte with multimodal byte modelling and says bGPT adapts MegaByte-style hierarchical patching. Its originality therefore rests on breadth of evaluation and native-binary simulation tasks, not on the architecture.**
   The primary novelty lies in the application and evaluation (native binary simulation), not in the model.
   Evidence status: inference.
   Reasoning: The authors report that MegaByte and ByteFormer already model bytes across modalities, and that bGPT's architecture is adapted from prior hierarchical work. That leaves the native-binary and simulation focus as the stated differentiator. The introduction and impact statement ('paradigm shift', 'pushing the boundaries') imply broader methodological novelty than the related-work section concedes. In the inspected results, no MegaByte or ByteFormer comparison appears; this is an absence observation over Section 5. The cited works' content is author-reported and has not been independently verified.
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
nary data, focusing on narrow tasks and overlooking the
broader potential of byte models in digital world simulation.
   Source `paper:chars/1238-5446`: training models for next byte predic-
tion can potentially lead to a paradigm shift in deep learning
   Source `paper:chars/38535-40096`: pushing
the boundaries of deep learning into the realm of native
binary data.
   - **Why this affects the decision:** Originality is central to the assessment. If bGPT is essentially MegaByte applied to new tasks, the paper should be weighed as an empirical study.
   - **Actionable revision:** State explicitly how bGPT's architecture differs from MegaByte, if at all. Reframe the abstract and introduction as an empirical study of byte models on native-binary tasks. Ideally, add a MegaByte or ByteFormer comparison on at least one media task.
   - **What would resolve it:** A paragraph distinguishing bGPT from MegaByte, or conceding equivalence, together with a revised contribution framing.

3. **The 99.99% CPU accuracy is a byte-wise score on a simplified, jump-free synthetic ISA with no baseline, so it does not establish the 'hardware simulation' claim as stated.**
   The 'beyond memorization' argument relies on the size of the scenario space, not on a held-out analysis.
   Evidence status: inference.
   Reasoning: In each 16-byte state, many bytes either persist unchanged or follow trivially, such as the PC increment. Byte-wise accuracy can therefore be very high even if many instructions are executed wrongly. The paper reports no copy-previous-state baseline and no per-state or per-program exact-match score. It also gives no breakdown by opcode.
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   Source `paper:chars/40096-79998`: complex instructions like jump commands were deliberately excluded
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets,
we investigated its performance across different data scales
   - **Why this affects the decision:** The 99.99% figure is a headline result in the abstract; if a trivial baseline scores similarly, the hardware-simulation claim loses most of its support.
   - **Actionable revision:** Report: (1) a copy-previous-state baseline; (2) per-state and per-program exact-match accuracy; (3) accuracy by opcode and by program length; (4) the train/eval overlap of programs.
   - **What would resolve it:** Exact-match accuracy that stays high and clearly exceeds the copy baseline, including on arithmetic opcodes such as MUL and DIV.

4. **The near-perfect ABC-to-MIDI (C1) and CPU (C2) results lack baselines and memorization controls. The CPU task is also deliberately simplified, which limits support for claims about 'simulating hardware'.**
   The headline numbers lack the context needed to interpret them.
   Evidence status: inference.
   Reasoning: Byte-wise accuracy over 16-byte states may be inflated, because many register bytes are unchanged at each step, so a copy-previous-state baseline could score highly. The authors argue against memorization only from combinatorics, not from a held-out overlap analysis. The ISA is simplified, so the abstract's 'exceptional capabilities in simulating CPU behaviour' outruns the evidence.
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets,
we investigated its performance across different data scales
   Source `paper:chars/34448-36748`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%), suggesting an efficiency beyond sim-
ple memorization
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   Source `paper:chars/36748-38535`: our
CPU state modelling experiments focused solely on simpli-
fied CPUs, omitting the use of real modern CPUs
   - **Why this affects the decision:** These results underpin the central 'digital world simulator' claim.
   - **Actionable revision:** Report a copy-previous-state baseline, per-state and per-program exact-match accuracy, accuracy by program length, and train/test sequence overlap. Scope the abstract claims to a simplified ISA.
   - **What would resolve it:** Exact-match accuracy that substantially exceeds a trivial copy baseline.

## Questions for the authors

1. **What is the per-state exact-match accuracy, and how does it compare to a no-state-change baseline?**
   If a no-change baseline reaches roughly 90% byte-wise accuracy, the 99.99% figure supports much less than claimed.
   Evidence status: inference.
   Reasoning: Byte-wise accuracy can be high even for a model that only copies the previous state.
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   - **Why the answer matters:** Determines how strongly the central result supports the claims.
   - **Requested response:** Report the no-change baseline and exact-match accuracy.
   - **Answer that would resolve it:** A large margin over the no-change baseline would confirm the CPU-simulation claim.

2. **Is the 0.0011 BPB for ABC→MIDI explained by MIDI bytes that are near-deterministic given the ABC?**
   Free-running generation accuracy would show whether the BPB figure supports 'almost flawlessly replicated'.
   Evidence status: inference.
   Reasoning: BPB is computed under teacher forcing, so it may not reflect whether the model can generate a correct MIDI file from scratch. There is also no comparison against simple predictors that exploit the conversion's structure.
   Source `paper:chars/31335-34448`: BPBmidi evaluates data conversion, considering the com-
plete ABC byte sequence is given.
   - **Why the answer matters:** If free-running conversion often fails, the 'almost flawlessly replicated' claim is overstated.
   - **Requested response:** Report the exact-match or valid-MIDI rate for greedy end-to-end conversion.
   - **Answer that would resolve it:** A high exact-match rate would confirm C1.

3. **Does the CPU States evaluation measure generalization or largely in-distribution reproduction? The dataset has a restricted instruction set with no jumps.**
   The dataset's value as a contribution depends on how well it probes generalization.
   Evidence status: observation.
   Reasoning: Train and test come from the same random generator, so the evaluation is in-distribution only.
   Source `paper:chars/18456-21674`: Instances are generated by execut-
ing random sequences of 1 to 256 instructions and capturing
the state after each execution.
   - **Why the answer matters:** Strong length or out-of-distribution generalization would substantially raise the significance of both the dataset and the simulation claims.
   - **Requested response:** Report accuracy on programs longer than those seen in training, and on held-out instruction combinations.
   - **Answer that would resolve it:** Accuracy broken down by program length and on held-out combinations.

## Decision synthesis

The strongest case for the paper is the distinctive framing of byte-level prediction as algorithm and hardware simulation, supported by very strong reported numbers (0.0011 BPB on ABC→MIDI; 99.97%/99.99% byte-wise CPU accuracy) and clear data-scaling trends on these new tasks. The most decision-relevant concern is that these headline numbers are hard to interpret. No baselines are reported, such as a copy-previous-state predictor or a non-patched byte Transformer. CPU accuracy is byte-wise over 16-byte states in which many bytes may be unchanged or trivially predictable, and no per-state or per-program exact match or per-opcode breakdown is given. The ISA omits jumps, and the argument against memorization relies on combinatorics rather than a held-out overlap analysis. Similarly, conversion BPB is computed under teacher forcing, and free-running generation correctness is not shown. Answers to these questions could change the assessment substantially: per-state exact match versus a no-change baseline, free-running conversion accuracy, and evidence of generalization beyond the training generator's distribution. Non-blocking improvements include softening the 'matches specialized models' and 'emergent ability' wording (the latter rests on one training run), recentring the multimodal contribution on the transfer findings, and reporting variance for small differences such as the 0.6-point accuracy gap between bGPT_image and bGPT_libri in Table 4, whose significance is currently unassessed.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The paper reports a negative result openly, and its appendices keep domain background out of the main argument.

**Writing-quality issues**

1. **The abstract headlines its results with metrics a non-specialist cannot interpret, and its first result is ambiguous about what was measured.**
   Calling a loss an "error rate" can mislead readers about what the number measures.
   - **Suggested revision:** In the abstract, describe 0.0011 as a prediction loss (bits per byte) on the MIDI output given the ABC input. Add one plain sentence saying what this means for conversion quality, such as the share of output bytes that are exactly correct.

2. **Several places assert understanding in words rather than showing it.**
   The prose claims more than the evidence it presents demonstrates.
   - **Suggested revision:** Replace these phrases with the specific observed behaviour, such as byte-level accuracy on held-out programs averaging 128 instructions.

3. **The instruction-variant count stated in the text (43) does not match the variants enumerated in Table 7.**
   Table 7, as transcribed, appears to enumerate 44 address variants across 21 instructions, but Section 4.2 states 43. This is a small internal inconsistency in the description of the instruction-set task.
   - **Suggested revision:** Reconcile the variant count in Section 4.2 with Table 7. If any derived quantity depends on the variant count, such as the 'over 516 million' scenario figure, recheck it as well.

4. **Table 6 reports results to four decimal places, which reads like log output.**
   The extra precision makes the key result harder to see.
   - **Suggested revision:** Round the reported values and state the takeaway in plain words, for example: "accuracy rises from about 27% to near-perfect between 10^4 and 10^5 training examples."

## Additional improvements (non-blocking)

1. **The unified multimodal claim overlaps with prior byte models as the paper describes them. The cross-modal transfer analysis is the incremental addition.**
   Reframe this contribution around the transfer findings.
   Evidence status: inference.
   Reasoning: The authors attribute unified byte modelling to prior work, which leaves the transfer study as the new element.
   Source `paper:chars/7775-10479`: allowing models to work with binary
representations of text, images, and diverse data types in
a universal framework.
   Source `paper:chars/25015-30472`: Positive trans-
fer occurs when models pre-trained on one data type
   - **Suggested revision:** Position the transfer analysis as the contribution.

2. **'Matches specialized models' overstates the Table 3 results, especially on CIFAR-10.**
   The ViT and AST numbers are taken from the original studies, so the comparison settings are not controlled.
   Evidence status: observation.
   Reasoning: The paper's own CIFAR-10 gap of nearly 10 points contradicts the 'matches' wording in the abstract.
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities
   Source `paper:chars/25015-30472`: a noticeable difference
is seen with bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%.
   - **Suggested revision:** Revise the abstract wording, for example: 'approaches specialized models on text/audio, lags on images'.

3. **The inferred supporting claims C1 and C2 are reported, but they only partly support the core bGPT contribution. They show learnability of a deterministic converter and a toy CPU, not general digital-world modelling.**
   Scope the general framing to the evidence.
   Evidence status: inference.
   Reasoning: The authors concede that the tasks are simple. Low conditional BPB measures likelihood, not verified functional conversion.
   Source `paper:chars/31335-34448`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   Source `paper:chars/34448-36748`: While
the tasks utilized for demonstration in this study were not
excessively complicated
   - **Suggested revision:** Report the exact-match rate of generated MIDI files against the reference converter output.

4. **The reported numbers support C1 and C2 within narrow scope. However, the claim of an "emergent ability" rests on a single training run showing a loss jump around epoch 11.**
   C1 and C2 are supported by Tables 5 and 6.
   Evidence status: observation.
   Reasoning: One run of a training curve does not establish emergence. The authors themselves limit the scope to simplified CPUs.
   Source `paper:chars/34448-36748`: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b, indicating
an emergent ability in CPU state modelling.
   Source `paper:chars/36748-38535`: our
CPU state modelling experiments focused solely on simpli-
fied CPUs
   - **Suggested revision:** Report results over multiple seeds, or soften the emergence language.

5. **Table 4 shows nearly identical BPB for bGPT_image and bGPT_libri, with a 0.6-point accuracy gap. Its robustness to run-to-run variance is not shown in the supplied record.**
   The rendered values match the text. The open point is whether the small accuracy difference is meaningful, not whether it was transcribed correctly.
   Evidence status: inference.
   Reasoning: The confirmed Table 4 values are BPB 0.3899 with Acc 84.66 for bGPT_image, and BPB 0.3900 with Acc 85.26 for bGPT_libri. The BPB difference is 0.0001 and the accuracy difference is 0.60 points. Bold marks only the per-column best value. Without seeds or confidence intervals, any interpretation that rests on the libri-over-image accuracy ordering depends on whether a 0.6-point gap exceeds normal variation.
   Source `review-record:visual/26`: Table 4 shows BPB/accuracy values of 0.4052/80.74 for random, 0.3899/84.66 for image, and 0.3900/85.26 for libri. The value 0.3899 and the libri accuracy 85.26 are in bold.
   Source `paper:chars/29311-29356`: bGPTimage 0.3899 84.66
bGPTlibri 0.3900 85.26
   - **Suggested revision:** If the paper draws conclusions from the libri versus image accuracy ordering, report variance across seeds or a significance test for the Table 4 accuracy values.

6. **The sharp loss drop of bGPT^5 near epoch 11 in Fig. 3b is presented as a significant improvement. It is unclear whether this is reproducible or specific to one run.**
   Only one curve per scale is shown.
   Evidence status: inference.
   Reasoning: Per record visual/23, the bGPT^5 train and eval curves stay flat near about 0.57 and then drop abruptly to about 0.4 between epochs 11 and 12. The paper highlights this drop. A discontinuous change of this kind in a single plotted curve could reflect a learning phase transition or optimization stochasticity. The figure alone cannot distinguish the two, so any interpretation of the timing needs support from repeated runs.
   Source `review-record:visual/23`: The x-axis is labelled Epoch and runs from 0 to 32. The y-axis is labelled Loss with ticks from 0.4 to 1.6. The legend lists bGPT4/5/6 Train and Eval. One orange curve drops sharply around epoch 11-12.
   Source `paper:chars/35331-35430`: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b
   - **Suggested revision:** Report whether the epoch-11 transition recurs across seeds. Alternatively, qualify the interpretation as an observation from a single run.

7. **Table 6 shows identical BPB (0.0969) for bGPT^5 and bGPT^6. This limits what the CPU-modeling results say about benefits from scaling data from 10^5 to 10^6.**
   Equal BPB across a 10x data increase means the CPU scaling evidence rests on a single effective step (bGPT^4 to bGPT^5).
   Evidence status: inference.
   Reasoning: Record visual/25 reads Table 6 as bGPT^4 0.6924/27.2404%, bGPT^5 0.0969/99.9702%, bGPT^6 0.0969/99.9961%. Record visual/21 confirms the 10^4 to 10^6 scale mapping. Together they show that the last tenfold increase in data leaves BPB unchanged to four decimals and moves accuracy by about 0.03 points. The 'diminishing returns' wording is consistent with this. However, the visible evidence supports a scaling benefit mainly from 10^4 to 10^5, not across the full range. The text also reports 99.9961 as 99.99%, which is truncation rather than rounding.
   Source `review-record:visual/25`: Table 6 shows bGPT4 at 0.6924 BPB and 27.2404% accuracy, bGPT5 at 0.0969 and 99.9702%, and bGPT6 at 0.0969 and 99.9961%.
   Source `review-record:visual/21`: Rendered text shows data scales 10^3 (bGPT^3), 10^4 (bGPT^4), 10^5 (bGPT^5), 10^6 (bGPT^6) with superscripts; data conversion uses 10^3 to 10^5 and CPU uses 10^4 to 10^6.
   Source `paper:chars/35044-35117`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%)
   Source `paper:chars/30886-30975`: utilizing data scales ranging from 103
(bGPT3), 104 (bGPT4), 105 (bGPT5), to 106 (bGPT6).
   - **Suggested revision:** State explicitly that CPU-modeling gains saturate at 10^5. Report BPB with more precision or with variance so the bGPT^5/bGPT^6 comparison is interpretable. Use consistent rounding in the text.

8. **The BPB_midi of 0.0011 for ABC→MIDI is described as 'impressively low'. The paper should contextualize this against the near-deterministic nature of the conversion.**
   The asymmetry between directions in Table 5 suggests that conversion determinism shapes the numbers.
   Evidence status: inference.
   Reasoning: Records visual/24 and visual/9 confirm that Table 5 and the text report 0.0011 BPB_midi for bGPT^5. The reverse direction (MIDI→ABC) in the same table is notably higher. An extremely low BPB on the target side of a rule-based conversion may mainly reflect learning a fixed mapping. Without a reference point, such as a deterministic converter's output entropy, the figure's significance for general byte-level simulation is hard to judge.
   Source `review-record:visual/24`: Table 5 lists bGPT5 with an ABC→MIDI BPB_midi value of 0.0011. The other values are 1.4319/0.2381/0.2796/1.1227, 0.9789/0.0202/0.1751/0.1763, and 0.7362/0.0011/0.1341/0.0789.
   Source `review-record:visual/9`: Page renders BPB_abc and BPB_midi with subscripts and bGPT^5, bGPT^3 with superscripts denoting data scale.
   Source `paper:chars/33656-33745`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   Source `paper:chars/33656-33745`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   - **Suggested revision:** Discuss conversion determinism. Add an exact-match or reconstruction rate for ABC→MIDI to accompany BPB.

9. **The hierarchical patch architecture is presented as a contribution, but the authors themselves say they adapted it from prior work. It should not be credited as novel.**
   The paper does not state how bGPT differs from MegaByte, for example in the byte-level decoder or the one-hot linear patch embedding.
   Evidence status: observation.
   Reasoning: The authors explicitly describe the architecture as an adaptation.
   Source `paper:chars/10851-15278`: bGPT adapts a hierarchical Trans-
former architecture
   - **Suggested revision:** State the concrete architectural differences from MegaByte, or label the architecture as reused.

10. **The emergent-ability argument for CPU modelling rests on a claimed linear, smooth BPB that Table 6 does not show; bGPT5 and bGPT6 have identical BPB.**
   The emergence claim needs more data scales or model sizes, or should be softened.
   Evidence status: inference.
   Reasoning: The paper describes a sudden jump around epoch 11, which is the evidence it uses for emergence. A sudden jump is not consistent with calling BPB 'linear and smooth', so this rebuttal of the metric-artifact critique is not coherent as written.
   Source `paper:chars/34448-36748`: the linear and
smooth nature of BPB counters this
   Source `paper:chars/31335-34448`: bGPT5 0.0969 99.9702
bGPT6 0.0969 99.9961
   - **Suggested revision:** Soften the emergence wording, or add evidence from more scales.

## Evidence to examine (advisory)

### Rendered formulas: Rendered as 𝒫 = [P_1, P_2, ..., P_N], (1); below it N = ⌈T/S⌉ and P_i = [b_{(i−1)S+1}, ..., b_{iS}] for 1 ≤ i ≤ N, with T mod S ≠ 0.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered patch definition and ceiling count match the extracted text. The ̸= extraction artifact is rendered as ≠.

- Source: `review-record:visual/0`
- Source: `paper:chars/11776-11885`
- Source: `paper:p.3`
- Source: `review-output:visual/page-3.png`

### Rendered formulas: P_N = [b_{(N−1)S+1}, ..., b_T, e,...,e] with an underbrace labeled S−(T mod S).

Scope: paper-only; analysis: visual; evidence status: inference.
The underbrace padding count matches the text. The garbled '| {z }' is extraction noise from the underbrace.

- Source: `review-record:visual/1`
- Source: `paper:chars/12865-12935`
- Source: `paper:p.3`
- Source: `review-output:visual/page-3.png`

### Rendered formulas: E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N, (3). The following text describes W_linear with shape (S × 257, H).

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered equation is consistent with the text. The 257D one-hot encoding (256 byte values + <eop>) is consistent with the S × 257 shape.

- Source: `review-record:visual/2`
- Source: `paper:chars/13892-13934`
- Source: `paper:p.3`
- Source: `review-output:visual/page-3.png`

### Rendered formulas: Ê_i = Decoder_patch(ℰ_{<i} ⊕ 𝒳_{<i}), (4).

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered equation matches the extracted text, apart from calligraphic glyphs that were lost in extraction.

- Source: `review-record:visual/3`
- Source: `paper:chars/14439-14473`
- Source: `paper:p.3`
- Source: `review-output:visual/page-3.png`

### Captions: The diagram shows Byte Patches feeding a Linear Projection Layer, then Patch Embeds & Position Embeds (0, 1, 2, N), then a Patch-Level Transformer Decoder, then a Byte-Level Transformer Decoder producing Output Bytes. The <eop> tokens pad the patches.

Scope: paper-only; analysis: visual; evidence status: inference.
The figure's components match both the caption and the three-component description in the text.

- Source: `review-record:visual/4`
- Source: `paper:chars/12668-12863`
- Source: `paper:p.3`
- Source: `review-output:visual/page-3.png`

### Units: The page shows a patch matrix of S × 257 and a 257D one-hot vector covering all 256 byte values plus an <eop> token.

Scope: paper-only; analysis: visual; evidence status: inference.
The dimension 257 = 256 + 1 is internally consistent across the rendered page and the text.

- Source: `review-record:visual/8`
- Source: `paper:chars/13514-13611`
- Source: `paper:p.3`
- Source: `review-output:visual/page-3.png`

### Rendered formulas: Page renders BPB_abc and BPB_midi with subscripts and bGPT^5, bGPT^3 with superscripts denoting data scale.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered sub/superscripts match the extracted text and Section 5.3 notation (10^3 to 10^6 scale models); extraction flattened them.

- Source: `review-record:visual/9`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.8`
- Source: `review-output:visual/page-8.png`

### Reviewer coverage limitation: units (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/10`
- Source: `paper:chars/32550-32583`
- Source: `paper:p.8`
- Source: `review-output:visual/page-8.png`

### Reviewer coverage limitation: sample counts (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/11`
- Source: `paper:chars/32719-32760`
- Source: `paper:p.8`
- Source: `review-output:visual/page-8.png`

### Reviewer coverage limitation: captions (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/12`
- Source: `paper:chars/32719-32760`
- Source: `paper:p.8`
- Source: `review-output:visual/page-8.png`

### Reviewer coverage limitation: axes (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/13`
- Source: `paper:chars/35331-35430`
- Source: `paper:p.8`
- Source: `review-output:visual/page-8.png`

### Reviewer coverage limitation: units (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/15`
- Source: `paper:chars/829-921`
- Source: `paper:p.1`
- Source: `review-output:visual/page-1.png`

### Sample counts: Rendered text shows data scales 10^3 (bGPT^3), 10^4 (bGPT^4), 10^5 (bGPT^5), 10^6 (bGPT^6) with superscripts; data conversion uses 10^3 to 10^5 and CPU uses 10^4 to 10^6.

Scope: paper-only; analysis: visual; evidence status: inference.
The extracted '103' and similar values are flattened superscripts; the rendered page shows 10^3 through 10^6, consistent with the paper text.

- Source: `review-record:visual/21`
- Source: `paper:chars/30886-30975`
- Source: `paper:p.7`
- Source: `review-output:visual/page-7.png`

### Axes: The x-axis is labelled Epoch with ticks from 0 to 32 in steps of 4. The y-axis is labelled Loss with ticks from 0.2 to 1.2. The legend lists bGPT3/4/5 Train and Eval.

Scope: paper-only; analysis: visual; evidence status: inference.
The plotted scales match the data-conversion scales of 10^3 to 10^5 and the 32 epochs listed in Table 2.

- Source: `review-record:visual/22`
- Source: `paper:chars/31908-31927`
- Source: `paper:p.7`
- Source: `review-output:visual/page-7.png`

### Axes: The x-axis is labelled Epoch and runs from 0 to 32. The y-axis is labelled Loss with ticks from 0.4 to 1.6. The legend lists bGPT4/5/6 Train and Eval. One orange curve drops sharply around epoch 11-12.

Scope: paper-only; analysis: visual; evidence status: inference.
The legend matches the CPU scales of 10^4 to 10^6. The visible drop in an orange curve near epoch 11-12 is consistent with the text, assuming orange denotes bGPT5 as the legend colours indicate.

- Source: `review-record:visual/23`
- Source: `paper:chars/35331-35430`
- Source: `paper:p.7`
- Source: `review-output:visual/page-7.png`

### Captions: Table 5 lists bGPT5 with an ABC→MIDI BPB_midi value of 0.0011. The other values are 1.4319/0.2381/0.2796/1.1227, 0.9789/0.0202/0.1751/0.1763, and 0.7362/0.0011/0.1341/0.0789.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered values match both the extracted table and the text.

- Source: `review-record:visual/24`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.7`
- Source: `review-output:visual/page-7.png`

### Captions: Table 6 shows bGPT4 at 0.6924 BPB and 27.2404% accuracy, bGPT5 at 0.0969 and 99.9702%, and bGPT6 at 0.0969 and 99.9961%.

Scope: paper-only; analysis: visual; evidence status: inference.
The rounded accuracies in the text match the table. The identical BPB values for bGPT5 and bGPT6 are consistent with the stated 'diminishing returns'.

- Source: `review-record:visual/25`
- Source: `paper:chars/35044-35117`
- Source: `paper:p.7`
- Source: `review-output:visual/page-7.png`

### Captions: Table 4 shows BPB/accuracy values of 0.4052/80.74 for random, 0.3899/84.66 for image, and 0.3900/85.26 for libri. The value 0.3899 and the libri accuracy 85.26 are in bold.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered values match the text's claims that the BPB values are closely matched and that libri has higher accuracy.

- Source: `review-record:visual/26`
- Source: `paper:chars/29311-29356`
- Source: `paper:p.7`
- Source: `review-output:visual/page-7.png`

### Units: The table headers show BPB and Acc (%), and Table 5 uses BPB_abc and BPB_midi subscripts.

Scope: paper-only; analysis: visual; evidence status: inference.
The units used in the tables are consistent with the metric definitions in the text.

- Source: `review-record:visual/27`
- Source: `paper:chars/32923-33012`
- Source: `paper:p.7`
- Source: `review-output:visual/page-7.png`

### Captions: Figure 1 shows .wav, .bmp, .mid, .abc and .bin inputs feeding a central bGPT block. The outputs are a waveform, a 'Cat' label, sheet music, and CPU chip icons labelled 0, 1, 2, 3, ..., N. The rendered caption reads 'The bGPT framework simulates digital systems through native binary data, and integrates diverse data types into a single model, treating everything as a byte sequence.'

Scope: paper-only; analysis: visual; evidence status: inference.
The figure shows several data types (audio, image, MIDI, ABC, binary) entering one model, and CPU state icons labelled 0 to N represent simulated digital systems. The rendered caption text matches the extracted text.

- Source: `review-record:visual/28`
- Source: `paper:chars/4825-5099`
- Source: `paper:p.2`
- Source: `review-output:visual/page-2.png`

### Sample counts: Table 1 row 'CPU States (proposed)' shows Total Files (Million) 2.1; body text says the CPU States dataset has 2.1 million instances.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered table count matches the text count of 2.1 million.

- Source: `review-record:visual/34`
- Source: `paper:chars/20705-20794`
- Source: `paper:p.5`
- Source: `review-output:visual/page-5.png`

### Units: The column headers read 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)', and 'GPU hours per Epoch'. The caption describes file counts in millions, dataset sizes in gigabytes, average file sizes in bytes, and GPU hours per epoch.

Scope: paper-only; analysis: visual; evidence status: inference.
The header units are consistent with the caption.

- Source: `review-record:visual/35`
- Source: `paper:chars/19668-19816`
- Source: `paper:p.5`
- Source: `review-output:visual/page-5.png`

### Budgets: Table 2 lists Patch Size 16/16, Patch Length 512/512, Hidden Size 768, Epochs 32, Learning Rate 1e-04/1e-05, and Batch Size 16/1. Section 5.1 states a patch size of 16 and a sequence length of 512, with support for files up to 8KB.

Scope: paper-only; analysis: visual; evidence status: inference.
16 × 512 = 8192 bytes, which equals 8KB. The rendered table values match the text.

- Source: `review-record:visual/36`
- Source: `paper:chars/21970-22056`
- Source: `paper:p.5`
- Source: `review-output:visual/page-5.png`

### Reviewer coverage limitation: units (paper:p.5)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/37`
- Source: `paper:chars/18196-18454`
- Source: `paper:p.5`
- Source: `review-output:visual/page-5.png`

### Captions: The Table 1 caption references NVIDIA V100 GPU hours. The table includes a 'GPU hours per Epoch' column with values such as 107, 2.1, and 18.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption content matches the rendered columns.

- Source: `review-record:visual/38`
- Source: `paper:chars/19554-19667`
- Source: `paper:p.5`
- Source: `review-output:visual/page-5.png`

### Rendered formulas: Rendered: b̂_{i,j} = Decoder_byte(Ê_i, b_{i,<j}), 1 ≤ j ≤ S, labelled (5).

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered equation matches the extracted text and the surrounding definitions of b̂_{i,j} and b_{i,<j}.

- Source: `review-record:visual/39`
- Source: `paper:chars/15098-15146`
- Source: `paper:p.4`
- Source: `review-output:visual/page-4.png`

### Rendered formulas: Rendered: L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,b_2,...,b_i;θ), labelled (6).

Scope: paper-only; analysis: visual; evidence status: inference.
The negative sum of log-probabilities over i=1..T−1 for the next byte is consistent with the described next-byte NLL over a length-T sequence.

- Source: `review-record:visual/40`
- Source: `paper:chars/15682-15785`
- Source: `paper:p.4`
- Source: `review-output:visual/page-4.png`

### Rendered formulas: Rendered: L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B;θ), labelled (7).

Scope: paper-only; analysis: visual; evidence status: inference.
The summation bound K and the y_k terms match the stated definitions of a cross-entropy loss over K categories.

- Source: `review-record:visual/41`
- Source: `paper:chars/16706-16893`
- Source: `paper:p.4`
- Source: `review-output:visual/page-4.png`

### Units: Text reads 'WAV format... 8000 Hz sampling rate, mono channel, and 8-bit depth, each trimmed to one-second lengths... BMP format with a resolution of 32×32, RGB colour, and 24-bit depth.'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered units match the text. They are also consistent with the reported mean file sizes (8044 B ≈ 8000 samples × 1 byte plus header; 3126 B ≈ 32×32×3 plus header).

- Source: `review-record:visual/42`
- Source: `paper:chars/18196-18454`
- Source: `paper:p.4`
- Source: `review-output:visual/page-4.png`

### Reviewer coverage limitation: sample counts (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/47`
- Source: `paper:chars/24561-24634`
- Source: `paper:p.6`
- Source: `review-output:visual/page-6.png`

### Reviewer coverage limitation: captions (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/48`
- Source: `paper:chars/24389-24559`
- Source: `paper:p.6`
- Source: `review-output:visual/page-6.png`

### Reviewer coverage limitation: units (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/49`
- Source: `paper:chars/25826-25993`
- Source: `paper:p.6`
- Source: `review-output:visual/page-6.png`

### Reviewer coverage limitation: units (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/50`
- Source: `paper:chars/28554-28594`
- Source: `paper:p.6`
- Source: `review-output:visual/page-6.png`

### Reviewer coverage limitation: rendered formulas (paper:p.6)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/51`
- Source: `paper:chars/24679-24728`
- Source: `paper:p.6`
- Source: `review-output:visual/page-6.png`

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/54`
- Source: `paper:chars/65157-65255`
- Source: `paper:p.16`
- Source: `review-output:visual/page-16.png`

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/55`
- Source: `paper:p.16`
- Source: `review-output:visual/page-16.png`

### Sample counts: The code block has the header X:1, L:1/8, M:3/4, K:D. It is followed by six lines of bars ending 'FD C3 D | F/G/A B3 e | dc d4 |]'.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered ABC example matches the extracted text and the original header from Appendix A.1: 3/4 meter, D key, 1/8 unit length. Its longer, repeat-free form is consistent with the paper's claim that repeated sections are written out.

- Source: `review-record:visual/56`
- Source: `paper:chars/69353-69435`
- Source: `paper:p.16`
- Source: `review-output:visual/page-16.png`

### Reviewer coverage limitation: units (paper:p.17)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/65`
- Source: `paper:chars/21207-21429`
- Source: `paper:p.17`
- Source: `review-output:visual/page-17.png`

### Reviewer coverage limitation: sample counts (paper:p.17)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/66`
- Source: `paper:chars/20730-20794`
- Source: `paper:p.17`
- Source: `review-output:visual/page-17.png`

### Sample counts: Instruction sequences vary 'in length from 1 to 256'; 'over 516 million potential scenarios'.

Scope: paper-only; analysis: visual; evidence status: inference.
Range matches Section 4.2; 516 million also matches Section 5.3.2 ('over 516 million').

- Source: `review-record:visual/67`
- Source: `paper:chars/21430-21510`
- Source: `paper:p.17`
- Source: `review-output:visual/page-17.png`

### Reviewer coverage limitation: sample counts (paper:p.17)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/68`
- Source: `paper:chars/76193-76340`
- Source: `paper:p.17`
- Source: `review-output:visual/page-17.png`

### Captions: Caption reads 'Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.' above a six-system score with key signature of two sharps, 3/4 time and tempo marking quarter note = 120.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered caption matches the text. The two-sharp key signature and 3/4 meter are consistent with the ABC header 'M:3/4' and 'K:D' for the same tune.

- Source: `review-record:visual/71`
- Source: `paper:chars/65157-65255`
- Source: `paper:p.15`
- Source: `review-output:visual/page-15.png`

### Reviewer coverage limitation: sample counts (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/72`
- Source: `paper:chars/70007-70196`
- Source: `paper:p.15`
- Source: `review-output:visual/page-15.png`

### Captions: Sheet music with key signature of two sharps (D major), 3/4 time, chord symbols D, A, C, G/B, Bm, F#m, G; caption reads 'Sheet music example corresponding to the ABC notation of a folk tune in D major.'

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered key signature (two sharps), meter 3/4 and chord labels match the caption and the ABC header K:D, M:3/4 and chord annotations in the listing.

- Source: `review-record:visual/89`
- Source: `paper:chars/62105-62195`
- Source: `paper:p.14`
- Source: `review-output:visual/page-14.png`

### Units: Measure numbers 6, 10, 14 appear at the starts of systems 2–4; repeat signs end system 2 and bracket systems 3–4; first system contains a pickup plus 5 bars.

Scope: paper-only; analysis: visual; evidence status: inference.
Bar structure and repeat markers ('::' and ':|') in the ABC listing are consistent with the rendered measure numbering and repeat barlines.

- Source: `review-record:visual/90`
- Source: `paper:chars/62883-63001`
- Source: `paper:p.14`
- Source: `review-output:visual/page-14.png`

### Reviewer coverage limitation: sample counts (paper:p.19)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/107`
- Source: `paper:chars/21049-21133`
- Source: `paper:p.19`
- Source: `review-output:visual/page-19.png`

### Sample counts: The Address Variants column shows: HLT 0; CLR, INC, DEC, SHL, SHR, ROL, ROR and NOT each 0, 1; PUSH, POP and LOADI each 1; SWAP 1, 2; ADD, SUB, MUL, DIV, AND, OR and XOR each 1, 2, 3; MOV 2.

Scope: paper-only; analysis: visual; evidence status: inference.
Summing the listed variants gives 1 + 7×2 + 3×1 + 2 + 7×3 + 1 = 42, not the 43 stated in the text. No row on the page accounts for an additional variant.

- Source: `review-record:visual/108`
- Source: `paper:chars/21049-21133`
- Source: `paper:p.19`
- Source: `review-output:visual/page-19.png`

### Captions: The caption reads 'Table 7. Defined instruction set and the address variants of different instructions.' The page is numbered 19.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption, the table content and the page location all match the appendix reference.

- Source: `review-record:visual/109`
- Source: `paper:chars/73809-73956`
- Source: `paper:p.19`
- Source: `review-output:visual/page-19.png`

### Sample counts: Page shows states at steps 1 through 10 (step 0 is on page 17), with PC incrementing 1..10 and final IR: HLT.

Scope: paper-only; analysis: visual; evidence status: inference.
Ten executed-instruction states plus the initial state on p.17 match the stated 10-instruction program ending in HLT.

- Source: `review-record:visual/114`
- Source: `paper:chars/75731-75868`
- Source: `paper:p.18`
- Source: `review-output:visual/page-18.png`

### Reviewer coverage limitation: units (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/115`
- Source: `paper:chars/72454-72535`
- Source: `paper:p.18`
- Source: `review-output:visual/page-18.png`

### Reviewer coverage limitation: captions (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/116`
- Source: `paper:chars/72539-72627`
- Source: `paper:p.18`
- Source: `review-output:visual/page-18.png`

### Reviewer coverage limitation: rendered formulas (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/117`
- Source: `paper:chars/79937-79994`
- Source: `paper:p.18`
- Source: `review-output:visual/page-18.png`

## Direct visual evidence (advisory)

- **agreement**, rendered page 3, rendered formulas: Rendered as 𝒫 = [P_1, P_2, ..., P_N], (1); below it N = ⌈T/S⌉ and P_i = [b_{(i−1)S+1}, ..., b_{iS}] for 1 ≤ i ≤ N, with T mod S ≠ 0.
  Paper quote: where N = ⌈ T
S ⌉ is the number of patches, and Pi =
[b(i−1)S+1, . . . , biS] for 1 ≤ i ≤ N. If T mod S ̸= 0,. The rendered patch definition and ceiling count match the extracted text. The ̸= extraction artifact is rendered as ≠.
- **agreement**, rendered page 3, rendered formulas: P_N = [b_{(N−1)S+1}, ..., b_T, e,...,e] with an underbrace labeled S−(T mod S).
  Paper quote: PN = [b(N −1)S+1, . . . , bT , e, . . . , e| {z }

S−(T mod S)

], (2). The underbrace padding count matches the text. The garbled '| {z }' is extraction noise from the underbrace.
- **agreement**, rendered page 3, rendered formulas: E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N, (3). The following text describes W_linear with shape (S × 257, H).
  Paper quote: Ei = Flatten(Pi) · Wlinear, 1 ≤ i ≤ N, (3). The rendered equation is consistent with the text. The 257D one-hot encoding (256 byte values + <eop>) is consistent with the S × 257 shape.
- **agreement**, rendered page 3, rendered formulas: Ê_i = Decoder_patch(ℰ_{<i} ⊕ 𝒳_{<i}), (4).
  Paper quote: ˆEi = Decoderpatch(E<i ⊕ X<i), (4). The rendered equation matches the extracted text, apart from calligraphic glyphs that were lost in extraction.
- **agreement**, rendered page 3, captions: The diagram shows Byte Patches feeding a Linear Projection Layer, then Patch Embeds & Position Embeds (0, 1, 2, N), then a Patch-Level Transformer Decoder, then a Byte-Level Transformer Decoder producing Output Bytes. The <eop> tokens pad the patches.
  Paper quote: Figure 2. bGPT segments byte sequences into patches, predicts
next patch features with a patch-level decoder, and reconstructs
bytes within patches using these features with a byte-level decoder.. The figure's components match both the caption and the three-component description in the text.
- **agreement**, rendered page 3, units: The page shows a patch matrix of S × 257 and a 257D one-hot vector covering all 256 byte values plus an <eop> token.
  Paper quote: each byte is one-hot encoded into a 257D vector, including
all 256 byte values and an <eop> token. The dimension 257 = 256 + 1 is internally consistent across the rendered page and the text.
- **agreement**, rendered page 8, rendered formulas: Page renders BPB_abc and BPB_midi with subscripts and bGPT^5, bGPT^3 with superscripts denoting data scale.
  Paper quote: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion. Rendered sub/superscripts match the extracted text and Section 5.3 notation (10^3 to 10^6 scale models); extraction flattened them.
- **agreement**, rendered page 7, sample counts: Rendered text shows data scales 10^3 (bGPT^3), 10^4 (bGPT^4), 10^5 (bGPT^5), 10^6 (bGPT^6) with superscripts; data conversion uses 10^3 to 10^5 and CPU uses 10^4 to 10^6.
  Paper quote: utilizing data scales ranging from 103
(bGPT3), 104 (bGPT4), 105 (bGPT5), to 106 (bGPT6).. The extracted '103' and similar values are flattened superscripts; the rendered page shows 10^3 through 10^6, consistent with the paper text.
- **agreement**, rendered page 7, axes: The x-axis is labelled Epoch with ticks from 0 to 32 in steps of 4. The y-axis is labelled Loss with ticks from 0.2 to 1.2. The legend lists bGPT3/4/5 Train and Eval.
  Paper quote: (a) Data Conversion. The plotted scales match the data-conversion scales of 10^3 to 10^5 and the 32 epochs listed in Table 2.
- **agreement**, rendered page 7, axes: The x-axis is labelled Epoch and runs from 0 to 32. The y-axis is labelled Loss with ticks from 0.4 to 1.6. The legend lists bGPT4/5/6 Train and Eval. One orange curve drops sharply around epoch 11-12.
  Paper quote: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b. The legend matches the CPU scales of 10^4 to 10^6. The visible drop in an orange curve near epoch 11-12 is consistent with the text, assuming orange denotes bGPT5 as the legend colours indicate.
- **agreement**, rendered page 7, captions: Table 5 lists bGPT5 with an ABC→MIDI BPB_midi value of 0.0011. The other values are 1.4319/0.2381/0.2796/1.1227, 0.9789/0.0202/0.1751/0.1763, and 0.7362/0.0011/0.1341/0.0789.
  Paper quote: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion. The rendered values match both the extracted table and the text.
- **agreement**, rendered page 7, captions: Table 6 shows bGPT4 at 0.6924 BPB and 27.2404% accuracy, bGPT5 at 0.0969 and 99.9702%, and bGPT6 at 0.0969 and 99.9961%.
  Paper quote: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%). The rounded accuracies in the text match the table. The identical BPB values for bGPT5 and bGPT6 are consistent with the stated 'diminishing returns'.
- **agreement**, rendered page 7, captions: Table 4 shows BPB/accuracy values of 0.4052/80.74 for random, 0.3899/84.66 for image, and 0.3900/85.26 for libri. The value 0.3899 and the libri accuracy 85.26 are in bold.
  Paper quote: bGPTimage 0.3899 84.66
bGPTlibri 0.3900 85.26. The rendered values match the text's claims that the BPB values are closely matched and that libri has higher accuracy.
- **agreement**, rendered page 7, units: The table headers show BPB and Acc (%), and Table 5 uses BPB_abc and BPB_midi subscripts.
  Paper quote: We separately calculated BPB values for each format to
clearly measure model performance.. The units used in the tables are consistent with the metric definitions in the text.
- **agreement**, rendered page 2, captions: Figure 1 shows .wav, .bmp, .mid, .abc and .bin inputs feeding a central bGPT block. The outputs are a waveform, a 'Cat' label, sheet music, and CPU chip icons labelled 0, 1, 2, 3, ..., N. The rendered caption reads 'The bGPT framework simulates digital systems through native binary data, and integrates diverse data types into a single model, treating everything as a byte sequence.'
  Paper quote: Figure 1. The bGPT framework simulates digital systems through native binary data, and integrates diverse data types into a single model,
treating everything as a byte sequence. This approach simplifies integration and expands application possibilities in the digital world.. The figure shows several data types (audio, image, MIDI, ABC, binary) entering one model, and CPU state icons labelled 0 to N represent simulated digital systems. The rendered caption text matches the extracted text.
- **agreement**, rendered page 5, sample counts: Table 1 row 'CPU States (proposed)' shows Total Files (Million) 2.1; body text says the CPU States dataset has 2.1 million instances.
  Paper quote: For CPU state modelling, we introduce the CPU States
dataset (with 2.1 million instances). The rendered table count matches the text count of 2.1 million.
- **agreement**, rendered page 5, units: The column headers read 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)', and 'GPU hours per Epoch'. The caption describes file counts in millions, dataset sizes in gigabytes, average file sizes in bytes, and GPU hours per epoch.
  Paper quote: Details include
file counts in millions, dataset sizes in gigabytes, average file sizes in bytes, and the GPU hours required per epoch for training.. The header units are consistent with the caption.
- **agreement**, rendered page 5, budgets: Table 2 lists Patch Size 16/16, Patch Length 512/512, Hidden Size 768, Epochs 32, Learning Rate 1e-04/1e-05, and Batch Size 16/1. Section 5.1 states a patch size of 16 and a sequence length of 512, with support for files up to 8KB.
  Paper quote: supporting file sizes up to
8KB using a patch size of 16 and a sequence length of 512.. 16 × 512 = 8192 bytes, which equals 8KB. The rendered table values match the text.
- **agreement**, rendered page 5, captions: The Table 1 caption references NVIDIA V100 GPU hours. The table includes a 'GPU hours per Epoch' column with values such as 107, 2.1, and 18.
  Paper quote: Table 1. Overview of datasets for bGPT evaluation, with computational costs benchmarked in NVIDIA V100 GPU hours.. The caption content matches the rendered columns.
- **agreement**, rendered page 4, rendered formulas: Rendered: b̂_{i,j} = Decoder_byte(Ê_i, b_{i,<j}), 1 ≤ j ≤ S, labelled (5).
  Paper quote: ˆbi,j = Decoderbyte( ˆEi, bi,<j), 1 ≤ j ≤ S, (5). The rendered equation matches the extracted text and the surrounding definitions of b̂_{i,j} and b_{i,<j}.
- **agreement**, rendered page 4, rendered formulas: Rendered: L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,b_2,...,b_i;θ), labelled (6).
  Paper quote: the objective is minimizing the
negative log-likelihood of the next byte prediction across
the sequence. The negative sum of log-probabilities over i=1..T−1 for the next byte is consistent with the described next-byte NLL over a length-T sequence.
- **agreement**, rendered page 4, rendered formulas: Rendered: L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B;θ), labelled (7).
  Paper quote: where yk is the boolean label for the k-th category, indicat-
ing whether the byte sequence belongs (true) or does not
belong (false) to that category. K is the total number of
categories. The summation bound K and the y_k terms match the stated definitions of a cross-entropy loss over K categories.
- **agreement**, rendered page 4, units: Text reads 'WAV format... 8000 Hz sampling rate, mono channel, and 8-bit depth, each trimmed to one-second lengths... BMP format with a resolution of 32×32, RGB colour, and 24-bit depth.'
  Paper quote: Audio files were converted to WA V
format, with specifications including an 8000 Hz sampling
rate, mono channel, and 8-bit depth, each trimmed to one-
second lengths. Image data were set to BMP format with a
resolution of 32×32, RGB colour, and 24-bit depth.. The rendered units match the text. They are also consistent with the reported mean file sizes (8044 B ≈ 8000 samples × 1 byte plus header; 3126 B ≈ 32×32×3 plus header).
- **agreement**, rendered page 16, sample counts: The code block has the header X:1, L:1/8, M:3/4, K:D. It is followed by six lines of bars ending 'FD C3 D | F/G/A B3 e | dc d4 |]'.
  Paper quote: X:1
L:1/8
M:3/4
K:D
de f3 g | ag/<f/ e4 | AB =c3 d | BA/<G/ A4 | fg a3 g | fd e4 |. The rendered ABC example matches the extracted text and the original header from Appendix A.1: 3/4 meter, D key, 1/8 unit length. Its longer, repeat-free form is consistent with the paper's claim that repeated sections are written out.
- **agreement**, rendered page 17, sample counts: Instruction sequences vary 'in length from 1 to 256'; 'over 516 million potential scenarios'.
  Paper quote: Instances are generated by execut-
ing random sequences of 1 to 256 instructions. Range matches Section 4.2; 516 million also matches Section 5.3.2 ('over 516 million').
- **agreement**, rendered page 15, captions: Caption reads 'Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.' above a six-system score with key signature of two sharps, 3/4 time and tempo marking quarter note = 120.
  Paper quote: Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.. Rendered caption matches the text. The two-sharp key signature and 3/4 meter are consistent with the ABC header 'M:3/4' and 'K:D' for the same tune.
- **agreement**, rendered page 14, captions: Sheet music with key signature of two sharps (D major), 3/4 time, chord symbols D, A, C, G/B, Bm, F#m, G; caption reads 'Sheet music example corresponding to the ABC notation of a folk tune in D major.'
  Paper quote: Figure 4. Sheet music example corresponding to the ABC notation of a folk tune in D major.. Rendered key signature (two sharps), meter 3/4 and chord labels match the caption and the ABC header K:D, M:3/4 and chord annotations in the listing.
- **agreement**, rendered page 14, units: Measure numbers 6, 10, 14 appear at the starts of systems 2–4; repeat signs end system 2 and bracket systems 3–4; first system contains a pickup plus 5 bars.
  Paper quote: de |"D" f3 g a{/g}f |"A" e4 AB |"C" =c3 d"G/B" B{/A}G |"A" A4 fg |
"D" a3 g fd |"A" e4 AB |"C" =c3 d e{/f}g |"D" f4 ::. Bar structure and repeat markers ('::' and ':|') in the ABC listing are consistent with the rendered measure numbering and repeat barlines.
- **mismatch**, rendered page 19, sample counts: The Address Variants column shows: HLT 0; CLR, INC, DEC, SHL, SHR, ROL, ROR and NOT each 0, 1; PUSH, POP and LOADI each 1; SWAP 1, 2; ADD, SUB, MUL, DIV, AND, OR and XOR each 1, 2, 3; MOV 2.
  Paper quote: These states include various instructions, totaling 21 unique
types with 43 variants. Summing the listed variants gives 1 + 7×2 + 3×1 + 2 + 7×3 + 1 = 42, not the 43 stated in the text. No row on the page accounts for an additional variant.
- **agreement**, rendered page 19, captions: The caption reads 'Table 7. Defined instruction set and the address variants of different instructions.' The page is numbered 19.
  Paper quote: Table 7 (located on page 19) details the instruction set and the variants each instruction can have, depending on the values in
the address fields.. The caption, the table content and the page location all match the appendix reference.
- **agreement**, rendered page 18, sample counts: Page shows states at steps 1 through 10 (step 0 is on page 17), with PC incrementing 1..10 and final IR: HLT.
  Paper quote: a randomly generated program for executing
10 instructions along with their corresponding states in human-readable form is provided below. Ten executed-instruction states plus the initial state on p.17 match the stated 10-instruction program ending in HLT.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 30 |
| Confirmed text-image mismatch (advisory) | 1 |
| Not applicable | 68 |
| Grounding failure: context, citation or readability | 0 |
| Missing or invalid confirmation | 7 |
| Conflicting assessments | 10 |
| Substantive uncertainty | 4 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.


