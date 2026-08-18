# Literature Review

A synthesis of the 40-paper corpus. Organized by *argument*, not by paper.

> **Scope and limits.** This review is written from each paper's **title page and abstract**, verified against the PDFs. Full texts have not yet been read end to end. Numbers are transcribed from the papers' own abstracts and have not been independently reproduced. Statements marked `TODO` are open work, not findings.

---

## 1. Corpus composition

| Dimension | Breakdown |
|---|---|
| **Total** | 40 papers |
| **2023–2024 (foundations)** | 6 — `2305.14325`, `2308.07201`, `2309.13007`, `2406.03075`, `2406.11776`, `2410.12853` |
| **2025 (turn toward critique)** | 8 — `2502.08788`, `2503.01829`, `2503.13657`, `2505.23352`, `2505.23840`, `2509.18970`, `2511.07784`, `2511.11182` |
| **2026 (current wave)** | 26 |
| **Surveys** | 3 — `2509.18970`, `2607.26212`, `2604.23505` |
| **Experimental** | ~30 |
| **Theoretical / simulation** | 3 — `2601.04170`, `2607.21912`, `2606.27409` (hybrid) |
| **Non-peer-reviewed** | at least 1 — `2604.02923` (self-described technical report) |

### The arc of the field

The corpus tells a clear three-act story, and this is the backbone of any article written from it:

**Act I — Optimism (2023–2024).** `2305.14325` establishes multiagent debate as a factuality improvement, invoking "society of minds." `2308.07201`, `2309.13007`, `2410.12853`, `2406.11776` build the design space: judging, heterogeneity, confidence weighting, sparse topology.

**Act II — Systematic doubt (2025).** `2502.08788` runs a fair evaluation and finds MAD often loses to single-agent baselines at higher cost. `2503.13657` builds the first validated failure taxonomy from 1600+ real traces. `2511.07784` asks whether debate is deliberation at all, or merely ensembling.

**Act III — Mechanism (2026).** The field stops asking *whether* multi-agent systems fail and starts modelling *how*: propagation dynamics (`2603.04474`), network contagion (`2607.21912`), phase transitions (`2608.02827`), verification stability thresholds (`2606.27409`), trajectory-level auditing (`2601.22984`).

**The article's thesis follows from this arc**: the question has moved from "are more agents better?" to "what protocol determines whether an agent network corrects or compounds its errors?"

---

## 2. Argument 1 — Hallucination becomes a system property

**Claim.** In multi-agent systems the unit of analysis must shift from the *response* to the *trajectory*.

**Support.** `2606.07937` tracks claim-level inconsistency across sequential interactions rather than scoring final outputs. `2601.22984` makes the methodological argument explicitly: end-to-end evaluation "obscures intermediate hallucinations that accumulate throughout the research trajectory," and proposes auditing the full plan–search–summarize trajectory (PING taxonomy: **P**ropagation, **I**ntent, **N**oise-induced, **G**rounding). `2606.07941` models hallucination as a time-evolving process over a network. `2604.23505` generalizes: uncertainty is "transformed and reused" across component boundaries and persistent state.

**Strength: strong.** Four independent papers converge on trajectory-level analysis. This is the corpus's most robust methodological consensus.

---

## 3. Argument 2 — Cascade direction is a variable, not a constant

**This is the corpus's central contradiction, and the most intellectually important thing in it.**

| Finding | Paper | Direction |
|---|---|---|
| Hallucination score 0.422 → 0.272 across 3 hops; amplification factor **0.644**; accuracy also fell 0.789 → 0.769 | `2606.07937` | **Attenuation** |
| Single atomic error seed → widespread failure; vulnerability classes: cascade amplification, topological sensitivity, consensus inertia | `2603.04474` | **Amplification** |
| Truth recovery 72.50% → 14.17% under one deceptive evidence holder | `2608.03421` | **Amplification** |
| Amplification 1.45 undefended vs 1.08 with adaptive control | `2606.07941` | **Both — control-dependent** |

**How to reconcile.** These are not contradictory results so much as different *conditions*. `2606.07937` studied heterogeneous models in an unseeded natural setting — later agents had genuine opportunity to correct. `2603.04474` and `2608.03421` *deliberately injected* an error and measured its spread. `2606.07941` shows the same system going either way depending on whether adaptive control is present.

**The synthesis:** an agent network is an error-control system that can run in either direction. Refinement stages *can* filter noise (attenuation); shared context and correlated priors *can* lock errors in (amplification). Which one dominates is determined by the protocol — topology, grounding, heterogeneity, verification.

**⚠️ Do not write "multi-agent systems amplify hallucination" as an established fact.** The most direct measurement in this corpus says the opposite in its setting. This nuance is what separates a serious article from a hype piece.

---

## 4. Argument 3 — Agreement is not evidence

**Claim.** Consensus among LLM agents carries far less information than it appears to.

**Three independent mechanisms:**

