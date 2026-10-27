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

The paper introduces bGPT, a hierarchical Transformer trained by next-byte prediction, as a unified model for binary data across media modalities and for native binary tasks. Beyond text, audio and image classification, it evaluates the model on ABC↔MIDI symbolic music conversion and on CPU state prediction, which the authors frame as algorithm and hardware simulation. For the latter, the paper introduces a CPU States dataset of about 2.1 million instances. It also reports scaling experiments, including a performance jump on the conversion task that the authors describe as emergent.

## Contributions

1. **bGPT: byte-level model via next byte prediction.** Introduces bGPT, a model that treats all digital data as byte sequences and trains with next byte prediction to model and simulate the digital world, unifying diverse data types in one framework.
   *Claim support: unresolved · Significance: supported · Originality: contested*
2. **Hierarchical patch-based Transformer architecture with byte-level objectives.** bGPT segments byte sequences into fixed-size patches processed by a linear projection, a patch-level decoder and a byte-level decoder, trained with generative next-byte modelling followed by classification fine-tuning.
   *Claim support: unresolved · Significance: unassessed · Originality: contested*
3. **Modality-agnostic digital media processing with cross-modal transfer.** bGPT performs generative modelling and classification on text, audio and image files at the byte level without modality-specific designs, and exhibits cross-modal knowledge transfer between modalities.
   *Claim support: unresolved · Significance: unassessed · Originality: unassessed*
4. **Algorithm simulation via ABC–MIDI data conversion.** bGPT learns to simulate and reverse a symbolic music conversion algorithm, converting text ABC notation to binary MIDI and back, directly from paired byte sequences.
   *Claim support (inferred links): contested · Significance: supported · Originality: unresolved*
5. **CPU States dataset and hardware state modelling.** Introduces a 2.1-million-instance CPU States dataset of machine instructions and register states, and uses bGPT to predict CPU state updates from instructions, simulating hardware behaviour.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unresolved*
6. **Scalability and emergent abilities on native binary data.** Shows that bGPT's performance on native binary tasks scales with data volume, with signs of emergent ability in CPU state modelling.
   *Claim support (inferred links): contested · Significance: unassessed · Originality: unassessed*

Advisory assessments; the human reviewer decides whether each contribution qualifies.

### Contribution 1: bGPT: byte-level model via next byte prediction

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: supported**
- Applying a single next-byte-prediction model to both media files and native binary tasks (format conversion, CPU state simulation) is an interesting and potentially impactful framing.
- Unified byte-level modelling extended to native binary tasks (algorithm and CPU simulation) is a distinctive, potentially impactful framing.
- Sources: paper:chars/1238-5446, paper:chars/18456-21674, paper:chars/7775-10479

**Originality: contested**
- The authors present bGPT as a new byte model and a general digital world simulator. Their own Background section says byte-level modelling across modalities already exists, and that the architecture is adapted from prior work. Originality therefore lies mainly in the application framing and the native-binary tasks, not in the model.
- The authors claim to introduce bGPT for binary data and digital world modelling. They build on next-token prediction and position against media-focused byte models.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/7775-10479, paper:chars/10851-15278, paper:chars/1238-5446, paper:chars/172-1238

Paper’s wording: “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”

### Contribution 2: Hierarchical patch-based Transformer architecture with byte-level objectives

**Claim support: unresolved**
- No claims are linked to this contribution.
- No grounded finding addressed this.

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: contested**
- The paper adopts the hierarchical patch architecture from prior work. Its novelty therefore rests on the application scope, not on the architecture.
- Architecture is acknowledged as adapted from prior hierarchical byte/patch models; novelty lies in application, not method.
- The architecture is explicitly adapted from prior hierarchical/patch designs. Its novelty lies in the application scope, not the model.
- The authors attribute the hierarchical patch architecture to prior work, so the architecture is not a novel contribution.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/10851-15278, paper:chars/7775-10479

Paper’s wording: “We start by present- ing its hierarchical Transformer framework, which segments byte sequences into patches to manage computational effi- ciency. Subsequently, we present the training objectives of bGPT, including generative modelling and classification.”

### Contribution 3: Modality-agnostic digital media processing with cross-modal transfer

**Claim support: unresolved**
- No claims are linked to this contribution.
- Abstract claim that bGPT 'matches specialized models' is not supported for images and lacks byte-model baselines.
- The claim that bGPT 'matches specialized models' is overstated given Table 3. The CIFAR-10 gap is large, and the baselines were not trained under matched conditions.
- The abstract's claim that bGPT 'matches specialized models' is stronger than the reported results, which show a clear gap on CIFAR-10 and mixed cross-modal transfer.
- Sources: paper:chars/172-1238, paper:chars/25015-30472, paper:chars/23408-25015

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “Our experiments demonstrate the effectiveness of bGPT in modelling digital media data, which showcases modality-agnostic knowledge transfer.”

### Contribution 4: Algorithm simulation via ABC–MIDI data conversion

**Claim support (inferred links): contested**
- Linked claims:
  - C1 (inferred by the reviewer, not declared by the authors): It has almost flawlessly replicated the process of converting symbolic music data, achieving a low error rate of 0.0011 bits per byte in converting ABC notat…
- The ABC→MIDI result (C1, BPB_midi 0.0011) is reported, but support for 'almost flawlessly replicated' is limited. There is no baseline and no sequence-level correctness metric.
- The ABC→MIDI result of 0.0011 BPB is reported. However, BPB is not a conversion error rate, and the reverse direction is much weaker.
- Sources: paper:chars/31335-34448, paper:chars/30472-31335

**Significance: supported**
- The paper's most distinctive contribution is to frame algorithm and hardware simulation as next-byte prediction tasks: ABC↔MIDI conversion and CPU state prediction. These underexplored tasks could seed follow-up work.
- Sources: paper:chars/18456-21674, paper:chars/7775-10479

**Originality: unresolved**
- ABC↔MIDI conversion is positioned as a new task. The authors note that prior music models avoided modelling MIDI directly.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/31335-34448

Paper’s wording: “The bGPT model learns to convert text-based ABC notation music scores into binary MIDI performance signals and, reversely, convert MIDI back into ABC notation.”

### Contribution 5: CPU States dataset and hardware state modelling

**Claim support (inferred links): contested**
- Linked claims:
  - C2 (inferred by the reviewer, not declared by the authors): In addition, bGPT demonstrates exceptional capabilities in simulating CPU behaviour, with an accuracy exceeding 99.99% in executing various operations.
- The CPU 99.99% accuracy is measured byte-wise on a simplified, jump-free synthetic CPU with no simple baseline. This weakens the 'exceptional capabilities' and emergence claims.
- The 99.99% CPU-state accuracy (C2) is a byte-wise metric on a CPU that the authors themselves describe as simplified. The inspected results do not report trace-level correctness, and there is no baseline.
- The 99.99% CPU-state accuracy is computed byte-wise over a simplified CPU that has no jumps. Byte-wise accuracy can be high even when many full states are wrong.
- Sources: paper:chars/34448-36748, paper:chars/30472-31335, paper:chars/40096-79998, paper:chars/18456-21674, paper:chars/36748-38535

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unresolved**
- The CPU States dataset is a new resource contributed by the authors. It is useful as a benchmark, though simplified by the authors' own admission.
- Basis: the authors' own statements; cited works were not read.
- Sources: paper:chars/18456-21674

Paper’s wording: “For CPU state modelling, we introduce the CPU States dataset (with 2.1 million instances), offering a simplified representation of CPU behaviour for ease of data collec- tion and evaluation.”

### Contribution 6: Scalability and emergent abilities on native binary data

**Claim support (inferred links): contested**
- Linked claims:
  - C1 (inferred by the reviewer, not declared by the authors): It has almost flawlessly replicated the process of converting symbolic music data, achieving a low error rate of 0.0011 bits per byte in converting ABC notat…
  - C2 (inferred by the reviewer, not declared by the authors): In addition, bGPT demonstrates exceptional capabilities in simulating CPU behaviour, with an accuracy exceeding 99.99% in executing various operations.
- The 0.0011 BPB result for ABC→MIDI is reported as conditional BPB. No exact-conversion success rate is given, and the 'emergent ability' claim rests on a training curve from a single run.
- 'Emergent abilities' rests on a single loss-curve jump at epoch 11, conflating training dynamics with scale emergence.
- The 'emergent abilities' claim rests on a loss-curve jump for one run, and the paper's own rebuttal argument is weak.
- The claims of 'strong scalability' and 'emergent abilities' rest on a few data scales and on a within-run loss jump. This is limited support for emergence.
- Sources: paper:chars/31335-34448, paper:chars/34448-36748

**Significance: unassessed**
- No grounded finding addressed this.

