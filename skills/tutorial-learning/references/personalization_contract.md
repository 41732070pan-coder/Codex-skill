# Personalization Contract

Use learner preferences to change the instructional route and lesson emphasis, not merely to restate the user's goal.

## Learner Profile Inputs

| Field | Examples | Route effect |
| --- | --- | --- |
| `familiarity` | `novice`, `rusty`, `comfortable` | Controls prerequisite expansion, terminology density, and pacing. |
| `goal` | `exam`, `practice`, `project`, `survey` | Controls assessment and practice emphasis. |
| `audience` | `beginner`, `ml_transition`, `engineer`, `exam_review`, `researcher` | Selects explanation depth and prerequisite handling. |
| `target_domain` | `general`, `cv`, `nlp`, `llm`, `deployment` | Raises relevant route priorities and defers unrelated branches when safe. |
| `time_budget_minutes` | positive integer | Limits designed scope and moves lower-priority content to planned or deferred stages. |
| `explanation_preference` | `balanced`, `intuition-first`, `math-focused`, `practice-focused` | Changes lecture ordering and worked-example style. |

## Required Output

Record the applied profile and at least one concrete route or lesson consequence in `learning_plan.md`. Examples:

- novice: add terminology and prerequisite checks;
- exam: add calculation and concept-recall checks;
- engineer: add code-reading, diagnosis, and transfer tasks;
- NLP goal: prioritize text-sequence prerequisites over optional CV branches.

If no profile is supplied, state the conservative default instead of silently pretending to personalize.
