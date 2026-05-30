#!/usr/bin/env python3
"""Validate skill-tune module layout and optional session artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import tune_lib as lib  # noqa: E402

SKILL_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/tune_contract.md",
    "references/rubric_contract.md",
    "references/run_contract.md",
    "references/artifacts_contract.md",
    "references/judge_contract.md",
    "references/default_rubric.md",
    "references/improve_contract.md",
    "references/self_iter_template.md",
    "references/tune_rubric_template.md",
    "examples/sample_round.md",
    "scripts/tune_lib.py",
    "scripts/tune_session.py",
    "scripts/check_runtime.py",
]

REQUIRED_SECTIONS = (
    "purpose",
    "triggers",
    "workflow",
    "inputs",
    "references",
    "resources",
    "extension",
    "quality",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_titles(markdown: str) -> set[str]:
    titles: set[str] = set()
    for line in markdown.splitlines():
        m = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if m:
            titles.add(m.group(1).strip().lower())
    return titles


def validate_skill_md(skill_md: Path) -> list[str]:
    errors: list[str] = []
    body = read(skill_md)
    if not body.startswith("---\n"):
        errors.append("SKILL.md missing YAML front matter")
        return errors
    try:
        _, _, body = body.split("---\n", 2)
    except ValueError:
        errors.append("SKILL.md front matter not closed")
        return errors
    titles = section_titles(body)
    for label in REQUIRED_SECTIONS:
        if not any(label in t for t in titles):
            errors.append(f"SKILL.md missing section matching {label!r}")
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    skill_md = root / "SKILL.md"
    if skill_md.is_file():
        errors.extend(validate_skill_md(skill_md))

    tune_contract = root / "references/tune_contract.md"
    if tune_contract.is_file():
        tc = read(tune_contract)
        if re.search(r"scores:\s*\n\s*taskFit:\s*1-5", tc):
            errors.append("tune_contract.md hard-codes dimension scores")

    default_rubric = root / "references/default_rubric.md"
    try:
        rubric = lib.parse_rubric_file(default_rubric) if default_rubric.is_file() else None
    except ValueError as exc:
        errors.append(f"default_rubric.md: {exc}")
        rubric = None

    if rubric:
        for dim in rubric.dimensions:
            if dim.excellent_threshold < 1:
                errors.append(f"invalid threshold for {dim.id}")

    for arg in sys.argv[2:]:
        if arg.startswith("--judge-result=") and rubric:
            jr = Path(arg.split("=", 1)[1])
            out_arg = next((a for a in sys.argv[2:] if a.startswith("--out-file=")), None)
            if jr.is_file() and out_arg:
                out_path = Path(out_arg.split("=", 1)[1])
                try:
                    result = lib.load_judge_result(jr)
                    errors.extend(
                        lib.validate_judge_result(result, rubric, read(out_path))
                    )
                except (json.JSONDecodeError, ValueError) as exc:
                    errors.append(f"judge result: {exc}")

        if arg.startswith("--log=") and rubric:
            log_path = Path(arg.split("=", 1)[1])
            if log_path.is_file():
                header_dims = lib.parse_log_dimension_ids(log_path)
                if header_dims and header_dims != [d.id for d in rubric.dimensions]:
                    errors.append(
                        f"log rubric dimensions {header_dims!r} != active rubric "
                        f"{[d.id for d in rubric.dimensions]!r}"
                    )

    return errors


def main() -> int:
    root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-")
        else SKILL_ROOT
    )
    errors = validate(root)
    if errors:
        print("skill-tune validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"skill-tune validation passed ({root})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
