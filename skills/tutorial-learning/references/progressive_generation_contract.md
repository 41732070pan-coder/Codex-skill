# Progressive Generation Contract

Use this contract for long tutorials. Progressive generation is a deliberate learning strategy, not an incomplete delivery fallback: keep the full route visible, render one complete study unit at a time, and let the learner explicitly generate the next lesson when ready.

## Lesson States

| State | Meaning | Learner action |
| --- | --- | --- |
| `completed` | Previously studied lesson. | Reopen for review. |
| `current` | Fully generated lesson available now. | Continue learning. |
| `ready-to-generate` | Immediate next lesson after completion requirements are met. | Inspect preview, choose preference, then click `生成并开始下一课`. |
| `locked` | Later route item whose prerequisites are not met. | Inspect a lightweight route preview and unlock condition. |

Do not render future lessons as silent disabled controls. A locked item remains inspectable and must explain its topic, why it is locked, and what unlocks it. A preview is not a generated lesson and must not invent detailed teaching content from headings alone.

## Completion Requirements

A lesson becomes `completed` when the learner:

1. finishes the core explanation;
2. attempts every required micro-assessment at least once;
3. submits the core practice task; and
4. explicitly marks the lesson complete.

Correct answers are not a gate. Preserve mistakes and uncertainty as useful signals. Mark the lesson `review-recommended` when weak signals remain, but allow progression.

## Explicit Next-Lesson Generation

Prefer learner-triggered generation over automatic generation. After completion, place a prominent `生成并开始下一课` action in both the lesson completion area and navigation preview.

Before generation, persist learner submissions and confirmations according to `learner_state_contract.md`, then rebuild `state/next_lesson_context.json`. Collect:

- first-attempt errors and repeated attempts;
- topics marked uncertain;
- optional unfinished practice;
- the learner's explanation preference;
- due review topics when a review scheduler is active.

Read the compact local `state/next_lesson_context.json` as the model-facing personalization input. Show an honest generating state. Only change the route item from `ready-to-generate` to `current` after a complete lesson has been generated. Preserve access to completed lessons.

## Explanation Preferences

Provide a lightweight optional selector with `balanced` as the default:

| Value | Behavior |
| --- | --- |
| `balanced` | Balance concepts, examples, and practice. |
| `intuition-first` | Add analogies, diagrams, and concrete examples. |
| `math-focused` | Add definitions, formulas, and derivations. |
| `practice-focused` | Add structured exercises, coding tasks, or transfer questions. |

The learner may override any recommendation. Do not silently infer a preference from weak signals.

## Dynamic Lesson Duration

Do not force every lesson to claim a fixed duration such as 45 minutes. Estimate reading, micro-assessment, practice, and recap separately after the lesson structure is known, then show the total.

## Quality Gate

- Long tutorials explain progressive generation on the homepage.
- Future route items are inspectable, not silent dead ends.
- The next lesson is generated only after explicit learner action.
- Submitted answers, confirmations, and preferences are persisted to local files before generation; the model reads compact extracted context instead of scraping UI state.
- Wrong answers inform the next lesson but never become a hard progression gate.
- Generated lessons remain complete, independently studyable learning units.
