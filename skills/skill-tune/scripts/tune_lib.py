#!/usr/bin/env python3
"""Shared library for skill-tune orchestration (no third-party deps)."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKILL_TUNE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_THRESHOLD = 5
SCORE_MIN = 1
SCORE_MAX = 5

FORBIDDEN_PATH_MARKERS = (
    ".cursor/skills-cursor",
    "skills-cursor",
    f"{Path('skills') / '.system'}",
    "/.system/",
    "\\.system\\",
    "node_modules",
    "plugin-cache",
    "vendor_imports",
)

FORBIDDEN_NAME_PARTS = (".system",)


@dataclass
class ResolvedTarget:
    ok: bool
    name: str = ""
    askill_dir: Path | None = None
    skill_md: Path | None = None
    skills_root: Path | None = None
    error: str = ""


@dataclass
class RubricDimension:
    id: str
    label: str = ""
    excellent_threshold: int = DEFAULT_THRESHOLD


@dataclass
class ActiveRubric:
    rubric_id: str
    source_path: str
    excellence_gate: str = "all_dimensions"
    dimensions: list[RubricDimension] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rubricId": self.rubric_id,
            "sourcePath": self.source_path,
            "excellenceGate": self.excellence_gate,
            "dimensions": [
                {
                    "id": d.id,
                    "label": d.label,
                    "excellentThreshold": d.excellent_threshold,
                }
                for d in self.dimensions
            ],
            "dimensionIds": [d.id for d in self.dimensions],
        }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def find_skills_root(start: Path | None = None) -> Path | None:
    cur = (start or SKILL_TUNE_ROOT).resolve()
    for parent in [cur, *cur.parents]:
        skills = parent / "skills"
        if (skills / "meta-skill" / "SKILL.md").is_file():
            return skills
        if parent.name == "skills" and (parent / "skill-tune" / "SKILL.md").is_file():
            return parent
    return None


def normalize_target_name(target: str) -> str:
    t = target.strip().replace("\\", "/")
    if t.endswith("/"):
        t = t[:-1]
    if "/" in t:
        t = t.split("/")[-1]
    return t


def resolve_target(target: str, skills_root: Path | None = None) -> ResolvedTarget:
    root = skills_root or find_skills_root()
    if root is None:
        return ResolvedTarget(False, error="skills root not found; pass --skills-root")

    raw = target.strip()
    resolved = (raw if Path(raw).is_absolute() else (root / raw)).resolve()
    raw_posix = raw.replace("\\", "/").lower()
    resolved_posix = str(resolved).replace("\\", "/").lower()

    for marker in FORBIDDEN_PATH_MARKERS:
        if marker.replace("\\", "/").lower() in raw_posix:
            return ResolvedTarget(False, error=f"forbidden path marker: {marker}")
        if marker.replace("\\", "/").lower() in resolved_posix:
            return ResolvedTarget(False, error=f"resolved path hits forbidden marker: {marker}")

    name = normalize_target_name(raw)
    if any(part in name for part in FORBIDDEN_NAME_PARTS):
        return ResolvedTarget(False, error=f"forbidden skill name segment: {name}")

    if resolved.is_dir() and (resolved / "SKILL.md").is_file():
        askill_dir = resolved
        name = resolved.name
    else:
        askill_dir = (root / name).resolve()

    if not askill_dir.is_dir():
        return ResolvedTarget(False, error=f"skill directory not found: {askill_dir}")
    skill_md = askill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ResolvedTarget(False, error=f"missing SKILL.md: {skill_md}")

    try:
        askill_dir.relative_to(root.resolve())
    except ValueError:
        return ResolvedTarget(
            False,
            error=f"skill must live under skills root {root}, got {askill_dir}",
        )

    return ResolvedTarget(
        True,
        name=name,
        askill_dir=askill_dir,
        skill_md=skill_md,
        skills_root=root.resolve(),
    )


def _parse_rubric_meta(text: str) -> tuple[str, str]:
    rubric_id = "default_rubric"
    gate = "all_dimensions"
    if "## Rubric meta" not in text:
        return rubric_id, gate
    section = text.split("## Rubric meta", 1)[1].split("\n## ", 1)[0]
    for line in section.splitlines():
        if line.strip().lower().startswith("rubric_id:"):
            rubric_id = line.split(":", 1)[1].strip()
        if line.strip().lower().startswith("excellence_gate:"):
            gate = line.split(":", 1)[1].strip()
    return rubric_id, gate


def _parse_markdown_table(section: str) -> tuple[list[str], list[list[str]]]:
    lines = [ln for ln in section.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    headers = [h.strip().strip("`").lower() for h in lines[0].strip("|").split("|")]
    rows: list[list[str]] = []
    for line in lines[2:]:
        if re.match(r"^\|\s*[-:]+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        rows.append(cells[: len(headers)])
    return headers, rows


def _threshold_from_row(headers: list[str], cells: list[str]) -> int:
    for key in ("threshold", "excellent threshold", "excellent_threshold"):
        if key in headers:
            idx = headers.index(key)
            raw = cells[idx].strip()
            if raw.isdigit():
                return int(raw)
    return DEFAULT_THRESHOLD


def _id_from_row(headers: list[str], cells: list[str]) -> str | None:
    if "id" not in headers:
        return None
    idx = headers.index("id")
    raw = cells[idx].strip().strip("`")
    if re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", raw):
        return raw
    return None


def parse_rubric_file(path: Path) -> ActiveRubric:
    text = read_text(path)
    rubric_id, gate = _parse_rubric_meta(text)
    if path.name == "tune_rubric.md" and rubric_id == "default_rubric":
        rubric_id = "tune_rubric"
    if "## Dimensions" not in text:
        raise ValueError(f"no ## Dimensions section in {path}")
    section = text.split("## Dimensions", 1)[1]
    if "\n## " in section:
        section = section.split("\n## ", 1)[0]
    headers, rows = _parse_markdown_table(section)
    if not headers or "id" not in headers:
        raise ValueError(f"Dimensions table missing ID column in {path}")
    dimensions: list[RubricDimension] = []
    label_idx = headers.index("what to score") if "what to score" in headers else None
    for cells in rows:
        dim_id = _id_from_row(headers, cells)
        if not dim_id:
            continue
        label = cells[label_idx] if label_idx is not None else ""
        threshold = _threshold_from_row(headers, cells)
        dimensions.append(
            RubricDimension(id=dim_id, label=label, excellent_threshold=threshold)
        )
    if not dimensions:
        raise ValueError(f"no dimensions parsed from {path}")
    return ActiveRubric(
        rubric_id=rubric_id,
        source_path=str(path.resolve()),
        excellence_gate=gate,
        dimensions=dimensions,
    )


def resolve_rubric(
    askill_dir: Path,
    skill_tune_root: Path | None = None,
    rubric_path: Path | None = None,
) -> ActiveRubric:
    root = skill_tune_root or SKILL_TUNE_ROOT
    if rubric_path and rubric_path.is_file():
        return parse_rubric_file(rubric_path.resolve())
    per_skill = askill_dir / "references" / "tune_rubric.md"
    if per_skill.is_file():
        return parse_rubric_file(per_skill)
    default = root / "references" / "default_rubric.md"
    if not default.is_file():
        raise FileNotFoundError(f"default rubric missing: {default}")
    return parse_rubric_file(default)


def parse_log_dimension_ids(log_path: Path) -> list[str] | None:
    for line in read_text(log_path).splitlines():
        if line.strip().lower().startswith("| rubric dimensions |"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                return [x.strip() for x in parts[1].split(",") if x.strip()]
    return None


def purpose_excerpt(skill_md: Path) -> str:
    body = read_text(skill_md)
    if body.startswith("---\n"):
        try:
            _, _, body = body.split("---\n", 2)
        except ValueError:
            pass
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped[:200]
    return ""


def build_judge_packet(
    scenario: str,
    out_text: str,
    rubric: ActiveRubric,
    judge_role: str = "product_manager",
    expected_artifact_type: str | None = None,
) -> str:
    lines = [
        "# Judge packet",
        "",
        "Do not include Askill SKILL.md or production chat.",
        "",
        f"## Judge role\n{judge_role}",
        "",
        "## User scenario",
        scenario.strip(),
        "",
        "## Expected artifact type (scenario only)",
        (expected_artifact_type or "not specified").strip(),
        "",
        "## Rubric",
        "",
        "| ID | Threshold | What to score |",
        "| --- | --- | --- |",
    ]
    for d in rubric.dimensions:
        label = d.label.replace("|", "\\|")
        lines.append(f"| `{d.id}` | {d.excellent_threshold} | {label} |")
    lines.extend(
        [
            "",
            "Score each dimension 1-5. Excellent means score >= Threshold.",
            "Set overall to pass_excellent only if EVERY dimension is excellent.",
            "",
            "## Deliverable (out)",
            "",
            out_text.strip(),
            "",
            "## Output format",
            "",
            "Write judge_result.json matching references/tune_contract.md (JSON preferred).",
        ]
    )
    return "\n".join(lines) + "\n"


def load_judge_result(path: Path) -> dict[str, Any]:
    text = read_text(path)
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = _parse_minimal_yaml(text)
    if not isinstance(data, dict):
        raise ValueError("judge result root must be an object")
    return data


def _parse_minimal_yaml(text: str) -> dict[str, Any]:
    """Restricted YAML subset for judge_result.yaml only."""
    root: dict[str, Any] = {}
    current_list: list[Any] | None = None
    current_key: str | None = None
    indent_stack: list[tuple[int, Any]] = []

    def set_nested(target: dict[str, Any], key: str, value: Any) -> None:
        target[key] = value

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        if re.match(r"^\s*-\s+", line) and current_list is not None:
            item: dict[str, Any] = {}
            m = re.match(r"^\s*-\s+(\w+):\s*(.*)$", line)
            if m:
                item[m.group(1)] = _coerce_scalar(m.group(2))
                j = i + 1
                while j < len(lines):
                    m2 = re.match(r"^\s{2,}(\w+):\s*(.*)$", lines[j])
                    if not m2:
                        break
                    item[m2.group(1)] = _coerce_scalar(m2.group(2))
                    j += 1
                current_list.append(item)
                i = j
                continue
            i += 1
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                if i + 1 < len(lines) and lines[i + 1].strip().startswith("- "):
                    current_list = []
                    root[key] = current_list
                    current_key = key
                elif i + 1 < len(lines) and re.match(r"^\s+\w+:", lines[i + 1]):
                    nested: dict[str, Any] = {}
                    root[key] = nested
                    j = i + 1
                    while j < len(lines):
                        m2 = re.match(r"^\s{2}(\w+):\s*(.*)$", lines[j])
                        if not m2:
                            break
                        nested[m2.group(1)] = _coerce_scalar(m2.group(2))
                        j += 1
                    i = j
                    continue
            else:
                root[key] = _coerce_scalar(val)
                current_list = None
            i += 1
            continue
        m = re.match(r"^\s{2}(\w+):\s*(.*)$", line)
        if m and isinstance(root.get(current_key or ""), dict):
            cast = root[current_key]  # type: ignore[index]
            if isinstance(cast, dict):
                cast[m.group(1)] = _coerce_scalar(m.group(2))
        i += 1
    return root


def _coerce_scalar(raw: str) -> Any:
    raw = raw.strip().strip('"').strip("'")
    if raw.lower() in ("true", "false"):
        return raw.lower() == "true"
    if re.match(r"^-?\d+$", raw):
        return int(raw)
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip('"').strip("'") for p in inner.split(",")]
    return raw


def validate_judge_result(
    result: dict[str, Any],
    rubric: ActiveRubric,
    out_text: str,
) -> list[str]:
    errors: list[str] = []
    dim_ids = [d.id for d in rubric.dimensions]
    expected_thresholds = {d.id: d.excellent_threshold for d in rubric.dimensions}

    for field_name in (
        "round",
        "rubricId",
        "dimensionIds",
        "judgeRole",
        "isolatedJudge",
        "scores",
        "thresholds",
        "overall",
        "findings",
        "priorityFixes",
    ):
        if field_name not in result:
            errors.append(f"missing field: {field_name}")

    rnd = result.get("round")
    if not isinstance(rnd, int) or isinstance(rnd, bool) or rnd < 1:
        errors.append("round must be a positive integer")

    isolated = result.get("isolatedJudge")
    if not isinstance(isolated, bool):
        errors.append("isolatedJudge must be boolean true or false")

    priority_fixes: Any = result.get("priorityFixes")
    if not isinstance(priority_fixes, list):
        errors.append("priorityFixes must be a list")
    elif priority_fixes and not all(isinstance(x, str) and x.strip() for x in priority_fixes):
        errors.append("priorityFixes must be non-empty strings")

    if result.get("rubricId") != rubric.rubric_id:
        errors.append(
            f"rubricId mismatch: {result.get('rubricId')!r} != {rubric.rubric_id!r}"
        )

    result_dims = result.get("dimensionIds")
    if not isinstance(result_dims, list) or result_dims != dim_ids:
        errors.append(f"dimensionIds must equal {dim_ids!r}")

    scores = result.get("scores")
    thresholds = result.get("thresholds")
    if not isinstance(scores, dict):
        errors.append("scores must be an object")
        scores = {}
    if not isinstance(thresholds, dict):
        errors.append("thresholds must be an object")
        thresholds = {}

    for dim_id in dim_ids:
        if dim_id not in scores:
            errors.append(f"scores missing dimension {dim_id!r}")
        if dim_id not in thresholds:
            errors.append(f"thresholds missing dimension {dim_id!r}")
        if dim_id in scores:
            score = scores[dim_id]
            if not isinstance(score, int) or not (SCORE_MIN <= score <= SCORE_MAX):
                errors.append(f"scores[{dim_id!r}] must be int {SCORE_MIN}-{SCORE_MAX}")
        if dim_id in thresholds:
            th = thresholds[dim_id]
            if not isinstance(th, int):
                errors.append(f"thresholds[{dim_id!r}] must be int")
            elif th != expected_thresholds[dim_id]:
                errors.append(
                    f"thresholds[{dim_id!r}]={th} != rubric excellentThreshold "
                    f"{expected_thresholds[dim_id]}"
                )

    overall = result.get("overall")
    if overall not in ("fail", "pass_excellent"):
        errors.append("overall must be fail or pass_excellent")

    if not errors and isinstance(scores, dict) and isinstance(thresholds, dict):
        all_excellent = all(
            isinstance(scores.get(d), int)
            and isinstance(thresholds.get(d), int)
            and scores[d] >= thresholds[d]
            for d in dim_ids
        )
        if overall == "pass_excellent" and not all_excellent:
            errors.append("overall pass_excellent but scores below thresholds")
        if overall == "fail" and all_excellent:
            errors.append("overall fail but all dimensions meet thresholds")

    findings = result.get("findings")
    low_score_findings = 0
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    else:
        for idx, item in enumerate(findings):
            if not isinstance(item, dict):
                errors.append(f"findings[{idx}] must be an object")
                continue
            dim = item.get("dimension")
            if dim not in dim_ids:
                errors.append(f"findings[{idx}] unknown dimension {dim!r}")
                continue
            f_score = item.get("score")
            if dim in scores and isinstance(f_score, int) and f_score != scores[dim]:
                errors.append(
                    f"findings[{idx}] score {f_score} != scores[{dim!r}] {scores[dim]}"
                )
            if (
                dim in scores
                and dim in thresholds
                and isinstance(scores[dim], int)
                and isinstance(thresholds[dim], int)
                and scores[dim] < thresholds[dim]
            ):
                low_score_findings += 1
            quote = item.get("evidenceQuote", "")
            if quote and isinstance(quote, str):
                if quote not in out_text:
                    errors.append(
                        f"findings[{idx}] evidenceQuote not found in out text"
                    )

    if overall == "fail":
        if isinstance(priority_fixes, list) and len(priority_fixes) == 0:
            errors.append("priorityFixes must be non-empty when overall is fail")
        if low_score_findings == 0 and not errors:
            errors.append(
                "overall fail requires at least one finding for a below-threshold dimension"
            )

    if overall == "pass_excellent" and isinstance(findings, list) and findings:
        for idx, item in enumerate(findings):
            if isinstance(item, dict) and item.get("gap"):
                errors.append(
                    f"findings[{idx}] should not have gaps when overall is pass_excellent"
                )

    role = result.get("judgeRole")
    if role not in ("product_manager", "creator"):
        errors.append("judgeRole must be product_manager or creator")

    return errors


def session_root(askill_dir: Path, session_id: str) -> Path:
    return askill_dir / "tune_sessions" / session_id


def session_state_path(askill_dir: Path, session_id: str) -> Path:
    return session_root(askill_dir, session_id) / "session_state.json"


def round_dir(askill_dir: Path, session_id: str, round_n: int) -> Path:
    return session_root(askill_dir, session_id) / f"round-{round_n:03d}"


def load_session_state(askill_dir: Path, session_id: str) -> dict[str, Any]:
    path = session_state_path(askill_dir, session_id)
    if not path.is_file():
        raise FileNotFoundError(f"session state not found: {path}")
    return json.loads(read_text(path))


def save_session_state(askill_dir: Path, session_id: str, state: dict[str, Any]) -> None:
    write_text(session_state_path(askill_dir, session_id), json.dumps(state, indent=2) + "\n")


def load_improve_record(round_dir: Path) -> dict[str, Any] | None:
    path = round_dir / "improve_record.json"
    if path.is_file():
        data = json.loads(read_text(path))
        if isinstance(data, dict):
            return data
    return None


def write_improve_record(round_dir: Path, record: dict[str, Any]) -> Path:
    path = round_dir / "improve_record.json"
    write_text(path, json.dumps(record, indent=2) + "\n")
    return path


def init_round_dir(askill_dir: Path, session_id: str, round_n: int) -> Path:
    rd = round_dir(askill_dir, session_id, round_n)
    rd.mkdir(parents=True, exist_ok=True)
    return rd


def write_round_manifest(
    rd: Path,
    scenario: str,
    files: dict[str, str],
) -> Path:
    manifest = {
        "scenario": scenario,
        "artifacts": files,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    path = rd / "manifest.json"
    write_text(path, json.dumps(manifest, indent=2) + "\n")
    return path


def init_self_iter_log(
    log_path: Path,
    askill_name: str,
    rubric: ActiveRubric,
    purpose: str,
) -> None:
    if log_path.is_file():
        return
    dim_csv = ", ".join(d.id for d in rubric.dimensions)
    started = datetime.now(timezone.utc).date().isoformat()
    content = f"""# Self-iteration log: {askill_name}

