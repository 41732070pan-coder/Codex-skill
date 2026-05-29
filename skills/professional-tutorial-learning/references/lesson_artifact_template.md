# Lesson Artifact Template

Use this template for markdown-first lessons. Keep headings stable so the artifact can later be parsed into a web learning app.

```markdown
# <Lesson title>

## Source Metadata

| Field | Value |
| --- | --- |
| Source title | <title> |
| Source type | <pdf/web/video/transcript/mixed> |
| Source locator | <file path or URL> |
| Author / publisher | <known or unknown> |
| Access date | <date or not applicable> |
| Chapter / section | <position> |
| Boundary confidence | <explicit/inferred-high/inferred-medium/inferred-low> |
| Lesson id | <stable id> |
| Estimated time | <minutes> |
| Learning depth | <deep/normal/skim/skip-with-link mix> |

## Why This Section Matters

<One concise paragraph tied to the learner goal.>

## Learning Objectives

- <observable objective>

## Knowledge Point Map

| Id | Knowledge point | Class | Depth | Why |
| --- | --- | --- | --- | --- |
| KP1 | <label> | core/supporting/reading/skip/advanced | deep/normal/skim/skip-with-link | <rationale> |

## Reading-Only Material

- <context that is useful to read but not memorize or practice deeply>

## Skipped Or Compressed Material

- <what was skipped or compressed and why>

## Guided Explanation

### <Concept block>

<Short explanation in the learner's language.>

## Worked Example

<Small example, walkthrough, or scenario.>

## Practice Task

<Prompt plus expected result.>

## Checkpoint Questions

1. <question>
   - Answer guide: <short guide>

## Common Pitfalls

- <pitfall and correction>

## Review Prompts

| When | Prompt |
| --- | --- |
| Same day | <prompt> |
| Next day | <prompt> |
| One week | <prompt> |

## Further Reading / Deep Dives

- [<label>](<url>) — <why this link matters>

## Web App Data

```json
{
  "lessonId": "<stable lesson id>",
  "contentBlockIds": ["CB1"],
  "practiceIds": ["P1"],
  "checkpointIds": ["C1"],
  "reviewPromptIds": ["R1"],
  "furtherReadingIds": ["L1"]
}
```

## Next Lesson Preview

<What to learn next and why.>
```

## Web-App-Compatible Fields

```json
{
  "lessonId": "string",
  "source": {},
  "unit": {},
  "estimatedMinutes": 30,
  "objectives": [],
  "knowledgePoints": [],
  "contentBlocks": [],
  "practice": [],
  "checkpoints": [],
  "reviewSchedule": [],
  "furtherReading": [],
  "webAppData": {
    "contentBlockIds": [],
    "practiceIds": [],
    "checkpointIds": [],
    "reviewPromptIds": []
  },
  "nextLessonPreview": "string"
}
```