**Originality: unassessed**
- No grounded finding addressed this.

Paper’s wording: “We observe a strong scalability of bGPT in mod- elling native binary data and even signs of emergent abilities.”

<details><summary>What the authors say is original (3 statements)</summary>

Authors' stated position:
- [claims, builds on] “Inspired by the success of next token prediction in natural lan- guage processing, we introduce bGPT, a model with next byte prediction to simulate the digi- tal world. bGPT matches specialized models in performance across various modalities, including text, audio, and images, and offers new possibil- ities for predicting, simulating, and diagnosing algorithm or hardware behaviour.”
- [claims; positioned against Raff et al., 2018, Guo et al., 2019] “In this paper, we introduce bGPT, a model designed for binary data processing and digital world modelling by next byte prediction.”
- [claims, builds on] “Conclusions In this paper, we present bGPT as a versatile simulator for the digital world, extending deep learning to binary data processing via next byte prediction.”

</details>


## Reasons to accept

1. **The paper's most distinctive contribution is to frame algorithm and hardware simulation as next-byte prediction tasks: ABC↔MIDI conversion and CPU state prediction. These underexplored tasks could seed follow-up work.**
   Likely builders on this work include researchers working on neural emulators, binary analysis, learned format converters and token-free foundation models.
   Evidence status: inference.
   Reasoning: The authors position prior byte-model work as neglecting native binary data. Against that positioning, treating format conversion and CPU state transitions as sequence modelling is a distinct and testable research direction. It is relevant to program analysis, emulation and binary reverse-engineering.
   Source `paper:chars/18456-21674`: This necessitates the ability to simulate and
reverse-engineer the conversion algorithm
   Source `paper:chars/7775-10479`: Despite progress, current research often neglects native bi-
nary data, focusing on narrow tasks

2. **Applying a single next-byte-prediction model to both media files and native binary tasks (format conversion, CPU state simulation) is an interesting and potentially impactful framing.**
   The value lies mainly in the task framing and in the CPU States dataset.
   Evidence status: inference.
   Reasoning: The paper studies byte-level modelling of native binary processes, a direction the authors describe as underexplored. A released task and dataset of this kind could enable follow-up work.
   Source `paper:chars/1238-5446`: In this paper, we introduce bGPT, a model designed for
binary data processing and digital world modelling by next
byte prediction.
   Source `paper:chars/18456-21674`: For CPU state modelling, we introduce the CPU States
dataset (with 2.1 million instances)

3. **Unified byte-level modelling extended to native binary tasks (algorithm and CPU simulation) is a distinctive, potentially impactful framing.**
   Value lies in the task framing and the new CPU States benchmark rather than in architecture.
   Evidence status: inference.
   Reasoning: The authors position the work against byte models that, as they describe them, address media or narrow tasks; evaluating byte models on algorithm/hardware simulation is a less-explored direction that could open a research agenda.
   Source `paper:chars/7775-10479`: Despite progress, current research often neglects native bi-
nary data, focusing on narrow tasks and overlooking the
broader potential of byte models in digital world simulation.
   Source `paper:chars/1238-5446`: underexplored tasks intrinsic to binary-native operations,
including data conversion and CPU state modelling, which
represent algorithm and hardware simulation, respectively.

4. **Extending next-byte prediction from media files to native binary tasks (algorithm and CPU simulation) is a distinctive, potentially impactful direction.**
   Likely impact rests on reframing byte models as simulators of digital processes.
   Evidence status: inference.
   Reasoning: The authors position prior byte models as media- or narrow-task focused. They frame algorithm and hardware simulation from raw bytes as a new evaluation axis. If this framing holds, the work opens a research direction rather than offering only another architecture.
   Source `paper:chars/7775-10479`: Despite progress, current research often neglects native bi-
nary data, focusing on narrow tasks and overlooking the
broader potential of byte models in digital world simulation.
   Source `paper:chars/1238-5446`: underexplored tasks intrinsic to binary-native operations,
including data conversion and CPU state modelling, which
represent algorithm and hardware simulation, respectively.

## Originality

By the paper's own account, the method is not where the originality lies. The Background section credits ByteFormer and MegaByte with modelling raw byte sequences across modalities, and states that bGPT adapts a hierarchical Transformer architecture from prior work that includes MegaByte. The inspected text does not state an architectural difference from MegaByte. The more distinctive element is the task framing: it treats format conversion and CPU state transitions as byte-sequence modelling, introduces a CPU States dataset, and positions ABC↔MIDI conversion as a new task because prior music models avoided modelling MIDI directly. These comparisons reflect the authors' descriptions of the cited works and were not independently verified. The 'paradigm shift' framing claims more than the related-work section concedes. A clear statement of what differs from MegaByte, and a comparison against MegaByte or ByteFormer on the native-binary tasks, would show whether any methodological novelty exists beyond the task and dataset contributions.

## Likely impact

The work could interest researchers on neural emulators, binary analysis and reverse-engineering, learned format converters, and token-free foundation models. A released CPU-state task and dataset could seed a benchmark line for byte models as simulators of digital processes. Several factors may limit its influence. The evaluation uses a simplified synthetic CPU that excludes jump instructions. CPU accuracy is measured byte-wise, with no trivial baselines. Conversion is reported only as BPB, without exact-match rates. Media results trail modality-specific baselines, and no other byte model is compared. Influence will likely come more from the framing and dataset than from bGPT as a model.

## Decision-critical concerns

1. **The authors present bGPT as a new byte model and a general digital world simulator. Their own Background section says byte-level modelling across modalities already exists, and that the architecture is adapted from prior work. Originality therefore lies mainly in the application framing and the native-binary tasks, not in the model.**
   The only distinction the paper draws is that prior work 'often neglects native binary data, focusing on narrow tasks'. In the inspected text, the paper does not specify an architectural difference from MegaByte.
   Evidence status: inference.
   Reasoning: The paper reports two relevant facts. First, ByteFormer and MegaByte already model byte sequences across modalities. Second, bGPT adapts a hierarchical architecture from cited work that includes MegaByte. By the authors' own account, therefore, neither the model nor multimodal byte modelling is new. The 'paradigm shift' framing claims more than the related-work section concedes. The cited works are described here only as the authors report them; I have not verified them.
   Source `paper:chars/7775-10479`: ByteFormer (Horton
et al., 2023) directly handles raw byte sequences converted
from images and audio
   Source `paper:chars/7775-10479`: MegaByte (Yu et al., 2023), on the other hand,
has been tested and proven to excel in modelling long byte
sequences across various modalities.
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture
   Source `paper:chars/1238-5446`: training models for next byte predic-
tion can potentially lead to a paradigm shift in deep learning
   - **Why this affects the decision:** Originality is central for a paper that introduces a model. If bGPT is essentially MegaByte applied to new data, it should be judged as an empirical or application study.
   - **Actionable revision:** Add an explicit comparison with MegaByte and ByteFormer that covers architecture, objective and scope, and state which components are new. Rescope the abstract and introduction to claim the native-binary evaluation rather than a new paradigm.
   - **What would resolve it:** Either a stated architectural or training difference from MegaByte, or revised framing that credits the novelty to the tasks and the dataset.

2. **Abstract claim that bGPT 'matches specialized models' is not supported for images and lacks byte-model baselines.**
   Single runs, no variance; ViT/AST pre-training scale differs.
   Evidence status: observation.
   Reasoning: A ~9.4-point CIFAR-10 gap contradicts 'matches'; baseline numbers come from different training pipelines, and no other byte model (ByteFormer, MegaByte) is compared.
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities, including
text, audio, and images
   Source `paper:chars/25015-30472`: bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%.
   Source `paper:chars/23408-25015`: ViT and AST
were pre-trained on ImageNet (Deng et al., 2009), and their
results were taken from the original studies.
   - **Why this affects the decision:** The headline modality-agnostic claim drives the contribution framing.
   - **Actionable revision:** Soften abstract/conclusion wording; add a same-budget byte-model baseline and seeds/variance.
   - **What would resolve it:** Revised claims matching Table 3, plus a comparable byte-model baseline.

3. **The CPU 99.99% accuracy is measured byte-wise on a simplified, jump-free synthetic CPU with no simple baseline. This weakens the 'exceptional capabilities' and emergence claims.**
   Near-perfect byte accuracy may overstate simulation ability.
   Evidence status: inference.
   Reasoning: Accuracy is computed per byte rather than per state or per program. Many register bytes are unchanged between steps, so a copy-previous-state baseline could already score high, and the paper reports no such baseline. In addition, with no jumps, the program counter increments trivially.
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets,
we investigated its performance across different data scales
   Source `paper:chars/40096-79998`: complex instructions like jump commands were deliberately excluded
   - **Why this affects the decision:** C2 is a headline abstract claim and underpins contribution 81b4... as well as the scalability contribution.
   - **Actionable revision:** Report a copy-previous-state baseline, plus exact-match accuracy per full state and per program on the CPU States evaluation set.
   - **What would resolve it:** A large gap between bGPT and the copy baseline on exact-match metrics would resolve this concern.

