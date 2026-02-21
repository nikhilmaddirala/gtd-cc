#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Manage skills with one wrapper for local and remote sources.

For local skills, this script uses `npx skills add` first (to let the upstream
CLI create the expected layout), then swaps `.agents/skills/<name>` from a
copied directory to a symlink pointing at the local source.

For remote sources (owner/repo), this script delegates directly to `npx skills`
and keeps the default copy-based behavior.

Final layout:
- .agents/skills/<name> -> <local source skill directory>
- .claude/skills/<name> -> ../../.agents/skills/<name> (created by npx)

OpenCode reads through .opencode/skill -> ../.claude/skills, so no additional
Opencode symlink is needed.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_AGENTS = ["claude-code", "opencode"]
ALLOWED_AGENTS = {"claude-code", "opencode"}
SOURCE_TYPES = {"auto", "local", "remote"}
REMOVE_MANAGERS = {"auto", "local", "remote"}


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def find_repo_root(explicit_root: str | None) -> Path:
    if explicit_root:
        root = Path(explicit_root).expanduser().resolve()
        if not root.is_dir():
            raise SystemExit(f"Error: --repo-root is not a directory: {root}")
        return root

    candidates = [Path.cwd(), Path(__file__).resolve().parent]
    for base in candidates:
        current = base
        while True:
            if (current / ".agents").is_dir() and (current / ".claude").is_dir():
                return current
            if current.parent == current:
                break
            current = current.parent

    raise SystemExit(
        "Error: could not find repo root. Run inside the monorepo or pass --repo-root."
    )


def parse_skill_name(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"Error: missing SKILL.md in {skill_dir}")

    text = skill_md.read_text(encoding="utf-8")
    if text.startswith("---"):
        lines = text.splitlines()
        for i in range(1, len(lines)):
            line = lines[i].strip()
            if line == "---":
                break
            if line.startswith("name:"):
                value = line.split(":", 1)[1].strip().strip('"').strip("'")
                if value:
                    return value

    return skill_dir.name


def detect_source_type(source: str, source_type: str) -> str:
    if source_type in {"local", "remote"}:
        return source_type

    local_prefixes = (".", "/", "~")
    if source.startswith(local_prefixes):
        return "local"

    if Path(source).expanduser().exists():
        return "local"

    return "remote"


def remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def run_command(command: list[str], workdir: Path) -> None:
    result = subprocess.run(command, cwd=workdir, capture_output=True, text=True)
    if result.returncode != 0:
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        details = "\n".join([x for x in [stdout, stderr] if x])
        if details:
            raise SystemExit(f"Error running {' '.join(command)}\n{details}")
        raise SystemExit(f"Error running {' '.join(command)}")


def refresh_manifest(repo_root: Path) -> None:
    discover_script = Path(__file__).resolve().parent / "discover-skills.py"
    if not discover_script.is_file():
        return
    run_command([str(discover_script), str(repo_root)], repo_root)


def ensure_symlink(link: Path, target: Path, force: bool) -> None:
    # Store relative targets for portability.
    relative_target = Path(os.path.relpath(target, start=link.parent))

    if link.is_symlink():
        current = Path(os.readlink(link))
        if current == relative_target:
            return
        if not force:
            raise SystemExit(
                f"Error: {link} already points to {current}. Use --force to replace."
            )
        link.unlink()
    elif link.exists():
        if not force:
            raise SystemExit(f"Error: {link} already exists. Use --force to replace.")
        remove_path(link)

    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(relative_target)


