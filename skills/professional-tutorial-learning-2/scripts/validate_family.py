#!/usr/bin/env python3
"""Validate professional-tutorial-learning registry, implementation, and lab artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "tutorial-implementations.json"
REQUIRED_ENTRY_FIELDS = {
    "id",
    "displayName",
    "status",
    "summary",
    "implementationPath",
    "exactAliases",
    "contextualAliases",
    "mediumCues",
    "domainCues",
    "negativeCues",
    "ambiguityRisks",
    "fallbackPolicy",
    "assetRoot",
}
REQUIRED_IMPLEMENTATION_SECTIONS = [
    "Purpose",
    "Selection Inputs",
    "Source Handling",
    "Structure Parsing",
    "Content Classification",
    "Depth Policy",
    "Workflow",
    "Output Contract",
    "Web App Hooks",
    "Quality Gates",
    "Failure Modes",
]
REQUIRED_LECTURE_SECTIONS = [
    "Source Trace",
    "Learning Goals",
    "Original Structure Recognition",
    "Core Knowledge Map",
    "Required Content",
    "Skim Or Skip",
    "Deeper Links",
    "Pitfalls",
    "Quiz",
    "Practice Task",
    "Web Review App Spec",
    "Spaced Review Cards",
]
REQUIRED_KNOWLEDGE_MAP_FIELDS = [
    "Source Trace",
    "Importance",
    "Difficulty",
    "Usefulness",
    "Depth Decision",
]
REQUIRED_WEB_SPEC_TERMS = [
    "Concept ids",
    "Quiz screen",
    "Review screen",
    "remediation",
]


def headings(text: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^##\s+(.+?)\s*$", text, re.M)}


def validate_registry(errors: list[str]) -> None:
    if not REGISTRY.exists():
        errors.append("registry/tutorial-implementations.json is missing")
        return
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"registry JSON is invalid: {exc}")
        return

    ids: set[str] = set()
    aliases: dict[str, str] = {}
    for entry in registry.get("implementations", []):
        missing = REQUIRED_ENTRY_FIELDS - set(entry)
        if missing:
            errors.append(f"{entry.get('id', '<unknown>')} missing fields: {sorted(missing)}")
        entry_id = entry.get("id", "")
        if not entry_id:
            errors.append("implementation entry missing id")
            continue
        if entry_id in ids:
            errors.append(f"duplicate implementation id: {entry_id}")
        ids.add(entry_id)
        for alias in entry.get("exactAliases", []):
            key = alias.lower()
            if key in aliases:
                errors.append(f"duplicate exact alias {alias!r}: {aliases[key]} and {entry_id}")
            aliases[key] = entry_id
        impl_path = ROOT / entry.get("implementationPath", "")
        if not impl_path.exists():
            errors.append(f"{entry_id} implementation path missing: {entry.get('implementationPath')}")
            continue
        impl_headings = headings(impl_path.read_text(encoding="utf-8"))
        for required in REQUIRED_IMPLEMENTATION_SECTIONS:
            if required not in impl_headings:
                errors.append(f"{entry_id} implementation missing section: {required}")


def validate_lectures(errors: list[str]) -> None:
    for name in ["pdf-a-first-section-lecture.md", "pdf-b-first-section-lecture.md"]:
        path = ROOT / "examples" / name
        if not path.exists():
            errors.append(f"example lecture missing: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        lecture_headings = headings(text)
        for required in REQUIRED_LECTURE_SECTIONS:
            if required not in lecture_headings:
                errors.append(f"{name} missing section: {required}")
        if not re.search(r"[\u4e00-\u9fff]", text):
            errors.append(f"{name} must contain Chinese learning content")
        for required in ["Author:", "Use condition:", "Source trust:"]:
            if required not in text:
                errors.append(f"{name} missing source metadata field: {required}")
        for required in REQUIRED_KNOWLEDGE_MAP_FIELDS:
            if required not in text:
                errors.append(f"{name} missing knowledge-map field: {required}")
        for required in REQUIRED_WEB_SPEC_TERMS:
            if required not in text:
                errors.append(f"{name} missing Web spec term: {required}")


def validate_iteration_log(errors: list[str]) -> None:
    path = ROOT / "logs" / "iteration-log.md"
    if not path.exists():
        errors.append("logs/iteration-log.md is missing")
        return
    text = path.read_text(encoding="utf-8")
    rounds = len(re.findall(r"^## Round\s+\d{2}\b", text, re.M))
    steps = len(re.findall(r"^### Step\s+\d{2}\b", text, re.M))
    if rounds != 10:
        errors.append(f"iteration log must contain 10 rounds, found {rounds}")
    if steps != 40:
        errors.append(f"iteration log must contain 40 steps, found {steps}")
    if "PDF A" not in text or "PDF B" not in text:
        errors.append("iteration log must record PDF A and PDF B")


def main() -> int:
    errors: list[str] = []
    validate_registry(errors)
    validate_lectures(errors)
    validate_iteration_log(errors)
    if errors:
        print("Family validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Family validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
