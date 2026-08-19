# Threat Model

A security view of multi-agent LLM systems: what the attack surface is, which attacks the corpus actually demonstrates, and where the evidence runs out.

> **Companion to** [`research-map.md`](research-map.md), which treats the same phenomena as *reliability* failures. This file treats them as *security* failures. That is not a rebrand — see §1.

---

## 1. Why this is a security document and not a reliability one

The corpus itself makes the case. **Four of the 40 papers are classified `cs.CR` (Cryptography and Security)** by their own authors:

| arXiv | Paper | Class |
|---|---|---|
| `2606.07937` | Hallucination Cascade | **cs.CR** |
| `2606.07941` | Collective Hallucination | **cs.CR** |
| `2603.15408` | TrinityGuard | **cs.CR** |
| `2607.26836` | Before Agents Speak | **cs.CR** |

The two most direct hallucination-cascade papers in this entire corpus were filed under **Security**, not `cs.AI` or `cs.CL`. That is a deliberate choice by their authors, and it is the clearest signal available that this problem is understood as a security problem by the people closest to it.

### The load-bearing insight

`2606.16710` establishes that misinformation propagates in **benign** multi-agent systems — no attacker required. Bad information enters from RAG, web search, model hallucination, agent misinterpretation, or noisy sources.

Combine that with `2603.04474`, which instantiates an **attack**: injecting a single atomic error seed produces widespread failure.

> **The same mechanism is both a naturally-occurring failure and a deliberately-inducible attack.**

This has a direct consequence that most agent-security writing misses:

- A system hardened only against *attackers* will still fail on its own, constantly.
- A system hardened only for *reliability* is already, incidentally, an attack surface — because the natural failure rate tells an attacker the exploit works.

**The controls are the same. The threat model must cover both.** That is this document's thesis.

---

## 2. Trust boundaries

The single most important security property of a multi-agent system:

> **Peer agent output is untrusted input.**

This is the classic "never trust user input" rule, relocated. It is violated by default in essentially every multi-agent framework, because a peer's message arrives in the next agent's context as ordinary text — indistinguishable from a user fact or a verified retrieval unless provenance is explicitly tracked.

`2608.03421` measures the consequence: **false testimony is adopted more readily than truthful testimony.** The trust boundary is not merely absent — the system is biased *against* the truthful side of it.

### The boundaries that need enforcing

| Boundary | Crossing it means | Enforcement |
|---|---|---|
| User → System | Goal definition | Immutable goal, restated per hop |
| Tool/Retrieval → Agent | External data enters reasoning | Evidence IDs, provenance labels |
| **Agent → Agent** | **Peer claim enters context** | **Claims marked as hypotheses, not facts** |
| Agent → Memory | Claim becomes durable state | Verified-only writes |
| Agent → Tool/Action | Belief becomes action | Human confirmation for irreversible actions |

The **Agent → Agent** row is the one this corpus is about, and the one no mainstream framework enforces.

The **Agent → Tool/Action** row is where epistemic failure becomes operational damage. `2602.16666` documents real incidents: an AI assistant deleting a production database despite instructions forbidding it, an agent making an unauthorized purchase that bypassed user confirmation, a government chatbot giving illegal advice.

---

## 3. Attack classes

Each class below is graded by what the corpus actually **demonstrates**, not what is plausible.

| Grade | Meaning |
|---|---|
| 🔴 **Demonstrated** | A paper implemented the attack and measured its effect |
| 🟠 **Evidenced** | The mechanism is measured; weaponization is a short step not taken in the paper |
| 🟡 **Plausible** | Follows from corpus findings; **not demonstrated anywhere here** |
| ⚫ **Out of corpus** | Real attack class, **no supporting paper in this corpus** |

---

### A1 — Error seed injection 🔴 Demonstrated

**Attack.** Inject one atomic false claim into a collaborative system and let its own message-passing distribute it.

**Evidence.** `2603.04474` explicitly "instantiates an attack where injecting just a single atomic error seed leads to widespread failure." It models collaboration as a directed dependency graph and identifies three vulnerability classes: **cascade amplification**, **topological sensitivity**, **consensus inertia**.

