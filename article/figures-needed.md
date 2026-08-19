# Figures Needed

Diagrams for the article. Source files go in [`../diagrams/`](../diagrams/).

**Rule:** no figure may present this repository's working hypothesis as an established finding, and no figure may show fabricated data. Figures plotting numbers must cite the paper the numbers come from.

| # | Figure | Purpose | Priority | Data source |
|---|---|---|---|---|
| 1 | **The cascade chain** | The working hypothesis, front and centre | **High** | Own model — must be labelled "working hypothesis" |
| 2 | **Two trajectories** | Same seed, two outcomes: amplification vs recovery. The article's core idea | **High** | Own model — conceptual |
| 3 | **Architecture A vs B** | Chain+verifier vs independent+judge | **High** | Own model |
| 4 | **Amplification factor comparison** | `2606.07937` (0.644, attenuation) beside `2608.03421` (72.50%→14.17%) | **High** | Cited papers — label each bar with its arXiv ID |
| 5 | **Oracle gap** | Correct answer in pool, discarded by voting | **High** | `2605.00914` (up to 32.3 pp) |
| 6 | **Topology vs error propagation** | Chain / star / mesh / sparse, with the "moderately sparse" optimum | Medium | `2505.23352` — schematic unless reproducing their numbers |
| 7 | **Target architecture** | Immutable goal → independent pass → ledger → verifier → verified memory | **High** | Own proposal |
| 8 | **Provenance envelope** | The JSON message contract, annotated | Medium | Own design |
| 9 | **Consensus illusion** | Agreement rising while reasoning similarity falls | Medium | `2606.08457` — schematic |
| 10 | **Verifier confirmation bias** | Verifier inheriting the generator's premise; asymmetric alternative | Medium | `2603.24579` — conceptual |
| 11 | **Three consensus mechanisms** | Sycophancy vs confabulation vs collapse, side by side | Medium | `2605.00914`, `2602.09341` |
| 12 | **Corpus timeline** | 2023 optimism → 2025 doubt → 2026 mechanism | Low | This corpus |
| 13 | **Trust boundary diagram** | Where agent→agent sits; which boundaries are enforced by default | **High** (security) | Own — `threat-model.md` §2 |
| 14 | **Persistence after removal** | Truth recovery 72.50%→14.17%; belief surviving the deceiver's exit | **High** (security) | `2608.03421` |
| 15 | **Attack-class grading** | A1–A8 by demonstrated / evidenced / plausible / out-of-corpus | Medium | Own — `threat-model.md` §3 |
| 16 | **Nominal vs real quorum** | 3 same-model agents rendered as one correlated vote | Medium | `2602.09341`, `2608.00243` |

## Style

- Readable at LinkedIn's inline width, and on mobile.
- Legible in greyscale — do not encode meaning in colour alone.
- Consistent visual language: **red** = error/unverified, **green** = verified, **grey** = neutral state.
- Label every axis. Every figure carrying data cites its source in the caption.
- Prefer one clear idea per figure over a dense composite.

## Captions must state provenance

Three honest patterns:

- `Figure 1 — Working hypothesis. This is our research model, not an established result.`
- `Figure 4 — Reported amplification factors. Source: arXiv 2606.07937, 2608.03421. Not independently reproduced.`
- `Figure 3 — Architectures compared in this repository's experiments. No results yet.`
