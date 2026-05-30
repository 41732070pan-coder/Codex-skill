#!/usr/bin/env python3
"""Find a usable Python interpreter for skill-tune scripts (Windows-friendly)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def try_run(cmd: list[str]) -> str | None:
    try:
        proc = subprocess.run(
            cmd + ["-c", "import sys; print(sys.executable)"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    exe = proc.stdout.strip()
    return exe or None


def pick_python() -> list[str] | None:
    candidates: list[list[str]] = []
    if sys.executable:
        candidates.append([sys.executable])
    py_launcher = shutil.which("py")
    if py_launcher:
        candidates.append([py_launcher, "-3"])
    for name in ("python3", "python"):
        path = shutil.which(name)
        if path:
            candidates.append([path])

    seen: set[str] = set()
    for cmd in candidates:
        key = " ".join(cmd)
        if key in seen:
            continue
        seen.add(key)
        exe = try_run(cmd)
        if exe:
            return cmd
    return None


def main() -> int:
    cmd = pick_python()
    if not cmd:
        print(
            "No Python found. Install Python 3 or run via Codex bundled Python.",
            file=sys.stderr,
        )
        return 1

    exe = try_run(cmd)
    if not exe:
        return 1

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    prefix = subprocess.list2cmdline(cmd) if os.name == "nt" else " ".join(cmd)

    print(exe)
    print(f"SKILL_TUNE_PYTHON={exe}")
    print(f"SKILL_TUNE_PYTHON_CMD={prefix}")
    print(f"# PowerShell examples (skill root: {skill_root}):")
    print(f'# & "{exe}" "{skill_root / "scripts" / "validate_skill_tune.py"}"')
    print(f'# & "{exe}" "{skill_root / "scripts" / "tune_session.py"}" resolve-rubric --help')
    print("# Or use scripts/run.ps1 from the skill-tune directory.")
    if os.environ.get("JSON"):
        print(json.dumps({"executable": exe, "command": cmd}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
