# Chaptered PDF Tutorial Implementation

## Purpose

Use this implementation when a tutorial source is a public or user-provided PDF with chapters, sections, examples, exercises, or a table of contents. The implementation turns a target chapter/section into focused Chinese learning material without copying long source passages.

## Selection Inputs

- Source medium is PDF or printable book.
- The user asks for learning, review, lecture notes, a study plan, knowledge triage, or section-level learning support.
- The PDF has enough structure to identify chapters, sections, examples, or exercises.
- If the PDF is a reference manual, paper, or slide deck, ask whether to adapt it as a tutorial before using this implementation.

## Source Handling

1. Record title, author, license or use condition when known, URL/file path, access date, and source trust.
2. Prefer table of contents, PDF bookmarks, headings, page labels, and chapter titles for structure.
3. If text extraction is noisy, record confidence and use page-local evidence only.
4. Never fabricate examples or claims that are not in the source or clearly labeled as supplementary explanation.

## Structure Parsing

Identify:

- chapter and section boundaries;
- front matter, copyright/license, acknowledgments, preface, appendices;
- conceptual explanation, examples, exercises, glossary, debugging or pitfalls;
- repeated or low-learning-value material.

The first section for a chaptered tutorial is normally the first real instructional chapter/section, not cover pages, copyright pages, or acknowledgments.

## Content Classification

| Class | Meaning | Action |
| --- | --- | --- |
| `core_knowledge` | Concept or skill needed for later progress. | Teach with depth decision and assessment. |
| `reading_material` | Context that helps orientation but is not a skill. | Summarize briefly. |
| `exercise_example` | Worked example or exercise. | Convert into practice when tied to core knowledge. |
| `reference` | License, installation detail, API link, glossary, appendix, external docs. | Preserve as metadata or deeper link. |
| `low_value_filler` | Repetition, non-instructional narrative, outdated or tangential detail. | Skip or link-only with reason. |

## Depth Policy

Apply `references/depth_policy.md`. For PDF tutorials, add these overrides:

- Table-of-contents pages are structure evidence, not learning content.
- Prefaces are usually `reading_material` unless they define learning strategy.
- Historical anecdotes become `skim` unless they explain the tutorial's method.
- Setup instructions become `understand` only if they block later practice.
- Language/operator surprises, debugging practices, and recurring mental models usually become `practice` or `master`.

## Workflow

1. Load the high-level contracts and this implementation only after registry resolution.
2. Extract or inspect the target unit and classify content segments.
3. Build a knowledge-point table with source trace, importance, difficulty, usefulness, depth decision, and reason.
4. Generate Chinese markdown lecture notes with required/skim/skip separation.
5. Add a small quiz, one practice task, pitfalls, deeper links, Web review spec, and day 0/1/3/7 review cards.
6. Evaluate against `references/evaluation_rubric.md` and revise weak sections.

## Output Contract

The lecture markdown must contain these headings:

- Source Trace
- Learning Goals
- Original Structure Recognition
- Core Knowledge Map
- Required Content
- Skim Or Skip
- Deeper Links
- Pitfalls
- Quiz
- Practice Task
- Web Review App Spec
- Spaced Review Cards

## Web App Hooks

Every knowledge point should expose enough structure for a later app:

- stable concept id;
- short prompt;
- correct answer criteria;
- quiz item id;
- review-card front/back;
- remediation hint for common mistakes.

## Quality Gates

- At least one source trace for each major knowledge point.
- No long verbatim source excerpt.
- Every major knowledge point has a depth decision and reason.
- The output explicitly names at least one skipped or skimmed content class when such content exists.
- Quiz, practice, Web spec, and review cards are present for each section-level lecture.

## Failure Modes

- Ask for a file or accessible URL when the PDF cannot be reached.
- Ask for the learner goal when the same content could be either skipped or mastered depending on purpose.
- Return an unresolved/recommend-extension result when the source is primarily video, web-native, or repository-native and no matching implementation is registered.
