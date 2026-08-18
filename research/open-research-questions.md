# Open Research Questions

The 15 questions driving this project, each with: what the corpus already answers, what remains open, and how it could be tested.

**Reading the evidence labels**

| Label | Meaning |
|---|---|
| 🟢 **Partly answered** | Direct evidence exists; the open part is scope or generalization |
| 🟡 **Contested** | Papers disagree, or the evidence cuts both ways |
| 🔴 **Open** | Little or no direct evidence in this corpus |

---

## RQ1 — Are multi-agent systems actually more reliable than single-agent systems?

🟡 **Contested — and the honest answer leans "not by default."**

**Evidence.** `2502.08788` systematically evaluated 5 MAD methods × 9 benchmarks × 4 models and found MAD *often fails to outperform* simple single-agent baselines (Chain-of-Thought, Self-Consistency) while consuming significantly more compute. `2605.00914` found isolated self-correction beat homogeneous debate at 2.1–3.4× lower token cost. `2608.00243` found a 3-agent panel ranged from +8.5 to −4.4 pp against a single-agent reference — two wins, one loss, three inconclusive. `2503.13657` notes MAS benchmark gains "are often minimal."

**Still open.** Every one of those studies evaluates *published MAD designs*. None establishes that a well-designed multi-agent system cannot win — only that the ones tested often do not. The distinction matters and is frequently blurred.

**How to test.** Cost-normalized comparison: single agent at N× compute vs N agents at 1× each. Most of the literature does not control for this.

---

## RQ2 — Does error probability fall or propagation risk rise as agent count grows?

🟡 **Contested — both effects are real and they compete.**

**Evidence.** `2607.21912` formalizes exactly this tension: reliability and error control impose **opposing graph constraints**, and characterizes when their feasible intersection is *empty*. `2505.23352` found **moderately sparse** topologies optimal — enough connectivity for beneficial diffusion, not enough for error propagation. `2605.00914` found conformity already high at minimal peer exposure (K=2), so the propagation cost arrives early.

**Still open.** No paper in the corpus sweeps agent count against a *fixed* task suite with cost held constant. The optimum is likely task-dependent and unmapped.

**How to test.** experiment-01, sweeping N ∈ {1,3,5,7} × topology, holding total compute fixed.

---

## RQ3 — How does one agent's hallucination get amplified by others?

🟡 **Contested — amplification is not the default.**

**Evidence.** `2606.07937` measured **net attenuation** (amplification factor 0.644, hallucination score 0.422→0.272 over 3 hops) — but with factual accuracy *also* falling (0.789→0.769). `2603.04474` found a single atomic error seed causing widespread failure, and named three vulnerability classes: cascade amplification, topological sensitivity, consensus inertia. `2606.07941` reports amplification of 1.45 undefended vs 1.08 with adaptive control.

**Still open.** **What determines the direction?** This is the single most important open question in the repository. The corpus contains both outcomes with no unified account of the conditions that select between them.

**How to test.** experiment-01. Vary topology, grounding, and heterogeneity while holding the seed constant; measure amplification factor per condition.

---

## RQ4 — Why do agents form incorrect consensus?

🟢 **Partly answered — three distinct mechanisms are documented.**

| Mechanism | Definition | Source |
|---|---|---|
| **Sycophantic conformity** | Agent abandons a correct position under peer pressure (modal adoption up to 85.5%) | `2605.00914` |
| **Confabulation consensus** | Correlated priors → agents independently reach the same wrong rationale; *no conformity required* | `2602.09341` |
| **Phase transition** | Collective bias emerges when conformity passes a critical threshold; noise (temperature) is a key driver | `2608.02827` |

`2606.08457` adds the **consistency illusion**: debate reduced contradictions while *decreasing* reasoning-chain similarity — agents appeared to agree more while reasoning less consistently.

**Still open.** Relative contribution of each mechanism in a given system, and whether they are separable in practice.

---

## RQ5 — Is majority voting always reliable?

🟢 **Answered: no.**

