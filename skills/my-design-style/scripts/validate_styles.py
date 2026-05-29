#!/usr/bin/env python3
"""Validate my-design-style concrete style conformance.

This checker is intentionally dependency-free so it can run in minimal Codex
skill environments. It validates the framework-level contracts that can be
checked statically; visual quality remains a manual quality gate.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / "skills" / "my-design-style"
REGISTRY = SKILL_DIR / "references" / "style_registry.md"

REQUIRED_INTERFACES = [
    "TriggerMatcher",
    "DesignIntentProvider",
    "PaletteProvider",
    "TypographyProvider",
    "LayoutSystem",
    "ComponentTranslator",
    "AssetPolicy",
    "SurfaceTexturePolicy",
    "QualityGate",
]

REQUIRED_SECTIONS = [
    "Implementation Map",
    "Triggers",
    "Intent",
    "Anti-Goals",
    "Color Tokens",
    "Typography",
    "Layout Principles",
    "PPT Slide Archetypes",
    "Web Translation",
    "App / Dashboard Translation",
    "Static Visual Translation",
    "Asset Interface",
    "Surface Texture Policy",
    "Asset Rules",
    "Self-Check",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_registry() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = read(REGISTRY).splitlines()
    header: list[str] | None = None
    in_entries = False

    for line in lines:
        if line.strip() == "## Registry Entries":
            in_entries = True
            continue
        if in_entries and line.startswith("## "):
            break
        if not in_entries or not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if set(cells) == {"---"} or all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if header is None:
            header = [cell.lower() for cell in cells]
            continue
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))

    return rows


def strip_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def section_titles(markdown: str) -> set[str]:
    titles: set[str] = set()
    for line in markdown.splitlines():
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            titles.add(match.group(1).strip())
    return titles


def section_body(markdown: str, section: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    next_match = re.search(r"^##\s+", markdown[match.end():], re.MULTILINE)
    if next_match:
        return markdown[match.end(): match.end() + next_match.start()]
    return markdown[match.end():]


def extract_bullet_value(markdown: str, key: str) -> str | None:
    pattern = re.compile(rf"^- `?{re.escape(key)}`?:\s*(.+?)\.?$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return None
    return strip_code(match.group(1).strip())


def validate_style(row: dict[str, str]) -> list[str]:
    errors: list[str] = []
    style = strip_code(row.get("style", ""))
    reference = strip_code(row.get("reference", ""))
    asset_root = strip_code(row.get("asset root", ""))

    if not style:
        return ["registry row is missing Style"]
    if not reference:
        return [f"registry row for {style} is missing Reference"]

    ref_path = SKILL_DIR / reference
    if not ref_path.exists():
        return [f"{style} reference does not exist: {reference}"]

    text = read(ref_path)
    titles = section_titles(text)

    for section in REQUIRED_SECTIONS:
        if section not in titles:
            errors.append(f"{reference} is missing section: {section}")

    for interface in REQUIRED_INTERFACES:
        if f"`{interface}`" not in text:
            errors.append(f"{reference} Implementation Map is missing {interface}")

    if "ok" not in text or "issues" not in text or "requiredFixes" not in text:
        errors.append(f"{reference} Self-Check must expose ok, issues, and requiredFixes")

    asset_section = section_body(text, "Asset Interface")
    surface_section = section_body(text, "Surface Texture Policy")

    declared_asset_root = extract_bullet_value(asset_section, "assetRoot")
    if declared_asset_root is None:
        errors.append(f"{reference} Asset Interface is missing assetRoot")
    elif declared_asset_root != asset_root:
        errors.append(
            f"{reference} assetRoot {declared_asset_root!r} does not match registry {asset_root!r}"
        )

    for root in {asset_root, declared_asset_root or ""}:
        if root and root != "none":
            asset_dir = SKILL_DIR / root
            if not asset_dir.is_dir():
                errors.append(f"{reference} declares missing asset root: {root}")
            elif not any(asset_dir.glob("*MANIFEST.md")):
                errors.append(f"{reference} asset root has no *MANIFEST.md: {root}")

    provider = extract_bullet_value(surface_section, "provider")
    if provider is None:
        errors.append(f"{reference} Surface Texture Policy is missing provider")
    elif provider != "none":
        provider_root = extract_bullet_value(surface_section, "assetRoot")
        manifest = extract_bullet_value(surface_section, "manifestFile")
        if not provider_root or provider_root == "none":
            errors.append(f"{reference} enables provider {provider!r} without an assetRoot")
        elif not (SKILL_DIR / provider_root).exists():
            errors.append(f"{reference} enables provider {provider!r} with missing root {provider_root!r}")
        if manifest and manifest != "none" and not (SKILL_DIR / manifest).exists():
            errors.append(f"{reference} enables provider {provider!r} with missing manifest {manifest!r}")

    return errors


def validate() -> list[str]:
    errors: list[str] = []
    if not REGISTRY.exists():
        return [f"missing registry: {REGISTRY.relative_to(ROOT)}"]

    rows = parse_registry()
    if not rows:
        return ["style_registry.md contains no registry rows"]

    expected_columns = {
        "style",
        "reference",
        "aliases",
        "domain cues",
        "medium cues",
        "priority",
        "asset root",
        "use when",
    }
    missing_columns = expected_columns - set(rows[0].keys())
    if missing_columns:
        errors.append("style_registry.md missing columns: " + ", ".join(sorted(missing_columns)))

    seen: set[str] = set()
    for row in rows:
        style = strip_code(row.get("style", ""))
        if style in seen:
            errors.append(f"duplicate style registry entry: {style}")
            continue
        seen.add(style)
        errors.extend(validate_style(row))

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Style validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Style validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
