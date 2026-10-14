"""Run both required Movies verification gates without a shell."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def verify(root: Path, python: str) -> int:
    """Run workspace validation and stdlib tests, preserving any failure."""
    commands = [
        [python, "-B", "scripts/manage.py", "validate"],
        [python, "-B", "-m", "unittest", "discover", "-s", "tests"],
    ]
    failed = 0
    for command in commands:
        print("Verification: " + " ".join(command), flush=True)
        try:
            status = subprocess.run(command, cwd=root, check=False).returncode
        except OSError as error:
            print(f"Verification could not start: {error}", file=sys.stderr)
            status = 127
        if status and not failed:
            failed = status if status > 0 else 1
    return failed


def main() -> int:
    """Verify the canonical workspace using this interpreter's environment."""
    return verify(Path(__file__).resolve().parents[1], sys.executable)


if __name__ == "__main__":
    raise SystemExit(main())
