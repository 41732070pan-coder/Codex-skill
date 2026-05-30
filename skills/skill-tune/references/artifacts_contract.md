# Artifacts Contract

Reproducible per-round files under the target skill. The append-only log indexes these; it does not duplicate full content.

## Layout

```text
skills/<Askill>/tune_sessions/<session_id>/round-<NNN>/
  manifest.json
  scenario.txt
  out.md
  active_rubric.json
  judge_packet.md
  judge_result.json
  improve_summary.md      # fail rounds only
  improve_record.json     # structured improve (required before complete-round on fail)
  improve.patch           # optional
  session_state.json      # under tune_sessions/<session_id>/
```

## manifest.json

```json
{
  "scenario": "...",
  "createdAt": "ISO-8601",
  "artifacts": {
    "out.md": { "path": "...", "sha256": "..." },
    "judge_result.json": { "path": "...", "sha256": "..." }
  }
}
```

## Tool Commands

| Step | Command |
| --- | --- |
| Create round dir + out | `tune_session.py init-round-dir ...` |
| Judge packet | `tune_session.py build-judge-packet ...` |
| Store judge outputs | `tune_session.py record-judge-artifacts ...` |
| Store improve | `tune_session.py record-improve ...` |
| Append log | `tune_session.py append-log ...` (reads `improve_record.json` from round dir) |
| Close round | `tune_session.py complete-round ...` |
| Session end | auto via `complete-round`, or `append-session-end` |

## Log Index

`self-iter.md` round blocks include **Artifacts** bullets with path + sha256 from `manifest.json`, plus `Artifact dir` for the round folder.

## Retention

Do not delete prior round directories when appending new rounds. Agents may compress old sessions only when the user requests cleanup.
