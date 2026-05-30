#!/usr/bin/env python3
"""List registered tutorial-learning implementations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "tutorial-implementations.json"


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="", help="Optional case-insensitive filter.")
    parser.add_argument("--status", default="", help="Optional status filter.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a table.")
    args = parser.parse_args()

    query = args.query.lower().strip()
    status = args.status.lower().strip()
    entries = load_registry()["implementations"]
    filtered = []
    for entry in entries:
        blob = json.dumps(entry, ensure_ascii=False).lower()
        if query and query not in blob:
            continue
        if status and entry.get("status", "").lower() != status:
            continue
        filtered.append(entry)

    if args.json:
        print(json.dumps(filtered, indent=2, ensure_ascii=False))
        return 0

    print("id\tstatus\tsummary")
    for entry in filtered:
        print(f"{entry['id']}\t{entry['status']}\t{entry['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