def cmd_add(args: argparse.Namespace) -> int:
    repo_root = find_repo_root(args.repo_root)
    selected_agents = args.agents or DEFAULT_AGENTS

    invalid = [a for a in selected_agents if a not in ALLOWED_AGENTS]
    if invalid:
        raise SystemExit(f"Error: invalid agents: {', '.join(invalid)}")

    source_type = detect_source_type(args.source, args.source_type)

    if source_type == "remote":
        cmd = ["npx", "skills", "add", args.source, "-a", *selected_agents, "-y"]
        if args.skill:
            cmd.extend(["--skill", args.skill])
        run_command(cmd, repo_root)
        print(f"Added remote skill source via npx: {args.source}")
        if args.skill:
            print(f"  skill: {args.skill}")
        if args.refresh_manifest:
            refresh_manifest(repo_root)
            print("  Manifest refreshed: skills-inventory.json")
        return 0

    skill_source = Path(args.source).expanduser().resolve()
    if not skill_source.is_dir():
        raise SystemExit(f"Error: skill path is not a directory: {skill_source}")

    skill_name = parse_skill_name(skill_source)

    # Step 1: bootstrap via npx skills so upstream layout stays consistent.
    run_command(
        [
            "npx",
            "skills",
            "add",
            str(skill_source),
            "-a",
            *selected_agents,
            "-y",
        ],
        repo_root,
    )

    # Step 2: swap the npx-copied .agents entry with a symlink to local source.
    agents_skill_link = repo_root / ".agents" / "skills" / skill_name
    if not agents_skill_link.exists() and not agents_skill_link.is_symlink():
        raise SystemExit(
            f"Error: expected npx to create {agents_skill_link}, but it was not found"
        )

    if agents_skill_link.is_symlink() and agents_skill_link.resolve() == skill_source:
        pass
    else:
        if agents_skill_link.exists() or agents_skill_link.is_symlink():
            remove_path(agents_skill_link)
        ensure_symlink(agents_skill_link, skill_source, force=True)

    # Step 3: ensure Claude link exists (npx usually creates this).
    if "claude-code" in selected_agents:
        claude_link = repo_root / ".claude" / "skills" / skill_name
        if not claude_link.exists() and not claude_link.is_symlink():
            ensure_symlink(claude_link, agents_skill_link, args.force)

    print(f"Added local skill via npx+symlink: {skill_name}")
    print(f"  .agents link: {agents_skill_link} -> {skill_source}")
    if "claude-code" in selected_agents:
        print(
            f"  .claude link: {repo_root / '.claude' / 'skills' / skill_name} -> {agents_skill_link}"
        )
    if "opencode" in selected_agents:
        print("  OpenCode: uses .opencode/skill -> ../.claude/skills")

    if args.refresh_manifest:
        refresh_manifest(repo_root)
        print("  Manifest refreshed: skills-inventory.json")

    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    repo_root = find_repo_root(args.repo_root)
    selected_agents = args.agents or DEFAULT_AGENTS

    invalid = [a for a in selected_agents if a not in ALLOWED_AGENTS]
    if invalid:
        raise SystemExit(f"Error: invalid agents: {', '.join(invalid)}")

    agents_link = repo_root / ".agents" / "skills" / args.skill
    inferred = "local" if agents_link.is_symlink() else "remote"
    manager = inferred if args.manager == "auto" else args.manager

    if manager == "remote":
        run_command(["npx", "skills", "remove", "--skill", args.skill, "-y"], repo_root)
        print(f"Removed via npx: {args.skill}")
    else:
        if "claude-code" in selected_agents:
            claude_link = repo_root / ".claude" / "skills" / args.skill
            if claude_link.exists() or claude_link.is_symlink():
                remove_path(claude_link)
                print(f"Removed: {claude_link}")

        if "opencode" in selected_agents:
            if agents_link.exists() or agents_link.is_symlink():
                remove_path(agents_link)
                print(f"Removed: {agents_link}")

    if args.refresh_manifest:
        refresh_manifest(repo_root)
        print("Manifest refreshed: skills-inventory.json")

    return 0


def cmd_list(args: argparse.Namespace) -> int:
    repo_root = find_repo_root(args.repo_root)
    agents_dir = repo_root / ".agents" / "skills"
    claude_dir = repo_root / ".claude" / "skills"

    if not agents_dir.is_dir():
        print("No .agents/skills directory found.")
        return 0

    entries = sorted(agents_dir.iterdir())
    if not entries:
        print("No installed skills found in .agents/skills.")
        return 0

    print("Installed skills:")
    for path in entries:
        manager = "local-skills" if path.is_symlink() else "npx"
        resolved = path.resolve() if path.is_symlink() else None
        exists = "yes" if (resolved and resolved.exists()) else "n/a"

        claude_path = claude_dir / path.name
        claude_status = "missing"
        if claude_path.is_symlink():
            claude_status = f"symlink -> {os.readlink(claude_path)}"
        elif claude_path.exists():
            claude_status = "exists (not symlink)"

        print(f"- {path.name}")
        print(f"  manager: {manager}")
        if path.is_symlink():
            print(f"  .agents: {path} -> {os.readlink(path)}")
            print(f"  source: {resolved} (exists: {exists})")
        else:
            print(f"  .agents: {path} (directory)")
        print(f"  .claude: {claude_status}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage local and remote skills via one wrapper"
    )
    parser.add_argument(
        "--repo-root",
        help="Monorepo root (auto-detected by default)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser(
        "add", help="Add a skill (local path or remote owner/repo)"
    )
    add.add_argument(
        "source",
        help="Local path (./path or /path) or remote source (owner/repo)",
    )
    add.add_argument(
        "--source-type",
        choices=sorted(SOURCE_TYPES),
        default="auto",
        help="Source type detection (default: auto)",
    )
    add.add_argument(
        "--skill",
        help="Skill name for remote sources (maps to npx --skill)",
    )
    add.add_argument(
        "-a",
        "--agents",
        nargs="+",
        choices=sorted(ALLOWED_AGENTS),
        help="Target agents (default: claude-code opencode)",
    )
    add.add_argument(
        "--force",
        action="store_true",
        help="Replace existing entries if needed",
    )
    add.add_argument(
        "--no-refresh-manifest",
        dest="refresh_manifest",
        action="store_false",
        help="Skip refreshing skills-inventory.json",
    )
    add.set_defaults(refresh_manifest=True)
    add.set_defaults(func=cmd_add)

    remove = subparsers.add_parser("remove", help="Remove a skill (auto/local/remote)")
    remove.add_argument("--skill", required=True, help="Skill name to remove")
    remove.add_argument(
        "--manager",
        choices=sorted(REMOVE_MANAGERS),
        default="auto",
        help="Removal mode (default: auto infers from .agents/skills entry type)",
    )
    remove.add_argument(
        "-a",
        "--agents",
        nargs="+",
        choices=sorted(ALLOWED_AGENTS),
        help="Target agents to remove from (default: claude-code opencode)",
    )
    remove.add_argument(
        "--no-refresh-manifest",
        dest="refresh_manifest",
        action="store_false",
        help="Skip refreshing skills-inventory.json",
    )
    remove.set_defaults(refresh_manifest=True)
    remove.set_defaults(func=cmd_remove)

    listing = subparsers.add_parser(
        "list", help="List installed skills and inferred manager"
    )
    listing.set_defaults(func=cmd_list)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        eprint(f"Error: {exc}")
        raise SystemExit(1)
