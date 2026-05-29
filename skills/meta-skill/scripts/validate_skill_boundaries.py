#!/usr/bin/env python3
"""Validate repository skill loading boundaries.

This checker is intentionally dependency-free. It catches static patterns that tend
to make agents load too much context: oversized entry files, implementation fan-out
from SKILL.md, asset catalogs in orchestration files, and growing implementation
families without deterministic dispatch scripts.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = ROOT / "skills"

MAX_SKILL_MD_CHARS = 30000
MAX_IMPLEMENTATION_PATHS_IN_SKILL = 8
MAX_ASSET_PATHS_IN_SKILL = 12
FAMILY_IMPLEMENTATION_THRESHOLD = 4

LIST_SCRIPT_RE = re.compile(r"(^|[_-])list([_-]|$)")
RESOLVE_SCRIPT_RE = re.compile(r"(^|[_-])resolve([_-]|$)")
GET_SCRIPT_RE = re.compile(r"(^|[_-])(get|materialize)([_-]|$)")
VALIDATE_SCRIPT_RE = re.compile(r"(^|[_-])validate([_-]|$)")

BROAD_READ_PATTERNS = [
    re.compile(r"read\s+(all|every)\s+files?\s+under\s+`?(references|implementations|assets)/?`?", re.I),
    re.compile(r"load\s+(all|every)\s+`?(references|implementations|assets)/?`?", re.I),
    re.compile(r"browse\s+(all|every)\s+`?(references|implementations|assets)/?`?", re.I),
]

IMPLEMENTATION_PATH_RE = re.compile(
    r"(?:references/[A-Za-z0-9_-]+(?:_style|_provider|_strategy|_adapter|_mode)\.md|implementations/[A-Za-z0-9_.\-/]+)"
)
ASSET_PATH_RE = re.compile(r"assets/[A-Za-z0-9_.\-/]+")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def script_names(skill_dir: Path) -> list[str]:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return []
    return [p.name for p in scripts_dir.iterdir() if p.is_file()]


def has_script(names: list[str], pattern: re.Pattern[str]) -> bool:
    return any(pattern.search(name) for name in names)


def implementation_count(skill_dir: Path, skill_text: str) -> int:
    count = 0
    implementations_dir = skill_dir / "implementations"
    if implementations_dir.is_dir():
        count += len([p for p in implementations_dir.iterdir() if p.is_dir()])

    # Count likely concrete implementation references from SKILL.md as a signal,
    # but de-duplicate so repeated command examples do not inflate the value.
    count = max(count, len(set(IMPLEMENTATION_PATH_RE.findall(skill_text))))
    return count


def registry_count(skill_dir: Path) -> int:
    total = 0
    registry_dir = skill_dir / "registry"
    if registry_dir.is_dir():
        total += len([p for p in registry_dir.iterdir() if p.is_file() and p.suffix in {".json", ".yaml", ".yml", ".md"}])
    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        total += len(list(references_dir.glob("*_registry.md")))
    return total


def looks_like_family(skill_dir: Path, skill_text: str) -> bool:
    lower = skill_text.lower()
    family_words = [
        "implementation family",
        "multi-implementation",
        "multiple implementations",
        "strategies",
        "providers",
        "adapters",
        "modes",
        "styles",
    ]
    return (
        any(word in lower for word in family_words)
        or (skill_dir / "implementations").is_dir()
        or registry_count(skill_dir) > 1
    )


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return errors

    text = read(skill_md)
    if len(text) > MAX_SKILL_MD_CHARS:
        errors.append(
            f"{rel(skill_md)} is {len(text)} chars; keep SKILL.md orchestration-focused "
            f"or raise MAX_SKILL_MD_CHARS intentionally"
        )

    for pattern in BROAD_READ_PATTERNS:
        if pattern.search(text):
            errors.append(f"{rel(skill_md)} instructs broad resource loading; use registries/scripts instead")
            break

    implementation_paths = set(IMPLEMENTATION_PATH_RE.findall(text))
    if len(implementation_paths) > MAX_IMPLEMENTATION_PATHS_IN_SKILL:
        errors.append(
            f"{rel(skill_md)} lists {len(implementation_paths)} implementation paths; "
            "move catalog discovery to a registry/list script"
        )

    asset_paths = set(ASSET_PATH_RE.findall(text))
    if len(asset_paths) > MAX_ASSET_PATHS_IN_SKILL:
        errors.append(
            f"{rel(skill_md)} lists {len(asset_paths)} asset paths; "
            "move asset catalogs to manifests and selected implementation policies"
        )

    impl_count = implementation_count(skill_dir, text)
    if looks_like_family(skill_dir, text) and impl_count >= FAMILY_IMPLEMENTATION_THRESHOLD:
        names = script_names(skill_dir)
        missing_roles = []
        if not has_script(names, LIST_SCRIPT_RE):
            missing_roles.append("list")
        if not has_script(names, RESOLVE_SCRIPT_RE):
            missing_roles.append("resolve")
        if not has_script(names, GET_SCRIPT_RE):
            missing_roles.append("get/materialize")
        if not has_script(names, VALIDATE_SCRIPT_RE):
            missing_roles.append("validate")
        if missing_roles:
            errors.append(
                f"{skill_dir.relative_to(ROOT)} looks like a growing implementation family "
                f"({impl_count} implementations) but is missing dispatch scripts: "
                + ", ".join(missing_roles)
            )

    return errors


def validate() -> list[str]:
    errors: list[str] = []
    if not SKILLS_DIR.exists():
        return ["skills/ directory is missing"]

    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        errors.extend(validate_skill(skill_dir))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Skill boundary validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill boundary validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
