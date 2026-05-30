# Review Protocol

## Review Cards

Per section, emit 3–5 `ReviewCard` entries:

- Mix `recall` and `application` prompts.
- At least one prompt asks the learner to explain a concept in their own words.
- Each card maps to one or more learning objective ids.
- Each card carries source trace ids for auditability.
- `answer_hint` is for self-grading and should not become source-paste.

## Spaced Schedule

Default `due_offsets_days` per card: `[1, 3, 7]`.

| Day | Action |
| --- | --- |
| 1 | Active recall without notes. |
| 3 | Recall + connect to a prior section or source trace. |
| 7 | Application, teach-back, or transfer. |

## review_plan.json Shape

```json
{
  "section_id": "ch01-s01",
  "cards": [
    {
      "id": "rc1",
      "prompt": "...",
      "answer_hint": "...",
      "mastery": "recall",
      "objective_ids": ["lo1"],
      "source_trace_ids": ["st1"]
    }
  ],
  "schedule": [
    { "card_id": "rc1", "due_offsets_days": [1, 3, 7] }
  ]
}
```

## Quality Gate

- Cards cover at least 80% of learning objectives.
- No card asks the learner to copy verbatim from the source.
- Duplicate cards across adjacent sections are avoided.
- Application cards include a checkable expected behavior or answer criterion.
