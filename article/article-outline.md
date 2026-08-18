# Article Outline

**Working title:**
> **Hallucination Cascade in Multi-Agent LLM Systems: When One Agent's Error Becomes Another Agent's Reality**

**Alternatives:**
- *When Agents Agree on the Wrong Thing*
- *More Agents, More Truth? The Reliability Problem Nobody Benchmarks*
- *Your Multi-Agent System Is an Epistemic Network. Design It Like One.*

**Target:** medium-to-advanced technical. Engineers building agent systems. ~2,500–3,500 words.

---

## ⚠️ Writing rules for this article

The corpus makes certain intuitive claims indefensible. Violating these will make the piece wrong, not just weak:

1. **Do not write "cascades amplify errors" as fact.** The most direct study (`2606.07937`) measured net **attenuation** (amplification factor 0.644). Direction is a variable.
2. **Do not write "more agents = more hallucination."** `2502.08788` found MAD often *underperforms* single agents — which is a different failure than amplification.
3. **Do not present the hypothesis chain as established.** Label it as a research model.
4. **Do not claim verifiers solve this.** `2603.24579` (confirmation bias), `2606.27409` (oscillation).
5. **Do not dismiss prompting.** `2606.08457` got Cohen's d = +1.43 to +1.99 from a prompt-level intervention. Prompting is necessary but not sufficient — not weak.
6. **Cite arXiv IDs for every number.** No unsourced statistics.
7. **No invented examples presented as real.** Illustrative examples must be labelled illustrative.

---

## The hook

Open with the asymmetry that makes this a systems problem:

> One model hallucinating is a model problem. Five agents building on that hallucination is a systems problem — and you cannot fix it by choosing a better model.

Then the central question:

> **What happens when one LLM agent's mistake becomes another agent's context?**

---

## Section-by-section

### 1. Why agentic AI is rising
Short. Multi-agent systems moved from proof-of-concept to deployment. `2608.02827` notes the transition into finance, politics, medicine.
**Do not oversell.** Two paragraphs at most; the reader already believes this.

### 2. The assumption: more agents = more intelligence
State the intuition honestly — it has real foundations. `2305.14325` ("society of minds"), `2309.13007`, `2410.12853`. This is a reasonable belief, not a strawman.

### 3. The evidence that complicates it
The turn. `2502.08788`: 5 MAD methods × 9 benchmarks × 4 models — MAD **often fails to beat** Chain-of-Thought and Self-Consistency, at significantly higher compute cost. `2605.00914`: isolated self-correction beat homogeneous debate at 2.1–3.4× lower token cost.

**Pivot line:** *More agents does not mean more truth. It means more channels.*

### 4. From single-agent to multi-agent hallucination
The unit of analysis shifts from **response** to **trajectory**. `2601.22984`: end-to-end evaluation "obscures intermediate hallucinations that accumulate throughout the research trajectory."
This is the article's core conceptual move — give it room.

### 5. Error propagation
Errors travel along message dependencies. `2603.04474` models collaboration as a directed dependency graph; a **single atomic error seed** produced widespread failure.
**Key reframe:** an agent network is an epidemic system (`2607.21912` models it literally as susceptible/exposed/infectious/corrected).

### 6. Hallucination cascade — and the honest complication
Introduce the amplification factor. Then present the contradiction squarely:

| `2606.07937` | 0.422 → 0.272 over 3 hops; factor **0.644** — attenuation. But accuracy *also* fell. |
| `2603.04474` | One seed → widespread failure |
| `2608.03421` | Truth recovery 72.50% → **14.17%** |

**This is the article's strongest intellectual moment.** Most writing on this topic asserts amplification. Showing that the direct measurement found the opposite — and explaining what selects the direction — is what separates this from the genre.

**Synthesis:** *A multi-agent system is an error-control network. It can filter noise or lock it in. The protocol decides which.*

### 7. Context and goal drift
`2606.21666`: a class of hallucination arises not from model incapacity but from **context drift** — divergent state between agents, each individually reasonable. `2601.04170`'s semantic / coordination / behavioral drift vocabulary (flag it as simulation-based).

### 8. False consensus
The strongest quantified section. `2605.00914`: modal adoption up to **85.5%**, contextual fragility up to **70.0%**, oracle gap up to **32.3 pp**. `2602.09341`: **confabulation consensus** — correlated priors, no conformity required. `2606.08457`: the **consistency illusion** — debate reduced contradictions while *decreasing* reasoning similarity.

**The line that will land:** *Agreement between agents from the same model is not three opinions. It is one opinion, sampled three times.*

### 9. The danger of shared context
`2608.03421`: false testimony is adopted **more readily** than truthful testimony, propagates to higher orders, and **persists through honest agents after the deceiver exits**. `2606.16710`: this happens in **benign** systems — no attacker required.

**Practical consequence:** removing a bad source does not remove the bad belief. Rollback is harder than it looks.

### 10. Why debate is not automatically the answer
`2511.07784` (is debate deliberation or ensembling?), `2608.00243` (second-round arguments add little semantic novelty), `2502.08788`.

### 11. Critic and verifier agents
Both sides. Helps: `2606.07941` (up to 39% reduction), `2602.09341` (+5 pp over majority vote). Conditional: `2603.24579` (verifier confirmation bias), `2606.27409` (too strong or too delayed → oscillation; grounding makes truth an absorbing boundary).

**The uncomfortable question to raise:** what if the verifier inherits the same false premise? Largely unstudied — flag it as an open problem, and note this repo's experiment-04 targets it.

### 12. Prompt architecture as a real control
Resist the "prompting isn't enough" cliché. `2606.08457`'s Grounded Debate Protocol is prompt-level and produced **Cohen's d = +1.43 to +1.99**. `2607.26836` predicts failure risk from role–task misalignment *before interaction*.

**The right framing:** *Prompting defines local agent behavior. Orchestration defines system behavior. You need both.*
Then give the 10-point prompt contract from `research/research-map.md`.

### 13. Proposed architecture
The diagram from `research/research-map.md`: immutable goal → independent first pass → claim/evidence ledger → independent verifier → verified-only memory → synthesis.

**The memorable principle:** *Do not make the chat transcript the database.* Agent conversation is untrusted working state; promote only verified claims into durable memory.

### 14. How to measure this properly
Trajectory metrics, not pass@1. Amplification factor, adoption probability, propagation depth, oracle gap, CDS, cost per corrected error.
**Insist on cost.** `2605.00914`'s 2.1–3.4× token finding is the discipline most reporting lacks.

### 15. Open questions
Be honest about the gaps: memory contamination (n=1 in this corpus), no validated goal-drift metric, the verifier-shares-the-premise problem, inter-agent error correlation never reported directly.
**Ending gaps rather than answers is a strength here** — it invites collaboration and is accurate.

### 16. Conclusion
The shift: from **prompt engineering** to **epistemic systems engineering**.

> Reliability in a multi-agent system is not the average reliability of its agents. Errors become messages, messages become context, context becomes evidence, and repeated evidence becomes consensus. Design the epistemics, not just the prompts.

---

## Structural notes

- **Sections 6 and 8 are the payload.** If space runs short, cut sections 1, 2, and 10 — not these.
- **Lead with the contradiction, not the scary story.** Readers have seen cascade-doom posts. They have not seen "the direct measurement found attenuation, and here is why that is *more* interesting."
- **Every number needs its arXiv ID inline.** This is the article's credibility.
- **One illustrative walkthrough**, clearly labelled as illustrative, around section 5 or 6.
- **Close with the repository link** and an invitation to contribute.
