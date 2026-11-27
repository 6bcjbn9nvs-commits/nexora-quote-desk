#!/usr/bin/env python3
"""Generate the Open Graph image for the B2B subscription survey page.

Run from the repository root:  python3 tools/make_og_b2b.py
Output: b2b/og-image-b2b.png (1200x630)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
FONT_DIR = "/workspace/.local/share/fonts"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "b2b", "og-image-b2b.png")

NAVY_DARK = (11, 30, 48)
NAVY = (14, 42, 71)
NAVY_LIGHT = (23, 63, 99)
TEAL = (13, 127, 117)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def gradient(size, top, bottom):
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((w, h), Image.BILINEAR)


def main():
    img = gradient((W, H), NAVY_LIGHT, NAVY_DARK).convert("RGBA")

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 560, -280, W + 240, 330], fill=(13, 127, 117, 78))
    gd.ellipse([-280, H - 320, 400, H + 240], fill=(30, 86, 132, 92))
    glow = glow.filter(ImageFilter.GaussianBlur(92))
    img = Image.alpha_composite(img, glow)

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdr = ImageDraw.Draw(grid)
    for x in range(0, W, 48):
        gdr.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, 48):
        gdr.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)
    img = Image.alpha_composite(img, grid)

    d = ImageDraw.Draw(img)

    mx, my, ms = 80, 66, 58
    d.rounded_rectangle([mx, my, mx + ms, my + ms], radius=17,
                        fill=(27, 74, 115, 255), outline=(255, 255, 255, 40), width=1)
    d.text((mx + ms / 2, my + ms / 2 - 2), "N", font=font("Pretendard-Black.otf", 33), fill=WHITE, anchor="mm")

    d.text((mx + ms + 16, my + 6), "Nexora Labs", font=font("Pretendard-ExtraBold.otf", 28), fill=WHITE)
    d.text((mx + ms + 18, my + 42), "B2B AUTOMATION", font=font("Pretendard-Bold.otf", 15), fill=(150, 205, 198))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    chip = "사전 수요 조사 · 결제 없음"
    f_chip = font("Pretendard-Bold.otf", 19)
    tw = d.textlength(chip, font=f_chip)
    od.rounded_rectangle([80, 186, 80 + tw + 34, 232], radius=23,
                         fill=(255, 255, 255, 16), outline=(120, 220, 205, 120), width=1)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    d.text((97, 199), chip, font=f_chip, fill=(150, 228, 216))

    lines = [("매달 반복되는 업무,", font("Pretendard-Black.otf", 62)),
             ("월 29.9만 원에 맡기세요", font("Pretendard-Black.otf", 62))]
    y = 258
    for text, f in lines:
        d.text((80, y), text, font=f, fill=WHITE)
        y += 76

    d.text((82, y + 8), "표준 템플릿 · 자동 계산 도구 · 월 1회 점검", font=font("Pretendard-SemiBold.otf", 25), fill=(196, 214, 232))
    d.text((82, y + 50), "3개월 단위 · 비구속 의향서 · 지금 결제 0원", font=font("Pretendard-Medium.otf", 21), fill=(170, 192, 212))

    labels = ["월 299,000원 (VAT 포함)", "3개월 단위", "비구속"]
    f_pill = font("Pretendard-Bold.otf", 19)
    px = 80
    boxes = []
    for label in labels:
        tw = d.textlength(label, font=f_pill)
        boxes.append((px, tw, label))
        px += tw + 54
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for bx, tw, _ in boxes:
        od.rounded_rectangle([bx, H - 92, bx + tw + 38, H - 48], radius=22,
                             fill=(255, 255, 255, 16), outline=(255, 255, 255, 60), width=1)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    for bx, tw, label in boxes:
        d.text((bx + 19, H - 83), label, font=f_pill, fill=(232, 241, 248))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
