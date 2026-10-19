"""Explicit browser QA with a temporary synthetic database. Check/register port first.

Not auto-discovered by unittest; never uses the operational database or its credentials.
"""
import argparse
import hashlib
import json
import os
import secrets
import signal
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from urllib.request import ProxyHandler, build_opener

from production_db import Store, credential


def descendant_groups(pid):
    """Snapshot only this runner's child tree, including detached Chromium groups (Linux)."""
    pending, groups = [pid], set()
    while pending:
        child = pending.pop()
        try:
            groups.add(os.getpgid(child))
            children = Path(f"/proc/{child}/task/{child}/children").read_text().split()
            pending.extend(int(value) for value in children)
        except (OSError, ProcessLookupError):
            pass
    return groups - {os.getpgrp()}


def stop_browser_tree(process):
    # Capture groups before the parent exits/reparents its detached browser children.
    groups = descendant_groups(process.pid)
    for group in groups:
        try:
            os.killpg(group, signal.SIGTERM)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass
    # The parent may exit before a detached Chromium group; reap that group as well.
    for group in groups:
        try:
            os.killpg(group, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=5)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--playwright-module", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not sys.platform.startswith("linux"):
        parser.error("browser QA requires Linux process-tree cleanup")
    if not 1024 <= args.port <= 65535:
        parser.error("invalid port")
    args.output.mkdir(mode=0o700, parents=True, exist_ok=False)
    scripts = Path(__file__).resolve().parent
    base_url = f"http://127.0.0.1:{args.port}/"
    with tempfile.TemporaryDirectory(prefix="production-browser-fixture-") as temp:
        root = Path(temp)
        nonce = secrets.token_urlsafe(32)
        (root / ".synthetic-browser-fixture").write_text(nonce)
        store = Store.initialize(root / "test.sqlite3", root, "operator", root / "operator.key")
        store.add_identity(credential(root / "operator.key"), "executor", root / "executor.key",
                           request_id="synthetic-executor", reason="Synthetic browser fixture only")
        with subprocess.Popen([sys.executable, str(scripts / "production_web.py"), "--db", str(store.database),
                               "--root", str(root), "--port", str(args.port)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as server:
            try:
                opener = build_opener(ProxyHandler({}))
                for _ in range(50):
                    if server.poll() is not None:
                        raise RuntimeError("synthetic server exited; check port")
                    try:
                        with opener.open(base_url, timeout=1) as response:
                            if response.status == 200:
                                break
                    except OSError:
                        time.sleep(.1)
                else:
                    raise RuntimeError("synthetic server did not become ready")
                with subprocess.Popen(["node", str(scripts / "production_browser_smoke.cjs"),
                                       str(args.playwright_module.resolve()), base_url, str(root),
                                       str(args.output.resolve())], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, start_new_session=True,
                                      env={**os.environ, "PRODUCTION_BROWSER_FIXTURE_NONCE": nonce}) as run:
                    try:
                        stdout, stderr = run.communicate(timeout=120)
                        # The child deliberately emits only sanitized summaries, never call logs.
                        report = json.loads(stdout if run.returncode == 0 else stderr)
                        status = run.returncode
                    except subprocess.TimeoutExpired:
                        stop_browser_tree(run)
                        report, status = {"status": "failed", "phase": "browser-timeout; process tree stopped"}, 1
                    except (ValueError, OSError):
                        stop_browser_tree(run)
                        report, status = {"status": "failed", "phase": "browser runner; diagnostics suppressed"}, 1
                    except BaseException:
                        stop_browser_tree(run)
                        raise
                report["python"] = sys.version.split()[0]
                report["sourceHashes"] = {name: hashlib.sha256((scripts / name).read_bytes()).hexdigest()
                                          for name in ("production_browser_check.py", "production_browser_smoke.cjs", "production_web.py", "production_db.py")}
                (args.output / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
                print(json.dumps(report, ensure_ascii=False))
                return status
            finally:
                server.terminate()
                server.wait(timeout=10)


if __name__ == "__main__":
    raise SystemExit(main())
