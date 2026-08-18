# Experiment 02 — Context & Goal Drift

> **Status: designed, not run. No results exist.**

## Question

**RQ13:** How is goal drift measured in long-running multi-agent systems?

Secondary: RQ12 (memory contamination persistence).

## Why this matters

There is **no validated goal-drift metric in this corpus.** `2601.04170` proposes the Agent Stability Index but is simulation-based and theoretical. `2606.21666` proposes the Context Divergence Score with n=30 per condition in two planning domains. Neither has been independently replicated.

Building a *validated* drift metric is therefore a genuine contribution, not a reproduction.

## Method

1. Define tasks with an explicit, checkable goal and a set of hard constraints (e.g. "plan a trip under $2000 that avoids overnight flights").
2. Run for a long horizon (20+ turns) — drift is a function of horizon length.
3. At each hop, capture the agent's *operative* objective, not just its output.
4. Measure distance from the original goal, and constraint retention.

## Metrics

| Metric | Definition | Status |
|---|---|---|
| Semantic distance from goal | Embedding distance, original goal vs operative objective at hop n | **Proposed here — unvalidated** |
| Constraint retention rate | Fraction of original constraints still honoured at hop n | **Proposed here — unvalidated** |
| Context Divergence Score | Pairwise knowledge-state divergence | `2606.21666` — one paper, unreplicated |
| Agent Stability Index | 12-dimension composite | `2601.04170` — **simulation-based** |
| Contaminated rounds | Turns for which corrupted memory stays readable | Adapted from `2606.24976` |

### ⚠️ Validation requirement

**Do not report these metrics without validating them against human judgment first.** An embedding distance that does not correlate with a human's sense of "this agent has gone off track" measures nothing. Recommended: have annotators rate drift on a sample of trajectories, then report the metric–human correlation *before* any headline result.

This is the step `2601.04170` skipped, and the reason its numbers cannot be cited as evidence.

## Conditions

| Variable | Levels |
|---|---|
| Horizon | 5 / 10 / 20 / 40 turns |
| Goal restatement | every turn / every 5 turns / only at start |
| Memory | isolated / shared raw / shared verified |
| Context policy | full broadcast / selective / verified-only |

The **goal restatement** arm directly tests prompt-contract requirement #1 (immutable goal). It is cheap to run and has an obvious practical payoff.

## Predictions

- **P1.** Drift grows with horizon, but non-linearly — expect an inflection, not a straight line.
- **P2.** Goal restatement every turn substantially reduces drift. Cheapest intervention available.
- **P3.** Constraint retention degrades *faster* than semantic distance grows — constraints are dropped silently while topic stays roughly on track. If so, semantic distance alone is an inadequate drift metric.
- **P4.** Shared raw memory drifts more than verified-only memory.
