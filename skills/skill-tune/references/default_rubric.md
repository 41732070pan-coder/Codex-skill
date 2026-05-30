# Default Rubric

Used when `skills/<Askill>/references/tune_rubric.md` does not exist.

## Excellence Gate

**Excellent** when every dimension has `score >= Threshold`. Default threshold is **5** when the Threshold column is omitted (parsed as 5 by `scripts/tune_lib.py`).

## Dimensions

| ID | What to score | Threshold | 3 (acceptable) | 5 (excellent) |
| --- | --- | --- | --- | --- |
| `taskFit` | Fit to the stated scenario | 5 | Addresses main intent with minor gaps | Fully addresses the user task with no major gaps |
| `clarity` | Structure and readability | 5 | Understandable with some re-reading | A new reader can follow without production context |
| `completeness` | Implied deliverables present | 5 | Most expected sections or artifacts present | All deliverables implied by scenario and expected artifact type are present |
| `correctness` | Accuracy visible in `out` alone | 5 | No major errors; minor issues only | No material errors or unsafe guidance visible in the artifact |
| `artifactAlignment` | Fit to scenario-implied artifact type and scope | 5 | Mostly matches expected type; minor scope drift | Deliverable type, scope, and tone match scenario and stated expected artifact type; no obvious drift |

## Threshold Rules

| Rule | Detail |
| --- | --- |
| Column | Use **Threshold** (integer). If absent for a row, tools default to `5`. |
| Gate | `pass_excellent` when every dimension has `score >= Threshold`. |
| Override | Per-skill `tune_rubric.md` may set Threshold per row (e.g. `4` for softer bars). |
| Tools | `python scripts/tune_session.py resolve-rubric` writes `active_rubric.json` with `excellentThreshold` per dimension. |

## `artifactAlignment` (judge-safe)

Judges do **not** read Askill `SKILL.md`. Score using only scenario, optional `expectedArtifactType`, and `out`.

## Per-Skill Override

Copy `references/tune_rubric_template.md` to `skills/<Askill>/references/tune_rubric.md` to add/remove rows or change thresholds.
