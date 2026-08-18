# Terminology

The vocabulary in this field is inconsistent. The 2026 MAD survey (`2607.26212`) explicitly identifies "inconsistent terminology and no rigorous synthesis" as a core problem. This file fixes a working vocabulary for this repository.

## How to read this file

Each concept below has five fields:

| Field | Meaning |
|---|---|
| **Definition** | What the term means here |
| **Distinguished from** | The nearest neighbouring concept and the line between them |
| **How it appears in MAS** | The concrete mechanism in a multi-agent system |
| **Measurable metrics** | How you would actually put a number on it |
| **Related papers** | Corpus papers that study it |

**Source discipline.** Where a definition is taken from a paper, the arXiv ID is given. Where a definition is *this repository's own working construction*, it is marked **[WORKING DEFINITION — no single authoritative source]**. That distinction is deliberate: several of these terms are in active use without a settled academic definition, and pretending otherwise would be exactly the kind of unsupported claim this project studies.

---

## The one-line separation

Before the detail, the distinctions that matter most:

- **Hallucination** is about *truth*. A claim is unsupported.
- **Propagation** is about *movement*. The claim travels to another agent.
- **Drift** is about *distance*. The system's state or goal has moved away from where it started.
- **Consensus failure** is about *agreement*. The group settled on the wrong thing.
- **Cascading failure** is about *consequence*. Something in the world broke.

A system can hallucinate without propagating, propagate without drifting, drift without consensus failure, and fail catastrophically from an error that was never a hallucination at all. Collapsing these into one word is the most common analytical mistake in this area.

---

## 1. Single-Agent Hallucination

**Definition.** One model, in one output, produces a fluent claim that is unsupported by its input, its evidence, or the facts. The unit of analysis is a **single response**.

Taxonomies of the subtypes (factual, faithfulness, reasoning, tool-use, instruction-following) are given in the agent-hallucination survey `2509.18970`, which organizes them by *where in the agent workflow* they occur.

**Distinguished from.** Multi-agent hallucination: the difference is not the content of the error but the **unit of analysis**. Single-agent hallucination is a property of an output. Everything below is a property of a *trajectory* or a *system*.

**How it appears in MAS.** As the seed. Every cascade in this corpus starts with either a hallucinated claim or an injected false one.

**Measurable metrics.**
- Claim-level factual inconsistency rate
- Groundedness / entailment against provided evidence
- Per-response hallucination score (e.g. the normalized score used in `2606.07937`)

**Related papers.** `2509.18970` (taxonomy by workflow stage), `2406.03075` (detection via structured debate).

---

## 2. Multi-Agent Hallucination

**Definition.** An umbrella term for hallucination phenomena whose explanation requires more than one agent. **[WORKING DEFINITION]** — used in this repo as a category header, not as a precise mechanism. When you need precision, use one of the specific terms below (cascade, collective, false consensus, context drift).

**Distinguished from.** Single-agent hallucination, by unit of analysis. Note the important negative case established by `2606.21666`: some multi-agent hallucination "cannot be explained by model deficiencies alone" — it arises from *state divergence between agents*, meaning the individual agents may each be functioning correctly.

**How it appears in MAS.** Output that no single agent would have produced alone.

**Measurable metrics.** Not directly measurable — decompose into a specific mechanism first.

**Related papers.** `2509.18970`, `2606.21666`, `2606.07941`.

---

## 3. Hallucination Cascade

**Definition.** A hallucination produced at one stage is consumed as *context* by a later stage, so subsequent reasoning is conditioned on it. Analysis is at the level of a **trajectory**, and the key variable is **cascade depth**.

The direct source is `2606.07937`, which tracks claim-level factual inconsistency across sequential agent interactions and defines an **amplification factor** = final error / initial error.

**Distinguished from.**
- *Error propagation* — cascade is the narrower case where the propagating item is a hallucinated claim and each hop conditions the next. Propagation is the general phenomenon.
- *Collective hallucination* — cascade is directional and sequential (A→B→C). Collective hallucination is mutual and reinforcing.

**⚠️ Important correction to the intuitive story.** The name suggests errors always grow. **The direct evidence is more mixed.** `2606.07937` measured a normalized hallucination score *dropping* from 0.422 to 0.272 across 3-agent chains — amplification factor **0.644**, i.e. net *attenuation* — while factual accuracy *also* fell (0.789 → 0.769). Meanwhile `2603.04474` shows a single injected atomic error seed causing widespread failure, and `2608.03421` shows truth recovery collapsing 72.50% → 14.17%.

