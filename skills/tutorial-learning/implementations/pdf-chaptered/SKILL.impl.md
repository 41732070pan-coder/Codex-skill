# PDF Chaptered Implementation

Concrete `TutorialLearningBase` for chaptered PDF textbooks.

## Triggers

- Source is PDF (path or URL).
- User wants section/chapter lecture, triage, or skip filler.

## Ingest

1. Load `pdf` skill for extraction conventions.
2. Download or open `TutorialRequest.source`.
3. Extract TOC: headings via pdf outline, or heuristic (font size / "Chapter N").
4. Limit text to `scope.pageRange` or first section pages when lab/testing.

Tools: `pdfplumber` preferred; `pypdf` fallback. Visual spot-check with `pdftoppm` only if layout blocks text extraction.

## Triage (section scope)

1. Split section into blocks (heading → content until next heading).
2. Apply `references/triage_protocol.md`.
3. Write sidecar `*.triage.json` when batching; else embed summary in lecture front matter.

## Lecture generation

Follow `references/lecture_template.md` exactly.

- **第一节 default for lab**: `scope.section` = first numbered section after preface (e.g. "1.1" or "Chapter 1" introduction).
- Include `## 跳过与延伸阅读` for all `skip_with_deep_dive` blocks.
- Emit `h5_stub.json` using `references/h5_lesson_schema.md`.

## Assessment

- 3–5 micro questions under `## 微测`.
- 3–5 review cards + **required sidecar** `<lecture_basename>.review_plan.json` per `references/review_protocol.md`.
- **Required sidecar** `<lecture_basename>.triage.json` for lab and audit runs.

## Deep dive links

Prefer: official docs, book PDF page (#page=N), or publisher errata — never fabricated URLs.

## Self-check

Run triage self-check from `triage_protocol.md` plus:

- [ ] Front matter valid YAML.
- [ ] `h5_lesson_id` present.
- [ ] `est_minutes_total` ≤ overlay budget when set.

## Cross-source migration (lab R6+)

When switching PDF sources, do **not** fork the lecture template. Only adjust:

- Triage cues (e.g. JS `typeof` vs Python `type()`)
- Identifier/language examples
- `h5_lesson_id` prefix

Re-run triage from scratch; never copy prior `triage.json` blocks by title alone.

## Failure modes

| Issue | Action |
| --- | --- |
| No TOC | Ask user for page range or section title once. |
| Scanned PDF | Report need for OCR; stop. |
| License unknown | Stop before redistribution of large excerpts. |
