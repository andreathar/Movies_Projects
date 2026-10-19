"""Isolated greenfield production management. Python stdlib only; no provider calls.

The CLI trusts possession of a private local credential, never an actor/role argument.
This is an application boundary, not a sandbox against the database's OS owner.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import sqlite3
import sys

SCHEMA = Path(__file__).with_name("production_schema.sql")


class ManagementError(ValueError):
    """Rejected operation; no database mutation was committed."""


def required(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManagementError("non-empty text required")
    return value.strip()


def identifier(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", required(value)):
        raise ManagementError("invalid identifier")
    return value


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def private_file(path: Path, content: str) -> None:
    # No overwrite and no credential in stdout or the audit log.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


def credential(path: Path) -> str:
    if path.is_symlink() or path.stat().st_mode & 0o077:
        raise ManagementError("credential must be a private regular file (mode 600)")
    if not path.is_file():
        raise ManagementError("credential must be a private regular file (mode 600)")
    return required(path.read_text(encoding="utf-8"))


class Store:
    def __init__(self, database: Path, root: Path):
        self.database = database.resolve()
        self.root = root.resolve(strict=True)

    @classmethod
    def initialize(cls, database: Path, root: Path, owner: str, credential_out: Path):
        identifier(owner)
        root = root.resolve(strict=True)
        if not root.is_dir():
            raise ManagementError("workspace root must be a directory")
        # Parent directories must already exist: no implicit setup elsewhere.
        fd = os.open(database, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
        created_credential = False
        try:
            token = secrets.token_urlsafe(32)
            private_file(credential_out, token + "\n")
            created_credential = True
            with sqlite3.connect(database) as connection:
                connection.execute("PRAGMA foreign_keys=ON")
                connection.executescript(SCHEMA.read_text(encoding="utf-8"))
                connection.execute("INSERT INTO workspace_anchor VALUES (?)", (str(root),))
                connection.execute("INSERT INTO identities VALUES (?,?,1)", (owner, digest(token.encode())))
                result = {"after": {"owner": owner, "schemaVersion": 1}}
                connection.execute(
                    "INSERT INTO events(actor_id,command,request_id,fingerprint,reason,occurred_at,result) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (owner, "initialize", "bootstrap", digest(b"bootstrap"), "Explicit clean initialization",
                     datetime.now(timezone.utc).isoformat(), encoded(result)),
                )
            return cls(database, root)
        except BaseException:
            database.unlink(missing_ok=True)
            if created_credential:
                credential_out.unlink(missing_ok=True)
            raise

    @contextmanager
    def _connect(self, write=False):
        # mode=rw refuses missing files instead of silently making an empty database.
        connection = sqlite3.connect(self.database.as_uri() + "?mode=rw", uri=True, timeout=5)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            version = connection.execute("SELECT version FROM schema_version").fetchall()
            if len(version) != 1 or version[0][0] != 1:
                raise ManagementError("unsupported database schema")
            anchors = connection.execute("SELECT root FROM workspace_anchor").fetchall()
            if len(anchors) != 1 or anchors[0][0] != str(self.root):
                raise ManagementError("workspace root differs from database anchor")
            connection.execute("BEGIN IMMEDIATE" if write else "BEGIN")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _one(connection, table, key):
        row = connection.execute(f"SELECT * FROM {table} WHERE id=?", (key,)).fetchone()
        if row is None:
            raise ManagementError(f"{table}: record not found")
        return dict(row)

    @staticmethod
    def _actor(connection, token):
        row = connection.execute("SELECT id,is_operator FROM identities WHERE token_hash=?",
                                 (digest(token.encode()),)).fetchone()
        if row is None:
            raise ManagementError("invalid credential")
        return dict(row)

    def _member(self, connection, actor, project, producer=False):
        self._one(connection, "projects", project)
        if actor["is_operator"]:
            return
        row = connection.execute("SELECT role FROM memberships WHERE project_id=? AND identity_id=?",
                                 (project, actor["id"])).fetchone()
        if row is None or (producer and row[0] != "producer"):
            raise ManagementError("project permission denied")

    @staticmethod
    def _operator(actor):
        if not actor["is_operator"]:
            raise ManagementError("operator credential required")

    def _task(self, connection, actor, args, *, producer=False):
        task = self._one(connection, "tasks", args["task"])
        self._member(connection, actor, task["project_id"], producer)
        if task["revision"] != args["revision"]:
            raise ManagementError("stale revision; reload before retrying")
        return task

    def _local_path(self, path):
        value = required(path)
        pure = PurePosixPath(value)
        if pure.is_absolute() or ".." in pure.parts or "\\" in value or str(pure) != value or value == ".":
            raise ManagementError("canonical workspace-relative file path required")
        resolved = (self.root / value).resolve()
        if not resolved.is_relative_to(self.root):
            raise ManagementError("path escapes workspace")
        return resolved

    def _check_artifact(self, artifact):
        path = self._local_path(artifact["path"])
        if not path.is_file() or digest(path.read_bytes()) != artifact["sha256"]:
            raise ManagementError("artifact is missing or its bytes changed")

    def _artifacts(self, connection, project, ids):
        for artifact_id in ids:
            artifact = self._one(connection, "artifact_versions", artifact_id)
            if artifact["project_id"] != project:
                raise ManagementError("cross-project artifact")
            self._check_artifact(artifact)
            yield artifact

    @staticmethod
    def _dependencies_ready(connection, task_id):
        if connection.execute(
            "SELECT 1 FROM task_dependencies d JOIN tasks t ON t.id=d.dependency_id "
            "WHERE d.task_id=? AND t.state<>'completed'", (task_id,),
        ).fetchone():
            raise ManagementError("task dependencies are not completed")

    @staticmethod
    def _update_task(connection, task, **changes):
        changes["revision"] = task["revision"] + 1
        connection.execute("UPDATE tasks SET " + ",".join(f"{k}=?" for k in changes) + " WHERE id=?",
                           (*changes.values(), task["id"]))
        return {"before": task, "after": {**task, **changes}}

    def execute(self, token: str, command: str, args: dict, *, request_id: str, reason: str):
        identifier(request_id)
        required(reason)
        fingerprint = digest(encoded([command, args, reason]).encode())
        with self._connect(write=True) as connection:
            actor = self._actor(connection, token)
            previous = connection.execute(
                "SELECT fingerprint,result FROM events WHERE actor_id=? AND request_id=?",
                (actor["id"], request_id),
            ).fetchone()
            if previous:
                if previous["fingerprint"] != fingerprint:
                    raise ManagementError("request id already used with different content")
                return json.loads(previous["result"])
            result, project = self._perform(connection, actor, command, args, reason)
            connection.execute(
                "INSERT INTO events(actor_id,project_id,command,request_id,fingerprint,reason,payload,occurred_at,result) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (actor["id"], project, command, request_id, fingerprint, reason, encoded(args),
                 datetime.now(timezone.utc).isoformat(), encoded(result)),
            )
            return result

    def add_identity(self, token, identity, credential_out: Path, *, request_id, reason):
        """Operator-only provisioning; credential files are never audit payloads."""
        identifier(identity)
        created = False
        try:
            with self._connect(write=True) as connection:
                actor = self._actor(connection, token)
                self._operator(actor)
                identifier(request_id)
                required(reason)
                if connection.execute("SELECT 1 FROM events WHERE actor_id=? AND request_id=?",
                                      (actor["id"], request_id)).fetchone():
                    raise ManagementError("provisioning request already used; do not replace credentials")
                secret = secrets.token_urlsafe(32)
                connection.execute("INSERT INTO identities VALUES (?,?,0)", (identity, digest(secret.encode())))
                private_file(credential_out, secret + "\n")
                created = True
                result = {"after": {"identity": identity}}
                connection.execute(
                    "INSERT INTO events(actor_id,command,request_id,fingerprint,reason,occurred_at,result) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (actor["id"], "identity-add", request_id, digest(identity.encode()), reason,
                     datetime.now(timezone.utc).isoformat(), encoded(result)),
                )
            return result
        except BaseException:
            if created:
                credential_out.unlink(missing_ok=True)
            raise

    def _perform(self, c, actor, command, a, reason):
        if command == "project-create":
            self._operator(actor)
            identifier(a["project"])
            c.execute("INSERT INTO projects VALUES (?,?)", (a["project"], required(a["title"])))
            return {"after": self._one(c, "projects", a["project"])}, a["project"]
        if command == "member-add":
            self._operator(actor)
            self._one(c, "projects", a["project"])
            self._one(c, "identities", a["user"])
            if a["role"] not in {"producer", "contributor", "reviewer"}:
                raise ManagementError("invalid project role")
            c.execute("INSERT INTO memberships VALUES (?,?,?)", (a["project"], a["user"], a["role"]))
            return {"after": a}, a["project"]
        if command == "task-create":
            project = a["project"]
            self._member(c, actor, project, producer=True)
            identifier(a["id"])
            c.execute("INSERT INTO tasks(id,project_id,title,state,responsible_id) VALUES (?,?,?,'ready',?)",
                      (a["id"], project, required(a["title"]), actor["id"]))
            # Dependencies point only to existing tasks; no dependency-update command exists.
            for dependency in a.get("depends_on", []):
                if self._one(c, "tasks", dependency)["project_id"] != project:
                    raise ManagementError("cross-project dependency")
                c.execute("INSERT INTO task_dependencies VALUES (?,?)", (a["id"], dependency))
            return {"after": self._one(c, "tasks", a["id"]), "dependencies": a.get("depends_on", [])}, project
        if command in {"task-offer", "task-accept", "task-block"}:
            task = self._task(c, actor, a, producer=command != "task-accept")
            project = task["project_id"]
            if command == "task-offer":
                if task["state"] not in {"ready", "offered", "blocked"}:
                    raise ManagementError("task cannot be offered in this state")
                self._dependencies_ready(c, task["id"])
                self._member(c, {"id": a["to"], "is_operator": 0}, project)
                scope = required(a["scope"])
                c.execute("DELETE FROM task_allowed_paths WHERE task_id=?", (task["id"],))
                for path in a.get("allowed_path", []):
                    self._local_path(path)
                    c.execute("INSERT INTO task_allowed_paths VALUES (?,?)", (task["id"], path))
                c.execute("DELETE FROM task_inputs WHERE task_id=?", (task["id"],))
                for artifact in self._artifacts(c, project, a.get("input", [])):
                    c.execute("INSERT INTO task_inputs VALUES (?,?)", (task["id"], artifact["id"]))
                return self._update_task(c, task, state="offered", offered_to=a["to"],
                                         assignment_scope=scope, assignment_version=task["assignment_version"] + 1,
                                         responsible_id=actor["id"],
                                         blocker_owner=None, unblock_condition=None), project
            if command == "task-accept":
                if task["state"] != "offered" or task["offered_to"] != actor["id"]:
                    raise ManagementError("only the offered recipient may accept")
                self._dependencies_ready(c, task["id"])
                inputs = [r[0] for r in c.execute("SELECT artifact_id FROM task_inputs WHERE task_id=?", (task["id"],))]
                list(self._artifacts(c, project, inputs))
                return self._update_task(c, task, state="active", responsible_id=actor["id"]), project
            if task["state"] not in {"ready", "offered", "active", "blocked"}:
                raise ManagementError("task cannot be blocked in this state")
            self._member(c, {"id": a["owner"], "is_operator": 0}, project)
            return self._update_task(c, task, state="blocked", blocker_owner=a["owner"],
                                     unblock_condition=required(a["condition"]), offered_to=None,
                                     responsible_id=actor["id"]), project
        if command == "artifact-add":
            task = self._task(c, actor, a)
            project = task["project_id"]
            if task["state"] != "active" or task["responsible_id"] != actor["id"]:
                raise ManagementError("artifact requires an active accepted assignment")
            if not c.execute("SELECT 1 FROM task_allowed_paths WHERE task_id=? AND path=?",
                             (task["id"], a["path"])).fetchone():
                raise ManagementError("artifact path is outside the assignment")
            path = self._local_path(a["path"])
            identifier(a["id"])
            supersedes = a.get("supersedes")
            if supersedes and self._one(c, "artifact_versions", supersedes)["project_id"] != project:
                raise ManagementError("cross-project artifact")
            c.execute("INSERT INTO artifact_versions VALUES (?,?,?,?,?,?,?,?)",
                      (a["id"], task["id"], project, a["path"], digest(path.read_bytes()), actor["id"],
                       task["assignment_version"], supersedes))
            return {"after": self._one(c, "artifact_versions", a["id"])}, project
        if command == "handoff-submit":
            task = self._task(c, actor, a)
            project = task["project_id"]
            if task["state"] != "active" or task["responsible_id"] != actor["id"]:
                raise ManagementError("handoff requires the accepted task owner")
            identifier(a["id"])
            artifacts = list(self._artifacts(c, project, a.get("artifact", [])))
            if not artifacts or not a.get("check"):
                raise ManagementError("handoff requires artifacts and explicit checks")
            if any(v["task_id"] != task["id"] or v["assignment_version"] != task["assignment_version"]
                   for v in artifacts):
                raise ManagementError("handoff outputs must belong to this assignment")
            c.execute("INSERT INTO handoffs(id,task_id,submitted_by,scope,limitations,state) "
                      "VALUES (?,?,?,?,?,'submitted')", (a["id"], task["id"], actor["id"],
                                                        required(a["scope"]), required(a["limitations"])))
            for artifact in artifacts:
                c.execute("INSERT INTO handoff_artifacts VALUES (?,?)", (a["id"], artifact["id"]))
            for name, result, evidence in a["check"]:
                c.execute("INSERT INTO handoff_checks VALUES (?,?,?,?)",
                          (a["id"], required(name), result, required(evidence)))
            for dependency in a.get("dependency", []):
                if self._one(c, "tasks", dependency)["project_id"] != project:
                    raise ManagementError("cross-project dependency")
                c.execute("INSERT INTO handoff_dependencies VALUES (?,?)", (a["id"], dependency))
            for decision in a.get("open_decision", []):
                if self._one(c, "decisions", decision)["project_id"] != project:
                    raise ManagementError("cross-project decision")
                c.execute("INSERT INTO handoff_open_decisions VALUES (?,?)", (a["id"], decision))
            change = self._update_task(c, task, state="delivered")
            return {"task": change, "after": self._one(c, "handoffs", a["id"]),
                    "artifacts": [v["id"] for v in artifacts], "checks": a["check"]}, project
        if command in {"handoff-verify", "handoff-integrate", "handoff-return"}:
            handoff = self._one(c, "handoffs", a["handoff"])
            task = self._one(c, "tasks", handoff["task_id"])
            project = task["project_id"]
            self._member(c, actor, project, producer=True)
            if handoff["revision"] != a["revision"]:
                raise ManagementError("stale revision; reload before retrying")
            if command == "handoff-return":
                if handoff["state"] not in {"submitted", "verified"}:
                    raise ManagementError("only a pending handoff may be returned")
                c.execute("UPDATE handoffs SET state='returned',revision=revision+1 WHERE id=?", (handoff["id"],))
                change = self._update_task(c, task, state="active")
                return {"before": handoff, "after": self._one(c, "handoffs", handoff["id"]), "task": change}, project
            artifacts = [r[0] for r in c.execute("SELECT artifact_id FROM handoff_artifacts WHERE handoff_id=?", (handoff["id"],))]
            list(self._artifacts(c, project, artifacts))
            if command == "handoff-verify":
                if handoff["state"] != "submitted":
                    raise ManagementError("handoff must be submitted")
                c.execute("UPDATE handoffs SET state='verified',revision=revision+1 WHERE id=?", (handoff["id"],))
                return {"before": handoff, "after": self._one(c, "handoffs", handoff["id"])}, project
            if handoff["state"] != "verified":
                raise ManagementError("handoff must be verified before integration")
            successor = a.get("successor")
            blocked = a.get("blocker_owner")
            if sum(bool(v) for v in (successor, blocked, a.get("closed"))) != 1:
                raise ManagementError("choose accepted successor, owned blocker, or closed stage")
            if successor:
                next_task = self._one(c, "tasks", successor)
                if next_task["project_id"] != project or next_task["state"] != "active" or successor == task["id"]:
                    raise ManagementError("successor must be a different accepted active task in this project")
                closure = "successor"
            elif blocked:
                self._member(c, {"id": blocked, "is_operator": 0}, project)
                required(a.get("condition", ""))
                closure = "blocked"
            else:
                closure = "closed"
            c.execute("UPDATE handoffs SET state='integrated',revision=revision+1,successor_task_id=?,"
                      "closure=?,blocker_owner=?,unblock_condition=? WHERE id=?",
                      (successor, closure, blocked, a.get("condition") if blocked else None, handoff["id"]))
            change = self._update_task(c, task, state="completed")
            return {"before": handoff, "after": self._one(c, "handoffs", handoff["id"]), "task": change}, project
        if command == "decision-record":
            project = a["project"]
            self._member(c, actor, project, producer=True)
            identifier(a["id"])
            supersedes = a.get("supersedes")
            if supersedes and self._one(c, "decisions", supersedes)["project_id"] != project:
                raise ManagementError("cross-project decision")
            c.execute("INSERT INTO decisions VALUES (?,?,?,?,?,?)",
                      (a["id"], project, required(a["title"]), reason, actor["id"], supersedes))
            return {"after": self._one(c, "decisions", a["id"])}, project
        if command == "approval-record":
            self._operator(actor)
            artifact = self._one(c, "artifact_versions", a["artifact"])
            if a["outcome"] == "approved":
                self._check_artifact(artifact)
            identifier(a["id"])
            purpose = required(a["purpose"])
            supersedes = a.get("supersedes")
            if supersedes:
                prior = self._one(c, "approvals", supersedes)
                if prior["artifact_id"] != artifact["id"] or prior["purpose"] != purpose:
                    raise ManagementError("approval correction must retain artifact and purpose")
                if c.execute("SELECT 1 FROM approvals WHERE supersedes=?", (supersedes,)).fetchone():
                    raise ManagementError("approval correction must target the current leaf")
            elif c.execute("SELECT 1 FROM approvals WHERE artifact_id=? AND purpose=?",
                           (artifact["id"], purpose)).fetchone():
                raise ManagementError("existing approval must be explicitly superseded")
            c.execute("INSERT INTO approvals VALUES (?,?,?,?,?,?,?)",
                      (a["id"], artifact["id"], purpose, a["outcome"], reason, actor["id"], supersedes))
            return {"after": self._one(c, "approvals", a["id"])}, artifact["project_id"]
        raise ManagementError("unsupported command")

    def projects(self, token):
        with self._connect() as c:
            actor = self._actor(c, token)
            if actor["is_operator"]:
                rows = c.execute("SELECT id,title FROM projects ORDER BY id")
            else:
                rows = c.execute("SELECT p.id,p.title FROM projects p JOIN memberships m "
                                 "ON p.id=m.project_id WHERE m.identity_id=? ORDER BY p.id", (actor["id"],))
            return [dict(row) for row in rows]

    def snapshot(self, token, project, kinds):
        """All projections share one authorized SQLite read transaction."""
        with self._connect() as c:
            actor = self._actor(c, token)
            self._member(c, actor, project)
            return {kind: self._query(c, project, kind) for kind in kinds}

    def query(self, token, project, kind):
        return self.snapshot(token, project, [kind])[kind]

    @staticmethod
    def _query(c, project, kind):
        tables = {"tasks", "artifact_versions", "decisions", "events"}
        if kind in tables:
            rows = c.execute(f"SELECT * FROM {kind} WHERE project_id=? ORDER BY " +
                             ("sequence" if kind == "events" else "id"), (project,))
        elif kind == "handoffs":
            rows = c.execute("SELECT h.* FROM handoffs h JOIN tasks t ON h.task_id=t.id WHERE t.project_id=? ORDER BY h.id", (project,))
        elif kind == "approvals":
            rows = c.execute("SELECT a.* FROM approvals a JOIN artifact_versions v ON a.artifact_id=v.id WHERE v.project_id=? ORDER BY a.id", (project,))
        elif kind in {"task_dependencies", "task_allowed_paths", "task_inputs"}:
            rows = c.execute(f"SELECT r.* FROM {kind} r JOIN tasks t ON r.task_id=t.id WHERE t.project_id=?", (project,))
        elif kind in {"handoff_artifacts", "handoff_checks", "handoff_dependencies", "handoff_open_decisions"}:
            rows = c.execute(f"SELECT r.* FROM {kind} r JOIN handoffs h ON r.handoff_id=h.id JOIN tasks t ON h.task_id=t.id WHERE t.project_id=?", (project,))
        else:
            raise ManagementError("unsupported query")
        return [dict(row) for row in rows]

    def backup(self, token, destination: Path):
        """Consistent SQLite snapshot, exclusive output; includes private identity hashes."""
        with self._connect() as source:
            self._operator(self._actor(source, token))
            fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(fd)
            try:
                with sqlite3.connect(destination) as target:
                    source.backup(target)
            except BaseException:
                destination.unlink(missing_ok=True)
                raise


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", type=Path, required=True)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--credential", type=Path)
    sub = p.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--owner", required=True)
    init.add_argument("--credential-out", type=Path, required=True)
    fields = {
        "identity-add": ["user", "credential-out"],
        "project-create": ["project", "title"],
        "member-add": ["project", "user", "role"],
        "task-create": ["project", "id", "title"],
        "task-offer": ["task", "revision", "to", "scope"],
        "task-accept": ["task", "revision"],
        "task-block": ["task", "revision", "owner", "condition"],
        "artifact-add": ["task", "revision", "id", "path"],
        "handoff-submit": ["task", "revision", "id", "scope", "limitations"],
        "handoff-verify": ["handoff", "revision"],
        "handoff-return": ["handoff", "revision"],
        "handoff-integrate": ["handoff", "revision"],
        "decision-record": ["project", "id", "title"],
        "approval-record": ["id", "artifact", "purpose", "outcome"],
    }
    for command, names in fields.items():
        cmd = sub.add_parser(command)
        cmd.add_argument("--request-id", required=True)
        cmd.add_argument("--reason", required=True)
        for name in names:
            cmd.add_argument("--" + name, required=True,
                             type=int if name == "revision" else str)
        if command == "task-create":
            cmd.add_argument("--depends-on", action="append", default=[])
        if command == "task-offer":
            cmd.add_argument("--allowed-path", action="append", default=[])
            cmd.add_argument("--input", action="append", default=[])
        if command == "handoff-submit":
            for field in ("artifact", "dependency", "open-decision"):
                cmd.add_argument("--" + field, action="append", default=[])
            cmd.add_argument("--check", nargs=3, metavar=("NAME", "RESULT", "EVIDENCE"), action="append", required=True)
        if command == "handoff-integrate":
            choice = cmd.add_mutually_exclusive_group(required=True)
            choice.add_argument("--successor")
            choice.add_argument("--blocker-owner")
            choice.add_argument("--closed", action="store_true")
            cmd.add_argument("--condition")
        if command in {"artifact-add", "decision-record", "approval-record"}:
            cmd.add_argument("--supersedes")
    query = sub.add_parser("query")
    query.add_argument("--project", required=True)
    query.add_argument("--kind", required=True)
    backup = sub.add_parser("backup")
    backup.add_argument("--output", type=Path, required=True)
    return p


def main(argv=None):
    p = parser()
    args = vars(p.parse_args(argv))
    database, root = args.pop("db"), args.pop("root")
    credential_path, command = args.pop("credential"), args.pop("command")
    try:
        if command == "init":
            Store.initialize(database, root, args["owner"], args["credential_out"])
            result = {"initialized": True, "schemaVersion": 1}
        else:
            if credential_path is None:
                raise ManagementError("--credential is required")
            token = credential(credential_path)
            store = Store(database, root)
            if command == "query":
                result = store.query(token, **args)
            elif command == "backup":
                store.backup(token, args["output"])
                result = {"backup": "created"}
            else:
                request_id, reason = args.pop("request_id"), args.pop("reason")
                if command == "identity-add":
                    result = store.add_identity(token, args["user"], Path(args["credential_out"]), request_id=request_id, reason=reason)
                else:
                    result = store.execute(token, command, args, request_id=request_id, reason=reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ManagementError, sqlite3.Error, OSError, TypeError, KeyError) as exc:
        # Do not echo SQL payloads or credentials, even on constraint failures.
        message = str(exc) if isinstance(exc, ManagementError) else "operation failed; check inputs, database and filesystem"
        print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
