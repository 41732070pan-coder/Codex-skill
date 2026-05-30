# Hypertext Tutorial Source Profiles

Each section below is a lightweight `SourceAdapter` profile governed by `source_adapter_contract.md`. Use these rules when ingesting PDF, HTML, Markdown, or heading-structured tutorial text. Shared triage, lecture, and review behavior lives in the corresponding reference files.

## Adapter Discovery

| id | profile | format | status | accepted access modes | required trace fields | summary | aliases / cues | ambiguity / fallback | delegated tooling |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pdf` | `#pdf` | `pdf` | experimental | attached file, extracted text, pasted excerpt | id, source format, locator or page range, boundary confidence, evidence type | Build page- and heading-aware outlines from usable PDF text. | PDF path, attachment, page range, chapter | Stop or request accessible extracted text when unreadable. | Delegate rendering and OCR to document-processing tools. |
| `html` | `#html--web-tutorial` | `html` | experimental | URL, extracted text, pasted excerpt | id, source format, URL or locator, anchor when available, boundary confidence, evidence type | Isolate tutorial main content while preserving URL and anchor traces. | URL, HTML, documentation page, web tutorial | Mark uncertainty when main content cannot be separated. | Delegate low-level crawling or rendering when needed. |
| `markdown` | `#markdown` | `markdown` | experimental | attached file, extracted text, pasted excerpt | id, source format, locator, heading path when available, boundary confidence, evidence type | Preserve heading structure, code, tables, and explicit links. | `.md` path, pasted Markdown, fenced blocks | Preserve generated anchors when available; infer cautiously otherwise. | None by default. |
| `plain-text-headings` | `#plain-text-with-headings` | `plain_text_with_headings` | experimental | extracted text, pasted excerpt | id, source format, locator or extraction slice, boundary confidence, evidence type | Infer a linear outline from heading-structured text. | pasted text with heading patterns | Ask for more text when only headings or TOC are available. | None by default. |

Add a YAML registry and resolver only when this compact table no longer supports deterministic selection. See `source_adapter_contract.md` for mechanical upgrade triggers. Profile-specific outline signals, noise rules, and failure modes remain in the source-handling sections below.

## Source Handling

1. Record title, author/publisher, locator, access mode, and rights/use note when available.
2. Build a `SourceOutline` from the strongest available structure signals.
3. Preserve `SourceTrace` ids for major blocks and learning objectives.
4. Mark boundary confidence and extraction uncertainty explicitly.
5. Never fabricate examples, claims, URLs, anchors, or page ranges.

## PDF

- Prefer bookmarks, table of contents, page labels, user-provided page ranges, and visible headings.
- Treat cover pages, copyright, acknowledgments, duplicated TOC, running headers/footers, and page numbers as metadata or structure unless they are the requested topic.
- Record page ranges or extraction slices for selected blocks.
- Mark split code blocks, noisy tables, missing glyphs, or extraction gaps.
- Stop or request OCR when the PDF is scanned and no usable text is available.

## HTML / Web Tutorial

- Prefer canonical URL, main content, heading hierarchy, anchors, previous/next links, and source links.
- Remove navigation, sidebars, comments, cookie banners, ads, duplicate headers/footers, and unrelated marketing copy from learning content.
- Preserve anchors and URLs for source traces and deep dives.
- Mark uncertainty if main content cannot be separated from navigation or marketing content.

## Markdown

- Prefer front matter, title, heading hierarchy, generated anchors, fenced code blocks, tables, and explicit links.
- Preserve commands, identifiers, code, and link targets exactly.
- Treat badges, generated TOCs, long reference tables, and license blocks as metadata or reference unless the scope requires them.

## Plain Text With Headings

- Use heading patterns and user-provided scope to infer a linear document outline.
- Mark boundaries as inferred unless the user supplied explicit section markers.
- Ask for more source text if only a TOC or heading list is available.

## Unit Selection

The selected unit should be lesson-sized. If a chapter is too large, recommend a heading, page range, or first meaningful section.

## Failure Modes

| Issue | Action |
| --- | --- |
| Source unreadable | Ask for accessible URL/path/text or stop. |
| Only TOC/headings available | Generate limited orientation or ask for source text; do not teach missing content. |
| Scanned PDF without text | Report need for OCR/tooling; stop. |
| Ambiguous selected unit | Ask once for page range, heading, anchor, or section title. |
| Rights/use condition unclear | Avoid substantial artifact generation until clarified. |