| Field | Value |
| --- | --- |
| Skill path | skills/{askill_name}/ |
| Rubric | {rubric.rubric_id} |
| Rubric dimensions | {dim_csv} |
| Started | {started} |
| Purpose excerpt | {purpose} |

---
"""
    write_text(log_path, content)


def append_log(
    log_path: Path,
    round_n: int,
    scenario: str,
    judge_role: str,
    isolated: bool,
    result: dict[str, Any],
    rubric: ActiveRubric,
    round_artifact_dir: Path,
    out_summary: str,
    improve: dict[str, Any] | None = None,
) -> None:
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    overall = result.get("overall", "fail")
    scores = result.get("scores", {})
    thresholds = result.get("thresholds", {})

    lines = [
        f"## Round {round_n}",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Timestamp | {ts} |",
        f"| Scenario | {scenario} |",
        f"| Judge role | {judge_role} |",
        f"| Isolated judge | {'yes' if isolated else 'no'} |",
        f"| Overall | {overall} |",
        f"| Artifact dir | {round_artifact_dir.as_posix()} |",
        "",
        "### Scores",
        "",
        "| Dimension | Score | Excellent threshold |",
        "| --- | --- | --- |",
    ]
    for d in rubric.dimensions:
        lines.append(
            f"| {d.id} | {scores.get(d.id, '')} | {thresholds.get(d.id, d.excellent_threshold)} |"
        )
    lines.extend(["", "### Findings", ""])
    findings = result.get("findings") or []
    if overall == "pass_excellent" and not findings:
        lines.append("- All dimensions met excellent threshold.")
    else:
        for item in findings:
            if not isinstance(item, dict):
                continue
            dim = item.get("dimension", "")
            score = item.get("score", "")
            gap = item.get("gap", "")
            quote = item.get("evidenceQuote", "")
            lines.append(f"- **{dim} ({score})**: {gap}")
            if quote:
                lines.append(f'  - Evidence: "{quote}"')

    lines.extend(["", "### Priority fixes", ""])
    fixes = result.get("priorityFixes") or []
    if overall == "pass_excellent":
        lines.append("None - excellence gate passed.")
    else:
        for i, fix in enumerate(fixes, 1):
            lines.append(f"{i}. {fix}")

    manifest_path = round_artifact_dir / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(read_text(manifest_path))
        artifacts = manifest.get("artifacts", {})
        lines.extend(["", "### Artifacts", ""])
        for name, meta in artifacts.items():
            if isinstance(meta, dict):
                lines.append(
                    f"- {name}: `{meta.get('path', '')}` sha256 `{meta.get('sha256', '')}`"
                )
            else:
                lines.append(f"- {name}: `{meta}`")

    lines.extend(
        [
            "",
            "### Output (out)",
            "",
            f"- Summary: {out_summary}",
            "",
            "### Improve",
            "",
        ]
    )
    if overall == "pass_excellent":
        lines.append("None - excellence gate passed; no Askill edits this round.")
    elif overall == "fail" and improve:
        touched = improve.get("filesTouched") or improve.get("files_touched") or []
        hypothesis = improve.get("hypothesis", "")
        generalized = improve.get("generalizedFrom") or improve.get("generalized_from") or ""
        lines.extend(
            [
                "| Field | Value |",
                "| --- | --- |",
                f"| Files touched | {', '.join(touched)} |",
                f"| Hypothesis | {hypothesis} |",
            ]
        )
        if generalized:
            lines.append(f"| Generalized from | {generalized} |")
        lines.append("")
        for bullet in improve.get("changesSummary") or improve.get("changes_summary") or []:
            lines.append(f"- {bullet}")
    elif overall == "fail":
        lines.append(
            "Pending - round failed; improve_record.json missing under artifact dir."
        )

    lines.extend(["", "---", ""])
    existing = read_text(log_path) if log_path.is_file() else ""
    write_text(log_path, existing + "\n".join(lines))


def append_session_end(
    log_path: Path,
    status: str,
    rounds_completed: int,
    remaining_gaps: str = "none",
    next_scenario: str = "",
) -> None:
    if status not in ("excellent", "capped", "aborted"):
        raise ValueError("status must be excellent, capped, or aborted")
    block = f"""
