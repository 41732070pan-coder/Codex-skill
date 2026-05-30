#!/usr/bin/env python3
"""Return one selected implementation body."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "tutorial-implementations.json"


def load_entry(implementation_id: str) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for entry in registry["implementations"]:
        if entry["id"] == implementation_id:
            return entry
    raise SystemExit(f"Unknown implementation id: {implementation_id}")


def extract_section(text: str, section: str) -> str:
    wanted = section.strip().lower()
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip().lower() == wanted:
            start = index
            break
    if start is None:
        raise SystemExit(f"Section not found: {section}")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end]).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("implementation_id")
    parser.add_argument("--section", default="", help="Optional level-2 heading to return.")
    args = parser.parse_args()

    entry = load_entry(args.implementation_id)
    path = ROOT / entry["implementationPath"]
    text = path.read_text(encoding="utf-8")
    print(extract_section(text, args.section) if args.section else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
