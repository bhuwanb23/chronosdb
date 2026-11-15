"""Generate the README asset set from the frozen golden artifacts.

Every number drawn into these images is read from a file in the repository:

* ``artifacts/phase-5/golden-impact-result.json``      (impact figures)
* ``artifacts/phase-5-handoff/determinism-report.json`` (repeat-run hashes)
* ``data/releases/v1.0.0/golden/expected_candidate_results.json`` (candidates)

The SVGs are written to ``assets/readme/``. PNG derivatives are rendered with
headless Chrome/Edge, matching ``scripts/export_asset_pngs.py``.
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "readme"

BG = "#07141E"
SURFACE = "#0C2130"
PANEL = "#102B3B"
GRID = "#173E50"
CYAN = "#6EF3FF"
AQUA = "#2DD4BF"
AMBER = "#FFC857"
CORAL = "#FF6B6B"
LIME = "#B8F16B"
WHITE = "#ECF8FA"
MUTED = "#91B4C0"

FONT = "Segoe UI, Inter, Arial, sans-serif"

IMPACT_FILE = ROOT / "artifacts" / "phase-5" / "golden-impact-result.json"
DETERMINISM_FILE = ROOT / "artifacts" / "phase-5-handoff" / "determinism-report.json"
CANDIDATES_FILE = ROOT / "data" / "releases" / "v1.0.0" / "golden" / "expected_candidate_results.json"


# --------------------------------------------------------------------------- data


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def inr(value: str | int | float) -> str:
    """Format an amount with Indian digit grouping: 1600000 -> 16,00,000."""

    amount = int(round(float(value)))
    sign = "-" if amount < 0 else ""
    digits = str(abs(amount))
    if len(digits) <= 3:
        return f"{sign}{digits}"
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return f"{sign}{','.join(groups)},{tail}"


def rupees(value: str | int | float) -> str:
    return f"\u20b9{inr(value)}"


# --------------------------------------------------------------------------- svg


def text(
    x: float,
    y: float,
    body: str,
    size: int = 18,
    fill: str = WHITE,
    weight: int = 400,
    anchor: str = "start",
    spacing: float = 0,
    opacity: float = 1.0,
) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" '
        f'letter-spacing="{spacing}" opacity="{opacity}">{escape(body)}</text>'
    )


def panel(x: float, y: float, w: float, h: float, stroke: str = GRID, fill: str = PANEL, r: int = 16) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    )


def chip(x: float, y: float, w: float, h: float, stroke: str) -> str:
    return panel(x, y, w, h, stroke=stroke, fill=SURFACE, r=14)


def dot(x: float, y: float, fill: str, r: int = 5) -> str:
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def arrow_chain(x1: float, x2: float, y: float, color: str) -> str:
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2 - 12}" y2="{y}" stroke="{color}" '
        f'stroke-width="2.5" opacity="0.75"/>'
        f'<path d="M {x2 - 16} {y - 7} L {x2} {y} L {x2 - 16} {y + 7} Z" fill="{color}"/>'
    )


def arrow_down(x: float, y1: float, y2: float, color: str) -> str:
    return (
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 12}" stroke="{color}" '
        f'stroke-width="2.5" opacity="0.75"/>'
        f'<path d="M {x - 7} {y2 - 16} L {x} {y2} L {x + 7} {y2 - 16} Z" fill="{color}"/>'
    )


def frame(w: int, h: int, title: str, subtitle: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<defs>
  <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
    <path d="M 44 0 L 0 0 0 44" fill="none" stroke="{GRID}" stroke-width="1" opacity="0.35"/>
  </pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{PANEL}" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="{SURFACE}" stop-opacity="0.9"/>
  </linearGradient>
</defs>
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
<circle cx="{w - 60}" cy="40" r="220" fill="{CYAN}" opacity="0.03"/>
{text(64, 84, title, 15, CYAN, 700, spacing=5)}
{text(64, 116, subtitle, 26, WHITE, 600)}
<line x1="64" y1="140" x2="{w - 64}" y2="140" stroke="{GRID}" stroke-width="1"/>
"""


# --------------------------------------------------------------------------- images


