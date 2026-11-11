"""Generate the ChronosDB visual identity and technical asset pack.

The assets are deliberately generated from editable SVG source so the same
visual language can be reused in the product, README, demo video, and pitch
materials. PNG derivatives are written beside each SVG.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "chronosdb"

BG = "#07141E"
BG_2 = "#0A1D2A"
SURFACE = "#0F2938"
PANEL = "#123244"
GRID = "#194456"
CYAN = "#6EF3FF"
AQUA = "#2DD4BF"
AMBER = "#FFC857"
CORAL = "#FF6B6B"
LIME = "#B8F16B"
WHITE = "#ECF8FA"
MUTED = "#91B4C0"


def esc(value: object) -> str:
    return escape(str(value))


def defs() -> str:
    return dedent(
        f"""
        <defs>
          <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="{BG}"/>
            <stop offset="0.58" stop-color="{BG_2}"/>
            <stop offset="1" stop-color="#102C3A"/>
          </linearGradient>
          <linearGradient id="cyanFlow" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stop-color="{CYAN}" stop-opacity="0.15"/>
            <stop offset="0.5" stop-color="{CYAN}"/>
            <stop offset="1" stop-color="{AQUA}"/>
          </linearGradient>
          <linearGradient id="riskFlow" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stop-color="{AMBER}"/>
            <stop offset="1" stop-color="{CORAL}"/>
          </linearGradient>
          <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#193E4D" stop-opacity="0.95"/>
            <stop offset="1" stop-color="#0B202D" stop-opacity="0.8"/>
          </linearGradient>
          <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
            <path d="M 44 0 L 0 0 0 44" fill="none" stroke="{GRID}" stroke-width="1" opacity="0.42"/>
            <circle cx="0" cy="0" r="1.4" fill="{CYAN}" opacity="0.35"/>
          </pattern>
          <filter id="glowCyan" x="-100%" y="-100%" width="300%" height="300%">
            <feGaussianBlur stdDeviation="7" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
          <filter id="glowAmber" x="-100%" y="-100%" width="300%" height="300%">
            <feGaussianBlur stdDeviation="6" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
          <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000" flood-opacity="0.3"/>
          </filter>
          <marker id="arrowCyan" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="{CYAN}"/>
          </marker>
          <marker id="arrowAmber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="{AMBER}"/>
          </marker>
        </defs>
        """
    )


def start(width: int, height: int, title: str, subtitle: str = "") -> str:
    sub = (
        f'<text x="76" y="116" fill="{MUTED}" font-size="20" '
        f'font-family="Segoe UI, Arial, sans-serif" letter-spacing="0.4">{esc(subtitle)}</text>'
        if subtitle
        else ""
    )
    return dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
             viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
          <title id="title">{esc(title)}</title>
          <desc id="desc">ChronosDB visual asset in the Temporal Operations design system.</desc>
          {defs()}
          <rect width="{width}" height="{height}" rx="28" fill="url(#bg)"/>
          <rect width="{width}" height="{height}" rx="28" fill="url(#grid)" opacity="0.42"/>
          <circle cx="{width - 130}" cy="-20" r="260" fill="{CYAN}" opacity="0.05"/>
          <circle cx="-90" cy="{height + 60}" r="270" fill="{AQUA}" opacity="0.04"/>
          <text x="76" y="78" fill="{WHITE}" font-size="30" font-weight="700"
                font-family="Segoe UI, Arial, sans-serif" letter-spacing="1.3">{esc(title.upper())}</text>
          {sub}
        """
    )


def end() -> str:
    return "</svg>\n"


def text(x: float, y: float, value: str, size: int = 18, color: str = WHITE,
         weight: int = 400, anchor: str = "start", spacing: float = 0) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" letter-spacing="{spacing}" '
        f'font-family="Segoe UI, Arial, sans-serif">{esc(value)}</text>'
    )


def rounded(x: float, y: float, width: float, height: float, fill: str = "url(#glass)",
            stroke: str = GRID, radius: int = 16, opacity: float = 1) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" opacity="{opacity}"/>'
    )


def pill(x: float, y: float, label: str, color: str = CYAN, width: int | None = None) -> str:
    width = width or max(96, len(label) * 8 + 36)
    return (
        rounded(x, y, width, 32, fill=color, stroke=color, radius=16, opacity=0.13)
        + f'<circle cx="{x + 16}" cy="{y + 16}" r="4" fill="{color}"/>'
        + text(x + 28, y + 21, label, 12, color, 700, spacing=0.7)
    )


