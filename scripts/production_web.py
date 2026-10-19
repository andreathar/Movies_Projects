"""Loopback-only greenfield dashboard and agent API. No legacy imports/provider calls.

Run explicitly; importing this module does not bind a port or create a database.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import sqlite3
import threading
import time
from urllib.parse import parse_qs, urlsplit

from production_db import ManagementError, Store, encoded, required

# Required scalar fields; arrays are newline-separated in the HTML forms, JSON arrays in API.
COMMANDS = {
    "project-create": ("Criar projeto", "project title", ""),
    "member-add": ("Vincular participante", "project user role", ""),
    "task-create": ("Criar tarefa", "project id title", "depends_on"),
    "task-offer": ("Oferecer atribuição", "task revision to scope", "allowed_path input"),
    "task-accept": ("Aceitar atribuição", "task revision", ""),
    "task-block": ("Registrar bloqueio", "task revision owner condition", ""),
    "artifact-add": ("Registrar versão de arquivo", "task revision id path", "supersedes"),
    "handoff-submit": ("Entregar handoff", "task revision id scope limitations", "artifact check dependency open_decision"),
    "handoff-verify": ("Verificar handoff", "handoff revision", ""),
    "handoff-return": ("Devolver para correção", "handoff revision", ""),
    "handoff-integrate": ("Integrar handoff", "handoff revision", "successor blocker_owner condition closed"),
    "decision-record": ("Registrar decisão", "project id title", "supersedes"),
    "approval-record": ("Registrar aprovação/rejeição", "id artifact purpose outcome", "supersedes"),
}
ARRAYS = {"depends_on", "allowed_path", "input", "artifact", "dependency", "open_decision", "check"}
KINDS = ("tasks", "handoffs", "artifact_versions", "decisions", "approvals", "events",
         "task_dependencies", "task_inputs", "task_allowed_paths", "handoff_artifacts",
         "handoff_checks", "handoff_dependencies", "handoff_open_decisions")
LABELS = {"project": "Projeto (ID)", "title": "Título", "user": "Participante (ID)",
          "role": "Papel: producer, contributor ou reviewer", "id": "Novo ID",
          "task": "Tarefa (ID)", "revision": "Revisão esperada", "to": "Destinatário (ID)",
          "scope": "Escopo", "owner": "Responsável (ID)", "condition": "Condição para desbloquear",
          "path": "Caminho relativo do arquivo", "supersedes": "Versão anterior (ID)",
          "handoff": "Handoff (ID)", "limitations": "Limitações / verificações não feitas",
          "artifact": "Artefatos (um ID por linha)", "check": "Verificações: nome | passed/failed/not_run | evidência (uma por linha)",
          "dependency": "Dependências declaradas (uma tarefa por linha)",
          "open_decision": "Decisões em aberto (um ID por linha)",
          "depends_on": "Pré-requisitos (uma tarefa por linha)",
          "allowed_path": "Caminhos permitidos (um caminho por linha)",
          "input": "Versões de entrada (um ID por linha)",
          "successor": "Sucessora já aceita (ID)", "blocker_owner": "Responsável pelo bloqueio (ID)",
          "closed": "Encerrar etapa sem sucessora", "purpose": "Finalidade da aprovação",
          "outcome": "Resultado: approved ou rejected"}
MAX_BODY = 65536
SESSION_SECONDS = 1800


def array_fields(command):
    return ARRAYS - ({"artifact"} if command == "approval-record" else set())


def validate_command(command, args):
    if command not in COMMANDS or not isinstance(args, dict):
        raise ManagementError("unsupported command or invalid arguments")
    _, mandatory, optional = COMMANDS[command]
    allowed = set((mandatory + " " + optional).split())
    if set(args) - allowed:
        raise ManagementError("unknown command fields")
    for key in mandatory.split():
        if key not in args:
            raise ManagementError("missing required field: " + key)
    cleaned = {}
    for key, value in args.items():
        if key == "revision":
            if type(value) is not int or value < 1:
                raise ManagementError("revision must be a positive integer")
        elif key == "closed":
            if type(value) is not bool:
                raise ManagementError("closed must be boolean")
        elif key in array_fields(command):
            if not isinstance(value, list) or len(value) > 200:
                raise ManagementError("invalid list field")
            for item in value:
                if key == "check":
                    if not isinstance(item, list) or len(item) != 3:
                        raise ManagementError("checks need name, result and evidence")
                    for field in item:
                        required(field)
                    if item[1] not in {"passed", "failed", "not_run"}:
                        raise ManagementError("invalid check result")
                else:
                    required(item)
        else:
            required(value)
        cleaned[key] = value
    if command == "handoff-integrate":
        if sum(bool(cleaned.get(k)) for k in ("successor", "blocker_owner", "closed")) != 1:
            raise ManagementError("choose accepted successor, owned blocker, or closed stage")
    return cleaned


@dataclass
class Response:
    status: int
    body: bytes
    headers: dict


class Application:
    def __init__(self, store: Store, authority: str, *, clock=time.monotonic):
        self.store = store
        self.authority = authority
        self.clock = clock
        self.sessions = {}
        self.lock = threading.Lock()
        self.login_attempts = []

    def projects(self, token):
        return self.store.projects(token)

    def _session(self, sid):
        # Session handles travel in POST bodies, never cookies, URLs or browser storage.
        # Cookies are host-scoped and would leak to neighboring loopback services/ports.
        with self.lock:
            now = self.clock()
            self.sessions = {k: v for k, v in self.sessions.items() if v["expires"] > now}
            return sid, self.sessions.get(sid)

    def response(self, status, body, *, html=False, extra=None):
        headers = {"Content-Type": "text/html; charset=utf-8" if html else "application/json; charset=utf-8",
                   "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff",
                   "Referrer-Policy": "no-referrer",
                   "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'"}
        headers.update(extra or {})
        return Response(status, (body if html else encoded(body)).encode(), headers)

    def handle(self, method, target, headers, body=b""):
        headers = {k.lower(): v for k, v in headers.items()}
        route = urlsplit(target)
        api = route.path.startswith("/api/")
        try:
            if headers.get("host") != self.authority:
                return self.response(403, {"error": "untrusted host"})
            if len(body) > MAX_BODY:
                return self.response(413, {"error": "request too large"})
            if method not in {"GET", "POST"}:
                return self.response(405, {"error": "method not allowed"})
            bearer = headers.get("authorization", "")
            token = bearer[7:] if bearer.startswith("Bearer ") else None
            # API is bearer-only. Browser mutations require both Origin and per-session CSRF.
            if api:
                if headers.get("origin") is not None or not token:
                    return self.response(401, {"error": "non-browser bearer authentication required"})
                self.projects(token)  # Authenticate even malformed requests.
                if route.path == "/api/projects" and method == "GET":
                    return self.response(200, {"projects": self.projects(token)})
                if route.path == "/api/snapshot" and method == "GET":
                    project = parse_qs(route.query).get("project", [""])[0]
                    return self.response(200, {"snapshot": self.store.snapshot(token, project, KINDS)})
                if route.path == "/api/query" and method == "GET":
                    query = parse_qs(route.query)
                    project, kind = query.get("project", [""])[0], query.get("kind", [""])[0]
                    return self.response(200, {"rows": self.store.query(token, project, kind)})
                if route.path == "/api/commands" and method == "POST":
                    if headers.get("content-type") != "application/json":
                        return self.response(415, {"error": "application/json required"})
                    data = json.loads(body)
                    if not isinstance(data, dict) or set(data) != {"command", "args", "request_id", "reason"}:
                        raise ManagementError("invalid command envelope")
                    args = validate_command(data["command"], data["args"])
                    result = self.store.execute(token, data["command"], args,
                                                request_id=data["request_id"], reason=data["reason"])
                    return self.response(200, result)
                return self.response(404, {"error": "route not found"})
            if method == "POST":
                if headers.get("origin") != "http://" + self.authority:
                    return self.response(403, {"error": "same-origin POST required"})
                if headers.get("content-type", "").split(";", 1)[0] != "application/x-www-form-urlencoded":
                    return self.response(415, {"error": "form content type required"})
                data = {k: v[0] for k, v in parse_qs(body.decode(), keep_blank_values=True).items()}
                sid, session = self._session(data.get("session", ""))
                if route.path == "/login":
                    with self.lock:
                        now = self.clock()
                        self.login_attempts = [t for t in self.login_attempts if t > now - 60]
                        if len(self.login_attempts) >= 10:
                            return self.response(429, {"error": "wait before another login attempt"})
                        self.login_attempts.append(now)
                    token = required(data.get("credential", ""))
                    self.projects(token)
                    new_sid = secrets.token_urlsafe(32)
                    with self.lock:
                        self.sessions.pop(sid, None)
                        if len(self.sessions) >= 100:
                            raise ManagementError("session limit reached")
                        self.sessions[new_sid] = {"token": token, "csrf": secrets.token_urlsafe(32),
                                                  "id": new_sid, "expires": self.clock() + SESSION_SECONDS}
                        session = self.sessions[new_sid]
                    return self.response(200, self.dashboard(session, ""), html=True)
                if not session:
                    return self.response(401, {"error": "login required"})
                if not secrets.compare_digest(data.get("csrf", ""), session["csrf"]):
                    return self.response(403, {"error": "invalid CSRF token"})
                if route.path == "/logout":
                    with self.lock:
                        self.sessions.pop(sid, None)
                    return self.response(303, {}, extra={"Location": "/"})
                if route.path == "/view":
                    return self.response(200, self.dashboard(session, data.get("project", "")), html=True)
                if route.path == "/command":
                    command = data.get("command", "")
                    args = {k: v for k, v in data.items() if k not in {"command", "csrf", "session", "request_id", "reason"} and v != ""}
                    for key in list(args):
                        if key == "revision":
                            try:
                                args[key] = int(args[key])
                            except ValueError:
                                raise ManagementError("revision must be a positive integer") from None
                        elif key == "closed":
                            args[key] = args[key] == "true"
                        elif key in array_fields(command):
                            args[key] = [v.strip() for v in args[key].splitlines() if v.strip()]
                            if key == "check":
                                args[key] = [[f.strip() for f in row.split("|", 2)] for row in args[key]]
                    args = validate_command(command, args)
                    result = self.store.execute(session["token"], command, args,
                                                request_id=data.get("request_id", ""), reason=data.get("reason", ""))
                    return self.response(200, self.page("Operação registrada", "<p>Confirmada no banco. Reenviar a mesma requisição não duplica a operação.</p>"
                        + "<pre>" + escape(json.dumps(result, ensure_ascii=False, indent=2)) + '</pre>' + self.navigation(session)), html=True)
                return self.response(404, {"error": "route not found"})
            if route.path != "/":
                return self.response(404, {"error": "route not found"})
            return self.response(200, self.page("Entrar na gestão local", '<p>Use sua própria credencial local. Não compartilhe credenciais de operador com agentes.</p>'
                    '<form action="/login" method="post"><label for="credential">Credencial</label>'
                    '<input id="credential" name="credential" type="password" autocomplete="current-password" required>'
                    '<button type="submit">Entrar</button></form>'), html=True)
        except (ManagementError, sqlite3.Error, OSError, ValueError, TypeError, KeyError):
            # Never echo user payloads, secrets, SQL errors, filesystem paths or request headers.
            message = "Operação recusada. Confira permissão, campos, revisão e integridade dos arquivos; recarregue antes de corrigir."
            if api:
                return self.response(400, {"error": message})
            return self.response(400, self.page("Operação recusada", '<p role="alert">' + message + '</p><a href="/">Recarregar painel</a>'), html=True)

    @staticmethod
    def page(title, content):
        return ('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>' + escape(title) + '</title><style>body{font:1rem/1.6 system-ui;max-width:80rem;margin:auto;padding:1.5rem;background:#111827;color:#f9fafb}'
                'a{color:#93c5fd}input,textarea,select,button{font:inherit;padding:.6rem;min-height:3rem;box-sizing:border-box;max-width:100%}'
                'label,input,textarea{display:block}input,textarea{width:100%;margin-bottom:1.2rem}textarea{min-height:6rem;resize:vertical}'
                'form{max-width:42rem}details,section{border:1px solid #9ca3af;padding:1rem;margin-block:1rem}summary{cursor:pointer;padding:.5rem}'
                'table{border-collapse:collapse;width:100%}td,th{border:1px solid #9ca3af;padding:.5rem;text-align:left;vertical-align:top;white-space:pre-wrap;overflow-wrap:anywhere}'
                '.table{overflow:auto}pre{white-space:pre-wrap;overflow-wrap:anywhere}:focus-visible{outline:3px solid #fbbf24;outline-offset:3px}</style>'
                '<body><header><h1>' + escape(title) + '</h1><p>Banco novo • sem importação • sem geração ou gasto automático</p></header><main>' + content + '</main></body></html>')

    @staticmethod
    def navigation(session, project="", action="/view", label="Voltar ao painel"):
        return ('<form method="post" action="' + action + '">'
                '<input type="hidden" name="session" value="' + escape(session["id"], quote=True) + '">'
                '<input type="hidden" name="csrf" value="' + escape(session["csrf"], quote=True) + '">'
                '<input type="hidden" name="project" value="' + escape(project, quote=True) + '">'
                '<button type="submit">' + escape(label) + '</button></form>')

    def dashboard(self, session, project):
        projects = self.projects(session["token"])
        if project and project not in {p["id"] for p in projects}:
            raise ManagementError("project permission denied")
        content = self.navigation(session, action="/logout", label="Sair")
        content += '<nav aria-label="Projetos"><h2>Projetos</h2>'
        for p in projects:
            content += self.navigation(session, p["id"], label=p["title"] + ' (' + p["id"] + ')')
        content += '</nav>'
        if not projects:
            content += '<p>Banco sem projetos. Cadastre o primeiro abaixo; nada será herdado.</p>'
        if project:
            snapshot = self.store.snapshot(session["token"], project, KINDS)
            for kind in KINDS:
                rows = snapshot[kind]
                content += '<section><h2>' + escape(kind) + '</h2>'
                if not rows:
                    content += '<p>Sem registros.</p>'
                else:
                    columns = list(rows[0])
                    content += '<div class="table" tabindex="0" role="region" aria-label="' + kind + '"><table><caption>' + kind + '</caption><thead><tr>'
                    content += ''.join('<th scope="col">' + escape(k) + '</th>' for k in columns) + '</tr></thead><tbody>'
                    for row in rows:
                        content += '<tr>' + ''.join('<td>' + escape(str(row[k]) if row[k] is not None else '—') + '</td>' for k in columns) + '</tr>'
                    content += '</tbody></table></div>'
                content += '</section>'
        content += '<h2>Operações</h2><p>Use IDs e revisões exibidos no banco. Os formulários não concedem papéis; o núcleo valida cada operação. Cadastro de identidades e backup permanecem na CLI local.</p>'
        for command, (title, mandatory, optional) in COMMANDS.items():
            content += '<details><summary>' + escape(title) + '</summary><form action="/command" method="post">'
            for key, value in (("command", command), ("session", session["id"]), ("csrf", session["csrf"]), ("request_id", "req-" + secrets.token_urlsafe(18))):
                content += '<input type="hidden" name="' + key + '" value="' + escape(value, quote=True) + '">'
            for key in (mandatory + ' ' + optional).split():
                field_id = command + '-' + key
                content += '<label for="' + field_id + '">' + escape(LABELS[key]) + (' (obrigatório)' if key in mandatory.split() else ' (opcional)') + '</label>'
                attrs = ' id="' + field_id + '" name="' + key + '"' + (' required' if key in mandatory.split() else '')
                if key == 'closed':
                    content += '<select' + attrs + '><option value="">Não</option><option value="true">Sim</option></select>'
                elif key in array_fields(command) or key in {'scope', 'limitations'}:
                    content += '<textarea' + attrs + '></textarea>'
                else:
                    value = project if key == 'project' else ''
                    content += '<input' + attrs + (' type="number" min="1" step="1"' if key == 'revision' else ' type="text"') + ' value="' + escape(value, quote=True) + '">'
            content += '<label for="' + command + '-reason">Motivo e evidência real (obrigatório)</label><textarea id="' + command + '-reason" name="reason" required></textarea>'
            content += '<button type="submit">' + escape(title) + '</button></form></details>'
        return self.page("Gestão de produção", content)


def handler_for(application):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Access logs could contain credentials or evidence identifiers.

        def do_GET(self):
            self.dispatch()

        def do_POST(self):
            self.dispatch()

        def dispatch(self):
            # Reject ambiguous framing; do not support chunked bodies on this local adapter.
            self.connection.settimeout(5)
            lengths = self.headers.get_all("Content-Length", [])
            try:
                if self.headers.get("Transfer-Encoding") or len(lengths) > 1:
                    raise ValueError
                length = int(lengths[0]) if lengths else 0
                if length < 0 or length > MAX_BODY:
                    raise ValueError
                body = self.rfile.read(length)
                if len(body) != length:
                    raise ValueError
                response = application.handle(self.command, self.path, dict(self.headers), body)
            except (ValueError, OSError):
                response = application.response(400, {"error": "invalid request framing"})
            self.send_response(response.status)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.send_header("Content-Length", str(len(response.body)))
            self.end_headers()
            self.wfile.write(response.body)
    return Handler


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error("port must be 1024..65535; check the port registry before starting")
    store = Store(args.db, args.root)
    with store._connect():
        pass  # Refuse missing/unrecognized database before opening the socket.
    authority = "127.0.0.1:" + str(args.port)
    app = Application(store, authority)
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(app)) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
