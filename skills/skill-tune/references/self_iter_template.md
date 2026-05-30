# Self-Iter Log Template

Path: `skills/<Askill>/self-iter.md` (append-only).

## File Header (create once)

After resolving the active rubric, record dimension ids in the header.

```markdown
# Self-iteration log: <Askill>

| Field | Value |
| --- | --- |
| Skill path | skills/<Askill>/ |
| Rubric | <rubric_id> |
| Rubric dimensions | <comma-separated dimension ids from active rubric> |
| Started | <ISO-8601 date> |
| Purpose excerpt | <one sentence from Askill Purpose> |

---
```

## Round Block (append each round)

Render **Scores** from the active rubric for this session (one row per dimension). Do not use a fixed dimension list.

```markdown
## Round <n>

| Field | Value |
| --- | --- |
| Timestamp | <ISO-8601> |
| Scenario | <quoted scenario> |
| Judge role | <product_manager or creator> |
| Isolated judge | <yes or no> |
| Overall | <fail or pass_excellent> |
| Artifact dir | tune_sessions/<session_id>/round-<NNN> |

### Scores

| Dimension | Score | Excellent threshold |
| --- | --- | --- |
| <dimension_id> | <1-5> | <threshold> |
| ... | ... | ... |

### Findings

- **<dimension> (<score>)**: <gap>
  - Evidence: "<quote from out only>"

For `pass_excellent`, findings may be a single line: all dimensions met excellent threshold.

### Priority fixes

1. <ordered item>

For `pass_excellent`, write: `None - excellence gate passed.`

### Artifacts

- out.md: `<path>` sha256 `<hash>`
- judge_packet.md: `<path>` sha256 `<hash>`
- judge_result.json: `<path>` sha256 `<hash>`
- improve_summary.md: `<path>` sha256 `<hash>` (fail rounds)

### Output (out)

- Summary: <one line>

### Improve

```

**If `overall` is `fail`**, continue:

```markdown
| Field | Value |
| --- | --- |
| Files touched | <comma-separated paths> |
| Hypothesis | <expected dimension lift> |

- <change bullet>

---
```

**If `overall` is `pass_excellent`**:

```markdown
None - excellence gate passed; no Askill edits this round.

---
```

## Session Footer (append once at end)

```markdown
## Session end

| Field | Value |
| --- | --- |
| Status | <excellent, capped, or aborted> |
| Rounds completed | <n> |
| Remaining gaps | <text or none> |
| Next scenario suggestion | <optional> |
```

Do not delete or rewrite prior round blocks.
