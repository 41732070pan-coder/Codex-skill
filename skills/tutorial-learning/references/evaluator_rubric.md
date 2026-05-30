# Evaluator Rubric

Score the tutorial-design bundle before delivery. Each dimension is scored from 0 to 5.

| Dimension | Check |
| --- | --- |
| `source_fidelity` | Claims, code, terminology, and boundaries remain traceable to the source; inferred and supplementary material are labeled. |
| `source_evidence_depth` | The selected mode and teaching depth are supported by outline-, section-, paragraph-, or code-level traces; outline-only input is not disguised as a complete tutorial. |
| `triage_depth_routing` | Core, supporting, reference-only, filler, and deferred operational material are routed consistently with depth guardrails. |
| `chinese_lecture_quality` | The lecture is understandable, complete enough to study independently, and written as teaching content rather than a design specification. |
| `lesson_learning_value` | Chapter-tutorial lessons contain source-specific explanations, worked reasoning or demonstrations, practice, and feedback guidance rather than repeated generic scaffolds. |
| `assessment_diagnostics` | Assessments diagnose specific capabilities using suitable prediction, concept, calculation, code-reading, diagnosis, or transfer prompts and include wrong-answer feedback guidance. |
| `personalization` | Learner profile inputs cause visible route or lesson consequences; defaults are explicit when inputs are absent. |
| `tutorial_design_completeness` | The Markdown bundle defines a coherent, medium-neutral course design that a downstream renderer can consume without inventing missing instructional structure. |

## Blocking Failures

Block delivery when source fidelity is materially broken, required tutorial-design documents are missing, core concepts are omitted, outline-only evidence is presented as a deep chapter tutorial, adjacent lessons repeat generic filler, applicable practical work is missing, assessments do not diagnose objective-level capabilities, learner-profile consequences are absent, filler leaks into the lecture core, or the bundle prescribes a final presentation artifact instead of remaining medium-neutral.
