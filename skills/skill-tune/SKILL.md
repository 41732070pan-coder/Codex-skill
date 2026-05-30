---
name: skill-tune
description: Tune an existing skill after a scenario run. Isolated judge on output, improve until excellent. Use tune_session.py. Not for skill creation.
---

# Skill Tune

## Purpose

Improve an **existing** skill (Askill): **scenario** -> **Run** (Askill only) -> **out** -> **Judge** (isolated) -> **Improve** when not excellent -> log **`skills/<Askill>/self-iter.md`** plus per-round artifacts.

Structural work uses **`meta-skill`**.

## Install Location

```text
skills/skill-tune/
```

## Orchestration (tools)

**Windows:** prefer `.\scripts\run.ps1` or run `scripts/check_runtime.py` and use the printed executable path.

```powershell
.\scripts\check_runtime.ps1   # optional; run.ps1 calls check_runtime when needed
.\scripts\run.ps1 init-session --target <Askill> --scenario "..." --session-id 2026-05-30 --skills-root <repo>/skills
```

### Session driver (recommended)

```text
init-session -> Run (Askill) -> out.md + judge_result.json
  -> [fail] record-improve -> complete-round
  -> [continue] next-round -> repeat
```

```bash
# 1) Start session (target check, rubric, log header, round-001 dir)
<PY> scripts/tune_session.py init-session \
  --target define-goal --scenario "..." --session-id 2026-05-30 \
  --skills-root <repo>/skills

# 2) After Run: copy deliverable to round dir
<PY> scripts/tune_session.py write-out \
  --round-dir skills/<Askill>/tune_sessions/<session>/round-001 --out-file /tmp/out.md

# 3) Isolated judge -> judge_result.json in round dir; validate
<PY> scripts/tune_session.py validate-judge-result --result .../judge_result.json \
  --rubric-json .../active_rubric.json --out-file .../out.md

# 4) Fail rounds: record improve (writes improve_record.json + summary)
<PY> scripts/tune_session.py record-improve --round-dir .../round-001 \
  --summary /tmp/improve.md --round 1 --files-touched SKILL.md \
  --hypothesis "..." --change "..." --generalized-from "taskFit: ..."

# 5) Close round (validate, manifest, append-log, session-end if done)
<PY> scripts/tune_session.py complete-round \
  --askill-dir skills/<Askill> --session-id 2026-05-30 --round 1 \
  --out-summary "one line"

# 6) Next round if not stopped
<PY> scripts/tune_session.py next-round \
  --askill-dir skills/<Askill> --session-id 2026-05-30
```

Shorthand: `run-session init ...`, `run-session complete-round ...`, `run-session next-round ...`

Low-level commands (`resolve-target`, `build-judge-packet`, `append-log`, ...) remain available. See `references/artifacts_contract.md`.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Tune an **existing** skill with a **concrete scenario** and **output artifact** (`out`) to judge. |
| Trigger | self-iter loop, forward-test, rubric excellence gate, isolated judge of deliverable. |
| Non-trigger | Skill creation, rename, registry, governance audit -> **`meta-skill`**. |
| Non-trigger | Evaluate/review a skill **without** scenario **and** without `out` -> **`meta-skill`**. |
| Non-trigger | One-off domain run without changing the skill. |
| Non-trigger | Non-user-maintained skills (`.system/`, plugin caches, `skills-cursor/`) unless copied to `skills/<Askill>/`. |

## Workflow

1. **Normalize** — `TuneRequest` in `references/tune_contract.md` (`targetSkill`, `scenario` required).
2. **resolve-target** — script enforces user-maintained `skills/<Askill>/`.
3. **resolve-rubric** — dynamic dimensions and thresholds; write `active_rubric.json`.
4. **Run** — `references/run_contract.md`; **init-round-dir** captures `out.md` + manifest.
5. **Judge** — `build-judge-packet`; isolated judge; **validate-judge-result** on `judge_result.json`.
6. **Gate** — `pass_excellent` when all `scores[id] >= thresholds[id]`.
7. **Improve** — `references/improve_contract.md` if fail; **record-improve** for artifacts.
8. **append-log** — index artifacts; Improve section only on fail.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required | `targetSkill`, `scenario`; `out` before judge |
| Outputs | Askill edits; `self-iter.md`; `tune_sessions/<session>/round-*/` artifacts |

## References

| Reference | Load when |
| --- | --- |
| `tune_contract.md` | Session start |
| `rubric_contract.md` | Rubric resolve / judge validate |
| `run_contract.md` | Run step |
| `artifacts_contract.md` | Round dirs and manifest |
| `judge_contract.md` | Judge step |
| `default_rubric.md` | No per-skill rubric |
| `improve_contract.md` | Improve step |
| `self_iter_template.md` | Log format |

## Resources

- Scripts: `tune_session.py`, `tune_lib.py`, `validate_skill_tune.py`, `check_runtime.py`
- Per-target: `self-iter.md`, `tune_sessions/`, optional `references/tune_rubric.md`

## Extension Points

| Extension | File |
| --- | --- |
| Per-skill rubric | `skills/<Askill>/references/tune_rubric.md` |
| Round artifacts | `references/artifacts_contract.md` |

## Quality Gate

**Session:** `validate-judge-result` passes; manifest hashes match files.

**Module:**

```bash
python scripts/check_runtime.py
python scripts/validate_skill_tune.py
```

Installed in a skills repo:

```bash
python skills/meta-skill/scripts/validate_skills.py
```

`git diff --check` only inside a git work tree.
