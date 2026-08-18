# Benchmarks

> **Status: none built. This documents what exists and what is missing.**

## Existing benchmarks in the corpus

Relevant evaluation resources named by the corpus papers. **Availability is not verified** — check each paper for release status.

| Benchmark | Measures | Source |
|---|---|---|
| **MAST-Data** | 1600+ annotated MAS failure traces across 7 frameworks; 14 failure modes, κ=0.88 | `2503.13657` |
| **DeepHalluBench** | 100 hallucination-prone deep-research tasks incl. adversarial | `2601.22984` |
| **SYCON** | Sycophantic conformity in multi-turn dialogue | `2505.23840` |
| **ForesightSafety-TIDE** | Distributed fact recovery; 120 five-agent environments, paired honest/deceptive | `2608.03421` |
| **TrinityGuard** | MAS risk evaluation, 20 risk types, OWASP-grounded | `2603.15408` |
| **PMIYC** | Persuasion effectiveness and susceptibility | `2503.01829` |

Standard task sets used for reliability evaluation in these papers: GSMHard, MMLU-Hard (`2605.00914`), TruthfulQA, TriviaQA (`2606.07941`), MedQA-USMLE, MedThink-Bench (`2606.08457`), HotpotQA, MuSiQue (`2606.04435`), HaluEval (`2604.02923`), GAIA (`2602.16666`).

## What is missing

No benchmark in this corpus measures **propagation directly**. They measure outcomes — final accuracy, final hallucination rate — with the honourable exceptions of `2601.22984` (trajectory auditing) and `2608.03421` (lineage tracking).

A propagation benchmark would need:

1. **Ground truth at claim level**, not just final-answer level
2. **Injectable error seeds** of controlled type and detectability
3. **Provenance tracking** — which agent introduced which claim at which hop
4. **Paired conditions** — identical task with and without the seed (`2608.03421`'s design is the model here)
5. **Cost accounting** built into the harness, not bolted on

## Proposed: a minimal propagation benchmark

Design sketch, not a build.

**Tasks.** ~200 multi-hop factual questions with verifiable intermediate steps, so a claim can be labelled correct or incorrect at each hop.

**Seeds.** For each task, one atomic false claim, pilot-tested for detectability — neither obvious nor undetectable — with the detectability level *reported*.

**Conditions.** Paired: identical task run with `SeedType.NONE` and with the seed. Without the control arm, baseline error cannot be separated from seed-driven propagation.

**Metrics.** Adoption probability per hop, propagation depth, amplification factor, recovery rate, persistence after originator exit, cost.

**Reporting.** Per-condition, not aggregate. The corpus's central contradiction (amplification vs attenuation) is invisible in aggregate numbers.

## Rules

1. **Do not report results from a benchmark that has not been run.** This directory will stay empty until something is actually built.
2. **Publish the seeds and the task set** with any results, or the numbers are unreproducible.
3. **Report detectability calibration.** A benchmark with trivially-detectable seeds measures nothing.
4. **Always include the no-seed control arm.**
