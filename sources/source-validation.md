# Source Validation

How the 40-paper corpus was verified, what was confirmed, and what was not.

> **Non-academic sources** (videos, talks, industry reports) are recorded separately in [`media-sources.md`](media-sources.md). They are context, never evidence.

---

## Why PDFs are not in this repository

The corpus is **not redistributed here**. `papers/` contains the category structure; the PDFs are gitignored.

**Reason.** arXiv's default submission licence — the *arXiv.org perpetual, non-exclusive license* — grants arXiv the right to distribute, **not third parties the right to redistribute**. Individual papers may carry CC-BY or similar, but that has to be checked per paper. Republishing 40 PDFs on a public repository without that check is a copyright risk with no research benefit, since every paper is one click away by arXiv ID.

**To rebuild the corpus locally:** each entry in [`../research/paper-index.md`](../research/paper-index.md) carries its arXiv ID and link. Download into `papers/<category>/`; `.gitignore` keeps them untracked.

**To publish them anyway:** verify each paper's licence individually, then remove the `papers/**/*.pdf` and `*.pdf` lines from `.gitignore`. That is a deliberate decision, not a default.

---

## Verification method

Every entry in the paper index was produced from **the actual PDF**, not from memory, a search engine, or a citation database:

1. `pdftotext` extraction of page 1 for all 40 files (all 40 yielded extractable text — no scanned/image-only PDFs).
2. Title and authors read directly from the extracted front matter.
3. arXiv ID, version, primary class, and date read from the in-document `arXiv:<id>v<n> [class] <date>` stamp.
4. That stamp compared programmatically against the ID in the filename.
5. Abstracts extracted for content summaries.
6. Duplicate detection by MD5 of PDF bytes and by normalized body-text signature.

---

## Results

### arXiv ID verification

| Result | Count |
|---|---|
| In-document arXiv stamp present **and matching the filename** | **39 / 40** |
| No in-document stamp — ID unconfirmed | **1 / 40** |
| Stamp present but **mismatching** the filename | **0** |

**The exception: `2410.12853`** — *Diversity of Thought Elicits Stronger Reasoning Capabilities in Multi-Agent Debate Frameworks* (Mahmood Hegazy).

The PDF is the **journal version**, published in *Journal of Robotics and Automation Research* 5(3), 01-10, dated 2024-12-13. It carries an ISSN and a citation block but **no arXiv stamp**. The arXiv ID in the filename could not be confirmed from the document. It is flagged inline in the paper index.

> **Action required before citing:** confirm the arXiv ID independently, or cite the journal version. Also check the venue's review standards before treating it as strong evidence.

### Duplicate detection

| Check | Result |
|---|---|
| Byte-identical PDFs (MD5) | **0 duplicates** |
| Near-duplicate body text (normalized signature) | **0 duplicates** |
| Same paper filed under two categories | **0** — each PDF has exactly one primary category |

**One related-work pair worth noting** (not duplicates): `2606.07937` (*Hallucination Cascade*) and `2606.07941` (*Collective Hallucination*) share a first author (Saeid Jamshidi) and have near-consecutive arXiv IDs, indicating simultaneous submission. They are distinct papers with different methods and results, but they are **not independent evidence** — treat them as one research programme when weighing corroboration.

### Extraction completeness

| Field | Coverage |
|---|---|
| Title | 40 / 40 read from the document |
| Authors | 40 / 40 read from the document |
| Abstract | 40 / 40 (3 needed a fallback extraction path) |
| Explicit "Limitations" section detected | 19 / 40 |
| Full text read end to end | **0 / 40** |

---

## What is verified, and what is not

### ✅ Verified
- Paper titles, as printed on the documents
- Author names and affiliations, as printed
- arXiv IDs (39/40) and version/date stamps
- Absence of duplicates
- Category assignments (each paper in exactly one)

### ⚠️ Transcribed but not independently checked
- **Numeric findings.** Every figure in the index comes from the paper's own abstract. None has been reproduced, and abstract numbers are sometimes the paper's best case.
- **Method descriptions.** Summarized from abstracts, not from reading the methods sections.