1. **Sycophantic conformity** (`2605.00914`) — modal adoption up to **85.5%**; contextual fragility destabilizes previously correct reasoning at up to **70.0%**. Critically, conformity is already high at **minimal** peer exposure (K=2) and *intensifies with greater initial diversity*.
2. **Confabulation consensus** (`2602.09341`) — agents with correlated priors independently reach the same wrong rationale. **No conformity is required**, which means independence does not fix it.
3. **Phase transition** (`2608.02827`) — collective bias emerges when conformity crosses a critical threshold; noise (sampling temperature) is a key driver; a finite-size crossover consistent with the predicted transition was observed.

**And agreement can be actively misleading.** `2606.08457`'s **consistency illusion**: debate *reduced* detectable contradictions while simultaneously *decreasing* the semantic similarity of reasoning chains. Agents appeared to agree more while reasoning less consistently. `2608.00243` adds that second-round arguments add little semantic novelty and self-reported confidence is only weakly predictive of correctness.

**Consequence for aggregation.** `2605.00914` measured an **oracle gap up to 32.3 pp** — the correct answer was present in the pool and voting discarded it. `2602.09341` replaced voting with reasoning-tree auditing for **+5 pp** over majority vote and **+3 pp** over LLM-as-Judge.

**Strength: strong.** Six papers, multiple mechanisms, quantified.

---

## 5. Argument 4 — Topology is a safety primitive

**Claim.** How agents are wired determines whether errors spread, independently of how good the agents are.

**Support.** `2505.23352` provides the cleanest result: **moderately sparse** topologies — suppressing error propagation while preserving beneficial information diffusion — achieve optimal task performance. `2406.11776` established the sparse-communication result earlier. `2607.21912` formalizes the tension: reliability and error control impose **opposing graph constraints**, and their feasible intersection can be **empty**; under a fixed sender budget the propagation threshold is independent of density, meaning *the communication-budget convention itself* determines whether adding edges is risky. `2603.04474` identifies topological sensitivity as one of three vulnerability classes. `2603.13325` monitors topology geometry (Ollivier–Ricci curvature) to detect cascading risk *before* it becomes semantically visible.

**Strength: strong**, with one caveat — `2607.21912` is analytic and simulation-based, not measured on live LLM agents.

---

## 6. Argument 5 — Verification is necessary but conditional

**Claim.** Adding a verifier does not automatically improve reliability; *when*, *how strongly*, and *how independently* it verifies all matter.

**Support for verification.** `2606.07941` (up to 39% hallucination reduction), `2603.24579` (MARCH), `2602.09341` (+5 pp), `2604.02923` (41.7% relative reduction, *technical report*), `2601.04742` (tool grounding).

**The conditions.**
- **Timing/dose** — `2606.27409` derives a closed-form stability threshold: correction that is too strong or too delayed turns consensus into **oscillation**, worst when communication and verification delays coincide. But grounded factual answering makes truth an **absorbing boundary**, eliminating the effect — grounded verification remains stabilizing.
- **Independence** — `2603.24579` identifies verifier **confirmation bias**: LLM-as-judge verifiers "inadvertently reproduce the errors of the original generation." Its fix is deliberate **information asymmetry** (Solver / Proposer / Checker).
- **Pre-hoc vs post-hoc** — `2607.26836` argues post-hoc detection is structurally too late, and predicts risk from role–task semantic misalignment *before* interaction.

**Strength: moderate.** The positive results are numerous; the conditions are established by fewer papers. RQ9 (verifier inheriting the same premise) remains largely unmeasured.

---

## 7. Argument 6 — Heterogeneity is the most reliable single lever

**Claim.** Of all interventions in this corpus, model heterogeneity has the most consistent positive evidence.

**Support.** `2502.08788` — heterogeneity is a "**universal antidote**" consistently improving MAD frameworks (the strongest evidence: 5 methods × 9 benchmarks × 4 models). `2604.02923` — 41.7% relative hallucination reduction from a heterogeneous council. `2309.13007`, `2410.12853` — foundational diversity results. The mirror image: `2602.09341` and `2608.00243` show homogeneous panels failing through correlated error.

**Caveats.** `2604.02923` is a self-described technical report with unusual author listing and no institutional affiliation — weigh accordingly. `2410.12853` appeared in *Journal of Robotics and Automation Research*, a venue whose review standards should be checked, and its PDF carries **no arXiv stamp** (its arXiv ID is unconfirmed).

**Strength: moderate-to-strong**, resting mainly on `2502.08788`.

---

## 8. Argument 7 — Prompt architecture is a first-class control

**Claim.** Prompt and role design measurably affect cascade risk — more than the "prompting isn't enough" reflex suggests.

**Support.** `2606.08457`'s **Grounded Debate Protocol** is a purely prompt-level intervention (agents must commit to named facts and take explicit stances on peers' claims) producing alignment improvements of **Cohen's d = +1.43 to +1.99** — a large effect. `2607.26836` shows fine-grained semantic misalignment between agent **roles** and task **queries** is predictive of hallucination risk *before any interaction*. `2503.13657`'s taxonomy places "system design issues" as one of three top-level failure categories.

