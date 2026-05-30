# Rubric Contract

Active rubric drives judge scoring, excellence gate, log rendering, and machine validation.

## ActiveRubric (resolved each session)

```ts
interface RubricDimension {
  id: string;
  label?: string;
  excellentThreshold: number;  // from Threshold column, default 5
}

interface ActiveRubric {
  rubricId: string;
  sourcePath: string;
  excellenceGate: "all_dimensions";
  dimensions: RubricDimension[];
  dimensionIds: string[];
}
```

Resolve with:

```bash
python scripts/tune_session.py resolve-rubric --askill-dir skills/<Askill> --write /tmp/active_rubric.json
```

## Resolution Order

1. `TuneRequest.rubricPath` when set
2. Else `skills/<Askill>/references/tune_rubric.md`
3. Else `skill-tune/references/default_rubric.md`

## Rubric File Shape

```markdown
## Dimensions

| ID | What to score | Threshold | 3 (acceptable) | 5 (excellent) |
| --- | --- | --- | --- | --- |
| `taskFit` | ... | 5 | ... | ... |
```

| Parsing rule | Behavior |
| --- | --- |
| Threshold column | Integer per row; gate uses `score >= Threshold`. |
| Missing Threshold cell | Tools default to `5`. |
| Custom dimensions | Allowed; `dimensionIds` and log score tables follow the resolved rubric. |

## JudgeResult (JSON required for validation)

Prefer `judge_result.json` in the round artifact directory:

```json
{
  "round": 1,
  "rubricId": "default_rubric",
  "dimensionIds": ["taskFit", "clarity"],
  "judgeRole": "product_manager",
  "isolatedJudge": true,
  "scores": { "taskFit": 3, "clarity": 5 },
  "thresholds": { "taskFit": 5, "clarity": 5 },
  "overall": "fail",
  "findings": [
    {
      "dimension": "taskFit",
      "score": 3,
      "gap": "...",
      "evidenceQuote": "verbatim substring from out"
    }
  ],
  "priorityFixes": ["..."]
}
```

Validate:

```bash
python scripts/tune_session.py validate-judge-result \
  --result tune_sessions/<session>/round-001/judge_result.json \
  --rubric-json tune_sessions/<session>/round-001/active_rubric.json \
  --out-file tune_sessions/<session>/round-001/out.md
```

## Log Rendering

- Scores table: one row per resolved dimension (not a fixed five).
- Header includes `Rubric dimensions` as comma-separated ids.
- Round block indexes artifact paths and sha256 from `manifest.json` (see `artifacts_contract.md`).
