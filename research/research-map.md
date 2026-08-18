# Research Map

The organizing model, hypotheses, and experimental design space for this repository.

---

## 1. The working hypothesis

This is the chain this project exists to **test**. It is a research model, not a finding.

```text
                    Initial User Goal
                            │
                            ▼
                        Agent 1
                            │
                            ▼
          Small reasoning / factual error
                            │
                            ▼
            Agent 2 accepts it as context
                            │
                            ▼
           Agent 3 reinforces the assumption
                            │
                            ▼
            Consensus / false confidence
                            │
                            ▼
              Context & Goal Drift
                            │
                            ▼
              Hallucination Cascade
                            │
                            ▼
            Cascading System Failure
```

> ### ⚠️ Status of this chain: **WORKING HYPOTHESIS — NOT AN ESTABLISHED RESULT**
>
> No paper in this corpus demonstrates this full chain end to end. It is assembled from separately-evidenced fragments, and **at least one link is contradicted by direct evidence**:
>
> - `2606.07937` — the corpus's most direct cascade study — measured net **attenuation** across 3-agent chains (amplification factor **0.644**), not amplification. Factual accuracy nonetheless declined.
> - `2502.08788` found multi-agent debate often **fails to beat** single-agent baselines, which cuts against the premise that more agents is the default failure driver.
>
> The chain is therefore best read as **one trajectory a system can take**, not the trajectory it takes by default.

### The competing trajectory, which is equally well evidenced

```text
Error Seed ──▶ Critique ──▶ Verification ──▶ Correction ──▶ Recovery
```

**The actual research question is not "does the bad chain happen?" but "what determines which of the two chains a system follows?"**

That reframing is the intellectual core of this repository. The candidate determinants — each independently supported in the corpus — are:

| Determinant | Evidence |
|---|---|
| Communication topology | `2505.23352` (moderately sparse best), `2406.11776`, `2607.21912` |
| Model heterogeneity | `2502.08788` ("universal antidote"), `2604.02923`, `2309.13007` |
| Verification timing & dose | `2606.27409` (too strong or too delayed → oscillation) |
| Verifier independence | `2603.24579` (confirmation bias; information asymmetry as fix) |
| Aggregation rule | `2602.09341` (reasoning-tree audit > majority vote), `2605.00914` |
| Grounding / evidence access | `2601.04742`, `2606.27409` (grounding makes truth an absorbing boundary) |
| Context-sharing policy | `2606.21666`, `2505.23352` |
| Prompt & role design | `2606.08457` (GDP, d=+1.43 to +1.99), `2607.26836` (role–task misalignment predicts risk) |

---

## 2. Decomposing the chain into testable links

Each arrow in the hypothesis is a separate empirical claim with its own evidence status.

| # | Link | Claim | Evidence status |
|---|---|---|---|
| L1 | Goal → Agent 1 error | Agents introduce unsupported premises at a measurable rate | **Well established** — `2509.18970` |
| L2 | Error → Agent 2 adopts | Downstream agents accept upstream claims as context | **Strong** — `2608.03421` (false testimony adopted *more* readily than true), `2606.16710` |
| L3 | Adoption → reinforcement | Repetition increases apparent credibility without adding evidence | **Moderate** — `2606.07941`, `2608.00243` (round 2 adds little semantic novelty) |
| L4 | Reinforcement → false consensus | The group locks onto the wrong answer | **Strong** — `2605.00914` (oracle gap 32.3 pp), `2608.02827` (phase transition), `2602.09341` |
| L5 | Consensus → drift | State/goal moves away from the original | **Weak–moderate** — `2601.04170` is *simulation-based*; `2606.21666` is empirical but small-n |
| L6 | Drift → cascade | Drift produces compounding hallucination | **Contested** — `2606.07937` measured attenuation; `2603.04474` measured widespread failure from one seed |
| L7 | Cascade → system failure | Epistemic error becomes operational failure | **Strong** — `2503.13657` (1600+ traces, κ=0.88), `2602.16666` (real incidents) |

**The weakest links are L5 and L6** — precisely the middle of the chain, and precisely where this repository's experiments are aimed.

---

## 3. Two architectures under comparison

Everything in `experiments/` compares these two shapes.

### Architecture A — Sequential chain with terminal verification

```text
  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐
  │ Agent A │───▶│ Agent B │───▶│ Agent C │───▶│ Verifier │
  └─────────┘    └─────────┘    └─────────┘    └──────────┘
       │              │              │               │
   introduces     inherits A     inherits A+B    sees only
    a claim        as context      as context     the end
```