The honest reading: **cascade direction is a variable, not a constant.** Whether an error amplifies or attenuates depends on topology, grounding, heterogeneity, and verification — which is precisely what this repository sets out to test. Do not write "cascades amplify errors" as an established fact.

**How it appears in MAS.** Agent 1's unsupported premise appears in Agent 2's prompt as ordinary context, indistinguishable from user-provided fact unless provenance is explicitly tracked.

**Measurable metrics.**
- **Amplification factor** = final hallucination score / initial (>1 amplify, <1 attenuate) — `2606.07937`
- **Propagation depth** — how many hops an error survives
- **Adoption probability** — chance a downstream agent accepts an injected false claim
- **Recovery rate** and **time-to-correction**

**Related papers.** `2606.07937` (direct), `2606.04435` (agentic RAG variant + 4-type cascade taxonomy), `2603.04474` (error seeds), `2601.22984` (trajectory auditing, "Propagation" as a taxonomy class).

---

## 4. Error Propagation

**Definition.** The general movement of any error — factual, reasoning, tool-output, or stale-state — through a multi-agent workflow along message dependencies. `2603.04474` models this as a **directed dependency graph**.

**Distinguished from.** Hallucination cascade is a *subtype* (propagating item = hallucinated claim). Error propagation also covers a wrong tool result, a bad retrieval, or a stale state value — none of which are hallucinations.

**How it appears in MAS.** Along message-passing edges. `2607.21912` models it explicitly as an epidemic process (susceptible → exposed → infectious → corrected).

**Measurable metrics.**
- Per-edge transmission / adoption rate
- Early-invasion threshold (`2607.21912`)
- Infection rate across runs (`2603.04474` reports its governance layer preventing final infection in ≥89% of runs)
- Topology sensitivity: error rate as a function of graph sparsity (`2505.23352`)

**Related papers.** `2603.04474`, `2607.21912`, `2505.23352`, `2406.11776`, `2604.23505` (uncertainty as the propagating quantity), `2606.16710`, `2603.13325`.

---

## 5. Context Drift

**Definition.** Divergence of **internal knowledge state** between concurrently operating agents — mismatched or stale representations of shared world state (different environmental assumptions, asynchronous updates, inconsistent task histories). Source: `2606.21666`.

**Distinguished from.**
- *Goal drift* — context drift is about the **facts/state** agents hold; goal drift is about the **objective** they pursue. An agent can hold perfectly current state and still pursue the wrong goal, and vice versa.
- *Memory contamination* — context drift is *divergence* (agents disagree about state); contamination is *corruption* (agents agree on state that is wrong).
- *Hallucination* — the key claim of `2606.21666` is that context drift **causes** output that looks like hallucination, without any agent being individually deficient.

**How it appears in MAS.** Agent A acts on a plan step that Agent B has already invalidated; neither is wrong given what it knows.

**Measurable metrics.**
- **Context Divergence Score (CDS)** — pairwise knowledge-state discrepancy across spatial, temporal, task dimensions (`2606.21666`)
- Rate of contradiction between concurrent agent outputs
- State staleness (hops since last synchronization)

**Related papers.** `2606.21666` (primary), `2601.04170` (semantic drift), `2604.23505`.

---

## 6. Goal Drift

**Definition.** The system progressively optimizes for an objective that differs from the original user goal, even while each individual step looks locally reasonable. **[WORKING DEFINITION — no paper in this corpus defines "goal drift" under that exact name.]**

The closest sourced concept is **semantic drift** in `2601.04170`: "progressive deviation from original intent." `2606.24976` reports "severe problem drift" in long-horizon subjective tasks. If you need a citable term, use *semantic drift* (`2601.04170`) or *problem drift* (`2606.24976`) and note that "goal drift" is this repo's umbrella phrasing.

**Distinguished from.**
- *Context drift* — state vs objective (see above).
- *Agent drift* — goal drift is one *manifestation*; agent drift is the broader behavioural envelope.

**How it appears in MAS.** Task decomposition where each sub-agent optimizes its local sub-goal; the composition no longer serves the original request. Reinforced when the original goal is not restated in each agent's context.

**Measurable metrics.**
- **Semantic distance from the original goal** — embedding distance between the user's stated goal and the system's operative objective at hop *n*
- Constraint retention rate — fraction of original constraints still honoured at step *n*
- Sub-goal / original-goal alignment score

