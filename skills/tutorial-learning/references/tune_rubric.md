# Tutorial-Learning Tune Rubric

Per-skill rubric for skill-tune sessions. Judges evaluate `out` only; do not read Askill `SKILL.md`.

## Rubric meta

```markdown
rubric_id: tutorial_learning_tune_rubric
excellence_gate: all_dimensions
```

## Dimensions

| ID | What to score | Threshold | 3 (acceptable) | 5 (excellent) |
| --- | --- | --- | --- | --- |
| `taskFit` | Fit to the stated scenario and scope | 5 | Addresses main intent with minor gaps | Fully addresses source format, scope, and downstream handoff intent |
| `clarity` | Structure and readability of the bundle | 5 | Understandable with some re-reading | Cold reader can follow all eight Markdown outputs without production context |
| `completeness` | Required tutorial-design deliverables | 5 | Most required files and sections present | All eight Markdown outputs present with cross-linked objectives, triage, and assessments |
| `sourceTraceability` | Fidelity visible in `out` alone | 5 | Major claims traceable; minor labeling gaps | Every non-literal lecture claim tagged or listed; fidelity doc matches lecture; no false labeling claims |
| `pedagogyAlignment` | Teaching design quality | 5 | Lecture teachable with minor gaps | Attempt-first assessments, triage routing, review cards, and lesson structure align with objectives |

## Notes for judges

- `expectedArtifactType`: medium-neutral Chinese course-design Markdown bundle (learning plan, lecture, structure, triage, assessment, practice, review, source fidelity).
- Score `sourceTraceability` down when `source_fidelity.md` claims labeling that `lecture.md` does not show.
- For multi-variant HTML (e.g. textbook pages with MXNet/PyTorch/TensorFlow/Paddle tabs), score `completeness` down when `triage.md` omits non-selected variants as `deferred_ops`, and `pedagogyAlignment` down when the lecture duplicates all variants.
- For minimal sources (≤3 concept sentences), score `pedagogyAlignment` down when inferred expansion exceeds what the source supports without explicit `[推断]` or **推断展开** documentation.
