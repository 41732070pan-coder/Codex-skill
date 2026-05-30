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

## Evidence Granularity

Record the strongest supported granularity on every `SourceTrace`. Granularity controls how deep the generated teaching may go.

| Granularity | Evidence example | Allowed output depth |
| --- | --- | --- |
| `outline` | TOC item, chapter title, navigation label | Route priority and orientation only. Label the result as a guided overview. |
| `section` | Heading plus section-level summary or bounded excerpt | Chapter knowledge map and candidate lessons; keep explanations limited. |
| `paragraph` | Source paragraph, table, worked prose example | Concept explanation, source-grounded example, diagnostic check, and practice. |
| `code` | Source code block, notebook cell, command, or runnable snippet | Code experiment: prediction, expected result, modification, common error, and transfer task. |

Do not upgrade granularity merely because a topic is familiar. General knowledge added beyond the available source is `supplementary`, not source-derived.

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
- If evidence is outline-only, emit `route_overview`; do not generate a chapter tutorial that merely looks complete.
- If a paragraph- or code-level claim lacks a supporting trace, downgrade the claim, mark it supplementary, or ask for a richer source excerpt.
