---
name: tutorial-learning
description: Learn from PDF, HTML, Markdown, and heading-structured tutorial sources. Produces a study plan and a content-first interactive tutorial web page with Chinese teaching content, source-traced triage, micro-assessments, practice tasks, review cards, and progressive navigation when needed.
---

# Tutorial Learning

## Purpose

Turn hypertext tutorial sources into a content-first, interactive Chinese tutorial web page. The web experience exists to teach the source material: navigation, layout, and interactions must support the lesson rather than replace it with a design specification. Treat PDF, HTML, Markdown, and heading-structured text as carriers of the same model: ordered sections, source traces, headings, links, content blocks, concepts, assessments, and review cards.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Learn from a PDF textbook, HTML tutorial, Markdown guide, documentation page, web tutorial, or other heading-structured tutorial source. |
| Trigger | Generate or refine Chinese lecture notes, content triage, micro-assessments, practice tasks, or spaced review cards from a tutorial section. |
| Trigger | Classify tutorial blocks as core, supporting, reference-only, filler, or deferred operational detail. |
| Non-trigger | Raw PDF extraction, rendering, OCR setup, or layout QA. Use a document-processing tool first, then pass usable text or source locations to this skill. |
| Non-trigger | Generic summarization without a learning workflow. |
| Ask if ambiguous | Source is inaccessible, source rights are unclear, source is not a tutorial, requested scope is missing, or the source lacks enough text to support the requested lesson. |

## Quick Start

This is an LLM-driven Skill with deterministic validators, not a standalone source-to-artifact CLI. Ask Codex to use `$tutorial-learning` with a source and scope, for example: `Use $tutorial-learning to learn the Retry Strategy section from this Markdown source. Generate the study plan first, then the learner-facing interactive tutorial web page.`

Deliver learner-facing files first: `learning_plan.md` and runnable `interactive_tutorial.html`. Preserve `lecture.md` as the source-traced content sidecar used to render the page. Keep JSON source-outline, triage, review-plan, and evaluator files as audit or machine-facing sidecars unless the user asks to inspect them.

## Workflow

1. **Normalize** the request into `TutorialRequest` (see `references/learning_contract.md`).
2. **Identify** the source format: PDF, HTML, Markdown, or plain text with headings.
3. **Build** a source outline from page ranges, headings, anchors, links, navigation order, and source traces.
4. **Triage** blocks with `references/triage_protocol.md`; route core material to the lecture, lookup material to the appendix, and omit filler.
5. **Generate** Chinese lecture notes with `references/lecture_template.md`.
6. **Add** micro-assessment, a practice task when applicable, and review cards using `references/review_protocol.md`.
7. **Plan** the full learning arrangement first, then choose `complete_course` or `progressive_chapter` webpage delivery from the routed content size.
8. **Render** `learning_plan.md` and a runnable, homepage-navigated `interactive_tutorial.html` with `references/interactive_webpage_contract.md`. Put the tutorial explanation, micro-test, practice, and review flow inside the page.
9. **Check** source fidelity, teaching-content coverage, and learner interactions with `references/evaluator_rubric.md` before delivery.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source URL/path/text and requested chapter, section, heading, page range, or anchor. |
| Optional inputs | Time budget, familiarity, learning goal, skip preference, and personal relevance hints. |
| Normalized shape | `TutorialRequest` in `references/learning_contract.md`. |
| Outputs | `learning_plan.md` first, a runnable homepage-navigated `interactive_tutorial.html`, Chinese lecture markdown as a content sidecar, content triage, learning route, micro-assessment, practice task when applicable, review cards, review plan JSON, and machine-readable evaluator report. Preserve source outline JSON as an audit sidecar when structured artifacts are produced. |
| Failure conditions | Stop or ask when source text is unavailable, rights/use constraints are unclear, the requested unit cannot be located, or only headings/TOC exist without lesson content. |

## References

Load progressively; do not read every reference by default.

| Reference | Load when |
| --- | --- |
| `references/learning_contract.md` | Any run; defines the shared tutorial model and workflow. |
| `references/source_adapter_contract.md` | Extending or auditing lightweight source adapters and their upgrade path. |
| `references/source_profiles.md` | Handling PDF, HTML, Markdown, or heading-structured text. |
| `references/source_fidelity.md` | Source trace, page/anchor/heading evidence, uncertainty, rights, or extraction confidence matters. |
| `references/triage_protocol.md` | Classifying blocks, filler, reference-only material, skip policy, or depth routing. |
| `references/lecture_template.md` | Generating or reviewing Chinese lecture markdown. |
| `references/review_protocol.md` | Producing review cards and spaced schedules. |
| `references/interactive_webpage_contract.md` | Rendering the content-first interactive tutorial page, selecting complete or progressive delivery, and wiring homepage navigation plus lesson interactions. |
| `references/evaluator_rubric.md` | Auditing output quality. |

## Resources

| Resource | Role |
| --- | --- |
| `references/source_profiles.md` | Source-format ingest rules for PDF, HTML, Markdown, and heading-structured text. |
| References listed above | Shared contracts, templates, and quality criteria loaded only when needed. |
| `scripts/minimal_schema.py` | Execute the dependency-free JSON Schema subset used by validators. |
| `scripts/validate_artifact.py` | Validate structured tutorial artifacts, lecture template conformance, and cross-artifact invariants. |
| `scripts/run_examples.py` | Run the Markdown, HTML noise, PDF excerpt, and plain-text heading regression fixtures. |

## Extension Points

Add a lightweight source-format adapter profile to `references/source_profiles.md` only when it can use the same outline, trace, triage, lecture, and review workflow. Use `references/source_adapter_contract.md`; add a registry and resolver only when profile count, ambiguity, or adapter-specific resources justify them.

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
- Emit `learning_plan.md` before `interactive_tutorial.html`; choose `complete_course` or `progressive_chapter` explicitly from content size.
- The runnable web page teaches the routed core content and includes homepage navigation with every ready, current, and planned lesson plus the learning plan and review center.
- The web page provides usable micro-test, practice, completion, and review interactions. A separate webpage design draft is optional and should only be produced when the user explicitly asks for one.
