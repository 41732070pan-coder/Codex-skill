# Triage Protocol

Triage operates on `HypertextBlock[]`, not on a PDF-only text stream. A block may come from a PDF page range, HTML heading/anchor, Markdown heading, or heading-structured plain text slice.

## Hypertext Block Types

| Block type | Examples | Default treatment |
| --- | --- | --- |
| `heading` | H1/H2/H3, PDF section title, Markdown heading | Structure; may introduce objectives. |
| `paragraph` | Concept explanation, narrative, warning | Classify by learning role. |
| `code` | Fenced code, inline command, PDF code listing | Usually core/supporting when tied to objectives. |
| `table` | API table, precedence chart, glossary table | Appendix unless objective requires mastery. |
| `figure` | Diagram, screenshot, chart | Supporting if it explains a concept; appendix if decorative. |
| `callout` | Tip, warning, note | Supporting or reference-only. |
| `exercise` | Practice, checkpoint, worked problem | Supporting or core when it tests a core skill. |
| `navigation` | TOC, previous/next, breadcrumbs | Source structure; not lecture body. |
| `sidebar` | Ads, comments, related links, repeated panels | Filler unless needed as reference. |
| `appendix` | Long reference sections | Reference-only by default. |
| `reference` | License, bibliography, API links | Preserve as metadata or appendix. |

## Content Roles

| Role | Definition | Lecture treatment |
| --- | --- | --- |
| `core` | Must know to meet section objectives or follow later tutorial material. | Body, full depth per route. |
| `supporting` | Helps understanding but is not itself the central concept. | Body if composite score is high enough; otherwise skim. |
| `reference_only` | Tables, bibliographies, appendices, long examples, API lists, or links for lookup. | Appendix "阅读材料". |
| `filler` | Repetition, navigation, marketing, empty transitions, decorative prose, duplicated headers/footers. | Omit from body; optional one-line skipped summary. |
| `deferred_ops` | Setup, installation, IDE operations, rendering/tooling steps not needed for current concept. | Skip body; provide deep-dive/setup link if important. |

## Depth Score

Score each block or knowledge point from 0–5:

| Field | Meaning |
| --- | --- |
| `importance` | Centrality to current section and later tutorial progress. |
| `complexity` | Explanation/practice needed to avoid misunderstanding. |
| `practical_frequency` | How often the learner will use it in real professional work. |
| `prerequisite_value` | Whether later sections depend on it. |
| `goal_relevance` | Fit with user's stated goal. |
| `personal_relevance` | Fit with user familiarity, time budget, and hints. |

Default composite:

```text
composite = round((importance + complexity + practical_frequency + prerequisite_value + goal_relevance + personal_relevance) / 6, 1)
```

Default `personal_relevance` from learner preference `familiarity`:

| familiarity | default personal_relevance |
| --- | --- |
| novice | 4 |
| rusty | 3 |
| comfortable | 2 |

Adjust with `personal_relevance_hints` by at most ±1 per matching concept, capped to 0–5.

| composite | study_depth | route default |
| --- | --- | --- |
| < 2.0 | skip | `skip_with_deep_dive` if importance or prerequisite value ≥ 3 |
| 2.0–3.4 | skim | `in_lecture`, ≤ 3 minutes |
| 3.5–4.4 | standard | `in_lecture` |
| ≥ 4.5 | deep | `in_lecture`, worked example or practice when applicable |

## Skip With Deep Dive

When `study_depth === skip` and the topic is important but not currently relevant:

- State one sentence explaining why it is skipped now.
- Provide `deep_dive`: official docs, source page/anchor, publisher errata, or user-provided resource.
- Never fabricate a URL.

## Self-Check

- [ ] Every selected heading or block has a source trace.
- [ ] At least one `core` block exists in the requested scope.
- [ ] No `filler` block appears in the lecture body.
- [ ] `reference_only` blocks are not listed as learning objectives.
- [ ] Important skipped content has a non-fabricated deep-dive target or a source-location note.
