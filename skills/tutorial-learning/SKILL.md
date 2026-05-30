---
name: tutorial-learning
description: Medium-agnostic professional tutorial learning with triaged depth, Chinese lecture notes, and spaced review. Use for PDF chapter study, skipping filler, lecture generation, tutorial triage, spaced repetition, and professional tutorial study. Resolves pdf-chaptered first; video and web-docs are planned. Not for OS-kernel-only tutoring (c-os-learning-tutor) or raw PDF tooling (pdf).
---

# Tutorial Learning

## Purpose

Turn professional tutorials into time-efficient Chinese study artifacts: triaged content roles, depth-scored study routes, section lectures, micro-assessments, and spaced review plans. `SKILL.md` orchestrates; contracts and the `pdf-chaptered` implementation family hold domain rules.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | PDF textbook, chapter study, skip filler, lecture notes, tutorial triage, spaced repetition, professional tutorial, depth scoring, review cards. |
| Trigger | Generate or refine Chinese markdown lectures from a chaptered tutorial. |
| Non-trigger | OS/kernel/C-only lessons with linked kernel code and H5 labs — use `c-os-learning-tutor` and `kernel-note-code-linker`. |
| Non-trigger | PDF install, render-only checks, or layout QA — use `pdf`. |
| Non-trigger | Add/rename/govern repository skills — use `meta-skill`. |
| Ask if ambiguous | Medium unclear, no chapter/section scope, or tutorial license unknown. |

## Workflow

1. **Normalize** the request into `TutorialRequest` (see `references/learning_contract.md`).
2. **Resolve medium** via `registry/mediums.yaml` or `python scripts/resolve_medium.py resolve <id|cue>`.
3. **Load** only the resolved implementation (`implementations/<id>/SKILL.impl.md`) plus references required by that implementation.
4. **Run** the `TutorialLearningBase` pipeline: ingest → triage → route → lecture → assessment → emit → selfCheck.
5. **Deliver** artifacts; attach `h5_lesson_id` stub when Phase 2 is requested (schema only in this repo phase).

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source (URL or path), medium or enough cues to resolve one, target chapter/section (e.g. section 1). |
| Optional inputs | `time_budget_minutes`, familiarity, learning goals, skip policy, personal relevance hints. |
| Normalized shape | `TutorialRequest` in `references/learning_contract.md`. |
| Outputs | Chinese `lecture_md`, `triage.json`, `review_plan.json`, optional `h5_stub.json`. |
| Failure modes | Stop if license unclear, source unreadable, or medium unresolved after one clarify pass. |

## References

Load progressively; do not read every reference by default.

| Reference | Load when |
| --- | --- |
| `references/learning_contract.md` | Any run; defines `TutorialLearningBase` and data shapes. |
| `references/medium_registry.md` | Listing or resolving implementations. |
| `references/triage_protocol.md` | Triage, skip, filler, reference-only content. |
| `references/lecture_template.md` | Generating or reviewing lectures. |
| `references/review_protocol.md` | Review cards and spaced schedule. |
| `references/h5_lesson_schema.md` | Phase 2 H5 stub or export. |
| `references/evaluator_rubric.md` | Lab evaluation or skill audit. |

## Resources

| Resource | Role |
| --- | --- |
| `registry/mediums.yaml` | Machine-readable medium family registry. |
| `implementations/pdf-chaptered/SKILL.impl.md` | PDF chaptered concrete implementation. |
| `scripts/resolve_medium.py` | List / resolve medium implementations. |
| `scripts/validate_tutorial_learning.py` | Static skill conformance check. |
| `lab/` | 40-step iteration log, lectures, evaluations (see `lab/README.md`). |

Delegate PDF extraction and rendering to the `pdf` skill. Do not duplicate Poppler or pdfplumber setup here.

## Implementation Families

| Family | Registry | List | Resolve | Validate |
| --- | --- | --- | --- | --- |
| `mediums` | `registry/mediums.yaml` | `python scripts/resolve_medium.py list` | `python scripts/resolve_medium.py resolve <id>` | `python scripts/validate_tutorial_learning.py` |

Normal-use rule: resolve through registry/scripts; load only the selected `implementations/<id>/` file.

## Overlay / Decorator Support

Optional learner overlay on `TutorialRequest.overlays`:

- `time_budget_minutes` — cap total `est_minutes` in the lecture.
- `familiarity` — adjusts `personal_relevance` default.
- `goal` — biases importance toward exam vs practice vs survey.

Overlays must not break triage invariants in `learning_contract.md`.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| New medium | Strategy + Registry | `registry/mediums.yaml`, `implementations/<id>/` |
| Triage rules | Contract | `references/triage_protocol.md` |
| Lecture shape | Template | `references/lecture_template.md` |
| Review schedule | Protocol | `references/review_protocol.md` |
| H5 export | Schema stub | `references/h5_lesson_schema.md` |

## Quality Gate

Before finishing:

- Trigger boundaries do not overlap `c-os-learning-tutor` or `pdf`.
- Lecture is Chinese; identifiers/commands stay in original spelling.
- Triage table present; filler skipped in body; reference-only in appendix.
- 2–4 testable learning objectives; micro-assessment checks understanding.
- Run `python skills/tutorial-learning/scripts/validate_tutorial_learning.py`.
- Run meta-skill validators when changing repository structure.
