#!/usr/bin/env python3
"""Validate my-design-style concrete style conformance.

This checker is intentionally dependency-free so it can run in minimal Codex
skill environments. It validates framework-level contracts that can be checked
statically; visual quality remains a manual quality gate.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / "skills" / "my-design-style"
REFERENCES = SKILL_DIR / "references"
REGISTRY = REFERENCES / "style_registry.md"
STYLE_TEMPLATE = REFERENCES / "style_template.md"
ASSETS = SKILL_DIR / "assets"
REQUIRED_MANIFEST = "ASSET_MANIFEST.md"

REQUIRED_SECTIONS = [
    "Contract Conformance",
    "Triggers",
    "Intent",
    "Creative Latitude",
    "Color Tokens",
    "Typography",
    "Layout Principles",
    "PPT Slide Archetypes",
    "Visual Rhythm System",
    "Web Translation",
    "App / Dashboard Translation",
    "Static Visual Translation",
    "Asset Interface",
    "Surface Texture Policy",
    "Asset Rules",
    "Modifier Compatibility",
    "Preview Option Sets",
    "Self-Check",
]

REQUIRED_PROVIDER_METADATA = [
    "assetRoot",
    "manifestFile",
    "indexFile",
    "provenanceFile",
    "defaultToken",
    "allowedTokens",
    "opacityRange",
    "allowedSurfaces",
    "protectedSurfaces",
    "fallbackPolicy",
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
    if value.endswith("."):
        value = value[:-1].strip()
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


def parse_markdown_list(value: str | None) -> list[str] | None:
    if value is None:
        return None
    value = value.strip()
    if value == "[]":
        return []
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return None
    if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
        return parsed
    return None


def parse_number_pair(value: str | None) -> list[int | float] | None:
    if value is None:
        return None
    try:
        parsed = ast.literal_eval(value.strip())
    except (SyntaxError, ValueError):
        return None
    if (
        isinstance(parsed, list)
        and len(parsed) == 2
        and all(isinstance(item, (int, float)) for item in parsed)
        and parsed[0] <= parsed[1]
    ):
        return parsed
    return None


def validate_contract_conformance_docs() -> list[str]:
    errors: list[str] = []
    for path, section in [
        (STYLE_TEMPLATE, "Contract Conformance"),
        (REGISTRY, "Contract Conformance Requirement"),
    ]:
        if not path.exists():
            errors.append(f"missing contract file: {path.relative_to(ROOT)}")
            continue
        text = read(path)
        body = section_body(text, section)
        if not body:
            errors.append(f"{path.relative_to(ROOT)} is missing section: {section}")
            continue
        for required in [
            "DesignStyleBase",
            "Preview Option Sets",
            "Visual Rhythm System",
            "Self-Check",
        ]:
            if required not in body:
                errors.append(
                    f"{path.relative_to(ROOT)} {section} is missing {required}"
                )
    return errors


def validate_enabled_surface_policy(
    reference: str, policy: dict[str, str], allowed_tokens: list[str]
) -> list[str]:
    """Validate provider policy shape without inspecting provider asset contents.

    Asset bundles are intentionally opaque to the skill framework: users may add,
    remove, or replace files under assets/ for task-specific needs. The validator
    therefore checks only the contract fields declared in style references, not
    directory existence, manifests, index contents, file names, or checksums.
    """
    errors: list[str] = []
    provider = policy["provider"]
    default_token = policy.get("defaultToken", "")
    opacity_range = parse_number_pair(policy.get("opacityRange"))

    for key in ["assetRoot", "manifestFile", "indexFile", "provenanceFile"]:
        value = policy.get(key, "").strip()
        if not value:
            errors.append(f"{reference} enables provider {provider!r} without {key}")

    if not default_token or default_token == "none":
        errors.append(f"{reference} enables provider {provider!r} without defaultToken")
    elif default_token not in allowed_tokens:
        errors.append(f"{reference} defaultToken must be included in allowedTokens")
    if not allowed_tokens:
        errors.append(f"{reference} enables provider {provider!r} without allowedTokens")
    if not opacity_range or opacity_range == [0, 0]:
        errors.append(f"{reference} enables provider {provider!r} without a positive opacityRange")

    return errors


def validate_surface_policy(reference: str, surface_section: str) -> list[str]:
    errors: list[str] = []
    policy = {"provider": extract_bullet_value(surface_section, "provider") or ""}
    if not policy["provider"]:
        return [f"{reference} Surface Texture Policy is missing provider"]

    for key in REQUIRED_PROVIDER_METADATA:
        value = extract_bullet_value(surface_section, key)
        if value is None:
            errors.append(f"{reference} Surface Texture Policy is missing {key}")
        else:
            policy[key] = value

    allowed_tokens = parse_markdown_list(policy.get("allowedTokens"))
    if allowed_tokens is None:
        errors.append(f"{reference} allowedTokens must be a string list such as [] or [\"token\"]")
        allowed_tokens = []

    allowed_surfaces = parse_markdown_list(policy.get("allowedSurfaces"))
    if allowed_surfaces is None:
        errors.append(
            f"{reference} allowedSurfaces must be a string list such as [] or [\"surface\"]"
        )

    protected_surfaces = parse_markdown_list(policy.get("protectedSurfaces"))
    if protected_surfaces is None:
        errors.append(
            f"{reference} protectedSurfaces must be a string list such as [] or [\"surface\"]"
        )

    fallback_policy = policy.get("fallbackPolicy", "").strip()
    if not fallback_policy:
        errors.append(f"{reference} fallbackPolicy must describe the texture fallback behavior")

    opacity_range = parse_number_pair(policy.get("opacityRange"))
    if opacity_range is None:
        errors.append(f"{reference} opacityRange must be a number pair such as [0, 0]")

    provider = policy["provider"]
    if provider == "none":
        expected_disabled = {
            "assetRoot": "none",
            "manifestFile": "none",
            "indexFile": "none",
            "provenanceFile": "none",
            "defaultToken": "none",
            "allowedTokens": "[]",
            "opacityRange": "[0, 0]",
            "allowedSurfaces": "[]",
            "protectedSurfaces": "[]",
        }
        for key, expected in expected_disabled.items():
            if policy.get(key) != expected:
                errors.append(f"{reference} disabled texture policy must set {key}: {expected}")
    else:
        errors.extend(validate_enabled_surface_policy(reference, policy, allowed_tokens))

    return errors


def expected_asset_root(style: str) -> str:
    return f"assets/{style}/"


def validate_asset_boundary(style: str, asset_root: str, reference: str) -> list[str]:
    """Verify required style asset boundary exists without inspecting file inventories."""
    errors: list[str] = []
    expected = expected_asset_root(style)

    if asset_root == "none":
        errors.append(
            f"{reference} registry asset root must be {expected!r}, not 'none'"
        )
        return errors

    if asset_root != expected:
        errors.append(
            f"{reference} registry asset root {asset_root!r} must equal {expected!r}"
        )

    asset_dir = ASSETS / style
    if not asset_dir.is_dir():
        errors.append(
            f"{style} missing required asset directory: assets/{style}/"
        )

    manifest = asset_dir / REQUIRED_MANIFEST
    if asset_dir.is_dir() and not manifest.is_file():
        errors.append(
            f"{style} missing required manifest: assets/{style}/{REQUIRED_MANIFEST}"
        )

    return errors


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

    if "ok" not in text or "issues" not in text or "requiredFixes" not in text:
        errors.append(f"{reference} Self-Check must expose ok, issues, and requiredFixes")

    asset_section = section_body(text, "Asset Interface")
    surface_section = section_body(text, "Surface Texture Policy")
    modifier_section = section_body(text, "Modifier Compatibility")
    rhythm_section = section_body(text, "Visual Rhythm System")

    declared_asset_root = extract_bullet_value(asset_section, "assetRoot")
    if declared_asset_root is None:
        errors.append(f"{reference} Asset Interface is missing assetRoot")
    elif declared_asset_root != asset_root:
        errors.append(
            f"{reference} assetRoot {declared_asset_root!r} does not match registry {asset_root!r}"
        )

    errors.extend(validate_asset_boundary(style, asset_root, reference))

    # Bundled file inventories are runtime inputs that may be customized by users;
    # framework validation only checks required boundary shape plus
    # registry/reference agreement on the declared handle.

    for required_rhythm_key in [
        "rhythmScope",
        "visualAnchorRule",
        "archetypeVarietyRule",
        "motifRotation",
        "assetFallbackRule",
        "variationCheck",
    ]:
        if required_rhythm_key not in rhythm_section:
            errors.append(f"{reference} Visual Rhythm System is missing {required_rhythm_key}")

    if "acceptsModifiers" not in modifier_section:
        errors.append(f"{reference} Modifier Compatibility is missing acceptsModifiers")
    if "conflictPolicy" not in modifier_section:
        errors.append(f"{reference} Modifier Compatibility is missing conflictPolicy")
    if "promotionPolicy" not in modifier_section:
        errors.append(f"{reference} Modifier Compatibility is missing promotionPolicy")

    errors.extend(validate_surface_policy(reference, surface_section))

    return errors


def validate() -> list[str]:
    errors: list[str] = []
    if not REGISTRY.exists():
        return [f"missing registry: {REGISTRY.relative_to(ROOT)}"]

    errors.extend(validate_contract_conformance_docs())

    rows = parse_registry()
    if not rows:
        return errors + ["style_registry.md contains no registry rows"]

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
