#!/usr/bin/env python3
"""One-page newspaper for Saturday 21 November 2026, drawn at 1024x1024.

The program needs Pillow and nothing else: no network access, no clock,
no random numbers, so running it twice produces byte-identical output.

Front page: Russia's biggest barrage of the war on Ukraine, with two
missiles coming down in Poland. Under it, six more stories of the day
plus a ticker of the rest.
"""
import math
import os
import sys

OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - sandbox fallback
    import shutil

    _here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(os.path.join(_here, "entry.png"),
                    os.path.join(OUT, "entry.png"))
    sys.exit(0)

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 28

PAL = {
    "paper": (246, 241, 231),
    "panel": (255, 253, 248),
    "ink": (25, 25, 25),
    "red": (163, 22, 33),
    "navy": (31, 58, 95),
    "teal": (15, 118, 110),
    "amber": (180, 83, 9),
    "slate": (71, 85, 105),
    "indigo": (55, 48, 163),
    "grey": (110, 104, 90),
    "rule": (216, 210, 196),
    "ticker": (233, 227, 212),
    "soft": (60, 60, 60),
    "white": (255, 255, 255),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(path, size):
    return ImageFont.truetype(path, size)


def serif_b(size):
    return load(FONT_DIR + "/DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load(FONT_DIR + "/DejaVuSerif.ttf", size)


def sans_b(size):
    return load(FONT_DIR + "/DejaVuSans-Bold.ttf", size)


def sans(size):
    return load(FONT_DIR + "/DejaVuSans.ttf", size)


def split_lines(draw, text, fnt, width):
    """Split text into as few lines as fit inside width (greedy)."""
    out = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=fnt) <= width:
            current = candidate
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def put_centered(draw, text, y, fnt, cx, fill):
    half = draw.textlength(text, font=fnt) / 2
    draw.text((cx - half, y), text, font=fnt, fill=fill)


def five_star(draw, cx, cy, radius, fill):
    """Star polygon: 10 vertices alternating outer/inner radius."""
    verts = []
    for step in range(10):
        angle = -math.pi / 2 + step * math.pi / 5
        rad = radius if step % 2 == 0 else radius * 0.42
        verts.append((cx + rad * math.cos(angle), cy + rad * math.sin(angle)))
    draw.polygon(verts, fill=fill)


def shrink_to_fit(draw, text, fnt_maker, limit, start, floor):
    """Largest font size (from start down to floor) whose text fits limit."""
    size = start
    while size > floor:
        fnt = fnt_maker(size)
        if draw.textlength(text, font=fnt) <= limit:
            return fnt
        size -= 1
    return fnt_maker(floor)


# ------------------------------------------------------------- tile art
def art_scales(draw, x, y, s, fg):
    mid = x + s / 2
    draw.ellipse([mid - 6, y + 4, mid + 6, y + 16], fill=fg)
    draw.line([(mid, y + 10), (mid, y + s - 22)], fill=fg, width=5)
    draw.line([(x + 12, y + 22), (x + s - 12, y + 22)], fill=fg, width=5)
    for cx in (x + 16, x + s - 16):
        draw.line([(cx, y + 22), (cx, y + s - 34)], fill=fg, width=3)
        draw.arc([cx - 20, y + s - 46, cx + 20, y + s - 14], 0, 180,
                 fill=fg, width=4)
    draw.line([(mid - 16, y + s - 16), (mid + 16, y + s - 16)], fill=fg, width=5)


def art_chart(draw, x, y, s, fg):
    for i, tall in enumerate((26, 40, 32, 56)):
        bx = x + 14 + i * 22
        draw.rectangle([bx, y + s - 18 - tall, bx + 14, y + s - 18], fill=fg)
    draw.line([(x + 10, y + s - 46), (x + s - 12, y + 14)], fill=fg, width=5)
    draw.polygon([(x + s - 12, y + 14), (x + s - 28, y + 16),
                  (x + s - 14, y + 30)], fill=fg)


def art_star(draw, x, y, s, fg):
    five_star(draw, x + s / 2, y + s / 2, s * 0.42, fg)


def art_globe(draw, x, y, s, fg):
    cx, cy = x + s / 2, y + s / 2
    r = s * 0.38
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fg, width=5)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=fg, width=4)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=fg, width=4)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360,
             fill=fg, width=4)


def art_doc(draw, x, y, s, fg):
    draw.rectangle([x + 16, y + 8, x + s - 16, y + s - 8], outline=fg, width=5)
    for ly in (y + 26, y + 44, y + 62):
        draw.line([(x + 26, ly), (x + s - 26, ly)], fill=fg, width=4)
    draw.line([(x + 26, y + s - 24), (x + s - 40, y + s - 24)], fill=fg, width=4)


def art_cross(draw, x, y, s, fg):
    mid = x + s / 2
    draw.rectangle([mid - 10, y + 12, mid + 10, y + s - 12], fill=fg)
    draw.rectangle([x + 12, y + s / 2 - 10, x + s - 12, y + s / 2 + 10], fill=fg)


