"""Draw the audio receiver icons: a white AV receiver outline (display and
volume knob) on transparent.

    media/osd/fullscreen/buttons/receiver.png   OSD button, 128x128 like the others
    media/icons/settings/receiver.png           Settings tile and the Denon page, 256x256 like lgtv.png
"""

from pathlib import Path

from PIL import Image, ImageDraw

S = 4  # draw big, then scale down for smooth edges
MEDIA = Path(__file__).resolve().parent.parent / "media"


def draw(size: int, scale: float, out: Path) -> None:
    """The glyph is designed on a 128 grid centred on (64, 65); `scale` sizes it."""
    c = size / 2

    def x(v: float) -> float:
        return (c + (v - 64) * scale) * S

    def y(v: float) -> float:
        return (c + (v - 65) * scale) * S

    def box(x0, y0, x1, y1):
        return (x(x0), y(y0), x(x1), y(y1))

    img = Image.new("LA", (size * S, size * S), (255, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box(24, 38, 104, 86), radius=8 * scale * S, outline=(255, 255), width=round(7 * scale * S))
    d.rounded_rectangle(box(34, 50, 64, 60), radius=3 * scale * S, fill=(255, 255))  # display
    d.rounded_rectangle(box(34, 67, 52, 73), radius=3 * scale * S, fill=(255, 255))  # buttons
    d.ellipse(box(76, 50, 96, 70), outline=(255, 255), width=round(5 * scale * S))    # volume knob
    d.rectangle(box(32, 86, 40, 92), fill=(255, 255))                                 # feet
    d.rectangle(box(88, 86, 96, 92), fill=(255, 255))
    img.resize((size, size), Image.LANCZOS).save(out, optimize=True)
    print(out)


def main() -> None:
    draw(128, 1.0, MEDIA / "osd/fullscreen/buttons/receiver.png")
    draw(256, 1.85, MEDIA / "icons/settings/receiver.png")


if __name__ == "__main__":
    main()
