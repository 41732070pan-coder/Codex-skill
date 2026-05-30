# Sample Tune Round (documentation only)

Fictional one-round excerpt for `define-goal`. Do not treat as live judge output.

## Setup

| Field | Value |
| --- | --- |
| Askill | `define-goal` |
| Scenario | Turn the vague request "make the app faster" into a concrete, measurable goal. |
| Judge role | `product_manager` |
| Rubric | `default_rubric` |
| Expected artifact type | Measurable goal statement with verification evidence and scope bounds |

## Mock out (abbreviated)

```markdown
## Proposed goal

Make the application faster for users.

## Success

We will know it is faster when users feel it is snappy.
```

## Mock JudgeResult

```yaml
round: 1
rubricId: default_rubric
dimensionIds: [taskFit, clarity, completeness, correctness, artifactAlignment]
judgeRole: product_manager
isolatedJudge: true
scores:
  taskFit: 3
  clarity: 4
  completeness: 2
  correctness: 4
  artifactAlignment: 3
thresholds:
  taskFit: 5
  clarity: 5
  completeness: 5
  correctness: 5
  artifactAlignment: 5
overall: fail
findings:
  - dimension: taskFit
    score: 3
    gap: Goal is not measurable; no metric or verification command.
    evidenceQuote: "when users feel it is snappy"
  - dimension: completeness
    score: 2
    gap: Missing scope bounds, evidence standard, and stop condition.
    evidenceQuote: "Make the application faster for users."
  - dimension: artifactAlignment
    score: 3
    gap: Deliverable reads as a slogan, not a measurable goal with verification evidence.
    evidenceQuote: "We will know it is faster when users feel it is snappy"
priorityFixes:
  - Require a quantitative or binary validator in the objective
  - Reject subjective-only success criteria unless user confirms
```

## Mock improve (summary)

- Files touched: `define-goal/SKILL.md`
- Hypothesis: Quantification checklist raises `taskFit` and `completeness` on rerun
- Under "Goal Quality Bar", reject subjective-only success unless sharpened with a metric or test command.
- Under workflow step 4, require verification evidence in the objective before `create_goal`.

## Mock log excerpt (`skills/define-goal/self-iter.md`)

File header (once):

```markdown
# Self-iteration log: define-goal

| Field | Value |
| --- | --- |
| Skill path | skills/define-goal/ |
| Rubric | default_rubric |
| Rubric dimensions | taskFit, clarity, completeness, correctness, artifactAlignment |
| Started | 2026-05-30T12:00:00Z |
| Purpose excerpt | Shape intent into measurable goals before work starts. |

---
```

Round block:

```markdown
## Round 1

| Field | Value |
| --- | --- |
| Timestamp | 2026-05-30T12:00:00Z |
| Scenario | Turn the vague request "make the app faster" into a concrete, measurable goal. |
| Judge role | product_manager |
| Isolated judge | yes |
| Overall | fail |

### Scores

| Dimension | Score | Excellent threshold |
| --- | --- | --- |
| taskFit | 3 | 5 |
| clarity | 4 | 5 |
| completeness | 2 | 5 |
| correctness | 4 | 5 |
| artifactAlignment | 3 | 5 |

### Findings

- **taskFit (3)**: Goal is not measurable; no metric or verification command.
  - Evidence: "when users feel it is snappy"
- **completeness (2)**: Missing scope bounds, evidence standard, and stop condition.
  - Evidence: "Make the application faster for users."
- **artifactAlignment (3)**: Deliverable does not match scenario-implied measurable goal with verification evidence.
  - Evidence: "We will know it is faster when users feel it is snappy"

### Priority fixes

1. Require a quantitative or binary validator in the objective
2. Reject subjective-only success criteria unless user confirms

### Output (out)

- Path: inline
- Summary: Vague performance goal with subjective success criterion only

### Improve

| Field | Value |
| --- | --- |
| Files touched | `SKILL.md` |
| Hypothesis | Quantification rules should raise taskFit and completeness on round 2 |

- Under "Goal Quality Bar", add: reject objectives with only subjective success unless sharpened with a named metric or test command.
- Under workflow step 4, add explicit check: objective must name verification evidence before `create_goal`.

---
```

Next round would **Run** again with the same scenario (not the judge text) to verify the updated skill.
