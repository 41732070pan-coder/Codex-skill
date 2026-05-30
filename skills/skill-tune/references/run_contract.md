# Run Contract

Rules for the **Run** step: execute `scenario` with Askill only and capture **out** for judging.

## Run Context Boundary

| Allowed during Run | Forbidden during Run |
| --- | --- |
| Askill `SKILL.md` and references per Askill load policy | `skill-tune` judge/improve instructions |
| Tools needed to produce the scenario deliverable | Prior round `self-iter.md` or judge conclusions |
| User-provided inputs required by the scenario | Editing Askill files (Improve happens later) |

Load `skill-tune` references for orchestration; load **only Askill** content to execute the scenario.

## Askill-Only Execution

1. Resolve `skills/<Askill>/` and read Askill entry + references Askill itself would load for this scenario.
2. Do not paste judge `priorityFixes`, improve diffs, or "expected answer" hints into the Run prompt.
3. On rerun after Improve, use the **same** `scenario` text; verify behavior changed via skill instructions alone.

## Artifact Capture (`out`)

| Rule | Detail |
| --- | --- |
| Final state only | Capture what a user receives when the task is done, not intermediate drafts unless the scenario asks for them. |
| Forms | Written files (paths), pasted markdown in chat, or a structured bundle listing paths + short excerpts. |
| Large files | Store path + SHA or size; include excerpts for sections the judge must score; note truncation. |
| Multi-file | List every path in `out` manifest; judge packet includes excerpts per file. |
| Inline vs path | Prefer paths for reproducibility; inline only when nothing was written to disk. |

Suggested `out` manifest shape:

```yaml
scenario: <echo scenario>
paths:
  - path: skills/<Askill>/...
    excerpt: <optional>
inline: <optional markdown when no files>
```

## Tool Use

| Case | Guidance |
| --- | --- |
| Scenario requires tools | Use tools Askill workflow implies; do not use tools solely to read forbidden judge context. |
| Scenario is doc-only | Do not run shell/network tools unless Askill requires them. |
| Sensitive data | Redact secrets from `out` excerpts; note redaction in manifest. |

## Handoff to Judge

Stop Run when `out` is stable. Pass to judge only:

- scenario one-liner
- `expectedArtifactType` (scenario-derived, optional)
- active rubric table
- `out` manifest / body

Do not pass Run chat, tool logs, or Askill file paths except as part of `out`.

## Run Checklist

- [ ] Askill-only context for execution
- [ ] Same scenario text on reruns
- [ ] `out` manifest lists paths and excerpts
- [ ] No judge/improve leakage in Run prompt
- [ ] Secrets redacted when applicable
