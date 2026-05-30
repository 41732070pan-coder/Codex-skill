---
name: tutorial-learning
description: Learn from PDF, HTML, Markdown, and heading-structured tutorial sources. Produces focused Chinese lecture notes, content triage, micro-assessments, practice tasks, and spaced review cards.
---

# Tutorial Learning

## Purpose

Turn hypertext tutorial sources into time-efficient Chinese study artifacts. Treat PDF, HTML, Markdown, and heading-structured text as carriers of the same model: ordered sections, source traces, headings, links, content blocks, concepts, assessments, and review cards.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Learn from a PDF textbook, HTML tutorial, Markdown guide, documentation page, web tutorial, or other heading-structured tutorial source. |
| Trigger | Generate or refine Chinese lecture notes, content triage, micro-assessments, practice tasks, or spaced review cards from a tutorial section. |
| Trigger | Classify tutorial blocks as core, supporting, reference-only, filler, or deferred operational detail. |
| Non-trigger | Raw PDF extraction, rendering, OCR setup, or layout QA. Use a document-processing tool first, then pass usable text or source locations to this skill. |
| Non-trigger | Generic summarization without a learning workflow. |
| Ask if ambiguous | Source is inaccessible, source rights are unclear, source is not a tutorial, requested scope is missing, or the source lacks enough text to support the requested lesson. |

## Workflow

1. **Normalize** the request into `TutorialRequest` (see `references/learning_contract.md`).
2. **Identify** the source format: PDF, HTML, Markdown, or plain text with headings.
3. **Build** a source outline from page ranges, headings, anchors, links, navigation order, and source traces.
4. **Triage** blocks with `references/triage_protocol.md`; route core material to the lecture, lookup material to the appendix, and omit filler.
5. **Generate** Chinese lecture notes with `references/lecture_template.md`.
6. **Add** micro-assessment, a practice task when applicable, and review cards using `references/review_protocol.md`.
7. **Check** the result with `references/evaluator_rubric.md` before delivery.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source URL/path/text and requested chapter, section, heading, page range, or anchor. |
| Optional inputs | Time budget, familiarity, learning goal, skip preference, and personal relevance hints. |
| Normalized shape | `TutorialRequest` in `references/learning_contract.md`. |
| Outputs | Chinese lecture markdown, content triage, learning route, micro-assessment, practice task when applicable, review cards, and review plan JSON. |
| Failure modes | Stop or ask when source text is unavailable, rights/use constraints are unclear, the requested unit cannot be located, or only headings/TOC exist without lesson content. |

## References

Load progressively; do not read every reference by default.

| Reference | Load when |
| --- | --- |
| `references/learning_contract.md` | Any run; defines the shared tutorial model and workflow. |
| `implementations/hypertext-tutorial/SKILL.impl.md` | Handling PDF, HTML, Markdown, or heading-structured text. |
| `references/source_fidelity.md` | Source trace, page/anchor/heading evidence, uncertainty, rights, or extraction confidence matters. |
| `references/triage_protocol.md` | Classifying blocks, filler, reference-only material, skip policy, or depth routing. |
| `references/lecture_template.md` | Generating or reviewing Chinese lecture markdown. |
| `references/review_protocol.md` | Producing review cards and spaced schedules. |
| `references/evaluator_rubric.md` | Auditing output quality. |

## Resources

| Resource | Role |
| --- | --- |
| `implementations/hypertext-tutorial/SKILL.impl.md` | Source-format ingest rules for PDF, HTML, Markdown, and heading-structured text. |
| References listed above | Shared contracts, templates, and quality criteria loaded only when needed. |

## Extension Points

Add a source-format profile to `implementations/hypertext-tutorial/SKILL.impl.md` only when it can use the same outline, trace, triage, lecture, and review workflow.

## Scope Boundary

This skill owns learning structure, triage, source fidelity, lecture generation, assessment, and review planning. Delegate raw PDF rendering, OCR, and low-level extraction tooling to document-processing tools when needed.

## Quality Gate

Before finishing:

- Source traces identify page ranges, heading paths, anchors, URLs, or extraction slices when available.
- Boundary and extraction uncertainty are explicit when inferred or weak.
- Lecture output is Chinese; identifiers, commands, API names, formulas, and URLs keep source spelling.
- Triage table is present; filler is omitted from the body; reference-only content goes to the appendix.
- Learning objectives are 2–4 and verifiable; micro-assessment checks prediction, teach-back, and application when applicable.
- Review cards map to learning objectives and use spaced due offsets.
