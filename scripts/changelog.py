#!/usr/bin/env python3
"""Changelog automation: categorize conventional commits and maintain CHANGELOG.md.

Deterministic, offline and stdlib-only. The script never touches git state other than
reading ``git log``: it writes files only when explicitly asked (``write``, ``release``).

Commands:
    ``list``     categorize the commits since a reference and print them (text or JSON)
    ``write``    merge missing categorized entries into the ``[Unreleased]`` section
    ``release``  move the ``[Unreleased]`` entries into a dated version section
    ``check``    report structural problems in CHANGELOG.md (exit 1 when ``--strict``)

Category mapping and formatting rules live in ``.serena/memories/changelog_conventions.md``;
this script is the mechanical backstop, the agent rewrites entries into user-facing prose.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from manage import DEFAULT_ROOT, require, scoped_path

CHANGELOG = "CHANGELOG.md"
SECTIONS = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security")

# conventional-commit type -> Keep a Changelog section; omitted types are skipped by default
TYPE_SECTIONS = {
    "feat": "Added",
    "feature": "Added",
    "fix": "Fixed",
    "bugfix": "Fixed",
    "perf": "Changed",
    "refactor": "Changed",
    "revert": "Removed",
    "remove": "Removed",
    "deprecate": "Deprecated",
    "sec": "Security",
    "security": "Security",
}
SKIPPED_TYPES = {"chore", "docs", "doc", "test", "tests", "ci", "style", "build"}
SUBJECT_RE = re.compile(
    r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]*)\))?(?P<breaking>!)?:\s*(?P<description>.+)$"
)
PR_RE = re.compile(r"\(#(\d+)\)\s*$")
BREAKING_RE = re.compile(r"^BREAKING[ -]CHANGE:", re.MULTILINE)
VERSION_HEADING_RE = re.compile(r"^##\s+\[(?P<version>[^\]]+)\](?:\s*-\s*(?P<date>\S+))?\s*$")
LINK_RE = re.compile(r"^\[(?P<label>[^\]]+)\]:\s*(?P<url>\S+)\s*$")

HEADER = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    require(result.returncode == 0, f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def repository_url(root: Path) -> str:
    """Normalize ``origin`` into an https base URL, empty when unavailable."""
    try:
        remote = git(root, "remote", "get-url", "origin").strip()
    except ValueError:
        return ""
    match = re.match(r"git@([^:]+):(.+?)(?:\.git)?$", remote)
    if match:
        return f"https://{match.group(1)}/{match.group(2)}"
    return re.sub(r"\.git$", "", remote)


def last_tag(root: Path) -> str:
    try:
        return git(root, "describe", "--tags", "--abbrev=0").strip()
    except ValueError:
        return ""


def resolve_reference(root: Path, since: str) -> tuple[str, str]:
    """Return ``(reference, source)`` for the commit range, source in explicit/tag/initial."""
    if since:
        return since, "explicit"
    tag = last_tag(root)
    if tag:
        return tag, "tag"
    return "", "initial"


def commits_since(root: Path, since: str) -> list[dict[str, str]]:
    reference, _ = resolve_reference(root, since)
    rev_range = f"{reference}..HEAD" if reference else "HEAD"
    raw = git(root, "log", rev_range, "--no-merges", "--format=%H%x1f%s%x1f%b%x1e")
    records = []
    for chunk in raw.split("\x1e"):
        fields = chunk.strip("\n").split("\x1f")
        if len(fields) < 2 or not fields[0]:
            continue
        records.append(
            {
                "sha": fields[0],
                "subject": fields[1],
                "body": fields[2] if len(fields) > 2 else "",
            }
        )
    return records


def categorize(subject: str, body: str = "") -> tuple[str, bool, str] | None:
    """Return ``(section, breaking, description)`` or ``None`` for skipped commits."""
    match = SUBJECT_RE.match(subject.strip())
    kind = (match.group("type").lower() if match else "")
    breaking = (bool(match and match.group("breaking")) or bool(BREAKING_RE.search(body))
                or bool(re.search(r"^[a-zA-Z]+(\([^)]*\))?!:", subject.strip())))
    section = TYPE_SECTIONS.get(kind, "")
    if breaking and not section:
        section = "Changed"
    if not section:
        return None
    description = match.group("description").strip() if match else subject.strip()
    return section, breaking, description


def entries(commits: list[dict[str, str]]) -> list[dict[str, str]]:
    collected = []
    for commit in commits:
        found = categorize(commit["subject"], commit.get("body", ""))
        if not found:
            continue
        section, breaking, description = found
        pr = PR_RE.search(description)
        collected.append(
            {
                "section": section,
                "breaking": breaking,
                "sha": commit["sha"],
                "description": description,
                "pr": pr.group(1) if pr else "",
            }
        )
    return collected


def bullet(entry: dict[str, str]) -> str:
    """Render one entry; the PR reference stays embedded in the commit subject."""
    prefix = "- **BREAKING** " if entry["breaking"] else "- "
    return f"{prefix}{entry['description']}"


def unreleased_block(text: str) -> tuple[int, int, str] | None:
    """Return ``(start, end, body)`` line indices of the ``[Unreleased]`` section."""
    lines = text.split("\n")
    start = next(
        (i for i, line in enumerate(lines) if VERSION_HEADING_RE.match(line)
         and VERSION_HEADING_RE.match(line).group("version") == "Unreleased"),
        None,
    )
    if start is None:
        return None
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return start, end, "\n".join(lines[start + 1:end])


def merge(text: str, collected: list[dict[str, str]]) -> tuple[str, int]:
    """Insert entries missing from ``[Unreleased]``; returns the new text and count."""
    if not collected:
        return text, 0
    if "[Unreleased]" not in text:
        text = f"{text.rstrip()}\n\n## [Unreleased]\n"
    block = unreleased_block(text)
    require(block is not None, "no [Unreleased] section found")
    start, end, body = block
    existing = set(re.findall(r"^- .*$", body, flags=re.MULTILINE))
    additions: dict[str, list[str]] = {}
    added = 0
    for entry in collected:
        line = bullet(entry)
        if line in existing or entry["description"] in body:
            continue
        additions.setdefault(entry["section"], []).append(line)
        added += 1
    if not added:
        return text, 0
    known = {match.group(1) for match in re.finditer(r"^### (.+)$", body, flags=re.MULTILINE)}
    for section in reversed(SECTIONS):  # keep canonical order when prepending
        if section in additions and section not in known:
            body = f"\n### {section}\n" + "\n".join(additions.pop(section)) + "\n" + body
    for section, lines in additions.items():
        heading = f"### {section}"
        require(heading in body, f"cannot place section {section} in [Unreleased]")
        body = body.replace(heading, heading + "\n" + "\n".join(lines), 1)
    lines = text.split("\n")
    trailing = [line for line in lines[end:] if line.strip()][:1]
    rebuilt = lines[:start + 1] + [""] + body.strip("\n").split("\n")
    if trailing:
        rebuilt.append("")
    return "\n".join(rebuilt + lines[end:]).rstrip() + "\n", added


def release(text: str, version: str, released: str, url: str) -> tuple[str, int]:
    """Turn the ``[Unreleased]`` entries into ``## [version] - released``.

    Never commits, tags or pushes. Older sections keep their blank lines; every link definition
    is dropped and re-emitted in canonical order so repeated releases stay stable.
    """
    require(re.match(r"^\d+\.\d+\.\d+$", version), f"version must be MAJOR.MINOR.PATCH: {version}")
    lines = text.split("\n")
    start = next(
        (i for i, line in enumerate(lines)
         if (match := VERSION_HEADING_RE.match(line)) and match.group("version") == "Unreleased"),
        None,
    )
    require(start is not None, "no [Unreleased] section found")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    body = "\n".join(lines[start + 1:end]).strip("\n")
    count = len(re.findall(r"^- .+$", body, flags=re.MULTILINE))
    require(count > 0, "[Unreleased] has no entries to release")

    links = {
        match.group("label"): match.group("url")
        for line in lines
        if (match := LINK_RE.match(line))
    }
    tail = [line for line in lines[end:] if not LINK_RE.match(line)]
    previous = next(
        (match.group("version") for line in tail
         if (match := VERSION_HEADING_RE.match(line))
         and match.group("version") not in {"Unreleased", version}),
        None,
    )
    section = [f"## [{version}] - {released}", ""] + body.split("\n")
    rebuilt = lines[:start] + ["## [Unreleased]", ""] + section + [""] + tail
    updated = "\n".join(rebuilt).rstrip() + "\n"

    if url:
        links["Unreleased"] = f"{url}/compare/v{version}...HEAD"
        # First release: link the tag itself; later releases compare against the previous one.
        links[version] = (
            f"{url}/compare/v{previous}...v{version}" if previous else f"{url}/releases/tag/v{version}"
        )
        ordered = [f"[Unreleased]: {links['Unreleased']}"]
        for line in rebuilt:
            match = VERSION_HEADING_RE.match(line)
            if match and match.group("version") in links and match.group("version") != "Unreleased":
                ordered.append(f"[{match.group('version')}]: {links[match.group('version')]}")
        updated = updated.rstrip() + "\n\n" + "\n".join(ordered) + "\n"
    return updated, count


def check(text: str) -> list[str]:
    problems = []
    if not text.startswith("# Changelog"):
        problems.append("missing '# Changelog' title")
    headings = [VERSION_HEADING_RE.match(line) for line in text.split("\n")]
    versions = [m.group("version") for m in headings if m]
    if "Unreleased" not in versions:
        problems.append("missing '## [Unreleased]' section")
    for heading, match in zip(text.split("\n"), headings):
        if not match:
            if heading.startswith("## ["):
                problems.append(f"malformed version heading: {heading}")
            continue
        version, released = match.group("version"), match.group("date")
        if version != "Unreleased":
            if not re.match(r"^\d+\.\d+\.\d+$", version):
                problems.append(f"version without MAJOR.MINOR.PATCH: {version}")
            if not released or not re.match(r"^\d{4}-\d{2}-\d{2}$", released or ""):
                problems.append(f"missing or non-ISO date for {version}: {released}")
    for body, name in section_bodies(text):
        if not re.search(r"^- .+$", body, flags=re.MULTILINE):
            problems.append(f"empty section: {name}")
    released_versions = [v for v in versions if v != "Unreleased"]
    ordered = sorted(released_versions, key=version_key, reverse=True)
    if released_versions != ordered:
        problems.append("released versions are not in descending order")
    return problems


def section_bodies(text: str) -> list[tuple[str, str]]:
    found = []
    lines = text.split("\n")
    for index, line in enumerate(lines):
        match = re.match(r"^### (.+)$", line)
        if not match:
            continue
        end = next(
            (i for i in range(index + 1, len(lines)) if lines[i].startswith(("### ", "## "))),
            len(lines),
        )
        found.append(("\n".join(lines[index + 1:end]), match.group(1)))
    return found


def version_key(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split(".")) if value.count(".") == 2 else (0, 0, 0)


def load(root: Path) -> str:
    path = scoped_path(root, CHANGELOG)
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def save(root: Path, text: str) -> None:
    scoped_path(root, CHANGELOG).write_text(text, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)

    listing = commands.add_parser("list", help="categorize commits since a reference")
    listing.add_argument("--since", default="", help="git reference (default: last tag)")
    listing.add_argument("--json", action="store_true", help="machine-readable output")

    writing = commands.add_parser("write", help="merge missing entries into [Unreleased]")
    writing.add_argument("--since", default="", help="git reference (default: last tag)")

    releasing = commands.add_parser("release", help="release [Unreleased] as a version")
    releasing.add_argument("version", help="MAJOR.MINOR.PATCH without the v prefix")
    releasing.add_argument("--date", default=date.today().isoformat())

    checking = commands.add_parser("check", help="report structural problems")
    checking.add_argument("--strict", action="store_true", help="exit 1 when problems are found")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.root.resolve()

    if args.command == "list":
        collected = entries(commits_since(root, args.since))
        if args.json:
            print(json.dumps(collected, indent=2))
            return 0
        for section in SECTIONS:
            lines = [bullet(entry) for entry in collected if entry["section"] == section]
            if lines:
                print(f"### {section}")
                print("\n".join(lines))
        return 0

    if args.command == "write":
        reference, source = resolve_reference(root, args.since)
        if source == "initial":
            print(
                "advisory: no git tag found, ranging over the full history; "
                "pass --since <ref> for a bounded first seed",
                file=sys.stderr,
            )
        text = load(root) or f"{HEADER}\n## [Unreleased]\n"
        updated, added = merge(text, entries(commits_since(root, reference)))
        if added:
            save(root, updated)
        print(f"{added} entries added to [Unreleased] in {CHANGELOG} (range: {reference or 'root'})")
        return 0

    if args.command == "release":
        updated, count = release(load(root), args.version, args.date, repository_url(root))
        save(root, updated)
        print(f"released {count} entries as {args.version}; update the tag and commit separately")
        return 0

    problems = check(load(root))
    for problem in problems:
        print(f"- {problem}")
    if not problems:
        print("CHANGELOG.md is structurally valid")
    return 1 if problems and args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())