## Session end

| Field | Value |
| --- | --- |
| Status | {status} |
| Rounds completed | {rounds_completed} |
| Remaining gaps | {remaining_gaps} |
| Next scenario suggestion | {next_scenario or "none"} |

---
"""
    existing = read_text(log_path) if log_path.is_file() else ""
    if "## Session end" in existing:
        return
    write_text(log_path, existing + block)


def remaining_gaps_from_result(result: dict[str, Any]) -> str:
    parts: list[str] = []
    for item in result.get("findings") or []:
        if isinstance(item, dict) and item.get("gap"):
            dim = item.get("dimension", "")
            parts.append(f"{dim}: {item.get('gap')}")
    return "; ".join(parts) if parts else "none"


def complete_round(
    askill_dir: Path,
    session_id: str,
    round_n: int,
    *,
    out_summary: str,
    require_improve_on_fail: bool = True,
) -> dict[str, Any]:
    """Validate judge, record artifacts, append log, update session; return status payload."""
    state = load_session_state(askill_dir, session_id)
    rd = round_dir(askill_dir, session_id, round_n)
    if not rd.is_dir():
        raise FileNotFoundError(f"round directory not found: {rd}")

    out_path = rd / "out.md"
    result_path = rd / "judge_result.json"
    rubric_path = rd / "active_rubric.json"
    if not out_path.is_file():
        raise FileNotFoundError(f"missing out.md in {rd}")
    if not result_path.is_file():
        raise FileNotFoundError(f"missing judge_result.json in {rd}")
    if not rubric_path.is_file():
        rubric_path = session_root(askill_dir, session_id) / "active_rubric.json"
    if not rubric_path.is_file():
        rubric = resolve_rubric(askill_dir, SKILL_TUNE_ROOT, None)
        write_text(rd / "active_rubric.json", json.dumps(rubric.to_dict(), indent=2) + "\n")
        rubric_path = rd / "active_rubric.json"

    rubric = _rubric_from_dict(json.loads(read_text(rubric_path)))
    out_text = read_text(out_path)
    result = load_judge_result(result_path)
    errors = validate_judge_result(result, rubric, out_text)
    if errors:
        raise ValueError("judge result validation failed: " + "; ".join(errors))

    packet_path = rd / "judge_packet.md"
    if not packet_path.is_file():
        scenario = state.get("scenario", "")
        packet = build_judge_packet(
            scenario,
            out_text,
            rubric,
            judge_role=state.get("judgeRole", "product_manager"),
            expected_artifact_type=state.get("expectedArtifactType"),
        )
        write_text(packet_path, packet)

    manifest_path = rd / "manifest.json"
    artifacts: dict[str, Any] = {}
    if manifest_path.is_file():
        artifacts = json.loads(read_text(manifest_path)).get("artifacts", {})
    for name, path in (
        ("out.md", out_path),
        ("judge_packet.md", packet_path),
        ("judge_result.json", result_path),
    ):
        if path.is_file():
            artifacts[name] = {"path": str(path.resolve()), "sha256": sha256_file(path)}
    write_round_manifest(rd, state.get("scenario", ""), artifacts)

    overall = result.get("overall", "fail")
    improve = load_improve_record(rd) if overall == "fail" else None
    if overall == "fail" and require_improve_on_fail and improve is None:
        raise FileNotFoundError(
            f"overall fail requires improve_record.json in {rd} (run record-improve first)"
        )

    log_path = Path(state["logPath"])
    if not log_path.is_file():
        init_self_iter_log(
            log_path,
            askill_dir.name,
            rubric,
            state.get("purposeExcerpt", purpose_excerpt(askill_dir / "SKILL.md")),
        )

    append_log(
        log_path,
        round_n,
        state.get("scenario", ""),
        result.get("judgeRole", state.get("judgeRole", "product_manager")),
        bool(result.get("isolatedJudge", True)),
        result,
        rubric,
        rd,
        out_summary,
        improve,
    )

    completed = list(state.get("completedRounds") or [])
    if round_n not in completed:
        completed.append(round_n)
    state["completedRounds"] = sorted(completed)
    state["currentRound"] = round_n
    state["lastOverall"] = overall
    save_session_state(askill_dir, session_id, state)

    payload: dict[str, Any] = {
        "ok": True,
        "round": round_n,
        "overall": overall,
        "roundDir": str(rd),
        "logPath": str(log_path),
    }

    max_rounds = int(state.get("maxRounds", 3))
    if overall == "pass_excellent":
        append_session_end(log_path, "excellent", round_n)
        state["status"] = "excellent"
        save_session_state(askill_dir, session_id, state)
        payload["sessionStatus"] = "excellent"
        payload["stop"] = True
    elif round_n >= max_rounds:
        gaps = remaining_gaps_from_result(result)
        append_session_end(log_path, "capped", round_n, gaps)
        state["status"] = "capped"
        save_session_state(askill_dir, session_id, state)
        payload["sessionStatus"] = "capped"
        payload["stop"] = True
        payload["remainingGaps"] = gaps
    else:
        payload["sessionStatus"] = "in_progress"
        payload["stop"] = False
        payload["nextRound"] = round_n + 1

    return payload


def _rubric_from_dict(data: dict[str, Any]) -> ActiveRubric:
    dims = [
        RubricDimension(
            id=d["id"],
            label=d.get("label", ""),
            excellent_threshold=int(d.get("excellentThreshold", DEFAULT_THRESHOLD)),
        )
        for d in data.get("dimensions", [])
    ]
    return ActiveRubric(
        rubric_id=data.get("rubricId", "default_rubric"),
        source_path=data.get("sourcePath", ""),
        excellence_gate=data.get("excellenceGate", "all_dimensions"),
        dimensions=dims,
    )


def init_session(
    target: str,
    scenario: str,
    session_id: str,
    skills_root: Path | None = None,
    max_rounds: int = 3,
    judge_role: str = "product_manager",
    expected_artifact_type: str | None = None,
) -> dict[str, Any]:
    resolved = resolve_target(target, skills_root)
    if not resolved.ok or not resolved.askill_dir:
        raise ValueError(resolved.error or "target resolution failed")
    askill_dir = resolved.askill_dir
    rubric = resolve_rubric(askill_dir, SKILL_TUNE_ROOT, None)
    sroot = session_root(askill_dir, session_id)
    sroot.mkdir(parents=True, exist_ok=True)
    rubric_json = sroot / "active_rubric.json"
    write_text(rubric_json, json.dumps(rubric.to_dict(), indent=2) + "\n")
    log_path = askill_dir / "self-iter.md"
    purpose = purpose_excerpt(askill_dir / "SKILL.md")
    init_self_iter_log(log_path, askill_dir.name, rubric, purpose)
    state = {
        "targetSkill": resolved.name,
        "askillDir": str(askill_dir),
        "skillsRoot": str(resolved.skills_root),
        "scenario": scenario,
        "sessionId": session_id,
        "maxRounds": max_rounds,
        "currentRound": 1,
        "judgeRole": judge_role,
        "expectedArtifactType": expected_artifact_type or "",
        "rubricJsonPath": str(rubric_json),
        "logPath": str(log_path),
        "purposeExcerpt": purpose,
        "status": "in_progress",
        "completedRounds": [],
    }
    save_session_state(askill_dir, session_id, state)
    rd = init_round_dir(askill_dir, session_id, 1)
    write_text(rd / "active_rubric.json", read_text(rubric_json))
    return {
        "ok": True,
        "sessionId": session_id,
        "askillDir": str(askill_dir),
        "logPath": str(log_path),
        "rubricJson": str(rubric_json),
        "roundDir": str(rd),
        "round": 1,
    }
