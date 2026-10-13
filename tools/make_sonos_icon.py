"""Render the Sonos icons from the wordmark (tools/sonos-logo.svg, white). Needs
rsvg-convert.

    media/icons/settings/sonos.png             Settings tile and the Sonos page, 256x256 like
                                               the others: the wordmark centred across it
    media/osd/fullscreen/buttons/sonos.png     the OSD's Sonos button, 128x128 like the others:
                                               Sonos's round logo inverted, a white disc with the
                                               wordmark cut out (white on transparent, so it
                                               takes the OSD's focus colour like the other buttons)

    python3 tools/make_sonos_icon.py
"""

import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "tools" / "sonos-logo.svg"
OUT = ROOT / "media" / "icons" / "settings" / "sonos.png"
OSD = ROOT / "media" / "osd" / "fullscreen" / "buttons" / "sonos.png"
SIZE, WIDTH = 256, 208  # canvas, and the wordmark's width on it
OSD_SIZE, DISC, OSD_WIDTH = 128, 80, 60  # canvas, the disc's diameter, the wordmark's width (as Sonos's logo)
S = 4  # draw big, then scale down for smooth edges


def wordmark(width: int) -> Image.Image:
    """The white wordmark, trimmed, `width` pixels wide."""
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "logo.png"
        subprocess.run(["rsvg-convert", "-w", str(width * 4), "-o", str(raw), str(SVG)], check=True)
        logo = Image.open(raw).convert("RGBA")
    logo = logo.crop(logo.getbbox())  # the SVG's viewBox has margins
    return logo.resize((width, round(logo.height * width / logo.width)), Image.LANCZOS)


def settings_icon() -> None:
    logo = wordmark(WIDTH)
    canvas = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    canvas.alpha_composite(logo, ((SIZE - logo.width) // 2, (SIZE - logo.height) // 2))
    canvas.save(OUT, optimize=True)
    print(OUT)


def osd_icon() -> None:
    big = OSD_SIZE * S
    disc = Image.new("L", (big, big), 0)
    edge = (big - DISC * S) // 2
    ImageDraw.Draw(disc).ellipse((edge, edge, big - edge, big - edge), fill=255)
    text = wordmark(OSD_WIDTH * S).getchannel("A")
    cut = Image.new("L", (big, big), 0)
    cut.paste(text, ((big - text.width) // 2, (big - text.height) // 2))
    alpha = ImageChops.subtract(disc, cut)  # the wordmark knocked out of the disc
    icon = Image.merge("RGBA", (*(Image.new("L", (big, big), 255),) * 3, alpha))
    icon.resize((OSD_SIZE, OSD_SIZE), Image.LANCZOS).save(OSD, optimize=True)
    print(OSD)


def main() -> None:
    settings_icon()
    osd_icon()


if __name__ == "__main__":
    main()
