# Experiment 01 — Error Propagation

> **Status: designed, not run. No results exist.**

## Question

**RQ3:** How does one agent's error get adopted and amplified by downstream agents — and *what determines the direction*?

Secondary: RQ2 (does agent count help or hurt), RQ7 (does context sharing contaminate).

## Why this matters

This targets the corpus's central contradiction. `2606.07937` measured net **attenuation** (amplification factor 0.644) across 3-agent chains. `2603.04474` measured a single atomic error seed causing widespread failure. `2608.03421` measured truth recovery collapsing 72.50% → 14.17%.

Both outcomes are real. Nobody has published a unified account of the conditions that select between them. That is the gap.

## Method

Adapted from `2603.04474`: inject one atomic error seed, then measure its spread.

1. Build a task set with verifiable ground truth (so claims can be labelled).
2. Inject exactly **one** false claim at hop 0.
3. Run the chain.
4. At every subsequent hop, record whether the seed was restated, challenged, or dropped.

**Controlled seed types** (`SeedType`): factual, instruction, tool output, stale state. Plus a `NONE` control arm — without it, a baseline drift rate cannot be separated from seed-driven propagation.

## Conditions

| Variable | Levels |
|---|---|
| Agent count | 1 / 3 / 5 |
| Topology | chain / star / mesh / sparse |
| Context policy | full broadcast / selective / verified-only |
| Models | homogeneous / heterogeneous |
| Provenance labelling | peer claims labelled as hypotheses / unlabelled |
| Seed type | factual / instruction / tool / stale / none |

The **provenance labelling** arm is the novel one. Labelling peer output as a hypothesis rather than a fact is widely recommended and, as far as this corpus shows, **never measured**.

## Metrics

| Metric | Source |
|---|---|
| Adoption probability (per hop) | `2608.03421` |
| Amplification factor (final ÷ initial) | `2606.07937` |
| Propagation depth | `2603.04474` |
| Recovery rate, time-to-correction | — |
| Persistence after originator exit | `2608.03421` exit ablation |
| Token cost, latency, turns | `2605.00914` |

## Predictions

Stated in advance so they can be wrong.

- **P1.** Adoption is higher for seeds phrased confidently than hedged ones.
- **P2.** Mesh > chain > sparse for propagation rate (from `2505.23352`).
- **P3.** Provenance labelling reduces adoption, but by less than expected — labels are easy to ignore once a claim is in context.
- **P4.** Heterogeneous chains attenuate more than homogeneous ones (from `2502.08788`).
- **P5.** Amplification factor is **not** consistently >1 — this experiment should reproduce *both* directions depending on condition. If it only ever amplifies, suspect the task design.

## Confounds to control

- **Seed detectability.** A blatantly false seed is trivially caught. Pilot for a seed difficulty that is neither obvious nor undetectable, and report it.
- **Position effects.** Later agents have more context *and* more chances to correct. Vary seed position, don't fix it at hop 0.
- **Verbosity.** Substring-based adoption detection rewards verbose agents. Use entailment matching before reporting.
