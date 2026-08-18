# Research Notes

Working observations from building this corpus. Rougher than the `research/` files — kept because the reasoning is worth preserving.

---

## The finding that reframed the project

Going in, the assumption was straightforward: errors propagate between agents and compound. The name "hallucination cascade" presupposes it.

Then `2606.07937` — the corpus's most direct study — measured **net attenuation**. Hallucination score 0.422 → 0.272 over three hops. Amplification factor **0.644**.

The first instinct was that this weakened the project. It does the opposite. It replaces a weak question with a strong one:

> ~~Do errors amplify in multi-agent systems?~~
> **What determines whether an agent network filters an error or locks it in?**

The second question has a real answer space — topology, heterogeneity, grounding, verification timing, context policy — and every one of those is independently evidenced in this corpus. The first question just wanted a yes.

**And the trade-off in that same result is the most underrated finding here:** hallucination went *down* while factual accuracy *also* went down (0.789 → 0.769). The cascade suppressed unsupported claims and lost true ones with them. That is a hedging dynamic, not a correction dynamic — later agents becoming more cautious rather than more correct. Worth designing an experiment around.

---

## Three failure modes that get conflated

Reading closely, "the agents agreed and were wrong" is at least three different failures that demand opposite fixes:

| Failure | Mechanism | Fix |
|---|---|---|
| **Sycophantic conformity** | Agent abandons a correct position under peer pressure | Independence, isolated first pass |
| **Confabulation consensus** | Correlated priors → same wrong answer, *no conformity needed* | Heterogeneity — independence does **not** help |
| **Consensus collapse** | Right answer was in the pool, voting discarded it | Better aggregation — neither of the above helps |

The distinction that matters most: **independence fixes the first, does nothing for the second, and is irrelevant to the third.** Most practical advice ("have agents reason independently first") only addresses one of three.

`2605.00914` finding that conformity is already high at K=2 peers is the practically alarming detail. You do not need a crowd — two peers is enough.

---

## The persistence result deserves more attention than it gets

`2608.03421`: a false claim **kept propagating through honest agents after its source left the conversation.**

The engineering implication is larger than the paper's framing suggests. It means:

- Removing a bad agent does not undo its influence
- Rollback at the *source* level is insufficient — the belief has been copied into downstream state
- Any "just remove the contaminated context" mitigation is probably inadequate

This connects directly to memory contamination, and it is why the target architecture insists on claim-level provenance rather than message-level. If you cannot trace which claim came from where, you cannot roll it back.

---

## Prompting is undersold in the discourse

The reflexive line in agent engineering is "you can't prompt your way out of this." The evidence pushes back.

`2606.08457`'s Grounded Debate Protocol is *purely prompt-level* — require agents to commit to named facts and take explicit stances on peers' claims — and produced **Cohen's d = +1.43 to +1.99**. Those are large effects, from prompting alone.

`2607.26836` goes further: semantic misalignment between agent **roles** and task **queries** predicts hallucination risk *before any interaction happens*. Prompt design is measurable as a risk factor in advance.

The accurate framing is necessary-but-not-sufficient, and it is worth being precise about it, because "prompting doesn't work" is both wrong and a convenient excuse for reaching straight for architecture.

---

## Where the corpus is genuinely thin

Noted while categorizing — the `memory-contamination/` folder holding **one** paper was not a filing accident. It reflects the field.

1. **Memory contamination: n=1** (`2606.24976`, persuasion domain). No decay curve, no half-life, no cross-session study. This is the most open area with the clearest experimental path.
2. **Goal drift has no dedicated paper.** Only `2601.04170`'s semantic drift, which is simulation-based.
3. **Inter-agent error correlation is never reported as a number.** `2602.09341` names confabulation consensus, `2608.00243` documents its symptoms, `2502.08788` shows heterogeneity fixes it. Nobody publishes the correlation coefficient — despite it being a few hours of compute and the direct answer to RQ15.
4. **Verifier-inherits-the-premise is named but not measured.** The production default, unstudied.
5. **Cost normalization is rare.** `2605.00914` is the exception, and it is the paper whose conclusions feel most trustworthy as a result.

Gap 3 is the most striking. It is cheap, decisive, and missing.

---

## On the two Jamshidi papers

`2606.07937` and `2606.07941` share a first author and near-consecutive arXiv IDs. Distinct papers, but **not independent evidence** — same research programme, likely same infrastructure and assumptions.

This matters because `2606.07937` is the single most-cited source for the attenuation result. If a systematic bias exists in that setup, it affects the corpus's most surprising finding. Worth reading both full texts together and checking whether the experimental setups share components.

Filed as a caution, not a criticism.

---

## Methodological standards worth copying

`2605.00914` is the model. It:

- included a **stochastic noise control** (rationales from unrelated problems) — separating "peer input helps" from "any input perturbs"
- reported **token cost alongside accuracy** (2.1–3.4×)
- decomposed failure into named mechanisms rather than reporting one aggregate
- ablated communication density and temperature

`2608.00243` is the model for honesty: it explicitly states that its reference and panel use different model variants, so results "characterize the complete systems rather than isolate a causal debate effect." Volunteering the confound that weakens your own headline is rare.

`2503.13657` is the model for rigor: 1600+ traces, 7 frameworks, expert annotators, κ=0.88.

---

## Open thread: is attenuation just hedging?

A hypothesis worth testing, from the 2606.07937 trade-off.

If later agents in a chain become more cautious — hedging, qualifying, declining to assert — then:
- hallucination score falls (fewer unsupported claims)
- factual accuracy also falls (fewer true claims asserted)
- the system looks safer and is less useful

That matches the observed 0.422→0.272 alongside 0.789→0.769 exactly.

**Testable:** measure assertion *rate* per hop alongside accuracy. If assertion rate falls with depth, attenuation is hedging, not correction — and the whole "cascades attenuate" reading needs qualifying.

This may be the most interesting original idea to come out of building this corpus. Nothing in the 40 papers appears to test it.
