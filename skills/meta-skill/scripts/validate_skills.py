#!/usr/bin/env python3
"""Validate repository-level Codex skill structure.

This checker intentionally avoids third-party dependencies so the meta-skill can
be validated in minimal environments.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
REGISTRY = ROOT / "skills" / "meta-skill" / "references" / "skill_registry.md"

REQUIRED_SECTION_GROUPS = {
    "purpose": ("purpose",),
    "triggers/non-triggers": ("triggers", "non-triggers"),
    "workflow": ("workflow",),
    "inputs/outputs": ("inputs", "outputs"),
    "references": ("references",),
    "resources": ("resources",),
    "extension": ("extens",),
    "quality gate": ("quality",),
}

REGISTRY_COLUMNS = [
    "skill",
    "path",
    "type",
    "status",
    "function",
    "trigger cues",
    "primary outputs",
    "overlap risks",
    "notes",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = read(path)
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML front matter fence")
    try:
        _, raw_frontmatter, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("missing closing YAML front matter fence") from exc

    metadata: dict[str, str] = {}
    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid front matter line: {line!r}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, body


def section_titles(markdown: str) -> set[str]:
    titles: set[str] = set()
    for line in markdown.splitlines():
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            titles.add(match.group(1).strip().lower())
    return titles


def has_section_group(titles: set[str], needles: tuple[str, ...]) -> bool:
    return any(all(needle in title for needle in needles) for title in titles)


def markdown_table_header(path: Path) -> list[str] | None:
    for line in read(path).splitlines():
        stripped = line.strip()
        if stripped.startswith("| Skill |"):
            return [cell.strip().lower() for cell in stripped.strip("|").split("|")]
    return None


def validate_asset_manifests(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    assets_dir = skill_dir / "assets"
    if not assets_dir.exists():
        return errors

    for asset_root in [assets_dir, *[p for p in assets_dir.iterdir() if p.is_dir()]]:
        has_files = any(p.is_file() for p in asset_root.iterdir())
        if not has_files:
            continue
        manifests = list(asset_root.glob("*MANIFEST.md"))
        if not manifests:
            errors.append(
                f"{asset_root.relative_to(ROOT)} contains asset files but no *MANIFEST.md"
            )
    return errors


def validate() -> list[str]:
    errors: list[str] = []
    if not SKILLS_DIR.exists():
        return ["skills/ directory is missing"]

    readme_text = read(README) if README.exists() else ""
    registry_text = read(REGISTRY) if REGISTRY.exists() else ""
    registry_header = markdown_table_header(REGISTRY) if REGISTRY.exists() else None

    if registry_header != REGISTRY_COLUMNS:
        errors.append(
            "skill_registry.md table header must be: "
            + " | ".join(REGISTRY_COLUMNS)
        )

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir.relative_to(ROOT)} is missing SKILL.md")
            continue

        try:
            metadata, body = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"{skill_md.relative_to(ROOT)}: {exc}")
            continue

        name = metadata.get("name")
        description = metadata.get("description")
        if not name:
            errors.append(f"{skill_md.relative_to(ROOT)} front matter is missing name")
        elif name != skill_dir.name:
            errors.append(
                f"{skill_md.relative_to(ROOT)} name {name!r} does not match directory {skill_dir.name!r}"
            )
        if not description:
            errors.append(f"{skill_md.relative_to(ROOT)} front matter is missing description")

        titles = section_titles(body)
        for label, needles in REQUIRED_SECTION_GROUPS.items():
            if not has_section_group(titles, needles):
                errors.append(f"{skill_md.relative_to(ROOT)} is missing a {label} section")

        rel_path = f"skills/{skill_dir.name}/"
        if rel_path not in readme_text:
            errors.append(f"README.md does not list {rel_path}")
        if rel_path not in registry_text:
            errors.append(f"skill_registry.md does not list {rel_path}")

        errors.extend(validate_asset_manifests(skill_dir))

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
