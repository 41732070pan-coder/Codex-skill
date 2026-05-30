#!/usr/bin/env python3
"""List and resolve tutorial-learning implementations (dependency-free)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REGISTRY = SKILL_DIR / "registry" / "implementations.yaml"
LIST_FIELDS = {"aliases", "sourceFormats", "domainCues"}


def parse_list(value: str) -> list[str]:
    value = value.strip()
    if not value.startswith("[") or not value.endswith("]"):
        return []
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [item.strip().strip('"\'') for item in inner.split(",")]


def load_registry() -> list[dict]:
    text = REGISTRY.read_text(encoding="utf-8")
    chunks = re.split(r"\n  - id:", text)
    entries: list[dict] = []
    for chunk in chunks[1:]:
        entry: dict = {}
        lines = ("id:" + chunk).splitlines()
        for line in lines:
            match = re.match(r"^\s*(\w+):\s*(.*)$", line)
            if not match:
                continue
            key, value = match.group(1), match.group(2).strip()
            if key in LIST_FIELDS:
                entry[key] = parse_list(value)
            else:
                entry[key] = value.strip('"')
        if entry.get("id"):
            entries.append(entry)
    return entries


def resolve(query: str) -> dict:
    q = query.lower().strip()
    entries = load_registry()
    for entry in entries:
        if entry.get("id", "").lower() == q:
            return {"status": "resolved", "implementationId": entry["id"], "entry": entry}
        for field in LIST_FIELDS:
            for cue in entry.get(field, []) or []:
                if cue.lower() == q:
                    return {"status": "resolved", "implementationId": entry["id"], "entry": entry}
    return {
        "status": "unresolved",
        "query": query,
        "candidates": [
            {"id": e["id"], "summary": e.get("summary", ""), "status": e.get("status", "")}
            for e in entries
        ],
    }


def cmd_list() -> int:
    for entry in load_registry():
        print(f"{entry.get('id')}\t{entry.get('status')}\t{entry.get('summary', '')}")
    return 0


def cmd_resolve(query: str) -> int:
    result = resolve(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "resolved" else 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: resolve_implementation.py list|resolve <id|cue>", file=sys.stderr)
        return 2
    if argv[1] == "list":
        return cmd_list()
    if argv[1] == "resolve" and len(argv) >= 3:
        return cmd_resolve(argv[2])
    print("usage: resolve_implementation.py list|resolve <id|cue>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
