# Lesson Design Contract

Use this contract in `chapter_tutorial` mode. A lesson teaches one evidence-backed concept or skill; it is not a repeated chapter-page template.

## Three-Layer Tutorial Design

| Layer | Required content |
| --- | --- |
| Route | Learner-specific order, priorities, prerequisites, time budget, and deferred topics. |
| Chapter guide | Knowledge map, lesson sequence, evidence boundary, and chapter-level transfer goal. |
| Lesson | Concept explanation, worked reasoning or demonstration, diagnostic check, practice, feedback guidance, and review prompt. |

## Lesson Archetypes

Choose an archetype from source content instead of applying one generic page shape everywhere.

| Archetype | Required teaching moves |
| --- | --- |
| `math_foundation` | Concept explanation, formula intuition, small calculation, and misconception check. |
| `model_mechanism` | Inputs/outputs, structural explanation, training or execution flow, worked example, and failure case. |
| `optimization_diagnosis` | Failure symptom, diagnostic path, parameter intervention, predicted outcome, and comparison. |
| `application_workflow` | Task definition, data shape, method choice, evaluation criterion, and transfer exercise. |
| `tool_operation` | Minimal command or code, expected result, modification experiment, common error, and environment check. |
| `conceptual` | Scenario, intuition, definition, positive example, counterexample, misconception check, and transfer. |

## Evidence-Gated Depth

- `outline`: route orientation only; no lesson body.
- `section`: chapter knowledge map and lesson candidates; keep explanations explicitly limited.
- `paragraph`: concept lesson with examples and checks grounded in paragraph-level traces.
- `code`: code experiment card with code trace, run-before prediction, expected-result explanation, modification experiment, common error, and transfer task.

When code is central and code-level evidence is present, include a code experiment. When code evidence is absent, do not invent runnable code and label any suggested experiment as supplementary.

## Diagnostic Assessment Types

Use the smallest useful mix for the lesson:

`prediction | concept_explanation | calculation | code_reading | diagnosis | transfer`

Each assessment records the capability being diagnosed, the expected evidence of understanding, and feedback guidance for a wrong or uncertain first attempt.

## Anti-Template Gate

Before delivery, compare adjacent lesson designs. Reject repetitive filler and repeated generic sentences. Each lesson must contain a source-specific concept, example, diagnostic prompt, or practice criterion.

## Downstream Renderer Handoff

Expose semantic hooks rather than implementation code: stable lesson ids, concept labels for search, lesson order, designed/planned/deferred route status, diagnostic prompts and feedback guidance, review tasks, and code-experiment cards when evidence supports them. A downstream web renderer may map these hooks to progress indicators, search, interactive quizzes, review panels, code-copy actions, or local persistence. This skill does not implement those UI or runtime features.
