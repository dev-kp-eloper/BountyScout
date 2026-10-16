#!/usr/bin/env python3
"""Minimal build gate — syntax-check scout_bounties.py."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    target = ROOT / "scout_bounties.py"
    if not target.is_file():
        print(f"Missing {target.name}", file=sys.stderr)
        return 1
    py_compile.compile(str(target), doraise=True)
    print("OK: scout_bounties.py syntax check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
