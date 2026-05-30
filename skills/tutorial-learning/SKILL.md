---
name: tutorial-learning
description: Learn from PDF, HTML, Markdown, and heading-structured tutorial sources. Produces a study plan and a content-first interactive tutorial web page with Chinese teaching content, source-traced triage, complete study units, attempt-first micro-assessments, learner-triggered progressive generation, review cards, and a pluggable design-style interface with a default Chinese traditional theme.
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
6. **Build** each lesson as an independently studyable unit: scenario, objectives, intuition, definitions, positive example, counterexample, misconceptions, attempt-first assessment, practice, analysis, recap, and bridge.
7. **Add** attempt-first micro-assessment, a practice task when applicable, and review cards using `references/review_protocol.md`. Wrong answers become learning signals, not progression blockers.
8. **Plan** the full learning arrangement first, then choose `complete_course` or `progressive_chapter` webpage delivery from the routed content size. For long tutorials, use learner-triggered next-lesson generation from `references/progressive_generation_contract.md`.
9. **Persist** learner submissions and confirmations to course-local JSON files with `references/learner_state_contract.md`. Rebuild compact model-facing context immediately before next-lesson generation.
10. **Resolve** visual styling through `references/design_style_interface.md`. Unless the user overrides it, apply `my-design-style` with its `chinese-traditional-color-style` theme.
11. **Render** `learning_plan.md` and a runnable, homepage-navigated `interactive_tutorial.html` with `references/interactive_webpage_contract.md`. Put the tutorial explanation, micro-test, practice, and review flow inside the page.
12. **Check** source fidelity, teaching-content coverage, learner interactions, progressive-generation behavior, and style separation with `references/evaluator_rubric.md` before delivery.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source URL/path/text and requested chapter, section, heading, page range, or anchor. |
| Optional inputs | Time budget, familiarity, learning goal, skip preference, personal relevance hints, next-lesson explanation preference, and design-style overrides. |
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
| `references/progressive_generation_contract.md` | Rendering a long tutorial one complete lesson at a time, exposing lock reasons, collecting learning signals, and wiring learner-triggered next-lesson generation. |
| `references/learner_state_contract.md` | Persisting submissions and confirmations into local JSON files, rebuilding bounded next-lesson context, and loading it in later model runs. |
| `references/design_style_interface.md` | Resolving pluggable visual themes. Load with `my-design-style` references unless the user overrides the default Chinese traditional style. |
| `references/interactive_webpage_contract.md` | Rendering the content-first interactive tutorial page, selecting complete or progressive delivery, and wiring homepage navigation plus lesson interactions. |
| `references/evaluator_rubric.md` | Auditing output quality. |

## Resources

| Resource | Role |
| --- | --- |
| `references/source_profiles.md` | Source-format ingest rules for PDF, HTML, Markdown, and heading-structured text. |
| References listed above | Shared contracts, templates, and quality criteria loaded only when needed. |
| `scripts/minimal_schema.py` | Execute the dependency-free JSON Schema subset used by validators. |
| `schemas/learner_state.schema.json` and `schemas/next_lesson_context.schema.json` | Validate durable local learner state and compact model-facing generation context. |
| `scripts/validate_artifact.py` | Validate structured tutorial artifacts, local learner-state files, lecture template conformance, and cross-artifact invariants. |
| `scripts/run_examples.py` | Run the Markdown, HTML noise, PDF excerpt, and plain-text heading regression fixtures. |

## Extension Points

Add visual themes through `references/design_style_interface.md` without changing teaching structure or interactions. Add a lightweight source-format adapter profile to `references/source_profiles.md` only when it can use the same outline, trace, triage, lecture, and review workflow. Use `references/source_adapter_contract.md`; add a registry and resolver only when profile count, ambiguity, or adapter-specific resources justify them.

## Scope Boundary

This skill owns learning structure, triage, source fidelity, lecture generation, assessment, and review planning. Delegate raw PDF rendering, OCR, and low-level extraction tooling to document-processing tools when needed.

## Quality Gate

Before finishing:

- Source traces identify page ranges, heading paths, anchors, URLs, or extraction slices when available.
- Boundary and extraction uncertainty are explicit when inferred or weak.
- Lecture output is Chinese; identifiers, commands, API names, formulas, and URLs keep source spelling.
- Triage table is present; filler is omitted from the body; reference-only content goes to the appendix.
- Learning objectives are 2–4 and verifiable; each lesson includes scenario, explanation, positive example, counterexample, misconceptions, assessment, practice, analysis, recap, and bridge.
- Micro-assessment is attempt-first: feedback appears only after learner input. Wrong answers inform later generation but do not block progression.
- Review cards map to learning objectives and use spaced due offsets.
- Emit `learning_plan.md` before `interactive_tutorial.html`; choose `complete_course` or `progressive_chapter` explicitly from content size.
- Learner submissions and confirmations are persisted into `state/learner_state.json`; next-lesson generation reads a rebuilt `state/next_lesson_context.json` instead of scraping HTML or relying only on browser storage.
- In progressive mode, navigation distinguishes `completed`, `current`, `ready-to-generate`, and `locked`; locked entries remain inspectable and the learner explicitly triggers next-lesson generation.
- Resolve visual style through the pluggable interface and default to `my-design-style` / `chinese-traditional-color-style` unless overridden.
- The runnable web page teaches the routed core content and provides usable attempt-first micro-test, practice, completion, generation, and review interactions. A separate webpage design draft is optional and should only be produced when the user explicitly asks for one.