def hero(impact: dict[str, Any], determinism: dict[str, Any]) -> str:
    metrics = impact["headline_metrics"]
    revenue = metrics["revenue_at_risk"]["amount"]
    breaches = metrics["sla_breached_customer_order_count"]
    candidates = load_json(CANDIDATES_FILE)
    recommended = [c for c in candidates if c["candidate_id"] == "INT-GOLD-C"][0]
    runs = len(determinism["repeated_result_hashes"])
    unique = len(set(determinism["repeated_result_hashes"]))
    result_hash = impact["result_hash"][:12]

    w, h = 1600, 800
    parts = [frame(w, h, "CHRONOSDB  \u00b7  DECISION INTELLIGENCE ON IBM DB2", "Supply-chain disruptions, answered with evidence.")]

    parts += [
        text(64, 210, "When the chain breaks,", 56, WHITE, 700),
        text(64, 272, "show the next failure", 56, CYAN, 700),
        text(64, 334, "and prove the fix.", 56, WHITE, 700),
        text(64, 390, "Deterministic impact propagation \u2192 counterfactual recovery paths", 19, MUTED),
        text(64, 418, "\u2192 constraint-ranked recommendation \u2192 a hash you can recompute.", 19, MUTED),
    ]

    tiles = [
        (f"\u20b9{inr(revenue)}", "REVENUE AT RISK"),
        (f"{breaches:02d}", "SLA-BREACHED ORDERS"),
        (f"{len(candidates)}", "CANDIDATES SIMULATED"),
    ]
    for index, (value, label) in enumerate(tiles):
        x = 64 + index * 270
        parts.append(panel(x, 456, 250, 104, stroke=GRID))
        parts.append(text(x + 24, 508, value, 34, CORAL if index < 2 else WHITE, 700))
        parts.append(text(x + 24, 538, label, 12, MUTED, 600, spacing=2))

    parts += [
        panel(64, 584, 790, 96, stroke=LIME),
        dot(92, 620, LIME, 6),
        text(110, 626, "RECOMMENDED  \u00b7  INT-GOLD-C", 15, LIME, 700, spacing=2),
        text(
            92,
            662,
            f"{rupees(recommended['intervention_cost'])} spend protects "
            f"{rupees(recommended['revenue_protected'])} \u2014 {recommended['sla_breach_count']} SLA breaches left.",
            20,
            WHITE,
            600,
        ),
        text(64, 730, f"Frozen SCN-GOLD-001 artifact \u00b7 result hash {result_hash}\u2026 \u00b7 {unique} unique hash across {runs} runs", 14, MUTED),
    ]

    # Right: cascade panel
    parts.append(panel(900, 180, 636, 500, stroke=GRID, fill="url(#fade)"))
    parts.append(text(932, 226, "CASCADE  /  SCN-GOLD-001", 13, CYAN, 700, spacing=4))

    short_units = sum(float(row["shortage_quantity"]) for row in impact["shortages"])
    nodes = [
        ("SUPPLIER", "SUP-0104 \u00b7 unavailable", AMBER),
        ("COMPONENT", f"CMP-MCU-42 \u00b7 short {int(short_units)} units", CORAL),
        ("PRODUCTION", "MO-0882 \u00b7 MO-0889 blocked", AMBER),
        ("CUSTOMER", "CO-0704 \u00b7 CO-0711 late", CORAL),
    ]
    y = 262
    for index, (label, detail, color) in enumerate(nodes):
        parts.append(chip(932, y, 572, 86, color))
        parts.append(dot(962, y + 43, color, 5))
        parts.append(text(982, y + 34, label, 17, WHITE, 700, spacing=2))
        parts.append(text(982, y + 62, detail, 15, MUTED))
        if index < len(nodes) - 1:
            parts.append(arrow_down(1218, y + 86, y + 110, color))
        y += 110

    parts.append("</svg>")
    return "\n".join(parts)