**The honest framing.** Prompting is **necessary but not sufficient**. `2606.08457` shows it can produce large gains; `2503.13657` and `2607.21912` show topology, verification, and memory are independent levers that prompting cannot substitute for.

**Strength: moderate** — one strong direct result, one predictive result.

---

## 9. Argument 8 — Contamination does not require an adversary

**Claim.** The cascade problem is a property of ordinary collaborative systems, not an attack scenario.

**Support.** `2606.16710` is the key paper: misinformation propagates in **benign** multi-agent systems, where bad information arises from RAG, web search, model hallucination, agent misinterpretation, or noisy sources — no malicious actor. `2606.24976` identifies **semantic leakage in standard RAG** as a reproducible trigger for compounding failure. `2503.13657`'s 1600+ traces are ordinary framework runs, not attacks.

**The adversarial results still matter as upper bounds.** `2608.03421` (deliberate deception) and `2603.04474` (injected error seed) establish worst-case dynamics — and `2608.03421`'s finding that a false claim **persists through honest agents after its source exits** is the mechanism that makes benign contamination hard to undo.

**Strength: strong**, and important for framing: this is a reliability-engineering problem, not primarily a security problem.

---

## 10. Contradictions to preserve, not resolve

A serious article should present these tensions rather than flattening them:

| Tension | Side A | Side B |
|---|---|---|
| Cascade direction | `2606.07937` — net attenuation (0.644) | `2603.04474`, `2608.03421` — amplification, collapse |
| Does debate help? | `2305.14325`, `2309.13007` — yes | `2502.08788`, `2605.00914`, `2608.00243` — often no |
| Is more context safer? | Intuition, full-broadcast designs | `2505.23352` — moderately sparse wins; `2606.21666` — naive sync causes drift |
| Does verification help? | `2606.07941`, `2603.24579` — yes | `2606.27409` — bad timing causes oscillation; `2603.24579` — verifier confirmation bias |
| Is prompting enough? | `2606.08457` — large prompt-only effects | `2503.13657`, `2607.21912` — independent structural levers |

---

## 11. Methodological quality notes

Weigh these when citing:

**Highest rigor.** `2503.13657` — 1600+ annotated traces, 7 frameworks, expert annotators, κ=0.88, strong institution (UC Berkeley). `2502.08788` — 5 methods × 9 benchmarks × 4 models. `2602.16666` — multi-provider, ~24-month longitudinal, strong authors (Narayanan, Kapoor).

**Treat with caution.**
- `2601.04170` (Agent Drift) — **simulation and theory only**, single independent researcher, hedged abstract ("could lead to", "theoretical analysis suggesting"). Excellent *vocabulary*, not empirical evidence.
- `2604.02923` (Council Mode) — self-described **technical report**, not peer-reviewed; author list gives degree titles rather than affiliations; currently v4.
- `2410.12853` — journal venue whose standards should be checked; **arXiv ID unconfirmed from the document**.
- `2607.21912`, `2606.27409` — analytic/simulation models; conclusions depend on modelling assumptions.
- `2603.13325` — workshop paper (lighter review).

**Commendable self-limitation.** `2608.00243` explicitly notes its reference and panel use different model variants, so its results "characterize the complete systems rather than isolate a causal debate effect." That honesty is worth emulating.

---

## 12. What the corpus does not cover

See `open-research-questions.md` for the full treatment. In brief:

1. **Memory contamination** — n=1 (`2606.24976`), persuasion domain only
2. **Goal drift** — no dedicated paper; only simulation-based semantic drift
3. **Independence × heterogeneity** — the interaction cell is untested
4. **Cost-normalized comparison** — only `2605.00914` reports it properly
5. **Verifier inheriting the generator's premise** — named but not measured
6. **Inter-agent error correlation** — never reported as a direct coefficient, despite being cheap to compute and central to RQ15

---

## 13. Reading order

**Start here (12 papers):**

1. `2503.13657` — Why Do Multi-Agent LLM Systems Fail? *(empirical grounding, highest rigor)*
2. `2606.07937` — Hallucination Cascade *(the direct paper — and the attenuation result)*
3. `2603.04474` — From Spark to Fire *(error seeds, propagation dynamics)*
4. `2605.00914` — The Cost of Consensus *(the richest quantified failure metrics)*
5. `2608.03421` — When Truth Is Distributed *(adoption, persistence after exit)*
6. `2502.08788` — Stop Overvaluing Multi-Agent Debate *(the fair-evaluation counterweight)*
7. `2602.09341` — Auditing Reasoning Trees *(confabulation consensus; beyond majority vote)*
8. `2606.27409` — Delayed Verification *(verifier timing and placement)*
9. `2505.23352` — Communication Topologies *(the topology result)*
10. `2606.21666` — Hallucination as Context Drift *(drift as a measurable quantity)*
11. `2606.08457` — The Consistency Illusion *(agreement ≠ alignment; prompt intervention works)*
12. `2602.16666` — Towards a Science of AI Agent Reliability *(why any of this matters)*

**Then the surveys for breadth:** `2509.18970` (agent hallucination taxonomy), `2607.26212` (MAD design space, 141 studies).
