# Tutorial Learning — Delivery Summary

## Skill location

`skills/tutorial-learning/` — governed by [meta-skill](https://github.com/41732070pan-coder/Codex-skill/tree/main/skills/meta-skill).

## Architecture

- **Abstract:** `references/learning_contract.md` (`TutorialLearningBase`)
- **Family:** `registry/mediums.yaml` — first implementation `pdf-chaptered`
- **Concrete:** `implementations/pdf-chaptered/SKILL.impl.md`
- **Phase 2:** `references/h5_lesson_schema.md` (stub only)

## Lab sources

| ID | Book | Rounds | License |
| --- | --- | --- | --- |
| source-a | [Think Python 2e](https://greenteapress.com/thinkpython2/thinkpython2.pdf) | R1–R5 | CC BY-NC |
| source-b | [Eloquent JavaScript 4e](https://eloquentjavascript.net/Eloquent_JavaScript.pdf) | R6–R10 | CC BY-NC (see book) |

OpenStax PDF was blocked (403) in lab; source-b substituted per `lab/sources/source-b.json`.

## Final lectures

- Think Python §1.1: `lab/lectures/r05-section01.md` (converged)
- Eloquent JS Values: `lab/lectures/r10-section01.md` (converged)

## Iteration

- 40 steps: `lab/iteration-log.md`
- Skill changes: `lab/CHANGELOG-skill.md`
- Eval trend: 16/25 (R1) -> 25/25 (R10)

## Validators

```powershell
# When Python is available:
python skills/tutorial-learning/scripts/validate_tutorial_learning.py
python skills/meta-skill/scripts/validate_skills.py
python skills/meta-skill/scripts/validate_skill_boundaries.py

python skills/tutorial-learning/scripts/resolve_medium.py resolve pdf-chaptered
```

## Usage

1. Load `$tutorial-learning` when studying a chaptered PDF tutorial.
2. Resolve medium: `pdf-chaptered`.
3. Provide PDF URL/path + section scope.
4. Outputs: Chinese lecture Markdown, `*.triage.json`, `*.review_plan.json`, optional `*.h5_stub.json`.