**Cost to attacker.** One claim. That is the entire payload.

**Mitigation with measured effect.** The paper's genealogy-graph governance layer, implemented as a message-layer plugin, **prevents final infection in at least 89% of runs** — without altering the collaboration architecture. This is the single most concrete defensive result in the corpus.

---

### A2 — False testimony / deceptive participant 🔴 Demonstrated

**Attack.** One agent holding key evidence reports it falsely.

**Evidence.** `2608.03421` pairs all-honest collaboration against controlled deception by a key evidence holder across 120 five-agent environments. **Truth recovery falls from 72.50% to 14.17%.**

**Three properties that make this severe:**

1. False testimony is **adopted more readily** than truthful testimony
2. It **propagates to higher orders** — second- and third-hand repetition
3. It **persists through honest agents after the deceiver exits**

**Property 3 is the security-critical one.** Ejecting the malicious agent does **not** remediate the system. The belief has been copied into the state of honest participants. Any incident response that assumes "remove the compromised component" is sufficient will fail here.

**Partial mitigation, honestly reported.** Observers without first-hand evidence *suppress* incorrect consensus but do **not** improve truth recovery. Adding watchers reduces the wrong answer without producing the right one.

---

### A3 — Sycophancy exploitation 🟠 Evidenced

**Attack.** Do not compromise the system's reasoning — compromise its *social* dynamics. Present a false claim confidently, or appear to be the majority.

**Evidence.** `2605.00914` measures the exploitable quantities in homogeneous debate:

- **Modal adoption up to 85.5%** — agents adopt the majority answer
- **Contextual fragility up to 70.0%** — peer rationales destabilize *previously correct* reasoning
- **Conformity is already high at K=2** — minimal peer exposure

**Why K=2 matters for security.** An attacker does not need to control a majority of agents, or many of them. Two influencing inputs are enough to move conformity substantially. This dramatically lowers the bar compared to classical Byzantine assumptions, where safety is usually stated in terms of controlling under a third or half of participants.

**Related.** `2503.01829` (PMIYC) frames susceptibility to persuasion explicitly as "a critical alignment challenge, raising questions about robustness, safety." `2606.24976` documents sycophantic conformity in long-horizon agentic persuasion.

---

### A4 — Consensus manipulation 🟠 Evidenced

**Attack.** Steer the group toward a biased or false consensus and let the aggregation rule ratify it.

**Evidence.** `2608.02827` predicts and observes a **phase transition** to collective bias when conformity exceeds a critical threshold, with **noise (e.g. sampling temperature) as a key driver**. A finite-size crossover consistent with the transition was observed.

**The security reading:** temperature is a *configuration* parameter. If a phase transition to collective bias is driven by noise, then a deployment-time setting — often chosen for output diversity with no security review — is a control surface for consensus integrity.

**Compounding factors.** `2602.09341`'s **confabulation consensus** means agents with correlated priors reach the same wrong answer with **no conformity required** — so enforcing independence does not close this. `2605.00914`'s **oracle gap up to 32.3 pp** means the correct answer can be present in the pool and discarded by voting.

---

### A5 — Memory and context poisoning 🟡 Plausible

**Attack.** Get a false claim written into durable memory, where it is re-read as established fact across turns or sessions.

**Evidence.** `2606.24976` identifies **semantic leakage in standard RAG** as a *reproducible trigger* for compounding failure: an early bad assumption "quietly contaminates memory writes" and surfaces steps later. `2606.21666` shows stale or mismatched shared state producing hallucination independent of model quality.

**Why only 🟡.** No paper in this corpus demonstrates *deliberate* memory poisoning, measures how long contamination persists, or tests whether rollback removes downstream effects. The mechanism is evidenced; the attack is not.

**This is the corpus's thinnest area** — see [`open-research-questions.md` RQ12](open-research-questions.md#rq12-if-agent-memory-is-contaminated-how-many-turns-does-the-error-persist). Given `2608.03421`'s persistence-after-exit result, the expectation should be that contamination outlives naive cleanup.

---

### A6 — Verifier subversion 🟡 Plausible

**Attack.** Defeat the control rather than the system: ensure the verifier shares the generator's false premise, or manipulate verification timing.

