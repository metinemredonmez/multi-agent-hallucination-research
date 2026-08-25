# Backlog

Task list carried over from the original `HLC/` working folder (`notes/TODO_NEXT.md`), with each item mapped to its current status.

> **Provenance.** These were the tasks defined when the corpus was first assembled, before this repository existed. Preserved so nothing from the original planning is silently dropped. Where an item is done, the file that completed it is linked.

**Legend:** ✅ done · 🟡 partly done · ⬜ open

---

## Literature synthesis

| Status | Task | Where |
|---|---|---|
| 🟡 | Extract central claim, method, benchmark, and key finding from each of the 40 papers | [`paper-index.md`](../research/paper-index.md) — done from abstracts; **full-text pass still open** (entries marked `TODO`) |
| ⬜ | **Mark each paper as direct evidence / supporting evidence / counterpoint / background** | **Not done.** See below — this is the most valuable open item here |
| ✅ | Identify duplicated claims and contradictory findings | [`literature-review.md` §10](../research/literature-review.md) — contradictions table |
| ✅ | Separate 2023–2024 foundations from 2025–2026 newer work | [`literature-review.md` §1](../research/literature-review.md) — the three-act arc |

### The open item: evidence-role tagging

Each paper should carry an explicit role relative to the central hypothesis:

- **Direct evidence** — studies the cascade mechanism itself (e.g. `2606.07937`, `2603.04474`)
- **Supporting** — evidences one link in the chain (e.g. `2605.00914`, `2608.03421`)
- **Counterpoint** — cuts against the hypothesis (e.g. `2606.07937`'s attenuation result, `2502.08788`)
- **Background** — context and vocabulary (e.g. surveys `2509.18970`, `2607.26212`)

Note that `2606.07937` belongs in **both** direct evidence and counterpoint — which is precisely why the tagging is worth doing explicitly rather than leaving implicit.

---

## Taxonomy

✅ **Done** — [`terminology.md`](../research/terminology.md) covers all ten originally-listed concepts, each with definition, distinction from neighbours, MAS mechanism, measurable metrics, and related papers:

local hallucination · unsupported assumption · error propagation · belief reinforcement · collective hallucination · context drift · goal drift · consensus collapse · tool/action failure · cascading system failure

The final file expanded to 15 concepts and added the distinctions the original list left implicit — notably consensus collapse vs collective hallucination, and confabulation consensus as a separate mechanism.

---

## Architecture section

✅ **Done** — [`research-map.md` §3, §7](../research/research-map.md) and [`threat-model.md` §4](../research/threat-model.md).

All originally-listed comparisons are covered: shared vs scoped prompt · centralized vs peer-to-peer · sequential vs parallel · independent-first vs debate-first · critic/verifier/judge agents · evidence and provenance tagging · confidence propagation · retrieval grounding · immutable goal anchors · memory isolation · tool output validation · human-in-the-loop checkpoints.

---

## Experiments worth reproducing

✅ **Designed** (⬜ none run) — [`experiments/`](../experiments/)

| Original task | Where |
|---|---|
| Inject one false fact into Agent 1, measure survival through N agents | [experiment-01](../experiments/experiment-01-error-propagation) |
| Compare homogeneous vs heterogeneous model teams | experiment-01 + [experiment-03](../experiments/experiment-03-consensus-collapse) |
| Compare full-context vs minimal scoped-context sharing | experiment-01 |
| Compare majority voting vs verifier-based adjudication | experiment-03 + [experiment-04](../experiments/experiment-04-verifier-agent) |
| Measure semantic distance from the original task after each hop | [experiment-02](../experiments/experiment-02-context-drift) |
| Measure whether confidence rises while factual accuracy falls | experiment-03 — confidence–correctness correlation |

---

## Article output

✅ **Outlined** (⬜ not written) — [`article/`](../article/)

The original 10-point structure is preserved in [`article-outline.md`](../article/article-outline.md), expanded to 16 sections. A second, security-focused article was added later: [`security-article-outline.md`](../article/security-article-outline.md).

**One substantive change from the original plan.** The original outline point 4 was *"Explain why multi-agent systems amplify some failure modes."* That framing had to be revised: `2606.07937` — the corpus's most direct cascade study — measured net **attenuation** (amplification factor 0.644), not amplification. The article now leads with the contradiction instead of asserting amplification. See [`research-notes.md`](research-notes.md).

---

## Added since the original list

Work not anticipated when the corpus was assembled:

- [`threat-model.md`](../research/threat-model.md) — security view, 8 graded attack classes
- [`open-research-questions.md`](../research/open-research-questions.md) — 15 questions with evidence status
- [`source-validation.md`](../sources/source-validation.md) — verification methodology
- [`media-sources.md`](../sources/media-sources.md) — non-academic sources
- [`experiments/framework/`](../experiments/framework/) — provider-agnostic scaffolding

## Current priorities

1. Full-text reading pass on the 12 priority papers — closes most `TODO` entries in the index
2. Evidence-role tagging (the open item above)
3. Acquire prompt-injection literature — corpus coverage is currently zero
4. Run experiment-04 arms A vs B
