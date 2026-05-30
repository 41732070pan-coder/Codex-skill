#!/usr/bin/env python3
"""List and resolve tutorial-learning medium implementations."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REGISTRY = SKILL_DIR / "registry" / "mediums.yaml"


def load_registry() -> list[dict]:
    text = REGISTRY.read_text(encoding="utf-8")
    entries: list[dict] = []
    current: dict | None = None
    in_entries = False
    for line in text.splitlines():
        if line.strip() == "entries:":
            in_entries = True
            continue
        if not in_entries:
            continue
        if line.startswith("  - id:"):
            if current:
                entries.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif current is not None and line.strip().startswith("- ") and "aliases" not in current:
            pass
        elif current is not None and ":" in line:
            key, _, val = line.strip().partition(":")
            key = key.strip()
            val = val.strip()
            if key == "aliases" or key == "domainCues" or key == "mediumCues":
                if key not in current:
                    current[key] = []
                item = val.strip("- ").strip()
                if item.startswith("["):
                    current[key] = json.loads(item.replace("'", '"'))
                elif item:
                    current[key].append(item)
            elif val.startswith("["):
                current[key] = json.loads(val.replace("'", '"'))
            else:
                current[key] = val.strip('"')
    if current:
        entries.append(current)
    return entries


def load_registry_simple() -> list[dict]:
    """Parse minimal YAML without PyYAML."""
    import re

    text = REGISTRY.read_text(encoding="utf-8")
    chunks = re.split(r"\n  - id:", text)
    entries = []
    for chunk in chunks[1:]:
        entry: dict = {}
        lines = ("id:" + chunk).splitlines()
        for line in lines:
            m = re.match(r"^    (\w+):\s*(.*)$", line)
            if not m:
                continue
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("["):
                entry[key] = json.loads(val.replace("'", '"'))
            else:
                entry[key] = val.strip('"')
        if entry.get("id"):
            entries.append(entry)
    return entries


def resolve(query: str) -> dict:
    q = query.lower().strip()
    entries = load_registry_simple()
    for e in entries:
        if e.get("id", "").lower() == q:
            return {"status": "resolved", "implementationId": e["id"], "entry": e}
        for field in ("aliases", "domainCues", "mediumCues"):
            for cue in e.get(field, []) or []:
                if cue.lower() == q:
                    return {"status": "resolved", "implementationId": e["id"], "entry": e}
    if q == "pdf":
        for e in entries:
            if e.get("id") == "pdf-chaptered":
                return {"status": "resolved", "implementationId": e["id"], "entry": e}
    candidates = [
        {"id": e["id"], "summary": e.get("summary", ""), "status": e.get("status", "")}
        for e in entries
        if e.get("status") != "draft" or q in str(e.get("aliases", [])).lower()
    ]
    return {"status": "unresolved", "query": query, "candidates": candidates}


def cmd_list() -> int:
    for e in load_registry_simple():
        print(f"{e.get('id')}\t{e.get('status')}\t{e.get('summary', '')}")
    return 0


def cmd_resolve(query: str) -> int:
    result = resolve(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "resolved" else 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: resolve_medium.py list|resolve <id|cue>", file=sys.stderr)
        return 2
    if argv[1] == "list":
        return cmd_list()
    if argv[1] == "resolve" and len(argv) >= 3:
        return cmd_resolve(argv[2])
    print("usage: resolve_medium.py list|resolve <id|cue>", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
