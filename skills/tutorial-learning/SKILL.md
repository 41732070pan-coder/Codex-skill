---
name: tutorial-learning
description: Hypertext tutorial learning for PDF, HTML, Markdown, and heading-structured tutorial sources. Produces Chinese lecture notes, content triage, micro-assessments, spaced review cards, and lightweight H5/hypertext projections.
---

# Tutorial Learning

## Purpose

Turn hypertext tutorial sources into time-efficient Chinese study artifacts. Treat PDF, HTML, Markdown, and heading-structured text as carriers of the same hypertext model: ordered sections, source traces, links, headings, blocks, concepts, assessments, and review cards.

The skill keeps one active implementation: `hypertext-tutorial`. PDF is a supported source format inside that implementation, not a separate implementation family.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Learn from a PDF textbook, HTML tutorial, Markdown guide, documentation page, web tutorial, or other heading-structured tutorial source. |
| Trigger | Generate or refine Chinese lecture notes, content triage, micro-assessments, practice tasks, spaced review cards, or H5/hypertext projections from a tutorial section. |
| Trigger | Classify tutorial blocks as core, supporting, reference-only, filler, or deferred operational detail. |
| Non-trigger | Non-hypertext sources or course bundles that cannot be represented as sections, headings, anchors, links, or page ranges. |
| Non-trigger | Raw PDF extraction, rendering, installation, or layout QA — use a PDF/tooling skill when available. |
| Non-trigger | OS/kernel/C-only lessons with linked kernel code and H5 labs — use the specialized OS/kernel learning skills when available. |
| Non-trigger | Add/rename/govern repository skills — use `meta-skill`. |
| Ask if ambiguous | Source is inaccessible, source rights are unclear, source is not a tutorial, requested scope is missing, or the source lacks enough text to support the requested lesson. |

## Workflow

1. **Normalize** the request into `TutorialRequest` (see `references/learning_contract.md`).
2. **Resolve** the single active implementation with `registry/implementations.yaml` or `python scripts/resolve_implementation.py resolve <id|cue>`.
3. **Identify** the hypertext source format: PDF, HTML, Markdown, or plain text with headings.
4. **Build** a source outline from page ranges, headings, anchors, links, navigation order, and source traces.
5. **Run** the `TutorialLearningBase` pipeline: ingest → triage → route → lecture → assessment → emit → selfCheck.
6. **Deliver** artifacts: Chinese `lecture_md`, `triage.json`, `review_plan.json`, and a lightweight `h5_stub.json` / hypertext projection when useful.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Tutorial source URL/path/text and requested chapter, section, heading, page range, or anchor. |
| Optional inputs | Time budget, familiarity, learning goal, skip preference, personal relevance hints, output artifact types. |
| Normalized shape | `TutorialRequest` in `references/learning_contract.md`. |
| Outputs | Chinese lecture markdown, content triage, learning route, micro-assessment, practice task, review cards, review plan JSON, optional H5/hypertext projection stub. |
| Failure modes | Stop or ask when source text is unavailable, license/use constraints are unclear, the requested unit cannot be located, or only headings/TOC exist without lesson content. |

## References

Load progressively; do not read every reference by default.

| Reference | Load when |
| --- | --- |
| `references/learning_contract.md` | Any run; defines shared hypertext tutorial model and pipeline. |
| `references/implementation_registry.md` | Listing or resolving the active implementation. |
| `references/source_fidelity.md` | Source trace, page/anchor/heading evidence, uncertainty, rights, or extraction confidence matters. |
| `references/triage_protocol.md` | Classifying hypertext blocks, filler, reference-only material, skip policy, or depth routing. |
| `references/lecture_template.md` | Generating or reviewing Chinese lecture markdown. |
| `references/review_protocol.md` | Producing review cards and spaced schedules. |
| `references/h5_lesson_schema.md` | Emitting lightweight H5/hypertext projection stubs or optional review-app contracts. |
| `references/evaluator_rubric.md` | Auditing output quality or skill maintainability. |

## Resources

| Resource | Role |
| --- | --- |
| `registry/implementations.yaml` | Machine-readable implementation registry; contains the single active implementation. |
| `implementations/hypertext-tutorial/SKILL.impl.md` | Concrete hypertext tutorial implementation, including PDF/HTML/Markdown source profiles. |
| `scripts/resolve_implementation.py` | List and resolve implementation aliases/cues. |
| `scripts/validate_tutorial_learning.py` | Static conformance check for this skill. |

Delegate raw PDF rendering, OCR setup, and low-level extraction tooling to appropriate document/PDF tools when available. This skill owns learning structure, triage, source fidelity, and artifact generation.

## Implementation Families

| Family | Registry | List | Resolve | Validate |
| --- | --- | --- | --- | --- |
| `implementations` | `registry/implementations.yaml` | `python scripts/resolve_implementation.py list` | `python scripts/resolve_implementation.py resolve <id|cue>` | `python scripts/validate_tutorial_learning.py` |

Normal-use rule: resolve to `hypertext-tutorial`.

## Overlay / Decorator Support

Optional learner overlay on `TutorialRequest.overlays`:

- `time_budget_minutes` — cap total estimated study time in the lecture.
- `familiarity` — adjusts default personal relevance and prerequisite explanation level.
- `goal` — biases importance toward exam, practice, project, or survey outcomes.
- `personal_relevance_hints` — raises or lowers specific concepts within bounded limits.

Overlays must not weaken source fidelity, allow filler into the lecture body, or convert reference-only material into learning objectives without an explicit learner goal.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| New hypertext source profile | Add profile rules inside the active implementation | `implementations/hypertext-tutorial/SKILL.impl.md` |
| Source fidelity rules | Contract | `references/source_fidelity.md` |
| Triage rules | Contract | `references/triage_protocol.md` |
| Lecture shape | Template | `references/lecture_template.md` |
| Review schedule | Protocol | `references/review_protocol.md` |
| H5/hypertext projection | Schema | `references/h5_lesson_schema.md` |


## Quality Gate

Before finishing:

- Only `hypertext-tutorial` is resolved as the active implementation.
- PDF, HTML, Markdown, and heading-structured text are treated as source formats, not separate implementations.
- Source traces identify page ranges, heading paths, anchors, URLs, or extraction slices when available.
- Boundary and extraction uncertainty are explicit when inferred or weak.
- Lecture output is Chinese; identifiers, commands, API names, formulas, and URLs keep source spelling.
- Triage table is present; filler is omitted from the body; reference-only content goes to the appendix.
- Learning objectives are 2–4 and verifiable; micro-assessment checks prediction, teach-back, and application when applicable.
- Review cards map to learning objectives and use spaced due offsets.
- Run `python skills/tutorial-learning/scripts/validate_tutorial_learning.py`.
