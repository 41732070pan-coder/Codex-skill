# skill_intro_deck — workflow map

This fixture demonstrates **one** pass through `SKILL.md` Workflow. Slide copy favors **Intent**, **Creative Latitude**, and **Self-Check** language from `references/*_style.md`. Safety boundaries appear as checklist questions, not as extra imperative bans for the agent.

| Workflow step | Where it appears in the example |
| --- | --- |
| 1. Normalize `DesignRequest` | `request.json`; slides on inputs and modifiers |
| 2. Resolve style | Registry table; style decision slide |
| 3. Load references progressively | Agenda + “references to load” cards |
| 4. Pipeline: modifiers → `ComposedStylePlan` → `StyleLock` → `VisualRhythmPlan` → compose → self-check | Flow slide, StyleLock slide, rhythm cards, closing checklist |
| 5. Asset boundary | AssetPolicy cards; `build_deck.py` rasterizes SVG motifs from `assets/chinese_traditional_color_style/` (see `content_outline.json` → `motifs` per slide) |
| 6. Deliver with note | Footer on each slide; regenerate via `build_deck.py` |

## StyleLock for this run

`previewMode: skip` → defaults from `chinese_traditional_color_style` (Indigo Scholarly + Ink Paper, low rice-paper texture, restrained motif level). See StyleLock slide in generated deck.

## What this example is not

- Not a substitute for `references/chinese_traditional_color_style.md` or other style files.
- Not a list of “never do X” commands; use each style’s **Self-Check** at delivery time.
- Not required reading for unrelated one-off design tasks.