**Related papers.** `2601.04170` (semantic drift — note: **simulation-based**, treat as proposed not demonstrated), `2606.24976` (problem drift), `2607.26836` (role–task semantic misalignment as a *pre-hoc* risk signal).

---

## 7. Agent Drift

**Definition.** Progressive degradation of agent behaviour, decision quality, and inter-agent coherence over extended interaction sequences. Source: `2601.04170`, which decomposes it into three types:

| Type | Meaning |
|---|---|
| **Semantic drift** | Progressive deviation from original intent |
| **Coordination drift** | Breakdown in multi-agent consensus mechanisms |
| **Behavioral drift** | Emergence of unintended strategies |

**⚠️ Evidence caveat.** `2601.04170` is theoretical and simulation-based, by a single independent researcher, and its own abstract is hedged ("could lead to", "theoretical analysis suggesting"). The **vocabulary** is useful; the **quantitative claims are not empirical evidence**.

**Distinguished from.** Goal drift and context drift are each narrower. Agent drift is specifically about **degradation over time / interaction length** — the independent variable is horizon length.

**How it appears in MAS.** Long-running systems where behaviour at turn 100 differs systematically from turn 5.

**Measurable metrics.**
- **Agent Stability Index (ASI)** — composite over 12 dimensions incl. response consistency, tool usage patterns, reasoning pathway stability, inter-agent agreement (`2601.04170`)
- Behaviour delta between early and late turns
- Human intervention rate over time

**Related papers.** `2601.04170` (primary), `2606.24976`, `2602.16666` (reliability over long horizons).

---

## 8. Collective Hallucination

**Definition.** Multiple agents mutually reinforce the same unsupported claim, so that apparent agreement makes the result look *more* credible than any single agent's output would. Modeled in `2606.07941` as a system-level, time-evolving process over a network, where hallucinated claims diffuse through the communication topology and intensify under adversarial perturbation.

**Distinguished from.**
- *Hallucination cascade* — cascade is sequential and directional; collective hallucination is **mutual and recursive**. Cascade: A→B→C. Collective: A↔B↔C, each reinforcing the others.
- *False consensus* — collective hallucination describes the *shared false belief*; false consensus describes the *agreement mechanism* that selects it. Closely coupled, often co-occurring, but a group can reach false consensus on a claim only one agent ever believed.

**How it appears in MAS.** Dense mesh debate where each round increases confidence without adding evidence. `2608.00243` found second-round arguments "add little semantic novelty" — agreement rising while information does not.

**Measurable metrics.**
- Confidence trajectory vs accuracy trajectory (divergence = collective hallucination signature)
- Amplification under adversarial perturbation (`2606.07941` reports 1.08 with adaptive control vs 1.45 without)
- Semantic novelty added per debate round

**Related papers.** `2606.07941` (primary), `2603.15408` (group-hallucination framing), `2608.02827`.

---

## 9. Consensus Failure

**Definition.** The group's agreement process produces a wrong output. **[WORKING DEFINITION — umbrella term.]** Use it as the general category, and prefer the two specific mechanisms below when you can identify which one occurred.

**Distinguished from.** It is the *outcome*; sycophancy, confabulation consensus, and consensus collapse are the *mechanisms* that produce it.

**Measurable metrics.** False consensus rate; group accuracy vs best-single-agent accuracy.

**Related papers.** All of §10–§12.

---

## 10. Consensus Collapse

**Definition.** The aggregation step **discards a correct answer that was already present in the candidate pool**. Source: `2605.00914`, which measures it as the **oracle gap** — the difference between "at least one agent was right" and "the group's final answer was right." Reported oracle gap: **up to 32.3 percentage points**.

**Distinguished from.**
- *Collective hallucination* — in collapse the right answer **existed and was thrown away**. In collective hallucination no agent had it. This is the sharpest and most useful distinction in this file, because the two demand opposite fixes: collapse is an **aggregation** problem, collective hallucination is a **generation/grounding** problem.
- *Consensus failure* — collapse is one specific mechanism of it.

**How it appears in MAS.** Plurality voting over agents whose errors are correlated. A lone correct minority agent is outvoted.

**Measurable metrics.**
- **Oracle gap** = pass@N (any agent correct) − final group accuracy (`2605.00914`)
- Minority-correct-but-overruled rate
- Aggregation regret vs an oracle selector

