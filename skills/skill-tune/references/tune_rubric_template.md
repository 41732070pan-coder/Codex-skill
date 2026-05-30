# Per-Skill Tune Rubric Template

Copy to `skills/<Askill>/references/tune_rubric.md`.

## Rubric meta

```markdown
## Rubric meta
rubric_id: tune_rubric
excellence_gate: all_dimensions
```

## Dimensions

| ID | What to score | Threshold | 3 (acceptable) | 5 (excellent) |
| --- | --- | --- | --- | --- |
| `taskFit` | Fit to the stated scenario | 5 | Addresses main intent with minor gaps | Fully addresses the user task |
| `exampleCustom` | Domain-specific criterion | 5 | Acceptable bar | Excellent bar |

After editing:

```bash
python scripts/tune_session.py resolve-rubric --askill-dir skills/<Askill>
```
