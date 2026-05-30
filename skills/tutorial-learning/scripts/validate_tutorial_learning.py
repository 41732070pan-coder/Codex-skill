#!/usr/bin/env python3
"""Validate tutorial-learning skill structure (dependency-free)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REQUIRED_REFS = [
    "learning_contract.md",
    "medium_registry.md",
    "triage_protocol.md",
    "lecture_template.md",
    "review_protocol.md",
    "h5_lesson_schema.md",
    "evaluator_rubric.md",
]
REQUIRED_SECTIONS = [
    "purpose",
    "triggers",
    "workflow",
    "inputs",
    "references",
    "resources",
    "quality",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_titles(md: str) -> set[str]:
    return {m.group(1).lower() for m in re.finditer(r"^##\s+(.+?)\s*$", md, re.M)}


def main() -> int:
    errors: list[str] = []
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.exists():
        errors.append("missing SKILL.md")
    else:
        titles = section_titles(read(skill_md))
        for needle in REQUIRED_SECTIONS:
            if not any(needle in t for t in titles):
                errors.append(f"SKILL.md missing section matching {needle!r}")
    for name in REQUIRED_REFS:
        if not (SKILL_DIR / "references" / name).exists():
            errors.append(f"missing references/{name}")
    impl = SKILL_DIR / "implementations" / "pdf-chaptered" / "SKILL.impl.md"
    if not impl.exists():
        errors.append("missing implementations/pdf-chaptered/SKILL.impl.md")
    reg = SKILL_DIR / "registry" / "mediums.yaml"
    if not reg.exists():
        errors.append("missing registry/mediums.yaml")
    else:
        text = read(reg)
        if "pdf-chaptered" not in text:
            errors.append("registry missing pdf-chaptered")
    if not (SKILL_DIR / "scripts" / "resolve_medium.py").exists():
        errors.append("missing scripts/resolve_medium.py")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("OK: tutorial-learning structure valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
