# Security Article Outline

**Working title:**
> **Your Multi-Agent System Has an Insider Threat Problem — And It Doesn't Need an Attacker**

**Alternatives:**
- *One Claim Is the Whole Payload: Attacking Multi-Agent LLM Systems*
- *Peer Agent Output Is Untrusted Input*
- *Why Removing the Malicious Agent Doesn't Fix Anything*

**Target:** security engineers, AI platform teams, red teamers. ~2,000–3,000 words.

**Relationship to the other article.** [`article-outline.md`](article-outline.md) covers the same phenomena as *reliability* failures for a general engineering audience. This one is the **security cut** for a security audience. They share a corpus and must not contradict each other. Write the reliability piece first if publishing both — this one lands harder once "consensus is not evidence" is established.

---

## ⚠️ Writing rules

Beyond the rules in [`article-outline.md`](article-outline.md#writing-rules-for-this-article), this article has four of its own:

1. **Do not claim this corpus covers prompt injection. It does not.** Zero of 40 papers. If prompt injection is mentioned, say explicitly that the evidence comes from elsewhere — and then actually cite elsewhere. This is the easiest way to discredit the piece.
2. **Do not inflate 🟡 Plausible into 🔴 Demonstrated.** [`threat-model.md`](../research/threat-model.md#3-attack-classes) grades every attack class. Memory poisoning and verifier subversion are *plausible*, not demonstrated. Say so.
3. **Do not cite OWASP or MITRE ATLAS item numbers from memory.** Both lists have been revised. Verify against the published list or omit the identifiers.
4. **Do not describe the contents of the video in [`media-sources.md`](../sources/media-sources.md).** It has not been watched. Cite it as motivation, not as a source.

---

## The hook

Lead with the finding that breaks a standard security assumption:

> In a controlled study of five-agent systems, one agent lying dropped collective truth recovery from **72.50% to 14.17%**.
>
> Then the researchers removed the liar.
>
> The false belief **kept propagating through the honest agents anyway.**

*(`2608.03421`)*

That is the article. Everything else explains why it happens and what to do.

---

## Structure

### 1. The assumption security teams are making
Agent systems are treated as software with an LLM inside: secure the endpoints, sanitize the inputs, sandbox the tools. That is necessary and insufficient, because it misses the channel that matters — **what agents tell each other**.

Keep this short. Do not lecture a security audience on security.

### 2. Peer output is untrusted input
The article's central reframe, and one that needs no new vocabulary for this audience:

> Every multi-agent framework violates "never trust user input" by default — it just calls the untrusted input "context."

A peer's claim arrives in the next agent's prompt as ordinary text, indistinguishable from a user fact or verified retrieval unless provenance is tracked. Almost nothing tracks provenance.

And the bias runs the wrong way: `2608.03421` found **false testimony is adopted more readily than truthful testimony.**

Use the trust-boundary table from [`threat-model.md` §2](../research/threat-model.md#2-trust-boundaries).

### 3. It's a vulnerability *and* a bug — same mechanism
The insight that distinguishes this piece. `2606.16710` shows misinformation propagating in **benign** systems — no attacker, bad data arriving from RAG, search, or an agent's own misreading. `2603.04474` shows the *same* mechanism weaponized.

> The natural failure rate is the attacker's proof-of-concept.

Consequence: reliability hardening and security hardening are the same work here. A security team that ignores the reliability literature is ignoring its own threat intel.

### 4. One claim is the whole payload
`2603.04474` "instantiates an attack where injecting just a single atomic error seed leads to widespread failure," with three named vulnerability classes: cascade amplification, topological sensitivity, consensus inertia.

**The economics are the story.** Payload size: one claim. No exploit chain, no memory corruption, no credential. The system's own message-passing is the delivery mechanism.

### 5. You don't need to control the majority
Classical Byzantine framing assumes safety while an attacker controls under some fraction of nodes. That intuition does not transfer.

`2605.00914`: modal adoption **up to 85.5%**, contextual fragility **up to 70.0%**, and conformity **already high at K=2 peers**.

> Two influencing inputs. Not a third of the network. Two.

Then the deeper problem — `2602.09341`'s **confabulation consensus**: agents with correlated priors reach the same wrong answer with *no conformity at all*. Enforcing independence does not fix it.

> Three agents on one foundation model are not three votes. They are one vote, sampled three times. Your quorum is nominal.

### 6. Removing the attacker doesn't remediate
Back to the hook, now with the mechanism. `2608.03421`: false claims propagate to higher orders and persist through honest agents after the deceiver exits.

**Incident response implications** — this is the section practitioners will act on:
- "Remove the compromised component" is insufficient
- Contaminated downstream state must be identified and **re-derived**, not just deleted
- Without claim-level lineage, you cannot even enumerate what to re-derive
- Observers help less than expected: `2608.03421` found they suppress incorrect consensus **without improving truth recovery**

### 7. Attacking the control, not the system
Where a security audience will lean in.

- **Verifier confirmation bias** — `2603.24579`: LLM-as-judge verifiers "inadvertently reproduce the errors of the original generation." The verifier is usually the same model family with the same context; guarantee it shares the premise and it ratifies the attack.
- **Timing as an attack surface** — `2606.27409`: correction that is too strong or too delayed turns consensus into **oscillation**, worst when communication and verification delays coincide. Influence *timing* and you degrade integrity without injecting a single false fact.
- **Configuration as an attack surface** — `2608.02827`: a phase transition to collective bias driven by **noise, e.g. sampling temperature**. A parameter usually tuned for output diversity, with no security review, is a control surface for consensus integrity.

**Flag honestly:** these are 🟡 *plausible* — the mechanisms are measured, the attacks are not demonstrated. Say it in the text.

### 8. What actually works
Lead with the strongest measured control, not a wish list.

| Control | Measured effect | Source |
|---|---|---|
| Message-layer lineage governance | Prevents final infection in **≥89%** of runs | `2603.04474` |
| Model heterogeneity | "Universal antidote" to correlated failure | `2502.08788` |
| Moderately sparse topology | Suppresses propagation, keeps useful diffusion | `2505.23352` |
| Evidence-aware aggregation | +5 pp over majority vote | `2602.09341` |
| Grounded verification | Truth becomes an absorbing boundary; oscillation vanishes | `2606.27409` |
| Information-asymmetric verifiers | Counters verifier confirmation bias | `2603.24579` |

**Then the honest part** — controls with *no* evidence, which most articles would assert anyway:
- **Provenance labelling** — recommended everywhere, measured nowhere in this corpus
- **Rollback / context purging** — `2608.03421` is direct evidence naive versions fail
- **More reviewer agents** — suppresses the wrong answer without producing the right one

Admitting the third column is what makes the first two credible.

### 9. The gap: prompt injection
Address it head-on rather than letting a reader notice the omission.

> Everything above concerns a false **claim** being *believed*. Prompt injection concerns a false **instruction** being *obeyed*. They chain — an injected instruction can plant a claim that then cascades — but they are different problems, and the 40-paper corpus behind this article contains **zero** prompt-injection studies.

Naming your own coverage boundary is a credibility move with this audience, and it sets up the framework mention: `2603.15408` (TrinityGuard), OWASP-grounded, 20 risk types across single-agent, **inter-agent communication**, and **system-level emergent** tiers — the two tiers single-agent tooling misses.

### 10. Checklist
Lift the practical checklist from [`threat-model.md` §7](../research/threat-model.md#7-practical-checklist), keeping the **[unvalidated]** markers. Do not silently promote unvalidated items to recommendations.

### 11. Close
> An LLM agent network is not a pipeline with a model in it. It is a distributed system where every participant's output becomes every downstream participant's evidence — and where the cheapest attack is a single sentence.
>
> Treat peer output as untrusted input. Track claim lineage. Assume removing the attacker does not remove the belief.

---

## Structural notes

- **Sections 4, 5, 6 are the payload.** If cutting, cut 1, 9, and 10.
- **Section 6 is the most actionable** — incident-response implications are the piece's practical contribution.
- **Section 5's "your quorum is nominal" is the memorable line.** Give it room.
- **Every number carries its arXiv ID inline.** With this audience, unsourced numbers are fatal.
- **Keep the reliability framing subordinate.** The audience wants attack surface and controls, not epistemics.

## Figures needed

Additions to [`figures-needed.md`](figures-needed.md):

| # | Figure | Purpose | Source |
|---|---|---|---|
| 13 | **Trust boundary diagram** | Where agent→agent sits among the boundaries; which are enforced by default | Own — [`threat-model.md` §2](../research/threat-model.md#2-trust-boundaries) |
| 14 | **Persistence after removal** | Truth recovery 72.50% → 14.17%, and belief surviving the deceiver's exit | `2608.03421` |
| 15 | **Attack-class grading** | A1–A8 by demonstrated / evidenced / plausible / out-of-corpus | Own — [`threat-model.md` §3](../research/threat-model.md#3-attack-classes) |
| 16 | **Nominal vs real quorum** | 3 same-model agents rendered as one correlated vote | `2602.09341`, `2608.00243` |

---

## Motivating source

This security track was prompted by a Turkish-language video on AI agents manipulating people and how much authority to grant agents over real systems — recorded with verified metadata in [`../sources/media-sources.md`](../sources/media-sources.md).

**It has not been watched and none of its claims are used here.** It is logged as motivation for the track, not as a source for any statement in this outline.

---

## Pre-publication checklist

- [ ] Every number traces to an arXiv ID in [`paper-index.md`](../research/paper-index.md)
- [ ] 🟡 Plausible attack classes are labelled as such in the prose
- [ ] The prompt-injection gap is stated explicitly (§9)
- [ ] No OWASP or MITRE identifier is cited without verification against the current list
- [ ] Controls with no evidence are listed as such, not as recommendations
- [ ] Nothing describes the contents of the unwatched video
- [ ] Does not contradict [`article-outline.md`](article-outline.md)
