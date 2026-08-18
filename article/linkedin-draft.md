# LinkedIn Draft

> **Status: skeleton with placeholders. Not ready to publish.**
>
> Every claim below is sourced or marked `[TODO]`. Do not publish while any `[TODO]` remains, and do not add a number that is not traceable to an arXiv ID in [`../research/paper-index.md`](../research/paper-index.md).

---

## Short version (~600 words, LinkedIn post)

**Hook**

> Everyone is building multi-agent systems on one assumption: more agents, more reliability.
>
> I spent a while reading the 2026 literature on that assumption. It does not hold up the way people think — and the reason is more interesting than "AI hallucinates."

**The setup**

When one model hallucinates, that is a model problem. When a second agent takes that output as *context*, it becomes a systems problem — and no amount of model-swapping fixes it.

The question that organizes all of this:

> **What happens when one agent's mistake becomes another agent's reality?**

**The finding people expect**

That errors compound. And sometimes they do — dramatically. In one controlled study, a **single false testimony** dropped collective truth recovery from **72.50% to 14.17%**. Worse: the false claim was adopted *more readily than a true one*, and **kept propagating through honest agents after its source left the conversation** (arXiv 2608.03421).

**The finding that surprised me**

The most direct study of hallucination cascades measured the opposite. Across 3-agent chains, the hallucination score *fell* — 0.422 → 0.272, an amplification factor of **0.644**. Net attenuation, not amplification.

But factual accuracy fell too (0.789 → 0.769). The system got less hallucinatory and less accurate at the same time (arXiv 2606.07937).

So the real question is not *"do errors amplify?"* It is: **what decides the direction?**

**Where consensus goes wrong**

This is where the numbers get uncomfortable. In homogeneous debate (arXiv 2605.00914):

- Agents adopted the majority answer up to **85.5%** of the time
- Peer rationales destabilized *previously correct* reasoning up to **70.0%** of the time
- Plurality voting discarded a correct answer that was **already in the pool** — an oracle gap up to **32.3 percentage points**
- All of this cost **2.1–3.4× more tokens** than a single agent correcting itself

And agreement can be an illusion: debate has been shown to *reduce* contradictions between agents while simultaneously *decreasing* the similarity of their reasoning (arXiv 2606.08457).

**The line worth remembering**

> Three agents built on the same foundation model are not three opinions. They are one opinion, sampled three times.

That is not rhetoric — it has a name in the literature: **confabulation consensus**, where agents with correlated priors independently converge on the same wrong rationale. No conformity required, so making them reason independently does *not* fix it (arXiv 2602.09341).

**What actually seems to help**

- **Model heterogeneity** — the most consistently supported intervention; one systematic study calls it a "universal antidote" (arXiv 2502.08788)
- **Moderately sparse communication** — not fully connected, not isolated (arXiv 2505.23352)
- **Aggregation that reads evidence**, not vote counts (arXiv 2602.09341)
- **Prompt architecture** — and more than expected: one prompt-level protocol produced effect sizes of Cohen's d = **+1.43 to +1.99** (arXiv 2606.08457)

**The uncomfortable open question**

Most systems add a verifier agent and call it solved. But verifiers suffer **confirmation bias** — they reproduce the errors of the output they are checking (arXiv 2603.24579). And verification that is too strong or too delayed can turn consensus into **oscillation** (arXiv 2606.27409).

What happens when the verifier inherits the *same false premise* as the generator? That is the production default — same model family, same context — and it is barely studied.

**Close**

The shift I would argue for: from **prompt engineering** to **epistemic systems engineering**.

Reliability in a multi-agent system is not the average reliability of its agents. Errors become messages. Messages become context. Context becomes evidence. And repeated evidence becomes consensus.

I am building this out in the open — 40-paper index, terminology, experiment designs: `[REPO LINK]`

`[TODO: decide CTA — collaborators? feedback? both?]`

---

## Long version (~2,500 words)

Follow [`article-outline.md`](article-outline.md) sections 1–16. The short version above corresponds to sections 3, 6, 8, 9, 11, 16.

`[TODO: draft after the full-text reading pass — several index entries still say "TODO: read full text".]`

---

## Pre-publication checklist

- [ ] Every number traces to an arXiv ID in `paper-index.md`
- [ ] No `[TODO]` markers remain
- [ ] The hypothesis chain is labelled as a working model, not a finding
- [ ] The attenuation result (`2606.07937`) is included — not just the scary numbers
- [ ] No claim that verifiers solve the problem
- [ ] Prompting is framed as necessary-but-not-sufficient, not dismissed
- [ ] Repo link works and the README does not overstate the project's status
- [ ] Turkish version considered — much of the original research intent was in Turkish

## Notes on tone

- **Do not fearmonger.** The attenuation result is the most credible thing in the piece precisely because it cuts against the narrative.
- **Numbers over adjectives.** "Oracle gap up to 32.3 pp" beats "consensus often fails."
- **Credit the papers inline.** arXiv IDs, visibly.
- **Say what is unknown.** The open questions are the most engaging part for a technical audience.
