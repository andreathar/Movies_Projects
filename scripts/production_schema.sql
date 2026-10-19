-- Greenfield management schema. Media and original evidence remain outside this database.
CREATE TABLE schema_version (version INTEGER PRIMARY KEY CHECK (version = 1));
INSERT INTO schema_version VALUES (1);
CREATE TABLE workspace_anchor (root TEXT NOT NULL);
CREATE TABLE identities (
    id TEXT PRIMARY KEY,
    token_hash TEXT NOT NULL UNIQUE,
    is_operator INTEGER NOT NULL CHECK (is_operator IN (0, 1))
);
CREATE TABLE projects (id TEXT PRIMARY KEY, title TEXT NOT NULL);
CREATE TABLE memberships (
    project_id TEXT NOT NULL REFERENCES projects(id),
    identity_id TEXT NOT NULL REFERENCES identities(id),
    role TEXT NOT NULL CHECK (role IN ('producer', 'contributor', 'reviewer')),
    PRIMARY KEY (project_id, identity_id)
);
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id),
    title TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('ready','offered','active','delivered','blocked','completed')),
    responsible_id TEXT NOT NULL REFERENCES identities(id),
    offered_to TEXT REFERENCES identities(id),
    assignment_scope TEXT,
    assignment_version INTEGER NOT NULL DEFAULT 0,
    blocker_owner TEXT REFERENCES identities(id),
    unblock_condition TEXT,
    revision INTEGER NOT NULL DEFAULT 1 CHECK (revision > 0),
    CHECK ((state = 'blocked') = (blocker_owner IS NOT NULL AND unblock_condition IS NOT NULL))
);
CREATE TABLE task_dependencies (
    task_id TEXT NOT NULL REFERENCES tasks(id),
    dependency_id TEXT NOT NULL REFERENCES tasks(id),
    PRIMARY KEY (task_id, dependency_id),
    CHECK (task_id <> dependency_id)
);
CREATE TABLE artifact_versions (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(id),
    project_id TEXT NOT NULL REFERENCES projects(id),
    path TEXT NOT NULL,
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64),
    created_by TEXT NOT NULL REFERENCES identities(id),
    assignment_version INTEGER NOT NULL,
    supersedes TEXT REFERENCES artifact_versions(id)
);
CREATE TABLE task_allowed_paths (
    task_id TEXT NOT NULL REFERENCES tasks(id),
    path TEXT NOT NULL,
    PRIMARY KEY (task_id, path)
);
CREATE TABLE task_inputs (
    task_id TEXT NOT NULL REFERENCES tasks(id),
    artifact_id TEXT NOT NULL REFERENCES artifact_versions(id),
    PRIMARY KEY (task_id, artifact_id)
);
CREATE TABLE handoffs (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES tasks(id),
    submitted_by TEXT NOT NULL REFERENCES identities(id),
    scope TEXT NOT NULL,
    limitations TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('submitted','verified','integrated','returned')),
    revision INTEGER NOT NULL DEFAULT 1 CHECK (revision > 0),
    successor_task_id TEXT REFERENCES tasks(id),
    closure TEXT CHECK (closure IN ('successor','blocked','closed')),
    blocker_owner TEXT REFERENCES identities(id),
    unblock_condition TEXT
);
CREATE UNIQUE INDEX handoffs_active_task ON handoffs(task_id) WHERE state <> 'returned';
CREATE TABLE handoff_artifacts (
    handoff_id TEXT NOT NULL REFERENCES handoffs(id),
    artifact_id TEXT NOT NULL REFERENCES artifact_versions(id),
    PRIMARY KEY (handoff_id, artifact_id)
);
CREATE TABLE handoff_checks (
    handoff_id TEXT NOT NULL REFERENCES handoffs(id),
    name TEXT NOT NULL,
    result TEXT NOT NULL CHECK (result IN ('passed','failed','not_run')),
    evidence TEXT NOT NULL,
    PRIMARY KEY (handoff_id, name)
);
CREATE TABLE handoff_dependencies (
    handoff_id TEXT NOT NULL REFERENCES handoffs(id),
    dependency_id TEXT NOT NULL REFERENCES tasks(id),
    PRIMARY KEY (handoff_id, dependency_id)
);
CREATE TABLE decisions (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id),
    title TEXT NOT NULL,
    rationale TEXT NOT NULL,
    decided_by TEXT NOT NULL REFERENCES identities(id),
    supersedes TEXT UNIQUE REFERENCES decisions(id)
);
CREATE TABLE handoff_open_decisions (
    handoff_id TEXT NOT NULL REFERENCES handoffs(id),
    decision_id TEXT NOT NULL REFERENCES decisions(id),
    PRIMARY KEY (handoff_id, decision_id)
);
CREATE TABLE approvals (
    id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL REFERENCES artifact_versions(id),
    purpose TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (outcome IN ('approved','rejected')),
    rationale TEXT NOT NULL,
    approved_by TEXT NOT NULL REFERENCES identities(id),
    supersedes TEXT UNIQUE REFERENCES approvals(id)
);
CREATE UNIQUE INDEX approvals_single_root ON approvals(artifact_id, purpose) WHERE supersedes IS NULL;
-- JSON is used only for immutable audit payloads/results, not live domain entities.
CREATE TABLE events (
    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
    actor_id TEXT NOT NULL REFERENCES identities(id),
    project_id TEXT REFERENCES projects(id),
    command TEXT NOT NULL,
    request_id TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    reason TEXT NOT NULL,
    payload TEXT NOT NULL DEFAULT '{}',
    occurred_at TEXT NOT NULL,
    result TEXT NOT NULL,
    UNIQUE (actor_id, request_id)
);
CREATE TRIGGER events_no_update BEFORE UPDATE ON events
BEGIN SELECT RAISE(ABORT, 'audit events are append-only'); END;
CREATE TRIGGER events_no_delete BEFORE DELETE ON events
BEGIN SELECT RAISE(ABORT, 'audit events are append-only'); END;
CREATE TRIGGER artifacts_no_update BEFORE UPDATE ON artifact_versions
BEGIN SELECT RAISE(ABORT, 'artifact versions are immutable'); END;
CREATE TRIGGER artifacts_no_delete BEFORE DELETE ON artifact_versions
BEGIN SELECT RAISE(ABORT, 'artifact versions are immutable'); END;
CREATE TRIGGER decisions_no_update BEFORE UPDATE ON decisions
BEGIN SELECT RAISE(ABORT, 'decisions are immutable'); END;
CREATE TRIGGER decisions_no_delete BEFORE DELETE ON decisions
BEGIN SELECT RAISE(ABORT, 'decisions are immutable'); END;
CREATE TRIGGER approvals_no_update BEFORE UPDATE ON approvals
BEGIN SELECT RAISE(ABORT, 'approvals are immutable'); END;
CREATE TRIGGER approvals_no_delete BEFORE DELETE ON approvals
BEGIN SELECT RAISE(ABORT, 'approvals are immutable'); END;
CREATE INDEX tasks_project ON tasks(project_id);
CREATE INDEX events_project ON events(project_id, sequence);
