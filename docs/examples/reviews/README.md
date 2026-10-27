# Example reviews (experimental, AI-generated)

> [!WARNING]
> **Experimental, AI-generated examples. No human judgement.** These reviews were produced
> automatically by an experimental reference implementation of the judge/reviewer
> specification. No person reviewed, edited, or endorsed them. They do not represent the
> opinion of the SDK maintainers, Microsoft, or any reviewer, and they are not assessments of
> the papers or their authors. They may contain errors. They are published only to show what
> the tool's output looks like.

> **Audience**: Readers of the judge/reviewer specification who want to see real output.
> **Source of truth for**: Nothing normative; these are illustrative examples. The
> specification in [`docs/judge-reviewer-spec/`](../../judge-reviewer-spec/README.md) governs.

Each example ran the paper adapter, the judge, and the reviewer on a public paper (the paper
only, no code), in the `artifact-informed` scope. In each directory, start with the README: it
links a one-page judge summary (claims, evidence, and verdicts) and gives a section-by-section
guide to the long review draft. The directories also hold the run's JSON outputs, the page
images the review cites, and the converted artifact.

| Example | Paper |
|---------|-------|
| [`bgpt/`](bgpt/README.md) | Wu et al., *Beyond Language Models: Byte Models are Digital World Simulators*, [arXiv:2402.19155v1](https://arxiv.org/abs/2402.19155v1) |
| [`lfmu/`](lfmu/README.md) | Foster, Schoepf, Brintrup, *Loss-Free Machine Unlearning*, [arXiv:2402.19308v1](https://arxiv.org/abs/2402.19308v1) |

Both papers are licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); quotations
from them are attributed to their authors. They are the spec's §8.7 conformance papers.
