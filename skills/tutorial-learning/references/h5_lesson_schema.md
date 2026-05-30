# H5 / Hypertext Lesson Projection

The default projection is a lightweight structured view of the lecture, not a frontend implementation. It lets future H5 or review applications map source traces, concepts, objectives, interactions, and review cards without coupling the skill to a web stack.

## Stub JSON (v0.2)

```json
{
  "schema_version": "0.2-hypertext-stub",
  "h5_lesson_id": "hypertext-tutorial-example-ch01-s01",
  "source": {
    "format": "pdf",
    "title": "",
    "locator": "",
    "section_id": ""
  },
  "source_traces": [
    {
      "id": "st1",
      "pageRange": [1, 2],
      "headingPath": ["Chapter 1", "Section 1"],
      "anchor": "",
      "boundaryConfidence": "explicit",
      "evidenceType": "source-derived"
    }
  ],
  "concept_ids": ["kp1"],
  "learning_objective_ids": ["lo1"],
  "interactions": [
    {
      "type": "prediction",
      "id": "ix1",
      "prompt": "",
      "objective_id": "lo1",
      "source_trace_ids": ["st1"]
    },
    {
      "type": "self_explain",
      "id": "ix2",
      "prompt": "",
      "objective_id": "lo1",
      "source_trace_ids": ["st1"]
    }
  ],
  "review_card_ids": ["rc1"],
  "progress_key": "tutorial-learning/<h5_lesson_id>"
}
```

## Mapping Rules

- Each `learning_objective_ids[]` entry must appear in lecture front matter.
- Each source trace may use PDF page ranges, HTML anchors, Markdown heading paths, URLs, or extraction slices.
- Each micro-assessment item should have a matching `interactions` entry when a projection is emitted.
- `progress_key` is reserved for a future client; this skill does not implement client storage.

## Optional Expanded Review App Contract

Generate this only when the user explicitly asks for interactive review or H5 planning.

| Screen | Purpose | Required controls |
| --- | --- | --- |
| `overview` | Show objectives, source traces, and concept map. | Start, jump to source trace. |
| `concept-drill` | Reveal concept prompts and ask teach-back. | Reveal, self-grade, mark uncertain. |
| `practice` | Run a small task with expected checks. | Submit/check or self-check. |
| `quiz` | Immediate feedback for micro-assessment. | Answer, retry, remediation hint. |
| `review` | Schedule day 1/3/7 review cards. | Mark remembered/forgotten. |

## Forbidden In This Skill

- Do not generate frontend app code unless the user explicitly requests implementation work.
- Do not store learner progress; only define stable ids and projection fields.
