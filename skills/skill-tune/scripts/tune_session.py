#!/usr/bin/env python3
"""CLI orchestration for skill-tune sessions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import tune_lib as lib  # noqa: E402


def _rubric_from_json(path: Path) -> lib.ActiveRubric:
    data = json.loads(lib.read_text(path))
    dims = [
        lib.RubricDimension(
            id=d["id"],
            label=d.get("label", ""),
            excellent_threshold=int(d.get("excellentThreshold", lib.DEFAULT_THRESHOLD)),
        )
        for d in data.get("dimensions", [])
    ]
    return lib.ActiveRubric(
        rubric_id=data.get("rubricId", "default_rubric"),
        source_path=data.get("sourcePath", str(path)),
        excellence_gate=data.get("excellenceGate", "all_dimensions"),
        dimensions=dims,
    )


def cmd_resolve_target(args: argparse.Namespace) -> int:
    root = Path(args.skills_root).resolve() if args.skills_root else None
    resolved = lib.resolve_target(args.target, root)
    if not resolved.ok:
        print(json.dumps({"ok": False, "error": resolved.error}, indent=2))
        return 1
    payload = {
        "ok": True,
        "name": resolved.name,
        "askillDir": str(resolved.askill_dir),
        "skillMd": str(resolved.skill_md),
        "skillsRoot": str(resolved.skills_root),
    }
    print(json.dumps(payload, indent=2))
    if args.write:
        lib.write_text(Path(args.write), json.dumps(payload, indent=2) + "\n")
    return 0


def cmd_resolve_rubric(args: argparse.Namespace) -> int:
    askill = Path(args.askill_dir).resolve()
    tune_root = Path(args.skill_tune_root).resolve() if args.skill_tune_root else lib.SKILL_TUNE_ROOT
    rubric_path = Path(args.rubric).resolve() if args.rubric else None
    try:
        rubric = lib.resolve_rubric(askill, tune_root, rubric_path)
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1
    data = rubric.to_dict()
    data["ok"] = True
    print(json.dumps(data, indent=2))
    if args.write:
        lib.write_text(Path(args.write), json.dumps(data, indent=2) + "\n")
    return 0


def cmd_build_judge_packet(args: argparse.Namespace) -> int:
    rubric = _rubric_from_json(Path(args.rubric_json))
    out_text = lib.read_text(Path(args.out_file))
    packet = lib.build_judge_packet(
        args.scenario,
        out_text,
        rubric,
        judge_role=args.judge_role,
        expected_artifact_type=args.expected_artifact_type or None,
    )
    out_path = Path(args.output)
    lib.write_text(out_path, packet)
    print(str(out_path))
    return 0


def cmd_validate_judge_result(args: argparse.Namespace) -> int:
    rubric = _rubric_from_json(Path(args.rubric_json))
    result = lib.load_judge_result(Path(args.result))
    out_text = lib.read_text(Path(args.out_file))
    errors = lib.validate_judge_result(result, rubric, out_text)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        return 1
    print(json.dumps({"ok": True}, indent=2))
    return 0


def cmd_init_round_dir(args: argparse.Namespace) -> int:
    askill = Path(args.askill_dir).resolve()
    rd = lib.init_round_dir(askill, args.session_id, int(args.round))
    out_src = Path(args.out_file).resolve()
    lib.write_text(rd / "out.md", lib.read_text(out_src))
    files: dict[str, dict[str, str]] = {
        "out.md": {
            "path": str((rd / "out.md").resolve()),
            "sha256": lib.sha256_file(rd / "out.md"),
        }
    }
    scenario = args.scenario or ""
    if scenario:
        lib.write_text(rd / "scenario.txt", scenario.strip() + "\n")
        files["scenario.txt"] = {
            "path": str((rd / "scenario.txt").resolve()),
            "sha256": lib.sha256_file(rd / "scenario.txt"),
        }
    if args.rubric_json:
        rpath = Path(args.rubric_json).resolve()
        if rpath.is_file():
            dest = rd / "active_rubric.json"
            lib.write_text(dest, lib.read_text(rpath))
            files["active_rubric.json"] = {
                "path": str(dest.resolve()),
                "sha256": lib.sha256_file(dest),
            }
    lib.write_round_manifest(rd, scenario, files)
    print(str(rd))
    return 0


def cmd_write_out(args: argparse.Namespace) -> int:
    rd = Path(args.round_dir).resolve()
    out_path = rd / "out.md"
    lib.write_text(out_path, lib.read_text(Path(args.out_file)))
    manifest_path = rd / "manifest.json"
    manifest = (
        json.loads(lib.read_text(manifest_path)) if manifest_path.is_file() else {"artifacts": {}}
    )
    artifacts = manifest.get("artifacts", {})
    artifacts["out.md"] = {
        "path": str(out_path.resolve()),
        "sha256": lib.sha256_file(out_path),
    }
    lib.write_round_manifest(rd, manifest.get("scenario", ""), artifacts)
    print(str(out_path))
    return 0


def cmd_record_judge_artifacts(args: argparse.Namespace) -> int:
    rd = Path(args.round_dir).resolve()
    lib.write_text(rd / "judge_packet.md", lib.read_text(Path(args.judge_packet)))
    result_src = Path(args.judge_result)
    result_dest = rd / "judge_result.json"
    if result_src.suffix.lower() == ".json":
        lib.write_text(result_dest, lib.read_text(result_src))
    else:
        data = lib.load_judge_result(result_src)
        lib.write_text(result_dest, json.dumps(data, indent=2) + "\n")
    manifest_path = rd / "manifest.json"
    manifest = (
        json.loads(lib.read_text(manifest_path)) if manifest_path.is_file() else {"artifacts": {}}
    )
    artifacts = manifest.get("artifacts", {})
    artifacts["judge_packet.md"] = {
        "path": str((rd / "judge_packet.md").resolve()),
        "sha256": lib.sha256_file(rd / "judge_packet.md"),
    }
    artifacts["judge_result.json"] = {
        "path": str(result_dest.resolve()),
        "sha256": lib.sha256_file(result_dest),
    }
    lib.write_round_manifest(rd, manifest.get("scenario", ""), artifacts)
    print(str(result_dest))
    return 0


def cmd_record_improve(args: argparse.Namespace) -> int:
    rd = Path(args.round_dir).resolve()
    summary_path = rd / "improve_summary.md"
    lib.write_text(summary_path, lib.read_text(Path(args.summary)))

    if args.record_json and Path(args.record_json).is_file():
        record = json.loads(lib.read_text(Path(args.record_json)))
    else:
        touched = [x.strip() for x in args.files_touched.split(",") if x.strip()]
        changes = [x.strip() for x in args.change if x.strip()]
        record = {
            "round": int(args.round) if args.round else 0,
            "filesTouched": touched,
            "changesSummary": changes,
            "hypothesis": args.hypothesis,
            "generalizedFrom": args.generalized_from,
        }
    record_path = lib.write_improve_record(rd, record)

    artifacts_update: dict[str, dict[str, str]] = {
        "improve_summary.md": {
            "path": str(summary_path.resolve()),
            "sha256": lib.sha256_file(summary_path),
        },
        "improve_record.json": {
            "path": str(record_path.resolve()),
            "sha256": lib.sha256_file(record_path),
        },
    }
    if args.patch and Path(args.patch).is_file():
        patch_dest = rd / "improve.patch"
        lib.write_text(patch_dest, lib.read_text(Path(args.patch)))
        artifacts_update["improve.patch"] = {
            "path": str(patch_dest.resolve()),
            "sha256": lib.sha256_file(patch_dest),
        }
    manifest_path = rd / "manifest.json"
    manifest = (
        json.loads(lib.read_text(manifest_path)) if manifest_path.is_file() else {"artifacts": {}}
    )
    artifacts = manifest.get("artifacts", {})
    artifacts.update(artifacts_update)
    lib.write_round_manifest(rd, manifest.get("scenario", ""), artifacts)
    print(json.dumps({"improveRecord": str(record_path), "summary": str(summary_path)}, indent=2))
    return 0


def cmd_append_log(args: argparse.Namespace) -> int:
    log_path = Path(args.log).resolve()
    askill_dir = Path(args.askill_dir).resolve()
    if args.rubric_json:
        rubric = _rubric_from_json(Path(args.rubric_json))
    else:
        rubric = lib.resolve_rubric(askill_dir, lib.SKILL_TUNE_ROOT, None)
    result = lib.load_judge_result(Path(args.judge_result))
    improve = None
    round_dir_path = Path(args.round_dir).resolve()
    if args.improve_json and Path(args.improve_json).is_file():
        improve = json.loads(lib.read_text(Path(args.improve_json)))
    else:
        improve = lib.load_improve_record(round_dir_path)
    if not log_path.is_file():
        purpose = args.purpose or lib.purpose_excerpt(askill_dir / "SKILL.md")
        lib.init_self_iter_log(log_path, askill_dir.name, rubric, purpose)
    lib.append_log(
        log_path,
        int(args.round),
        args.scenario,
        args.judge_role,
        args.isolated_judge.lower() in ("1", "true", "yes"),
        result,
        rubric,
        round_dir_path,
        args.out_summary,
        improve,
    )
    print(str(log_path))
    return 0


def cmd_append_session_end(args: argparse.Namespace) -> int:
    log_path = Path(args.log).resolve()
    lib.append_session_end(
        log_path,
        args.status,
        int(args.rounds_completed),
        args.remaining_gaps or "none",
        args.next_scenario or "",
    )
    print(str(log_path))
    return 0


def cmd_init_session(args: argparse.Namespace) -> int:
    root = Path(args.skills_root).resolve() if args.skills_root else None
    try:
        payload = lib.init_session(
            args.target,
            args.scenario,
            args.session_id,
            root,
            max_rounds=int(args.max_rounds),
            judge_role=args.judge_role,
            expected_artifact_type=args.expected_artifact_type or None,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(payload, indent=2))
    return 0


def cmd_complete_round(args: argparse.Namespace) -> int:
    askill = Path(args.askill_dir).resolve()
    try:
        payload = lib.complete_round(
            askill,
            args.session_id,
            int(args.round),
            out_summary=args.out_summary,
            require_improve_on_fail=not args.skip_improve_requirement,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1
    print(json.dumps(payload, indent=2))
    return 0


def cmd_next_round(args: argparse.Namespace) -> int:
    askill = Path(args.askill_dir).resolve()
    state = lib.load_session_state(askill, args.session_id)
    n = int(args.round) if args.round else int(state.get("currentRound", 0)) + 1
    max_rounds = int(state.get("maxRounds", 3))
    if n > max_rounds:
        print(json.dumps({"ok": False, "error": "round exceeds maxRounds"}, indent=2))
        return 1
    rd = lib.init_round_dir(askill, args.session_id, n)
    rubric_src = Path(state["rubricJsonPath"])
    if rubric_src.is_file():
        lib.write_text(rd / "active_rubric.json", lib.read_text(rubric_src))
    scenario = state.get("scenario", "")
    if scenario:
        lib.write_text(rd / "scenario.txt", scenario.strip() + "\n")
    state["currentRound"] = n
    lib.save_session_state(askill, args.session_id, state)
    print(
        json.dumps(
            {
                "ok": True,
                "round": n,
                "roundDir": str(rd),
                "hint": "Run Askill, write out.md, judge, then record-improve (if fail) and complete-round",
            },
            indent=2,
        )
    )
    return 0


def cmd_run_session(args: argparse.Namespace) -> int:
    if args.phase == "init":
        if not args.target or not args.scenario:
            print(
                json.dumps(
                    {"ok": False, "error": "init requires --target and --scenario"},
                    indent=2,
                )
            )
            return 1
        return cmd_init_session(args)
    if args.phase == "complete-round":
        if not args.askill_dir or not args.out_summary:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "complete-round requires --askill-dir and --out-summary",
                    },
                    indent=2,
                )
            )
            return 1
        return cmd_complete_round(args)
    if args.phase == "next-round":
        if not args.askill_dir:
            print(json.dumps({"ok": False, "error": "next-round requires --askill-dir"}, indent=2))
            return 1
        return cmd_next_round(args)
    print(json.dumps({"ok": False, "error": f"unknown phase {args.phase!r}"}, indent=2))
    return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="skill-tune session orchestration")
    sub = p.add_subparsers(dest="command", required=True)

    t = sub.add_parser("resolve-target")
    t.add_argument("--target", required=True)
    t.add_argument("--skills-root", default="")
    t.add_argument("--write", default="")
    t.set_defaults(func=cmd_resolve_target)

    r = sub.add_parser("resolve-rubric")
    r.add_argument("--askill-dir", required=True)
    r.add_argument("--skill-tune-root", default="")
    r.add_argument("--rubric", default="")
    r.add_argument("--write", default="")
    r.set_defaults(func=cmd_resolve_rubric)

    b = sub.add_parser("build-judge-packet")
    b.add_argument("--scenario", required=True)
    b.add_argument("--out-file", required=True)
    b.add_argument("--rubric-json", required=True)
    b.add_argument("--output", required=True)
    b.add_argument("--judge-role", default="product_manager")
    b.add_argument("--expected-artifact-type", default="")
    b.set_defaults(func=cmd_build_judge_packet)

    v = sub.add_parser("validate-judge-result")
    v.add_argument("--result", required=True)
    v.add_argument("--rubric-json", required=True)
    v.add_argument("--out-file", required=True)
    v.set_defaults(func=cmd_validate_judge_result)

    i = sub.add_parser("init-round-dir")
    i.add_argument("--askill-dir", required=True)
    i.add_argument("--session-id", required=True)
    i.add_argument("--round", required=True, type=int)
    i.add_argument("--out-file", required=True)
    i.add_argument("--scenario", default="")
    i.add_argument("--rubric-json", default="")
    i.set_defaults(func=cmd_init_round_dir)

    wo = sub.add_parser("write-out")
    wo.add_argument("--round-dir", required=True)
    wo.add_argument("--out-file", required=True)
    wo.set_defaults(func=cmd_write_out)

    j = sub.add_parser("record-judge-artifacts")
    j.add_argument("--round-dir", required=True)
    j.add_argument("--judge-packet", required=True)
    j.add_argument("--judge-result", required=True)
    j.set_defaults(func=cmd_record_judge_artifacts)

    im = sub.add_parser("record-improve")
    im.add_argument("--round-dir", required=True)
    im.add_argument("--summary", required=True)
    im.add_argument("--patch", default="")
    im.add_argument("--record-json", default="", help="Structured improve_record.json input")
    im.add_argument("--round", type=int, default=0)
    im.add_argument("--files-touched", default="")
    im.add_argument("--hypothesis", default="")
    im.add_argument("--generalized-from", default="")
    im.add_argument("--change", action="append", default=[])
    im.set_defaults(func=cmd_record_improve)

    a = sub.add_parser("append-log")
    a.add_argument("--log", required=True)
    a.add_argument("--askill-dir", required=True)
    a.add_argument("--round", required=True, type=int)
    a.add_argument("--scenario", required=True)
    a.add_argument("--judge-role", default="product_manager")
    a.add_argument("--isolated-judge", default="yes")
    a.add_argument("--judge-result", required=True)
    a.add_argument("--rubric-json", default="")
    a.add_argument("--round-dir", required=True)
    a.add_argument("--out-summary", required=True)
    a.add_argument("--improve-json", default="", help="Optional; else reads round-dir/improve_record.json")
    a.add_argument("--purpose", default="")
    a.set_defaults(func=cmd_append_log)

    se = sub.add_parser("append-session-end")
    se.add_argument("--log", required=True)
    se.add_argument("--status", required=True, choices=["excellent", "capped", "aborted"])
    se.add_argument("--rounds-completed", required=True, type=int)
    se.add_argument("--remaining-gaps", default="none")
    se.add_argument("--next-scenario", default="")
    se.set_defaults(func=cmd_append_session_end)

    ins = sub.add_parser("init-session")
    ins.add_argument("--target", required=True)
    ins.add_argument("--scenario", required=True)
    ins.add_argument("--session-id", required=True)
    ins.add_argument("--skills-root", default="")
    ins.add_argument("--max-rounds", default="3")
    ins.add_argument("--judge-role", default="product_manager")
    ins.add_argument("--expected-artifact-type", default="")
    ins.set_defaults(func=cmd_init_session)

    cr = sub.add_parser("complete-round")
    cr.add_argument("--askill-dir", required=True)
    cr.add_argument("--session-id", required=True)
    cr.add_argument("--round", required=True, type=int)
    cr.add_argument("--out-summary", required=True)
    cr.add_argument("--skip-improve-requirement", action="store_true")
    cr.set_defaults(func=cmd_complete_round)

    nr = sub.add_parser("next-round")
    nr.add_argument("--askill-dir", required=True)
    nr.add_argument("--session-id", required=True)
    nr.add_argument("--round", type=int, default=0)
    nr.set_defaults(func=cmd_next_round)

    rs = sub.add_parser("run-session")
    rs.add_argument(
        "phase",
        choices=["init", "complete-round", "next-round"],
        help="init | complete-round | next-round",
    )
    rs.add_argument("--target", default="")
    rs.add_argument("--scenario", default="")
    rs.add_argument("--session-id", required=True)
    rs.add_argument("--skills-root", default="")
    rs.add_argument("--max-rounds", default="3")
    rs.add_argument("--judge-role", default="product_manager")
    rs.add_argument("--expected-artifact-type", default="")
    rs.add_argument("--askill-dir", default="")
    rs.add_argument("--round", type=int, default=0)
    rs.add_argument("--out-summary", default="")
    rs.add_argument("--skip-improve-requirement", action="store_true")
    rs.set_defaults(func=cmd_run_session)

    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
