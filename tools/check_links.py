#!/usr/bin/env python3
"""Check that every relative markdown link points at a file that exists.

    python3 tools/check_links.py

Exit code 0 when the documentation set is internally consistent, 1 otherwise.
External links (http/https/mailto) and pure anchors are ignored on purpose —
link checking over the network is flaky and is not evidence of correctness.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_DIRS = {".git", "build", "node_modules", ".gradle", "archive"}
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def main() -> int:
    broken: list[str] = []
    checked = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = Path(dirpath) / name
            rel = path.relative_to(ROOT)
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for target in LINK.findall(text):
                if target.startswith(SKIP_PREFIXES):
                    continue
                clean = urllib.parse.unquote(target.split("#", 1)[0].strip())
                if not clean:
                    continue
                checked += 1
                resolved = (path.parent / clean).resolve()
                if not resolved.exists():
                    broken.append(f"{rel} -> {target}")

    if broken:
        print("broken relative links:")
        for line in broken:
            print(f"  {line}")
        print(f"\n{len(broken)} broken of {checked} checked")
        return 1

    print(f"all {checked} relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