4. **CPU 99.99% accuracy is byte-wise on a simplified, jump-free synthetic CPU with teacher-forcing-like setup and no simple baselines.**
   Also unclear whether evaluation conditions on ground-truth previous states.
   Evidence status: inference.
   Reasoning: Many state bytes (e.g., unchanged registers, PC increments, IR copied from memory) are trivially predictable, so byte-wise accuracy can be very high without correct execution; without a copy-previous-state baseline or per-program exact-match, 99.99% does not establish simulation ability.
   Source `paper:chars/34448-36748`: The accuracy was
assessed through byte-wise comparisons with actual states.
   Source `paper:chars/40096-79998`: complex instructions like jump commands were deliberately excluded
   Source `paper:chars/30472-31335`: Due to the lack of baseline models and widely used datasets,
   - **Why this affects the decision:** C2 is a headline claim; its meaning depends on this.
   - **Actionable revision:** Report trivial baselines (copy previous state), whole-state and whole-program exact match, and per-instruction-type accuracy.
   - **What would resolve it:** High exact-match far above the copy baseline.

## Questions for the authors

1. **How do the authors scope generality claims given that Table 3's best bGPT variant trails each modality-specific baseline, by about 9.4 points on CIFAR-10?**
   Near-parity holds for text and speech but not for images. Baseline size and pre-training data may confound the comparison.
   Evidence status: inference.
   Reasoning: Two records report Table 3 values. In the first, the AG News baseline is 0.9237 BPB / 94.50% against bGPT_wiki at 92.49, CIFAR-10 is 88.69 vs 98.13, and Speech Commands is 96.03 vs 98.11. In the second, the bolded entries are the best bGPT values. Together they show the best bGPT variant is below the baseline on all three tasks, by about 2.0, 9.4 and 2.1 points.
   Source `review-record:visual/38`: The table shows bGPT_wiki at 1.0639/92.49 and Baselines at 0.9237/94.50 for AG News. It shows bGPT_image at 88.69 vs a baseline of 98.13 for CIFAR-10, and bGPT_libri at 96.03 vs 98.11 for Speech Commands.
   Source `review-record:visual/39`: Bold entries are 1.0639 and 92.49 (AG News), 3.1234 and 88.69 (CIFAR-10), and 1.4818 and 96.03 (Speech Commands).
   Source `paper:chars/25956-25993`: scored 0.9237 BPB and 94.50% accuracy
   Source `paper:chars/25380-25438`: excels in spoken content tasks compared to other variants.
   - **Why the answer matters:** If the paper states comparable performance to specialised models without qualification, the CIFAR-10 gap would weaken that central claim. If the claim is scoped per modality, the gap is consistent with it.
   - **Requested response:** Clarify how 'comparable performance' is meant for each modality, and discuss the image gap explicitly. Report baseline parameter counts and pre-training data next to bGPT.
   - **Answer that would resolve it:** Per-modality wording that acknowledges the gaps, plus a size and pre-training comparison of bGPT and the baselines.

2. **How does bGPT differ from MegaByte, and how would MegaByte or ByteFormer perform on the same native-binary tasks?**
   If bGPT outperforms MegaByte, that strengthens the case for a methodological contribution. If the two are equivalent, the originality rests on the tasks and the dataset.
   Evidence status: observation.
   Reasoning: MegaByte is the closest prior work the paper cites, and the results tables include no comparison against it.
   Source `paper:chars/7775-10479`: Inspired by MegaByte
(Yu et al., 2023)
   - **Why the answer matters:** This determines where the paper's novelty lies.
   - **Requested response:** Answer the question and, if feasible, report MegaByte results on the CPU States and ABC↔MIDI tasks.
   - **Answer that would resolve it:** A comparison table or a stated architectural difference.

3. **The 0.0011 BPB result for ABC→MIDI is reported as conditional BPB. No exact-conversion success rate is given, and the 'emergent ability' claim rests on a training curve from a single run.**
   The question for the authors: what fraction of greedily decoded MIDI files exactly match the reference? Is the epoch-11 jump reproducible across seeds?
   Evidence status: inference.
   Reasoning: Low BPB does not by itself establish that generated MIDI files are byte-exact or valid. A jump within one training run reflects optimization dynamics, not scale-driven emergence.
   Source `paper:chars/31335-34448`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   Source `paper:chars/34448-36748`: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b, indicating
an emergent ability
   - **Why the answer matters:** High exact-match rates would substantiate 'almost flawlessly'. A seed-dependent jump would undercut the emergence claim.
   - **Requested response:** Report exact-match and valid-file rates, and results from multiple seeds.
   - **Answer that would resolve it:** Exact-match tables and seed variance.

## Decision synthesis

The strongest case for the paper is its reframing of byte models as simulators of algorithms and hardware. The concrete CPU States dataset and the ABC↔MIDI task make that direction testable. The main concerns are about whether the evidence supports the claims.

(1) The abstract says bGPT 'matches specialized models'. Table 3, however, places the best bGPT variant below baselines on all three media tasks: by about 2 points on AG News and Speech Commands, and by about 9.4 points on CIFAR-10 (88.69% vs 98.13%). The baselines come from original studies with ImageNet pre-training. All results are single runs without variance, and no byte-model baseline is included.

(2) The 99.99% CPU accuracy is computed byte-wise on a jump-free synthetic CPU. Many state bytes may be trivially predictable, for example unchanged registers and an incrementing program counter. Without a copy-previous-state baseline, per-state or per-program exact match, and clarity on whether evaluation conditions on ground-truth prior states, this number may overstate simulation ability. Table 6 also suggests a threshold-like jump from 27% to near-perfect accuracy between 10^4 and 10^5 instances, followed by saturation; this is an advisory reading of three scale points.

(3) The ABC→MIDI result of 0.0011 BPB is a likelihood measure, not the 'error rate' the abstract calls it. The reverse direction is weaker (0.0789). The 'emergent ability' claim rests on a jump around epoch 11 in a single training run.

The score-changing questions for the authors are:
- How does bGPT differ from MegaByte, and how do MegaByte or ByteFormer perform on these tasks?
- What are the trivial baselines and exact-match rates for the CPU and conversion tasks?
- Is the epoch-11 jump reproducible across seeds?
- How will the generality claims be rescoped in light of Table 3?

Non-blocking improvements are to align the abstract wording with the tables and to state the architectural differences from prior hierarchical byte models explicitly.

This section identifies the evidence that appears most important; it intentionally does not provide a recommendation or score.

## Writing quality

Advisory assessment of whether the paper is written for a human reader (legibility of the central result, jargon discipline, evidence-as-prose, reader takeaway, and freedom from authoring-process leakage). The human reviewer owns any presentation score.

**What reads well**

- The abstract states two concrete headline results in plain terms, which makes the paper's claims easy to locate.
- The results section reports negative transfer and the CIFAR-10 shortfall openly, alongside explanations.

**Writing-quality issues**

1. **The abstract uses 'bits per byte' as if it were an error rate, without explaining it. It also does not say that the near-perfect results come from a simplified CPU and a single converter.**
   The abstract presents 0.0011 bits per byte as an 'error rate' and claims over 99.99% accuracy for CPU simulation. It does not say that this is byte-wise accuracy on a simplified synthetic CPU, or that only one ABC-to-MIDI converter was studied.
   - **Suggested revision:** In the abstract, describe bits per byte plainly, for example as prediction uncertainty where 0 means the output is perfectly predictable, rather than as an error rate. Also state that the CPU is a simplified synthetic one and that accuracy is measured byte by byte.

2. **The paper asserts significance and understanding with phrases such as 'paradigm shift', 'truly understand', and 'real comprehension' rather than letting the measurements speak.**
   Wording that matches the evidence would make the paper more credible to practitioners.
   - **Suggested revision:** Replace these phrases with statements of what was measured.

3. **Results are reported with four-decimal precision, which obscures the overall shape of the findings.**
   The key message is that performance jumps sharply as training data grows and then levels off. The excess precision buries that message.
   - **Suggested revision:** Round the reported values and state the jump with data scale in one plain sentence.

4. **Section 4.2 states 43 instruction variants, but the address variants enumerated in Table 7 sum to 44.**
   Table 7 enumerates 44 address variants, while Section 4.2 reports 43.
   - **Suggested revision:** Reconcile the count in Section 4.2 with Table 7. If one variant is intentionally excluded (for example, an invalid operand combination), state which one and why.

