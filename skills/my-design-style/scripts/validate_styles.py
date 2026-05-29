#!/usr/bin/env python3
"""Validate my-design-style concrete style conformance.

This checker is intentionally dependency-free so it can run in minimal Codex
skill environments. It validates framework-level contracts that can be checked
statically; visual quality remains a manual quality gate.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / "skills" / "my-design-style"
REFERENCES = SKILL_DIR / "references"
REGISTRY = REFERENCES / "style_registry.md"
STYLE_TEMPLATE = REFERENCES / "style_template.md"

REQUIRED_INTERFACES = [
    "TriggerMatcher",
    "DesignIntentProvider",
    "PaletteProvider",
    "TypographyProvider",
    "LayoutSystem",
    "ComponentTranslator",
    "AssetPolicy",
    "SurfaceTexturePolicy",
    "ModifierCompatibilityProvider",
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
    "Modifier Compatibility",
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


def validate_implementation_map_contracts() -> list[str]:
    errors: list[str] = []
    for path, section in [
        (STYLE_TEMPLATE, "Implementation Map"),
        (REGISTRY, "Implementation Map Requirement"),
    ]:
        if not path.exists():
            errors.append(f"missing contract file: {path.relative_to(ROOT)}")
            continue
        text = read(path)
        body = section_body(text, section)
        if not body:
            errors.append(f"{path.relative_to(ROOT)} is missing section: {section}")
            continue
        for interface in REQUIRED_INTERFACES:
            if f"`{interface}`" not in body:
                errors.append(
                    f"{path.relative_to(ROOT)} {section} is missing {interface}"
                )
        if path == STYLE_TEMPLATE and "`DesignStyleBase.getModifierCompatibility()`" not in body:
            errors.append(
                f"{path.relative_to(ROOT)} Implementation Map is missing DesignStyleBase.getModifierCompatibility()"
            )
    return errors


def load_provider_index(index_file: str) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    index_path = SKILL_DIR / index_file
    if not index_path.exists():
        return None, [f"provider index does not exist: {index_file}"]
    try:
        data = json.loads(read(index_path))
    except json.JSONDecodeError as exc:
        return None, [f"provider index is not valid JSON: {index_file}: {exc}"]
    textures = data.get("textures")
    if not isinstance(textures, list) or not textures:
        errors.append(f"provider index has no textures: {index_file}")
    return data, errors


def validate_provider_files(reference: str, policy: dict[str, str], allowed_tokens: list[str]) -> list[str]:
    errors: list[str] = []
    provider = policy["provider"]
    provider_root = policy.get("assetRoot", "")
    manifest = policy.get("manifestFile", "")
    index_file = policy.get("indexFile", "")
    provenance = policy.get("provenanceFile", "")

    for label, path_value in [
        ("assetRoot", provider_root),
        ("manifestFile", manifest),
        ("indexFile", index_file),
        ("provenanceFile", provenance),
    ]:
        if not path_value or path_value == "none":
            errors.append(f"{reference} enables provider {provider!r} without {label}")
            continue
        path = SKILL_DIR / path_value
        if label == "assetRoot":
            if not path.is_dir():
                errors.append(f"{reference} provider assetRoot is missing: {path_value}")
        elif not path.is_file():
            errors.append(f"{reference} provider {label} is missing: {path_value}")

    if errors:
        return errors

    index, index_errors = load_provider_index(index_file)
    errors.extend(f"{reference} {error}" for error in index_errors)
    if index is None:
        return errors

    textures = index.get("textures", [])
    by_token = {item.get("token"): item for item in textures if isinstance(item, dict)}
    for token in allowed_tokens + [policy.get("defaultToken", "")]:
        if token and token not in by_token:
            errors.append(f"{reference} references missing texture token: {token}")

    for token, item in by_token.items():
        for key in [
            "file",
            "sourceUrl",
            "sourceHomepage",
            "attribution",
            "licenseOrTerms",
            "sourceFormat",
            "sha256",
            "visualCharacter",
            "recommendedRoles",
            "defaultOpacity",
            "safePlacement",
        ]:
            if key not in item or item[key] in ("", None, []):
                errors.append(f"{reference} provider token {token!r} is missing {key}")
        file_value = item.get("file")
        if isinstance(file_value, str):
            item_path = SKILL_DIR / provider_root / file_value
            if not item_path.is_file():
                errors.append(f"{reference} provider token {token!r} file is missing: {file_value}")
            else:
                digest = hashlib.sha256(item_path.read_bytes()).hexdigest()
                if item.get("sha256") != digest:
                    errors.append(f"{reference} provider token {token!r} sha256 mismatch")
        default_opacity = item.get("defaultOpacity")
        if not (
            isinstance(default_opacity, list)
            and len(default_opacity) == 2
            and all(isinstance(value, (int, float)) for value in default_opacity)
            and default_opacity[0] <= default_opacity[1]
        ):
            errors.append(f"{reference} provider token {token!r} has invalid defaultOpacity")

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
        errors.append(f"{reference} allowedSurfaces must be a string list such as [] or [\"surface\"]")

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
        }
        for key, expected in expected_disabled.items():
            if policy.get(key) != expected:
                errors.append(f"{reference} disabled texture policy must set {key}: {expected}")
    else:
        if provider != "transparent_textures":
            errors.append(f"{reference} uses unsupported surface provider: {provider}")
        default_token = policy.get("defaultToken", "")
        if not default_token or default_token == "none":
            errors.append(f"{reference} enables provider {provider!r} without defaultToken")
        elif default_token not in allowed_tokens:
            errors.append(f"{reference} defaultToken must be included in allowedTokens")
        if not allowed_tokens:
            errors.append(f"{reference} enables provider {provider!r} without allowedTokens")
        if not opacity_range or opacity_range == [0, 0]:
            errors.append(f"{reference} enables provider {provider!r} without a positive opacityRange")
        errors.extend(validate_provider_files(reference, policy, allowed_tokens))

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

    implementation_map = section_body(text, "Implementation Map")
    for interface in REQUIRED_INTERFACES:
        if f"`{interface}`" not in implementation_map:
            errors.append(f"{reference} Implementation Map is missing {interface}")

    if "ok" not in text or "issues" not in text or "requiredFixes" not in text:
        errors.append(f"{reference} Self-Check must expose ok, issues, and requiredFixes")

    asset_section = section_body(text, "Asset Interface")
    surface_section = section_body(text, "Surface Texture Policy")
    modifier_section = section_body(text, "Modifier Compatibility")

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

    errors.extend(validate_implementation_map_contracts())

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