### ❌ Not verified
- **Full texts.** No paper has been read end to end. Entries marked `TODO: read full text` are open work.
- **Limitations.** Present for only a minority of entries; where absent, the field says so rather than inventing one.
- **Whether papers are peer-reviewed.** Assume arXiv preprint status unless a venue is stated. `2604.02923` self-identifies as a technical report; `2603.13325` is an ICLR 2026 workshop paper.
- **Reproducibility.** No result in this corpus has been reproduced here.

---

## Evidence-strength flags

Applied in the paper index where warranted:

| Paper | Flag | Reason |
|---|---|---|
| `2601.04170` | **EVIDENCE STRENGTH: low (simulation/theory)** | Simulation and theory only; single independent researcher; abstract hedged ("could lead to", "theoretical analysis suggesting"). Useful vocabulary, not empirical evidence. |
| `2604.02923` | **EVIDENCE STRENGTH: low (non-peer-reviewed)** | Self-described technical report; degree titles instead of institutional affiliations; no institution; currently v4. |
| `2607.21912` | **theoretical** | Analytic model + simulation, not measurements on live LLM agents. |
| `2410.12853` | **PARTIALLY VERIFIED** | arXiv ID unconfirmed; venue standards should be checked. |
| `2603.13325` | note | Workshop paper — lighter review. |

---

## PDF integrity check

Carried over from the original working folder's `reports/PDF_VALIDATION_REPORT.txt`, cross-referenced against this repository's categories.

All **40 PDFs** opened cleanly and yielded extractable text — no scanned or image-only documents, no corrupt files. Total **830 pages**.

Page counts are recorded so a rebuilt local corpus can be checked against the one this repository's analysis was written from. A mismatch means a different version of the paper, and any transcribed number should be re-checked.