## Additional improvements (non-blocking)

1. **Table 6 shows CPU-modelling accuracy jumping sharply between two data scales and then saturating, with identical BPB at the two largest scales.**
   Only three scale points are reported for this task.
   Evidence status: inference.
   Reasoning: Accuracy is 27.24% at 10^4, 99.97% at 10^5 and 99.996% at 10^6. BPB is 0.0969 at both 10^5 and 10^6. Nearly all of the gain therefore occurs in one step, which looks more like a threshold effect than steady scaling.
   Source `review-record:visual/22`: Table 6 lists bGPT^4 (BPB 0.6924, Acc 27.2404), bGPT^5 (0.0969, 99.9702), and bGPT^6 (0.0969, 99.9961). Section 5.3 renders the data scales as superscripts 10^3 to 10^6.
   Source `review-record:visual/27`: The column header reads 'Acc (%)', with values such as 99.9702 and 99.9961.
   Source `paper:chars/30886-30975`: utilizing data scales ranging from 103
(bGPT3), 104 (bGPT4), 105 (bGPT5), to 106 (bGPT6).
   Source `paper:chars/35044-35117`: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%)
   - **Suggested revision:** Describe the result as a threshold effect, consider adding intermediate scales between 10^4 and 10^5, and explain why BPB is identical at 10^5 and 10^6.

2. **Architecture is acknowledged as adapted from prior hierarchical byte/patch models; novelty lies in application, not method.**
   Explicitly state what differs from MegaByte beyond task choice.
   Evidence status: observation.
   Reasoning: The paper itself credits the patch hierarchy to prior work and describes MegaByte/ByteFormer as already handling multi-modal bytes; the architectural contribution should not be credited as novel, and the difference from MegaByte is not stated explicitly. Cited works not independently checked.
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture
   Source `paper:chars/7775-10479`: MegaByte (Yu et al., 2023), on the other hand,
has been tested and proven to excel in modelling long byte
sequences across various modalities.
   - **Suggested revision:** Add a direct comparison paragraph (and ideally an empirical row) versus MegaByte/ByteFormer.

3. **The media results are competitive but below baselines, and the claimed 'matches specialized models' overstates them, especially for CIFAR-10.**
   The framing should be aligned with the results tables.
   Evidence status: observation.
   Reasoning: The authors themselves report a gap of about 10 points on CIFAR-10 against ViT. This contradicts the abstract's 'matches'. Cross-modal transfer is shown but is mixed, including negative transfer for text.
   Source `paper:chars/172-1238`: bGPT matches specialized models in
performance across various modalities
   Source `paper:chars/25015-30472`: a noticeable difference
is seen with bGPTimage lagging ViT, with an accuracy of
88.69% against 98.13%.
   - **Suggested revision:** Revise the abstract and conclusions to say 'approaches' and to note the image gap.

4. **The ABC→MIDI result of 0.0011 BPB is reported. However, BPB is not a conversion error rate, and the reverse direction is much weaker.**
   C1 is supported as a BPB value, but the 'error rate' wording should be corrected.
   Evidence status: observation.
   Reasoning: Table 5 supports C1 numerically. The abstract, however, calls the number an 'error rate', while BPB is a likelihood measure. MIDI→ABC reaches 0.0789, so the bidirectional framing is less strong than the abstract implies.
   Source `paper:chars/31335-34448`: bGPT5 0.7362 0.0011 0.1341 0.0789
   Source `paper:chars/31335-34448`: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion
   - **Suggested revision:** Rename the metric in the abstract and report the exact-match file conversion rate under greedy decoding.

5. **ABC↔MIDI conversion is positioned as a new task. The authors note that prior music models avoided modelling MIDI directly.**
   The originality rests on the task framing, not on the method.
   Evidence status: observation.
   Reasoning: The authors explicitly distinguish this task from the cited symbolic music models. The cited works are described here only as the authors report them; I have not verified them.
   Source `paper:chars/31335-34448`: While previous
studies avoided direct MIDI modelling due to its binary
   - **Suggested revision:** None required.

6. **The claims of 'strong scalability' and 'emergent abilities' rest on a few data scales and on a within-run loss jump. This is limited support for emergence.**
   A plateau-break during training is a different phenomenon from emergence induced by scale.
   Evidence status: inference.
   Reasoning: The jump occurs within a single training run rather than across scales. In addition, bGPT6's BPB equals bGPT5's (0.0969). Together these weaken the scaling and emergence framing.
   Source `paper:chars/34448-36748`: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b, indicating
an emergent ability in CPU state modelling.
   Source `paper:chars/31335-34448`: bGPT6 0.0969 99.9961
   - **Suggested revision:** Soften the 'emergent' language, or add results across multiple model and data scales with multiple seeds.

7. **In Table 4, bGPT_libri's accuracy advantage over bGPT_image is 0.6 points, and their BPB values are effectively tied.**
   The supplied records show no multi-seed results for this comparison.
   Evidence status: inference.
   Reasoning: The table shows 85.26 vs 84.66 accuracy and BPB of 0.3900 vs 0.3899. The text presents the accuracy difference as notable evidence that audio pre-training transfers better. A 0.6-point gap may fall within run-to-run variation.
   Source `review-record:visual/26`: Table 4 shows BPB values of 0.4052, 0.3899 (bold), and 0.3900, and Acc values of 80.74, 84.66, and 85.26 (bold).
   Source `paper:chars/29720-29837`: Notably, bGPTlibri, pre-trained
on audio, achieves higher accuracy than bGPTimage on
spectrograms with speech content
   - **Suggested revision:** Report the mean and spread over several seeds, or soften the 'notably' wording.

8. **The architecture is explicitly adapted from prior hierarchical/patch designs. Its novelty lies in the application scope, not the model.**
   The architecture should be credited as an adaptation of prior designs.
   Evidence status: observation.
   Reasoning: The authors state that the architecture is adapted from prior work. They also describe MegaByte as already modelling bytes across modalities. As a result, architectural novelty is not claimed, and the author-reported difference from MegaByte and ByteFormer is task scope. Independent verification of that difference is unresolved.
   Source `paper:chars/10851-15278`: inspired by previous
work (Wu et al., 2023b; Yu et al., 2023; Wu et al., 2023a;
Yang et al., 2023), bGPT adapts a hierarchical Trans-
former architecture
   Source `paper:chars/7775-10479`: MegaByte (Yu et al., 2023), on the other hand,
has been tested and proven to excel in modelling long byte
sequences across various modalities.
   - **Suggested revision:** State explicitly which architectural differences from MegaByte exist, if any.

9. **The authors attribute the hierarchical patch architecture to prior work, so the architecture is not a novel contribution.**
   The inspected text does not identify any modification relative to the cited hierarchical models.
   Evidence status: observation.
   Reasoning: The word 'adapts', together with the attached citations, presents the architecture as borrowed. It should be credited as a design choice, not as an advance.
   Source `paper:chars/10851-15278`: bGPT adapts a hierarchical Trans-
former architecture
   - **Suggested revision:** State explicitly which details, if any, differ from MegaByte. Examples include the one-hot linear patch projection and the classification head.

10. **The limitations and impact sections candidly acknowledge simplified CPUs, low-resolution media, and the risk of intellectual-property misuse.**
   These limitations should also temper the wording of the abstract.
   Evidence status: observation.
   Reasoning: The scope limits are stated directly in the paper.
   Source `paper:chars/36748-38535`: our
CPU state modelling experiments focused solely on simpli-
fied CPUs, omitting the use of real modern CPUs
   - **Suggested revision:** Mirror these limitations in the abstract.

## Evidence to examine (advisory)

### Sample counts: Table 1 row 'CPU States (proposed)' shows Total Files (Million) = 2.1; the body text on the same page states the CPU States dataset has 2.1 million instances.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered table count matches the text count. Appendix B also gives 2.1 million training entries.

- Source: `review-record:visual/0`
- Source: `paper:chars/20705-20794`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: The caption specifies file counts in millions, sizes in gigabytes, average file sizes in bytes, and GPU hours per epoch. The column headers read 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)', and 'GPU hours per Epoch'.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption units match the rendered column headers.

- Source: `review-record:visual/1`
- Source: `paper:chars/19668-19816`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Units: Mean file sizes are rendered as ImageNet/CIFAR-10 3126, LibriSpeech/Speech Commands 8044, and CPU States 3103 bytes. The text describes 32×32 24-bit BMP files, one-second 8 kHz 8-bit WAV files, an 8KB limit, and a 1KB memory block plus 16-byte states.

Scope: paper-only; analysis: visual; evidence status: inference.
32×32×3 = 3072 bytes plus a header gives about 3126. 8000 samples plus a header gives about 8044. All values are within 16×512 = 8192 bytes, so they are consistent.

