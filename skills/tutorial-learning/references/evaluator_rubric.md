# Evaluator Rubric

Score each category 0–5. Fix any blocking failure before delivery even if the numeric score is otherwise high.

## Categories

### 1. Source Fidelity (0–5)

- Source traces identify page ranges, anchors, heading paths, URLs, or extraction slices.
- Boundary and extraction uncertainty are explicit.
- Source-derived, inferred, supplementary, and user-supplied content are not conflated.
- No lesson content is invented from headings or navigation alone.

### 2. Triage And Depth Routing (0–5)

- Filler, navigation, duplicated headers/footers, sidebars, and decorative content are omitted from the lecture body.
- Reference-only content goes to the appendix.
- Core/supporting decisions match the requested scope and learning objectives.
- Time budget trims skim/supporting material before core material.
- Important skipped content has a source location or non-fabricated deep dive.

### 3. Chinese Lecture Quality (0–5)

- Chinese is clear and mechanism-first.
- Identifiers, commands, formulas, API names, and URLs preserve original spelling.
- Objectives are 2–4, verifiable, and source-traced.
- The lesson is not a source paste.

### 4. Assessment And Review (0–5)

- Micro-test includes prediction, teach-back, and application when applicable.
- Practice task is checkable when the section supports practice.
- Review cards map to objectives and source traces.
- Spaced schedule uses day 1/3/7 or a justified variant.

## Blocking Failures

- Fabricated source content.
- Long verbatim copyrighted excerpts without user-provided permission and necessity.
- Rights/use uncertainty ignored when it materially affects output.
- Filler appears in the lecture body as core content.
- Reference-only content becomes a learning objective without an explicit user goal.

## Output Format

```markdown
## Scores
| Category | Score | Evidence | Patch |
| --- | ---: | --- | --- |

## Blocking failures
- None / ...

## Top patches
- P0: ...
- P1: ...
- P2: ...
```
