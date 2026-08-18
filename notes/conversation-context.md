# Conversation Context

Preserved origin of this research programme — the working conversation and the intent that produced the corpus.

> **Provenance.** Carried over verbatim from the original `HLC/` working folder (`conversation/00_FULL_CONVERSATION_CONTEXT.md`). Quoted user messages are informal Turkish notes reproduced as written; the "normalized intent" blocks are cleaned-up restatements.
>
> **Status.** This is a record of how the project started, not a statement of current findings. Where it conflicts with [`../research/`](../research/), the research files are authoritative — in particular, the framing below predates the discovery that `2606.07937` measured cascade *attenuation* rather than amplification.

---


## Project
**HLC = Hallucination Cascade / Multi-Agent LLM Reliability Research**

This file preserves the visible working conversation and the research intent that led to the HLC corpus.

---

## 1. Initial research idea

### User
> aget halusoaslyonu yenı llm modelerınden bırden fazla gent clasırken konudan sapıyor bunun la ılgılı bır makale yazacam gorsel oslutur lınkdınden paysacagım 1. bırden fazla agent a prom tu ıyı vermek alzım ort aderecem bır makale ols

### Normalized intent
The goal is to write a medium-to-advanced LinkedIn article about hallucination and topic/goal drift in multi-agent LLM systems, especially when multiple agents collaborate and errors propagate between them. The article should also cover how prompts, role boundaries, context boundaries, validation, and coordination should be designed when several agents work together.

---

## 2. Naming the phenomenon

### User
> son zamanlaın konusu bu agent dunyası cunku bunun bır ısmı varmı

### Working terminology identified
The discussion converged on these related terms:

- **Hallucination Cascade** — a hallucination/error produced by one agent propagates into downstream agents.
- **Error Propagation** — broader systems term for local errors spreading through a multi-agent workflow.
- **Collective / Group Hallucination** — multiple agents converge on or reinforce the same false belief.
- **Context Drift** — agent state or generated content drifts away from the original grounding/context.
- **Goal Drift / Agent Drift** — the system gradually optimizes for a different objective than the original user goal.
- **Consensus Collapse / Consensus Amplification** — repeated agreement gives false claims increased apparent credibility.
- **Sycophantic Conformity** — agents conform to other agents' assertions rather than independently verifying them.
- **Cascading Failure** — hallucination or reasoning error eventually causes tool, workflow, or decision failure.

### Candidate article title
**Hallucination Cascade in Multi-Agent LLM Systems: Why Agents Drift From the Original Goal**

Turkish working title:
**Multi-Agent LLM Sistemlerinde Hallucination Cascade: Agentlar Neden Ana Hedeften Sapıyor?**

### Core failure chain

`Hallucination → Propagation → Reinforcement → Context/Goal Drift → Cascading Failure`

### Conceptual example

`USER GOAL → AGENT 1 → AGENT 2 → AGENT 3 → AGENT 4`

A small unsupported assumption introduced by Agent 1 is accepted by Agent 2, expanded by Agent 3, and may be treated as an established fact by Agent 4. The final answer can therefore be far from the original user objective even though every individual agent output looks locally plausible.

---

## 3. Request for a deep research corpus

### User
> tmm bu konu ıle ıgılı byuk derecem makale ıcın bana alt yapı olsutur arasıtıma alzım butun arsix makelelemasa ustune at banaam snr aonları derlrım buradna farklı konualr var buyuk konu senden kendını gslıtırmsı oluyorsun bu asamamda bılemdıgın bır konu cunku

### Normalized research scope
Build a broad research foundation before writing the article. Collect papers and organize them by subtopic rather than treating the problem as only generic LLM hallucination.

Research tracks:

1. Multi-agent hallucination and hallucination cascades
2. Error propagation and cascading failure
3. Context drift / goal drift / agent drift
4. Collective hallucination and misinformation propagation
5. Multi-agent debate, consensus, conformity, sycophancy
6. Verification, critics, judges, self-check, uncertainty propagation
7. Communication topology and information propagation
8. Memory/context contamination
9. Tool-using agent reliability and agentic RAG
10. Reliability measurement, auditing, and failure taxonomy

The corpus in `../papers/` was assembled around these tracks.

---

## 4. HLC folder request

### User
> evet hersyeı masa ustune at dosya olsutur hlc diye

### Result
A local working folder named **HLC** was created containing a 40-paper corpus plus research mapping, categorized index, validation, and supporting notes.

---

## 5. User's requested deliverable labels

### User
> ### Dosyalar
>
> **Hepsini tek seferde indir:**
>  📦 Agent Hallucination / Multi-Agent Research Corpus 2026 — 40 PDF
>
> Ayrıca hazırladığım çalışma altyapısı:
>
> 📘 Research Map + Makale Altyapısı
>
> 📚 40 Makalenin Kategorize Edilmiş İndeksi
>
> ✅ PDF Doğrulama Raporu bu ve yarım kalan konusmanın hepsını hlc ye at olsutu mkdir ıle

### Action taken
The HLC folder was reorganized with `mkdir` into explicit subdirectories and this conversation context was added so the research can be resumed later without losing the original purpose.

---

## 6. Main article thesis to preserve

The article should not argue merely that “LLMs hallucinate.” The stronger thesis is:

> **In multi-agent systems, reliability is not the average reliability of the participating agents. Errors become messages. Messages become context. Context becomes evidence. Repeated evidence can become consensus, and consensus can move the entire system away from the original goal.**

This creates a systems-level reliability problem that is different from single-model hallucination.

Important design questions for the eventual article:

- How should prompts be decomposed across agents?
- Should every agent receive the entire original prompt, or only its scoped task plus invariant constraints?
- Which context should be immutable?
- How should provenance be preserved between agents?
- When should an agent treat another agent's output as evidence versus a hypothesis?
- Should agents independently solve before seeing peer answers?
- How can confidence and uncertainty be propagated rather than hidden?
- When should a verifier/judge be introduced?
- Can majority vote amplify a shared error?
- How do homogeneous models create correlated failure?
- What communication topology minimizes error propagation?
- How does long-running memory contaminate downstream reasoning?
- What metrics measure drift from the original goal?

These questions are the backbone for the next research/writing phase.
