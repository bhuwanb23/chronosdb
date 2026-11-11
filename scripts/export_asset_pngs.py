"""Render the generated SVG assets to PNG using headless Chrome on Windows."""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "chronosdb"
WIDTH_RE = re.compile(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"', re.IGNORECASE)


def browser_path() -> str:
    candidates = (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise RuntimeError("Chrome or Edge is required to export PNG assets.")


def export() -> None:
    browser = browser_path()
    svg_paths = sorted(ASSET_DIR.glob("*.svg"))
    if not svg_paths:
        raise RuntimeError("No SVG assets found. Run generate_assets.py first.")

    with tempfile.TemporaryDirectory(prefix="chronosdb-render-") as profile_root:
        for svg_path in svg_paths:
            svg = svg_path.read_text(encoding="utf-8")
            match = WIDTH_RE.search(svg)
            if not match:
                raise RuntimeError(f"Could not determine dimensions for {svg_path.name}")
            width, height = match.groups()
            output = svg_path.with_suffix(".png")
            uri = svg_path.resolve().as_uri()
            profile = Path(profile_root) / svg_path.stem
            profile.mkdir()
            command = [
                browser,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                f"--user-data-dir={profile}",
                f"--window-size={width},{height}",
                f"--screenshot={output}",
                uri,
            ]
            subprocess.run(command, check=True, timeout=45)
            if not output.exists() or output.stat().st_size == 0:
                raise RuntimeError(f"Chrome did not create {output.name}")
            print(f"{output.name}: {width}x{height}")


if __name__ == "__main__":
    export()
