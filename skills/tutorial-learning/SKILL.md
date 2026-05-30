---
name: tutorial-learning
description: Transform PDF, HTML, Markdown, and heading-structured tutorial sources into source-traced Chinese course-design documents. Supports route-overview and chapter-tutorial modes, evidence-gated lesson depth, learner-specific routes, diagnostic assessments, practice design, review planning, and downstream renderer handoff without choosing a visual style or presentation medium.
---

# Tutorial Learning

## Purpose

Turn tutorial source material into a teachable, reviewable, and assessable course-design intermediate layer. Treat PDF, HTML, Markdown, and heading-structured text as carriers of the same source model: ordered sections, traces, headings, links, content blocks, concepts, assessments, practice tasks, and review cards.

This skill owns instructional design. It does **not** produce a final webpage, slide deck, H5 experience, document layout, visual theme, CSS, JavaScript, or runtime persistence implementation. A downstream rendering or design skill may consume the course-design documents.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Learn from a PDF textbook, HTML tutorial, Markdown guide, documentation page, web tutorial, or other heading-structured tutorial source. |
| Trigger | Generate or refine Chinese lecture notes, content triage, learning routes, micro-assessments, practice tasks, or spaced-review cards from tutorial material. |
| Trigger | Prepare medium-neutral tutorial-design documents for a downstream web, H5, PPT, DOCX, or other renderer. |
| Trigger | Classify tutorial blocks as core, supporting, reference-only, filler, or deferred operational detail. |
| Non-trigger | Implement HTML, CSS, JavaScript, slide layouts, H5 screens, visual tokens, or runtime state storage. Use the relevant downstream rendering or design skill. |
| Non-trigger | Raw PDF extraction, OCR setup, rendering, or layout QA. Use a document-processing tool first, then pass usable text or source locations to this skill. |
| Non-trigger | Generic summarization without a learning workflow. |
| Ask if ambiguous | Source is inaccessible, source rights are unclear, source is not a tutorial, requested scope is missing, or the source lacks enough text to support the requested lesson. |

## Quick Start

Ask Codex to use `$tutorial-learning` with a source and scope, for example: `Use $tutorial-learning to turn the Retry Strategy section from this Markdown source into course-design documents for a downstream renderer.`

Deliver the Markdown tutorial-design bundle first. Add machine-readable JSON audit sidecars only when downstream automation, auditing, or explicit user requirements justify them.

## Workflow

1. **Normalize** the request into `TutorialRequest` with `references/learning_contract.md`.
2. **Identify** the source format: PDF, HTML, Markdown, or plain text with headings.
3. **Build** a source outline from page ranges, headings, anchors, links, navigation order, and source traces.
4. **Triage** blocks with `references/triage_protocol.md`; route core material to the lecture, lookup material to the appendix, and omit filler.
5. **Select** `route_overview` or `chapter_tutorial` with `references/tutorial_modes.md`; never present outline-only evidence as a complete tutorial.
6. **Personalize** the route with `references/personalization_contract.md`; record how learner background, goal, domain, and time budget change priorities.
7. **Plan** the learning route with `references/learning_route_contract.md`; keep the full teaching sequence visible without choosing a presentation container.
8. **Generate** Chinese lecture notes with `references/lecture_template.md` and, in `chapter_tutorial` mode, evidence-backed lessons with `references/lesson_design_contract.md`.
9. **Add** diagnostic attempt-first assessments, practice tasks when applicable, and review cards with `references/review_protocol.md`. Wrong answers become learning signals, not progression blockers.
10. **Document** source boundaries, evidence granularity, inferred material, and omissions with `references/source_fidelity.md`.
11. **Evaluate** learning value, instructional completeness, anti-template quality, and source fidelity with `references/evaluator_rubric.md` before delivery.
12. **Hand off** the medium-neutral bundle to a downstream renderer only when the user requests a final presentation artifact.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source URL/path/text and requested chapter, section, heading, page range, or anchor. |
| Optional inputs | Design mode, time budget, familiarity, audience, learning goal, target domain, skip preference, personal relevance hints, and explanation preference. |
| Normalized shape | `TutorialRequest` in `references/learning_contract.md`. |
| Required Markdown outputs | `learning_plan.md`, `lecture.md`, `tutorial_structure.md`, `triage.md`, `assessment_plan.md`, `practice_plan.md`, `review_plan.md`, and `source_fidelity.md`. |
| Recommended JSON audit sidecars | When automation or auditing justifies JSON, optionally emit `source_outline.json`, `triage.json`, `learning_route.json`, `review_plan.json`, and `evaluator_report.json`. Validators check each sidecar when present; maintained examples include the complete audit bundle. |
| Explicitly out of scope | Final HTML, PPT, H5, DOCX, visual styling, design-provider resolution, component layout, CSS/JavaScript implementation, and runtime learner-state persistence. |
| Failure conditions | Stop or ask when source text is unavailable, rights/use constraints are unclear, the requested unit cannot be located, or only headings/TOC exist without lesson content. |

