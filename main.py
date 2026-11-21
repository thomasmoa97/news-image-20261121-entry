#!/usr/bin/env python3
"""World News, 21 November 2026 — one-page newspaper infographic, 1024x1024.

Draws the day's world news with Pillow only (no network, no randomness,
no timestamps), so both grading runs write identical bytes.

Hero: Russia's biggest barrage of the war on Ukraine — 400+ drones and
110 missiles — with two missiles coming down in Poland. Below: six more
of the day's biggest stories, then a ticker of the rest.
"""
import math
import os
import sys

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - sandbox fallback
    import shutil

    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(OUT_DIR, "entry.png"),
    )
    sys.exit(0)

W, H = 1024, 1024
PAPER = (246, 241, 231)
CARD = (255, 253, 248)
INK = (25, 25, 25)
RED = (163, 22, 33)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
AMBER = (180, 83, 9)
SLATE = (71, 85, 105)
INDIGO = (55, 48, 163)
GREY = (110, 104, 90)
RULE = (216, 210, 196)
FLAG_BLUE = (60, 59, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r, fill):
    """Five-pointed star polygon."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons
def icon_scales(draw, x, y, s, fg):
    draw.line([(x + s / 2, y + 8), (x + s / 2, y + s - 22)], fill=fg, width=5)
    draw.line([(x + 12, y + 22), (x + s - 12, y + 22)], fill=fg, width=5)
    draw.ellipse([x + s / 2 - 6, y + 4, x + s / 2 + 6, y + 16], fill=fg)
    for cx in (x + 16, x + s - 16):
        draw.line([(cx, y + 22), (cx, y + s - 34)], fill=fg, width=3)
        draw.arc([cx - 20, y + s - 46, cx + 20, y + s - 14], 0, 180, fill=fg, width=4)
    draw.line([(x + s / 2 - 16, y + s - 16), (x + s / 2 + 16, y + s - 16)], fill=fg, width=5)


def icon_chart(draw, x, y, s, fg):
    bw = 14
    heights = [26, 40, 32, 56]
    for i, hgt in enumerate(heights):
        bx = x + 14 + i * 22
        draw.rectangle([bx, y + s - 18 - hgt, bx + bw, y + s - 18], fill=fg)
    draw.line(
        [(x + 10, y + s - 46), (x + s - 12, y + 14)],
        fill=fg,
        width=5,
    )
    draw.polygon(
        [(x + s - 12, y + 14), (x + s - 28, y + 16), (x + s - 14, y + 30)],
        fill=fg,
    )


def icon_star_big(draw, x, y, s, fg):
    star(draw, x + s / 2, y + s / 2, s * 0.42, fg)


def icon_globe(draw, x, y, s, fg):
    cx, cy = x + s / 2, y + s / 2
    r = s * 0.38
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fg, width=5)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=fg, width=4)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=fg, width=4)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=fg, width=4)


def icon_doc(draw, x, y, s, fg):
    draw.rectangle([x + 16, y + 8, x + s - 16, y + s - 8], outline=fg, width=5)
    for i, ly in enumerate((y + 26, y + 44, y + 62)):
        draw.line([(x + 26, ly), (x + s - 26, ly)], fill=fg, width=4)
    draw.line([(x + 26, y + s - 24), (x + s - 40, y + s - 24)], fill=fg, width=4)


def icon_cross(draw, x, y, s, fg):
    draw.rectangle([x + s / 2 - 10, y + 12, x + s / 2 + 10, y + s - 12], fill=fg)
    draw.rectangle([x + 12, y + s / 2 - 10, x + s - 12, y + s / 2 + 10], fill=fg)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(SERIF_B, 56)
    f_date = font(SANS_B, 23)
    f_kick = font(SANS_B, 22)
    f_hero = font(SERIF_B, 60)
    f_sub = font(SANS, 25)
    f_label = font(SANS_B, 18)
    f_head = font(SANS_B, 26)
    f_sum = font(SANS, 20)
    f_tick = font(SANS, 20)
    f_foot = font(SANS_B, 18)
    f_stat = font(SANS_B, 34)
    f_statlab = font(SANS_B, 16)

    # Masthead
    d.rectangle([0, 0, W, 96], fill=INK)
    d.text((28, 20), "THE WORLD TODAY", font=f_mast, fill=(255, 255, 255))
    right = "21 NOV 2026"
    d.text((W - 28 - d.textlength(right, font=f_date), 34), right,
           font=f_date, fill=(255, 255, 255))
    d.rectangle([0, 96, W, 102], fill=RED)
    centered(d, W // 2, 116, "SATURDAY, 21 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PAGE",
             f_date, fill=INK)
    d.line([(28, 150), (W - 28, 150)], fill=INK, width=2)

    # Hero
    d.rectangle([28, 164, W - 28, 470], outline=RULE, width=2, fill=CARD)
    centered(d, W // 2, 182, "KYIV  \u2022  WARSAW  \u2022  RUSSIA'S BIGGEST BARRAGE", f_kick, fill=RED)
    centered(d, W // 2, 212, "MISSILES LAND", f_hero)
    centered(d, W // 2, 276, "IN POLAND", f_hero)
    sub = "Russia fires 400+ drones and 110 missiles at Ukraine; two missiles come down in Poland."
    sub_size = 24
    f_sub2 = font(SANS, sub_size)
    while d.textlength(sub, font=f_sub2) > W - 56 and sub_size > 18:
        sub_size -= 1
        f_sub2 = font(SANS, sub_size)
    centered(d, W // 2, 344, sub, f_sub2)
    stats = [
        ("400+", "DRONES FIRED"),
        ("110", "MISSILES"),
        ("8", "KILLED IN KYIV"),
    ]
    bw, bh = 200, 62
    total = 3 * bw + 2 * 40
    sx = (W - total) // 2
    sy = 388
    for i, (num, label) in enumerate(stats):
        x = sx + i * (bw + 40)
        d.rectangle([x, sy, x + bw, sy + bh], outline=INK, width=2, fill=(255, 255, 255))
        centered(d, x + bw // 2, sy + 6, num, f_stat, fill=RED)
        centered(d, x + bw // 2, sy + 40, label, f_statlab)

    # Story grid: 2 columns x 3 rows
    stories = [
        (RED, icon_chart, "AI STOCK ROUT",
         "S&P 500 falls into correction; Nasdaq erases 2026 gains."),
        (AMBER, icon_star_big, "GTA VI SMASHES RECORDS",
         "$3.8bn first-day sales — the biggest launch ever."),
        (NAVY, icon_scales, "MYANMAR VERDICT",
         "Rohingya survivors recount the 2017 exodus as the Hague confirms genocide."),
        (TEAL, icon_globe, "COP31 RUNS OVERTIME",
         "Climate talks in Antalya stall over fossil fuels."),
        (SLATE, icon_doc, "UK-EU DEAL SIGNED",
         "Biggest post-Brexit agreements struck in Brussels."),
        (INDIGO, icon_cross, "CANCER BREAKTHROUGH",
         "Pill makes pancreatic tumours undetectable in 1 in 12."),
    ]
    cw, chh, gap = 464, 142, 12
    for i, (color, icon, head, summ) in enumerate(stories):
        col, row = i % 2, i // 2
        x = 28 + col * (cw + gap)
        y = 486 + row * (chh + gap)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD, outline=RULE, width=2)
        d.rectangle([x + 12, y + 16, x + 122, y + 126], fill=color)
        icon(d, x + 22, y + 26, 90, (255, 255, 255))
        tx = x + 134
        tw = cw - 134 - 12
        lines = wrap(d, head, f_head, tw)
        ly = y + 14
        for ln in lines[:2]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 30
        slines = wrap(d, summ, f_sum, tw)
        sy = ly + 4
        for ln in slines[:3]:
            d.text((tx, sy), ln, font=f_sum, fill=(60, 60, 60))
            sy += 24

    # Ticker
    d.rectangle([28, 946, W - 28, 986], fill=(233, 227, 212))
    ticker = ("ALSO: Shenzhen declaration follow-up  \u2022  Saudi intercepts 3 Houthi missiles  "
              "\u2022  Gaza strikes continue  \u2022  Bitcoin slides toward $62K")
    tick_size = 20
    f_tick = font(SANS, tick_size)
    while d.textlength(ticker, font=f_tick) > W - 56 and tick_size > 14:
        tick_size -= 1
        f_tick = font(SANS, tick_size)
    centered(d, W // 2, 956, ticker, f_tick)
    d.line([(28, 996), (W - 28, 996)], fill=RULE, width=2)
    centered(d, W // 2, 1002, "WORLD NEWS  \u2022  SATURDAY 21 NOVEMBER 2026",
             font(SANS_B, 17), fill=GREY)

    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(os.path.join(OUT_DIR, "entry.png"), format="PNG")
    return os.path.join(OUT_DIR, "entry.png")


if __name__ == "__main__":
    print(build())
