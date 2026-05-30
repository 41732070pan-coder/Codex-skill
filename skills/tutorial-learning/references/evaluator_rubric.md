# Evaluator Rubric

Score the tutorial-design bundle before delivery. Each dimension is scored from 0 to 5.

| Dimension | Check |
| --- | --- |
| `source_fidelity` | Claims, code, terminology, and boundaries remain traceable to the source; inferred and supplementary material are labeled. |
| `triage_depth_routing` | Core, supporting, reference-only, filler, and deferred operational material are routed consistently with depth guardrails. |
| `chinese_lecture_quality` | The lecture is understandable, complete enough to study independently, and written as teaching content rather than a design specification. |
| `assessment_review` | Objectives, attempt-first checks, practice tasks, review cards, and spaced-review guidance align. |
| `tutorial_design_completeness` | The Markdown bundle defines a coherent, medium-neutral course design that a downstream renderer can consume without inventing missing instructional structure. |

## Blocking Failures

Block delivery when source fidelity is materially broken, required tutorial-design documents are missing, core concepts are omitted, filler leaks into the lecture core, assessments do not cover objectives, or the bundle prescribes a final presentation artifact instead of remaining medium-neutral.