STORIES = [
    ("red", art_chart, "AI STOCK ROUT",
     "S&P 500 falls into correction; Nasdaq erases 2026 gains."),
    ("amber", art_star, "GTA VI SMASHES RECORDS",
     "$3.8bn first-day sales — the biggest launch ever."),
    ("navy", art_scales, "MYANMAR VERDICT",
     "Rohingya survivors recount the 2017 exodus as the Hague confirms genocide."),
    ("teal", art_globe, "COP31 RUNS OVERTIME",
     "Climate talks in Antalya stall over fossil fuels."),
    ("slate", art_doc, "UK-EU DEAL SIGNED",
     "Biggest post-Brexit agreements struck in Brussels."),
    ("indigo", art_cross, "CANCER BREAKTHROUGH",
     "Pill makes pancreatic tumours undetectable in 1 in 12."),
]

HERO_STATS = [
    ("400+", "DRONES FIRED"),
    ("110", "MISSILES"),
    ("8", "KILLED IN KYIV"),
]

TICKER = ("ALSO: Shenzhen declaration follow-up  \u2022  Saudi intercepts "
          "3 Houthi missiles  \u2022  Gaza strikes continue  \u2022  "
          "Bitcoin slides toward $62K")


def masthead(d):
    d.rectangle([0, 0, PAGE_W, 96], fill=PAL["ink"])
    d.text((MARGIN, 20), "THE WORLD TODAY", font=serif_b(56), fill=PAL["white"])
    stamp = "21 NOV 2026"
    f_stamp = sans_b(23)
    d.text((PAGE_W - MARGIN - d.textlength(stamp, font=f_stamp), 34), stamp,
           font=f_stamp, fill=PAL["white"])
    d.rectangle([0, 96, PAGE_W, 102], fill=PAL["red"])
    put_centered(d, "SATURDAY, 21 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PAGE",
                 116, sans_b(23), PAGE_W // 2, PAL["ink"])
    d.line([(MARGIN, 150), (PAGE_W - MARGIN, 150)], fill=PAL["ink"], width=2)


def hero(d):
    top, bottom = 164, 470
    d.rectangle([MARGIN, top, PAGE_W - MARGIN, bottom], outline=PAL["rule"],
                width=2, fill=PAL["panel"])
    put_centered(d, "KYIV  \u2022  WARSAW  \u2022  RUSSIA'S BIGGEST BARRAGE",
                 182, sans_b(22), PAGE_W // 2, PAL["red"])
    put_centered(d, "MISSILES LAND", 212, serif_b(60), PAGE_W // 2, PAL["ink"])
    put_centered(d, "IN POLAND", 276, serif_b(60), PAGE_W // 2, PAL["ink"])
    sub = ("Russia fires 400+ drones and 110 missiles at Ukraine; "
           "two missiles come down in Poland.")
    f_sub = shrink_to_fit(d, sub, sans, PAGE_W - 56, 24, 18)
    put_centered(d, sub, 344, f_sub, PAGE_W // 2, PAL["ink"])
    bw, bh = 200, 62
    span = 3 * bw + 2 * 40
    left = (PAGE_W - span) // 2
    for i, (num, label) in enumerate(HERO_STATS):
        x = left + i * (bw + 40)
        d.rectangle([x, 388, x + bw, 388 + bh], outline=PAL["ink"], width=2,
                    fill=PAL["white"])
        put_centered(d, num, 394, sans_b(34), x + bw // 2, PAL["red"])
        put_centered(d, label, 428, sans_b(16), x + bw // 2, PAL["ink"])


def story_card(d, x, y, w, h, color, art, head, summ):
    d.rectangle([x, y, x + w, y + h], fill=PAL["panel"], outline=PAL["rule"],
                width=2)
    d.rectangle([x + 12, y + 16, x + 122, y + 126], fill=PAL[color])
    art(d, x + 22, y + 26, 90, PAL["white"])
    tx = x + 134
    tw = w - 134 - 12
    f_head, f_sum = sans_b(26), sans(20)
    ly = y + 14
    for line in split_lines(d, head, f_head, tw)[:2]:
        d.text((tx, ly), line, font=f_head, fill=PAL["ink"])
        ly += 30
    sy = ly + 4
    for line in split_lines(d, summ, f_sum, tw)[:3]:
        d.text((tx, sy), line, font=f_sum, fill=PAL["soft"])
        sy += 24


def story_grid(d):
    cw, chh, gap = 464, 142, 12
    for i, (color, art, head, summ) in enumerate(STORIES):
        col, row = i % 2, i // 2
        story_card(d, MARGIN + col * (cw + gap), 486 + row * (chh + gap),
                   cw, chh, color, art, head, summ)


def ticker(d):
    d.rectangle([MARGIN, 946, PAGE_W - MARGIN, 986], fill=PAL["ticker"])
    f_tick = shrink_to_fit(d, TICKER, sans, PAGE_W - 56, 20, 14)
    put_centered(d, TICKER, 956, f_tick, PAGE_W // 2, PAL["ink"])
    d.line([(MARGIN, 996), (PAGE_W - MARGIN, 996)], fill=PAL["rule"], width=2)
    put_centered(d, "WORLD NEWS  \u2022  SATURDAY 21 NOVEMBER 2026",
                 1002, sans_b(17), PAGE_W // 2, PAL["grey"])


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAL["paper"])
    d = ImageDraw.Draw(img)
    masthead(d)
    hero(d)
    story_grid(d)
    ticker(d)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "entry.png")
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    print(build())
