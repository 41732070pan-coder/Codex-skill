# Evaluation Rubric

Use this rubric for self-review or subagent review. Score each category 0-2 and record at least one concrete improvement when any score is below 2.

| Category | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Source traceability | Missing source metadata or section trace. | Source exists but unit evidence is loose. | Source, access date, unit, and evidence are clear. |
| Abstraction integrity | Output is hard-coded to one medium. | Mentions abstraction but concrete implementation leaks upward. | High-level contracts and implementation body remain separated. |
| Content classification | No core/reading/filler split. | Some labels but inconsistent. | Every major source segment is classified. |
| Depth decision | Summaries lack skip/master logic. | Depth exists but reasons are thin. | Each major point has reasoned depth and deeper-link policy. |
| Learning usefulness | Notes are mostly paraphrase. | Some quizzes or tasks. | Goals, mental model, quiz, practice, pitfalls, and review cards are all present. |
| Web review readiness | No app spec. | Vague UI notes. | Screens, controls, state, and feedback rules are specified. |
| Iteration closure | Feedback is not applied. | Feedback appears but mapping is unclear. | Evaluation finding maps to a concrete skill/output change. |

## Required Evaluation Output

```md
## Evaluation
- Scores:
- Highest-risk issue:
- Evidence:
- Required skill change:
- Required lecture change:
- Gate decision:
```

## Hard Fails

- Invented source details.
- Long verbatim copyrighted excerpts.
- No assessment or review card for a section-level lecture.
- No distinction between core knowledge and low-value filler.
- Iteration logs that do not show which evaluation finding caused which change.