**Evidence.**
- **Confirmation bias** — `2603.24579` establishes that LLM-as-judge verifiers "inadvertently reproduce the errors of the original generation." Its fix is deliberate **information asymmetry** (Solver / Proposer / Checker).
- **Timing as an attack surface** — `2606.27409` derives a closed-form stability threshold and finds correction that is **too strong or too delayed turns consensus into oscillation**, with the most unstable regime when communication and verification delays coincide.

**The availability angle.** An attacker who can influence verification *timing or strength* may be able to destabilize belief without ever injecting a false fact — closer to a denial-of-integrity than a data attack. `2606.27409` shows the instability is specific to signed-belief tasks; **grounded factual answering makes truth an absorbing boundary and eliminates the effect.** Grounding is therefore a defense against this class, not merely an accuracy improvement.

**Why only 🟡.** Nobody has measured verifier failure rate *conditioned on the verifier inheriting the generator's premise* — which is the production default. See [RQ9](open-research-questions.md#rq9-what-happens-when-the-verifier-shares-the-same-false-assumption).

---

### A7 — Topology and contagion exploitation 🟠 Evidenced

**Attack.** Target the communication graph — position a compromised or unreliable agent where propagation is maximal.

**Evidence.** `2607.21912` models an LLM agent network with an explicit epidemic formulation (susceptible / exposed / infectious / corrected) and derives an **early-invasion condition** for heterogeneous networks, validated over 21,000 simulated trajectories.

**The uncomfortable structural result:** reliability and error control impose **opposing graph constraints**, and the paper characterizes when their feasible intersection is **empty** — configurations where you cannot be both connected enough to aggregate well and sparse enough to contain errors.

**Defensive counterpart.** `2505.23352` finds **moderately sparse** topologies optimal — suppressing error propagation while preserving beneficial diffusion. Topology is a security control, tunable at design time.

`2606.27409` adds the placement half: a supermodular objective with a greedy (1−1/e)-approximation for assigning a limited corrector budget to influential nodes. **Where you put your verifiers is an optimization problem with a known approximation guarantee.**

---

### A8 — Prompt injection ⚫ Out of corpus

**Attack.** External content — a retrieved page, a document, a tool result — carries text that the agent treats as instructions rather than data.

**Corpus status: NOT COVERED.**

> ### ⚠️ Explicit gap
>
> **No paper in this 40-paper corpus studies prompt injection.** The corpus covers *error and misinformation propagation between agents*; it does not cover *instruction hijacking from external content*.
>
> These are genuinely different: A1–A7 concern a false **claim** being believed, whereas prompt injection concerns a false **instruction** being obeyed. They interact — an injected instruction can plant a claim that then cascades via A1 — but the corpus contains no evidence about the first step.
>
> **Do not cite this corpus as evidence about prompt injection.** Acquiring prompt-injection literature is the **top priority for the security track** (see §6).

