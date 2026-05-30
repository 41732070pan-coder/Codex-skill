# Improve Contract

Changes to Askill after a failed excellence gate. Improve maps judge gaps to concrete instruction edits.

## Allowed Changes

| Target | Examples |
| --- | --- |
| `skills/<Askill>/SKILL.md` | Workflow steps, triggers clarity, checklists, failure modes, output contract |
| `skills/<Askill>/references/` | Load map, templates, examples, domain references used during runs |
| `skills/<Askill>/references/tune_rubric.md` | Tune-specific rubric when gaps are skill-specific |

## Forbidden Without meta-skill

| Action | Route to |
| --- | --- |
| Rename or split skill directory | `meta-skill` |
| Change front matter `name` vs directory | `meta-skill` |
| Edit `meta-skill/references/skill_registry.md` or root README inventory | `meta-skill` |
| Add implementation-family scripts or registry layout | `meta-skill` |
| Change asset manifests or provenance | `meta-skill` |

Note forbidden structural needs in `self-iter.md`; do not perform them inside `skill-tune`.

## Improve Rules

1. **One primary failure mode per round** when possible — address the lowest-scoring dimension or top `priorityFixes` item first.
2. **Minimal diff** — prefer adding a checklist, explicit step, or failure mode over rewriting entire sections.
3. **Traceability** — each change links to a `findings` entry (dimension + gap).
4. **Hypothesis** — log what dimension should improve on the next run.
5. **No judge leakage into run** — do not paste judge conclusions into the next scenario prompt; let the updated skill speak through behavior.
6. **Generalize, do not overfit** — every edit must generalize the judge finding into a reusable rule (checklist, step, failure mode, output contract). Never hard-code a specific scenario answer, example string, or user wording from the tune session into Askill.
7. **Record improve artifacts** — write `improve_summary.md` (and optional `improve.patch`) under the round directory via `tune_session.py record-improve`; log indexes sha256 only.

## Mapping Gaps to Edits

| Dimension gap | Typical instruction fix |
| --- | --- |
| `taskFit` | Clarify scenario handling, scope boundaries, or first-step normalization |
| `clarity` | Add output structure template, headings contract, or "write for cold reader" rule |
| `completeness` | Add required sections checklist or deliverables table |
| `correctness` | Add verification step, forbidden claims, or "cite only from sources" rule |
| `artifactAlignment` | Add output-type contract, scenario scope bounds, or deliverable checklist derived from common scenario shapes |

Avoid generic prose ("be better", "improve quality") without an executable rule.

## After Improve

Append the round to `skills/<Askill>/self-iter.md` before starting the next run round.