**Evidence.** `2605.00914` measured an **oracle gap up to 32.3 pp** — the correct answer was in the candidate pool and plurality voting discarded it. `2602.09341` shows voting "discards the evidential structure of reasoning traces" and is brittle under confabulation consensus; replacing it with reasoning-tree auditing gained up to **5 pp** over majority vote and **3 pp** over LLM-as-Judge.

**Still open.** The alternatives' gains are modest (3–5 pp) and add adjudication compute. Whether evidence-aware aggregation is worth its cost at scale is unestablished.

---

## RQ6 — What is the trade-off between independent reasoning and shared context?

🟢 **Partly answered, with a clean quantitative anchor.**

**Evidence.** `2605.00914`: isolated self-correction beat unguided homogeneous debate, at 2.1–3.4× lower cost. `2505.23352`: moderately sparse beats both dense and very sparse. `2607.21912`: the two objectives impose opposing constraints, sometimes with empty intersection.

**Still open.** All the independence evidence is from **homogeneous** teams. Whether independence still wins when agents are genuinely heterogeneous — where shared context might transmit genuinely *new* information rather than correlated noise — is untested. This is corpus gap #3.

---

## RQ7 — Does context sharing cause error contamination?

🟢 **Yes, with a strong quantified result.**

**Evidence.** `2608.03421`: a single false testimony is **adopted more readily than truthful testimony**, propagates to higher orders, and **persists through honest agents after the deceiver exits**. Truth recovery 72.50% → 14.17%. `2606.16710` establishes the same class of failure with **no adversary at all** — misinformation from RAG, search, or agent misinterpretation.

**Still open.** Whether provenance labelling (marking peer claims as hypotheses, not facts) actually reduces adoption. Widely recommended; not measured in this corpus.

**How to test.** experiment-01, provenance-labelled vs unlabelled context.

---

## RQ8 — Does a critic/verifier agent actually reduce errors?

🟡 **Contested — verifiers help, but not unconditionally.**

**Evidence for.** `2603.24579` (MARCH), `2606.07941` (up to 39% hallucination reduction), `2602.09341`. `2606.27409` finds grounded verification *stabilizing* — grounded factual answering makes truth an absorbing boundary.

**Evidence against.** `2606.27409` also shows correction that is **too strong or too delayed turns consensus into oscillation**, worst when communication and verification delays coincide. `2603.24579` identifies verifier **confirmation bias**: LLM-as-judge verifiers reproduce the errors of the generation they check.

**Still open.** Verifier *dose* and *placement* have one theoretical treatment (`2606.27409`) and little empirical validation.

---

## RQ9 — What happens when the verifier shares the same false assumption?

🔴 **Largely open — and this is the most important gap in the corpus.**

**Evidence.** `2603.24579` names the problem (confirmation bias) and proposes **deliberate information asymmetry** — Solver / Proposer / Checker with asymmetric access. `2511.11182` obtains ground truth about *which agent is hallucinating* via counterfactual image tests, but that trick is vision-specific and does not transfer to text pipelines.

**Still open.** Almost everything. No paper systematically measures verifier failure rate *conditioned on the verifier inheriting the generator's premise*. Yet this is exactly the production failure mode: the verifier is usually the same model family, given the same context.

**How to test.** experiment-04. Inject a false premise into shared context, then compare verifiers with (a) full shared context, (b) information-asymmetric context, (c) a different model family. This is the highest-value experiment in the repository.

---

## RQ10 — Should agents reason independently before seeing peer outputs?

🟢 **Evidence says yes — for homogeneous teams.**

**Evidence.** `2605.00914`: peer exposure produces contextual fragility (vulnerability up to 70.0%) and conformity is already high at K=2. Isolated self-correction won outright.

**Still open.** The heterogeneous case (see RQ6). Also: whether independence should hold for *all* rounds or only round 1.

---

## RQ11 — How does prompt structure affect cascades?

🟢 **More answerable than expected — and prompt effects are larger than commonly assumed.**

**Evidence.** `2606.08457`'s Grounded Debate Protocol — a **prompt-level** intervention requiring agents to commit to named facts and take explicit stances on peers' claims — produced alignment improvements of **Cohen's d = +1.43 to +1.99**. That is a large effect from prompting alone. `2607.26836` shows fine-grained semantic misalignment between agent **roles** and task **queries** predicts hallucination risk *before interaction begins*.

