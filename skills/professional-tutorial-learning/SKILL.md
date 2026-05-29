---
name: professional-tutorial-learning
description: Workflow skill for learning professional tutorials from PDFs, web courses, videos, transcripts, or chaptered technical material by normalizing sources, separating knowledge points from reading-only or low-value content, generating markdown-first lessons, practice, checkpoints, review plans, and future web-app-ready learning artifacts.
---

# Professional Tutorial Learning

## Purpose

Use this skill to convert professional tutorials into focused learning and review artifacts. Treat each tutorial as a structured source with a medium, internal organization, knowledge density, learner goal, and review path. The skill is markdown-first today and web-app-ready by design: generated lessons should be readable as standalone Markdown while preserving stable fields that can later render in a learning web application.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Learn, review, summarize, or turn a professional tutorial into lessons, notes, quizzes, checkpoints, flashcards, or a study plan. |
| Trigger | Process a PDF tutorial, chaptered web tutorial, course link, transcript, video outline, or local extracted text. |
| Trigger | Classify tutorial content into core knowledge points, examples, reading-only material, low-value filler, optional advanced material, and review prompts. |
| Trigger | Improve this learning skill through iterative lesson generation, evaluation, and revision. |
| Non-trigger | Repository-level skill governance, naming, registry policy, and cross-skill quality rules belong to `meta-skill`. |
| Non-trigger | Visual style or UI branding for a learning web app belongs to a design skill unless the request is only for data shape or markdown structure. |
| Ask if ambiguous | The source medium, learner goal, target section, or expected output format is unclear and cannot be safely inferred. |

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source or description, source medium if known, learner goal, and requested chapter/section or scope. |
| Optional inputs | Current skill level, available study time, preferred depth, target technology stack, desired practice style, review cadence, output language, and future web-app constraints. |
| Normalized shape | `TutorialLearningRequest` with source metadata, medium, structure, selected unit, learner profile, depth policy, output target, review policy, and uncertainty notes. |
| Outputs | Markdown lesson artifacts, section study plans, knowledge-point maps, skip/read classifications, practice tasks, checkpoint questions, review cards, further-reading links, and skill iteration logs. |
| Failure modes | Mark inferred structure or uncertain importance explicitly; ask once for missing high-impact inputs; recommend a registered workflow rather than inventing an unregistered one. |

## Workflow

1. Normalize the request into `TutorialLearningRequest` using `references/tutorial_model_contract.md` when schema-level decisions matter.
2. Resolve the source workflow from `references/source_workflow_registry.md`:
   - exact medium or workflow id wins;
   - file/URL/transcript cues may select a registered workflow;
   - if two workflows fit equally, present candidates and ask once;
   - load only the selected workflow reference.
3. Segment the tutorial into chapters, sections, and lesson-sized units. Preserve explicit boundaries and mark inferred boundaries.
4. Classify each unit's content:
   - core knowledge point;
   - supporting example;
   - reading-only material;
   - skip candidate or low-value filler;
   - optional advanced topic with a deep-dive link target.
5. Calibrate learning depth with `references/learning_strategy_contract.md`: importance, prerequisite value, practical frequency, complexity, user goal relevance, and time budget decide whether to study deeply, normally, skim, or skip with a link.
6. Produce a markdown-first lesson using `references/lesson_artifact_template.md`. Keep stable metadata and block names so the same output can later feed a web learning interface.
7. Add practice, checkpoint questions, review prompts, and next-step guidance for every lesson-sized unit.
8. If improving this skill, follow `references/iteration_protocol.md` and record each round's abstract update, concrete workflow update, trial generation, evaluator feedback, and accepted revision.
9. Run the quality gates before delivery or commit.

## References

| Reference | Load when |
| --- | --- |
| `references/tutorial_model_contract.md` | Normalizing tutorial sources, structures, lesson objects, content classes, or web-app-ready data fields. |
| `references/learning_strategy_contract.md` | Choosing learning depth, time budget, skip policy, practice intensity, or review cadence. |
| `references/source_workflow_registry.md` | Resolving PDF, web, video, transcript, or mixed-media workflows. |
| `references/pdf_chapter_workflow.md` | The selected source is a PDF, PDF-derived text, or chaptered document. |
| `references/web_course_workflow.md` | The selected source is a web tutorial, online course page, or chaptered article series. |
| `references/video_course_workflow.md` | The selected source is video, transcript, timestamped lecture, or course recording. |
| `references/lesson_artifact_template.md` | Generating or validating lesson markdown artifacts. |
| `references/iteration_protocol.md` | Running the 10-round optimization loop or recording skill-improvement evidence. |
| `examples/first_lesson.md` | The user asks for an example lesson or output-shape validation. |

## Resources

- User-provided PDFs, URLs, transcripts, copied excerpts, extracted text, and local Markdown files are input resources, not bundled assets.
- Preserve source title, URL or file name, author/publisher when known, access date when browsing, and extraction confidence in generated lessons.
- For long tutorials, process the selected chapter, section, or lesson-sized slice first instead of trying to load the entire source.
- Mark inferred chapter boundaries, inferred topic importance, and uncertain skip decisions rather than presenting guesses as facts.
- External deep-dive links must be verified when browsing is available; otherwise label them as link targets to verify.
- This skill currently owns no binary assets. If future templates, screenshots, or sample datasets are bundled, add provenance and a manifest before using them.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| New source medium | Strategy + registry row | `references/source_workflow_registry.md` plus a selected workflow reference. |
| Learning depth policy | Contract refinement | `references/learning_strategy_contract.md`. |
| Lesson output shape | Template Method | `references/lesson_artifact_template.md`. |
| Web learning app renderer | Adapter | Preserve markdown block ids and JSON-compatible fields before adding renderer-specific code. |
| Skill optimization | Evaluation loop | `references/iteration_protocol.md`. |
| Deterministic validation | Script | `scripts/validate_tutorial_skill.py`. |

## Quality Gate

Before delivery or commit:

- Run `python skills/professional-tutorial-learning/scripts/validate_tutorial_skill.py`.
- Run `python skills/meta-skill/scripts/validate_skills.py`.
- Run `python skills/meta-skill/scripts/validate_skill_boundaries.py`.
- Run `git diff --check`.
- Manually verify that each generated lesson distinguishes core knowledge, reading-only material, skip candidates, practice, checkpoints, and review prompts.