**Related papers.** `2605.00914` (primary, quantified), `2602.09341` (AgentAuditor beats majority vote by up to 5 pp precisely by rescuing evidence-based minority answers), `2608.00243`.

---

## 11. Sycophancy / Sycophantic Conformity

**Definition.** An agent abandons a correct or well-supported position because another party is more persuasive, more authoritative, or represents the apparent majority — prioritizing agreement over accuracy.

`2605.00914` measures it in agent-to-agent debate as **modal adoption rate**: up to **85.5%**. It pairs this with **contextual fragility** — peer rationales destabilizing previously *correct* reasoning, vulnerability rate up to **70.0%**.

**⚠️ A distinction worth preserving.** The classic sycophancy literature (`2505.23840`, SYCON benchmark) measures **model-to-user** conformity. This repo cares about **agent-to-agent** conformity. These are plausibly related but *not the same measurement*, and transfer between them is an assumption to test — not an established result.

**Distinguished from.**
- *Consensus collapse* — sycophancy is an agent **changing its own belief**; collapse is the **voting rule** discarding a belief that was never abandoned.
- *Persuasion susceptibility* (`2503.01829`) — essentially the same phenomenon measured from the persuader's side.

**How it appears in MAS.** Round 2 of a debate, where an agent that answered correctly in round 1 switches to the majority. Notably, `2605.00914` found conformity already high at **minimal** peer exposure (K=2) — you do not need a large crowd to induce it.

**Measurable metrics.**
- **Modal adoption rate** — how often an agent switches to the majority answer (`2605.00914`)
- **Vulnerability rate** — correct→incorrect switches after peer exposure (`2605.00914`)
- **Flip rate** conditioned on whether the peer was right or wrong (the diagnostic ratio: switching toward correct peers is *good*)
- SYCON benchmark scores (`2505.23840`)

**Related papers.** `2605.00914`, `2505.23840`, `2503.01829`, `2606.24976`.

---

## 12. Confabulation Consensus

**Definition.** Agents sharing **correlated biases** converge on the same *incorrect rationale* — so agreement carries no independent information. Source: `2602.09341`.

**Distinguished from.** This is the *mechanism* that makes majority voting unsafe. Sycophancy is agents *changing* to match each other; confabulation consensus is agents *independently arriving* at the same wrong answer because they share priors. Critically: **no conformity is required.** Three instances of one model can produce it while never seeing each other's output.

**How it appears in MAS.** Homogeneous panels. `2608.00243` found "self-reported confidence is only weakly predictive of correctness" in exactly this setting.

**Measurable metrics.**
- **Inter-agent error correlation** — the central quantity for RQ14/RQ15
- Diversity of failure modes across agents
- Homogeneous vs heterogeneous accuracy delta (`2502.08788` identifies heterogeneity as a "universal antidote")

**Related papers.** `2602.09341` (names it), `2608.00243`, `2502.08788`, `2604.02923`, `2309.13007`.

---

## 13. Misinformation Propagation

**Definition.** The spread of false information through an agent network. Distinguished from hallucination cascade by the **origin** of the falsehood: misinformation may enter from retrieval, web search, a noisy source, a misinterpreting agent, or a deceptive agent — not necessarily from a model's own confabulation (`2606.16710`).

**Two threat models, kept separate:**

| | Origin | Corpus source |
|---|---|---|
| **Benign** | RAG, web search, model hallucination, agent misinterpretation, noisy sources. No malicious actor. | `2606.16710` |
| **Adversarial** | A deliberately deceptive agent or injected error seed. | `2608.03421`, `2603.04474` |

The benign case is the one that matters for ordinary production systems, and `2606.16710` is the paper that makes it explicit that **no attacker is required**.

**A key finding worth isolating.** `2608.03421`: a single false testimony is **adopted more readily than truthful testimony**, propagates to higher orders, and **persists through honest agents after the deceiver exits**. Truth recovery fell 72.50% → 14.17%. This is the mechanism behind why rollback is hard: removing the source does not remove the belief.

**Measurable metrics.**
- Testimony adoption rate, split by true vs false
- Evidence-root lineage depth (`2608.03421`)
- Persistence after source removal (exit ablation)
- Truth recovery rate

**Related papers.** `2606.16710` (benign), `2608.03421` (adversarial + persistence), `2603.04474`, `2607.21912`.

---

## 14. Memory Contamination

