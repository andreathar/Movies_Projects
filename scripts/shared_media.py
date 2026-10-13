"""Resolves canonical inputs and validates the existing asset registry.

No command here modifies the registry, hydrates LFS, grants access or approves
an asset. Hashes in legacy source text are proposals, never fresh verification.
"""

from __future__ import annotations

import csv
from collections import Counter
import hashlib
import re
from pathlib import Path

HEADER = [
    "asset_id", "kind", "path_or_provider_id", "path_base", "source",
    "sha256", "approved", "notes",
]
HASH = re.compile(r"^[0-9a-f]{64}$")


def scoped(root: Path, value: str, *, file: bool = True) -> Path:
    """Contains a literal relative path within one explicit root."""
    if (
        not isinstance(value, str) or not value or not value.isprintable()
        or "\\" in value or ":" in value or Path(value).is_absolute()
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise ValueError("path must be relative without traversal or a drive")
    root = root.resolve()
    result = (root / value).resolve()
    if not result.is_relative_to(root):
        raise ValueError("path escapes its declared root through a symlink")
    if file and not result.is_file():
        raise ValueError("input absent from the canonical media root: " + value)
    return result


def input_path(film: Path, value: str, *, media_root: Path | None = None) -> Path:
    """Uses an explicit canonical film root, preserving containment checks."""
    return scoped(media_root if media_root is not None else film, value)


def output_path(media_root: Path, output_root: Path, value: str) -> Path:
    """Resolves a task derivative without allowing overlap with originals."""
    canonical, output = media_root.resolve(), output_root.resolve()
    if output.is_relative_to(canonical) or canonical.is_relative_to(output):
        raise ValueError("task output root must be separate from canonical media")
    target = scoped(output, value, file=False)
    if target.exists() or target.is_symlink():
        raise ValueError("output already exists; choose a new task/version, never overwrite")
    return target


def _legacy(row: list[str], root: Path, film: Path) -> dict | None:
    """Proposes only six-field legacy values whose bases are unambiguous."""
    if len(row) != 6 or row[4] not in {"true", "false"}:
        return None
    hashes = re.findall(r"sha256=([0-9a-f]{64})(?![0-9a-f])", row[3])
    if len(hashes) != 1:
        return None
    bases = []
    for label, base in (("workspace", root), ("film", film)):
        try:
            scoped(base, row[2])
        except ValueError:
            continue
        bases.append(label)
    if len(bases) != 1:
        return None
    return {
        "candidate": dict(zip(HEADER, [*row[:3], bases[0], row[3], hashes[0], *row[4:]])),
        "basis": "six-field legacy shape; one existing contained path base; embedded hash",
        "hash_verified": False, "applied": False,
    }


def read_catalog(root: Path, film_relative: str) -> dict:
    """Parses exact CSV records with line provenance instead of shifting fields."""
    root = root.resolve()
    film = scoped(root, film_relative, file=False)
    path = scoped(root, film_relative + "/asset-registry.csv")
    if not path.is_file() or path.stat().st_size > 4 * 1024 * 1024:
        raise ValueError("catalog missing or too large; select the canonical film")
    records, errors, proposals = [], [], []
    seen: set[str] = set()
    identifiers: Counter[str] = Counter()
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.reader(stream, strict=True)
        if next(reader, None) != HEADER:
            raise ValueError("asset registry header differs from its eight-column schema")
        for row in reader:
            line = reader.line_num
            identifier = row[0] if row else ""
            duplicated = identifier in seen
            if identifier:
                identifiers[identifier] += 1
                seen.add(identifier)
            if len(records) + len(errors) > 10000:
                raise ValueError("catalog record limit exceeded")
            if len(row) != len(HEADER):
                errors.append({"line": line, "code": "CSV_WIDTH", "columns": len(row), "expected": len(HEADER), "asset_id": identifier or None, "duplicate_asset_id": duplicated})
                if proposal := _legacy(row, root, film):
                    proposals.append({"line": line, **proposal})
                continue
            record = dict(zip(HEADER, row))
            identifier = record["asset_id"]
            problems = []
            if not identifier or duplicated:
                problems.append("asset ID absent or duplicated")
            if record["path_base"] not in {"film", "workspace", "provider"}:
                problems.append("path_base must be film/workspace/provider")
            if record["sha256"] and not HASH.fullmatch(record["sha256"]):
                problems.append("sha256 is not a lower-case 64-character digest")
            if record["approved"] not in {"true", "false"}:
                problems.append("approved must be true/false; never inferred")
            if record["path_base"] in {"film", "workspace"}:
                try:
                    scoped(film if record["path_base"] == "film" else root, record["path_or_provider_id"])
                except ValueError as error:
                    problems.append(str(error))
            if problems:
                errors.append({"line": line, "code": "ASSET_INVALID", "asset_id": identifier, "errors": problems})
            records.append({**record, "line": line, "valid": not problems})
    duplicate_ids = {identifier: count for identifier, count in identifiers.items() if count > 1}
    for proposal in proposals:
        proposal["identity_conflict"] = proposal["candidate"]["asset_id"] in duplicate_ids
    return {
        "schema": "movies/assets/read/v1", "status": "error" if errors else "ok",
        "read_only": True, "catalog": str(path),
        "catalog_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "records": records, "errors": errors, "proposals": proposals,
        "duplicate_asset_ids": duplicate_ids,
        "proposals_applied": False,
    }


def resolve_asset(root: Path, film_relative: str, asset_id: str) -> dict:
    """Fails on invalid registry data rather than inventing missing columns."""
    report = read_catalog(root, film_relative)
    if report["errors"]:
        raise ValueError("asset registry invalid; run assets validate and review proposals")
    matches = [record for record in report["records"] if record["asset_id"] == asset_id]
    if len(matches) != 1:
        raise ValueError("asset ID absent or ambiguous")
    record = matches[0]
    if record["path_base"] == "provider":
        raise ValueError("provider ID is not a local file; no download attempted")
    base = scoped(root, film_relative, file=False) if record["path_base"] == "film" else root
    path = scoped(base, record["path_or_provider_id"])
    with path.open("rb") as stream:
        if stream.read(80).startswith(b"version https://git-lfs.github.com/spec/v1"):
            raise ValueError("asset is an LFS pointer; hydrate the canonical source explicitly")
    return {"asset_id": asset_id, "path": str(path), "recorded_sha256": record["sha256"] or None, "hash_verified": False, "approved": record["approved"] == "true", "bytes": path.stat().st_size}
