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

Use `implementations/hypertext-tutorial/SKILL.impl.md` for source-format-specific ingest rules.

## Rights And Safety

- Record rights/use conditions or uncertainty before generating substantial artifacts.
- Do not provide long verbatim copyrighted excerpts; summarize and cite source metadata instead.
- For medical, legal, financial, safety, or compliance tutorials, generate study aids only and do not replace qualified professional instruction or current standards.
- Never invent chapter content from a title, TOC, URL slug, or anchor alone.