def dot(x: float, y: float, color: str = CYAN, radius: int = 7, glow: bool = False) -> str:
    return (
        f'<circle cx="{x}" cy="{y}" r="{radius * 2.3}" fill="{color}" opacity="0.12" '
        f'{"filter=\"url(#glowCyan)\"" if glow and color == CYAN else ""}/>'
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" '
        f'{"filter=\"url(#glowCyan)\"" if glow and color == CYAN else ""}/>'
    )


def node(x: float, y: float, label: str, sub: str, color: str = CYAN, width: int = 190) -> str:
    return (
        rounded(x - width / 2, y - 42, width, 84, fill="url(#glass)", stroke=color)
        + dot(x - width / 2 + 22, y - 15, color, 5)
        + text(x - width / 2 + 40, y - 11, label, 16, WHITE, 700)
        + text(x - width / 2 + 40, y + 16, sub, 12, MUTED, 400)
    )


def metric(x: float, y: float, label: str, value: str, accent: str = CYAN, width: int = 210) -> str:
    return (
        rounded(x, y, width, 98, fill="#102B39", stroke=GRID)
        + text(x + 20, y + 28, label.upper(), 11, MUTED, 700, spacing=1.2)
        + text(x + 20, y + 70, value, 28, accent, 700)
    )


def logo_mark(size: int = 512) -> str:
    c = size / 2
    return dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
          <title>ChronosDB logo mark</title>
          {defs()}
          <rect width="{size}" height="{size}" rx="{size * 0.22}" fill="{BG}"/>
          <circle cx="{c}" cy="{c}" r="178" fill="none" stroke="{GRID}" stroke-width="18"/>
          <path d="M {c - 178} {c} A 178 178 0 0 1 {c + 108} {c - 142}"
                fill="none" stroke="{CYAN}" stroke-width="18" stroke-linecap="round" filter="url(#glowCyan)"/>
          <path d="M {c + 178} {c} A 178 178 0 0 1 {c - 108} {c + 142}"
                fill="none" stroke="{AMBER}" stroke-width="18" stroke-linecap="round" opacity="0.92"/>
          <circle cx="{c + 108}" cy="{c - 142}" r="15" fill="{CYAN}" filter="url(#glowCyan)"/>
          <circle cx="{c - 108}" cy="{c + 142}" r="15" fill="{AMBER}"/>
          <path d="M {c - 104} {c - 54} Q {c} {c - 118} {c + 104} {c - 54}
                   L {c + 104} {c + 84} Q {c} {c + 148} {c - 104} {c + 84} Z"
                fill="#123244" stroke="{WHITE}" stroke-width="7"/>
          <ellipse cx="{c}" cy="{c - 54}" rx="104" ry="36" fill="#194456" stroke="{WHITE}" stroke-width="7"/>
          <path d="M {c - 103} {c + 6} Q {c} {c + 69} {c + 103} {c + 6}"
                fill="none" stroke="{CYAN}" stroke-width="7" opacity="0.9"/>
          <path d="M {c - 103} {c + 68} Q {c} {c + 131} {c + 103} {c + 68}"
                fill="none" stroke="{CYAN}" stroke-width="7" opacity="0.9"/>
          <path d="M {c - 43} {c - 12} L {c - 4} {c + 26} L {c + 54} {c - 32}"
                fill="none" stroke="{LIME}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """
    )


