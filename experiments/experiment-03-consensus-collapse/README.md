# Experiment 03 — Consensus Collapse

> **Status: designed, not run. No results exist.**

## Question

**RQ5:** Is majority voting reliable? **RQ15:** Are agents from the same foundation model genuinely independent?

Secondary: RQ4 (why incorrect consensus forms), RQ10 (independent-first reasoning).

## Why this matters

Two distinct failures are routinely conflated:

- **Consensus collapse** — the right answer *was in the pool* and voting discarded it. An **aggregation** problem. `2605.00914` measured an oracle gap up to **32.3 pp**.
- **Confabulation consensus** — agents shared priors and were *all* wrong. A **generation** problem. Named by `2602.09341`.

They demand opposite fixes, so separating them is the point of this experiment.

Additionally: **no paper in this corpus reports an inter-agent error-correlation coefficient directly**, despite it being the single number that answers RQ15 and being cheap to compute.

## Method

1. Run N agents on a shared item set with ground truth.
2. Record every agent's individual answer **before** any aggregation.
3. Apply several aggregation rules to the *same* candidate pool.
4. Compute the oracle gap: was a correct answer available and discarded?

Applying multiple aggregators to one pool is what isolates aggregation from generation.

## Conditions

| Variable | Levels |
|---|---|
| Agent count | 3 / 5 / 10 |
| Models | homogeneous / heterogeneous |
| Peer visibility | independent / peer-visible |
| Rounds | 1 / 3 |
| Aggregation | majority / confidence-weighted / evidence-ledger |
| Temperature | 0.4 / 0.7 / 1.0 |

**Temperature is included deliberately:** `2608.02827` identifies noise as a key driver of the phase transition to collective bias. This design can test for that crossover.

## Metrics

| Metric | Source |
|---|---|
| **Oracle gap** = pass@N − final group accuracy | `2605.00914` |
| **Inter-agent error correlation** (pairwise, on which items) | **Corpus gap — nobody reports this** |
| Modal adoption rate | `2605.00914` |
| Vulnerability rate (correct → incorrect after peer exposure) | `2605.00914` |
| False consensus rate | — |
| Confidence–correctness correlation | `2608.00243` |
| Token cost per correct answer | `2605.00914` |

## Predictions

- **P1.** Oracle gap is substantial (>10 pp) for homogeneous majority voting.
- **P2.** Inter-agent error correlation is **high** for same-model agents (Jaccard > 0.5) and markedly lower cross-model. This is the headline number.
- **P3.** Confidence–correctness correlation is weak (`2608.00243` found self-reported confidence "only weakly predictive").
- **P4.** Independent-first reduces modal adoption but does **not** reduce error correlation — because confabulation consensus needs no conformity. If P4 holds, independence alone is insufficient and heterogeneity is required.

**P4 is the most informative prediction here**, because it distinguishes the two failure modes cleanly.

## Confounds

- **Ties.** Define tie-breaking in advance; ties are common with small N and silently bias results.
- **Answer normalization.** Semantically identical answers phrased differently will register as disagreement. Normalize before voting, and report how.