**Still open.** Which specific prompt elements carry the effect. GDP bundles several changes; no ablation isolates them.

**Note.** Resist the reflex that "prompting is not enough." `2606.08457` is direct evidence that prompt architecture is a *first-class* control, not a weak one. The correct claim is that prompting is necessary but not *sufficient* — topology, verification, and memory remain independent levers.

---

## RQ12 — If agent memory is contaminated, how many turns does the error persist?

🔴 **Open — the thinnest-supported area in the corpus.**

**Evidence.** `2606.24976` is the only paper whose primary mechanism is memory-write contamination: an early bad assumption "quietly contaminates memory writes" and surfaces steps later; semantic leakage in standard RAG is a reproducible trigger. `2608.03421` supplies the closest quantitative analogue — persistence through honest agents *after the source exits* — but that is conversational, not durable-memory, persistence.

**Still open.** Essentially the whole question. No decay curve, no half-life measurement, no cross-session study, no test of whether rollback actually removes downstream effects.

**How to test.** Inject a false fact into memory; measure readable-contamination duration in turns; test rollback completeness. High-value, low-competition.

---

## RQ13 — How is goal drift measured in long-running systems?

🔴 **Open — no agreed metric.**

**Evidence.** `2601.04170` proposes the **Agent Stability Index** over 12 dimensions and names semantic drift — but the paper is **simulation-based and theoretical**, single independent author, hedged throughout. `2606.21666`'s **Context Divergence Score** measures state divergence between agents, which is related but not the same as distance from the *goal*.

**Still open.** No validated goal-drift metric exists in this corpus. Neither ASI nor CDS has been independently replicated.

**How to test.** experiment-02. Embedding distance between the immutable original goal and the operative objective at each hop, plus constraint-retention rate. Both need validation against human judgment before being trusted.

---

## RQ14 — Does model heterogeneity reduce error correlation?

🟢 **Evidence says yes — the most consistent positive finding in the corpus.**

**Evidence.** `2502.08788` calls heterogeneity a "**universal antidote**" that consistently improves MAD frameworks. `2604.02923` reports 41.7% relative hallucination reduction from a heterogeneous council. `2309.13007` and `2410.12853` are the foundational diversity results.

**Caveats.** `2604.02923` is a **non-peer-reviewed technical report**; `2410.12853` appeared in a venue whose review standards should be checked. The strongest evidence is `2502.08788`.

**Still open.** *How much* heterogeneity, and along which axis — different model families, different sizes, different prompts, different temperature? Treated as binary in most work.

---

## RQ15 — Are agents derived from the same foundation model genuinely independent?

🟢 **Evidence says no.**

**Evidence.** `2602.09341` names **confabulation consensus** — agents sharing correlated biases converge on the same incorrect rationale, with no conformity needed. `2608.00243` found second-round arguments add little semantic novelty and self-reported confidence only weakly predicts correctness in homogeneous panels. `2502.08788`'s heterogeneity result is the mirror image of the same finding.

**Still open.** **Nobody in this corpus reports a direct inter-agent error-correlation coefficient.** That single number — how often do agents fail on the same items — would quantify the whole question, and it is cheap to compute.

**How to test.** Run N agents independently on a shared item set; report the pairwise error-correlation matrix for same-model vs cross-model pairs. Low-cost, high-value, and directly fills a corpus gap.

---

## Priority ranking for original work

Ranked by *evidence gap × feasibility*:

| Rank | Question | Why |
|---|---|---|
| 1 | **RQ9** — verifier shares the premise | Most important production failure mode; barely studied |
| 2 | **RQ15** — inter-agent error correlation | One cheap number closes a real gap |
| 3 | **RQ12** — memory contamination persistence | Corpus n=1; no decay curve exists |
| 4 | **RQ3** — what determines amplification direction | The corpus's central contradiction |
| 5 | **RQ6/RQ10** — independence × heterogeneity | Untested interaction cell |
| 6 | **RQ13** — goal drift metric | No validated metric; needed by everything else |
