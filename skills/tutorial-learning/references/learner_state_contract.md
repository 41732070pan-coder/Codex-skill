# Learner State Local-File Contract

Persist learner submissions and confirmations into local JSON files so a later model invocation can extract reliable learning context without scraping rendered HTML or guessing from `localStorage`.

## Required Local Files

Store course-local state under a stable `state/` directory beside the generated tutorial artifacts:

```text
state/
├── learner_state.json
└── next_lesson_context.json
```

| File | Purpose | Read pattern |
| --- | --- | --- |
| `state/learner_state.json` | Durable source of truth for learner-entered answers, confirmations, preferences, lesson completion, uncertainty markers, and review feedback. | Read when resuming a course, rendering progress, preparing review, or rebuilding context. |
| `state/next_lesson_context.json` | Compact model-facing extraction generated from `learner_state.json` immediately before creating the next lesson. | Read first when the learner triggers `生成并开始下一课`; use it as the bounded personalization input. |

Do not require the model to parse browser storage directly. `localStorage` may remain a responsive UI cache, but it is not the durable model-facing source of truth.

## Write Triggers

Update `state/learner_state.json` whenever the learner submits or confirms meaningful information:

| Trigger | Persisted information |
| --- | --- |
| Micro-assessment submit | item id, topic id, answer, attempt count, correctness when objectively checkable, feedback viewed, and uncertainty marker |
| Practice save or submit | task id, answer or structured fields, status, self-check values, and uncertainty marker |
| Explanation-preference change | selected `balanced`, `intuition-first`, `math-focused`, or `practice-focused` value |
| Lesson completion confirmation | completion timestamp, completion state, and whether review is recommended |
| Review-card feedback | card id, `forgot`, `fuzzy`, or `mastered`, review timestamp, and next due timestamp |
| Manual learner note | topic id and learner-entered note when the page supports notes |

Immediately before next-lesson generation, rebuild `state/next_lesson_context.json` from the durable learner state. Include only the minimum useful signals: completed lesson ids, next lesson id, explanation preference, first-attempt errors, repeated attempts, uncertain topics, unfinished optional practice, and due review topics.

## Runtime Write Methods

Choose one method explicitly based on the generated runtime:

1. **Filesystem-capable runtime**: write both JSON files directly. Use atomic replacement: write `*.tmp`, validate JSON, then rename over the target file.
2. **Portable static HTML**: mirror changes to `localStorage` for immediate UX and provide visible `下载学习记录` / `导出下一课上下文` actions. Export the exact JSON shapes below. Before a later model run, save the exported files into `state/` or attach them to the generation request.
3. **Hosted runtime**: persist server-side or through a local companion process, while preserving the same JSON file shapes for export and model ingestion.

A static browser page cannot silently write arbitrary local files. Do not claim that `localStorage` alone satisfies this contract. Tell the learner when an export is required before continuing in another model session.

## Model Extraction Procedure

When generating the next lesson or resuming a course:

1. Read `state/next_lesson_context.json` first if it exists and is current.
2. Read `state/learner_state.json` when rebuilding context, investigating a signal, rendering progress, or scheduling review.
3. Validate both files against `schemas/next_lesson_context.schema.json` and `schemas/learner_state.schema.json` before use.
4. Merge the compact context with the requested next route item and source traces.
5. Use mistakes and uncertainty to add a short recap, example, or exercise. Do not treat them as a hard gate and do not expose raw learner answers unnecessarily in generated prose.
6. After successfully generating the next lesson, retain the historical learner state and update the route state without deleting earlier attempts.

## Data-Minimization Rules

- Save only learning-relevant information. Do not collect unrelated personal data.
- Keep user-entered text local unless the learner explicitly supplies it to a model invocation.
- Preserve timestamps in ISO 8601 form.
- Use stable course, lesson, assessment, practice, card, and topic ids.
- Prefer compact signal summaries in `next_lesson_context.json`; keep raw answers in `learner_state.json`.
