# Evaluator Rubric (Lab / Audit)

Score each category 0–5. Total /30. Provide **≥3** prioritized patches (`P0`–`P2`).

## Categories

### 1. Triage (0–5)

- Filler truly omitted from body; not mislabeled as core.
- Reference-only in appendix only.
- Skip + deep_dive justified when important but low personal use.

### 2. Depth routing (0–5)

- `est_minutes` sum reasonable vs `time_budget`.
- skim/standard/deep matches composite scores.
- No over-deep treatment of low-importance blocks.

### 3. Lecture quality (0–5)

- Chinese clear; terms preserved.
- 2–4 verifiable objectives; not PDF paste.
- Mechanism-first explanations.

### 4. Assessment (0–5)

- Micro-test checks understanding (predict, self-explain, apply).
- Review cards align with objectives.

### 5. Skill maintainability (0–5)

- Contracts executable; load boundaries clean.
- No overlap with `pdf` / `c-os-learning-tutor`.
- Templates referenced, not duplicated ad hoc.

### 6. Migration (0–5)

- Rounds 1–5: score N/A or 3/5 baseline if single source only.
- Rounds 6–10: same pipeline on second source without forked one-off rules.

## Output format

```markdown
## Scores
| Category | Score | Note |
...

## Top patches
- P0: ...
- P1: ...
- P2: ...

## Adopted next round
- [ ] item
```