**Predicted weakness.** Verification arrives after false context has accumulated. `2606.27409` shows delayed correction can destabilize belief rather than fix it, with the worst regime when communication and verification delays coincide.

### Architecture B — Independent-first, then adjudication

```text
  ┌─────────┐   ┌─────────┐   ┌─────────┐
  │ Agent A │   │ Agent B │   │ Agent C │    ← no peer visibility
  └────┬────┘   └────┬────┘   └────┬────┘
       └─────────────┼─────────────┘
                     ▼
            Independent Answers
                     │
                     ▼
          ┌─────────────────────┐
          │ Judge / Aggregator  │
          └─────────────────────┘
```

**Predicted weakness.** Independence removes conformity but not **correlated error**. If all three are the same model, `2602.09341`'s confabulation consensus applies and the judge sees three copies of the same bias. `2605.00914` found isolated self-correction *beat* homogeneous debate — supporting A-vs-B in favour of B — while `2502.08788` found heterogeneity is what actually rescues these systems.

**The interesting cell is the interaction:** independence × heterogeneity, which little in the corpus tests directly.

### Target architecture (this repo's proposal)

```text
        ┌──────────────────────────────┐
        │   Immutable User Goal        │  restated in every agent context
        └──────────────┬───────────────┘
                       ▼
              ┌─────────────────┐
              │    Planner      │
              └────────┬────────┘
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     ┌────────┐  ┌────────┐  ┌────────┐
     │Agent A │  │Agent B │  │Agent C │   independent first pass
     └───┬────┘  └───┬────┘  └───┬────┘
         └───────────┼───────────┘
                     ▼
          ┌────────────────────────┐
          │  Claim / Evidence      │   claims separated from evidence,
          │       Ledger           │   every claim carries provenance
          └───────────┬────────────┘
                      ▼
          ┌────────────────────────┐
          │  Independent Verifier  │   information-asymmetric (2603.24579)
          └───────────┬────────────┘
              ┌───────┴────────┐
              ▼                ▼
        verified state   contradiction
              │                │
    ┌─────────▼──────┐   ┌─────▼──────────┐
    │ Shared Memory  │   │ rollback /     │
    │ VERIFIED ONLY  │   │ re-retrieve    │
    └─────────┬──────┘   └────────────────┘
              ▼
       ┌─────────────┐
       │  Synthesis  │
       └─────────────┘
```

**Core engineering principle: do not make the chat transcript the database.** Treat inter-agent conversation as untrusted working state; promote only verified claims into durable memory.

---

## 4. Hypotheses

Proposed for testing. **None is an established law.**

| ID | Hypothesis | Rationale in corpus | Counter-evidence to respect |
|---|---|---|---|
| **H1** | Independent-first reasoning outperforms immediate peer visibility | `2605.00914` (isolated self-correction wins) | — |
| **H2** | Evidence lineage beats majority vote | `2602.09341` (up to +5 pp) | Gains are modest |
| **H3** | Early/per-transition verification beats terminal-only | `2606.27409` | Same paper: correction that is too *strong* also destabilizes |
| **H4** | Homogeneous agents have correlated failure modes | `2602.09341`, `2608.00243` | — |
| **H5** | Heterogeneity helps only if aggregation is evidence-aware | `2502.08788`, `2604.02923` | `2604.02923` is a non-peer-reviewed technical report |
| **H6** | Full-context broadcast increases contamination vs selective sync | `2505.23352` (moderately sparse best) | Sparsity also reduces beneficial diffusion |
| **H7** | An explicit dissent/falsification role improves epistemic diversity | `2602.09341` (ACPO rewards minority) | Untested directly |
| **H8** | Prompting is necessary but not sufficient | `2606.08457` (GDP works, d=+1.43–1.99), `2503.13657` | `2606.08457` shows prompt-level fixes can be *large* — do not understate them |

---

## 5. Metrics

The central methodological commitment: **final accuracy alone hides propagation dynamics.** Measure the trajectory.

### Cascade & propagation
| Metric | Definition | Source |
|---|---|---|
| Initial / final hallucination rate | Claim-level error at first vs last hop | `2606.07937` |
| **Amplification factor** | final ÷ initial (>1 amplify, <1 attenuate) | `2606.07937` |
| **Adoption probability** | P(downstream agent accepts injected false claim) | `2608.03421` |
| **Propagation depth** | Hops an error survives | `2603.04474` |
| **Recovery rate** / time-to-correction | Fraction of bad claims fixed before output | — |
| Persistence after source exit | Does the claim outlive its originator? | `2608.03421` |