- Source: `review-record:visual/2`
- Source: `paper:chars/21970-22056`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Budgets: Table 2 shows Patch Size 16 and Patch Length 512 for both pre-training and fine-tuning. It also shows Hidden Size 768, Epochs 32, Learning Rate 1e-04 for pre-training and 1e-05 for fine-tuning, and Batch Size 16 for pre-training and 1 for fine-tuning.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered hyperparameters match the text, and 16×512 = 8192 bytes, which is 8KB.

- Source: `review-record:visual/3`
- Source: `paper:chars/21970-22056`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: The caption reads 'Hyperparameter settings for pre-training and fine-tuning.' The columns are Pre-training and Fine-tuning.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption matches the table structure.

- Source: `review-record:visual/4`
- Source: `paper:chars/22396-22462`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Captions: The caption mentions NVIDIA V100 GPU hours, and the table includes a 'GPU hours per Epoch' column with values from 1.1 to 107.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption is consistent with the rendered column.

- Source: `review-record:visual/5`
- Source: `paper:chars/19605-19666`
- Source: `paper:p.5`
- Source: [`review-output:visual/page-5.png`](visual/page-5.png)

### Rendered formulas: Eq. (1) renders as 𝒫 = [P1, P2, ..., PN]; text below renders N = ⌈T/S⌉ and Pi = [b_{(i−1)S+1}, ..., b_{iS}] for 1 ≤ i ≤ N, with condition T mod S ≠ 0.

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered formula matches the extracted definition; ceiling of T/S gives patch count consistent with S bytes per patch.

- Source: `review-record:visual/8`
- Source: `paper:chars/11776-11885`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Eq. (2) renders P_N = [b_{(N−1)S+1}, ..., b_T, e, ..., e] with an underbrace labelled S−(T mod S).

Scope: paper-only; analysis: visual; evidence status: inference.
Padding count S−(T mod S) is consistent with padding the last patch to length S.

- Source: `review-record:visual/9`
- Source: `paper:chars/12865-12927`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N; text states shape (S × 257, H) and S × 257 matrix, 257D one-hot including 256 bytes and <eop>.

Scope: paper-only; analysis: visual; evidence status: inference.
Dimensions are consistent: flattened S×257 vector times (S×257, H) matrix yields H-dim vector; 256+1=257.

- Source: `review-record:visual/10`
- Source: `paper:chars/13936-14031`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Rendered formulas: Ê_i = Decoder_patch(ℰ_{<i} ⊕ 𝒳_{<i}).

Scope: paper-only; analysis: visual; evidence status: inference.
Rendered formula matches text.

- Source: `review-record:visual/11`
- Source: `paper:chars/14439-14473`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Captions: Diagram shows Byte Patches → Linear Projection Layer → Patch Embeds & Position Embeds (0,1,2,N) → Patch-Level Transformer Decoder → Patch Features & Input Bytes → Byte-Level Transformer Decoder → Output Bytes; last patch padded with <eop>.

Scope: paper-only; analysis: visual; evidence status: inference.
Caption describes the depicted pipeline accurately.

- Source: `review-record:visual/12`
- Source: `paper:chars/12668-12863`
- Source: `paper:p.3`
- Source: [`review-output:visual/page-3.png`](visual/page-3.png)

### Units: Abstract states "0.0011 bits per byte in converting ABC notation to MIDI format".

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered unit and value match the extracted text and the Table 5 bGPT5 BPBmidi value of 0.0011.

- Source: `review-record:visual/16`
- Source: `paper:chars/829-921`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Reviewer coverage limitation: sample counts (paper:p.1)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/17`
- Source: `paper:chars/1010-1075`
- Source: `paper:p.1`
- Source: [`review-output:visual/page-1.png`](visual/page-1.png)

### Sample counts: Table 6 lists bGPT^4 (BPB 0.6924, Acc 27.2404), bGPT^5 (0.0969, 99.9702), and bGPT^6 (0.0969, 99.9961). Section 5.3 renders the data scales as superscripts 10^3 to 10^6.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered superscripts show the data scales are 10^3 through 10^6. The CPU table uses scales 10^4 to 10^6, consistent with the text's statement that CPU state modelling was 'evaluated on scales from 104 to 106'.

- Source: `review-record:visual/22`
- Source: `paper:chars/30886-30975`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Axes: Panel (a) has an Epoch x-axis from 0 to 32 and a Loss y-axis from 0.2 to 1.2. Its legend lists bGPT^3, bGPT^4, and bGPT^5 Train/Eval.

Scope: paper-only; analysis: visual; evidence status: inference.
The legend matches the scales 10^3 to 10^5. The 32-epoch axis matches Table 2, which lists 32 epochs.

- Source: `review-record:visual/23`
- Source: `paper:chars/31078-31239`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Axes: Panel (b) has an Epoch axis from 0 to 32, a Loss axis from 0.4 to 1.6, and a legend with bGPT^4, bGPT^5, and bGPT^6. One orange curve drops sharply near epoch 11–12.

Scope: paper-only; analysis: visual; evidence status: inference.
The visible drop in the orange (bGPT^5) curve near epoch 11 matches the text's claim of an improvement around epoch 11.

- Source: `review-record:visual/24`
- Source: `paper:chars/35331-35430`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Rendered formulas: Table 5 columns are rendered as BPB with subscripts abc and midi under ABC→MIDI and MIDI→ABC headers. bGPT^5 has BPB_midi 0.0011 under ABC→MIDI.

Scope: paper-only; analysis: visual; evidence status: inference.
The subscripts are rendered correctly, and the 0.0011 value matches the text.

- Source: `review-record:visual/25`
- Source: `paper:chars/33656-33745`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Captions: Table 4 shows BPB values of 0.4052, 0.3899 (bold), and 0.3900, and Acc values of 80.74, 84.66, and 85.26 (bold).

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered values match the text: BPB is closely matched, and bGPT_libri has the higher accuracy.

- Source: `review-record:visual/26`
- Source: `paper:chars/29720-29837`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Units: The column header reads 'Acc (%)', with values such as 99.9702 and 99.9961.

Scope: paper-only; analysis: visual; evidence status: inference.
The percent unit is consistent, and the text's figures are rounded versions of the table values.

- Source: `review-record:visual/27`
- Source: `paper:chars/35044-35117`
- Source: `paper:p.7`
- Source: [`review-output:visual/page-7.png`](visual/page-7.png)

### Reviewer coverage limitation: rendered formulas (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/29`
- Source: `paper:chars/30886-30975`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: sample counts (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/30`
- Source: `paper:chars/32550-32583`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: sample counts (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/31`
- Source: `paper:chars/32719-32760`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: axes (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Substantive uncertainty. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/32`
- Source: `paper:chars/35331-35430`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Reviewer coverage limitation: units (paper:p.8)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/34`
- Source: `paper:chars/22225-22365`
- Source: `paper:p.8`
- Source: [`review-output:visual/page-8.png`](visual/page-8.png)

### Captions: Caption names GPT2-small on AG News, ViT-B/16 on CIFAR-10, AST on Speech Commands v2; bGPT_signal = ImageNet+LibriSpeech, bGPT_mix = ImageNet+LibriSpeech+Wikipedia.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption is consistent with the model definitions in Section 5.2 and the baselines in Section 5.2.1.

- Source: `review-record:visual/35`
- Source: `paper:chars/23083-23186`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Sample counts: The column headers read AG News (4 classes), CIFAR-10 (10 classes) and Speech Commands v2 (36 classes). The rows list six bGPT variants plus Baselines.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered class counts match the extracted text. The six variants match the six models described in Section 5.2.

- Source: `review-record:visual/36`
- Source: `paper:chars/24561-24634`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Units: Each dataset has metric columns labelled BPB and Acc (%). Accuracy values fall in the percent range (76.73–98.13), and BPB values have no percent sign.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered header units match the extracted header text. The accuracy cells fall in a plausible percent range.

- Source: `review-record:visual/37`
- Source: `paper:chars/24636-24677`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Captions: The table shows bGPT_wiki at 1.0639/92.49 and Baselines at 0.9237/94.50 for AG News. It shows bGPT_image at 88.69 vs a baseline of 98.13 for CIFAR-10, and bGPT_libri at 96.03 vs 98.11 for Speech Commands.

Scope: paper-only; analysis: visual; evidence status: inference.
The values cited in the page text match the rendered table cells, including the GPT2-small baseline of 0.9237 BPB and 94.50%.

- Source: `review-record:visual/38`
- Source: `paper:chars/25956-25993`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Captions: Bold entries are 1.0639 and 92.49 (AG News), 3.1234 and 88.69 (CIFAR-10), and 1.4818 and 96.03 (Speech Commands).

Scope: paper-only; analysis: visual; evidence status: inference.
Each bolded value is the best bGPT value in its column (lowest BPB, highest Acc). This is consistent with the text's claims about bGPT_libri and bGPT_wiki.

- Source: `review-record:visual/39`
- Source: `paper:chars/25380-25438`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Units: The text reads '32×32 BMP spectrograms' and 'converting 8KB audio files to 3KB images'.

Scope: paper-only; analysis: visual; evidence status: inference.
These sizes are consistent with 8 kHz/8-bit/1 s WAV files (mean 8044 bytes in Table 1) and 32×32 24-bit BMP files (mean 3126 bytes).

- Source: `review-record:visual/40`
- Source: `paper:chars/28540-28633`
- Source: `paper:p.6`
- Source: [`review-output:visual/page-6.png`](visual/page-6.png)

### Rendered formulas: Rendered: b̂_{i,j} = Decoder_byte(Ê_i, b_{i,<j}), 1 ≤ j ≤ S, (5)

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered equation matches the extracted text once extraction noise is accounted for.

- Source: `review-record:visual/44`
- Source: `paper:chars/15098-15146`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: Rendered: L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,...,b_i; θ), (6)

Scope: paper-only; analysis: visual; evidence status: inference.
The summation bounds from i=1 to T−1 are consistent with next-byte prediction over a sequence of length T.

- Source: `review-record:visual/45`
- Source: `paper:chars/15800-15858`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Rendered formulas: Rendered: L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B; θ), (7)

