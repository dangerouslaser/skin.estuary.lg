"""Draw the OSD's audio receiver button (media/osd/fullscreen/buttons/receiver.png):
a white AV receiver outline (display and volume knob) on transparent, sized
like the other OSD buttons (128x128, glyph about 24..104)."""

from pathlib import Path

from PIL import Image, ImageDraw

S = 4  # draw big, then scale down for smooth edges
OUT = Path(__file__).resolve().parent.parent / "media/osd/fullscreen/buttons/receiver.png"


def main() -> None:
    img = Image.new("LA", (128 * S, 128 * S), (255, 0))
    d = ImageDraw.Draw(img)
    w = 7 * S
    d.rounded_rectangle((24 * S, 38 * S, 104 * S, 86 * S), radius=8 * S, outline=(255, 255), width=w)
    d.rounded_rectangle((34 * S, 50 * S, 64 * S, 60 * S), radius=3 * S, fill=(255, 255))  # display
    d.rounded_rectangle((34 * S, 67 * S, 52 * S, 73 * S), radius=3 * S, fill=(255, 255))  # buttons
    d.ellipse((76 * S, 50 * S, 96 * S, 70 * S), outline=(255, 255), width=5 * S)          # volume knob
    d.rectangle((32 * S, 86 * S, 40 * S, 92 * S), fill=(255, 255))                        # feet
    d.rectangle((88 * S, 86 * S, 96 * S, 92 * S), fill=(255, 255))
    img.resize((128, 128), Image.LANCZOS).save(OUT, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
