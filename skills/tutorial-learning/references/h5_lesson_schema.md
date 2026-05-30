# H5 Lesson Schema (Phase 2 Stub)

No browser implementation in current phase. Export stub JSON alongside lecture for future Vite + TypeScript + Web Components stack (aligned with `c-os-learning-tutor` / `kernel-note-code-linker`).

## Stub JSON (v0.1)

```json
{
  "schema_version": "0.1-stub",
  "h5_lesson_id": "pdf-chaptered-thinkpython2-ch01",
  "source": {
    "medium": "pdf-chaptered",
    "title": "",
    "section_id": ""
  },
  "learning_objectives": [],
  "interactions": [
    {
      "type": "prediction",
      "id": "ix1",
      "prompt": "",
      "objective_id": "lo1"
    },
    {
      "type": "self_explain",
      "id": "ix2",
      "prompt": "",
      "objective_id": "lo2"
    }
  ],
  "review_card_ids": [],
  "progress_key": "tutorial-learning/<h5_lesson_id>"
}
```

## Mapping rules

- Each `learning_objectives[].id` must appear in lecture front matter.
- Each micro-assessment item should have a matching `interactions` entry when H5 is built.
- `progress_key` is reserved for `localStorage` in Phase 2.

## Forbidden in stub phase

- Do not add `interactive/` app code under this skill until user requests Phase 2.
