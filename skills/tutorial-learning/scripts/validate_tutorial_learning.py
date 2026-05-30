#!/usr/bin/env python3
"""Validate the tutorial-learning runtime contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "implementations/hypertext-tutorial/SKILL.impl.md",
    "references/evaluator_rubric.md",
    "references/h5_lesson_schema.md",
    "references/implementation_registry.md",
    "references/learning_contract.md",
    "references/lecture_template.md",
    "references/review_protocol.md",
    "references/source_fidelity.md",
    "references/triage_protocol.md",
    "registry/implementations.yaml",
    "scripts/resolve_implementation.py",
    "scripts/validate_tutorial_learning.py",
}
REQUIRED_REFS = {
    "learning_contract.md",
    "implementation_registry.md",
    "source_fidelity.md",
    "triage_protocol.md",
    "lecture_template.md",
    "review_protocol.md",
    "h5_lesson_schema.md",
    "evaluator_rubric.md",
}
REQUIRED_SECTIONS = {
    "purpose",
    "triggers",
    "workflow",
    "inputs",
    "references",
    "resources",
    "extension",
    "quality",
}
REQUIRED_CONTRACT_TERMS = {
    "TutorialImplementation",
    "HypertextSourceFormat",
    "SourceTrace",
    "HypertextBlock",
    "TutorialLearningBase",
    "hypertext-tutorial",
}
REQUIRED_TEMPLATE_HEADINGS = {
    "本节目标",
    "来源与边界",
    "学习路线",
    "核心讲解",
    "跳过与延伸阅读",
    "微测",
    "练习任务",
    "复习卡",
    "阅读材料（附录）",
}
REQUIRED_SOURCE_FORMATS = {"pdf", "html", "markdown", "plain_text_with_headings"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_titles(md: str) -> set[str]:
    return {match.group(1).lower() for match in re.finditer(r"^##\s+(.+?)\s*$", md, re.M)}


def parse_list(value: str) -> set[str]:
    value = value.strip()
    if not value.startswith("[") or not value.endswith("]"):
        return set()
    return {item.strip().strip("\"'") for item in value[1:-1].split(",") if item.strip()}


def parse_registry_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    chunks = re.split(r"\n  - id:", text)
    for chunk in chunks[1:]:
        entry: dict[str, str] = {}
        for line in ("id:" + chunk).splitlines():
            match = re.match(r"^\s*(\w+):\s*(.*)$", line)
            if match:
                entry[match.group(1)] = match.group(2).strip().strip('"')
        if entry.get("id"):
            entries.append(entry)
    return entries


def runtime_files() -> set[str]:
    return {
        str(path.relative_to(SKILL_DIR))
        for path in SKILL_DIR.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def check_manifest(errors: list[str]) -> None:
    actual = runtime_files()
    for path in sorted(EXPECTED_FILES - actual):
        errors.append(f"missing runtime file: {path}")
    for path in sorted(actual - EXPECTED_FILES):
        errors.append(f"unexpected runtime file: {path}")


def main() -> int:
    errors: list[str] = []
    check_manifest(errors)

    skill_md = SKILL_DIR / "SKILL.md"
    if skill_md.exists():
        titles = section_titles(read(skill_md))
        for needle in REQUIRED_SECTIONS:
            if not any(needle in title for title in titles):
                errors.append(f"SKILL.md missing section matching {needle!r}")

    for name in REQUIRED_REFS:
        if not (SKILL_DIR / "references" / name).exists():
            errors.append(f"missing references/{name}")

    registry = SKILL_DIR / "registry" / "implementations.yaml"
    if registry.exists():
        entries = parse_registry_entries(read(registry))
        ids = [entry.get("id") for entry in entries]
        if ids != ["hypertext-tutorial"]:
            errors.append(f"registry must contain only hypertext-tutorial, found {ids}")
        for entry in entries:
            implementation = SKILL_DIR / entry.get("implementationPath", "")
            if entry.get("status") != "stable":
                errors.append("hypertext-tutorial must be stable")
            if not implementation.exists():
                errors.append(f"implementation path missing: {entry.get('implementationPath')}")
            source_formats = parse_list(entry.get("sourceFormats", ""))
            if source_formats != REQUIRED_SOURCE_FORMATS:
                errors.append(f"hypertext-tutorial source formats must be {sorted(REQUIRED_SOURCE_FORMATS)}, found {sorted(source_formats)}")

    implementation = SKILL_DIR / "implementations" / "hypertext-tutorial" / "SKILL.impl.md"
    if implementation.exists():
        implementation_text = read(implementation)
        for term in {"source_fidelity.md", "triage_protocol.md", "lecture_template.md", "review_protocol.md", "h5_lesson_schema.md"}:
            if term not in implementation_text:
                errors.append(f"hypertext implementation does not reference {term}")

    contract = SKILL_DIR / "references" / "learning_contract.md"
    if contract.exists():
        contract_text = read(contract)
        for term in REQUIRED_CONTRACT_TERMS:
            if term not in contract_text:
                errors.append(f"learning_contract.md missing required term: {term}")

    template = SKILL_DIR / "references" / "lecture_template.md"
    if template.exists():
        template_text = read(template)
        for heading in REQUIRED_TEMPLATE_HEADINGS:
            if f"## {heading}" not in template_text:
                errors.append(f"lecture_template.md missing heading: {heading}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK: tutorial-learning runtime contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
