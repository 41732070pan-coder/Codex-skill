# Review Protocol

## Review cards

Per section, emit 3–5 `ReviewCard` entries:

- Mix `recall` (definitions, steps) and `application` (small scenario).
- At least one "用自己的话解释 …" prompt.
- `answer_hint` is for self-grading, not shown in lecture body by default.

## Spaced schedule (simplified SM-2)

Default `due_offsets_days` per card: `[1, 3, 7]`.

| Day | Action |
| --- | --- |
| 1 | Active recall without notes |
| 3 | Recall + connect to prior section |
| 7 | Application or teach-back |

## review_plan.json shape

```json
{
  "section_id": "ch01-s01",
  "cards": [
    {
      "id": "rc1",
      "prompt": "...",
      "answer_hint": "...",
      "mastery": "recall",
      "due_offsets_days": [1, 3, 7]
    }
  ],
  "schedule": [
    { "card_id": "rc1", "due_offsets_days": [1, 3, 7] }
  ]
}
```

## Quality gate

- Cards map to learning objectives (coverage ≥ 80%).
- No card asks to copy verbatim from PDF.
- Duplicate cards across adjacent sections avoided.
