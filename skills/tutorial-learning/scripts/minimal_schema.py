#!/usr/bin/env python3
"""Validate the JSON Schema subset used by tutorial-learning without dependencies."""
from __future__ import annotations

from typing import Any


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object": return isinstance(value, dict)
    if expected == "array": return isinstance(value, list)
    if expected == "string": return isinstance(value, str)
    if expected == "boolean": return isinstance(value, bool)
    if expected == "integer": return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number": return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "null": return value is None
    return False


def _resolve_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported schema reference: {ref}")
    node: Any = root_schema
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or token not in node:
            raise ValueError(f"unresolved schema reference: {ref}")
        node = node[token]
    if not isinstance(node, dict):
        raise ValueError(f"schema reference does not resolve to an object: {ref}")
    return node


def validate_json_schema(instance: Any, schema: dict[str, Any], *, label: str = "$") -> list[str]:
    """Return errors for the intentionally small schema subset used in this skill."""
    errors: list[str] = []

    def visit(value: Any, rule: dict[str, Any], path: str) -> None:
        if "$ref" in rule:
            visit(value, _resolve_ref(schema, rule["$ref"]), path)
            return
        expected = rule.get("type")
        if expected and not _type_matches(value, expected):
            errors.append(f"{path}: expected {expected}, got {type(value).__name__}")
            return
        if "enum" in rule and value not in rule["enum"]:
            errors.append(f"{path}: value {value!r} is not one of {rule['enum']!r}")
        if isinstance(value, dict):
            properties = rule.get("properties", {})
            for key in rule.get("required", []):
                if key not in value:
                    errors.append(f"{path}: missing required property {key!r}")
            if rule.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        errors.append(f"{path}: unexpected property {key!r}")
            for key, child in properties.items():
                if key in value:
                    visit(value[key], child, f"{path}.{key}")
        if isinstance(value, list):
            if len(value) < rule.get("minItems", 0):
                errors.append(f"{path}: needs at least {rule['minItems']} items")
            if "maxItems" in rule and len(value) > rule["maxItems"]:
                errors.append(f"{path}: allows at most {rule['maxItems']} items")
            for index, child in enumerate(rule.get("prefixItems", [])):
                if index < len(value):
                    visit(value[index], child, f"{path}[{index}]")
            if "items" in rule:
                for index, item in enumerate(value):
                    visit(item, rule["items"], f"{path}[{index}]")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if "minimum" in rule and value < rule["minimum"]:
                errors.append(f"{path}: value {value} is below minimum {rule['minimum']}")
            if "maximum" in rule and value > rule["maximum"]:
                errors.append(f"{path}: value {value} is above maximum {rule['maximum']}")

    visit(instance, schema, label)
    return errors
