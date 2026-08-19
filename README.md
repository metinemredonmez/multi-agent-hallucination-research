# Multi-Agent Hallucination Research

Research into hallucination cascades, error propagation, context drift, false consensus, and reliability failures in multi-agent LLM systems.

This repository investigates a central question:

> **What happens when one LLM agent's mistake becomes another agent's context?**

[![Papers](https://img.shields.io/badge/papers-40-blue)](research/paper-index.md)
[![Verified](https://img.shields.io/badge/arXiv%20IDs%20verified-39%2F40-green)](sources/source-validation.md)
[![Status](https://img.shields.io/badge/status-literature%20phase-orange)](#current-status)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

---

## Motivation

When a single model hallucinates, that is a model problem. When a second agent consumes that output as **context**, it becomes a systems problem — and choosing a better model does not fix it.

Multi-agent systems are being deployed on the assumption that more agents means more reliability. The 2025–2026 literature makes that assumption hard to defend:

- A systematic evaluation across 5 debate methods, 9 benchmarks, and 4 models found multi-agent debate **often fails to beat** single-agent Chain-of-Thought and Self-Consistency, at significantly higher compute cost — `2502.08788`
- In homogeneous debate, plurality voting discarded a correct answer **already present in the candidate pool** — an oracle gap up to **32.3 percentage points**, while consuming **2.1–3.4× more tokens** — `2605.00914`
- A **single false testimony** dropped collective truth recovery from **72.50% to 14.17%** — and kept propagating through honest agents **after its source left the conversation** — `2608.03421`
- Reliability gains have **lagged behind accuracy gains** across ~24 months of frontier releases, clustering similarly across all providers — an industry-wide plateau — `2602.16666`

This repository collects that evidence, separates the concepts, and designs experiments to test what actually determines whether an agent network corrects its errors or compounds them.

---

## Research scope

Multi-agent LLM systems, specifically:

| | |
|---|---|
| Hallucination cascade | Error propagation |
| Context drift | Goal drift |
| Agent drift | Collective hallucination |
| Consensus failure | Consensus collapse |
| Sycophantic conformity | Misinformation propagation |
| Memory contamination | Cascading failure |
| Multi-agent debate | Verification / critic agents |
| Inter-agent communication | Prompt design for multiple agents |

The focus is the mechanism by which **a small error made by one agent is transmitted to later agents, strengthened, and moves the system away from its original goal.**

Every term above is defined and — more importantly — *distinguished from its neighbours* in [`research/terminology.md`](research/terminology.md).

---

## Core hypothesis

```text
Initial User Goal
       ↓
    Agent 1
       ↓
Small reasoning / factual error
       ↓
Agent 2 accepts it as context
       ↓
Agent 3 reinforces the assumption
       ↓
Consensus / false confidence
       ↓
Context & Goal Drift
       ↓
Hallucination Cascade
       ↓
Cascading System Failure
```

> ### ⚠️ This is a working hypothesis, not an established result.
>
> **No paper in this corpus demonstrates this full chain end to end**, and at least one link is contradicted by direct evidence.
>
> The most direct study of hallucination cascades (`2606.07937`) measured **net attenuation** across 3-agent chains — an amplification factor of **0.644**, meaning error *decreased* with depth. Factual accuracy declined too (0.789 → 0.769), suggesting the system became more cautious rather than more correct.
>
> Meanwhile `2603.04474` showed a single injected error seed causing widespread failure, and `2608.03421` measured truth recovery collapsing to 14.17%.
>
> **Both outcomes are real.** An agent network is an error-control system that can run in either direction:
>
> ```text
> Error Seed ──▶ Critique ──▶ Verification ──▶ Correction ──▶ Recovery
> ```
>
> So the question this project actually asks is not *"do errors amplify?"* but:
>
> **What determines which trajectory a multi-agent system follows?**

Full treatment, including a link-by-link evidence audit: [`research/research-map.md`](research/research-map.md).

---

## Research questions

Fifteen questions drive the project. Each is assessed in [`research/open-research-questions.md`](research/open-research-questions.md) with 🟢 partly answered / 🟡 contested / 🔴 open.

| # | Question | Status |
|---|---|---|
| 1 | Are multi-agent systems actually more reliable than single-agent? | 🟡 Contested — leans *not by default* |
| 2 | Does error probability fall or propagation risk rise with agent count? | 🟡 Both effects are real and compete |
| 3 | How does one agent's hallucination get amplified by others? | 🟡 **Direction is contested** |
| 4 | Why do agents form incorrect consensus? | 🟢 Three distinct mechanisms documented |
| 5 | Is majority voting always reliable? | 🟢 **No** — oracle gap up to 32.3 pp |
| 6 | Independent reasoning vs shared context — what's the trade-off? | 🟢 Partly answered |
| 7 | Does context sharing cause contamination? | 🟢 Yes, strongly evidenced |
| 8 | Do critic/verifier agents actually reduce errors? | 🟡 Conditional on timing and dose |
| 9 | **What if the verifier shares the same false assumption?** | 🔴 **Largest gap in the corpus** |
| 10 | Should agents reason independently before seeing peers? | 🟢 Yes — for homogeneous teams |
| 11 | How does prompt structure affect cascades? | 🟢 More than expected (d = +1.43 to +1.99) |
| 12 | How long does contaminated memory persist? | 🔴 Open — corpus n=1 |
| 13 | How is goal drift measured in long-running systems? | 🔴 Open — no validated metric |
| 14 | Does model heterogeneity reduce error correlation? | 🟢 Yes — most consistent finding |
| 15 | Are agents from one foundation model genuinely independent? | 🟢 **No** — confabulation consensus |

---

## Literature

**40 papers**, spanning 2023–2026, verified against the source PDFs.

| Category | Papers | Focus |
|---|---|---|
| [`multi-agent-debate`](papers/multi-agent-debate) | 9 | Debate as method — foundations and critiques |
| [`error-propagation`](papers/error-propagation) | 8 | Propagation dynamics, topology, contagion |
| [`verification`](papers/verification) | 7 | Verifier placement, aggregation beyond voting |
| [`consensus-conformity`](papers/consensus-conformity) | 6 | False consensus, sycophancy, persuasion |
| [`hallucination-cascade`](papers/hallucination-cascade) | 4 | Direct cascade studies |
| [`general-mas-reliability`](papers/general-mas-reliability) | 3 | Failure taxonomies, reliability science |
| [`context-goal-drift`](papers/context-goal-drift) | 2 | State divergence, behavioral degradation |
| [`memory-contamination`](papers/memory-contamination) | 1 | ⚠️ Corpus gap — see below |

**The field's arc**, which is itself the story: *2023–2024 optimism* (`2305.14325` "society of minds") → *2025 systematic doubt* (`2502.08788`, `2503.13657`) → *2026 mechanism* (propagation dynamics, phase transitions, stability thresholds).

- **[`research/paper-index.md`](research/paper-index.md)** — all 40, with research question, method, findings, limitations, and verification status
- **[`research/literature-review.md`](research/literature-review.md)** — synthesis organized by argument, including the contradictions
- **[`research/terminology.md`](research/terminology.md)** — 15 concepts, each with definition, distinction, metrics, and sources
- **[`research/threat-model.md`](research/threat-model.md)** — the security view: attack surface, graded attack classes, defensive controls
- **[`sources/source-validation.md`](sources/source-validation.md)** — how everything was checked
- **[`sources/media-sources.md`](sources/media-sources.md)** — non-academic sources (context only, never evidence)

### 📄 A note on the PDFs

**The paper PDFs are not stored in this repository.** arXiv's default licence grants arXiv distribution rights, not third-party redistribution rights. Each entry in the index carries its arXiv ID and link; `papers/` holds the category structure so a local corpus can be rebuilt in place. See [`sources/source-validation.md`](sources/source-validation.md).

---

## Security

The same phenomena, read as an attack surface rather than a reliability problem — in [`research/threat-model.md`](research/threat-model.md).

This is not a rebrand. **Four of the 40 papers are classified `cs.CR` (Cryptography and Security) by their own authors** — including both of the corpus's most direct hallucination-cascade papers (`2606.07937`, `2606.07941`).

**The load-bearing insight:** `2606.16710` shows misinformation propagating in **benign** systems with no attacker at all, while `2603.04474` weaponizes the identical mechanism. The natural failure rate is the attacker's proof-of-concept — so reliability hardening and security hardening are the same work.

**The trust boundary nobody enforces:**

> **Peer agent output is untrusted input.**

A peer's claim enters the next agent's context as ordinary text, indistinguishable from a user fact unless provenance is tracked. And the bias runs the wrong way: `2608.03421` found **false testimony is adopted more readily than truthful testimony** — then kept propagating through honest agents **after the deceiver left the conversation**. Removing the attacker does not remediate the system.

Attack classes are graded by what the corpus actually demonstrates:

| | Class | Grade |
|---|---|---|
| A1 | Error seed injection — one claim is the entire payload | 🔴 Demonstrated |
| A2 | False testimony — truth recovery 72.50% → 14.17% | 🔴 Demonstrated |
| A3 | Sycophancy exploitation — conformity high at just K=2 peers | 🟠 Evidenced |
| A4 | Consensus manipulation — phase transition driven by temperature | 🟠 Evidenced |
| A7 | Topology/contagion — epidemic model, invasion thresholds | 🟠 Evidenced |
| A5 | Memory poisoning | 🟡 Plausible |
| A6 | Verifier subversion | 🟡 Plausible |
| A8 | **Prompt injection** | ⚫ **Not covered — zero papers** |

> **⚠️ Do not cite this repository as evidence about prompt injection.** The corpus covers a false *claim* being believed, not a false *instruction* being obeyed. Acquiring that literature is the security track's top priority.

The security article for this track is outlined in [`article/security-article-outline.md`](article/security-article-outline.md).

---

## Experiments

**No experiment has been run. No results exist in this repository.** Scaffolding and designs only.

The framework is deliberately minimal — plain Python with a provider abstraction, no orchestration library, because the orchestration *is* the object of study.

**Two architectures under comparison:**

```text
A:  Agent A ──▶ Agent B ──▶ Agent C ──▶ Verifier

B:  Agent A ─┐
    Agent B ─┼──▶ Independent Answers ──▶ Judge / Aggregator
    Agent C ─┘
```

| Experiment | Question | Key metric |
|---|---|---|
| [01 — Error propagation](experiments/experiment-01-error-propagation) | RQ3 — what determines amplification direction? | Adoption probability, amplification factor |
| [02 — Context drift](experiments/experiment-02-context-drift) | RQ13 — how is goal drift measured? | CDS, semantic distance from goal |
| [03 — Consensus collapse](experiments/experiment-03-consensus-collapse) | RQ5, RQ15 — voting and independence | Oracle gap, inter-agent error correlation |
| [⭐ 04 — Verifier agent](experiments/experiment-04-verifier-agent) | RQ9 — verifier shares the false premise | Verifier failure rate under shared context |

**Experiment 04 is the recommended starting point** — it targets the corpus's largest gap at the lowest cost.

```bash
cp experiments/.env.example experiments/.env
```

```bash
python -m framework.runner --help
```

No API key is required to inspect the scaffolding; the `echo` provider exercises the wiring offline.

---

## Repository structure

```text
multi-agent-hallucination-research/
├── papers/                  # 40 papers in 8 categories (PDFs gitignored)
├── research/
│   ├── research-map.md      # working hypothesis, architectures, metrics
│   ├── literature-review.md # synthesis by argument
│   ├── terminology.md       # 15 concepts, precisely distinguished
│   ├── threat-model.md      # security view: attack classes, controls
│   ├── open-research-questions.md
│   └── paper-index.md       # the verified 40-paper index
├── experiments/
│   ├── framework/           # types, metrics, providers, runner
│   └── experiment-01..04/   # designs with pre-registered predictions
├── benchmarks/              # existing benchmarks + what's missing
├── diagrams/                # figure sources
├── article/                 # outlines (reliability + security), draft, figures
├── notes/                   # working notes, project origin
└── sources/                 # verification methodology, media sources
```

---

## Current status

**Phase: literature analysis complete, experiments designed, none run.**

| | |
|---|---|
| ✅ | 40 papers collected, categorized, verified against source PDFs |
| ✅ | 39/40 arXiv IDs confirmed from in-document stamps; 1 flagged |
| ✅ | Zero duplicates (byte-level and near-duplicate checks) |
| ✅ | Terminology, literature synthesis, research questions written |
| ✅ | Experiment framework scaffolded; four experiments designed |
| ✅ | Security threat model written; attack classes graded by evidence |
| ⬜ | Full-text reading pass (index entries marked `TODO`) |
| ⬜ | Provider adapters implemented |
| ⬜ | Any experiment run |
| ⬜ | Article written |

**What this repository does not contain:** experimental results, reproduced findings, or claims beyond what the cited papers state.

---

## Roadmap

**Phase 1 — Literature** ✅ *complete*
Corpus verification, categorization, terminology, synthesis, research questions.

**Phase 2 — Deep reading** ⬜ *next*
Full texts of the 12 priority papers. Fill every `TODO` in the index. Extract methodologies and stated limitations.

**Phase 3 — First experiment** ⬜
Implement one provider adapter. Run experiment-04 arms A vs B: verifier failure rate under shared vs asymmetric context. Report with confidence intervals and cost.

**Phase 4 — Propagation benchmark** ⬜
Claim-level ground truth, injectable seeds, provenance tracking, paired control arms.

**Phase 5 — Articles** ⬜
Two technical articles grounded in the literature and this repository's own results: the reliability piece ([`article-outline.md`](article/article-outline.md)) and the security piece ([`security-article-outline.md`](article/security-article-outline.md)).

**Security track — parallel** ⬜
Acquire prompt-injection literature (corpus coverage is currently zero), then map attack classes onto the current OWASP LLM Top 10 and MITRE ATLAS.

---

## Contributing

Contributions welcome — especially full-text readings that close `TODO` entries, and reproductions.

**Standards** (from [`sources/source-validation.md`](sources/source-validation.md)):

1. **Read the PDF** before adding a paper. Never add from a title or citation alone.
2. **Verify the arXiv ID** against the in-document stamp; flag it if absent.
3. **Transcribe numbers exactly**, and state whether they came from the abstract or the full text.
4. **Use `TODO` for unknowns.** Never guess a year, author, or result.
5. **Flag weak evidence** — simulation-only, non-peer-reviewed, unusual venue.
6. **Report cost alongside accuracy** in any experimental result.
7. **Publish negative results.** The most valuable papers in this corpus are negative.

---

## Disclaimer

This is an **independent research repository in its literature phase**.

- The core hypothesis chain is a **working research model**, explicitly not an established finding.
- **No experimental results are reported here**, because none have been produced.
- All numeric findings are **transcribed from the cited papers' abstracts** and have not been independently reproduced.
- The corpus is **not exhaustive**. This field is moving quickly, and 2026 work is appearing faster than it can be catalogued.
- Papers are cited under their own licences; this repository does not redistribute them.
- Where evidence is thin, contested, or simulation-based, it is **labelled as such** rather than smoothed over.

If you find an error, an unsupported claim, or a misrepresented finding, please open an issue. Accuracy matters more here than completeness — the failure mode this project studies is precisely the one it must avoid.

---

## License

[MIT](LICENSE) for the original content of this repository — research notes, taxonomy, synthesis, and code.

The referenced academic papers remain the property of their respective authors and publishers under their own licences.
