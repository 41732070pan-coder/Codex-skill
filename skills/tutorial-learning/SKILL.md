---
name: tutorial-learning
description: Transform PDF, HTML, Markdown, and heading-structured tutorial sources into source-traced Chinese course-design documents. Produces a learning plan, lecture notes, tutorial structure, content triage, assessments, practice, review planning, and source-fidelity evidence for downstream renderers without choosing a visual style or presentation medium.
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

Deliver the Markdown tutorial-design bundle first. Add machine-readable JSON sidecars only when downstream automation, auditing, or explicit user requirements justify them.

## Workflow

1. **Normalize** the request into `TutorialRequest` with `references/learning_contract.md`.
2. **Identify** the source format: PDF, HTML, Markdown, or plain text with headings.
3. **Build** a source outline from page ranges, headings, anchors, links, navigation order, and source traces.
4. **Triage** blocks with `references/triage_protocol.md`; route core material to the lecture, lookup material to the appendix, and omit filler.
5. **Plan** the learning route with `references/learning_route_contract.md`; keep the full teaching sequence visible without choosing a presentation container.
6. **Generate** Chinese lecture notes with `references/lecture_template.md`.
7. **Specify** each lesson as an independently teachable unit: scenario, objectives, intuition, definitions, positive example, counterexample, misconceptions, assessment, practice, analysis, recap, and bridge.
8. **Add** attempt-first micro-assessments, practice tasks when applicable, and review cards with `references/review_protocol.md`. Wrong answers become learning signals, not progression blockers.
9. **Document** source boundaries, evidence types, inferred material, and omissions with `references/source_fidelity.md`.
10. **Evaluate** instructional completeness and source fidelity with `references/evaluator_rubric.md` before delivery.
11. **Hand off** the medium-neutral bundle to a downstream renderer only when the user requests a final presentation artifact.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source URL/path/text and requested chapter, section, heading, page range, or anchor. |
| Optional inputs | Time budget, familiarity, learning goal, skip preference, personal relevance hints, and explanation preference. |
| Normalized shape | `TutorialRequest` in `references/learning_contract.md`. |
| Required Markdown outputs | `learning_plan.md`, `lecture.md`, `tutorial_structure.md`, `triage.md`, `assessment_plan.md`, `practice_plan.md`, `review_plan.md`, and `source_fidelity.md`. |
| Optional JSON sidecars | `source_outline.json`, `triage.json`, `learning_route.json`, `review_plan.json`, and `evaluator_report.json` for automation or audit workflows. |
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
| `references/learning_route_contract.md` | Planning lesson order, dependencies, and long-course sequencing without binding a presentation medium. |
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
- Do not generate final presentation artifacts, design-style defaults, CSS/JavaScript, or runtime learner-state files from this skill.
