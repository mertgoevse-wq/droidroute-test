#!/usr/bin/env python3
"""Design gate — the mechanical part of docs/14-design-system.md.

    python3 tools/check_design_slop.py              # scan the UI sources
    python3 tools/check_design_slop.py --self-test   # prove the gate still bites
    python3 tools/check_design_slop.py --path <dir>  # scan somewhere else

What it catches (all decidable from source; the craft tests in docs/14 §11 catch
the rest, and a passing gate is not evidence that a screen is good):

1. Banned aesthetics  — glass/blur, gradient brushes, decorative shadow or elevation
2. Unmanaged values   — hardcoded colours, off-scale dp, stray radii
3. Untranslated text  — user-facing string literals inside composables
4. Missing states     — a screen that collects state but never names loading/empty/error

A line carrying ``design-allow: <reason>`` is exempt, so a genuine exception is
visible in the diff instead of hiding in a threshold.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCAN = ROOT / "app" / "src" / "main" / "kotlin"
TOKENS_FILE = "Tokens.kt"
ALLOW = "design-allow:"

# 1 — banned aesthetics -------------------------------------------------------
BANNED = [
    (r"Modifier\s*\.\s*blur\s*\(", "blur — a banned aesthetic (docs/14 §11)"),
    (r"Brush\s*\.\s*(horizontal|vertical|linear|radial|sweep)Gradient\s*\(", "gradient brush — banned as decoration (docs/14 §11)"),
    (r"\.shadow\s*\(", "drop shadow — depth is borders-only (docs/14 §7)"),
    (r"tonalElevation|shadowElevation|cardElevation", "elevation shadow — depth is borders-only (docs/14 §7)"),
    (r"glassmorphism|neumorph|skeuomorph|liquidGlass|frosted", "banned aesthetic by name (docs/14 §11)"),
    (r"\.alpha\s*\(\s*0?\.\d+\s*\)\s*\.\s*blur", "fake glass layering"),
]

# 2 — unmanaged values -------------------------------------------------------
COLOR_LITERAL = re.compile(r"Color\s*\(\s*0x[0-9A-Fa-f]{6,8}\s*\)")
DP_LITERAL = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*\.\s*dp\b")
RADIUS_LITERAL = re.compile(r"RoundedCornerShape\s*\(\s*(\d+(?:\.\d+)?)\s*\.\s*dp\s*\)")
SPACING_SCALE = {0, 1, 2, 3, 4, 6, 8, 12, 16, 20, 24, 32, 48, 64, 96, 128, 200}
RADIUS_SCALE = {0, 4, 8, 12, 16, 999}

# 3 — untranslated user-facing text -----------------------------------------
TEXT_LITERAL = re.compile(r"""\bText\s*\(\s*(?:text\s*=\s*)?"([^"\\]{2,})" """.strip())

# 4 — missing states --------------------------------------------------------
STATE_MARKERS = ("loading", "empty", "error")


def scan_text(text: str, rel: str) -> list[str]:
    """Return one message per violation in a single source file."""
    problems: list[str] = []
    lines = text.splitlines()
    is_tokens = Path(rel).name == TOKENS_FILE
    is_screen = Path(rel).name.endswith("Screen.kt")

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("*") or ALLOW in line:
            continue

        for pattern, why in BANNED:
            if re.search(pattern, line):
                problems.append(f"{rel}:{number}: {why}")

        if not is_tokens:
            if COLOR_LITERAL.search(line):
                problems.append(f"{rel}:{number}: hardcoded colour — use a token from ui/theme/Tokens.kt (docs/14 §5)")
        if not is_tokens:
            for value in DP_LITERAL.findall(line):
                if float(value) not in SPACING_SCALE:
                    problems.append(f"{rel}:{number}: {value}.dp is off the spacing scale (docs/14 §7)")
            for value in RADIUS_LITERAL.findall(line):
                if float(value) not in RADIUS_SCALE:
                    problems.append(f"{rel}:{number}: {value}.dp radius is off the shape scale (docs/14 §7)")

        match = TEXT_LITERAL.search(line)
        if match:
            problems.append(
                f'{rel}:{number}: user-facing literal {match.group(1)!r} — use stringResource (T-093)'
            )

    if is_screen and ("collectAsState" in text or "uiState" in text):
        lowered = text.lower()
        missing = [marker for marker in STATE_MARKERS if marker not in lowered]
        if missing:
            problems.append(
                f"{rel}: screen collects state but never names: {', '.join(missing)} (docs/14 §10)"
            )
    return problems


def scan(target: Path) -> tuple[list[str], int]:
    files = sorted(target.rglob("*.kt")) if target.exists() else []
    problems: list[str] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:  # pragma: no cover
            continue
        problems.extend(scan_text(text, str(path.relative_to(target.parent))))
    return problems, len(files)


BAD_FIXTURE = """
package com.droidroute.ui.demo
import androidx.compose.ui.graphics.Color
val surface = Color(0xFF1B1E23)
@Composable
fun DemoCard(uiState: DemoState) {
    val state by uiState.collectAsState()
    Box(Modifier.shadow(8.dp).background(Brush.horizontalGradient(listOf(surface, surface)))) {
        Text("Willkommen bei DroidRoute")
        Spacer(Modifier.height(13.dp))
    }
}
"""

GOOD_FIXTURE = """
package com.droidroute.ui.demo
import com.droidroute.ui.theme.Tokens
@Composable
fun DemoCard(uiState: DemoState) {
    val state by uiState.collectAsState()
    when {
        state.loading -> Skeleton()
        state.error -> ErrorRow(state.error)
        state.isEmpty -> EmptyState()
        else -> Box(Modifier.padding(16.dp).border(1.dp, Tokens.line, RoundedCornerShape(8.dp))) {
            Text(stringResource(R.string.demo_title))
        }
    }
}
"""


def self_test() -> int:
    """Prove the gate still bites: the bad fixture must fail, the good one must pass."""
    work = Path(tempfile.mkdtemp(prefix="design-slop-"))
    try:
        (work / "ui").mkdir()
        (work / "ui" / "Bad.kt").write_text(BAD_FIXTURE, encoding="utf-8")
        bad, _ = scan(work / "ui")

        (work / "ui" / "Bad.kt").unlink()
        (work / "ui" / "Good.kt").write_text(GOOD_FIXTURE, encoding="utf-8")
        good, _ = scan(work / "ui")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    if not bad:
        print("SELF-TEST FAILED  the gate found nothing in a file that violates every rule")
        return 1
    if good:
        print("SELF-TEST FAILED  the gate flagged a compliant file:")
        for line in good:
            print(f"  {line}")
        return 1

    print(f"self-test ok — {len(bad)} violations detected in the bad fixture, 0 in the good one")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="verify the gate itself")
    parser.add_argument("--path", type=Path, default=DEFAULT_SCAN, help="directory to scan")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    problems, scanned = scan(args.path)
    if scanned == 0:
        print(
            f"no Kotlin sources under {args.path.relative_to(ROOT) if args.path.is_relative_to(ROOT) else args.path} "
            "— nothing to check. The gate becomes evidence when phase 07 lands; "
            "run --self-test to confirm it still bites."
        )
        return 0

    for line in problems:
        print(f"FAIL  {line}")

    if problems:
        print(f"\n{len(problems)} design violation(s) across {scanned} file(s)")
        print("rules: docs/14-design-system.md · handbooks/07-anti-slop-rules.md §11–§14")
        return 1

    print(f"design gate clean — {scanned} file(s) scanned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
