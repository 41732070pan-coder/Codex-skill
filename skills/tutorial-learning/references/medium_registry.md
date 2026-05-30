# Medium Registry

Human-readable mirror of `registry/mediums.yaml`. Source of truth for scripts is YAML.

| id | status | summary | implementation | aliases / cues |
| --- | --- | --- | --- | --- |
| `pdf-chaptered` | stable | Chaptered PDF textbook; triage + Chinese lecture per section | `implementations/pdf-chaptered/SKILL.impl.md` | pdf, textbook, chapter, section, 分章 |
| `video-chaptered` | draft | Planned: video course with chapter markers | — | video, 课程视频 |
| `web-docs` | draft | Planned: multi-page official docs | — | docs, documentation |

Resolution: `python scripts/resolve_medium.py resolve <id|cue>`

Fallback: if cue matches only `pdf`, resolve `pdf-chaptered`.