## References

Load progressively; do not read every reference by default.

| Reference | Load when |
| --- | --- |
| `references/learning_contract.md` | Any run; defines the shared medium-neutral tutorial model and bundle. |
| `references/source_adapter_contract.md` | Extending or auditing lightweight source adapters and their upgrade path. |
| `references/source_profiles.md` | Ingesting a supported source format. |
| `references/source_fidelity.md` | Recording source boundaries, traces, and evidence types. |
| `references/triage_protocol.md` | Classifying, scoring, routing, or skipping source blocks. |
| `references/tutorial_modes.md` | Selecting route-overview or chapter-tutorial depth from scope and evidence. |
| `references/personalization_contract.md` | Applying learner background, goal, domain, and time budget to route decisions. |
| `references/learning_route_contract.md` | Planning lesson order, dependencies, and long-course sequencing without binding a presentation medium. |
| `references/lesson_design_contract.md` | Designing evidence-backed, archetype-specific lessons, code experiments, and diagnostic checks. |
| `references/lecture_template.md` | Writing the Chinese lecture content sidecar. |
| `references/review_protocol.md` | Designing micro-assessments, practice tasks, and review cards. |
| `references/evaluator_rubric.md` | Running the final instructional-design self-check. |

## Resources

Use the references above as the instructional-design resource set. The scripts below validate the skill and its example bundles; this skill intentionally carries no renderer templates or visual assets.

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/validate_tutorial_learning.py` | Validate skill structure, request fixtures, and example bundles. |
| `scripts/validate_artifact.py` | Validate tutorial-design bundles and cross-artifact invariants. |
| `scripts/run_examples.py` | Run example regression validation. |

## Extension Rules

Add a lightweight source-format adapter profile to `references/source_profiles.md` only when it can use the same outline, trace, triage, lecture, route, assessment, practice, review, and fidelity workflow. Use `references/source_adapter_contract.md`; add a registry and resolver only when profile count, ambiguity, or adapter-specific resources justify them.

Do not add renderer-specific behavior here. A webpage, PPT, H5, DOCX, or design-style integration belongs in a downstream adapter skill that consumes this bundle.

## Quality Gates

- Preserve source provenance and distinguish source-derived, paraphrased, inferred, user-supplied, supplementary, and missing evidence.
- Produce the complete required Markdown bundle before any optional renderer handoff.
- Keep triage explicit: core and supporting material route to teaching content; reference-only material routes to an appendix; filler stays omitted.
- Keep assessments attempt-first and align objectives, practice, and review cards.
- Keep lesson structure independent of visual style and final presentation medium.
- Distinguish `route_overview` from `chapter_tutorial`; do not market a route scaffold as a complete tutorial.
- Gate explanation depth by evidence granularity: outline, section, paragraph, or code.
- In chapter-tutorial mode, produce source-specific lesson designs, diagnostic feedback, and practical tasks instead of repeated generic scaffolds.
- Record at least one route or lesson consequence from the learner profile.
- Do not generate final presentation artifacts, design-style defaults, CSS/JavaScript, or runtime learner-state files from this skill.
