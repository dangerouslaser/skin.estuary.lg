"""Draw the soundbar icon (the OSD's Sonos button): a white soundbar outline
with a speaker grille, on transparent, in the style of tools/make_receiver_icon.py.
(The Settings tile and the Sonos page use the Sonos wordmark: make_sonos_icon.py.)

    media/osd/fullscreen/buttons/soundbar.png   OSD button, 128x128 like the others
"""

from pathlib import Path

from PIL import Image, ImageDraw

S = 4  # draw big, then scale down for smooth edges
MEDIA = Path(__file__).resolve().parent.parent / "media"


def draw(size: int, scale: float, out: Path) -> None:
    """The glyph is designed on a 128 grid centred on (64, 64); `scale` sizes it."""
    c = size / 2

    def x(v: float) -> float:
        return (c + (v - 64) * scale) * S

    def y(v: float) -> float:
        return (c + (v - 64) * scale) * S

    img = Image.new("LA", (size * S, size * S), (255, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x(10), y(48), x(118), y(80)), radius=16 * scale * S,
                        outline=(255, 255), width=round(7 * scale * S))
    for row, offset in ((58, 0.0), (70, 5.0)):  # the grille: two staggered rows of dots
        cx = 26 + offset
        while cx <= 102:
            r = 2.6
            d.ellipse((x(cx - r), y(row - r), x(cx + r), y(row + r)), fill=(255, 255))
            cx += 10
    img.resize((size, size), Image.LANCZOS).save(out, optimize=True)
    print(out)


def main() -> None:
    draw(128, 1.0, MEDIA / "osd/fullscreen/buttons/soundbar.png")


if __name__ == "__main__":
    main()
