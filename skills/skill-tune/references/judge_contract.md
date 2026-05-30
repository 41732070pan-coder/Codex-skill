# Judge Contract

Isolated evaluation of `out` only. The judge must not see how `out` was produced.

## Judge Roles

| Role | Use when | Emphasis |
| --- | --- | --- |
| `product_manager` | Deliverables, user tasks, specs, decisions | User value, completeness, clarity, fitness for scenario |
| `creator` | Lessons, docs, design craft, pedagogy | Structure, voice, teaching flow, craft quality |

Pick one role per round; record it in the log and `JudgeResult`.

## Allowed Context

- `scenario` (one-line summary of the user task)
- Rubric table and excellent thresholds (from active rubric)
- Raw `out` (full text or faithful excerpts with paths)
- Judge role definition (PM or creator)
- **`expectedArtifactType`** (optional, max one or two sentences): deliverable shape implied by the scenario only — e.g. "measurable goal statement with verification evidence", "lesson note with exercises". Do **not** copy from Askill `SKILL.md` or references.

## Forbidden Context

Do not pass any of the following to the judge:

| Forbidden | Reason |
| --- | --- |
| Askill `SKILL.md` or references | Leaks intended behavior; judge must evaluate product only |
| Production conversation from the run step | Leaks process and fixes |
| Prior `self-iter.md` rounds | Leaks iteration history and expected fixes |
| Diffs, improve plans, or suspected root causes | Leaks diagnosis; judge must derive gaps from `out` |
| Other skills' instructions | Irrelevant and biases scoring |

## Execution Modes

Use a **platform-agnostic** isolation strategy. Do not assume a specific subagent API.

### Preferred: isolated judge pass

When the runtime provides a **separate judge context** that the user or policy allows (e.g. dedicated subagent, child agent, or fresh thread) **and** that context can be limited to the allowed inputs above:

1. Start judge work only after `out` is finalized.
2. Pass the judge prompt template below and nothing from the forbidden list.
3. Record `isolatedJudge: yes` in the log.

**Spawn constraints**: Only use subagents or parallel agents when the user explicitly requests them or platform policy allows. Never spawn solely because this skill prefers isolation.

### Fallback: fresh pass in the current agent

When no allowed isolated mechanism exists:

1. State explicitly: judging in isolation; ignoring all prior production context except allowed inputs.
2. Use the same prompt template; do not re-read Askill `SKILL.md` during the judge step.
3. Warn the user that isolation is weaker than a separate context.
4. Record `isolatedJudge: no` in the log.

## Judge Prompt Template

Use this shape; replace placeholders only:

```text
You are a {judgeRole} reviewing a final deliverable. You have NOT seen how it was produced.

## User scenario
{scenario_one_liner}

## Expected artifact type (from scenario only)
{expectedArtifactType_or_none}

## Rubric
{rubric_table_with_excellent_criteria}

Score each dimension 1-5. Excellent means meeting the "Excellent" column for that dimension.
Set overall to pass_excellent only if EVERY dimension is excellent.

## Deliverable (out)
{out_body_or_excerpt_with_paths}

## Rules
- Base all findings only on the deliverable above and the scenario.
- Score every dimension id listed in the rubric; use the excellent threshold shown for each.
- For each sub-excellent dimension, quote evidence from out.
- Output judge_result.json per skill-tune/references/rubric_contract.md (JSON required for validate-judge-result).
- Do not suggest skill edits; only score and prioritize fixes for the deliverable.
```

## Integrity Checks

Before accepting judge output:

- Every `evidenceQuote` appears in the provided `out`.
- `scores` and `thresholds` keys match `dimensionIds` from the active rubric.
- Scores are integers 1-5 unless the rubric documents another scale.
- `overall: pass_excellent` implies every dimension meets its threshold.
- No finding cites Askill instructions unless that text appears in `out`.