The closest adjacent items are `2603.15408` (TrinityGuard's inter-agent communication threat tier) and `2606.24976` (semantic leakage in RAG) — neither is a prompt-injection study.

---

## 4. Defensive controls

Controls with evidence in this corpus, strongest first.

| Control | Effect | Source | Confidence |
|---|---|---|---|
| **Message-layer lineage governance** | Prevents final infection in **≥89%** of runs | `2603.04474` | High — measured against a real attack |
| **Model heterogeneity** | "Universal antidote"; breaks correlated failure | `2502.08788` | High — 5 methods × 9 benchmarks × 4 models |
| **Moderately sparse topology** | Suppresses propagation, preserves useful diffusion | `2505.23352` | High |
| **Evidence-aware aggregation** (not voting) | +5 pp over majority vote, +3 pp over LLM-as-Judge | `2602.09341` | Moderate — modest absolute gains |
| **Grounded verification** | Makes truth an absorbing boundary; removes oscillation | `2606.27409` | Moderate — analytic + 5 open models |
| **Information-asymmetric verifiers** | Counters verifier confirmation bias | `2603.24579` | Moderate — proposed, not ablated here |
| **Interaction-aware control stack** | Up to **39%** hallucination reduction; caps adversarial amplification at 1.08 vs 1.45 | `2606.07941` | Moderate |
| **Optimal corrector placement** | Greedy (1−1/e) approximation under budget | `2606.27409` | Moderate — theoretical |
| **Pre-hoc risk inference** | Estimates failure risk *before* interaction | `2607.26836` | Low-moderate |
| **Structural auditing** (graph geometry) | Early warning before semantic visibility | `2603.13325` | Low-moderate — workshop paper |
| **Prompt-level protocols** (GDP) | Cohen's d = **+1.43 to +1.99** on reasoning alignment | `2606.08457` | Moderate — medical QA only |

### Controls with *no* evidence here — do not assume they work

- **Provenance labelling** (marking peer claims as hypotheses). Recommended throughout this repository and by common sense; **never measured in this corpus.** It is a hypothesis, and experiment-01 is designed to test it.
- **Rollback / context purging.** `2608.03421`'s persistence-after-exit result is direct evidence that naive versions of this are **insufficient**.
- **Adding more reviewer agents.** `2608.03421` found observers suppress incorrect consensus without improving truth recovery.

---

## 5. Frameworks and standards

**`2603.15408` (TrinityGuard)** is the corpus's only systematic safety framework. Grounded in **OWASP standards**, it provides a three-tier risk taxonomy identifying **20 risk types**:

1. Single-agent vulnerabilities
2. **Inter-agent communication threats**
3. **System-level emergent hazards**

Tiers 2 and 3 are exactly where cascade attacks live, and they are the tiers that single-agent security tooling does not cover. Code is public: `https://github.com/AI45Lab/TrinityGuard`.

> **TODO — needs verification.** Map A1–A8 above onto the current OWASP Top 10 for LLM Applications and onto MITRE ATLAS. Both have been revised recently; **do not write specific item identifiers from memory.** Verify against the published lists before publishing any mapping.

---

## 6. Security research gaps

Priority order for the security track:

1. **Prompt injection — corpus coverage is zero.** Acquire the literature before making any claim in this area. (§A8)
2. **Deliberate memory poisoning.** Never demonstrated here; persistence never measured. (A5, RQ12)
3. **Verifier inheriting the attacker's premise.** The production default, unmeasured. (A6, RQ9)
4. **Attacker cost curves.** No paper reports how many compromised agents, or how much influence, is needed for a given success rate. `2605.00914`'s K=2 conformity result hints the bar is low; nobody has mapped it.
5. **Rollback and remediation.** `2608.03421` shows removing the source is insufficient. Nothing here measures what *is* sufficient.
6. **Inter-agent error correlation as a security metric.** Never reported as a coefficient — yet it directly quantifies how much independent redundancy a defense actually has. (RQ15)

---

## 7. Practical checklist

Derived from the above. Items marked **[unvalidated]** follow from corpus findings but are not themselves measured here.

**Trust boundaries**
- [ ] Peer agent output is labelled as hypothesis, never as fact **[unvalidated]**
- [ ] Claims carry `origin_agent` and `hop_introduced` so propagation is traceable **[unvalidated]**
- [ ] Only verified claims are written to durable memory **[unvalidated]**
- [ ] Irreversible actions (payments, deletions, sends) require human confirmation

**Architecture**
- [ ] Agents are heterogeneous where feasible — `2502.08788`
- [ ] Topology is moderately sparse, not fully connected — `2505.23352`
- [ ] Aggregation reads evidence rather than counting votes — `2602.09341`
- [ ] Verifiers have information asymmetry from generators — `2603.24579`
- [ ] Verification is grounded in external evidence, not peer belief — `2606.27409`

**Monitoring**
- [ ] Claim lineage is logged — `2603.04474`
- [ ] Inter-agent error correlation is tracked (redundancy is real, not nominal)
- [ ] Confidence is *not* treated as a reliability signal — `2608.00243`
- [ ] Consensus is *not* treated as a correctness signal — `2605.00914`, `2602.09341`

**Incident response**
- [ ] Assume removing a compromised agent does **not** remediate — `2608.03421`
- [ ] Contaminated downstream state is identified and re-derived, not just deleted
- [ ] Sampling temperature is treated as a security-relevant setting — `2608.02827`
