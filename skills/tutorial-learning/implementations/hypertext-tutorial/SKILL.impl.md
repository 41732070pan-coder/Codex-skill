# Hypertext Tutorial Implementation

Concrete `TutorialLearningBase` for PDF, HTML, Markdown, and heading-structured tutorial sources.

## Purpose

Use this implementation when the source is a tutorial encoded as hypertext: it has pages, headings, anchors, links, sections, or a linear document structure that can be traced back to source locations. The implementation turns a target unit into focused Chinese learning artifacts without copying long source passages.

PDF is handled as a hypertext source format with page ranges, outlines, bookmarks, and text extraction slices. It is not a separate implementation.

## Triggers

- Source is PDF, HTML, Markdown, a documentation page, a web tutorial, or heading-structured extracted text.
- User asks for section/chapter learning, triage, lecture notes, review cards, micro-assessments, or H5/hypertext projection.
- Source contains enough tutorial text to ground the requested lesson.

## Non-Triggers

- Sources that cannot be represented as hypertext sections, headings, anchors, links, or page ranges.
- Raw PDF rendering, OCR setup, extraction library installation, or layout QA.
- Generic summarization with no learning workflow or review artifact.

## Selection Inputs

- `TutorialRequest.source.format` is `pdf`, `html`, `markdown`, or `plain_text_with_headings`, or can be inferred from locator/cue.
- `TutorialRequest.scope` identifies a chapter, section, heading path, page range, anchor, or small selected range.
- Source rights/use conditions are known enough for summarized study artifacts.

## Source Handling

1. Record title, author/publisher, locator, access mode, source trust, license/use note, and access date when available.
2. Build a `SourceOutline` from the source's strongest structure signals.
3. Preserve `SourceTrace` ids for every major block and learning objective.
4. Mark boundary confidence and extraction uncertainty explicitly.
5. Never fabricate examples, claims, URLs, anchors, or page ranges.

## Source Profiles

### PDF

- Prefer PDF bookmarks, table of contents, page labels, user-provided page ranges, and visible headings.
- Treat cover pages, copyright, acknowledgments, duplicated TOC, running headers/footers, and page numbers as metadata/structure unless they are the requested topic.
- Record page ranges or extraction slices for selected blocks.
- Mark split code blocks, noisy tables, missing glyphs, or extraction gaps.
- Stop or request OCR when the PDF is scanned and no usable text is available.

### HTML / Web Tutorial

- Prefer canonical URL, main content, heading hierarchy, anchors, previous/next links, and source links.
- Remove navigation, sidebars, comments, cookie banners, ads, duplicate headers/footers, and unrelated marketing copy from learning content.
- Preserve anchors and URLs for source traces and deep dives.
- Mark uncertainty if main content cannot be separated from navigation or marketing content.

### Markdown

- Prefer front matter, title, heading hierarchy, generated anchors, fenced code blocks, tables, and explicit links.
- Preserve commands, identifiers, code, and link targets exactly.
- Treat badges, generated TOCs, long reference tables, and license blocks as metadata/reference unless the scope requires them.

### Plain Text With Headings

- Use heading patterns and user-provided scope to infer a linear document outline.
- Mark boundaries as inferred unless the user supplied explicit section markers.
- Ask for more source text if only a TOC or heading list is available.

## Structure Parsing

Identify:

- tutorial title and selected unit;
- heading path, page range, anchor, URL, or extraction slice;
- conceptual explanation, examples, exercises, warnings, tables, figures, reference links;
- navigation, sidebars, duplicated structure text, appendices, and low-learning-value filler.

The selected unit should be lesson-sized. If a chapter is too large, recommend a heading, page range, or first meaningful section.

## Content Classification

Apply `references/source_fidelity.md` and `references/triage_protocol.md` to every selected hypertext block.

- `core`: required for objectives or later tutorial progress.
- `supporting`: examples, diagrams, or context that improve understanding.
- `reference_only`: long tables, appendices, bibliographies, license/use notes, API lists.
- `filler`: repeated navigation, empty transitions, marketing, decorative or duplicated text.
- `deferred_ops`: setup or tooling details not needed for the current concept.

## Depth Policy

Use `references/triage_protocol.md` for scoring. For hypertext sources, add these overrides:

- Navigation structure is evidence, not learning content.
- Setup instructions become `standard` or `deep` only if they block the user's immediate practice goal.
- Long reference tables become appendix content unless the user's goal requires memorization.
- Recurring mental models, debugging patterns, and prerequisite concepts usually become `standard` or `deep`.

## Workflow

1. Normalize request and source metadata.
2. Determine source format and selected unit.
3. Build source outline and source traces.
4. Classify blocks and compute depth routing.
5. Generate Chinese lecture notes using `references/lecture_template.md`.
6. Add micro-assessment, practice task when applicable, review cards, and review plan.
7. Emit review cards and schedules using `references/review_protocol.md`.
8. Emit lightweight H5/hypertext projection using `references/h5_lesson_schema.md` when useful.
9. Evaluate with `references/evaluator_rubric.md` before delivery.

## Output Contract

Emit:

- `lecture_md` with required Chinese headings from `references/lecture_template.md`.
- `triage.json` with `TriageBlock[]` and skipped summary.
- `review_plan.json` with review cards and due offsets.
- optional `h5_stub.json` / hypertext projection with stable ids.

## Quality Gates

- Every major knowledge point has at least one source trace.
- Boundary confidence is explicit for selected unit and major blocks.
- No long verbatim source excerpt.
- Filler is omitted from the lecture body.
- Reference-only material is appendix, not objective.
- Quiz, practice when applicable, and review cards are present for each lesson-sized unit.
- The implementation does not accept non-hypertext carrier sources.

## Failure Modes

| Issue | Action |
| --- | --- |
| Source unreadable | Ask for accessible URL/path/text or stop. |
| Only TOC/headings available | Generate limited orientation or ask for source text; do not teach missing content. |
| Scanned PDF without text | Report need for OCR/tooling; stop. |
| Ambiguous selected unit | Ask once for page range, heading, anchor, or section title. |
| License/use condition unclear | Avoid substantial artifact generation until clarified. |
| Unsupported non-hypertext carrier | Decline this skill and ask for a supported hypertext source. |