Scope: paper-only; analysis: visual; evidence status: inference.
The sum over K categories agrees with the definition of K as the total number of categories.

- Source: `review-record:visual/46`
- Source: `paper:chars/16662-16704`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Units: Text reads: WAV, 8000 Hz sampling rate, mono channel, 8-bit depth, one-second lengths; BMP 32×32, RGB, 24-bit depth.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered values match the extracted text. They are also consistent with Table 1 mean file sizes of 8044 B (about 8000 bytes plus header) and 3126 B (32×32×3 = 3072 bytes plus header).

- Source: `review-record:visual/47`
- Source: `paper:chars/18269-18454`
- Source: `paper:p.4`
- Source: [`review-output:visual/page-4.png`](visual/page-4.png)

### Captions: Figure 1 shows .wav, .bmp (cat images), .mid (piano roll), .abc and .bin (chip labelled 0) inputs flowing into a central bGPT box, with outputs of an audio waveform, a 'Cat' label, sheet music, and chips labelled 1, 2, 3 … N. The caption reads 'The bGPT framework simulates digital systems through native binary data, and integrates diverse data types into a single model, treating everything as a byte sequence.'

Scope: paper-only; analysis: visual; evidence status: inference.
The caption's rendered text matches the extracted text. The diagram's content is consistent with the caption: multiple data types go into one model, and the 0→1…N CPU-state chips represent digital-system simulation.

- Source: `review-record:visual/52`
- Source: `paper:chars/4825-5099`
- Source: `paper:p.2`
- Source: [`review-output:visual/page-2.png`](visual/page-2.png)

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/58`
- Source: `paper:chars/4825-5002`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Reviewer coverage limitation: captions (paper:p.16)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/59`
- Source: `paper:chars/65157-65255`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Rendered formulas: A gray code block shows the header X:1, L:1/8, M:3/4, K:D. The body is written out without repeat signs and ends with 'dc d4 |]'.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered ABC block matches the extracted text. It has no '::' repeat markers, which agrees with the stated elimination of repeat signs.

- Source: `review-record:visual/60`
- Source: `paper:chars/69353-69435`
- Source: `paper:p.16`
- Source: [`review-output:visual/page-16.png`](visual/page-16.png)

### Sample counts: Page 17 states that the dataset comprises 2.1 million training entries and 21,000 evaluation entries.

Scope: paper-only; analysis: visual; evidence status: inference.
This matches Section 4.2, which reports 2.1 million instances, and Table 1, which lists 2.1 million CPU States files.

- Source: `review-record:visual/65`
- Source: `paper:chars/75331-75450`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Units: The page shows 1KB memory blocks paired with a 16-byte state sequence. The listed register sizes are PC 1 byte, ACC 1-byte, IR 4 bytes and general-purpose registers 10 bytes.

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered register sizes sum to 1+1+4+10=16 bytes. This matches the stated 16-byte state and the 1KB memory block described in Section 4.2.

- Source: `review-record:visual/66`
- Source: `paper:chars/72023-72138`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Sample counts: The page states that random instruction sequences vary in length from 1 to 256 and that there are over 516 million potential scenarios.

Scope: paper-only; analysis: visual; evidence status: inference.
The 1 to 256 range matches Section 4.2. The figure of over 516 million matches the count of over 516 million scenarios in Section 5.3.2.

- Source: `review-record:visual/67`
- Source: `paper:chars/74807-74900`
- Source: `paper:p.17`
- Source: [`review-output:visual/page-17.png`](visual/page-17.png)

### Reviewer coverage limitation: captions (paper:p.9)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/78`
- Source: `paper:chars/39090-39240`
- Source: `paper:p.9`
- Source: [`review-output:visual/page-9.png`](visual/page-9.png)

### Captions: Single-staff score in D major (two sharps), 3/4 time, tempo marking quarter = 120, measure numbers 7, 13, 19, 25, 30, with no repeat signs and an ending double barline. The caption reads 'Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.'

Scope: paper-only; analysis: visual; evidence status: inference.
The rendered caption matches the paper text. The time signature and key match the ABC header 'M:3/4' and 'K:D'. The absence of repeat signs matches the stated elimination of repeats in MIDI conversion.

