# Tune Contract

Normalized request and round artifacts for `skill-tune` sessions.

## TuneRequest

```ts
interface TuneRequest {
  targetSkill: string;
  scenario: string;
  maxRounds?: number;        // default 3
  rubricPath?: string;
  judgeRole?: "product_manager" | "creator";
  expectedArtifactType?: string;
}
```

| Field | Required | Rule |
| --- | --- | --- |
| `targetSkill` | yes | User-maintained `skills/<Askill>/SKILL.md`. Reject `.system/`, plugin caches, `~/.cursor/skills-cursor/` unless copied into `skills/<Askill>/` first. |
| `scenario` | yes | Concrete user-style task. Required to trigger skill-tune (structural review without scenario/out goes to meta-skill). |
| `maxRounds` | no | Default `3`. Stop early on `pass_excellent` or user abort. |
| `rubricPath` | no | See `references/rubric_contract.md` resolution order. |
| `judgeRole` | no | PM for deliverables; creator for craft or pedagogy. |
| `expectedArtifactType` | no | Scenario-derived; for judge only. |

## Active Rubric

Resolve before Run and Judge. Shape: `ActiveRubric` in `references/rubric_contract.md`.

## Output Artifact (`out`)

See `references/run_contract.md` for capture rules.

| Property | Rule |
| --- | --- |
| Definition | Final deliverable(s) from Run with Askill only. |
| Forms | Paths + excerpts, inline markdown, or manifest per run_contract. |
| Isolation | No production chat, judge rounds, or improve diffs attached. |

## JudgeResult

Machine validation requires **`judge_result.json`** (see `references/rubric_contract.md`). YAML is optional for human editing; run `validate-judge-result` before `append-log`.

Required fields: `round`, `rubricId`, `dimensionIds`, `judgeRole`, `isolatedJudge`, `scores`, `thresholds`, `overall`, `findings`, `priorityFixes`.

`scores` and `thresholds` are dynamic maps keyed by `dimensionIds`. `thresholds` must match `excellentThreshold` from the active rubric.

| `overall` | Meaning |
| --- | --- |
| `pass_excellent` | For every id in `dimensionIds`, `scores[id] >= thresholds[id]`. |
| `fail` | At least one dimension below threshold; improve unless user stops. |

`scores` and `thresholds` keys must match `dimensionIds` exactly.

## ImproveRecord

```yaml
round: number
filesTouched: string[]
changesSummary: string[]
hypothesis: string
generalizedFrom: string   # finding dimension + gap, not scenario-specific answer text
```

## Session Exit

| Status | When |
| --- | --- |
| `excellent` | Last round `pass_excellent`. |
| `capped` | `maxRounds` without excellence. |
| `aborted` | User stopped. |

Log path: `skills/<Askill>/self-iter.md` (append-only).
