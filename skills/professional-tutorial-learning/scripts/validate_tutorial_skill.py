#!/usr/bin/env python3
"""Validate the professional tutorial learning skill structure.

This checker intentionally avoids third-party dependencies.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / "skills" / "professional-tutorial-learning"
REFERENCES = SKILL_DIR / "references"
REGISTRY = REFERENCES / "source_workflow_registry.md"
TEMPLATE = REFERENCES / "lesson_artifact_template.md"
EXAMPLE = SKILL_DIR / "examples" / "first_lesson.md"
ITERATION = REFERENCES / "iteration_protocol.md"
MODEL_CONTRACT = REFERENCES / "tutorial_model_contract.md"
PDF_WORKFLOW = REFERENCES / "pdf_chapter_workflow.md"

REQUIRED_TEMPLATE_SECTIONS = [
    "Source Metadata",
    "Learning Objectives",
    "Knowledge Point Map",
    "Reading-Only Material",
    "Skipped Or Compressed Material",
    "Guided Explanation",
    "Practice Task",
    "Checkpoint Questions",
    "Review Prompts",
    "Further Reading / Deep Dives",
    "Web App Data",
    "Next Lesson Preview",
]

REQUIRED_EXAMPLE_SECTIONS = [
    "Source Metadata",
    "Why This Section Matters",
    "Learning Objectives",
    "Knowledge Point Map",
    "Reading-Only Material",
    "Skipped Or Compressed Material",
    "Guided Explanation",
    "Practice Task",
    "Checkpoint Questions",
    "Review Prompts",
    "Further Reading / Deep Dives",
    "Web App Data",
    "Next Lesson Preview",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_headings(text: str) -> set[str]:
    headings: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.add(match.group(1).strip())
    return headings


def parse_registry_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or stripped.lower().startswith("| id |"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) == 9 and cells[0].startswith("`"):
            rows.append(cells)
    return rows


def validate_registry() -> list[str]:
    errors: list[str] = []
    if not REGISTRY.exists():
        return [f"{REGISTRY.relative_to(ROOT)} is missing"]
    rows = parse_registry_rows(read(REGISTRY))
    if not rows:
        errors.append("source_workflow_registry.md has no registry rows")
    ids: set[str] = set()
    for row in rows:
        workflow_id = row[0].strip("`")
        path_value = row[1].strip("`")
        if workflow_id in ids:
            errors.append(f"duplicate workflow id: {workflow_id}")
        ids.add(workflow_id)
        target = SKILL_DIR / path_value
        if not target.exists():
            errors.append(f"registry path does not exist: {path_value}")
    return errors


def validate_sections(path: Path, required: list[str]) -> list[str]:
    if not path.exists():
        return [f"{path.relative_to(ROOT)} is missing"]
    headings = markdown_headings(read(path))
    return [f"{path.relative_to(ROOT)} missing section: {section}" for section in required if section not in headings]


def table_rows_containing(text: str, prefix_pattern: str) -> list[list[str]]:
    rows: list[list[str]] = []
    pattern = re.compile(prefix_pattern)
    for line in text.splitlines():
        if pattern.match(line):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def validate_iteration() -> list[str]:
    if not ITERATION.exists():
        return [f"{ITERATION.relative_to(ROOT)} is missing"]
    text = read(ITERATION)
    errors: list[str] = []
    rows = table_rows_containing(text, r"^\|\s*(?:[1-9]|10)\s*\|")
    if len(rows) < 20:
        errors.append("iteration protocol should contain 10 summary rows and 10 detail rows")
    for round_number in range(1, 11):
        matches = [row for row in rows if row and row[0] == str(round_number)]
        if len(matches) < 2:
            errors.append(f"iteration log missing summary or detail evidence for round {round_number}")
        for row in matches:
            if len(row) < 5 or any(len(cell) < 8 for cell in row[1:5]):
                errors.append(f"iteration row {round_number} has an underspecified four-step record")
    for phrase in ["Abstract model update", "Concrete workflow update", "Trial generation", "Evaluation and revision", "Rubric snapshot", "Rejected revision"]:
        if phrase not in text:
            errors.append(f"iteration protocol missing phrase: {phrase}")
    return errors


def validate_semantics() -> list[str]:
    errors: list[str] = []
    model = read(MODEL_CONTRACT) if MODEL_CONTRACT.exists() else ""
    pdf = read(PDF_WORKFLOW) if PDF_WORKFLOW.exists() else ""
    example = read(EXAMPLE) if EXAMPLE.exists() else ""
    template = read(TEMPLATE) if TEMPLATE.exists() else ""

    for phrase in ["interface TutorialLearningRequest", "learnerGoal", "depthPolicy", "reviewPolicy", "sourceAccessMode"]:
        if phrase not in model:
            errors.append(f"tutorial model contract missing semantic requirement: {phrase}")
    for phrase in ["Concrete PDF Processing Procedure", "Normalize page ranges", "TutorialUnit.sourceRange", "OCR", "code blocks", "Minimum Viable Input"]:
        if phrase not in pdf:
            errors.append(f"PDF workflow missing concrete processing requirement: {phrase}")
    for phrase in ["core_knowledge_point", "reading_only_material", "advanced_optional", "CB1", "P1", "C1", "R1", "L1"]:
        if phrase not in example:
            errors.append(f"example missing semantic marker: {phrase}")
    for phrase in ["webAppData", "checkpointIds", "reviewPromptIds"]:
        if phrase not in template:
            errors.append(f"lesson template missing web-app field: {phrase}")
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    errors.extend(validate_registry())
    errors.extend(validate_sections(TEMPLATE, REQUIRED_TEMPLATE_SECTIONS))
    errors.extend(validate_sections(EXAMPLE, REQUIRED_EXAMPLE_SECTIONS))
    errors.extend(validate_iteration())
    errors.extend(validate_semantics())
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Tutorial skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Tutorial skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
