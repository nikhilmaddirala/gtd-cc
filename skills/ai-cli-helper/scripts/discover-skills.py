#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pyyaml>=6.0",
# ]
# ///
"""Build a unified skills manifest (discovery + activation status).

The manifest combines:
- Discovery: all SKILL.md sources found in the monorepo
- Activation: what is currently enabled in .agents/skills and .claude/skills

Usage:
    ./discover-skills.py
    ./discover-skills.py /path/to/monorepo
    ./discover-skills.py --output out.json
    ./discover-skills.py --stdout-only
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml


SKIP_DIRS = {
    "node_modules",
    ".git",
    ".agents",
    ".worktrees",
    "__pycache__",
    ".venv",
}

SKIP_PREFIXES = [
    ".claude/skills/",
]

# Customize these rules to match your repo structure.
# Each tuple is (path_prefix, ownership_label). Skills found under a matching
# prefix get tagged with that label in the manifest.
OWNERSHIP_RULES = [
    ("40-code/43-private/ai-skills/", "private"),
    ("40-code/41-subtrees/gtd-cc/", "public"),
    ("40-code/42-lab/", "project-specific"),
]


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    try:
        parsed = yaml.safe_load(text[3:end])
    except yaml.YAMLError:
        return None
    return parsed if isinstance(parsed, dict) else None


def infer_ownership(rel_path: str) -> str:
    for prefix, ownership in OWNERSHIP_RULES:
        if rel_path.startswith(prefix):
            return ownership
    return "unknown"


def relpath_or_abs(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def discover_sources(root: Path) -> dict[str, dict]:
    by_name: dict[str, dict] = {}

    for dirpath, dirnames, filenames in root.walk():
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        rel_dir = str(dirpath.relative_to(root))
        if any(rel_dir.startswith(prefix) for prefix in SKIP_PREFIXES):
            dirnames.clear()
            continue

        if "SKILL.md" not in filenames:
            continue

        skill_md = dirpath / "SKILL.md"
        fm = parse_frontmatter(skill_md)

        raw_name = fm.get("name", dirpath.name) if fm else dirpath.name
        raw_desc = fm.get("description", "") if fm else ""

        name = str(raw_name) if not isinstance(raw_name, str) else raw_name
        desc = str(raw_desc) if not isinstance(raw_desc, str) else raw_desc

        # Skip placeholder scaffold skills from templates.
        if name.strip() in {"skill-name", "['skill-name']"} or name.strip().startswith(
            "["
        ):
            continue

        path_str = str(dirpath.relative_to(root))
        ownership = infer_ownership(path_str)

        subskills: list[str] = []
        sub_dir_a = dirpath / "sub-skills"
        sub_dir_b = dirpath / "subskills"
        if sub_dir_a.is_dir():
            subskills = [f.stem for f in sorted(sub_dir_a.glob("*.md"))]
        elif sub_dir_b.is_dir():
            subskills = [f.stem for f in sorted(sub_dir_b.glob("*.md"))]

        source_entry = {
            "path": path_str,
            "ownership": ownership,
            "description": desc,
            "sub_skills": subskills,
        }

        existing = by_name.get(name)
        if not existing:
            by_name[name] = {
                "name": name,
                "description": desc,
                "sources": [source_entry],
            }
            continue

        existing_paths = {s["path"] for s in existing["sources"]}
        if path_str not in existing_paths:
            existing["sources"].append(source_entry)

        if not existing.get("description") and desc:
            existing["description"] = desc

    return by_name


def detect_activation(root: Path) -> dict[str, dict]:
    activation: dict[str, dict] = {}

    agents_dir = root / ".agents" / "skills"
    claude_dir = root / ".claude" / "skills"
    opencode_skill_dir = root / ".opencode" / "skill"
    opencode_uses_claude = opencode_skill_dir.is_symlink()

    if not agents_dir.is_dir():
        return activation

    for entry in sorted(agents_dir.iterdir()):
        name = entry.name

        state = {
            "installed": True,
            "manager": "npx",
            "agents_entry_type": "directory",
            "agents_path": relpath_or_abs(entry, root),
            "agents_link_target": None,
            "agents_resolved_source": None,
            "claude_enabled": False,
            "claude_entry_type": "missing",
            "claude_link_target": None,
            "opencode_enabled": False,
            "opencode_via": "none",
        }

        if entry.is_symlink():
            state["manager"] = "local-skills"
            state["agents_entry_type"] = "symlink"
            state["agents_link_target"] = os.readlink(entry)
            state["agents_resolved_source"] = relpath_or_abs(entry.resolve(), root)
        elif entry.is_dir():
            state["manager"] = "npx"
        elif entry.exists():
            state["agents_entry_type"] = "file"
            state["manager"] = "unknown"

        claude_entry = claude_dir / name
        if claude_entry.is_symlink():
            state["claude_enabled"] = True
            state["claude_entry_type"] = "symlink"
            state["claude_link_target"] = os.readlink(claude_entry)
        elif claude_entry.is_dir():
            state["claude_enabled"] = True
            state["claude_entry_type"] = "directory"
        elif claude_entry.exists():
            state["claude_enabled"] = True
            state["claude_entry_type"] = "file"

        if opencode_uses_claude and state["claude_enabled"]:
            state["opencode_enabled"] = True
            state["opencode_via"] = ".opencode/skill -> .claude/skills"

        activation[name] = state

    return activation


def build_manifest(root: Path) -> dict:
    discovered = discover_sources(root)
    active = detect_activation(root)

    all_names = sorted(set(discovered.keys()) | set(active.keys()), key=str.casefold)
    skills: list[dict] = []

    for name in all_names:
        discovered_entry = discovered.get(name)
        active_entry = active.get(name)

        if discovered_entry:
            description = discovered_entry.get("description", "")
            sources = discovered_entry.get("sources", [])
        else:
            description = ""
            sources = []

        if not description and active_entry:
            agents_path = root / active_entry["agents_path"]
            skill_md = agents_path / "SKILL.md"
            if skill_md.is_file():
                fm = parse_frontmatter(skill_md)
                if fm and isinstance(fm.get("description"), str):
                    description = fm["description"]

        compact_sources: list[dict] = []
        for source in sources:
            entry = {
                "path": source.get("path"),
                "ownership": source.get("ownership", "unknown"),
            }
            subskills = source.get("sub_skills") or []
            if subskills:
                entry["sub_skills"] = subskills
            compact_sources.append(entry)

        activation = active_entry or {
            "installed": False,
            "manager": None,
            "agents_path": f".agents/skills/{name}",
            "agents_resolved_source": None,
            "claude_enabled": False,
            "opencode_enabled": False,
        }

        skills.append(
            {
                "name": name,
                "description": description,
                "discovered": bool(discovered_entry),
                "sources": compact_sources,
                "installed": activation["installed"],
                "manager": activation.get("manager"),
                "source": activation.get("agents_resolved_source"),
                "agents_path": activation.get("agents_path"),
                "claude_enabled": activation.get("claude_enabled", False),
                "opencode_enabled": activation.get("opencode_enabled", False),
            }
        )

    return {
        "schema_version": 3,
        "manifest_type": "skills-discovery-and-activation",
        "repo_root": str(root),
        "summary": {
            "discovered_total": len(discovered),
            "installed_total": sum(1 for item in skills if item["installed"]),
            "installed_local_symlink_total": sum(
                1
                for item in skills
                if item["installed"] and item["manager"] == "local-skills"
            ),
            "installed_npx_total": sum(
                1 for item in skills if item["installed"] and item["manager"] == "npx"
            ),
        },
        "skills": skills,
    }


DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "skills-inventory.json"


def parse_args(argv: list[str]) -> tuple[Path, Path | None, bool]:
    if "--help" in argv or "-h" in argv:
        print("Usage: discover-skills.py [REPO_ROOT] [--output PATH] [--stdout-only]")
        print("Builds a unified discovery+activation manifest.")
        raise SystemExit(0)

    stdout_only = "--stdout-only" in argv

    output_path: Path | None = None
    if "--output" in argv:
        idx = argv.index("--output")
        if idx + 1 < len(argv):
            output_path = Path(argv[idx + 1])
        else:
            print("Error: --output requires a path argument", file=sys.stderr)
            sys.exit(1)

    positional = [
        arg for arg in argv[1:] if not arg.startswith("-") and arg != str(output_path)
    ]
    root = (
        Path(positional[0]).expanduser().resolve()
        if positional
        else Path.cwd().resolve()
    )

    return root, output_path, stdout_only


def main() -> None:
    root, output_path, stdout_only = parse_args(sys.argv)

    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    manifest = build_manifest(root)
    result = json.dumps(manifest, indent=2)

    print(result)

    if not stdout_only:
        dest = output_path or DEFAULT_OUTPUT
        dest.write_text(result + "\n", encoding="utf-8")
        print(
            f"Wrote {manifest['summary']['discovered_total']} discovered skills to {dest}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
