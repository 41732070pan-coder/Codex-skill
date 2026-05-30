# Depth Policy

Use this policy to decide whether content should be skipped, skimmed, understood, practiced, or mastered.

## Scoring Inputs

| Field | Meaning |
| --- | --- |
| `importance` | How central the point is to later tutorial progress. |
| `difficulty` | How much explanation and practice the learner needs. |
| `usefulness` | How likely the learner is to use it in real professional work. |
| `sourceRole` | Whether the source treats it as mainline concept, example, aside, warning, exercise, reference, or appendix. |
| `learnerGoalFit` | Whether it supports the user's stated goal and near-term tasks. |

## Depth Decisions

| Decision | Use when | Required output |
| --- | --- | --- |
| `skip_link_only` | Complex, low-use, tangential, outdated, or source-side detail. | One-sentence reason plus a deeper link. |
| `skim` | Useful context but not needed for practice. | Short summary and why it matters. |
| `understand` | Conceptual prerequisite or common source of confusion. | Explanation, example, pitfall, quiz item. |
| `practice` | Skill must be executable, not just recognized. | Worked pattern, exercise, expected result. |
| `master` | Foundational, repeated later, or high professional value. | Mental model, practice, quiz, review card, error cases. |

## Default Rule

Use a balanced default:

```text
depth_score = importance + usefulness - max(0, difficulty - learner_support)
```

Then override with source role:

- Appendices and historical notes usually become `skim` or `skip_link_only`.
- Exercises/examples become `practice` when they test a core concept.
- Setup instructions become `understand` only when blocking; otherwise `skim`.
- Advanced implementation internals become `skip_link_only` unless the learner goal asks for them.

## Filler Detection

Treat content as `low_value_filler` when it is repetitive marketing, long contributor lists, non-instructional acknowledgments, verbose story without a learning function, duplicated table-of-contents material, or outdated operational detail. Do not discard copyright/license notices; classify them as `reference`.
