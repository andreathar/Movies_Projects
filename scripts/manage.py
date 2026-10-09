#!/usr/bin/env python3
"""Read-only, offline status and validation for the Movies_Projects workspace."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
TASK_STATES = {"pending", "ready", "blocked", "in_progress", "completed", "cancelled"}


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("command", choices=["validate", "status"])
    arguments = parser.parse_args()
    report = (status if arguments.command == "status" else validate)(arguments.root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
