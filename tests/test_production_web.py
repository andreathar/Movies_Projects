"""Greenfield UI/API integration tests. No socket, real credential or legacy state."""
import io
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import unittest
from urllib.parse import urlencode, parse_qs, urlsplit
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from production_db import Store, credential, ManagementError
from production_web import Application, KINDS, MAX_BODY, SESSION_SECONDS, handler_for, validate_command
from production_client import Client, NoRedirect


class ProductionWebTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.db = self.root / "new.sqlite3"
        self.store = Store.initialize(self.db, self.root, "operator", self.root / "operator.key")
        self.owner = credential(self.root / "operator.key")
        self.now = 1000
        self.app = Application(self.store, "127.0.0.1:19876", clock=lambda: self.now)
        self.count = 0

    def execute(self, command, **args):
        self.count += 1
        return self.store.execute(self.owner, command, args, request_id=f"test-{self.count}", reason="Synthetic fixture")

    def call(self, method="GET", path="/", *, data=None, token=None, cookie=None, origin=None, content=None, raw=None, host="127.0.0.1:19876"):
        headers = {"Host": host}
        # 'cookie' is an obsolete-session/cookie probe on the API. For browser helpers,
        # it names the opaque session handle now sent only in POST form bodies.
        if cookie and not path.startswith("/api/"):
            if method == "GET" and path.startswith("/"):
                project = parse_qs(urlsplit(path).query).get("project", [""])[0]
                method, path, origin = "POST", "/view", "http://127.0.0.1:19876"
                data = {"project": project, "csrf": self.app.sessions.get(cookie, {}).get("csrf", "")}
            data = {**(data or {}), "session": cookie}
        if token:
            headers["Authorization"] = "Bearer " + token
        if cookie:
            headers["Cookie"] = cookie
        if origin:
            headers["Origin"] = origin
        body = b""
        if data is not None:
            if path.startswith("/api/"):
                body = json.dumps(data).encode()
                headers["Content-Type"] = "application/json"
            else:
                body = urlencode(data).encode()
                headers["Content-Type"] = "application/x-www-form-urlencoded"
        if content:
            headers["Content-Type"] = content
        if raw is not None:
            body = raw
        return self.app.handle(method, path, headers, body)

    def login(self, token=None):
        token = token or self.owner
        response = self.call("POST", "/login", data={"credential": token}, origin="http://127.0.0.1:19876")
        self.assertEqual(response.status, 200)
        self.assertNotIn("Set-Cookie", response.headers)
        sid = next(reversed(self.app.sessions))
        return sid, self.app.sessions[sid]["csrf"]

    def api(self, command, args, *, request_id="api-1", token=None):
        return self.call("POST", "/api/commands", token=token or self.owner, data={
            "command": command, "args": args, "request_id": request_id, "reason": "Synthetic API check"})

    def test_predefined_dropdowns_and_project_scoped_options(self):
        self.execute("project-create", project="one", title="Projeto <um>")
        self.execute("project-create", project="two", title="Projeto dois")
        self.execute("task-create", project="one", id="T-one", title="Tarefa <um>")
        self.execute("task-create", project="two", id="T-other", title="Outra tarefa")
        cookie, _ = self.login()
        page = self.call(path="/?project=one", cookie=cookie).body.decode()
        def options(field):
            return re.search(r'<select[^>]*id="' + field + r'"[^>]*>(.*?)</select>', page).group(1)
        self.assertIn('value="producer"', options("member-add-role"))
        self.assertIn('value="contributor"', options("member-add-role"))
        self.assertIn('value="reviewer"', options("member-add-role"))
        self.assertIn('value="approved"', options("approval-record-outcome"))
        self.assertIn('value="rejected"', options("approval-record-outcome"))
        self.assertIn('value="one" selected', options("task-create-project"))
        self.assertIn('value="T-one"', options("task-offer-task"))
        self.assertNotIn('T-other', options("task-offer-task"))
        self.assertIn('Tarefa &lt;um&gt;', options("task-offer-task"))
        self.assertIn('id="project-create-project" name="project" required type="text"', page)
        self.assertIn("Equipe e permissões", page)
        self.assertNotIn("Motivo e evidência real", page)
        self.assertNotIn(self.owner, page)

    def test_participant_choices_do_not_leak_other_projects_or_secrets(self):
        self.store.add_identity(self.owner, "reader", self.root / "reader.key", request_id="reader-id", reason="Synthetic fixture")
        self.store.add_identity(self.owner, "unrelated", self.root / "unrelated.key", request_id="other-id", reason="Synthetic fixture")
        self.execute("project-create", project="one", title="One")
        self.execute("project-create", project="two", title="Two")
        self.execute("member-add", project="one", user="operator", role="producer")
        self.execute("member-add", project="one", user="reader", role="reviewer")
        self.execute("member-add", project="two", user="unrelated", role="contributor")
        reader = credential(self.root / "reader.key")
        self.assertEqual(self.store.participants(reader), [{"id": "reader"}])
        members = self.store.participants(reader, "one")
        self.assertEqual({row["id"] for row in members}, {"operator", "reader"})
        self.assertTrue(all(set(row) == {"id", "role"} for row in members))
        with self.assertRaises(ManagementError):
            self.store.participants(reader, "two")
        cookie, _ = self.login(reader)
        page = self.call(path="/?project=one", cookie=cookie).body.decode()
        self.assertNotIn("unrelated", page)
        self.assertNotIn(reader, page)
        self.assertEqual(self.api("member-add", {"project": "one", "user": "unrelated", "role": "admin"}).status, 400)
        self.assertEqual({row["id"] for row in self.store.participants(self.owner, "one")}, {"operator", "reader"})

    def test_command_return_preserves_selected_project(self):
        self.execute("project-create", project="one", title="One")
        self.execute("task-create", project="one", id="T1", title="Task")
        self.execute("member-add", project="one", user="operator", role="producer")
        cookie, csrf = self.login()
        response = self.call("POST", "/command", cookie=cookie, origin="http://127.0.0.1:19876", data={
            "command": "task-block", "task": "T1", "revision": "1", "owner": "operator",
            "condition": "Synthetic missing input", "reason": "Synthetic fixture", "request_id": "block-ui",
            "csrf": csrf, "view_project": "one"})
        self.assertEqual(response.status, 200)
        self.assertIn(b'name="project" value="one"', response.body)

    def test_empty_dashboard_does_not_seed_and_requires_login(self):
        page = self.call()
        self.assertEqual(page.status, 200)
        self.assertIn(b'type="password"', page.body)
        # no-referrer makes native browser form POSTs send Origin:null and blocks login.
        self.assertEqual(page.headers["Referrer-Policy"], "same-origin")
        self.assertEqual(self.store.projects(self.owner), [])
        cookie, _ = self.login()
        page = self.call(cookie=cookie)
        self.assertIn("Banco sem projetos".encode(), page.body)
        self.assertNotIn(self.owner.encode(), page.body)
        self.assertEqual(self.store.projects(self.owner), [])
        self.assertFalse((self.root / "workspace.json").exists())

    def test_host_origin_csrf_and_cookie_protections(self):
        self.assertEqual(self.call(host="attacker.invalid").status, 403)
        self.assertEqual(self.call("POST", "/login", data={"credential": self.owner}).status, 403)
        self.assertEqual(self.call("POST", "/login", data={"credential": self.owner}, origin="https://evil.example").status, 403)
        cookie, csrf = self.login()
        self.assertEqual(self.call("POST", "/logout", cookie=cookie, data={"csrf": csrf}).status, 403)
        self.assertEqual(self.call("POST", "/logout", cookie=cookie, origin="http://127.0.0.1:19876", data={"csrf": "bad"}).status, 403)
        self.assertEqual(self.call("POST", "/logout", cookie=cookie, origin="http://127.0.0.1:19876", data={"csrf": csrf}).status, 303)
        self.assertEqual(self.call(cookie=cookie).status, 401)

    def test_expiry_and_login_rate_limit(self):
        cookie, _ = self.login()
        self.now += SESSION_SECONDS + 1
        self.assertEqual(self.call(cookie=cookie).status, 401)
        for _ in range(10):
            self.call("POST", "/login", origin="http://127.0.0.1:19876", data={"credential": "invalid"})
        response = self.call("POST", "/login", origin="http://127.0.0.1:19876", data={"credential": self.owner})
        self.assertEqual(response.status, 429)
        self.now += 61
        self.login()

    def test_api_bearer_not_cookie_and_no_browser_cross_origin(self):
        cookie, _ = self.login()
        self.assertEqual(self.call(path="/api/projects", cookie=cookie).status, 401)
        self.assertEqual(self.call(path="/api/projects", token=self.owner, origin="https://evil.example").status, 401)
        self.assertEqual(self.call(path="/api/projects?credential=" + self.owner).status, 401)
        self.assertEqual(self.call(path="/api/projects", token="invalid").status, 400)
        response = self.call(path="/api/projects", token=self.owner)
        self.assertEqual(json.loads(response.body), {"projects": []})
        self.assertNotIn("Access-Control-Allow-Origin", response.headers)

    def test_api_commands_share_audit_idempotency_and_revisions(self):
        data = {"project": "fresh", "title": "Empty start"}
        first = self.api("project-create", data)
        self.assertEqual(first.status, 200)
        self.assertEqual(self.api("project-create", data).body, first.body)
        self.assertEqual(self.api("project-create", {**data, "title": "Changed"}).status, 400)
        self.assertEqual(self.api("task-create", {"project": "fresh", "id": "T1", "title": "Draft"}, request_id="task").status, 200)
        self.assertEqual(len(self.store.query(self.owner, "fresh", "events")), 2)
        self.assertEqual(self.api("task-offer", {"task": "T1", "revision": 8, "to": "operator", "scope": "Test"}, request_id="stale").status, 400)
        self.assertEqual(self.store.query(self.owner, "fresh", "tasks")[0]["state"], "ready")

    def test_api_blocks_provisioning_arbitrary_paths_and_bad_payloads(self):
        for command in ("init", "identity-add", "backup", "query", "execute-sql"):
            self.assertEqual(self.api(command, {}).status, 400)
        self.assertEqual(self.api("project-create", {"project": "x", "title": "Test", "actor": "operator"}).status, 400)
        self.assertEqual(self.api("task-accept", {"task": "x", "revision": True}).status, 400)
        self.assertEqual(self.call("POST", "/api/commands", token=self.owner, raw=b"{}", content="text/plain").status, 415)
        self.assertEqual(self.call("POST", "/api/commands", token=self.owner, raw=b"{", content="application/json").status, 400)
        self.assertEqual(self.call("POST", "/api/commands", token=self.owner, raw=b"x" * (MAX_BODY + 1)).status, 413)
        self.assertEqual(self.store.projects(self.owner), [])

    def test_project_isolation_and_atomic_snapshot(self):
        self.execute("project-create", project="one", title="One")
        self.execute("project-create", project="two", title="Two")
        self.store.add_identity(self.owner, "reader", self.root / "reader.key", request_id="reader", reason="Test user")
        token = credential(self.root / "reader.key")
        self.execute("member-add", project="one", user="reader", role="reviewer")
        projects = json.loads(self.call(path="/api/projects", token=token).body)["projects"]
        self.assertEqual([p["id"] for p in projects], ["one"])
        self.assertEqual(self.call(path="/api/snapshot?project=two", token=token).status, 400)
        with patch.object(self.store, "_connect", wraps=self.store._connect) as connection:
            response = self.call(path="/api/snapshot?project=one", token=token)
            self.assertEqual(response.status, 200)
            # One for authentication, one transaction for all projection reads.
            self.assertEqual(connection.call_count, 2)
        self.assertEqual(set(json.loads(response.body)["snapshot"]), set(KINDS))
        self.assertEqual(self.api("task-create", {"project": "one", "id": "T1", "title": "Forbidden"}, token=token).status, 400)

    def test_snapshot_remains_consistent_across_concurrent_wal_commit(self):
        self.execute("project-create", project="fresh", title="Fresh")
        self.execute("task-create", project="fresh", id="T1", title="Before snapshot")
        with sqlite3.connect(self.db) as c:
            c.execute("PRAGMA journal_mode=WAL")
        original = self.store._query
        def read_then_write(c, project, kind):
            rows = original(c, project, kind)
            if kind == "tasks":
                self.execute("task-create", project="fresh", id="T2", title="Concurrent commit")
            return rows
        with patch.object(self.store, "_query", side_effect=read_then_write):
            snapshot = self.store.snapshot(self.owner, "fresh", ["tasks", "events"])
        self.assertEqual([t["id"] for t in snapshot["tasks"]], ["T1"])
        self.assertEqual(len(snapshot["events"]), 2)
        self.assertEqual(len(self.store.query(self.owner, "fresh", "tasks")), 2)
        self.assertEqual(len(self.store.query(self.owner, "fresh", "events")), 3)

    def test_browser_sessions_never_set_cookies_or_authenticate_gets(self):
        session, _ = self.login()
        page = self.app.handle("GET", "/", {"Host": "127.0.0.1:19876", "Cookie": "pdb=" + session})
        self.assertIn(b'type="password"', page.body)
        self.assertNotIn(session.encode(), page.body)
        self.assertNotIn("Set-Cookie", page.headers)

    def test_browser_form_writes_same_database_and_escapes_content(self):
        cookie, csrf = self.login()
        form = {"csrf": csrf, "request_id": "browser-1", "reason": "Explicit fresh start",
                "command": "project-create", "project": "fresh", "title": '<script>alert("x")</script>'}
        response = self.call("POST", "/command", cookie=cookie, origin="http://127.0.0.1:19876", data=form)
        self.assertEqual(response.status, 200)
        self.assertNotIn(b"<script>", response.body)
        page = self.call(path="/?project=fresh", cookie=cookie)
        self.assertIn(b"&lt;script&gt;", page.body)
        self.assertIn(b'lang="pt-BR"', page.body)
        self.assertIn(b'Content-Security-Policy', str(page.headers).encode())
        self.assertNotIn(self.owner.encode(), page.body)
        for request_id in re.findall(rb'name="request_id" value="([^"]+)"', page.body):
            self.assertRegex(request_id.decode(), r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
        self.assertEqual(self.call("POST", "/command", cookie=cookie, origin="http://127.0.0.1:19876", data=form).status, 200)
        self.assertEqual(len(self.store.query(self.owner, "fresh", "events")), 1)

    def test_approval_scalar_and_handoff_arrays_have_distinct_validation(self):
        approval = {"id": "P1", "artifact": "A1", "purpose": "test", "outcome": "rejected"}
        self.assertEqual(validate_command("approval-record", approval), approval)
        with self.assertRaises(ManagementError):
            validate_command("handoff-submit", {"task": "T1", "revision": 1, "id": "H1", "scope": "test",
                                               "limitations": "test", "artifact": "not-an-array"})

    def test_full_flow_through_api_and_form_checks(self):
        self.execute("project-create", project="fresh", title="Fresh")
        self.execute("member-add", project="fresh", user="operator", role="producer")
        self.execute("task-create", project="fresh", id="T1", title="Proposal")
        self.assertEqual(self.api("task-offer", {"task": "T1", "revision": 1, "to": "operator", "scope": "Only proposal",
                                "allowed_path": ["proposal.md"]}, request_id="offer").status, 200)
        self.assertEqual(self.api("task-accept", {"task": "T1", "revision": 2}, request_id="accept").status, 200)
        (self.root / "proposal.md").write_text("Synthetic proposal")
        self.assertEqual(self.api("artifact-add", {"task": "T1", "revision": 3, "id": "A1", "path": "proposal.md"}, request_id="artifact").status, 200)
        cookie, csrf = self.login()
        response = self.call("POST", "/command", cookie=cookie, origin="http://127.0.0.1:19876", data={
            "command": "handoff-submit", "csrf": csrf, "request_id": "handoff", "reason": "Synthetic handoff",
            "task": "T1", "revision": "3", "id": "H1", "scope": "Proposal", "limitations": "Not artistic approval",
            "artifact": "A1", "check": "readback | passed | Compared synthetic bytes"})
        self.assertEqual(response.status, 200)
        self.assertEqual(self.api("handoff-verify", {"handoff": "H1", "revision": 1}, request_id="verify").status, 200)
        self.assertEqual(self.api("handoff-integrate", {"handoff": "H1", "revision": 2, "closed": True}, request_id="integrate").status, 200)
        self.assertEqual(self.store.query(self.owner, "fresh", "tasks")[0]["state"], "completed")
        self.assertEqual(self.store.query(self.owner, "fresh", "approvals"), [])
        self.assertEqual(self.api("approval-record", {"id": "P1", "artifact": "A1", "purpose": "synthetic", "outcome": "rejected"}, request_id="approval").status, 200)

    def test_missing_database_fails_closed_and_errors_do_not_echo_secrets(self):
        self.db.unlink()
        response = self.call(path="/api/projects", token=self.owner)
        self.assertEqual(response.status, 400)
        self.assertFalse(self.db.exists())
        self.assertNotIn(self.owner.encode(), response.body)
        self.assertNotIn(str(self.root).encode(), response.body)

    def test_agent_client_uses_header_not_url_and_never_retries(self):
        client = Client("http://127.0.0.1:19876", self.root / "operator.key")
        calls = []
        def send(request, timeout):
            self.assertEqual(timeout, 10)
            self.assertNotIn(self.owner, request.full_url)
            calls.append(request)
            parsed = request.full_url.removeprefix("http://127.0.0.1:19876")
            headers = dict(request.header_items())
            headers["Host"] = "127.0.0.1:19876"
            response = self.app.handle(request.get_method(), parsed, headers, request.data or b"")
            self.assertEqual(response.status, 200)
            return io.BytesIO(response.body)
        with patch.object(client.opener, "open", side_effect=send):
            self.assertEqual(client.projects(), [])
            client.execute("project-create", {"project": "fresh", "title": "New"}, request_id="client-1", reason="Explicit fixture")
            self.assertEqual(client.snapshot("fresh")["tasks"], [])
        self.assertEqual(len(calls), 3)
        with patch.object(client.opener, "open", side_effect=OSError("must not leak private details")) as attempt:
            with self.assertRaisesRegex(ManagementError, "reload state"):
                client.projects()
            self.assertEqual(attempt.call_count, 1)
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, "", {}, "http://evil.invalid"))

    def test_agent_client_rejects_non_loopback_urls_and_public_credentials(self):
        for url in ("http://localhost:19876", "https://127.0.0.1:19876", "http://127.0.0.1",
                    "http://127.0.0.1:19876/path", "http://user:secret@127.0.0.1:19876", "http://evil.invalid:19876"):
            with self.assertRaises((ManagementError, ValueError)):
                Client(url, self.root / "operator.key")
        (self.root / "operator.key").chmod(0o644)
        with self.assertRaises(ManagementError):
            Client("http://127.0.0.1:19876", self.root / "operator.key").projects()

    def test_http_handler_without_binding_socket(self):
        class FakeSocket:
            def __init__(self, raw):
                self.input = io.BytesIO(raw)
                self.output = io.BytesIO()
            def makefile(self, *args, **kwargs):
                return self.input
            def sendall(self, data):
                self.output.write(data)
            def settimeout(self, seconds):
                self.timeout = seconds
        session, csrf = self.login()
        valid_body = urlencode({"session": session, "csrf": csrf, "command": "project-create",
                                "project": "must-not-exist", "title": "Truncated command",
                                "request_id": "truncated", "reason": "Synthetic framing test"}).encode()
        truncated = (b"POST /command HTTP/1.1\r\nHost: 127.0.0.1:19876\r\n"
                     b"Origin: http://127.0.0.1:19876\r\nContent-Type: application/x-www-form-urlencoded\r\n"
                     + f"Content-Length: {len(valid_body) + 10}\r\n\r\n".encode() + valid_body)
        for request, expected in [
            (truncated, b"400 Bad Request"),
            (b"GET / HTTP/1.1\r\nHost: 127.0.0.1:19876\r\n\r\n", b"200 OK"),
            (b"POST /login HTTP/1.1\r\nHost: 127.0.0.1:19876\r\nContent-Length: 2\r\nContent-Length: 3\r\n\r\n{}", b"400 Bad Request"),
            (b"POST /login HTTP/1.1\r\nHost: 127.0.0.1:19876\r\nTransfer-Encoding: chunked\r\n\r\n", b"400 Bad Request"),
            (b"POST /login HTTP/1.1\r\nHost: 127.0.0.1:19876\r\nContent-Length: 250\r\n\r\ncredential=short", b"400 Bad Request"),
        ]:
            socket = FakeSocket(request)
            with patch.object(self.app, "handle", wraps=self.app.handle) as dispatch:
                handler_for(self.app)(socket, ("127.0.0.1", 1), None)
                if expected == b"400 Bad Request":
                    dispatch.assert_not_called()
            self.assertIn(expected, socket.output.getvalue())
        self.assertEqual(self.store.projects(self.owner), [])


if __name__ == "__main__":
    unittest.main()
