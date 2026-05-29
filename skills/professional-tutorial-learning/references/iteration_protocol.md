# Iteration Protocol

Use this protocol when improving this skill through repeated trial generation and evaluation.

## Round Structure

Each round must record four steps:

1. Abstract model update: what changed in tutorial concepts, schemas, learning strategy, or evaluation criteria.
2. Concrete workflow update: what changed in a source workflow, registry, lesson template, validator, or examples.
3. Trial generation: source used, selected unit, generated first lesson, and known limitations.
4. Evaluation and revision: evaluator feedback, accepted changes, rejected changes, and next risk.

## Evaluation Rubric

Score each dimension from 1 to 5:

| Dimension | Question |
| --- | --- |
| Source fidelity | Does the lesson preserve the source's actual intent and structure? |
| Knowledge extraction | Are core concepts separated from examples and context? |
| Skip/read accuracy | Are reading-only and low-value materials identified without hiding important content? |
| Depth calibration | Does study depth match importance, frequency, complexity, and learner goal? |
| Practice quality | Does practice test usable skill rather than recall only? |
| Review usefulness | Are review prompts spaced and action-oriented? |
| Markdown clarity | Is the lesson easy to study as a standalone artifact? |
| Web readiness | Are ids and sections stable enough for future app rendering? |
| Safety and uncertainty | Are inferred boundaries, weak evidence, and link gaps visible? |

## Ten-Round Execution Log

| Round | Step 1 abstract model update | Step 2 concrete workflow update | Step 3 trial generation | Step 4 evaluation and revision |
| --- | --- | --- | --- | --- |
| 1 | Established media, structure, content-class, lesson, and review entities. | Added PDF-first workflow and markdown lesson template. | Selected `Learn Programming` as a public tutorial source and generated lesson 1 on orientation. | Added explicit reading-only vs core concept separation after self-review. |
| 2 | Added learning-depth axes for importance, frequency, complexity, prerequisite value, and goal relevance. | Updated PDF workflow to score knowledge points before writing explanations. | Rechecked first lesson to keep motivation concise. | Accepted stronger depth labels in the knowledge map. |
| 3 | Added web-app-compatible lesson fields. | Updated lesson template with stable metadata and JSON-compatible conceptual shape. | Mapped first lesson sections to stable ids. | Accepted requirement that markdown headings remain parseable. |
| 4 | Added skip policy for complex low-frequency material. | Added PDF heuristics for appendices, screenshots, and repeated installation steps. | Marked early philosophical material as reading-only rather than core. | Accepted visible skip/compress notes to preserve trust. |
| 5 | Added source confidence and boundary confidence. | Updated workflows to mark inferred boundaries and extraction gaps. | Marked the example's first lesson boundary as inferred from the online table of contents. | Accepted uncertainty notes in source metadata. |
| 6 | Added practice policy by knowledge profile. | Updated template with practice task and expected result. | Added an orientation practice task that asks the learner to classify study goals. | Accepted more observable mastery criteria. |
| 7 | Added review policy with same-day, next-day, and one-week prompts. | Updated template review schedule table. | Added spaced prompts to the example. | Accepted review prompts that require recall and transfer. |
| 8 | Added registry dispatch for PDF, web, video, and mixed-media modes. | Added source workflow registry and mode-specific references. | Treated `Learn Programming` as PDF-capable but used the web index for safe metadata. | Accepted source workflow recommendation language. |
| 9 | Added iteration rubric for evaluator feedback. | Added this protocol as a required skill-improvement reference. | Evaluated example lesson against rubric. | Accepted evaluator-oriented scoring dimensions. |
| 10 | Added deterministic validation expectations. | Added `validate_tutorial_skill.py` to check registry, template, example, and iteration log. | Ran local validation plan after implementation. | Accepted validator-backed quality gates for future edits. |

## Recording Rules

- Keep one row per round and four concrete step notes per row.
- Include the trial source and selected lesson artifact path when available.
- Incorporate evaluator feedback into the next round unless explicitly rejected with a reason.
- Prefer small skill changes per round over large undocumented rewrites.

## Round Detail Evidence

| Round | Trial artifact | Rubric snapshot | Accepted revision | Rejected revision | Next risk |
| --- | --- | --- | --- | --- | --- |
| 1 | `examples/first_lesson.md` | Source fidelity 3; extraction 3; clarity 4 | Added explicit content classes and source metadata. | Rejected full-course summary because the first iteration needed a small lesson. | Overgeneralizing from headings. |
| 2 | `examples/first_lesson.md` | Depth 4; practice 3; review 3 | Added depth axes and normal/deep/skim decisions. | Rejected equal depth for every paragraph. | Weak scoring consistency. |
| 3 | `references/lesson_artifact_template.md` | Web readiness 3; markdown clarity 4 | Added JSON-compatible output fields. | Rejected frontend implementation in this phase. | Human-readable output may still lack IDs. |
| 4 | `references/pdf_chapter_workflow.md` | Skip/read accuracy 4; source fidelity 3 | Added visible skip/compress material. | Rejected hiding skipped material from the learner. | Skipping important prerequisites. |
| 5 | `references/tutorial_model_contract.md` | Uncertainty 4; structure 4 | Added boundary and extraction confidence. | Rejected pretending inferred sections are explicit. | Low-confidence PDFs. |
| 6 | `examples/first_lesson.md` | Practice 4; mastery 3 | Added an observable study-contract practice. | Rejected recall-only practice. | Practice may be too generic. |
| 7 | `references/learning_strategy_contract.md` | Review 4; transfer 3 | Added spaced review prompts. | Rejected one-time summary-only review. | Review prompt fatigue. |
| 8 | `references/source_workflow_registry.md` | Dispatch 4; ambiguity 4 | Added registered source workflows. | Rejected silent fallback to PDF for all sources. | Mixed-media handling remains planned. |
| 9 | `references/iteration_protocol.md` | Evaluation 4; traceability 3 | Added evaluator rubric and round logs. | Rejected undocumented optimization claims. | Evidence can still be compressed. |
| 10 | `scripts/validate_tutorial_skill.py` | Validation 4; maintainability 4 | Added deterministic validator and quality gates. | Rejected manual-only quality checking. | Validator may miss semantic drift. |
