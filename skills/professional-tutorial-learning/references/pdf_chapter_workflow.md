# PDF Chapter Workflow

Use this workflow for user-provided PDFs, PDF URLs, extracted PDF text, or chaptered documents.

## Inputs

| Field | Required | Notes |
| --- | --- | --- |
| Source locator | Yes | File path, URL, or pasted extracted text. |
| Selected scope | Preferred | Chapter, section, page range, or “first lesson”. |
| Learner goal | Preferred | If missing, infer a general learning goal and mark it. |
| Extraction method | Optional | PDF text, OCR, manual paste, or unknown. |

## Workflow

1. Capture source metadata: title, locator, author/publisher when known, access date for web sources, extraction confidence, and selected scope.
2. Discover structure from table of contents, headings, page ranges, typography, or repeated patterns.
3. Create a `TutorialUnit` for the selected chapter or first lesson-sized section.
4. Classify source material into content classes from `tutorial_model_contract.md`.
5. Score knowledge points with `learning_strategy_contract.md`.
6. Decide depth:
   - study foundational and frequent concepts deeply;
   - treat examples as support unless they teach a reusable pattern;
   - keep motivational or historical text as reading-only;
   - skip repeated prose, tool screenshots without decisions, or specialized details outside the learner goal;
   - provide advanced link targets for rare complex details.
7. Generate a markdown lesson from `lesson_artifact_template.md`.
8. Include source-boundary notes: explicit vs inferred chapter, page range if available, extraction gaps, and uncertain classifications.
9. Add checkpoint questions, review prompts, and next lesson preview.

## Concrete PDF Processing Procedure

1. Identify whether the PDF is text-based, scanned, image-heavy, or already extracted text.
2. Prefer the lowest-loss extraction path available: embedded text, table of contents metadata, page-range extraction, OCR only when necessary, then user-pasted excerpts for low-confidence pages.
3. Normalize page ranges: distinguish PDF page index, printed page number, and chapter-local page number when visible.
4. Remove repeated headers, footers, page numbers, navigation artifacts, and unrelated front/back matter before classifying content.
5. Verify the selected scope against extracted text. If the selected chapter cannot be located, ask for a page range or pasted excerpt.
6. Preserve `TutorialUnit.sourceRange` with page range, heading, or extraction slice whenever possible.
7. Handle special blocks explicitly:
   - code blocks become practice or worked examples when runnable or inspectable;
   - figures and captions become supporting examples unless they define a process;
   - tables become concept maps or comparison tables when central, otherwise reading-only;
   - exercises become practice tasks or checkpoints;
   - footnotes and references become further reading unless they change the main concept.
8. If OCR or extraction confidence is low, generate only a structure map or ask for a cleaner excerpt; do not fabricate missing details.

## Minimum Viable Input

| Input available | Allowed output | Must disclose |
| --- | --- | --- |
| PDF file or reliable extracted text | Full lesson for selected unit | Extraction method and source range. |
| PDF URL plus browsable metadata only | Orientation lesson or study plan | That body content was not fully extracted. |
| Table of contents only | Roadmap and first-lesson plan | That knowledge details are inferred from headings. |
| Scanned/low-confidence pages | Ask for OCR/text or produce limited outline | Low confidence and missing text risk. |

## PDF-Specific Heuristics

| Signal | Interpretation |
| --- | --- |
| Table of contents entry | Strong boundary candidate. |
| Numbered heading | Strong section boundary candidate. |
| Figure caption or screenshot | Usually supporting example unless it encodes a workflow decision. |
| Long introduction or motivation | Often reading-only after extracting one-sentence purpose. |
| Repeated installation steps | Compress unless the learner is setting up the tool now. |
| Dense mathematical appendix | Usually `advanced_optional` unless prerequisite to the selected goal. |

## Output Requirements

- One markdown lesson per small section by default.
- Do not force a whole PDF into one artifact.
- Keep skip decisions visible so the learner trusts the time-saving choices.
- If a PDF cannot be read directly, ask for extracted text or a selected excerpt.
