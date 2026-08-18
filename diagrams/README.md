# Diagrams

Source files for figures used in the article and documentation.

> **Status: empty.** Figures are specified in [`../article/figures-needed.md`](../article/figures-needed.md) but not yet drawn.

## Conventions

**Format.** Prefer text-based sources that diff cleanly in git — Mermaid, Graphviz, or hand-written SVG. Export PNG for LinkedIn; keep the source alongside it.

```text
diagrams/
├── 01-cascade-chain.mmd        # source
├── 01-cascade-chain.png        # export
└── ...
```

Number files to match the table in `figures-needed.md`.

**Visual language.**

| Element | Meaning |
|---|---|
| 🔴 Red | Error, unverified, contaminated |
| 🟢 Green | Verified, grounded |
| ⚪ Grey | Neutral state |
| Solid arrow | Message passing |
| Dashed arrow | Verification / audit path |

Legible in greyscale — never encode meaning in colour alone.

## Provenance rule

Every diagram must make its epistemic status obvious:

- **Working hypothesis** → caption it as such. The cascade chain is a research model, not a finding.
- **Data from a paper** → cite the arXiv ID in the caption.
- **Own proposal** → say so.

**Never plot fabricated data**, including as a "for illustration" placeholder that could be mistaken for a measurement. If a shape is illustrative, remove the axis numbers.

## Starting point

The ASCII diagrams in [`../research/research-map.md`](../research/research-map.md) are ready to be redrawn: the cascade chain (§1), Architectures A and B (§3), and the target architecture (§3).
