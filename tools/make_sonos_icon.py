"""Render the Sonos wordmark (tools/sonos-logo.svg, white) as the Settings tile
and Sonos page icon: media/icons/settings/sonos.png, 256x256 like the others,
the wordmark centred across it. Needs rsvg-convert.

    python3 tools/make_sonos_icon.py
"""

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "tools" / "sonos-logo.svg"
OUT = ROOT / "media" / "icons" / "settings" / "sonos.png"
SIZE, WIDTH = 256, 208  # canvas, and the wordmark's width on it


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "logo.png"
        subprocess.run(["rsvg-convert", "-w", str(WIDTH * 4), "-o", str(raw), str(SVG)], check=True)
        logo = Image.open(raw).convert("RGBA")
    logo = logo.crop(logo.getbbox())  # the SVG's viewBox has margins
    logo = logo.resize((WIDTH, round(logo.height * WIDTH / logo.width)), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    canvas.alpha_composite(logo, ((SIZE - logo.width) // 2, (SIZE - logo.height) // 2))
    canvas.save(OUT, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
