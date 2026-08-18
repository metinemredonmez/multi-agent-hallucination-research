# Experiments

Minimal, provider-agnostic scaffolding for testing the working hypothesis in [`research/research-map.md`](../research/research-map.md).

> **Status: scaffolding only. No experiment has been run. No results exist in this repository.**
>
> Any number you find here is either transcribed from a cited paper or is an illustrative placeholder explicitly marked as such. There are no findings of our own yet.

---

## Design principles

1. **No heavy framework.** Plain Python, a provider abstraction, dataclasses. No orchestration library, because the orchestration *is* the object of study — using someone else's would bake in their assumptions.
2. **Provider-agnostic from day one.** `AgentSpec` names a provider and model; the runner does not care which. Anthropic / OpenAI / Gemini / local all sit behind one interface.
3. **Every claim carries provenance.** `origin_agent` and `hop_introduced` are recorded on every claim. Without them, propagation depth is not measurable at all.
4. **Trajectory, not just outcome.** Every hop is logged. Final-answer-only evaluation is exactly the methodology `2601.22984` criticizes.
5. **Cost is a first-class metric.** `2605.00914` found debate costing 2.1–3.4× more tokens for equal or worse accuracy. A reliability gain reported without its cost is not a result.
6. **No API keys in the repo.** Copy `.env.example` to `.env`. `.env` is gitignored.

---

## Architectures under comparison

**Architecture A — sequential chain**
```text
Agent A ──▶ Agent B ──▶ Agent C ──▶ Verifier
```
Each agent sees its predecessors' output as context. Verification is terminal.

**Architecture B — independent then adjudicate**
```text
Agent A ─┐
Agent B ─┼──▶ Independent Answers ──▶ Judge / Aggregator
Agent C ─┘
```
No peer visibility during generation.

Both are implemented by the same runner over different `Topology` values, so the comparison is controlled.

---

## The four experiments

| # | Name | Primary RQ | Key metric | Anchor papers |
|---|---|---|---|---|
| 01 | Error propagation | RQ2, RQ3, RQ7 | Adoption probability, amplification factor, propagation depth | `2603.04474`, `2608.03421`, `2606.07937` |
| 02 | Context drift | RQ13 | Context Divergence Score, semantic distance from goal | `2606.21666`, `2601.04170` |
| 03 | Consensus collapse | RQ4, RQ5, RQ15 | Oracle gap, modal adoption, inter-agent error correlation | `2605.00914`, `2602.09341` |
| 04 | Verifier agent | RQ8, RQ9 | Verifier correction rate, **failure rate under shared premise** | `2606.27409`, `2603.24579` |

**Recommended first experiment: 04.** See [`experiment-04-verifier-agent/README.md`](experiment-04-verifier-agent/README.md) — it targets the corpus's largest gap (RQ9) and is cheap to run.

---

## Metrics

Implemented in `framework/metrics.py`. Definitions and sources in [`research/research-map.md`](../research/research-map.md#5-metrics).

| Metric | Definition |
|---|---|
| `factual_accuracy` | Fraction of claims that are correct |
| `task_completion_accuracy` | Did the system produce the right final answer |
| `error_propagation_rate` | P(downstream agent adopts an upstream false claim) |
| `hallucination_amplification_rate` | final hallucination score ÷ initial (>1 amplify, <1 attenuate) |
| `context_drift` | Pairwise knowledge-state divergence (CDS-style) |
| `semantic_distance_from_goal` | Embedding distance, original goal vs operative objective at hop n |
| `consensus_accuracy` | Group answer correct |
| `false_consensus_rate` | Group agreed and was wrong |
| `oracle_gap` | pass@N − final group accuracy |
| `verifier_correction_rate` | Real errors the verifier caught |
| `verifier_failure_rate` | Real errors it missed |
| `token_cost`, `latency`, `agent_turns` | Cost accounting |

---

## Setup

```bash
cp .env.example .env
```

```bash
pip install -r requirements.txt
```

Provider SDKs are **not** pinned as hard dependencies — install only what you use.

---

## Running

> Provider adapters are stubs. `python -m framework.runner` currently exercises the wiring with the echo provider and produces **no research results**.

```bash
python -m framework.runner --help
```

---

## Honest reporting rules

Adopted from the corpus's better methodology:

1. **Report cost alongside accuracy.** Always (`2605.00914`).
2. **Compare against a strong single-agent baseline** — CoT and self-consistency at matched compute, not a naive one-shot (`2502.08788`).
3. **Report the oracle gap**, so aggregation failures are visible separately from generation failures (`2605.00914`).
4. **State what the comparison does not isolate.** `2608.00243` is the model here.
5. **Pre-register the metric.** Decide before running; do not select the flattering one afterwards.
6. **Publish negative results.** The most valuable papers in this corpus are negative (`2502.08788`, `2605.00914`, `2608.00243`).