- Source: `review-record:visual/85`
- Source: `paper:chars/65157-65255`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Reviewer coverage limitation: sample counts (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/86`
- Source: `paper:chars/69373-69435`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Reviewer coverage limitation: rendered formulas (paper:p.15)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Grounding failure: context, citation or readability. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/87`
- Source: `paper:p.15`
- Source: [`review-output:visual/page-15.png`](visual/page-15.png)

### Reviewer coverage limitation: captions (paper:p.14)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/107`
- Source: `paper:chars/62105-62195`
- Source: `paper:p.14`
- Source: [`review-output:visual/page-14.png`](visual/page-14.png)

### Reviewer coverage limitation: units (paper:p.14)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/108`
- Source: `paper:chars/63694-63733`
- Source: `paper:p.14`
- Source: [`review-output:visual/page-14.png`](visual/page-14.png)

### Reviewer coverage limitation: sample counts (paper:p.19)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Conflicting assessments. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/113`
- Source: `paper:chars/21049-21133`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Sample counts: The Address Variants column shows HLT=0 (1 variant); CLR, INC, DEC, SHL, SHR, ROL, ROR and NOT=0,1 (8×2=16); PUSH, POP and LOADI=1 (3); SWAP=1,2 (2); ADD, SUB, MUL, DIV, AND, OR and XOR=1,2,3 (7×3=21); MOV=2 (1). Together these list 44 address variants.

Scope: paper-only; analysis: visual; evidence status: inference.
The variants rendered in Table 7 add up to 44, not the 43 stated in Section 4.2.

- Source: `review-record:visual/114`
- Source: `paper:chars/21049-21133`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Captions: The caption reads 'Table 7. Defined instruction set and the address variants of different instructions.' The page number 19 is shown.

Scope: paper-only; analysis: visual; evidence status: inference.
The caption, the table content and the page location match the Appendix B reference.

- Source: `review-record:visual/115`
- Source: `paper:chars/73809-73956`
- Source: `paper:p.19`
- Source: [`review-output:visual/page-19.png`](visual/page-19.png)

### Sample counts: The rendered trace shows states at steps 1 through 10, ending with IR: HLT and PC: 10. Together with step 0 on page 17, this gives 10 executed instructions.

Scope: paper-only; analysis: visual; evidence status: inference.
The listed program has 10 instructions, ending in 'HLT'. The rendered states run PC 1 to 10, which matches the stated count.

- Source: `review-record:visual/120`
- Source: `paper:chars/75731-75868`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

### Reviewer coverage limitation: units (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Missing or invalid confirmation. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/121`
- Source: `paper:chars/72658-72741`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

### Reviewer coverage limitation: sample counts (paper:p.18)

Scope: paper-only; analysis: visual; evidence status: unassessed.
Grounding failure: context, citation or readability. This is not evidence of a readability or scientific defect in the submission. Inspect the original source with adequate resolution and context before drawing conclusions; the raw model output remains in the audit.

- Source: `review-record:visual/126`
- Source: `paper:p.18`
- Source: [`review-output:visual/page-18.png`](visual/page-18.png)

## Direct visual evidence (advisory)

- **agreement**, rendered page 5, sample counts: Table 1 row 'CPU States (proposed)' shows Total Files (Million) = 2.1; the body text on the same page states the CPU States dataset has 2.1 million instances.
  Paper quote: For CPU state modelling, we introduce the CPU States
dataset (with 2.1 million instances). The rendered table count matches the text count. Appendix B also gives 2.1 million training entries.
- **agreement**, rendered page 5, units: The caption specifies file counts in millions, sizes in gigabytes, average file sizes in bytes, and GPU hours per epoch. The column headers read 'Total Files (Million)', 'Total Bytes (GB)', 'Mean File Size (Byte)', and 'GPU hours per Epoch'.
  Paper quote: Details include
file counts in millions, dataset sizes in gigabytes, average file sizes in bytes, and the GPU hours required per epoch for training.. The caption units match the rendered column headers.
- **agreement**, rendered page 5, units: Mean file sizes are rendered as ImageNet/CIFAR-10 3126, LibriSpeech/Speech Commands 8044, and CPU States 3103 bytes. The text describes 32×32 24-bit BMP files, one-second 8 kHz 8-bit WAV files, an 8KB limit, and a 1KB memory block plus 16-byte states.
  Paper quote: supporting file sizes up to
8KB using a patch size of 16 and a sequence length of 512.. 32×32×3 = 3072 bytes plus a header gives about 3126. 8000 samples plus a header gives about 8044. All values are within 16×512 = 8192 bytes, so they are consistent.
- **agreement**, rendered page 5, budgets: Table 2 shows Patch Size 16 and Patch Length 512 for both pre-training and fine-tuning. It also shows Hidden Size 768, Epochs 32, Learning Rate 1e-04 for pre-training and 1e-05 for fine-tuning, and Batch Size 16 for pre-training and 1 for fine-tuning.
  Paper quote: supporting file sizes up to
8KB using a patch size of 16 and a sequence length of 512.. The rendered hyperparameters match the text, and 16×512 = 8192 bytes, which is 8KB.
- **agreement**, rendered page 5, captions: The caption reads 'Hyperparameter settings for pre-training and fine-tuning.' The columns are Pre-training and Fine-tuning.
  Paper quote: Table 2. Hyperparameter settings for pre-training and fine-tuning.. The caption matches the table structure.
- **agreement**, rendered page 5, captions: The caption mentions NVIDIA V100 GPU hours, and the table includes a 'GPU hours per Epoch' column with values from 1.1 to 107.
  Paper quote: with computational costs benchmarked in NVIDIA V100 GPU hours. The caption is consistent with the rendered column.
- **agreement**, rendered page 3, rendered formulas: Eq. (1) renders as 𝒫 = [P1, P2, ..., PN]; text below renders N = ⌈T/S⌉ and Pi = [b_{(i−1)S+1}, ..., b_{iS}] for 1 ≤ i ≤ N, with condition T mod S ≠ 0.
  Paper quote: where N = ⌈ T
S ⌉ is the number of patches, and Pi =
[b(i−1)S+1, . . . , biS] for 1 ≤ i ≤ N. If T mod S ̸= 0,. Rendered formula matches the extracted definition; ceiling of T/S gives patch count consistent with S bytes per patch.
- **agreement**, rendered page 3, rendered formulas: Eq. (2) renders P_N = [b_{(N−1)S+1}, ..., b_T, e, ..., e] with an underbrace labelled S−(T mod S).
  Paper quote: PN = [b(N −1)S+1, . . . , bT , e, . . . , e| {z }

S−(T mod S). Padding count S−(T mod S) is consistent with padding the last patch to length S.
- **agreement**, rendered page 3, rendered formulas: E_i = Flatten(P_i) · W_linear, 1 ≤ i ≤ N; text states shape (S × 257, H) and S × 257 matrix, 257D one-hot including 256 bytes and <eop>.
  Paper quote: where Wlinear is the weight matrix of the linear projection
layer with a shape of (S × 257, H).. Dimensions are consistent: flattened S×257 vector times (S×257, H) matrix yields H-dim vector; 256+1=257.
- **agreement**, rendered page 3, rendered formulas: Ê_i = Decoder_patch(ℰ_{<i} ⊕ 𝒳_{<i}).
  Paper quote: ˆEi = Decoderpatch(E<i ⊕ X<i), (4). Rendered formula matches text.
- **agreement**, rendered page 3, captions: Diagram shows Byte Patches → Linear Projection Layer → Patch Embeds & Position Embeds (0,1,2,N) → Patch-Level Transformer Decoder → Patch Features & Input Bytes → Byte-Level Transformer Decoder → Output Bytes; last patch padded with <eop>.
  Paper quote: Figure 2. bGPT segments byte sequences into patches, predicts
next patch features with a patch-level decoder, and reconstructs
bytes within patches using these features with a byte-level decoder.. Caption describes the depicted pipeline accurately.
- **agreement**, rendered page 1, units: Abstract states "0.0011 bits per byte in converting ABC notation to MIDI format".
  Paper quote: achieving a low error rate of
0.0011 bits per byte in converting ABC notation
to MIDI format. The rendered unit and value match the extracted text and the Table 5 bGPT5 BPBmidi value of 0.0011.
- **agreement**, rendered page 7, sample counts: Table 6 lists bGPT^4 (BPB 0.6924, Acc 27.2404), bGPT^5 (0.0969, 99.9702), and bGPT^6 (0.0969, 99.9961). Section 5.3 renders the data scales as superscripts 10^3 to 10^6.
  Paper quote: utilizing data scales ranging from 103
(bGPT3), 104 (bGPT4), 105 (bGPT5), to 106 (bGPT6).. The rendered superscripts show the data scales are 10^3 through 10^6. The CPU table uses scales 10^4 to 10^6, consistent with the text's statement that CPU state modelling was 'evaluated on scales from 104 to 106'.
- **agreement**, rendered page 7, axes: Panel (a) has an Epoch x-axis from 0 to 32 and a Loss y-axis from 0.2 to 1.2. Its legend lists bGPT^3, bGPT^4, and bGPT^5 Train/Eval.
  Paper quote: For data conversion,
we utilized the IrishMAN dataset (Wu et al., 2023a), which
includes paired ABC notation and MIDI files, evaluated on
scales from 103 to 105.. The legend matches the scales 10^3 to 10^5. The 32-epoch axis matches Table 2, which lists 32 epochs.
- **agreement**, rendered page 7, axes: Panel (b) has an Epoch axis from 0 to 32, a Loss axis from 0.4 to 1.6, and a legend with bGPT^4, bGPT^5, and bGPT^6. One orange curve drops sharply near epoch 11–12.
  Paper quote: A significant improvement in the performance of bGPT5
occurred around epoch 11, as shown in Fig. 3b. The visible drop in the orange (bGPT^5) curve near epoch 11 matches the text's claim of an improvement around epoch 11.
- **agreement**, rendered page 7, rendered formulas: Table 5 columns are rendered as BPB with subscripts abc and midi under ABC→MIDI and MIDI→ABC headers. bGPT^5 has BPB_midi 0.0011 under ABC→MIDI.
  Paper quote: The bGPT5 model achieves an impressively low BPBmidi

of 0.0011 in ABC to MIDI conversion. The subscripts are rendered correctly, and the 0.0011 value matches the text.
- **agreement**, rendered page 7, captions: Table 4 shows BPB values of 0.4052, 0.3899 (bold), and 0.3900, and Acc values of 80.74, 84.66, and 85.26 (bold).
  Paper quote: Notably, bGPTlibri, pre-trained
on audio, achieves higher accuracy than bGPTimage on
spectrograms with speech content. The rendered values match the text: BPB is closely matched, and bGPT_libri has the higher accuracy.
- **agreement**, rendered page 7, units: The column header reads 'Acc (%)', with values such as 99.9702 and 99.9961.
  Paper quote: Both
bGPT5 and bGPT6 achieved near-perfect accuracies
(99.97% and 99.99%). The percent unit is consistent, and the text's figures are rounded versions of the table values.
- **agreement**, rendered page 6, captions: Caption names GPT2-small on AG News, ViT-B/16 on CIFAR-10, AST on Speech Commands v2; bGPT_signal = ImageNet+LibriSpeech, bGPT_mix = ImageNet+LibriSpeech+Wikipedia.
  Paper quote: bGPTsignal
combined the ImageNet and LibriSpeech datasets, while
bGPTmix integrated all three datasets.. The rendered caption is consistent with the model definitions in Section 5.2 and the baselines in Section 5.2.1.
- **agreement**, rendered page 6, sample counts: The column headers read AG News (4 classes), CIFAR-10 (10 classes) and Speech Commands v2 (36 classes). The rows list six bGPT variants plus Baselines.
  Paper quote: AG News (4 classes) CIFAR-10 (10 classes) Speech Commands v2 (36 classes). The rendered class counts match the extracted text. The six variants match the six models described in Section 5.2.
- **agreement**, rendered page 6, units: Each dataset has metric columns labelled BPB and Acc (%). Accuracy values fall in the percent range (76.73–98.13), and BPB values have no percent sign.
  Paper quote: Model BPB Acc (%) BPB Acc (%) BPB Acc (%). The rendered header units match the extracted header text. The accuracy cells fall in a plausible percent range.
- **agreement**, rendered page 6, captions: The table shows bGPT_wiki at 1.0639/92.49 and Baselines at 0.9237/94.50 for AG News. It shows bGPT_image at 88.69 vs a baseline of 98.13 for CIFAR-10, and bGPT_libri at 96.03 vs 98.11 for Speech Commands.
  Paper quote: scored 0.9237 BPB and 94.50% accuracy. The values cited in the page text match the rendered table cells, including the GPT2-small baseline of 0.9237 BPB and 94.50%.
- **agreement**, rendered page 6, captions: Bold entries are 1.0639 and 92.49 (AG News), 3.1234 and 88.69 (CIFAR-10), and 1.4818 and 96.03 (Speech Commands).
  Paper quote: excels in spoken content tasks compared to other variants.. Each bolded value is the best bGPT value in its column (lowest BPB, highest Acc). This is consistent with the text's claims about bGPT_libri and bGPT_wiki.
- **agreement**, rendered page 6, units: The text reads '32×32 BMP spectrograms' and 'converting 8KB audio files to 3KB images'.
  Paper quote: This process, converting 8KB audio files to
3KB images, inevitably leads to information loss.. These sizes are consistent with 8 kHz/8-bit/1 s WAV files (mean 8044 bytes in Table 1) and 32×32 24-bit BMP files (mean 3126 bytes).
- **agreement**, rendered page 4, rendered formulas: Rendered: b̂_{i,j} = Decoder_byte(Ê_i, b_{i,<j}), 1 ≤ j ≤ S, (5)
  Paper quote: ˆbi,j = Decoderbyte( ˆEi, bi,<j), 1 ≤ j ≤ S, (5). The rendered equation matches the extracted text once extraction noise is accounted for.
- **agreement**, rendered page 4, rendered formulas: Rendered: L_GEN(θ) = −Σ_{i=1}^{T−1} log p(b_{i+1}|b_1,...,b_i; θ), (6)
  Paper quote: LGEN(θ) =−
T −1X

i=1

log p(bi+1|b1, b2, ..., bi; θ), (6). The summation bounds from i=1 to T−1 are consistent with next-byte prediction over a sequence of length T.
- **agreement**, rendered page 4, rendered formulas: Rendered: L_CLF(θ) = −Σ_{k=1}^{K} y_k log p(y_k|B; θ), (7)
  Paper quote: LCLF(θ) =−
KX

k=1

yk log p(yk|B; θ), (7). The sum over K categories agrees with the definition of K as the total number of categories.
- **agreement**, rendered page 4, units: Text reads: WAV, 8000 Hz sampling rate, mono channel, 8-bit depth, one-second lengths; BMP 32×32, RGB, 24-bit depth.
  Paper quote: an 8000 Hz sampling
rate, mono channel, and 8-bit depth, each trimmed to one-
second lengths. Image data were set to BMP format with a
resolution of 32×32, RGB colour, and 24-bit depth.. The rendered values match the extracted text. They are also consistent with Table 1 mean file sizes of 8044 B (about 8000 bytes plus header) and 3126 B (32×32×3 = 3072 bytes plus header).
- **agreement**, rendered page 2, captions: Figure 1 shows .wav, .bmp (cat images), .mid (piano roll), .abc and .bin (chip labelled 0) inputs flowing into a central bGPT box, with outputs of an audio waveform, a 'Cat' label, sheet music, and chips labelled 1, 2, 3 … N. The caption reads 'The bGPT framework simulates digital systems through native binary data, and integrates diverse data types into a single model, treating everything as a byte sequence.'
  Paper quote: Figure 1. The bGPT framework simulates digital systems through native binary data, and integrates diverse data types into a single model,
treating everything as a byte sequence. This approach simplifies integration and expands application possibilities in the digital world.. The caption's rendered text matches the extracted text. The diagram's content is consistent with the caption: multiple data types go into one model, and the 0→1…N CPU-state chips represent digital-system simulation.
- **agreement**, rendered page 16, rendered formulas: A gray code block shows the header X:1, L:1/8, M:3/4, K:D. The body is written out without repeat signs and ends with 'dc d4 |]'.
  Paper quote: X:1
L:1/8
M:3/4
K:D
de f3 g | ag/<f/ e4 | AB =c3 d | BA/<G/ A4 | fg a3 g | fd e4 |. The rendered ABC block matches the extracted text. It has no '::' repeat markers, which agrees with the stated elimination of repeat signs.
- **agreement**, rendered page 17, sample counts: Page 17 states that the dataset comprises 2.1 million training entries and 21,000 evaluation entries.
  Paper quote: The dataset thus produced comprises 2.1 million entries for the training set and 21,000 entries for the evaluation set.. This matches Section 4.2, which reports 2.1 million instances, and Table 1, which lists 2.1 million CPU States files.
- **agreement**, rendered page 17, units: The page shows 1KB memory blocks paired with a 16-byte state sequence. The listed register sizes are PC 1 byte, ACC 1-byte, IR 4 bytes and general-purpose registers 10 bytes.
  Paper quote: The dataset comprises entries of 1KB memory blocks, each paired with a subsequent 16-byte sequence representing the. The rendered register sizes sum to 1+1+4+10=16 bytes. This matches the stated 16-byte state and the 1KB memory block described in Section 4.2.
- **agreement**, rendered page 17, sample counts: The page states that random instruction sequences vary in length from 1 to 256 and that there are over 516 million potential scenarios.
  Paper quote: in length from 1 to 256, with the effect of each instruction on the CPU state being recorded.. The 1 to 256 range matches Section 4.2. The figure of over 516 million matches the count of over 516 million scenarios in Section 5.3.2.
- **agreement**, rendered page 15, captions: Single-staff score in D major (two sharps), 3/4 time, tempo marking quarter = 120, measure numbers 7, 13, 19, 25, 30, with no repeat signs and an ending double barline. The caption reads 'Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.'
  Paper quote: Figure 5. Sheet music example corresponding to the MIDI of the same folk tune presented in Fig. 4.. The rendered caption matches the paper text. The time signature and key match the ABC header 'M:3/4' and 'K:D'. The absence of repeat signs matches the stated elimination of repeats in MIDI conversion.
- **mismatch**, rendered page 19, sample counts: The Address Variants column shows HLT=0 (1 variant); CLR, INC, DEC, SHL, SHR, ROL, ROR and NOT=0,1 (8×2=16); PUSH, POP and LOADI=1 (3); SWAP=1,2 (2); ADD, SUB, MUL, DIV, AND, OR and XOR=1,2,3 (7×3=21); MOV=2 (1). Together these list 44 address variants.
  Paper quote: These states include various instructions, totaling 21 unique
types with 43 variants. The variants rendered in Table 7 add up to 44, not the 43 stated in Section 4.2.
- **agreement**, rendered page 19, captions: The caption reads 'Table 7. Defined instruction set and the address variants of different instructions.' The page number 19 is shown.
  Paper quote: Table 7 (located on page 19) details the instruction set and the variants each instruction can have, depending on the values in
the address fields.. The caption, the table content and the page location match the Appendix B reference.
- **agreement**, rendered page 18, sample counts: The rendered trace shows states at steps 1 through 10, ending with IR: HLT and PC: 10. Together with step 0 on page 17, this gives 10 executed instructions.
  Paper quote: a randomly generated program for executing
10 instructions along with their corresponding states in human-readable form is provided below. The listed program has 10 instructions, ending in 'HLT'. The rendered states run PC 1 to 10, which matches the stated count.

Visual interpretation requires human confirmation.

## Visual comparison outcomes (reviewer audit)

| Outcome | Records |
|---|---:|
| Confirmed text-image agreement | 36 |
| Confirmed text-image mismatch (advisory) | 1 |
| Not applicable | 74 |
| Grounding failure: context, citation or readability | 2 |
| Missing or invalid confirmation | 3 |
| Conflicting assessments | 10 |
| Substantive uncertainty | 1 |
| Unresolved reason not recorded | 0 |

Counts are observations, not distinct figures or validated scientific claims. Not-applicable checks are not failed inspections. Grounding/confirmation failures are reviewer limitations, not paper defects. Legacy untyped reasons remain unspecified.


