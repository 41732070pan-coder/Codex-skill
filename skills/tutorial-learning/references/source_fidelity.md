# Source Fidelity

Use this contract whenever a lesson, triage block, assessment, or projection depends on source evidence.

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

## PDF Profile

- Prefer explicit PDF bookmarks, table of contents entries, page labels, headings, and user-supplied page ranges.
- Treat running headers, footers, repeated page numbers, copyright pages, and duplicated TOC text as structure or metadata, not learning content.
- Mark extraction gaps, broken code blocks, split tables, and uncertain page ranges.
- Stop or request OCR when the PDF is scanned and no usable text is available.
- Delegate raw rendering/OCR tooling to appropriate document tools; this skill records learning-relevant structure and uncertainty.

## HTML Profile

- Prefer canonical URLs, heading hierarchy, semantic main content, anchors, and previous/next navigation.
- Remove navigation, sidebars, cookie notices, comments, ads, duplicate headers/footers, and unrelated marketing blocks from the lecture body.
- Preserve source links and anchors for deep dives and source traces.
- Mark uncertainty when main content extraction is ambiguous.

## Markdown Profile

- Prefer front matter, title, heading hierarchy, fenced code blocks, tables, explicit links, and generated anchors.
- Preserve command/code spelling exactly.
- Treat long reference tables as appendix material unless the user goal requires memorization.

## Rights And Safety

- Record license, use condition, or uncertainty before generating substantial artifacts.
- Do not provide long verbatim copyrighted excerpts; summarize and cite source metadata instead.
- For medical, legal, financial, safety, or compliance tutorials, generate study aids only and do not replace qualified professional instruction or current standards.
- Never invent chapter content from a title, TOC, URL slug, or anchor alone.
