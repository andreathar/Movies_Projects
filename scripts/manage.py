#!/usr/bin/env python3
"""Offline management commands for the Movies_Projects workspace.

Commands: ``validate`` and ``status`` (workspace integrity), ``lint`` (hard contradictions and
advisories for the active film), ``resume`` (session-start digest), ``handoff check PATH``
(handoff schema and hash verification) and ``handoff ingest PATH --by ROLE`` (records producer
reconciliation). Only ``handoff ingest`` writes, and only the handoff's ``ingest`` object.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
TASK_STATES = {"pending", "ready", "blocked", "in_progress", "completed", "cancelled"}
OPEN_TASK_STATES = {"in_progress", "blocked"}
GENERIC_BLOCKER = "Awaiting dependency completion and applicable approval"
LINT_ERRORS = (OSError, ValueError, KeyError, TypeError)
MISTAKE_RULE_GRACE_DAYS = 7
GIT_STATUS_CAP = 50


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def scoped_path(root: Path, value: str, *, shared_skill: bool = False) -> Path:
    relative = Path(value)
    require(
        not relative.is_absolute() and ".." not in relative.parts,
        f"path must be workspace-relative: {value}",
    )
    result = root / relative
    require(
        shared_skill or result.resolve().is_relative_to(root.resolve()),
        f"path escapes workspace: {value}",
    )
    return result


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path.name}")
    return value


def check_dependencies(tasks: list[dict[str, Any]]) -> None:
    mapping = {task["id"]: task for task in tasks}
    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(identifier: str) -> None:
        require(identifier in mapping, f"unknown task dependency: {identifier}")
        require(identifier not in visiting, f"cyclic task dependency: {identifier}")
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in mapping[identifier].get("dependsOn", []):
            visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in mapping:
        visit(identifier)


def production_plan_report(root: Path, *, coherence: bool = False) -> dict[str, Any]:
    import importlib.util
    spec = importlib.util.spec_from_file_location("managed_production_plan", Path(__file__).with_name("production_plan.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.coherence_report(root) if coherence else module.validate(root)


def lint_production_plan(root: Path, hard: list[str], advisory: list[str]) -> None:
    report = production_plan_report(root)
    hard.extend(report["errors"])
    if report["errors"] or report.get("status") == "not_configured":
        return
    for item in production_plan_report(root, coherence=True)["items"]:
        message = f"coherence {item.get('shotId', '')} {item['code']}: {item['msg']}"
        if item["level"] == "ERROR":
            hard.append(message)
        elif item["level"] == "WARN":
            if item.get("acknowledged"):
                message += " [aviso reconhecido com justificativa; não é aprovação]"
            advisory.append(message)


def validate(root: Path) -> dict[str, Any]:
    report: dict[str, Any] = {"status": "ok", "errors": [], "warnings": [], "projects": []}
    try:
        workspace = read_json(root / "workspace.json")
        require(
            not workspace.get("paidGenerationAutomation"),
            "paid generation automation is not permitted by this workspace",
        )
        for relative in workspace["requiredDirectories"]:
            require(scoped_path(root, relative).is_dir(), f"missing directory: {relative}")
        for relative in [
            "AGENTS.md",
            "README.md",
            "memory/projects.json",
            "agents/registry.json",
            "skills/registry.json",
        ]:
            require(scoped_path(root, relative).is_file(), f"missing metadata file: {relative}")

        agents = read_json(root / "agents/registry.json")
        roles = {role["id"] for role in agents["roles"]}
        require(len(roles) == len(agents["roles"]), "duplicate agent role IDs")
        for role in agents["roles"]:
            require(
                scoped_path(root, role["brief"]).is_file(), f"missing agent brief: {role['id']}"
            )
        skills = read_json(root / "skills/registry.json")
        skill_names = {skill["name"] for skill in skills["skills"]}
        for role in agents["roles"]:
            for skill_name in role.get("skills", []):
                require(
                    isinstance(skill_name, str) and skill_name in skill_names,
                    f"role {role['id']} names unknown skill: {skill_name}",
                )
        for skill in skills["skills"]:
            skill_file = scoped_path(root, skill["path"], shared_skill=True) / "SKILL.md"
            require(skill_file.is_file(), f"missing or broken skill source: {skill['name']}")
            expected_hash = skill.get("sourceSha256")
            if (
                expected_hash
                and hashlib.sha256(skill_file.read_bytes()).hexdigest() != expected_hash
            ):
                report["warnings"].append(f"shared skill changed since linking: {skill['name']}")

        project_ids = [project["id"] for project in workspace["projects"]]
        require(len(set(project_ids)) == len(project_ids), "duplicate film project IDs")
        require(workspace["activeFilm"] in project_ids, "active film is not registered")
        for project in workspace["projects"]:
            film = scoped_path(root, project["root"])
            manifest = read_json(scoped_path(root, project["manifest"]))
            board = read_json(scoped_path(root, project["tasks"]))
            require(scoped_path(root, project["state"]).is_file(), "missing film resume state")
            for relative in [
                "docs/production-plan.md",
                "01_script/script-en.md",
                "00_brief/approvals.json",
                "asset-registry.csv",
                "credit-ledger.csv",
            ]:
                require(scoped_path(film, relative).is_file(), f"missing film file: {relative}")

            approvals = read_json(film / "00_brief/approvals.json")
            require(
                manifest["approvals"] == approvals["creativeApprovals"],
                "manifest and canonical creative approvals disagree",
            )
            require(
                manifest["approvals"]["paidBatch"]
                == approvals["paidGenerationBatchApproved"],
                "paid batch approval flags disagree",
            )
            require(
                manifest["budget"]["externalAudioServiceBudgetApproved"]
                == approvals["externalAudioServiceBudgetApproved"],
                "external audio approval flags disagree",
            )
            require(
                not manifest["finalMovieVerified"] or manifest["approvals"]["finalPicture"],
                "final movie verification requires final picture approval",
            )
            with (film / "01_script/dialogue-lines.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                dialogue = list(csv.DictReader(handle))
            require(len({row["line_id"] for row in dialogue}) == len(dialogue),
                    "duplicate dialogue IDs")
            script_text = (film / "01_script/script-en.md").read_text(encoding="utf-8")
            for row in dialogue:
                require(row["text_en"] in script_text,
                        f"canonical script and dialogue CSV disagree: {row['line_id']}")

            chapters = manifest["chapters"]
            require(len({c["id"] for c in chapters}) == len(chapters), "duplicate chapter IDs")
            shots = manifest["shots"]
            shot_ids = [shot["id"] for shot in shots]
            require(len(set(shot_ids)) == len(shot_ids), "duplicate shot IDs")
            require(
                len(shots) == manifest["scope"]["primaryStoryboardSlots"],
                "shot inventory count disagrees with scope",
            )
            declared = (
                manifest["openingSlotIds"]
                + [sid for chapter in chapters for sid in chapter["slotIds"]]
                + manifest["endingSlotIds"]
            )
            require(shot_ids == declared, "shot order disagrees with chapter declarations")
            require(all(shot["targetSeconds"] > 0 for shot in shots), "invalid shot duration")
            total_seconds = sum(shot["targetSeconds"] for shot in shots)
            require(
                total_seconds == manifest["scope"]["targetSeconds"],
                "shot durations disagree with runtime scope",
            )
            for chapter in chapters:
                actual = sum(s["targetSeconds"] for s in shots if s["chapter"] == chapter["key"])
                require(
                    actual == manifest["scope"]["chapterSeconds"],
                    f"chapter runtime mismatch: {chapter['key']}",
                )
            with (film / "05_storyboard/shot-list.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                csv_shots = list(csv.DictReader(handle))
            require(
                [row["shot_id"] for row in csv_shots] == shot_ids,
                "CSV shot order disagrees with manifest",
            )
            require(
                [int(row["target_seconds"]) for row in csv_shots]
                == [shot["targetSeconds"] for shot in shots],
                "CSV shot duration mismatch",
            )

            budget = manifest["budget"]
            require(
                sum(budget["phaseCaps"].values()) == budget["verifiedBalanceSnapshot"],
                "budget allocations disagree with snapshot ceiling",
            )
            require(
                all(value >= 0 for value in budget["phaseCaps"].values()),
                "negative budget allocation",
            )
            tasks = board["tasks"]
            require(len({task["id"] for task in tasks}) == len(tasks), "duplicate task IDs")
            check_dependencies(tasks)
            for task in tasks:
                require(task["ownerRole"] in roles, f"unknown task role: {task['id']}")
                require(task["status"] in TASK_STATES, f"invalid task state: {task['id']}")
                if task["status"] == "completed":
                    require(
                        bool(task.get("deliverables")) and bool(task.get("verifiedAt")),
                        f"completed task has no verified deliverables: {task['id']}",
                    )
                    for artifact in task["deliverables"]:
                        require(
                            scoped_path(film, artifact).is_file(),
                            f"completed task artifact is missing: {task['id']}",
                        )
            take_ids = {take["id"] for take in manifest["takes"]}
            require(len(take_ids) == len(manifest["takes"]), "duplicate take IDs")
            for shot in shots:
                accepted = shot.get("acceptedTakeId")
                require(
                    set(shot.get("takeIds", [])) <= take_ids,
                    f"shot references an unrecorded take: {shot['id']}",
                )
                require(
                    accepted is None or accepted in shot.get("takeIds", []),
                    f"accepted take is not recorded: {shot['id']}",
                )

            registry = read_json(film / "00_brief/research/source-registry.json")
            missing_snapshots = []
            for source in registry["sources"]:
                if source.get("snapshotPath"):
                    snapshot = scoped_path(film, source["snapshotPath"])
                    require(snapshot.is_file(), f"missing research snapshot: {source['id']}")
                    require(
                        hashlib.sha256(snapshot.read_bytes()).hexdigest()
                        == source["snapshotSha256"],
                        f"research snapshot checksum mismatch: {source['id']}",
                    )
                else:
                    missing_snapshots.append(source["id"])
            if missing_snapshots:
                report["warnings"].append({"missingCachedSourceSnapshots": missing_snapshots})
            report["projects"].append(
                {
                    "id": project["id"],
                    "chapters": len(chapters),
                    "storyboardSlots": len(shots),
                    "targetSeconds": total_seconds,
                    "budgetCeiling": sum(budget["phaseCaps"].values()),
                    "productionTasks": len(tasks),
                    "taskStates": dict(Counter(t["status"] for t in tasks)),
                    "recordedTakes": len(manifest["takes"]),
                    "finalMovieVerified": manifest["finalMovieVerified"],
                    "registeredSources": len(registry["sources"]),
                    "importedSourceSnapshots": len(registry["sources"]) - len(missing_snapshots),
                }
            )
        plan_report = production_plan_report(root)
        require(not plan_report["errors"], "production plan: " + "; ".join(plan_report["errors"]))
    except (OSError, ValueError, KeyError, TypeError) as error:
        report["status"] = "error"
        report["errors"].append(str(error))
    return report


def status(root: Path) -> dict[str, Any]:
    report = validate(root)
    if report["status"] != "ok":
        return report
    workspace = read_json(root / "workspace.json")
    report["activeFilm"] = workspace["activeFilm"]
    report["memoryBackend"] = workspace["memoryBackend"]
    report["paidGenerationAutomation"] = workspace["paidGenerationAutomation"]
    for project, summary in zip(workspace["projects"], report["projects"]):
        board = read_json(scoped_path(root, project["tasks"]))
        manifest = read_json(scoped_path(root, project["manifest"]))
        summary["readyTasks"] = [
            {"id": task["id"], "title": task["title"], "ownerRole": task["ownerRole"]}
            for task in board["tasks"]
            if task["status"] == "ready"
        ]
        summary["balanceSnapshotIsLive"] = manifest["budget"].get("snapshotIsLiveBalance", False)
        summary["balanceMustBeRefreshed"] = manifest["budget"]["refreshBeforeSpend"]
    report["inbox"] = []
    media_extensions = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".wav", ".mp3"}
    for folder in sorted((root / "inbox").iterdir()):
        if folder.is_dir():
            files = [path for path in folder.iterdir() if path.is_file()]
            report["inbox"].append(
                {
                    "folder": folder.name,
                    "fileCount": len(files),
                    "mediaFileCount": sum(
                        path.suffix.lower() in media_extensions for path in files
                    ),
                }
            )
    return report


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_project(root: Path) -> dict[str, Any]:
    """Return the workspace.json project entry for the active film."""
    workspace = read_json(root / "workspace.json")
    for project in workspace["projects"]:
        if project["id"] == workspace["activeFilm"]:
            return project
    raise ValueError("active film is not registered")


def film_root(root: Path, project: dict[str, Any]) -> Path:
    return scoped_path(root, project["root"])


def resolve_evidence(root: Path, film: Path, value: Any) -> Path | None:
    """Resolve a recorded path workspace-relative first, then film-relative; None if absent."""
    if not isinstance(value, str) or not value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    for base in (root, film):
        candidate = base / relative
        if candidate.is_file():
            return candidate
    return None


def hash_findings(root: Path, film: Path, handoff: dict[str, Any], label: str) -> list[str]:
    """Compare changedFiles[].sha256After and claims[].sha256 of a handoff against disk."""
    findings: list[str] = []
    records = [
        (entry.get("path"), entry.get("sha256After"), "changedFiles")
        for entry in handoff.get("changedFiles", [])
        if isinstance(entry, dict)
    ] + [
        (entry.get("evidence"), entry.get("sha256"), "claims")
        for entry in handoff.get("claims", [])
        if isinstance(entry, dict) and entry.get("sha256")
    ]
    for value, expected, section in records:
        resolved = resolve_evidence(root, film, value)
        if resolved is None:
            findings.append(f"{label}: {section} file missing on disk: {value}")
        elif sha256_file(resolved) != expected:
            findings.append(f"{label}: {section} sha256 mismatch: {value}")
    return findings


def load_handoffs(film: Path) -> list[tuple[str, dict[str, Any]]]:
    folder = film / "agents/handoffs"
    if not folder.is_dir():
        return []
    return [(path.name, read_json(path)) for path in sorted(folder.glob("*.json"))]


def ingest_status(handoff: dict[str, Any]) -> str | None:
    ingest = handoff.get("ingest")
    return ingest.get("status") if isinstance(ingest, dict) else None


def decision_ids(film: Path) -> list[str]:
    """Return canonical decision IDs from 00_brief/decisions, by field or filename prefix."""
    identifiers = []
    for path in sorted((film / "00_brief/decisions").glob("*.json")):
        record = read_json(path)
        identifiers.append(str(record.get("id") or path.stem.split("-")[0]))
    return identifiers


def read_mistakes(film: Path) -> list[dict[str, Any]] | None:
    path = film / "memory/mistakes.jsonl"
    if not path.is_file():
        return None
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entry = json.loads(line)
            require(isinstance(entry, dict), "mistakes.jsonl line is not an object")
            entries.append(entry)
    return entries


def lint_approvals(film: Path, hard: list[str], advisory: list[str]) -> None:
    manifest = read_json(film / "manifest.json")
    approvals = read_json(film / "00_brief/approvals.json")
    if "approvals" in manifest and "creativeApprovals" in approvals:
        if manifest["approvals"] != approvals["creativeApprovals"]:
            hard.append("manifest.approvals and approvals.json creativeApprovals disagree")
        advisory.append("approval flags duplicated in manifest.json and approvals.json (R06)")


def lint_decisions(film: Path, hard: list[str]) -> None:
    canonical = decision_ids(film)
    duplicates = sorted(key for key, count in Counter(canonical).items() if count > 1)
    if duplicates:
        hard.append(f"duplicate decision ids in 00_brief/decisions: {', '.join(duplicates)}")
    legacy_path = film / "memory/decisions.json"
    if legacy_path.is_file():
        legacy = read_json(legacy_path).get("decisions", [])
        collisions = sorted(
            str(entry.get("id"))
            for entry in legacy
            if isinstance(entry, dict)
            and not str(entry.get("id", "")).startswith("LEGACY-")
            and entry.get("id") in canonical
        )
        if collisions:
            hard.append(
                "memory/decisions.json ids collide with 00_brief/decisions: "
                + ", ".join(collisions)
            )


def superseded_handoff_names(handoffs: list[tuple[str, dict[str, Any]]]) -> set[str]:
    """Return handoff filenames a different handoff lists in ``supersedes``.

    The named file stays the historical delivery. Lint does not treat its stored
    hashes as a claim about the current tree. ``handoff check`` on that file
    still compares the hashes.
    """
    present = {name for name, _handoff in handoffs}
    superseded: set[str] = set()
    for name, handoff in handoffs:
        listed = handoff.get("supersedes", [])
        if not isinstance(listed, list):
            continue
        for item in listed:
            if isinstance(item, str) and item in present and item != name:
                superseded.add(item)
    return superseded


def lint_handoffs(root: Path, film: Path, hard: list[str], advisory: list[str]) -> None:
    loaded = load_handoffs(film)
    superseded = superseded_handoff_names(loaded)
    pending = []
    for name, handoff in loaded:
        if name in superseded:
            continue
        if ingest_status(handoff) in (None, "pending"):
            pending.append(name)
            if handoff.get("schemaVersion") == "2.0":
                hard.extend(hash_findings(root, film, handoff, name))
    if pending:
        advisory.append(f"{len(pending)} handoff(s) not ingested: {', '.join(pending)}")
    if superseded:
        advisory.append(
            f"{len(superseded)} handoff(s) superseded; stored hashes kept as history: "
            + ", ".join(sorted(superseded))
        )


def lint_current_plan(root: Path, film: Path, hard: list[str], advisory: list[str]) -> None:
    pointer = film / "07_generations/plans/current-plan.json"
    if not pointer.is_file():
        advisory.append("current-plan pointer missing: 07_generations/plans/current-plan.json")
        return
    plan = read_json(pointer)
    resolved = resolve_evidence(root, film, plan.get("path"))
    if resolved is None:
        hard.append(f"current-plan.json path missing on disk: {plan.get('path')}")
    elif sha256_file(resolved) != plan.get("sha256"):
        hard.append(f"current-plan.json sha256 mismatch: {plan.get('path')}")


def lint_mistakes(film: Path, advisory: list[str]) -> None:
    entries = read_mistakes(film)
    if entries is None:
        advisory.append("memory/mistakes.jsonl missing")
        return
    cutoff = dt.date.today() - dt.timedelta(days=MISTAKE_RULE_GRACE_DAYS)
    stale = []
    for entry in entries:
        if entry.get("rule_added"):
            continue
        try:
            recorded = dt.date.fromisoformat(str(entry.get("date")))
        except ValueError:
            advisory.append(f"mistakes.jsonl entry has an invalid date: {entry.get('id')}")
            continue
        if recorded < cutoff:
            stale.append(str(entry.get("id")))
    if stale:
        advisory.append(
            f"{len(stale)} mistake(s) older than {MISTAKE_RULE_GRACE_DAYS} days without "
            f"rule_added: {', '.join(stale)}"
        )


def lint_session_log(film: Path, advisory: list[str]) -> None:
    path = film / "memory/session-log.json"
    if not path.is_file():
        return
    offsets = set()
    for entry in read_json(path).get("entries", []):
        moment = dt.datetime.fromisoformat(str(entry.get("at")))
        if moment.tzinfo is not None:
            offsets.add(moment.strftime("%z"))
    if len(offsets) > 1:
        advisory.append(
            f"session-log.json entries use {len(offsets)} UTC offsets: "
            + ", ".join(sorted(offsets))
        )


def lint_git_status(root: Path, project: dict[str, Any], advisory: list[str]) -> None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--", project["root"]],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        advisory.append("git status unavailable")
        return
    if result.returncode != 0:
        advisory.append("git status unavailable")
        return
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if lines:
        shown = lines[:GIT_STATUS_CAP]
        suffix = "" if len(lines) <= GIT_STATUS_CAP else f" (+{len(lines) - GIT_STATUS_CAP} more)"
        advisory.append(
            f"{len(lines)} untracked or modified path(s) under {project['root']}: "
            + "; ".join(shown)
            + suffix
        )


def lint_blockers(root: Path, project: dict[str, Any], advisory: list[str]) -> None:
    tasks = read_json(scoped_path(root, project["tasks"]))["tasks"]
    by_id = {task["id"]: task for task in tasks}
    stale = []
    for task in tasks:
        if task.get("status") not in OPEN_TASK_STATES:
            continue
        if task.get("blocker") not in (None, "", GENERIC_BLOCKER):
            continue
        dependencies = [by_id.get(identifier, {}) for identifier in task.get("dependsOn", [])]
        if any(dependency.get("status") == "completed" for dependency in dependencies):
            stale.append(task["id"])
    if stale:
        advisory.append(
            "open tasks with generic or missing blocker text while a dependency is completed: "
            + ", ".join(stale)
        )


def lint(root: Path) -> dict[str, Any]:
    """Report hard contradictions and advisories for the active film without validate."""
    hard: list[str] = []
    advisory: list[str] = []
    report: dict[str, Any] = {"status": "ok", "hard": hard, "advisory": advisory, "film": None}
    try:
        project = active_project(root)
        film = film_root(root, project)
    except LINT_ERRORS as error:
        hard.append(f"active film unavailable: {error}")
        report["status"] = "error"
        return report
    report["film"] = project["id"]
    checks = [
        ("production-plan", lambda: lint_production_plan(root, hard, advisory)),
        ("approvals", lambda: lint_approvals(film, hard, advisory)),
        ("decisions", lambda: lint_decisions(film, hard)),
        ("handoffs", lambda: lint_handoffs(root, film, hard, advisory)),
        ("current-plan", lambda: lint_current_plan(root, film, hard, advisory)),
        ("mistakes", lambda: lint_mistakes(film, advisory)),
        ("session-log", lambda: lint_session_log(film, advisory)),
        ("git", lambda: lint_git_status(root, project, advisory)),
        ("blockers", lambda: lint_blockers(root, project, advisory)),
    ]
    for name, check in checks:
        try:
            check()
        except LINT_ERRORS as error:
            hard.append(f"lint check {name} failed: {error}")
    report["status"] = "ok" if not hard else "error"
    return report


def state_headline(path: Path) -> str | None:
    """Return the first non-empty, non-heading line of a STATE.md file."""
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return None


def resume(root: Path) -> dict[str, Any]:
    """Build the read-only session-start digest for the active film."""
    project = active_project(root)
    film = film_root(root, project)
    film_relative = project["root"]
    tasks = read_json(scoped_path(root, project["tasks"]))["tasks"]
    manifest = read_json(scoped_path(root, project["manifest"]))
    approvals = read_json(film / "00_brief/approvals.json")
    budget = manifest.get("budget", {})
    handoffs = load_handoffs(film)[-3:]
    mistakes = read_mistakes(film) or []
    lint_report = lint(root)
    return {
        "activeFilm": project["id"],
        "readOrder": [
            "AGENTS.md",
            "workspace.json",
            project["state"],
            project["manifest"],
            project["tasks"],
            f"{film_relative}/00_brief/approvals.json",
            f"{film_relative}/00_brief/decisions/",
            f"{film_relative}/tasks/plans/workflow-map-v1.md",
        ],
        "stateHeadline": state_headline(scoped_path(root, project["state"])),
        "taskCounts": dict(Counter(task["status"] for task in tasks)),
        "openTasks": [
            {
                "id": task["id"],
                "title": task.get("title"),
                "ownerRole": task.get("ownerRole"),
                "status": task["status"],
                "blocker": task.get("blocker"),
            }
            for task in tasks
            if task["status"] in OPEN_TASK_STATES
        ],
        "creativeApprovals": approvals.get("creativeApprovals", {}),
        "andreOnlyGates": approvals.get("andreOnlyGates", []),
        "balance": {
            "snapshot": budget.get("verifiedBalanceSnapshot"),
            "observedDate": budget.get("snapshotObservedDate"),
            "isLive": budget.get("snapshotIsLiveBalance", False),
        },
        "recentHandoffs": [
            {
                "name": name,
                "reviewStatus": handoff.get("reviewStatus", handoff.get("status")),
                "ingest": ingest_status(handoff),
            }
            for name, handoff in handoffs
        ],
        "openMistakes": sum(1 for entry in mistakes if not entry.get("rule_added")),
        "lint": {"hard": len(lint_report["hard"]), "advisory": len(lint_report["advisory"])},
    }


HANDOFF_V2_FIELDS = [
    "episode",
    "agentRole",
    "assignment",
    "contributorKind",
    "readFirst",
    "baseFiles",
    "changedFiles",
    "claims",
    "verification",
    "blockers",
    "andreOnlyGates",
    "proposedDecisions",
    "mistakes",
    "paidJobsSubmitted",
    "canonicalStateChanged",
    "ingest",
]
HANDOFF_OBJECT_LISTS = {
    "baseFiles": ("path", "sha256Before"),
    "changedFiles": ("path", "sha256After", "reason"),
    "claims": ("statement", "evidence", "sha256"),
    "blockers": ("description", "owner", "unblockCondition"),
    "mistakes": ("mistake", "solution"),
}
CONTRIBUTOR_KINDS = {"registry-role", "contributor"}
INGEST_STATES = {"pending", "ingested"}


def object_list_errors(handoff: dict[str, Any], key: str, fields: tuple[str, ...]) -> list[str]:
    value = handoff.get(key)
    if not isinstance(value, list):
        return [f"{key} must be a list"]
    return [
        f"{key}[{index}] must be an object with {', '.join(fields)}"
        for index, entry in enumerate(value)
        if not isinstance(entry, dict) or any(field not in entry for field in fields)
    ]


def handoff_v2_errors(handoff: dict[str, Any]) -> list[str]:
    """Return schema errors for a v2 handoff, without touching the filesystem."""
    errors = []
    for key in ("episode", "agentRole", "assignment"):
        if not isinstance(handoff.get(key), str) or not handoff.get(key):
            errors.append(f"{key} must be a non-empty string")
    if handoff.get("contributorKind") not in CONTRIBUTOR_KINDS:
        errors.append(f"contributorKind must be one of {sorted(CONTRIBUTOR_KINDS)}")
    read_first = handoff.get("readFirst")
    if not isinstance(read_first, list) or not all(isinstance(x, str) for x in read_first):
        errors.append("readFirst must be a list of strings")
    for key, fields in HANDOFF_OBJECT_LISTS.items():
        errors.extend(object_list_errors(handoff, key, fields))
    verification = handoff.get("verification")
    if not isinstance(verification, list) or not verification:
        errors.append("verification must be a non-empty list")
    for key in ("andreOnlyGates", "proposedDecisions"):
        if not isinstance(handoff.get(key), list):
            errors.append(f"{key} must be a list")
    paid = handoff.get("paidJobsSubmitted")
    if not isinstance(paid, int) or isinstance(paid, bool):
        errors.append("paidJobsSubmitted must be an integer")
    if not isinstance(handoff.get("canonicalStateChanged"), bool):
        errors.append("canonicalStateChanged must be a boolean")
    ingest = handoff.get("ingest")
    if (
        not isinstance(ingest, dict)
        or ingest.get("status") not in INGEST_STATES
        or "by" not in ingest
        or "at" not in ingest
    ):
        errors.append("ingest must be an object with status (pending|ingested), by and at")
    next_actions = handoff.get("nextActions")
    has_next = (
        isinstance(next_actions, list)
        and bool(next_actions)
        and all(
            isinstance(entry, dict) and "role" in entry and "action" in entry
            for entry in next_actions
        )
    )
    if not has_next:
        if handoff.get("stageComplete") is not True:
            errors.append(
                "nextActions must be a non-empty list of {role, action} or stageComplete true"
            )
        elif not isinstance(handoff.get("stageCompleteReason"), str):
            errors.append("stageCompleteReason must be a string when stageComplete is true")
    return errors


def resolve_handoff_argument(root: Path, value: Path) -> Path:
    if value.is_absolute() or value.exists():
        return value
    return root / value


def handoff_check(root: Path, path: Path) -> dict[str, Any]:
    """Validate a handoff file: v2 schema and hashes, or advisory field gaps for legacy."""
    report: dict[str, Any] = {"status": "ok", "version": "legacy", "errors": [], "advisory": []}
    try:
        project = active_project(root)
        film = film_root(root, project)
        handoffs = (film / "agents" / "handoffs").resolve()
        require(
            path.resolve().parent == handoffs and path.suffix == ".json",
            f"handoff must be a JSON file directly under {film.name}/agents/handoffs/",
        )
        handoff = read_json(path)
    except LINT_ERRORS as error:
        report["status"] = "error"
        report["errors"].append(str(error))
        return report
    if handoff.get("schemaVersion") != "2.0":
        missing = [key for key in HANDOFF_V2_FIELDS if key not in handoff]
        if "nextActions" not in handoff and "stageComplete" not in handoff:
            missing.append("nextActions or stageComplete")
        if missing:
            report["advisory"].append(f"legacy handoff lacks v2 fields: {', '.join(missing)}")
        return report
    report["version"] = "2.0"
    report["errors"].extend(handoff_v2_errors(handoff))
    report["errors"].extend(hash_findings(root, film, handoff, path.name))
    if report["errors"]:
        report["status"] = "error"
    return report


def handoff_ingest(root: Path, path: Path, by: str) -> dict[str, Any]:
    """Run the check and, when it passes, record ingestion in the handoff's ingest object."""
    report = handoff_check(root, path)
    if report["status"] != "ok":
        return report
    handoff = read_json(path)
    if ingest_status(handoff) == "ingested":
        report["status"] = "error"
        report["errors"].append("already ingested")
        return report
    handoff["ingest"] = {
        "status": "ingested",
        "by": by,
        "at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report["ingested"] = True
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="check workspace integrity")
    commands.add_parser("status", help="validate and report pending state")
    commands.add_parser("lint", help="report hard contradictions and advisories")
    commands.add_parser("resume", help="print the session-start digest")
    handoff = commands.add_parser("handoff", help="check or ingest a handoff file")
    actions = handoff.add_subparsers(dest="action", required=True)
    check = actions.add_parser("check", help="validate a handoff and its hashes")
    check.add_argument("path", type=Path)
    ingest = actions.add_parser("ingest", help="record producer ingestion of a handoff")
    ingest.add_argument("path", type=Path)
    ingest.add_argument("--by", required=True)
    return parser


def main() -> int:
    arguments = build_parser().parse_args()
    root = arguments.root.resolve()
    if arguments.command == "resume":
        print(json.dumps(resume(root), ensure_ascii=False, indent=2))
        return 0
    if arguments.command == "handoff":
        path = resolve_handoff_argument(root, arguments.path)
        if arguments.action == "ingest":
            report = handoff_ingest(root, path, arguments.by)
        else:
            report = handoff_check(root, path)
    else:
        commands = {"validate": validate, "status": status, "lint": lint}
        report = commands[arguments.command](root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
