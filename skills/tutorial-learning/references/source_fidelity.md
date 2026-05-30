# Source Fidelity

Use this contract whenever a lesson, triage block, or assessment depends on source evidence.

## Evidence Types

| Evidence type | Meaning | Allowed use |
| --- | --- | --- |
| `source-derived` | Directly grounded in visible source text or structure. | Main teaching claims, objectives, source trace. |
| `paraphrased` | Restates source content in the learner's language. | Lecture explanations and summaries. |
| `inferred` | Reasonable structure or importance inference from available evidence. | Boundary notes, depth rationale; must mark confidence. |
| `user-supplied` | Supplied by the user outside the source. | Learner goals, constraints, known background. |
| `supplementary` | Added by the assistant as general context or deep-dive guidance. | Mark as supplementary; do not present as source content. |
| `missing` | Needed evidence is absent or inaccessible. | Ask, stop, or emit a limited orientation only. |

## Boundary Confidence

| Confidence | Use when |
| --- | --- |
| `explicit` | The source has a bookmark, heading, anchor, page label, or clear section marker. |
| `inferred-high` | Multiple signals agree, such as TOC plus heading text or URL anchor plus H1/H2. |
| `inferred-medium` | One strong signal exists but surrounding structure is noisy. |
| `inferred-low` | Boundary is guessed from layout, typography, or partial extraction. |

## SourceTrace

A `SourceTrace` should preserve at least one stable locator when available:

- PDF: `pageRange`, page label, bookmark title, TOC entry, extraction slice.
- HTML: canonical URL, anchor, heading path, main-content block id.
- Markdown: file path or URL, heading path, explicit anchor if present.
- Plain text with headings: heading path and extraction slice.

Use `references/source_profiles.md` for source-format-specific ingest rules.

## Rights And Safety

- Record rights/use conditions or uncertainty before generating substantial artifacts.
- Do not provide long verbatim copyrighted excerpts; summarize and cite source metadata instead.
- For medical, legal, financial, safety, or compliance tutorials, generate study aids only and do not replace qualified professional instruction or current standards.
- Never invent chapter content from a title, TOC, URL slug, or anchor alone.

## Lecture Claim Labeling

Every teaching claim in `lecture.md` **核心讲解** must be traceable without opening other skill files:

| Rule | Detail |
| --- | --- |
| Literal source text | Tag inline or in **来源与边界** as `source-derived` or `paraphrased` with a `source_trace_ids` entry. |
| Non-literal expansion | Tag as `inferred` or `supplementary` inline (e.g. `[推断]`) **or** list subsection titles in `source_fidelity.md` under **推断展开** with evidence type. |
| No false claims | Do not write in `source_fidelity.md` that the lecture "already labels" inferred content unless those tags or the **推断展开** table exist. |

## Minimal Source Guardrail

When the scoped source body has **≤3 sentences** of concept text (excluding filler):

- Keep **核心讲解** concise; prefer `skim` depth for supporting blocks.
- Add **推断说明** under **来源与边界** or a short **推断展开** table in `source_fidelity.md` listing each inferred subsection.
- Do not fabricate worked examples, counterexamples, or misconceptions beyond what one sentence can support; state `[推断]` and lower boundary confidence when expanding pedagogically.
