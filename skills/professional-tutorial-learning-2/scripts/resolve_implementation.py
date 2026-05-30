#!/usr/bin/env python3
"""Resolve a tutorial-learning implementation from registry metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "tutorial-implementations.json"


def norm(value: str) -> str:
    return " ".join(value.lower().strip().split())


def score(entry: dict, query: str, medium: str) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score_value = 0
    exact_values = [entry["id"], *entry.get("exactAliases", [])]
    if query in {norm(v) for v in exact_values}:
        return 100, ["exact id or alias match"]

    for negative in entry.get("negativeCues", []):
        if norm(negative) in query:
            return -100, [f"negative cue: {negative}"]

    for cue in entry.get("mediumCues", []):
        if norm(cue) in query or (medium and norm(cue) == medium):
            score_value += 25
            reasons.append(f"medium cue: {cue}")
    for cue in entry.get("domainCues", []):
        if norm(cue) in query:
            score_value += 15
            reasons.append(f"domain cue: {cue}")
    for alias in entry.get("contextualAliases", []):
        if norm(alias) in query:
            score_value += 10
            reasons.append(f"contextual alias: {alias}")
    return score_value, reasons


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="User request or implementation id.")
    parser.add_argument("--medium", default="", help="Optional known medium, such as pdf.")
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    query = norm(args.query)
    medium = norm(args.medium)
    candidates = []
    for entry in registry["implementations"]:
        if entry.get("status") == "deprecated":
            continue
        value, reasons = score(entry, query, medium)
        if value > 0:
            candidates.append(
                {
                    "id": entry["id"],
                    "summary": entry["summary"],
                    "score": value,
                    "reason": "; ".join(reasons),
                }
            )

    candidates.sort(key=lambda item: item["score"], reverse=True)
    if not candidates:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "unresolved",
                    "reason": "No registered implementation matched the request.",
                    "candidates": [
                        {"id": e["id"], "summary": e["summary"], "reason": "available registered option"}
                        for e in registry["implementations"]
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1

    if len(candidates) == 1 or candidates[0]["score"] >= 100 or candidates[0]["score"] >= candidates[1]["score"] + 20:
        print(
            json.dumps(
                {
                    "ok": True,
                    "status": "resolved",
                    "implementationId": candidates[0]["id"],
                    "confidence": "explicit" if candidates[0]["score"] >= 100 else "strong",
                    "reason": candidates[0]["reason"],
                    "nextCommand": f"python scripts/get_implementation.py {candidates[0]['id']}",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    print(
        json.dumps(
            {
                "ok": False,
                "status": "ambiguous",
                "reason": "Multiple registered implementations are plausible.",
                "candidates": candidates,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
