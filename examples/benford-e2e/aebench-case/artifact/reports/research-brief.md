# Research brief: Empirical Validation of Benford's Law on a Real-World Public Dataset

## Research idea and motivation

Benford's Law (the first-digit law) states that in many naturally occurring collections of
numbers that span several orders of magnitude, the leading significant digit `d` is not
uniformly distributed but follows

    P(first digit = d) = log10(1 + 1/d),   d ∈ {1, …, 9}

so a leading `1` occurs about 30.1% of the time and a leading `9` only about 4.6%. The law
generalizes to the second digit and to digit pairs. It is widely used in forensic accounting,
election-fraud screening, and data-quality auditing precisely because *conforming* data has a
known, closed-form expected distribution.

Unlike a purely self-generated study, this artifact's input is a **real external dataset that
must be downloaded**: World Bank country/year population figures. **We empirically measure how
closely the leading-digit distribution of a real public dataset tracks the Benford prediction,
and we quantify conformity with standard, externally-defined test statistics.**

This is a small, fully reproducible, CPU-only study whose ground truth is a mathematical law —
an ideal candidate for artifact evaluation, since every reported number can be checked against
theory. It differs from a self-contained study in one important way: the evidence depends on an
**external data source**, so dataset provenance (source URL, retrieval, and checksum) is itself
part of what must be recorded and evaluated.

## External data source (must be downloaded and provenance-recorded)

- **Primary dataset:** World Bank total population by country and year.
  - **Pinned URL (immutable by commit):**
    `https://raw.githubusercontent.com/datasets/population/425fc447a53a26c767a15a7de60c4cc2478a0595/data/population.csv`
  - **Columns:** `Country Name, Country Code, Year, Value` (one row per country-year; `Value`
    is the population count — the quantity whose leading digits we analyze).
  - **Expected shape at time of writing:** 17,195 data rows.
  - **SHA-256 (record and verify after download):**
    `7d2dd6a17f5ed7916de1f89a9c116791e64d207f2e2f6ce47c57e1ab46f0088a`
  - **License/attribution:** World Bank Open Data via the `datasets/population` community
    package (record the source and license in the dataset provenance).

The pinned commit URL makes the download **reproducible**: the same bytes are fetched every
run. **Record the dataset's source URL, retrieval timestamp, row count, and SHA-256 checksum in
the artifact's dataset provenance so a reviewer can confirm the exact input.** Populations span
five to six orders of magnitude (from small territories to the world total), which is the regime
in which Benford's Law is expected to hold.

## Hypotheses

1. **Leading digits conform to Benford's Law.** The empirical first-digit distribution of the
   `Value` column tracks `log10(1 + 1/d)` with small deviation. Operationalize conformity with
   the **Mean Absolute Deviation (MAD)** of first-digit proportions and Nigrini's published MAD
   conformity ranges (close conformity < 0.006; acceptable < 0.012; marginal < 0.015;
   nonconformity ≥ 0.015), and report a Pearson chi-square goodness-of-fit statistic against the
   Benford expectation.

2. **Second-digit distribution also follows the generalized law.** The second significant digit
   `d2 ∈ {0, …, 9}` follows `P(d2) = Σ_{k=1}^{9} log10(1 + 1/(10k + d2))`, again within a small
   MAD.

3. **Negative control discriminates.** A synthetic control column of the same size drawn from a
   uniform distribution over a single order of magnitude does **not** conform (MAD well into the
   nonconformity range), demonstrating that the conformity test is discriminating rather than
   trivially accepting any input.

## Experimental approach

1. **Download and verify the dataset** from the pinned URL. Assert the SHA-256 matches the
   recorded value and record the row count; fail loudly if the checksum differs (this protects
   the reproducibility claim).

2. **Extract leading digits.** For every positive, finite `Value`, take the first significant
   digit (strip sign, leading zeros, and decimal point). Exclude zeros and non-finite/missing
   values and **report how many rows were excluded and why** (data-quality transparency).

3. **Compute the empirical distributions** for the first digit (1–9) and second digit (0–9), as
   proportions over the retained rows.

4. **Compare to theory** for each digit: expected Benford proportion, observed proportion,
   absolute deviation. Aggregate with MAD and a chi-square statistic (with the appropriate
   degrees of freedom), and classify conformity by Nigrini's MAD ranges.

5. **Negative control.** Generate a uniform-random control of the same length from a fixed seed,
   run the identical first-digit pipeline, and confirm nonconformity.

## What to record

- A first-digit results table: `digit (1–9)`, `observed_count`, `observed_proportion`,
  `benford_proportion`, `abs_deviation`.
- A second-digit results table: `digit (0–9)`, `observed_proportion`, `benford_proportion`,
  `abs_deviation`.
- Summary statistics: first-digit MAD, second-digit MAD, chi-square value (+ dof), the Nigrini
  conformity classification, total rows analyzed, and rows excluded (with reasons).
- The negative-control first-digit MAD (to contrast with the real data).
- Dataset provenance: source URL (pinned commit), retrieval timestamp, row count, SHA-256.

## Figures

- **Figure 1:** first-digit distribution — observed proportions (bars) overlaid with the
  Benford curve (line/points), digits 1–9 on the x-axis.
- **Figure 2:** second-digit distribution — observed vs. generalized-Benford expectation,
  digits 0–9 on the x-axis.

## Success criteria

1. The dataset is downloaded from the pinned URL and its SHA-256 is verified against the
   recorded checksum before any analysis runs.
2. A working, tested leading-digit extraction routine with unit tests (e.g., first digit of
   `54922` is `5`; of `0.0071` is `7`; zeros/blanks are excluded), plus deterministic behavior
   given the fixed input file and control seed.
3. A quantitative conformity result: first-digit MAD and chi-square with an explicit Nigrini
   conformity classification, and a clear statement of where the data conforms and where it
   deviates.
4. The negative control demonstrably fails the same conformity test (MAD in the nonconformity
   range), confirming the test discriminates.
5. The two figures above, generated from the recorded data.

## Hardware

Standard multicore CPU machine. **No GPU.** **Network is required once, to download the pinned
dataset**, after which the analysis is fully offline, in-process, and deterministic. Total
runtime budget: a couple of minutes.

## Constraints

- **Pure CPU, single machine.** Allowed libraries: the Python standard library plus `numpy`,
  `pandas`, `matplotlib`, `requests` (or `urllib`) for the one download.
- **Reproducibility:** the dataset is pinned by commit and verified by checksum; the control
  uses an explicit seed, so results are reproducible run-to-run.
- **Provenance first:** the artifact must record the external dataset's source, retrieval, row
  count, and checksum — the study is only as trustworthy as the recorded provenance of its
  external input.

## Target venue

A short empirical/reproducibility note (e.g., an experiments-and-analysis or data-audit track).
Two-column format; a standard ACM `acmart` template is fine if a `template/` directory is
provided.