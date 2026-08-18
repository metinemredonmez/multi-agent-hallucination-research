# Experiment 04 — Verifier Agent

> **Status: designed, not run. No results exist.**
>
> **⭐ Recommended first experiment.**

## Question

**RQ9:** What happens when the verifier shares the same false assumption as the generator?

Secondary: RQ8 (does verification help at all), RQ11 (prompt architecture effects).

## Why this is the priority

This is the **largest gap in the corpus** combined with the **lowest cost to run**.

`2603.24579` names the problem — LLM-as-judge verifiers suffer **confirmation bias**, "inadvertently reproducing the errors of the original generation" — and proposes deliberate information asymmetry (Solver / Proposer / Checker). But **no paper in this corpus measures verifier failure rate conditioned on the verifier inheriting the generator's premise.**

That is precisely the production configuration: the verifier is usually the same model family, handed the same context. The most common real-world setup is the least studied one.

## Method

1. Inject a false premise into the generator's context.
2. Have the generator produce output conditioned on it.
3. Run a verifier under **four** context conditions.
4. Measure what the verifier catches versus misses.

## The four arms

| Arm | Verifier sees | Tests |
|---|---|---|
| **A. Shared context** | Everything the generator saw, including the false premise | The production default |
| **B. Information-asymmetric** | Only the claim + independent evidence access, *not* the generator's reasoning | `2603.24579`'s proposed fix |
| **C. Different model family** | Same as A, but a different foundation model | Whether heterogeneity alone is enough |
| **D. Asymmetric + heterogeneous** | B and C combined | The predicted best case |

Arm A vs B is the core comparison. Arm C separates *model diversity* from *information diversity* — a distinction the literature tends to blur.

## Also test: verifier timing

From `2606.27409`, which derives a closed-form stability threshold and finds that correction which is **too strong or too delayed turns consensus into oscillation**, worst when communication and verification delays coincide.

| Variable | Levels |
|---|---|
| Verifier placement | none / terminal-only / per-transition |
| Verification delay | 0 / 1 / 2 hops |
| Correction strength | soft flag / hard reject / rewrite |

`2606.27409` predicts an unstable regime at delay 2 (threshold at the inverse golden ratio). **That is a falsifiable, quantitative prediction from a theoretical paper.** Testing it on real agents would be a genuine contribution — it has not been done.

## Metrics

| Metric | Definition |
|---|---|
| **Verifier failure rate under shared premise** | The RQ9 headline number |
| Verifier correction rate | Real errors caught |
| Verifier false-positive rate | Correct claims wrongly rejected |
| Delta between arms A and B | The size of the confirmation-bias effect |
| Oscillation onset | Does belief destabilize under strong/delayed correction? |
| Cost per corrected error | Is the verifier worth its tokens? |

**Report the false-positive rate.** A verifier that rejects everything scores perfectly on correction rate. Without the false-positive number, correction rate alone is meaningless — a trap several mitigation papers in this corpus do not clearly avoid.

## Predictions

- **P1.** Arm A (shared context) shows a substantially higher failure rate than Arm B. This is the confirmation-bias effect, quantified for the first time.
- **P2.** Arm C helps less than Arm B — *information* asymmetry matters more than *model* diversity. If true, this is a practical and slightly counterintuitive result, since swapping models is the more common advice.
- **P3.** Arm D is best but only marginally better than B.
- **P4.** Per-transition verification beats terminal-only, but with diminishing returns and a real cost penalty.
- **P5.** Some correction-strength setting produces *worse* accuracy than no verifier at all, via the oscillation mechanism of `2606.27409`.

**P5 is the most valuable prediction to test.** "A verifier can make things worse" is both practically important and currently unproven on real agents.

## Minimal first run

The cheapest useful version, if resources are tight:

- One task set, ~100 items with ground truth
- Arms A and B only
- Terminal verification only
- One model family
- Report: verifier failure rate A vs B, with a confidence interval

That single comparison already addresses an open question in the literature.
