# Corpus Archive

**[`multi-agent-hallucination-corpus-40-papers.zip`](multi-agent-hallucination-corpus-40-papers.zip)** — 87 MB · 40 PDFs · 830 pages

The complete paper corpus behind this repository, in a single archive.

## Usage

Unzip over the repository root to place every PDF into its correct category folder:

```bash
unzip corpus/multi-agent-hallucination-corpus-40-papers.zip -d .
```

The loose PDFs remain gitignored after extraction — only this archive is tracked.

## Contents

| Category | Papers |
|---|---|
| [`multi-agent-debate`](../papers/multi-agent-debate) | 9 |
| [`error-propagation`](../papers/error-propagation) | 8 |
| [`verification`](../papers/verification) | 7 |
| [`consensus-conformity`](../papers/consensus-conformity) | 6 |
| [`hallucination-cascade`](../papers/hallucination-cascade) | 4 |
| [`general-mas-reliability`](../papers/general-mas-reliability) | 3 |
| [`context-goal-drift`](../papers/context-goal-drift) | 2 |
| [`memory-contamination`](../papers/memory-contamination) | 1 |
| **Total** | **40** |

Each category folder inside the archive carries its own README with arXiv links.

## Verification

- **39 / 40** PDFs carry an in-document `arXiv:` stamp matching the filename
- **1 / 40** (`2410.12853`) is a journal version with no arXiv stamp — arXiv ID **unconfirmed**, flagged in the index
- **0 duplicates** — verified by MD5 and by normalized body-text signature
- All 40 yield extractable text; no scanned or image-only documents

Per-paper detail in [`research/paper-index.md`](../research/paper-index.md). Methodology and the full page-count table in [`sources/source-validation.md`](../sources/source-validation.md).

## ⚠️ Copyright

These papers are the property of their respective authors and publishers, each under its own license. They are collected here for research and study.

**This archive is _not_ covered by the repository's [MIT license](../LICENSE)**, which applies only to the repository's original content — research notes, taxonomy, synthesis, and code.

Note that arXiv's default submission license (*arXiv.org perpetual, non-exclusive license*) grants **arXiv** the right to distribute, not third parties. Individual papers may carry CC-BY or similar, but that has not been checked per paper. Every paper is freely available from arXiv using the ID in its filename:

```text
https://arxiv.org/abs/<ID>
```

**Authors:** if you would prefer your paper not be included in this archive, please open an issue and it will be removed promptly.
