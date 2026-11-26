#!/usr/bin/env python3
"""Generate Open Graph share images (1200x630) for Nexora Quote Desk.

Run from the repository root:  python3 tools/make_og_image.py
Outputs og-image-ko.png and og-image-en.png next to this script's parent.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
FONT_DIR = "/workspace/.local/share/fonts"
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAVY_DARK = (11, 32, 54)
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


def build(lang):
    img = gradient((W, H), NAVY_LIGHT, NAVY_DARK).convert("RGBA")

    # soft teal glow top-right + grid, drawn on a separate layer
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 520, -260, W + 260, 320], fill=(13, 127, 117, 70))
    gd.ellipse([-260, H - 300, 380, H + 240], fill=(30, 86, 132, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img = Image.alpha_composite(img, glow)

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdr = ImageDraw.Draw(grid)
    for x in range(0, W, 48):
        gdr.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, 48):
        gdr.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)
    img = Image.alpha_composite(img, grid)

    d = ImageDraw.Draw(img)

    # logo mark
    mx, my, ms = 80, 74, 62
    d.rounded_rectangle([mx, my, mx + ms, my + ms], radius=18,
                        fill=(27, 74, 115, 255), outline=(255, 255, 255, 40), width=1)
    f_mark = font("Pretendard-Black.otf", 36)
    d.text((mx + ms / 2, my + ms / 2 - 2), "N", font=f_mark, fill=WHITE, anchor="mm")

    f_brand = font("Pretendard-ExtraBold.otf", 30)
    d.text((mx + ms + 18, my + 12), "Nexora Quote Desk", font=f_brand, fill=WHITE)
    f_tag = font("Pretendard-Bold.otf", 17)
    d.text((mx + ms + 20, my + 50), "NEXORA LABS", font=f_tag, fill=(150, 205, 198))

    # eyebrow chip (translucent fills go on their own layer so they blend)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    f_chip = font("Pretendard-Bold.otf", 19)
    chip_text = "인테리어 · 시공 견적 도구" if lang == "ko" else "ESTIMATING TOOL FOR CONTRACTORS"
    tw = d.textlength(chip_text, font=f_chip)
    od.rounded_rectangle([80, 198, 80 + tw + 34, 244], radius=23,
                         fill=(255, 255, 255, 16), outline=(120, 220, 205, 120), width=1)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    d.text((80 + 17, 211), chip_text, font=f_chip, fill=(150, 228, 216))

    # headline
    if lang == "ko":
        lines = [("인테리어 견적,", font("Pretendard-Black.otf", 68)),
                 ("링크 하나로 오늘 바로", font("Pretendard-Black.otf", 68))]
        sub = "원가·마진 자동 계산 → 견적서 인쇄까지 한 화면"
        sub2 = "설치 없음 · 회원가입 없음 · 입력한 견적은 내 기기에만"
    else:
        lines = [("Contractor estimates,", font("Pretendard-Black.otf", 62)),
                 ("opened from a single link", font("Pretendard-Black.otf", 62))]
        sub = "Cost, margin and tax in one screen, printed on Letter"
        sub2 = "No install, no sign-up. Your quotes stay on your device."

    y = 272
    for text, f in lines:
        d.text((80, y), text, font=f, fill=WHITE)
        y += 82

    f_sub = font("Pretendard-SemiBold.otf", 26)
    d.text((82, y + 6), sub, font=f_sub, fill=(196, 214, 232))
    f_sub2 = font("Pretendard-Medium.otf", 22)
    d.text((82, y + 50), sub2, font=f_sub2, fill=(170, 192, 212))

    # bottom pills
    labels = (["무료 Lite", "Business Kit 39,000원", "아이폰 · PC"] if lang == "ko"
              else ["Free Lite", "Business Kit $27", "iPhone · desktop"])
    f_pill = font("Pretendard-Bold.otf", 20)
    px = 80
    boxes = []
    for label in labels:
        tw = d.textlength(label, font=f_pill)
        boxes.append((px, tw, label))
        px += tw + 56
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for bx, tw, _ in boxes:
        od.rounded_rectangle([bx, H - 96, bx + tw + 40, H - 50], radius=23,
                             fill=(255, 255, 255, 16), outline=(255, 255, 255, 60), width=1)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    for bx, tw, label in boxes:
        d.text((bx + 20, H - 87), label, font=f_pill, fill=(232, 241, 248))

    out = os.path.join(OUT_DIR, f"og-image-{lang}.png")
    img.convert("RGB").save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out))


if __name__ == "__main__":
    build("ko")
    build("en")
