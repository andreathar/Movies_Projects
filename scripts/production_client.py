"""Agent client for the loopback production API; JSON is transport, never state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from production_db import ManagementError, credential, encoded
from production_web import MAX_BODY, validate_command


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, url: str, credential_path: Path):
        parsed = urlsplit(url)
        if (parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or not parsed.port
                or parsed.username or parsed.password or parsed.path not in {"", "/"}
                or parsed.query or parsed.fragment):
            raise ManagementError("explicit http://127.0.0.1:PORT URL required")
        self.url = f"http://127.0.0.1:{parsed.port}"
        self.credential_path = credential_path
        # Neither environment proxies nor redirects may receive the bearer credential.
        self.opener = build_opener(ProxyHandler({}), NoRedirect())

    def request(self, path, payload=None):
        headers = {"Authorization": "Bearer " + credential(self.credential_path)}
        data = encoded(payload).encode() if payload is not None else None
        if data is not None:
            if len(data) > MAX_BODY:
                raise ManagementError("request too large")
            headers["Content-Type"] = "application/json"
        request = Request(self.url + path, data=data, headers=headers)
        try:
            with self.opener.open(request, timeout=10) as response:
                return json.load(response)
        except (HTTPError, URLError, OSError, ValueError):
            # Do not dump payload, headers, server body or credentials into agent logs.
            raise ManagementError("API request failed; reload state before retrying with the same request id") from None

    def projects(self):
        return self.request("/api/projects")["projects"]

    def snapshot(self, project):
        return self.request("/api/snapshot?" + urlencode({"project": project}))["snapshot"]

    def query(self, project, kind):
        return self.request("/api/query?" + urlencode({"project": project, "kind": kind}))["rows"]

    def execute(self, command, args, *, request_id, reason):
        return self.request("/api/commands", {"command": command, "args": validate_command(command, args),
                                              "request_id": request_id, "reason": reason})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--credential", type=Path, required=True)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("projects")
    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--project", required=True)
    query = sub.add_parser("query")
    query.add_argument("--project", required=True)
    query.add_argument("--kind", required=True)
    execute = sub.add_parser("execute", help="read command arguments as a JSON object on stdin")
    execute.add_argument("command")
    execute.add_argument("--request-id", required=True)
    execute.add_argument("--reason", required=True)
    args = parser.parse_args(argv)
    try:
        client = Client(args.url, args.credential)
        if args.action == "projects":
            result = client.projects()
        elif args.action == "snapshot":
            result = client.snapshot(args.project)
        elif args.action == "query":
            result = client.query(args.project, args.kind)
        else:
            raw = sys.stdin.buffer.read(MAX_BODY + 1)
            if len(raw) > MAX_BODY:
                raise ManagementError("request too large")
            result = client.execute(args.command, json.loads(raw), request_id=args.request_id, reason=args.reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ManagementError, OSError, ValueError, TypeError, KeyError):
        print('{"error":"API operation failed; check identity, state and local service"}', file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
