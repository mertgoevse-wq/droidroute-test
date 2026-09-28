#!/usr/bin/env python3
"""Design gate — the mechanical part of docs/14-design-system.md.

    python3 tools/check_design_slop.py              # scan the UI sources and the drawings
    python3 tools/check_design_slop.py --self-test   # prove the gate still bites
    python3 tools/check_design_slop.py --path <dir>  # scan somewhere else

What it catches (all decidable from source; the craft tests in docs/14 §11 catch
the rest, and a passing gate is not evidence that a screen is good):

1. Banned aesthetics  — glass/blur, gradient brushes, decorative shadow or elevation
2. Unmanaged values   — hardcoded colours, off-scale dp, stray radii
3. Untranslated text  — user-facing string literals inside composables
4. Missing states     — a screen that collects state but never names loading/empty/error
5. Drawings           — design/**/*.svg must parse as XML, and every drawing must obey
                        the same bans as the app (design/README.md §2, docs/14 §11)

A line carrying ``design-allow: <reason>`` is exempt, so a genuine exception is
visible in the diff instead of hiding in a threshold.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import xml.dom.minidom
import xml.parsers.expat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCAN = ROOT / "app" / "src" / "main" / "kotlin"
DESIGN_DIR = ROOT / "design"
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

# 5 — the drawings ----------------------------------------------------------
# A drawing may not show what the app may not build. Same bans, applied to the
# artefacts in design/ — otherwise the previews would quietly teach the wrong
# thing to whoever implements the next screen.
BANNED_ASSET = [
    (r"<(?:linear|radial|conic)Gradient\b", "gradient element — banned in drawings (design/README.md §2)"),
    (r"<filter\b|feGaussianBlur|feDropShadow", "filter or shadow — depth is borders-only (docs/14 §7)"),
    # `filter: blur(4px)` is a defect; `element.blur()` is a DOM call. The dot is the difference.
    (r"(?<![\w.-])(?:backdrop-)?blur\s*\(", "blur — banned aesthetic (docs/14 §11)"),
    (r"box-shadow|text-shadow", "shadow — depth is borders-only (docs/14 §7)"),
]
ASSET_SUFFIXES = {".svg", ".html"}


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


def scan_asset_text(text: str, rel: str, *, is_svg: bool) -> list[str]:
    """Return one message per violation in a single drawing."""
    problems: list[str] = []
    if is_svg:
        # An SVG that is not well-formed XML does not render as a file, only as an
        # inline fragment — the kind of defect that survives to a release unnoticed.
        try:
            xml.dom.minidom.parseString(text)
        except xml.parsers.expat.ExpatError as error:  # pragma: no cover - fixture covers it
            problems.append(f"{rel}: not well-formed XML ({error})")
    for number, line in enumerate(text.splitlines(), start=1):
        if ALLOW in line:
            continue
        for pattern, why in BANNED_ASSET:
            if re.search(pattern, line):
                problems.append(f"{rel}:{number}: {why}")
    return problems


def scan_design(target: Path) -> tuple[list[str], int]:
    """Check every drawing: parse the vectors, ban the same aesthetics as the app."""
    if not target.exists():
        return [], 0
    files = sorted(p for p in target.rglob("*") if p.is_file() and p.suffix in ASSET_SUFFIXES)
    problems: list[str] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:  # pragma: no cover
            continue
        rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
        problems.extend(scan_asset_text(text, rel, is_svg=path.suffix == ".svg"))
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


BAD_ASSET = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <!-- ---------- a separator XML does not allow ---------- -->
  <defs>
    <linearGradient id="g"><stop offset="0" stop-color="#fff"/></linearGradient>
    <filter id="f"><feGaussianBlur stdDeviation="2"/></filter>
  </defs>
  <rect width="24" height="24" filter="url(#f)"/>
</svg>
"""

GOOD_ASSET = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <!-- a compliant drawing: geometry only, borders only -->
  <circle cx="12" cy="12" r="7" stroke="#DE8F57" stroke-width="2"/>
  <line x1="2" y1="12" x2="22" y2="12" stroke="#E5E8EB" stroke-width="2"/>
</svg>
"""


def self_test() -> int:
    """Prove the gate still bites: the bad fixtures must fail, the good ones must pass."""
    work = Path(tempfile.mkdtemp(prefix="design-slop-"))
    try:
        (work / "ui").mkdir()
        (work / "ui" / "Bad.kt").write_text(BAD_FIXTURE, encoding="utf-8")
        bad, _ = scan(work / "ui")

        (work / "ui" / "Bad.kt").unlink()
        (work / "ui" / "Good.kt").write_text(GOOD_FIXTURE, encoding="utf-8")
        good, _ = scan(work / "ui")

        (work / "assets").mkdir()
        (work / "assets" / "bad.svg").write_text(BAD_ASSET, encoding="utf-8")
        bad_assets, _ = scan_design(work / "assets")

        (work / "assets" / "bad.svg").unlink()
        (work / "assets" / "good.svg").write_text(GOOD_ASSET, encoding="utf-8")
        good_assets, _ = scan_design(work / "assets")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    failures: list[str] = []
    if not bad:
        failures.append("the gate found nothing in a Kotlin file that violates every rule")
    if good:
        failures.append("the gate flagged a compliant Kotlin file:")
        failures.extend(f"  {line}" for line in good)
    if len(bad_assets) < 3:
        failures.append(
            "the gate missed part of a drawing that has a broken comment, a gradient and a filter "
            f"(found {len(bad_assets)})"
        )
    if good_assets:
        failures.append("the gate flagged a compliant drawing:")
        failures.extend(f"  {line}" for line in good_assets)

    if failures:
        print("SELF-TEST FAILED")
        for line in failures:
            print(f"  {line}")
        return 1

    print(
        f"self-test ok — {len(bad)} violations in the bad Kotlin fixture, 0 in the good one; "
        f"{len(bad_assets)} in the bad drawing, 0 in the good one"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="verify the gate itself")
    parser.add_argument("--path", type=Path, default=DEFAULT_SCAN, help="directory to scan")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    problems, scanned = scan(args.path)
    asset_problems, assets = scan_design(DESIGN_DIR)
    problems.extend(asset_problems)

    source_label = args.path.relative_to(ROOT) if args.path.is_relative_to(ROOT) else args.path
    if scanned == 0:
        print(
            f"no Kotlin sources under {source_label} — nothing to check there. "
            "The source gate becomes evidence when phase 07 lands; "
            "run --self-test to confirm it still bites."
        )

    for line in problems:
        print(f"FAIL  {line}")

    if problems:
        print(f"\n{len(problems)} design violation(s) across {scanned} source and {assets} drawing file(s)")
        print("rules: docs/14-design-system.md · handbooks/07-anti-slop-rules.md §11–§14")
        return 1

    print(f"design gate clean — {scanned} source file(s) and {assets} drawing(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
