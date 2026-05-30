# Examples

Optional fixtures for `my-design-style`. They illustrate the same **Workflow** in `SKILL.md`; they do not add rules beyond `references/` and concrete style files.

## When to load

| Situation | Load |
| --- | --- |
| First PPT delivery with this skill, or unsure how `DesignRequest` maps to slides | `skill_intro_deck/request.json` and `skill_intro_deck/NOTES.md` |
| Need a runnable reference implementation (python-pptx) | `skill_intro_deck/build_deck.py` after reading the request fixture |
| Maintaining or extending the example | `skill_intro_deck/content_outline.json` (slide copy only; no extra prohibitions) |

Do **not** load examples on every trigger. Resolve the user task through the normal workflow first.

## Layout

```text
examples/
├── README.md
└── skill_intro_deck/
    ├── request.json           # DesignRequest fixture
    ├── NOTES.md               # Maps fixture → workflow steps
    ├── content_outline.json   # Slide titles and body copy
    ├── build_deck.py          # Regenerates sample PPTX (optional)
    └── generated/             # Raster cache + textures (gitignored; not hand-edited)
```

## Regenerate sample deck

From the repository root (requires `python-pptx`, `Pillow`, `svglib`, and `reportlab`):

Slide copy may declare per-slide `motifs` in `content_outline.json`; each `file` must exist under the active style asset root.

SVG motifs are rasterized with a transparent background (corner color knock-out). If you still see white boxes after updating `build_deck.py`, delete `examples/skill_intro_deck/generated/` and regenerate.

Do not keep ad-hoc probe files such as `_probe.png` or `_test.png` in `generated/`; that folder is only for `build_deck.py` output.

```bash
python skills/my-design-style/examples/skill_intro_deck/build_deck.py
```

Output: `examples/skill_intro_deck/my-design-style-intro.pptx`
