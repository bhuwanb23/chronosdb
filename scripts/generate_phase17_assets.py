"""Phase 17 asset generator: SVG -> PNG (2x) for Db2 depth graphic and thumbnail."""
import cairosvg, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
BG, CARD, TEXT, MUTED, BLUE, GREEN, RED, AMBER, PURPLE = "#0B1220", "#1E293B", "#F8FAFC", "#94A3B8", "#3B82F6", "#10B981", "#EF4444", "#F59E0B", "#8B5CF6"

def card(x, y, w, h, title, sub, color):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CARD}" stroke="{color}" stroke-width="3"/>'
            f'<text x="{x+w/2}" y="{y+h/2-6}" text-anchor="middle" font-size="26" font-weight="700" fill="{TEXT}" font-family="DejaVu Sans, Arial">{title}</text>'
            f'<text x="{x+w/2}" y="{y+h/2+26}" text-anchor="middle" font-size="18" fill="{MUTED}" font-family="DejaVu Sans, Arial">{sub}</text>')

def db2_depth():
    parts = [card(60, 200, 340, 120, "Operational Records", "Suppliers • Orders • Inventory", BLUE),
             card(430, 200, 340, 120, "Temporal Replay", "As-of state reconstruction", AMBER),
             card(800, 200, 340, 120, "Vector Retrieval", "VECTOR • Recall@5 (pending verification)", PURPLE),
             card(60, 380, 340, 120, "Audit Ledger", "Decisions • Replays • Verifications", RED),
             card(430, 380, 340, 120, "Scenario Storage", "Golden Scenario SCN-GOLD-001", GREEN),
             card(800, 380, 340, 120, "Recommendations", "INT-GOLD-C • INT-GOLD-C recommended", GREEN)]
    body = "".join(parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620">
<rect width="1200" height="620" fill="{BG}"/>
<text x="600" y="70" text-anchor="middle" font-size="40" font-weight="700" fill="{TEXT}" font-family="DejaVu Sans, Arial">Why Db2?</text>
<text x="600" y="110" text-anchor="middle" font-size="22" fill="{MUTED}" font-family="DejaVu Sans, Arial">One engine: operational + temporal + vector + audit + scenario storage</text>
{body}
<rect x="300" y="530" width="600" height="60" rx="30" fill="{BLUE}"/>
<text x="600" y="568" text-anchor="middle" font-size="28" font-weight="700" fill="#FFFFFF" font-family="DejaVu Sans, Arial">IBM Db2 — the time machine</text>
</svg>'''

def thumbnail():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B1220"/><stop offset="1" stop-color="#1E3A8A"/></linearGradient></defs>
<rect width="1280" height="720" fill="url(#g)"/>
<circle cx="110" cy="110" r="44" fill="{BLUE}"/>
<text x="110" y="124" text-anchor="middle" font-size="44" font-weight="700" fill="#FFFFFF" font-family="DejaVu Sans, Arial">C</text>
<text x="640" y="300" text-anchor="middle" font-size="76" font-weight="800" fill="{TEXT}" font-family="DejaVu Sans, Arial">ChronosDB</text>
<text x="640" y="380" text-anchor="middle" font-size="36" fill="{TEXT}" font-family="DejaVu Sans, Arial">The Db2 Time Machine for Enterprise Decisions</text>
<rect x="140" y="440" width="1000" height="70" rx="35" fill="{GREEN}"/>
<text x="640" y="486" text-anchor="middle" font-size="30" font-weight="700" fill="#FFFFFF" font-family="DejaVu Sans, Arial">₹16,00,000 at risk → INT-GOLD-C (₹1,32,000) → ₹16,00,000 protected</text>
<text x="640" y="600" text-anchor="middle" font-size="24" fill="{MUTED}" font-family="DejaVu Sans, Arial">Disruption → Cascade → Futures → Recommendation → Evidence → Replay</text>
</svg>'''

out = ROOT / "assets/demo"
for name, svg, w in [("db2-depth-graphic.png", db2_depth(), 2400), ("thumbnails/thumbnail-16x9.png", thumbnail(), 2560)]:
    svg_path = out / name.replace(".png", ".svg")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / name), output_width=w)
    print("✅", name)
