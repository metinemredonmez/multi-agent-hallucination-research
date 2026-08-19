# Media Sources

Non-academic sources — talks, videos, documentaries, industry reports — that inform the framing of this research.

> **These are not evidence.** Media sources are recorded here for provenance and context. No claim in [`research/`](../research/) rests on any of them. Empirical claims cite papers in [`paper-index.md`](../research/paper-index.md); media sources may motivate a question but never answer one.

---

## Verification standard

Each entry separates **what was verified** from **what was not**. Where a video has not been watched, or a transcript could not be obtained, the entry says so plainly and does **not** summarize its content.

Describing the contents of a video nobody here has watched would be exactly the failure mode this repository studies: a plausible-sounding claim entering the record without grounding, then being cited later as established.

---

## V1 — Yapay Zeka Ajanları İnsanları Nasıl Manipüle Etti?

*("How Did AI Agents Manipulate People?")*

### Verified metadata

| Field | Value |
|---|---|
| **Title** | Yapay Zeka Ajanları İnsanları Nasıl Manipüle Etti? |
| **Channel** | Arman ACAR ([@armanacaryt](https://www.youtube.com/@armanacaryt)) |
| **URL** | https://www.youtube.com/watch?v=c8p86cUrQw8 |
| **Published** | 2026-08-19 |
| **Duration** | 22 min 30 s (1350 s) |
| **Language** | Turkish |
| **Format** | Self-tagged `belgesel` (documentary) |

*Metadata retrieved 2026-08-19 via YouTube's oEmbed endpoint and page metadata. View count at retrieval: 1,070 — recorded only to timestamp the retrieval, not as a signal of anything.*

### Stated topic

The video's own description poses two questions (translated from Turkish):

> What happens if AI agents begin manipulating people in pursuit of a goal? How much authority can we give an AI agent over the internet, code, and real systems?

### Author-supplied keywords

Taken verbatim from the page's metadata — these are the author's tags, not an assessment of coverage:

`yapay zeka ajanları` · `AI agents` · `yapay zeka güvenliği` · `AI safety` · `AI Security Institute (AISI)` · `AI agent security` · `prompt injection` · `sosyal mühendislik` (social engineering) · `cyber security` · `siber güvenlik` · `yapay zeka kontrolü` (AI control) · `ChatGPT` · `OpenAI` · `Anthropic`

### ⚠️ Not verified

- **The video has not been watched.** No one on this project has viewed its contents.
- **No transcript was obtained.** Auto-generated Turkish captions exist, but YouTube's `timedtext` endpoint returned empty without authentication.
- **No claim made in the video is recorded here**, because none could be checked.
- The keywords above are **author-assigned tags**. A tag is a claim about topic, not proof of coverage, and carries no evidentiary weight.

> **Consequence:** cite this entry for *what the video is*, never for *what it says*. To use its content, someone must watch it and add sourced, timestamped notes below.

### Relevance to this repository

The video's stated framing — agents manipulating people, and how much authority to grant an agent over real systems — sits adjacent to two things this corpus does cover:

- **Agent-to-agent persuasion and susceptibility** — `2503.01829` (PMIYC) frames susceptibility to persuasion as an alignment and safety problem; `2606.24976` documents sycophantic conformity in agentic persuasion.
- **Authority over real systems** — `2602.16666` documents real incidents where agent authority produced harm: a production database deleted despite instructions forbidding it, an unauthorized purchase bypassing user confirmation, a chatbot giving illegal advice.

**Note the direction difference.** This corpus studies agent→**agent** influence. The video's title concerns agent→**human** manipulation. These are related but distinct; do not treat corpus findings as evidence about the human-facing case.

**One tag marks a real gap.** `prompt injection` appears in the video's keywords, and **no paper in this corpus covers prompt injection** — see [`threat-model.md` §A8](../research/threat-model.md#a8-prompt-injection-out-of-corpus). The video did not create that gap, but it makes it visible.

### Follow-up

- [ ] Watch the video; add timestamped notes with claims attributed to specific moments
- [ ] Record which claims are the author's own vs sourced, and to what
- [ ] Chase any papers or incidents it cites — those, not the video, become citable
- [ ] Check whether the AI Security Institute (AISI) material referenced by the tags is publicly available

---

## Adding a media source

1. **Verify metadata first** — title, author, date, duration, from the platform itself, not from memory.
2. **Separate verified from unverified** explicitly.
3. **Do not summarize content you have not consumed.** An empty content section is correct and honest; a plausible guess is not.
4. **Never use a media source as evidence for an empirical claim.** Follow it to its primary sources and cite those.
5. **Quote sparingly**, attribute clearly, and translate rather than reproducing long passages.
6. **Record the retrieval date** — media metadata changes and videos are deleted.