**Definition.** Incorrect information is written into shared or persistent memory and subsequently re-read as established fact by the same or other agents. The corruption outlives the conversation turn that produced it. **[WORKING DEFINITION]**

The closest direct source is `2606.24976`, which describes how in long-horizon runs "an early bad assumption quietly contaminates memory writes," surfacing many steps later. It identifies **semantic leakage in standard RAG** as a reproducible trigger.

**⚠️ Corpus gap.** This is the **thinnest-supported concept in this repository** — only one paper (`2606.24976`) treats memory-write contamination as its primary mechanism, and it does so in the persuasion domain. See `open-research-questions.md`.

**Distinguished from.**
- *Context drift* — contamination is agents agreeing on **wrong** state; drift is agents **disagreeing** about state.
- *Hallucination cascade* — cascade travels through the *message* channel within a task; contamination travels through the *storage* channel and can cross task boundaries and sessions.

**How it appears in MAS.** A summarization or memory-write step promotes an unverified intermediate claim into durable state. Later retrieval returns it with no provenance, so it is indistinguishable from a verified fact.

**Measurable metrics.**
- Contaminated-rounds count — turns for which corrupted memory remains readable
- Persistence after source removal (`2608.03421`'s exit ablation, adapted)
- Rollback completeness — does removing a claim actually remove its downstream effects?
- Fraction of memory writes lacking provenance

**Related papers.** `2606.24976` (primary), `2608.03421` (persistence mechanism), `2606.21666`.

---

## 15. Cascading Failure

**Definition.** A local epistemic error becomes an **operational** failure: wrong tool call, wrong plan, bad code, unsafe action, or system-level task failure. The transition point is where a *belief* problem becomes an *action* problem.

**Distinguished from.** Everything above is epistemic — about what the system *believes*. Cascading failure is about what the system *does*. This distinction matters for severity: a false belief that never reaches an actuator may cost nothing; the same belief driving a tool call can be unrecoverable.

`2602.16666` grounds this with real incidents: an AI assistant deleting a production database despite instructions forbidding it, an agent making an unauthorized purchase bypassing user confirmation, a government chatbot giving illegal advice.

**How it appears in MAS.** The final hop, where accumulated false context reaches a tool, an API, or a user decision.

**Measurable metrics.**
- Task completion accuracy (not just factual accuracy)
- **Failure severity** — graded, not binary success/fail
- Incidence of unsafe or irreversible actions
- Human intervention rate

**Related papers.** `2602.16666` (reliability vs accuracy, real incidents), `2503.13657` (14 empirical failure modes, κ=0.88), `2603.15408` (20-type risk taxonomy incl. system-level emergent hazards), `2603.13325`.

---

## Terms this repository deliberately does NOT use as established

| Term | Status |
|---|---|
| **Epistemic Cascade** | This repo's own editorial umbrella phrase. Not established terminology. Label it as a framing device if used in the article. |
| **Goal drift** | Widely used informally; **no corpus paper defines it under this name**. Cite `2601.04170` semantic drift or `2606.24976` problem drift instead. |
| **Multi-agent hallucination** | Useful category header, not a mechanism. Decompose before making claims. |
| **Memory contamination** | Real phenomenon, thin corpus support (n=1). Flag as under-evidenced. |
| **Consensus failure** | Umbrella. Prefer *consensus collapse* / *confabulation consensus* / *sycophantic conformity*. |

---

## Claims that must NOT be made without qualification

Drawn from the corpus's own contradictions:

1. ~~"Cascades always amplify errors."~~ — `2606.07937` measured net **attenuation** (amplification factor 0.644).
2. ~~"More agents means more reliability."~~ — `2502.08788`: MAD often fails to beat single-agent CoT / Self-Consistency at higher cost.
3. ~~"Majority voting is a reliable aggregator."~~ — `2605.00914` (oracle gap 32.3 pp), `2602.09341` (confabulation consensus).
4. ~~"A verifier agent solves hallucination."~~ — `2603.24579` (verifier confirmation bias), `2606.27409` (badly-timed correction causes oscillation).
5. ~~"Three agents are three independent sources."~~ — `2602.09341`, `2608.00243`, `2502.08788`.
6. ~~"Debate improves reasoning."~~ — `2606.08457`: debate *reduced* contradictions while *decreasing* reasoning-chain similarity (the consistency illusion).
7. ~~"Sharing full context is safer."~~ — `2505.23352`: *moderately sparse* topologies performed best; `2607.21912`: reliability and error control impose opposing graph constraints.