def lockup() -> str:
    return dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320">
          <title>ChronosDB logo lockup</title>
          {defs()}
          <rect width="1200" height="320" rx="36" fill="{BG}"/>
          <g transform="translate(34,34) scale(0.49)">{logo_mark(512).split("<svg", 1)[1].split(">", 1)[1].rsplit("</svg>", 1)[0]}</g>
          {text(326, 143, "Chronos", 70, WHITE, 700, spacing=-2)}
          {text(635, 143, "DB", 70, CYAN, 700, spacing=-2)}
          {text(330, 194, "RECONSTRUCT  /  SIMULATE  /  PROVE", 17, MUTED, 700, spacing=3)}
          <path d="M 332 235 H 850" stroke="url(#cyanFlow)" stroke-width="3"/>
          <circle cx="332" cy="235" r="5" fill="{CYAN}"/>
          <circle cx="850" cy="235" r="5" fill="{AMBER}"/>
        </svg>
        """
    )


def hero() -> str:
    s = start(1600, 900, "The Db2 time machine", "AUDITABLE COUNTERFACTUAL INTELLIGENCE  /  SUPPLY-CHAIN DISRUPTIONS")
    s += pill(76, 154, "LIVE SCENARIO", CYAN, 148)
    s += text(76, 270, "When the chain breaks,", 58, WHITE, 700)
    s += text(76, 338, "see the next failure", 58, CYAN, 700)
    s += text(76, 406, "before it becomes one.", 58, WHITE, 700)
    s += text(80, 470, "Replay the disruption. Compare recovery paths.", 22, MUTED)
    s += text(80, 505, "Keep every number tied to Db2 evidence.", 22, MUTED)
    s += rounded(78, 570, 286, 62, fill=CYAN, stroke=CYAN, radius=31)
    s += text(221, 609, "RUN COUNTERFACTUAL", 15, BG, 700, "middle", 1.2)
    s += text(80, 710, "SUPPLIER S-104  /  14 DAYS", 14, AMBER, 700, spacing=1.4)
    s += '<path d="M 778 220 C 930 120 1310 150 1450 290" fill="none" stroke="{0}" stroke-width="2" opacity="0.4"/>'.format(CYAN)
    s += '<path d="M 690 370 C 880 280 1220 360 1438 505" fill="none" stroke="{0}" stroke-width="2" opacity="0.25"/>'.format(AMBER)
    s += node(850, 250, "SUPPLIER", "S-104  /  unavailable", AMBER, 220)
    s += node(1050, 350, "COMPONENT", "MCU-42  /  shortage", CORAL, 220)
    s += node(1240, 465, "PRODUCTION", "7 orders  /  exposed", AMBER, 220)
    s += node(1375, 610, "CUSTOMER", "3 SLAs  /  at risk", CORAL, 220)
    s += '<path d="M 945 286 L 960 316" stroke="url(#riskFlow)" stroke-width="4" marker-end="url(#arrowAmber)"/>'
    s += '<path d="M 1142 390 L 1156 424" stroke="url(#riskFlow)" stroke-width="4" marker-end="url(#arrowAmber)"/>'
    s += '<path d="M 1330 510 L 1340 566" stroke="url(#riskFlow)" stroke-width="4" marker-end="url(#arrowAmber)"/>'
    s += rounded(1000, 690, 390, 92, fill="#102B39", stroke=CYAN)
    s += text(1025, 720, "RECOMMENDED PATH", 11, MUTED, 700, spacing=1.5)
    s += text(1025, 757, "71% revenue risk protected", 24, LIME, 700)
    return s + end()


def dashboard() -> str:
    s = start(1600, 1000, "Operations war room", "ONE SCENARIO  /  FIVE FUTURES  /  ZERO UNVERIFIED NUMBERS")
    s += rounded(58, 150, 1484, 790, fill="#081923", stroke=GRID, radius=22, opacity=0.98)
    s += rounded(58, 150, 1484, 58, fill="#0D2735", stroke=GRID, radius=22)
    s += text(90, 187, "CHRONOS", 17, WHITE, 700, spacing=2)
    s += text(205, 187, "DB", 17, CYAN, 700, spacing=2)
    s += pill(1210, 166, "SCENARIO  /  SR-0118", CYAN, 238)
    s += text(90, 256, "SYSTEM HEALTH", 12, MUTED, 700, spacing=1.5)
    s += text(90, 291, "AT RISK", 29, CORAL, 700)
    s += dot(236, 281, CORAL, 6, True)
    s += metric(320, 238, "Revenue at risk", "₹18.4L", CORAL)
    s += metric(548, 238, "SLA breaches", "03", AMBER)
    s += metric(776, 238, "Best protection", "71%", LIME)
    s += metric(1004, 238, "Decision confidence", "0.86", CYAN)
    s += rounded(90, 370, 790, 500, fill="url(#glass)", stroke=GRID)
    s += text(120, 410, "DEPENDENCY CASCADE", 13, MUTED, 700, spacing=1.5)
    s += text(120, 446, "The disruption has a shape.", 23, WHITE, 700)
    s += node(245, 560, "S-104", "supplier outage", AMBER, 170)
    s += node(430, 560, "MCU-42", "component", CORAL, 170)
    s += node(615, 560, "PO-882", "production order", AMBER, 170)
    s += node(800, 560, "CO-711", "customer order", CORAL, 170)
    s += '<path d="M 330 560 H 345 M 515 560 H 530 M 700 560 H 715" stroke="url(#riskFlow)" stroke-width="4" marker-end="url(#arrowAmber)"/>'
    s += text(142, 690, "AFFECTED NODES", 11, MUTED, 700, spacing=1.4)
    s += text(142, 730, "4", 34, CORAL, 700)
    s += text(260, 730, "PROJECTED DELAY", 11, MUTED, 700, spacing=1.4)
    s += text(260, 770, "11.6 days", 26, AMBER, 700)
    s += text(480, 730, "EVIDENCE", 11, MUTED, 700, spacing=1.4)
    s += text(480, 770, "47 Db2 rows", 26, CYAN, 700)
    s += rounded(910, 370, 570, 500, fill="url(#glass)", stroke=GRID)
    s += text(940, 410, "RECOVERY OPTIONS", 13, MUTED, 700, spacing=1.5)
    s += text(940, 446, "Choose the safest future.", 23, WHITE, 700)
    options = [("Do nothing", "3 SLA", CORAL, 25), ("Transfer stock", "1 SLA", LIME, 71),
               ("Alternate supplier", "2 SLA", CYAN, 54), ("Expedite shipment", "2 SLA", AMBER, 46)]
    for i, (label, result, color, bar) in enumerate(options):
        y = 505 + i * 76
        s += text(940, y, label, 16, WHITE, 600)
        s += text(1400, y, result, 14, color, 700, "end")
        s += rounded(940, y + 18, 440, 10, fill=GRID, stroke=GRID, radius=5)
        s += rounded(940, y + 18, bar * 4, 10, fill=color, stroke=color, radius=5)
    s += pill(940, 815, "WHY THIS PLAN?", LIME, 150)
    return s + end()


def cascade() -> str:
    s = start(1600, 900, "Cascade anatomy", "A SINGLE OUTAGE  /  FOUR DEPENDENCY EDGES  /  ONE EXPLAINABLE IMPACT")
    s += text(78, 188, "Trace the failure like a signal moving through a circuit.", 25, WHITE, 600)
    stages = [
        (190, "01", "SUPPLIER", "S-104 unavailable", AMBER),
        (495, "02", "COMPONENT", "MCU-42 shortage", CORAL),
        (800, "03", "PRODUCTION", "PO-876 / PO-882", AMBER),
        (1105, "04", "CUSTOMER", "CO-701 / CO-711", CORAL),
        (1410, "05", "VALUE", "₹18.4L at risk", LIME),
    ]
    for x, number, label, sub, color in stages:
        s += rounded(x - 104, 350, 208, 198, fill="url(#glass)", stroke=color, radius=24)
        s += text(x - 76, 390, number, 13, color, 700, spacing=2)
        s += text(x - 76, 444, label, 18, WHITE, 700)
        s += text(x - 76, 482, sub, 13, MUTED)
        s += dot(x + 60, 510, color, 6, color == CYAN)
    for x in (294, 599, 904, 1209):
        s += f'<path d="M {x} 449 H {x + 92}" stroke="url(#riskFlow)" stroke-width="5" marker-end="url(#arrowAmber)"/>'
    s += rounded(200, 665, 1200, 106, fill="#102B39", stroke=GRID)
    s += pill(230, 702, "CALCULATION TRACE", CYAN, 174)
    s += text(450, 728, "inventory projection", 15, WHITE, 600)
    s += text(670, 728, "→", 22, CYAN, 700)
    s += text(715, 728, "BOM traversal", 15, WHITE, 600)
    s += text(900, 728, "→", 22, CYAN, 700)
    s += text(945, 728, "SLA rule v3", 15, WHITE, 600)
    s += text(1112, 728, "→", 22, CYAN, 700)
    s += text(1158, 728, "47 source rows", 15, LIME, 700)
    return s + end()


def architecture() -> str:
    s = start(1600, 1000, "Controlled intelligence", "AI INTERPRETS  /  DETERMINISTIC SERVICES CALCULATE  /  DB2 PROVES")
    s += text(78, 180, "Authority is designed into the topology.", 28, WHITE, 700)
    lanes = [
        (190, "USER", "Natural-language intent", CYAN),
        (450, "CONTROL PLANE", "Typed scenario + evidence", AMBER),
        (790, "DECISION ENGINE", "Business truth", LIME),
        (1130, "IBM Db2", "Operational memory", CYAN),
    ]
    for x, label, sub, color in lanes:
        s += rounded(x, 300, 280, 470, fill="url(#glass)", stroke=color, radius=24)
        s += text(x + 26, 345, label, 13, color, 700, spacing=1.5)
        s += text(x + 26, 380, sub, 16, WHITE, 700)
    s += pill(222, 438, "PROMPT", CYAN, 106)
    s += text(222, 500, "“Supplier S-104", 16, WHITE, 600)
    s += text(222, 528, "down for 14 days”", 16, WHITE, 600)
    s += pill(482, 438, "VALIDATE", AMBER, 118)
    for i, label in enumerate(["Schema", "Entity", "Constraint"]):
        s += rounded(482, 505 + i * 58, 220, 40, fill="#122C39", stroke=GRID, radius=10)
        s += dot(505, 525 + i * 58, AMBER, 4)
        s += text(523, 531 + i * 58, label, 14, WHITE, 600)
    s += pill(822, 438, "NO LLM CALCULATIONS", LIME, 202)
    for i, label in enumerate(["Impact engine", "Simulator", "Optimizer", "Claim verifier"]):
        s += rounded(822, 505 + i * 52, 220, 36, fill="#122C39", stroke=GRID, radius=10)
        s += text(842, 529 + i * 52, label, 14, WHITE, 600)
    s += pill(1162, 438, "EVIDENCE", CYAN, 120)
    for i, label in enumerate(["Facts", "History", "Vectors", "Audit"]):
        s += rounded(1162, 505 + i * 52, 220, 36, fill="#122C39", stroke=GRID, radius=10)
        s += text(1182, 529 + i * 52, label, 14, WHITE, 600)
    for x in (470, 730, 1070):
        s += f'<path d="M {x} 535 H {x + 70}" stroke="{CYAN}" stroke-width="4" marker-end="url(#arrowCyan)"/>'
    s += rounded(240, 830, 1120, 74, fill="#0C2531", stroke=GRID)
    s += text(280, 875, "The model can narrate the result.", 18, MUTED, 600)
    s += text(850, 875, "It cannot become the source of truth.", 18, LIME, 700, "end")
    return s + end()


def replay() -> str:
    s = start(1600, 900, "Decision replay", "TIME IS A FIRST-CLASS INPUT  /  MOVE BACKWARD  /  SEE WHAT WAS KNOWABLE")
    s += text(78, 184, "Every recommendation has a before, a turning point, and an after.", 25, WHITE, 600)
    s += rounded(120, 300, 1360, 220, fill="url(#glass)", stroke=GRID, radius=24)
    s += '<path d="M 190 410 H 1400" stroke="{0}" stroke-width="4" opacity="0.42"/>'.format(GRID)
    points = [(250, "08:00", "BASELINE", "healthy", CYAN), (570, "10:00", "DETECTED", "S-104 outage", AMBER),
              (890, "12:00", "PROJECTED", "cascade visible", CORAL), (1210, "14:00", "DECIDED", "transfer stock", LIME)]
    for x, time, label, sub, color in points:
        s += dot(x, 410, color, 10, color == CYAN)
        s += text(x, 350, time, 16, color, 700, "middle")
        s += text(x, 470, label, 13, WHITE, 700, "middle", 1.1)
        s += text(x, 496, sub, 12, MUTED, 400, "middle")
    s += rounded(120, 610, 620, 160, fill="#102B39", stroke=CYAN)
    s += pill(150, 638, "AT 10:00", CYAN, 108)
    s += text(150, 708, "The system knew the supplier was down.", 17, WHITE, 600)
    s += text(150, 736, "It did not yet know the full cascade.", 17, MUTED, 400)
    s += rounded(820, 610, 660, 160, fill="#102B39", stroke=LIME)
    s += pill(850, 638, "AT 14:00", LIME, 108)
    s += text(850, 708, "The evidence-backed intervention is selected.", 17, WHITE, 600)
    s += text(850, 736, "The baseline remains untouched.", 17, MUTED, 400)
    return s + end()


def evidence() -> str:
    s = start(1600, 900, "Evidence contract", "NO FLOATING NUMBERS  /  NO MYSTERY SOURCES  /  NO UNVERIFIED CLAIMS")
    s += text(78, 186, "A metric is only useful when you can walk backwards from it.", 26, WHITE, 600)
    chain = [("CLAIM", "₹18.4L revenue at risk", CORAL), ("RUN", "SR-2026-0118", CYAN),
             ("RULE", "revenue_at_risk_v3", AMBER), ("ROWS", "47 Db2 records", LIME), ("AUDIT", "verified  /  14:02", CYAN)]
    for i, (label, value, color) in enumerate(chain):
        x = 92 + i * 300
        s += rounded(x, 350, 248, 160, fill="url(#glass)", stroke=color, radius=22)
        s += text(x + 24, 388, label, 12, color, 700, spacing=1.6)
        s += text(x + 24, 448, value, 17, WHITE, 700)
        if i < len(chain) - 1:
            s += f'<path d="M {x + 248} 430 H {x + 286}" stroke="{CYAN}" stroke-width="3" marker-end="url(#arrowCyan)"/>'
    s += rounded(250, 640, 1100, 100, fill="#102B39", stroke=GRID)
    s += text(286, 681, "SOURCE CLASS", 11, MUTED, 700, spacing=1.4)
    s += pill(286, 700, "DATABASE FACT", CYAN, 145)
    s += pill(470, 700, "DERIVED VALUE", AMBER, 150)
    s += pill(660, 700, "RETRIEVED DOC", LIME, 160)
    s += pill(860, 700, "MODEL NARRATIVE", CORAL, 178)
    s += text(1180, 720, "TRACEABLE", 14, WHITE, 700, "end", 1.4)
    return s + end()


def db2_backbone() -> str:
    s = start(1600, 900, "Db2 as backbone", "ONE DATABASE  /  FIVE ROLES  /  A DECISION THAT SURVIVES RESTART")
    s += text(78, 180, "ChronosDB gives Db2 the whole memory of the decision.", 26, WHITE, 600)
    cx, cy = 800, 510
    rings = [(270, GRID, "AUDIT"), (215, CYAN, "EVIDENCE"), (160, AMBER, "SCENARIO"), (105, LIME, "STATE")]
    for radius, color, label in rings:
        s += f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-width="2" opacity="0.75"/>'
        s += dot(cx + radius, cy, color, 5)
        s += text(cx + radius + 18, cy + 5, label, 13, color, 700, spacing=1.3)
    s += '<ellipse cx="800" cy="510" rx="74" ry="42" fill="#194456" stroke="{0}" stroke-width="4"/>'.format(CYAN)
    s += text(800, 516, "IBM Db2", 20, WHITE, 700, "middle")
    satellites = [(400, 330, "OPERATIONAL\nRECORDS", CYAN), (1190, 330, "HISTORICAL\nSTATE", AMBER),
                  (360, 700, "VECTOR\nEVIDENCE", LIME), (1240, 700, "DECISION\nAUDIT", CORAL)]
    for x, y, label, color in satellites:
        s += rounded(x - 120, y - 42, 240, 84, fill="url(#glass)", stroke=color)
        for j, line in enumerate(label.split("\n")):
            s += text(x, y - 4 + j * 22, line, 14, WHITE if j == 0 else MUTED, 700 if j == 0 else 600, "middle")
        s += f'<path d="M {cx + (x - cx) * 0.48} {cy + (y - cy) * 0.48} L {x - (x - cx) * 0.16} {y - (y - cy) * 0.16}" stroke="{color}" stroke-width="2" opacity="0.5"/>'
    return s + end()


def interventions() -> str:
    s = start(1600, 900, "Counterfactual board", "SAME BASELINE  /  FIVE FUTURES  /  ONE FEASIBLE RECOMMENDATION")
    s += text(78, 182, "Do nothing is also a scenario. Make the trade-off visible.", 26, WHITE, 600)
    cards = [("DO NOTHING", "₹18.4L", "3 SLA", CORAL, 22, "baseline"),
             ("TRANSFER STOCK", "₹5.2L", "1 SLA", LIME, 72, "recommended"),
             ("ALT SUPPLIER", "₹8.7L", "2 SLA", CYAN, 58, "feasible"),
             ("EXPEDITE", "₹11.1L", "2 SLA", AMBER, 45, "feasible")]
    for i, (label, value, sla, color, protection, status) in enumerate(cards):
        x = 78 + i * 365
        s += rounded(x, 310, 325, 385, fill="url(#glass)", stroke=color if status == "recommended" else GRID, radius=22)
        if status == "recommended":
            s += pill(x + 22, 332, "SELECTED", LIME, 104)
        else:
            s += text(x + 22, 355, status.upper(), 11, MUTED, 700, spacing=1.4)
        s += text(x + 22, 412, label, 17, WHITE, 700)
        s += text(x + 22, 478, "REVENUE AT RISK", 11, MUTED, 700, spacing=1.2)
        s += text(x + 22, 520, value, 30, color, 700)
        s += text(x + 22, 570, "PROTECTED", 11, MUTED, 700, spacing=1.2)
        s += rounded(x + 22, 595, 275, 12, fill=GRID, stroke=GRID, radius=6)
        s += rounded(x + 22, 595, protection * 2.75, 12, fill=color, stroke=color, radius=6)
        s += text(x + 22, 656, sla, 15, color, 700)
    s += text(78, 785, "Rank by service, cost, delay, and risk — never by an opaque model score.", 18, MUTED, 600)
    return s + end()


def supply_chain() -> str:
    s = start(1600, 900, "Supply-chain signal map", "THE NETWORK IS THE PRODUCT  /  THE OUTAGE IS THE SIGNAL")
    s += text(78, 182, "One disruption. Many connected consequences.", 26, WHITE, 600)
    paths = [
        ("M 230 400 C 420 250 560 280 700 400 C 840 520 960 520 1110 390 C 1230 290 1350 330 1430 420", CYAN),
        ("M 230 400 C 400 500 540 560 700 400 C 860 240 1020 260 1110 390 C 1240 530 1330 560 1430 420", AMBER),
        ("M 230 400 C 420 390 560 390 700 400 C 860 410 970 390 1110 390 C 1240 390 1340 400 1430 420", CORAL),
    ]
    for path, color in paths:
        s += f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3" opacity="0.42" stroke-dasharray="8 12"/>'
    nodes = [(230, 400, "SUPPLIERS", "S-104  /  outage", AMBER), (700, 400, "COMPONENTS", "MCU-42", CORAL),
             (1110, 390, "FACILITIES", "Pune + Chennai", CYAN), (1430, 420, "CUSTOMERS", "SLA network", LIME)]
    for x, y, label, sub, color in nodes:
        s += dot(x, y, color, 14, color == CYAN)
        s += rounded(x - 110, y + 42, 220, 76, fill="#102B39", stroke=color, radius=18)
        s += text(x, y + 73, label, 13, color, 700, "middle", 1.1)
        s += text(x, y + 98, sub, 12, MUTED, 400, "middle")
    s += pill(635, 690, "IMPACT PROPAGATES", CORAL, 190)
    s += text(865, 712, "until an intervention changes the path", 17, WHITE, 600)
    return s + end()


def trust_boundary() -> str:
    s = start(1600, 900, "Trust boundary", "THE MODEL CAN SPEAK  /  ONLY RULES CAN CALCULATE  /  ONLY Db2 CAN PROVE")
    s += text(78, 180, "ChronosDB keeps the dangerous permissions outside the prompt.", 26, WHITE, 600)
    s += rounded(100, 300, 420, 400, fill="#102B39", stroke=CORAL, radius=26)
    s += pill(134, 334, "MODEL ZONE", CORAL, 126)
    s += text(134, 410, "May interpret", 22, WHITE, 700)
    s += text(134, 450, "May retrieve", 22, WHITE, 700)
    s += text(134, 490, "May explain", 22, WHITE, 700)
    s += text(134, 574, "May not calculate", 20, CORAL, 700)
    s += text(134, 612, "May not write", 20, CORAL, 700)
    s += '<path d="M 520 500 H 1080" stroke="{0}" stroke-width="2" stroke-dasharray="8 10"/>'.format(AMBER)
    s += text(800, 464, "VALIDATION BOUNDARY", 12, AMBER, 700, "middle", 1.6)
    s += rounded(1080, 300, 420, 400, fill="#102B39", stroke=LIME, radius=26)
    s += pill(1114, 334, "TRUTH ZONE", LIME, 126)
    s += text(1114, 410, "Typed scenario", 22, WHITE, 700)
    s += text(1114, 450, "Deterministic rules", 22, WHITE, 700)
    s += text(1114, 490, "Db2 evidence", 22, WHITE, 700)
    s += text(1114, 574, "Numbers verified", 20, LIME, 700)
    s += text(1114, 612, "Audit preserved", 20, LIME, 700)
    s += rounded(420, 780, 760, 58, fill="#0C2531", stroke=GRID)
    s += text(800, 817, "If the LLM disappears, the evidence-backed summary remains.", 17, WHITE, 600, "middle")
    return s + end()


def decision_flow() -> str:
    s = start(1600, 900, "Decision loop", "FROM QUESTION TO VERIFIED ACTION  /  A CLOSED LOOP, NOT A CHAT TRANSCRIPT")
    labels = [("ASK", "Describe the disruption", CYAN), ("FRAME", "Validate the scenario", AMBER),
              ("SIMULATE", "Project the cascade", CORAL), ("COMPARE", "Score interventions", LIME),
              ("PROVE", "Open the evidence", CYAN)]
    for i, (label, sub, color) in enumerate(labels):
        x = 160 + i * 315
        s += dot(x, 420, color, 17, color == CYAN)
        s += text(x, 350, f"0{i + 1}", 12, color, 700, "middle", 1.4)
        s += text(x, 474, label, 19, WHITE, 700, "middle", 1)
        s += text(x, 505, sub, 13, MUTED, 400, "middle")
        if i < len(labels) - 1:
            s += f'<path d="M {x + 28} 420 H {x + 282}" stroke="{CYAN}" stroke-width="3" marker-end="url(#arrowCyan)" opacity="0.7"/>'
    s += rounded(345, 650, 910, 94, fill="#102B39", stroke=GRID)
    s += text(800, 692, "REPLAYABLE DECISION RECORD", 13, CYAN, 700, "middle", 1.7)
    s += text(800, 724, "scenario  /  baseline  /  candidates  /  winner  /  evidence  /  audit", 16, WHITE, 600, "middle")
    return s + end()


def signal_grid() -> str:
    s = start(1600, 900, "Signal grid", "CHRONOSDB VISUAL LANGUAGE  /  TIME, FLOW, EVIDENCE")
    s += text(78, 180, "A visual system for decisions under pressure.", 26, WHITE, 600)
    for i in range(6):
        x = 130 + i * 250
        s += f'<path d="M {x} 300 V 760" stroke="{GRID}" stroke-width="1"/>'
    for i in range(4):
        y = 300 + i * 115
        s += f'<path d="M 130 {y} H 1430" stroke="{GRID}" stroke-width="1"/>'
    for i, (x, y, color) in enumerate([(220, 620, CYAN), (440, 500, AMBER), (690, 620, CORAL),
                                        (890, 410, LIME), (1120, 525, CYAN), (1350, 355, AMBER)]):
        s += dot(x, y, color, 11, color == CYAN)
        if i:
            px, py, _ = [(220, 620, CYAN), (440, 500, AMBER), (690, 620, CORAL),
                         (890, 410, LIME), (1120, 525, CYAN), (1350, 355, AMBER)][i - 1]
            s += f'<path d="M {px} {py} L {x} {y}" stroke="{color}" stroke-width="3" opacity="0.72"/>'
    s += rounded(180, 300, 390, 110, fill="#102B39", stroke=CYAN)
    s += text(210, 340, "TEMPORAL", 12, CYAN, 700, spacing=1.5)
    s += text(210, 380, "Replay the state", 22, WHITE, 700)
    s += rounded(610, 680, 390, 110, fill="#102B39", stroke=CORAL)
    s += text(640, 720, "COUNTERFACTUAL", 12, CORAL, 700, spacing=1.5)
    s += text(640, 760, "Compare the futures", 22, WHITE, 700)
    s += rounded(1060, 280, 390, 110, fill="#102B39", stroke=LIME)
    s += text(1090, 320, "EVIDENCE", 12, LIME, 700, spacing=1.5)
    s += text(1090, 360, "Prove the decision", 22, WHITE, 700)
    return s + end()


def social_card() -> str:
    s = start(1200, 630, "ChronosDB", "AUDITABLE COUNTERFACTUAL INTELLIGENCE")
    s += text(80, 220, "The Db2", 64, WHITE, 700)
    s += text(80, 294, "time machine", 64, CYAN, 700)
    s += text(80, 364, "for supply-chain decisions.", 36, WHITE, 600)
    s += text(84, 468, "RECONSTRUCT  /  SIMULATE  /  PROVE", 15, MUTED, 700, spacing=2.2)
    s += '<path d="M 760 140 C 920 70 1100 150 1080 300 C 1060 450 900 530 760 450 C 640 380 640 210 760 140 Z" fill="none" stroke="{0}" stroke-width="2" opacity="0.3"/>'.format(CYAN)
    s += '<path d="M 770 145 C 940 230 980 350 1080 445" fill="none" stroke="{0}" stroke-width="4" opacity="0.7"/>'.format(AMBER)
    s += '<path d="M 740 450 C 880 350 940 260 1080 180" fill="none" stroke="{0}" stroke-width="4" opacity="0.7"/>'.format(CYAN)
    s += node(760, 300, "Db2", "evidence", CYAN, 180)
    s += node(1030, 210, "FUTURE", "compare", AMBER, 180)
    s += node(1030, 440, "PROOF", "audit", LIME, 180)
    return s + end()


ASSETS = {
    "logo-mark": (logo_mark(), 1024),
    "logo-lockup": (lockup(), 2),
    "favicon": (logo_mark(128), 4),
    "hero-time-machine": (hero(), 2),
    "operations-war-room": (dashboard(), 2),
    "cascade-anatomy": (cascade(), 2),
    "controlled-intelligence": (architecture(), 2),
    "decision-replay": (replay(), 2),
    "evidence-contract": (evidence(), 2),
    "db2-backbone": (db2_backbone(), 2),
    "counterfactual-board": (interventions(), 2),
    "supply-chain-signal-map": (supply_chain(), 2),
    "trust-boundary": (trust_boundary(), 2),
    "decision-loop": (decision_flow(), 2),
    "signal-grid": (signal_grid(), 2),
    "social-card": (social_card(), 2),
}


def write_assets() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (_svg, _scale) in ASSETS.items():
        svg = _svg
        svg_path = OUT / f"{name}.svg"
        svg_path.write_text(svg, encoding="utf-8")
    print(f"Generated {len(ASSETS)} editable SVG sources in {OUT}")


if __name__ == "__main__":
    write_assets()