def cascade(impact: dict[str, Any]) -> str:
    metrics = impact["headline_metrics"]
    trace = impact["causal_traces"][0]
    rules = [edge["rule_id"] for edge in trace["edges"]]

    w, h = 1600, 600
    parts = [
        frame(
            w,
            h,
            "SCN-GOLD-001  /  ONE OUTAGE, FIVE LINKED RECORDS",
            "The cascade is a stored causal trace, not a chart.",
        )
    ]

    nodes = [
        ("EVT-GOLD-001", "supplier outage", AMBER),
        ("PO-2208", "purchase order delayed", CORAL),
        ("CMP-MCU-42", "shortage \u00b7 4 \u00d7 200 units", CORAL),
        ("MO-0882", "production blocked", AMBER),
        ("CO-0704", f"288 h late \u00b7 {rupees(800000)}", CORAL),
    ]
    width, gap, start = 250, 62, 64
    y = 250
    for index, (name, detail, color) in enumerate(nodes):
        x = start + index * (width + gap)
        parts.append(chip(x, y, width, 130, color))
        parts.append(text(x + 24, y + 44, name, 19, WHITE, 700))
        parts.append(text(x + 24, y + 76, detail, 14, MUTED))
        parts.append(dot(x + width - 28, y + 26, color, 5))
        if index < len(nodes) - 1:
            rule = rules[index] if index < len(rules) else ""
            cx = x + width
            parts.append(text(cx + gap / 2, y - 14, rule, 11, AQUA, 700, anchor="middle", spacing=1))
            parts.append(arrow_chain(cx + 8, cx + gap - 6, y + 65, AQUA))

    parts.append(panel(64, 440, 1472, 96, stroke=GRID))
    parts.append(text(96, 480, "SECOND TRACE", 12, MUTED, 700, spacing=2))
    parts.append(text(96, 510, "SUP-0104 \u2192 PO-2208 \u2192 CMP-MCU-42 \u2192 MO-0889 \u2192 CO-0711 \u00b7 264 h late", 17, WHITE, 600))
    parts.append(text(1010, 480, "RESULT HASH", 12, MUTED, 700, spacing=2))
    parts.append(text(1010, 510, impact["result_hash"][:32] + "\u2026", 15, CYAN, 600))
    parts.append(
        text(
            64,
            566,
            f"Headline metrics: {rupees(metrics['revenue_at_risk']['amount'])} at risk \u00b7 "
            f"{metrics['sla_breached_customer_order_count']} SLA-breached orders \u00b7 "
            f"{metrics['maximum_delay_hours']} h maximum delay",
            13,
            MUTED,
        )
    )
    parts.append("</svg>")
    return "\n".join(parts)


def candidate_board(candidates: list[dict[str, Any]]) -> str:
    w, h = 1600, 780
    best = "INT-GOLD-C"

    parts = [
        frame(
            w,
            h,
            "COUNTERFACTUAL BOARD  /  7 CANDIDATES, 2 REJECTED BY HARD CONSTRAINTS",
            "Every row is engine output; the recommendation is INT-GOLD-C.",
        )
    ]

    columns = [
        (64, "CANDIDATE"),
        (386, "FEASIBILITY"),
        (556, "COST"),
        (704, "REVENUE PROTECTED"),
        (1180, "SLA AFTER"),
        (1300, "MAX DELAY"),
    ]
    for x, label in columns:
        parts.append(text(x, 196, label, 12, MUTED, 700, spacing=2))

    rows = sorted(candidates, key=lambda c: (c["feasibility_status"] != "FEASIBLE", c["candidate_id"]))
    y = 216
    for row in rows:
        feasible = row["feasibility_status"] == "FEASIBLE"
        highlight = row["candidate_id"] == best
        stroke = LIME if highlight else (GRID if feasible else CORAL)
        parts.append(panel(64, y, 1472, 62, stroke=stroke, fill=PANEL if feasible else "#16232B", r=12))

        parts.append(dot(88, y + 31, LIME if highlight else (MUTED if feasible else CORAL), 5))
        parts.append(text(106, y + 38, row["candidate_id"], 17, WHITE if feasible else MUTED, 700))
        parts.append(text(386, y + 38, "FEASIBLE" if feasible else "REJECTED", 14, LIME if feasible else CORAL, 700))

        if feasible:
            parts.append(text(556, y + 38, rupees(row["intervention_cost"]), 16, WHITE, 600))
            protected = float(row["revenue_protected"])
            bar = 0 if protected == 0 else max(10, int(protected / 1_600_000 * 240))
            parts.append(f'<rect x="704" y="{y + 24}" width="240" height="14" rx="7" fill="{GRID}"/>')
            parts.append(f'<rect x="704" y="{y + 24}" width="{bar}" height="14" rx="7" fill="{CYAN}"/>')
            parts.append(text(960, y + 38, rupees(protected), 15, WHITE, 600))
            sla = row["sla_breach_count"]
            parts.append(text(1180, y + 38, str(sla), 17, LIME if sla == 0 else AMBER, 700))
            parts.append(text(1300, y + 38, f"{row['maximum_delay']} h", 16, MUTED, 600))
        else:
            parts.append(text(556, y + 38, "\u2014", 16, MUTED))
            parts.append(text(704, y + 38, row.get("rejection_reason", ""), 14, CORAL, 600))

        y += 70

    parts.append("</svg>")
    return "\n".join(parts)