### Consensus
| Metric | Definition | Source |
|---|---|---|
| **Oracle gap** | pass@N − final group accuracy | `2605.00914` |
| **Modal adoption rate** | How often an agent switches to the majority | `2605.00914` |
| **Vulnerability rate** | Correct→incorrect switches after peer exposure | `2605.00914` |
| False consensus rate | Group agrees, group is wrong | — |
| **Inter-agent error correlation** | Do agents fail on the same items? | `2602.09341` |

### Drift
| Metric | Definition | Source |
|---|---|---|
| **Context Divergence Score (CDS)** | Pairwise knowledge-state discrepancy | `2606.21666` |
| **Semantic distance from original goal** | Embedding distance, goal vs operative objective at hop n | *this repo* |
| Constraint retention rate | Original constraints still honoured at step n | *this repo* |
| **Agent Stability Index (ASI)** | 12-dimension composite | `2601.04170` |

### Verification
| Metric | Definition | Source |
|---|---|---|
| **Verifier correction rate** | Real errors caught | — |
| **Verifier failure rate** | Errors missed, *especially* those sharing the generator's premise | `2603.24579` |
| Verifier false-positive rate | Correct claims wrongly rejected | — |
| Oscillation onset | Does correction destabilize belief? | `2606.27409` |

### Cost
Token cost, latency, number of agent turns, **cost per corrected error**. `2605.00914` found debate consumed **2.1–3.4× more tokens** (up to 28,631 per problem) for equal or worse accuracy. A reliability intervention that triples cost for +2 pp must be reported as such.

---

## 6. Experiment matrix

| Dimension | Variants |
|---|---|
| Agent count | 1 / 3 / 5 |
| Models | homogeneous / heterogeneous |
| Topology | chain / star / mesh / sparse |
| Context sharing | full broadcast / selective / verified-only |
| First pass | independent / peer-visible |
| Verification | none / terminal-only / per-transition |
| Aggregation | majority / confidence-weighted / evidence-ledger |
| Memory | shared raw / shared verified / isolated |
| Prompt contract | minimal / role-specific / evidence-aware |
| Error seed | factual / instruction / tool output / stale state |

Full factorial is infeasible. `experiments/README.md` defines the prioritized subset.

---

## 7. The prompt contract

Ten requirements for a multi-agent prompt, derived from the corpus:

1. **Immutable goal** — restate the original task in every agent's context (counters goal drift)
2. **Role scope** — what the agent decides, and explicitly what it must not (`2607.26836`: role–task misalignment predicts failure)
3. **Input provenance** — label user facts, tool facts, retrieved evidence, and peer claims *separately*
4. **No implicit trust** — peer output is a hypothesis, not ground truth (`2608.03421`)
5. **Evidence requirement** — important claims carry a source ID (`2606.08457`'s GDP)
6. **Uncertainty field** — permit `unknown` / `insufficient_evidence` instead of forced completion (`2604.23505`)
7. **Contradiction handling** — define what happens when evidence conflicts with upstream context
8. **Dissent rule** — require at least one independent falsification pass before consensus
9. **State boundary** — only verified facts enter durable memory (counters contamination)
10. **Termination criteria** — stop on sufficient evidence, not on remaining round budget

### Message envelope

```json
{
  "original_goal": "immutable, restated every hop",
  "agent_role": "scoped responsibility",
  "claims": [
    {
      "claim": "...",
      "status": "verified | unverified | contradicted",
      "evidence_ids": ["src-001"],
      "confidence": 0.0,
      "origin_agent": "agent_a",
      "hop_introduced": 1
    }
  ],
  "assumptions": [],
  "open_questions": [],
  "recommended_next_action": "..."
}
```

The point: separate **claims from evidence**, **facts from assumptions**, and **local reasoning from shared system state**. `origin_agent` and `hop_introduced` are what make propagation depth measurable at all.

---

## 8. Corpus gaps

Where this corpus is thin — and therefore where original work has the most room:

1. **Memory contamination: n=1.** Only `2606.24976`, in the persuasion domain. Cross-session memory contamination is essentially unstudied here.
2. **Goal drift has no dedicated paper.** Only `2601.04170`'s semantic drift (simulation-based).
3. **Independence × heterogeneity interaction is untested.** `2605.00914` tests independence in homogeneous teams; `2502.08788` tests heterogeneity in peer-visible debate. The combined cell is open.
4. **Almost no cost-normalized comparison.** `2605.00914` is the exception. Most reliability gains are reported without the compute they cost.
5. **Verifier-shares-the-premise is barely studied.** `2603.24579` names confirmation bias; almost nothing measures what happens when the verifier inherits the *same* false assumption.
6. **Drift metrics are proposed, not validated.** CDS and ASI each appear in one paper, neither independently replicated.
