# Tutorial Modes

Choose the instructional-design mode before generating the bundle. Do not claim to produce a deep tutorial when the available source evidence only supports orientation.

| Mode | Use when | Required design emphasis |
| --- | --- | --- |
| `route_overview` | The source scope is book-sized, the learner needs prioritization, or evidence is mostly outline-level. | Learner profile, route, chapter priorities, prerequisites, review cadence, and explicit deep-dive boundaries. |
| `chapter_tutorial` | The requested chapter or section has enough section-, paragraph-, or code-level evidence for teaching. | Chapter knowledge map and lesson sequence. For a normal chapter, design 3–5 lessons; for a narrow section, design the smallest evidence-backed lesson set and state why fewer lessons are sufficient. |

## Mode Selection Rules

- Ask or infer the mode from scope, evidence, learner goal, and time budget. Record the choice in `learning_plan.md` and `tutorial_structure.md`.
- Use `route_overview` when only titles, TOC entries, or navigation labels are available. Do not fabricate chapter explanations, code, worked examples, or mastery checks from headings alone.
- Use `chapter_tutorial` only when the source includes enough teaching material to support lesson-level claims.
- Do not pad a narrow section to reach three lessons. The 3–5 lesson rule applies to normal chapters, not tiny fixtures or short source sections.
- A downstream renderer may turn either mode into a webpage, slide deck, H5 flow, or document. Rendering remains out of scope here.