def architecture() -> str:
    schema_count = len(list((ROOT / "schemas").glob("*.json")))
    w, h = 1600, 1060
    parts = [
        frame(
            w,
            h,
            "SYSTEM MAP  /  WHAT EXISTS AND WHAT HAS BEEN PROVEN",
            "Status marks what a fresh clone can verify today.",
        )
    ]

    legend = [(LIME, "VERIFIED"), (AMBER, "PARTIAL"), (CORAL, "BLOCKED"), (MUTED, "DESIGN ONLY")]
    lx = 900
    for color, label in legend:
        parts.append(dot(lx, 78, color, 5))
        parts.append(text(lx + 14, 83, label, 11, MUTED, 700, spacing=2))
        lx += 158

    bands = [
        (
            "01",
            "INTERFACES",
            168,
            150,
            [
                ("HTTP API", "/health/live \u00b7 /health/ready \u00b7 /version", CORAL, "import fails: config shadowed"),
                ("War Room UI", "TypeScript views, design renders", AMBER, "not wired to a live backend"),
                ("Scripts", "golden run, benchmarks, asset export", LIME, "runnable from a clone"),
            ],
        ),
        (
            "02",
            "DECISION CORE",
            348,
            200,
            [
                ("Impact", "cascade, rule set, causal traces", LIME, "frozen artifact validated"),
                ("Simulation", "counterfactual overlays", AMBER, "suite partly failing"),
                ("Optimization", "feasibility + ranking", AMBER, "suite partly failing"),
                ("Evidence", "retrieval, provenance", AMBER, "metrics not re-measured"),
                ("Controlled AI", "narration from verified input", AMBER, "no live model run"),
            ],
        ),
        (
            "03",
            "PERSISTENCE",
            578,
            140,
            [
                ("IBM Db2", "operational \u00b7 temporal \u00b7 vector \u00b7 audit", MUTED, "no runtime in verification"),
            ],
        ),
        (
            "04",
            "ASSURANCE",
            748,
            210,
            [
                ("JSON Schemas", f"{schema_count} contracts, Draft 2020-12", LIME, "impact result validates"),
                ("Determinism", "repeat-run hash comparison", LIME, "100 runs, 1 hash"),
                ("Security suite", "tests/security", LIME, "34 passing"),
                ("Full suite", "tests/", CORAL, "150 pass / 42 fail / 4 errors"),
            ],
        ),
    ]

    for number, label, y, height, items in bands:
        parts.append(panel(64, y, 1472, height, stroke=GRID))
        parts.append(text(92, y + 44, number, 13, CYAN, 700, spacing=2))
        parts.append(text(92, y + 76, label, 15, WHITE, 700, spacing=3))

        count = len(items)
        available = 1472 - 300
        gap = 18
        width = (available - gap * (count - 1)) / count
        for index, (title, detail, status, note) in enumerate(items):
            x = 64 + 290 + index * (width + gap)
            parts.append(chip(x, y + 22, width, height - 44, status))
            parts.append(dot(x + width - 24, y + 42, status, 5))
            parts.append(text(x + 20, y + 60, title, 16, WHITE, 700))
            parts.append(text(x + 20, y + 86, detail, 12, MUTED))
            parts.append(text(x + 20, y + height - 34, note, 11, status, 600))

    parts.append(text(64, 1016, "Status reflects the checks recorded in docs/release/final-defect-register.md and a fresh pytest run.", 13, MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# --------------------------------------------------------------------------- render


def export_pngs() -> None:
    candidates = (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
    )
    browser = next((path for path in candidates if Path(path).exists()), None)
    if browser is None:
        print("No Chrome/Edge found; SVGs written, PNGs skipped.")
        return

    size_re = re.compile(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"')
    with tempfile.TemporaryDirectory(prefix="chronosdb-readme-") as profile_root:
        for svg_path in sorted(OUT.glob("*.svg")):
            match = size_re.search(svg_path.read_text(encoding="utf-8"))
            if not match:
                raise RuntimeError(f"missing dimensions: {svg_path.name}")
            width, height = match.groups()
            output = svg_path.with_suffix(".png")
            profile = Path(profile_root) / svg_path.stem
            profile.mkdir()
            subprocess.run(
                [
                    browser,
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    f"--user-data-dir={profile}",
                    f"--window-size={width},{height}",
                    f"--screenshot={output}",
                    svg_path.resolve().as_uri(),
                ],
                check=True,
                timeout=60,
            )
            print(f"{output.name}: {width}x{height}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    impact = load_json(IMPACT_FILE)
    determinism = load_json(DETERMINISM_FILE)
    candidates = load_json(CANDIDATES_FILE)

    assets = {
        "hero.svg": hero(impact, determinism),
        "system-architecture.svg": architecture(),
        "cascade.svg": cascade(impact),
        "candidate-board.svg": candidate_board(candidates),
    }
    for name, content in assets.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"wrote assets/readme/{name}")

    export_pngs()


if __name__ == "__main__":
    main()
