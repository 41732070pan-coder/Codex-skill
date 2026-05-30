#!/usr/bin/env python3
"""Fetch and report whether a local branch is safe to edit without remote drift."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        text=True,
        capture_output=True,
    )


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def ref_exists(repo: Path, ref: str) -> bool:
    return git(repo, "rev-parse", "--verify", "--quiet", ref, check=False).returncode == 0


def resolve_target(repo: Path, remote: str, branch: str | None) -> str | None:
    if branch:
        return branch if branch.startswith("refs/") else f"refs/remotes/{remote}/{branch}"
    upstream = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", check=False)
    if upstream.returncode == 0:
        return upstream.stdout.strip()
    current = git(repo, "branch", "--show-current").stdout.strip()
    same_name = f"refs/remotes/{remote}/{current}"
    if current and ref_exists(repo, same_name):
        return same_name
    remote_head = git(repo, "symbolic-ref", "--quiet", f"refs/remotes/{remote}/HEAD", check=False)
    return remote_head.stdout.strip() if remote_head.returncode == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Git worktree to inspect. Defaults to the current directory.")
    parser.add_argument("--remote", default="origin", help="Remote name to fetch and compare. Defaults to origin.")
    parser.add_argument("--branch", help="Remote branch name or full ref. Defaults to upstream, same-name branch, then remote HEAD.")
    parser.add_argument("--fetch", action="store_true", help="Fetch and prune the selected remote before comparing refs.")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow a dirty worktree while checking remote drift.")
    args = parser.parse_args()
    repo = args.repo.resolve()

    if git(repo, "rev-parse", "--is-inside-work-tree", check=False).returncode != 0:
        return fail(f"{repo} is not a Git worktree")
    remotes = git(repo, "remote").stdout.split()
    if args.remote not in remotes:
        return fail(f"remote {args.remote!r} is not configured; add the intended URL with: git remote add {args.remote} <url>")
    if not args.allow_dirty and git(repo, "status", "--porcelain").stdout.strip():
        return fail("worktree is dirty; commit, stash, or rerun with --allow-dirty for inspection only")
    if args.fetch:
        fetched = git(repo, "fetch", args.remote, "--prune", check=False)
        if fetched.returncode:
            detail = fetched.stderr.strip() or fetched.stdout.strip()
            return fail(f"git fetch {args.remote} --prune failed: {detail}")

    target = resolve_target(repo, args.remote, args.branch)
    if not target or not ref_exists(repo, target):
        return fail(f"cannot resolve a remote comparison ref for {args.remote!r}; pass --branch <remote-branch>")
    counts = git(repo, "rev-list", "--left-right", "--count", f"HEAD...{target}").stdout.split()
    ahead, behind = (int(value) for value in counts)
    print(f"remote={args.remote} target={target} ahead={ahead} behind={behind}")
    if behind and ahead:
        return fail("local and remote histories have diverged; integrate the fetched remote before editing")
    if behind:
        return fail("local branch is behind the fetched remote; integrate remote changes before editing")
    if ahead:
        print("OK: local branch contains commits not yet in the remote, with no fetched remote drift")
    else:
        print("OK: local branch matches the fetched remote")
    return 0


if __name__ == "__main__":
    sys.exit(main())
