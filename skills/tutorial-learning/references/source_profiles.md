# Hypertext Tutorial Source Profiles

Use these rules when ingesting PDF, HTML, Markdown, or heading-structured tutorial text. Shared triage, lecture, and review behavior lives in the corresponding reference files.

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
