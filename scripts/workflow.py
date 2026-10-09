#!/usr/bin/env python3
"""Local handoff inventory and clean continuation drafts; no provider integration."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re

from manage import DEFAULT_ROOT, require, scoped_path

SCAN_ROOTS = [
    ".gitignore", ".gitattributes", "AGENTS.md", "README.md", "START_HERE.md",
    "workspace.json", "pyproject.toml",
    "agents", "docs", "inbox", "memory", "projects", "scripts", "shared", "series",
    "tests", "drafts", "skills/andre-time-travel", "skills/registry.json", "reports",
]
SKIP_PARTS = {"__pycache__", ".ruff_cache", ".pytest_cache", ".venv", ".git"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def write_new(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def files_in_scope(root: Path, excluded: set[str]) -> list[Path]:
    files: set[Path] = set()
    for name in SCAN_ROOTS:
        base = scoped_path(root, name)
        candidates = base.rglob("*") if base.is_dir() else [base]
        for path in candidates:
            relative = path.relative_to(root)
            if (path.is_symlink() or not path.is_file()
                    or SKIP_PARTS.intersection(relative.parts)
                    or relative.as_posix() in excluded):
                continue
            require(path.resolve().is_relative_to(root.resolve()), "inventory path escapes workspace")
            files.add(path)
    return sorted(files)


def category(path: str) -> str:
    if path.startswith("inbox/"):
        return "incoming_original_or_candidate_not_automatically_approved"
    if "/source/" in path or "/01_script/" in path or "/03_bibles/" in path:
        return "editable_creative_source"
    if "/02_references/" in path:
        return "reference_check_canonical_registry_for_classification_and_approval"
    if "/07_generations/" in path:
        return "provider_request_response_or_original"
    if "/04_audio/" in path:
        return "audio_or_provenance"
    if "/05_storyboard/" in path:
        return "storyboard_or_derived_review_artifact"
    if path.startswith("drafts/"):
        return "unregistered_continuation_draft"
    return "management_documentation_or_evidence"


def inventory(root: Path, output: str) -> dict:
    target = scoped_path(root, output)
    require(not target.exists(), "inventory exists; choose a new snapshot filename")
    records = []
    for path in files_in_scope(root, {output}):
        relative = path.relative_to(root).as_posix()
        records.append({"path": relative, "bytes": path.stat().st_size,
                        "sha256": digest(path), "category": category(relative)})
    result = {
        "schemaVersion": "1.0", "createdAt": now(), "pathBase": "workspace",
        "scope": SCAN_ROOTS, "excludedPaths": [output],
        "excludedKinds": ["external skill symlinks", "runtime environments", "cache files"],
        "approvalPolicy": "Inventory presence and hash equality never imply creative approval.",
        "fileCount": len(records), "totalBytes": sum(r["bytes"] for r in records),
        "files": records,
    }
    write_new(target, result)
    return {k: result[k] for k in ("fileCount", "totalBytes", "createdAt")}


def verify(root: Path, index: str) -> dict:
    data = json.loads(scoped_path(root, index).read_text(encoding="utf-8"))
    missing, changed = [], []
    paths = [r["path"] for r in data["files"]]
    require(len(paths) == len(set(paths)), "duplicate inventory paths")
    for record in data["files"]:
        path = scoped_path(root, record["path"])
        if not path.is_file():
            missing.append(record["path"])
        elif digest(path) != record["sha256"]:
            changed.append(record["path"])
    current = {p.relative_to(root).as_posix()
               for p in files_in_scope(root, set(data.get("excludedPaths", [])) | {index})}
    added = sorted(current - set(paths))
    return {"status": "ok" if not (missing or changed) else "changed",
            "checkedFiles": len(paths), "missing": missing, "changed": changed,
            "addedSinceSnapshot": added, "creativeApproval": "not_evaluated"}


def new_draft(root: Path, identifier: str, title: str, test_only: bool = False) -> dict:
    require(bool(re.fullmatch(r"[a-z][a-z0-9-]{2,63}", identifier)), "invalid draft identifier")
    require(bool(title.strip()), "title is required")
    template = json.loads((root / "shared/templates/continuation.json").read_text())
    target = scoped_path(root, f"drafts/{identifier}")
    require(not target.exists(), "draft exists; never overwrite a continuation")
    for directory in template["directories"]:
        scoped_path(target, directory)  # Validate every template path before writing anything.
    data = template["episode"]
    data.update(id=identifier, workingTitle=title, createdAt=now(), testOnly=test_only)
    data["seriesRules"] = "series/andre-time-travel/series.json"
    target.mkdir(parents=True, exist_ok=False)
    for directory in template["directories"]:
        scoped_path(target, directory).mkdir(parents=True, exist_ok=True)
    write_new(target / "00_brief/episode.json", data)
    write_new(target / "00_brief/approvals.json", template["approvals"])
    write_new(target / "02_references/reuse-requests.json", {
        "schemaVersion": "1.0", "requests": [],
        "rule": "Request a specific source version/hash and scope; never inherit approval or jobs."
    })
    write_new(target / "tasks/board.json", {"schemaVersion": "1.0", "tasks": template["tasks"]})
    write_new(target / "memory/session-log.json", {"schemaVersion": "1.0", "entries": [{
        "at": now(), "event": "clean_draft_created", "testOnly": test_only,
        "paidJobs": 0, "creativeApprovalsInherited": 0,
    }]})
    (target / "01_script/script.md").write_text(
        "# " + title + "\n\nRascunho sem história definida. Preencher objetivo dramático, "
        "encontro, consequência, retorno ao presente e fontes antes da decupagem.\n")
    (target / "01_script/dialogue-lines.csv").write_text(
        "line_id,speaker,text,language,audio_path,measured_seconds,approved\n")
    (target / "05_storyboard/shot-list.csv").write_text(
        "shot_id,chapter,target_seconds,description,framing_restriction,accepted_take_id\n")
    (target / "credit-ledger.csv").write_text(
        "entry_id,recorded_at,provider,generation_id,credits_consumed,charge_status,authorization_ref\n")
    (target / "memory/STATE.md").write_text(
        "# Continuação em preparação\n\n" + ("ENSAIO LOCAL — não é um episódio em produção.\n\n"
        if test_only else "Rascunho não registrado como produção.\n\n")
        + "Nenhuma história, referência, voz, compra, job ou take aprovado. "
        "Começar pelo briefing; consultar START_HERE.md e docs/REPEATABLE_WORKFLOW.md "
        "na raiz. O filme ativo não foi alterado.\n")
    (target / "README.md").write_text(
        "# " + title + "\n\n" + ("**ENSAIO, SEM PRODUÇÃO.**\n\n" if test_only else "")
        + "Esta pasta é um rascunho independente, não um clone do filme anterior. "
        "Os arquivos são editáveis. Aprovações, orçamento e mídia começam vazios. "
        "Ainda não satisfaz o manifesto de uma produção.\n\n"
        "Ao definir o briefing, o produtor cria o manifesto, plano de tomadas e dependências "
        "do novo episódio, valida sua consistência e só então registra a produção.\n")
    return {"status": "created", "path": target.relative_to(root).as_posix(),
            "testOnly": test_only, "registeredAsActiveFilm": False, "paidJobs": 0}


def check_clean_draft(root: Path, relative: str) -> dict:
    target = scoped_path(root, relative)
    template = json.loads((root / "shared/templates/continuation.json").read_text())
    episode = json.loads((target / "00_brief/episode.json").read_text())
    approvals = json.loads((target / "00_brief/approvals.json").read_text())
    require(episode["state"] == "draft_unregistered", "draft already advanced")
    require(episode["chapters"] == [] and episode["targetSeconds"] is None,
            "clean draft cannot inherit chapter layout or runtime")
    require(episode["budget"] == template["episode"]["budget"], "draft inherited a budget")
    require(episode["providerJobs"] == [] and episode["acceptedTakes"] == [],
            "draft inherited provider jobs or takes")
    require(approvals == template["approvals"], "draft inherited approvals")
    require(episode["constraints"] == template["episode"]["constraints"],
            "series constraints differ from the template")
    for directory in template["directories"]:
        require(scoped_path(target, directory).is_dir(), "draft directory missing")
    for relative_file in ("01_script/dialogue-lines.csv", "05_storyboard/shot-list.csv",
                          "credit-ledger.csv"):
        require(len((target / relative_file).read_text().splitlines()) == 1,
                "clean draft inherited production rows")
    board = json.loads((target / "tasks/board.json").read_text())
    require(board["tasks"] == template["tasks"], "clean draft inherited task progress")
    return {"status": "ok", "testOnly": episode["testOnly"], "paidJobs": 0,
            "inheritedApprovals": 0, "runtimeAndChapterCountInherited": False,
            "scope": "clean starting template only; not production acceptance"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("index").add_argument("--output", required=True)
    sub.add_parser("verify").add_argument("--index", required=True)
    draft = sub.add_parser("new-draft")
    draft.add_argument("--id", required=True)
    draft.add_argument("--title", required=True)
    draft.add_argument("--test-only", action="store_true")
    sub.add_parser("check-clean-draft").add_argument("--path", required=True)
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if args.command == "index":
            report = inventory(root, args.output)
        elif args.command == "verify":
            report = verify(root, args.index)
        elif args.command == "new-draft":
            report = new_draft(root, args.id, args.title, args.test_only)
        else:
            report = check_clean_draft(root, args.path)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("status") not in {"changed", "error"} else 2
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
