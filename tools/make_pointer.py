"""Draw the webOS-style mouse pointers (media/pointer_*.png).

In the style of the LG Magic Remote cursor, drawn from scratch: a white
pointing hand with a crimson outline, a coral teardrop over clickable items.

    python3 tools/make_pointer.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

MEDIA = Path(__file__).resolve().parent.parent / "media"
S = 8  # supersampling
W, H = 58, 68
CRIMSON = (196, 22, 74, 255)
WHITE = (255, 255, 255, 255)
CORAL = (244, 92, 92, 255)


def hand_mask(pressed: bool = False) -> Image.Image:
    m = Image.new("L", (W * S, H * S), 0)
    d = ImageDraw.Draw(m)

    def rr(x0, y0, x1, y1, r):
        d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), radius=r * S, fill=255)

    top = 8 if pressed else 3
    rr(16, top, 25, 40, 4.5)          # index finger
    rr(24.5, 21, 32.5, 44, 4)         # folded fingers
    rr(32, 24, 40, 46, 4)
    rr(39.5, 28, 47, 48, 3.8)
    rr(14, 34, 47, 60, 9)             # palm
    d.polygon([(x * S, y * S) for x, y in ((16, 46), (6, 38), (3.5, 41), (10, 54), (17, 58))], fill=255)
    d.ellipse((2.5 * S, 36 * S, 9 * S, 43 * S), fill=255)  # thumb tip
    return m


def hand(pressed: bool = False) -> Image.Image:
    mask = hand_mask(pressed)
    outline = mask.filter(ImageFilter.MaxFilter(2 * int(2.0 * S) + 1))
    shadow = outline.filter(ImageFilter.GaussianBlur(1.6 * S))
    img = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    img.paste((0, 0, 0, 110), (int(1.2 * S), int(1.8 * S)), shadow)
    img.paste(CRIMSON, (0, 0), outline)
    fill = WHITE if not pressed else (236, 232, 236, 255)
    img.paste(fill, (0, 0), mask)
    # finger crease lines
    d = ImageDraw.Draw(img)
    for x in (24.5, 32, 39.5):
        d.line((x * S, 31 * S, x * S, 40 * S), fill=(205, 196, 205, 255), width=int(0.8 * S))
    return img.resize((W, H), Image.LANCZOS)


def drop() -> Image.Image:
    m = Image.new("L", (W * S, H * S), 0)
    d = ImageDraw.Draw(m)
    cx, cy, r = 30, 40, 23
    d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill=255)
    # a short taper to the tip at the top left (the hotspot)
    d.polygon([(9 * S, 5 * S), ((cx - r + 0.5) * S, (cy - 2) * S), ((cx + 2) * S, (cy - r + 0.5) * S)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2.2 * S)).point(lambda v: 255 if v > 110 else 0)
    shadow = m.filter(ImageFilter.GaussianBlur(1.8 * S))
    img = Image.new("RGBA", m.size, (0, 0, 0, 0))
    img.paste((0, 0, 0, 100), (int(1.2 * S), int(2 * S)), shadow)
    img.paste(CORAL, (0, 0), m)
    # glossy dot
    d = ImageDraw.Draw(img)
    gx, gy, gr = cx + 4, cy + 4, 7
    d.ellipse(((gx - gr) * S, (gy - gr) * S, (gx + gr) * S, (gy + gr) * S), fill=(255, 150, 150, 255))
    d.ellipse(((gx - 3.2) * S, (gy - 3.6) * S, (gx - 0.4) * S, (gy - 0.8) * S), fill=(255, 235, 235, 255))
    return img.resize((W, H), Image.LANCZOS)


# Same layout as service.webostv's cursor.py, so Pointer.xml has one geometry
# for these and for the TV's own pointer images: a 256x256 canvas with the
# hotspot (here the topmost solid row's middle) in its middle.
CANVAS = (256, 256)
HOTSPOT = (128, 128)


def laid_out(img: Image.Image) -> Image.Image:
    alpha = img.getchannel("A")
    for y in range(img.height):
        xs = [x for x in range(img.width) if alpha.getpixel((x, y)) >= 128]
        if xs:
            tip = ((xs[0] + xs[-1]) // 2, y)
            break
    out = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    out.alpha_composite(img, (HOTSPOT[0] - tip[0], HOTSPOT[1] - tip[1]))
    return out


if __name__ == "__main__":
    laid_out(hand()).save(MEDIA / "pointer_arrow.png")
    laid_out(drop()).save(MEDIA / "pointer_focus.png")
    laid_out(hand(pressed=True)).save(MEDIA / "pointer_click.png")
    print("wrote pointer_arrow.png, pointer_focus.png, pointer_click.png")