| arXiv | Pages | Category | File |
|---|---|---|---|
| `2305.14325` | 27 | `multi-agent-debate` | 2305.14325_Improving_Factuality_Multiagent_Debate.pdf |
| `2308.07201` | 16 | `multi-agent-debate` | 2308.07201_ChatEval.pdf |
| `2309.13007` | 20 | `multi-agent-debate` | 2309.13007_ReConcile.pdf |
| `2406.03075` | 18 | `multi-agent-debate` | 2406.03075_Markov_Chain_Multi_Agent_Hallucination_Detection.pdf |
| `2406.11776` | 13 | `error-propagation` | 2406.11776_Sparse_Communication_Multi_Agent_Debate.pdf |
| `2410.12853` | 10 | `multi-agent-debate` | 2410.12853_Diversity_of_Thought_Multi_Agent_Debate.pdf |
| `2502.08788` | 33 | `multi-agent-debate` | 2502.08788_Stop_Overvaluing_Multi_Agent_Debate.pdf |
| `2503.01829` | 25 | `consensus-conformity` | 2503.01829_Persuade_Me_if_You_Can.pdf |
| `2503.13657` | 47 | `general-mas-reliability` | 2503.13657_Why_Do_Multi_Agent_LLM_Systems_Fail.pdf |
| `2505.23352` | 14 | `error-propagation` | 2505.23352_Information_Propagation_Communication_Topologies.pdf |
| `2505.23840` | 21 | `consensus-conformity` | 2505.23840_Measuring_Sycophancy_Multi_Turn_Dialogues.pdf |
| `2509.18970` | 22 | `general-mas-reliability` | 2509.18970_LLM_Agents_Hallucination_Survey.pdf |
| `2511.07784` | 20 | `multi-agent-debate` | 2511.07784_Can_LLM_Agents_Really_Debate.pdf |
| `2511.11182` | 13 | `verification` | 2511.11182_Multi_Agent_Undercover_Gaming.pdf |
| `2601.04170` | 12 | `context-goal-drift` | 2601.04170_Agent_Drift.pdf |
| `2601.04742` | 13 | `multi-agent-debate` | 2601.04742_Tool_MAD.pdf |
| `2601.22984` | 29 | `hallucination-cascade` | 2601.22984_Deep_Research_Agent_Hallucination_Trajectory.pdf |
| `2602.09341` | 20 | `verification` | 2602.09341_Auditing_Multi_Agent_Reasoning_Trees.pdf |
| `2602.16666` | 52 | `general-mas-reliability` | 2602.16666_Towards_a_Science_of_AI_Agent_Reliability.pdf |
| `2603.04474` | 20 | `error-propagation` | 2603.04474_From_Spark_to_Fire_Error_Cascades.pdf |
| `2603.13325` | 16 | `error-propagation` | 2603.13325_Auditing_Cascading_Risks.pdf |
| `2603.15408` | 17 | `verification` | 2603.15408_TrinityGuard.pdf |
| `2603.24579` | 26 | `verification` | 2603.24579_MARCH_Multi_Agent_Reinforced_Self_Check.pdf |
| `2604.02923` | 24 | `verification` | 2604.02923_Council_Mode.pdf |
| `2604.23505` | 29 | `error-propagation` | 2604.23505_Uncertainty_Propagation_in_LLM_Systems.pdf |
| `2605.00914` | 19 | `consensus-conformity` | 2605.00914_The_Cost_of_Consensus.pdf |
| `2606.04435` | 14 | `hallucination-cascade` | 2606.04435_CHARM_Agentic_RAG.pdf |
| `2606.07937` | 20 | `hallucination-cascade` | 2606.07937_Hallucination_Cascade.pdf |
| `2606.07941` | 19 | `hallucination-cascade` | 2606.07941_Collective_Hallucination.pdf |
| `2606.08457` | 20 | `consensus-conformity` | 2606.08457_The_Consistency_Illusion.pdf |
| `2606.16710` | 21 | `error-propagation` | 2606.16710_Misinformation_Propagation_in_Benign_MAS.pdf |
| `2606.21666` | 11 | `context-goal-drift` | 2606.21666_Hallucination_as_Context_Drift.pdf |
| `2606.24976` | 12 | `memory-contamination` | 2606.24976_Compounding_Failures_Agentic_Persuasion.pdf |
| `2606.27409` | 20 | `verification` | 2606.27409_Delayed_Verification_Destabilizes_Belief.pdf |
| `2607.21912` | 13 | `error-propagation` | 2607.21912_Reliability_Contagion_Feasibility.pdf |
| `2607.26212` | 35 | `multi-agent-debate` | 2607.26212_Multi_Agent_Debate_Strategies_Survey.pdf |
| `2607.26836` | 12 | `verification` | 2607.26836_Before_Agents_Speak_Pre_hoc_Failure_Risk.pdf |
| `2608.00243` | 15 | `consensus-conformity` | 2608.00243_Structural_Limits_Homogeneous_Multi_Agent_Groundedness.pdf |
| `2608.02827` | 23 | `consensus-conformity` | 2608.02827_Emergence_of_Biased_Consensus.pdf |
| `2608.03421` | 19 | `error-propagation` | 2608.03421_When_Truth_Is_Distributed.pdf |

**Total: 40 files, 830 pages.** Verified with `pdftotext`; every file produced text.

---

## Standards for adding a paper

1. **Read the PDF.** Do not add from a title or a citation.
2. **Confirm the arXiv ID** against the in-document stamp. If absent, flag it as unverified — do not assume.
3. **Check for duplicates**, including different versions of the same work.
4. **Assign exactly one primary category**; use tags for cross-cutting themes.
5. **Fill every index field.** Use `TODO` where unknown — never guess a year, author, or result.
6. **Transcribe numbers exactly**, and say where they came from (abstract vs full text).
7. **Flag weak evidence** — simulation, non-peer-reviewed, single-author-no-affiliation, unusual venue.
8. **Record limitations**, including the authors' own stated ones.

## Things this repository will not do

- Invent a paper title, author, DOI, or arXiv ID
- Report a finding not present in a cited paper
- Present a working hypothesis as an established result
- Cite a paper nobody here has opened
- Report an experimental result that was not run
