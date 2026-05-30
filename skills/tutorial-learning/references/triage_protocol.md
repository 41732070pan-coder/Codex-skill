# Triage Protocol

## Content roles

| Role | Definition | Lecture treatment |
| --- | --- | --- |
| `core` | Must know to meet section objectives | Body, full depth per route |
| `supporting` | Helps understanding; not always exam-critical | Body if composite ≥ 3.5; else skim paragraph |
| `reference_only` | Tables, bibliography, long examples for lookup | Appendix "阅读材料" |
| `filler` | Preface fluff, repeated marketing, empty transitions | Omit; one-line in `skipped_summary` |
| `deferred_ops` | Install, IDE setup, environment (not conceptual) | Skip body; `skip_with_deep_dive` with setup link |

## Depth score

Compute per block:

```
composite = round((importance + complexity + personal_relevance) / 3, 1)
```

Default `personal_relevance` from overlay `familiarity`:

| familiarity | default personal_relevance |
| --- | --- |
| novice | 4 |
| rusty | 3 |
| comfortable | 2 |

Adjust with `personal_relevance_hints` (+1 max per hint, cap 5).

| composite | study_depth | route default |
| --- | --- | --- |
| < 2.0 | skip | skip_with_deep_dive if importance ≥ 3 |
| 2.0–3.4 | skim | in_lecture, ≤ 3 min |
| 3.5–4.4 | standard | in_lecture |
| ≥ 4.5 | deep | in_lecture, worked example if applicable |

## Skip with deep dive

When `study_depth === skip` and the topic is important but low personal use:

- One sentence why skipped.
- `deep_dive`: label + URL (official docs, original PDF page anchor, or "原书 §x").

## Chapter opener heuristic

The first block of a chapter (before the first numbered section) is often motivational
prose. Default to `supporting` + `skim` unless it introduces new technical terms.
If it only repeats the book preface themes, mark `filler`.

## Red flags for filler

- Author biography, "how to use this book", duplicate chapter summaries.
- Sidebars that repeat the previous paragraph.
- Exercise solutions without learning new concepts (mark `reference_only`).

## Wide tables and notation-heavy blocks

Tables wider than 4 columns, full operator precedence charts, or language comparison matrices:
default `reference_only` unless the section objective explicitly requires memorization.

## Self-check (triage)

- [ ] Every outline heading has a role.
- [ ] At least one `core` block in scope.
- [ ] No `filler` in lecture body.
- [ ] `reference_only` not listed as learning objectives.
