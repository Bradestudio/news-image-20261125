#!/usr/bin/env python3
"""Render entry.png for the news-image-20261125 bounty.

Build-machine only: draws the whole front page procedurally with Pillow
and the local DejaVu fonts (falls back to Pillow's default bitmap font
if DejaVu is missing). No network, no clock, no randomness: two runs
produce a byte-identical file.

Output: entry.png, 1024x1024, next to this script.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 22
CW = W - 2 * MARGIN  # 980

PAPER = (248, 242, 228)
INK = (26, 26, 26)
RED = (163, 31, 31)
DARKRED = (122, 20, 20)
NAVY = (22, 35, 61)
NAVY2 = (27, 31, 58)
GREEN = (30, 125, 50)
ORANGE = (178, 106, 0)
GOLD = (201, 162, 39)
LIGHTBLUE = (223, 233, 242)
RULE = (26, 26, 26)
MUTED = (90, 84, 72)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
]


def load_font(bold=False, serif=False, size=12):
    """Pick a local DejaVu font; fall back to Pillow's default font."""
    names = []
    if serif:
        names = ["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf"] if bold else [
            "DejaVuSerif.ttf",
            "DejaVuSerif-Bold.ttf",
        ]
    else:
        names = ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"] if bold else [
            "DejaVuSans.ttf",
            "DejaVuSans-Bold.ttf",
        ]
    for directory in FONT_DIRS:
        for name in names:
            path = Path(directory) / name
            if path.exists():
                try:
                    return ImageFont.truetype(str(path), size)
                except OSError:
                    continue
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, font, fill=INK, leading=None):
    """Draw lines top-down; return the y just below the last line."""
    if leading is None:
        leading = font.size + 3
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def badge(draw, x, y, label, fill):
    """Small rounded label; returns its width."""
    font = load_font(bold=True, size=9)
    w = int(draw.textlength(label, font=font)) + 12
    h = 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill)
    draw.text((x + 6, y + 2), label, font=font, fill=(255, 255, 255))
    return w


def number_disc(draw, cx, cy, number, r=14):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    font = load_font(bold=True, size=15)
    label = str(number)
    tw = draw.textlength(label, font=font)
    draw.text((cx - tw / 2, cy - 9), label, font=font, fill=(255, 255, 255))


# ---------------------------------------------------------------- heroes

def hero_ship(draw, x, y, w, h):
    """Burning cargo ship at night in the Gulf of Finland."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    draw.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(18, 28, 52))
    # moon
    draw.ellipse([x + w - 52, y + 14, x + w - 18, y + 48], fill=(238, 226, 190))
    # stars
    for sx, sy in [(30, 18), (90, 30), (150, 14), (210, 26), (260, 12)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # sea
    sea_y = y + int(h * 0.62)
    draw.rectangle([x, sea_y, x + w, y + h], fill=(16, 42, 66))
    for i in range(5):
        ly = sea_y + 8 + i * 9
        draw.line([x + 8, ly, x + w - 8, ly], fill=(52, 96, 128), width=2)
    # hull
    hull_y = sea_y - 16
    draw.polygon(
        [(x + 18, hull_y), (x + w - 18, hull_y), (x + w - 34, hull_y + 18),
         (x + 34, hull_y + 18)],
        fill=(38, 38, 44),
    )
    # containers
    draw.rectangle([x + 44, hull_y - 26, x + 96, hull_y], fill=(178, 58, 40))
    draw.rectangle([x + 100, hull_y - 26, x + 152, hull_y], fill=(46, 110, 62))
    draw.rectangle([x + 156, hull_y - 26, x + 208, hull_y], fill=(198, 142, 40))
    # flames over the middle container
    fx = x + 126
    draw.polygon([(fx - 26, hull_y - 24), (fx, hull_y - 66), (fx + 26, hull_y - 24)],
                 fill=(230, 110, 20))
    draw.polygon([(fx - 14, hull_y - 24), (fx, hull_y - 52), (fx + 14, hull_y - 24)],
                 fill=(244, 196, 48))
    draw.polygon([(fx - 6, hull_y - 24), (fx, hull_y - 38), (fx + 6, hull_y - 24)],
                 fill=(250, 240, 180))
    # smoke
    for sx, sy, sr in [(104, 26, 9), (122, 16, 12), (146, 24, 9), (134, 34, 7)]:
        draw.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                     fill=(70, 70, 78))
    # bridge tower
    draw.rectangle([x + w - 78, hull_y - 44, x + w - 48, hull_y], fill=(220, 220, 214))
    for wy in range(hull_y - 40, hull_y - 4, 9):
        draw.rectangle([x + w - 74, wy, x + w - 52, wy + 5], fill=(30, 60, 90))
    # drone silhouette
    dx, dy = x + 240, y + 22
    draw.line([dx - 12, dy - 8, dx + 12, dy + 8], fill=(255, 255, 255), width=2)
    draw.line([dx - 12, dy + 8, dx + 12, dy - 8], fill=(255, 255, 255), width=2)
    draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=RED)


def hero_tower(draw, x, y, w, h):
    """Riyadh's tallest tower struck by a drone at night."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY2)
    draw.ellipse([x + 24, y + 14, x + 52, y + 42], fill=(238, 226, 190))
    # skyline
    buildings = [
        (8, 62, 34, 46), (48, 78, 30, 30), (84, 58, 36, 50),
        (236, 70, 32, 38), (274, 56, 30, 52),
    ]
    for bx, by, bw, bh in buildings:
        draw.rectangle([x + bx, y + by, x + bx + bw, y + by + bh], fill=(12, 16, 34))
        for wy in range(by + 6, by + bh - 4, 10):
            for wx in range(bx + 5, bx + bw - 4, 10):
                draw.rectangle([x + wx, y + wy, x + wx + 4, y + wy + 5],
                               fill=(244, 196, 80))
    # tallest tower, centre
    tx = x + w // 2
    draw.rectangle([tx - 26, y + 34, tx + 26, y + h], fill=(10, 13, 30))
    draw.rectangle([tx - 20, y + 22, tx + 20, y + 34], fill=(10, 13, 30))
    for wy in range(40, h - 6, 11):
        draw.rectangle([tx - 18, y + wy, tx - 8, y + wy + 6], fill=(244, 196, 80))
        draw.rectangle([tx + 8, y + wy, tx + 18, y + wy + 6], fill=(244, 196, 80))
    # blast diamond on the tower
    bx, by = tx, y + 62
    draw.polygon([(bx, by - 22), (bx + 18, by), (bx, by + 22), (bx - 18, by)],
                 fill=(244, 140, 30))
    draw.polygon([(bx, by - 12), (bx + 10, by), (bx, by + 12), (bx - 10, by)],
                 fill=(250, 220, 120))
    draw.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 255, 255))
    # smoke puffs
    for sx, sy, sr in [(tx - 34, 34, 8), (tx + 36, 26, 10), (tx + 44, 44, 7)]:
        draw.ellipse([sx - sr, y + sy - sr, sx + sr, y + sy + sr], fill=(80, 80, 88))
    # ground glow
    draw.rectangle([x, y + h - 10, x + w, y + h], fill=(40, 26, 18))


def hero_medal(draw, x, y, w, h):
    """Presidential Medal of Freedom on a navy field with bunting."""
    draw.rectangle([x, y, x + w, y + h], fill=(28, 36, 71))
    # bunting
    colours = [RED, (255, 255, 255), (30, 60, 140), (255, 255, 255)]
    for i in range(8):
        bx = x + 6 + i * 40
        col = colours[i % len(colours)]
        draw.polygon([(bx, y + 6), (bx + 34, y + 6), (bx + 17, y + 30)], fill=col)
    # gold dots (stars)
    for sx, sy in [(30, 52), (90, 44), (250, 48), (292, 60), (60, 92), (268, 96)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(244, 210, 110))
    # ribbon
    cx = x + w // 2
    draw.polygon([(cx - 26, y + 40), (cx + 26, y + 40), (cx + 12, y + 78),
                  (cx - 12, y + 78)], fill=RED)
    draw.polygon([(cx - 9, y + 40), (cx + 9, y + 40), (cx + 4, y + 78),
                  (cx - 4, y + 78)], fill=(255, 255, 255))
    draw.polygon([(cx - 26, y + 40), (cx - 9, y + 40), (cx - 4, y + 78),
                  (cx - 12, y + 78)], fill=(30, 60, 140))
    draw.polygon([(cx + 9, y + 40), (cx + 26, y + 40), (cx + 12, y + 78),
                  (cx + 4, y + 78)], fill=(30, 60, 140))
    # medal
    my = y + 96
    draw.ellipse([cx - 26, my - 26, cx + 26, my + 26], fill=(212, 175, 55))
    draw.ellipse([cx - 20, my - 20, cx + 20, my + 20], outline=(150, 115, 30), width=2)
    sx, sy = cx, my
    draw.polygon([(sx, sy - 13), (sx + 4, sy - 4), (sx + 13, sy - 4), (sx + 6, sy + 3),
                  (sx + 8, sy + 12), (sx, sy + 7), (sx - 8, sy + 12), (sx - 6, sy + 3),
                  (sx - 13, sy - 4), (sx - 4, sy - 4)], fill=RED)


# ---------------------------------------------------------------- thumbnails

def thumb(draw, x, y, s, kind):
    """Small 58x58 procedural illustration for briefs 4-12."""
    draw.rectangle([x, y, x + s, y + s], outline=RULE, width=1)
    if kind == 4:  # Kremlin towers + flame
        draw.rectangle([x, y, x + s, y + s], fill=(122, 20, 20))
        for tx in (x + 8, x + 24, x + 40):
            draw.rectangle([tx, y + 26, tx + 10, y + s], fill=(212, 175, 55))
            draw.polygon([(tx - 2, y + 26), (tx + 5, y + 12), (tx + 12, y + 26)],
                         fill=(212, 175, 55))
        draw.polygon([(x + 30, y + 34), (x + 36, y + 18), (x + 42, y + 34)],
                     fill=(244, 140, 30))
    elif kind == 5:  # flag stripes
        draw.rectangle([x, y, x + s, y + 20], fill=RED)
        draw.rectangle([x, y + 20, x + s, y + 39], fill=(255, 255, 255))
        draw.rectangle([x, y + 39, x + s, y + s], fill=(20, 20, 20))
        draw.rectangle([x + 22, y + 30, x + 36, y + s], fill=(90, 70, 40))
    elif kind == 6:  # turkey
        draw.rectangle([x, y, x + s, y + s], fill=(232, 214, 176))
        draw.ellipse([x + 12, y + 26, x + 46, y + 52], fill=(120, 72, 32))
        draw.ellipse([x + 34, y + 12, x + 48, y + 28], fill=(120, 72, 32))
        draw.polygon([(x + 46, y + 18), (x + 54, y + 21), (x + 46, y + 24)],
                     fill=(230, 120, 30))
        draw.ellipse([x + 40, y + 17, x + 43, y + 20], fill=(20, 20, 20))
    elif kind == 7:  # courthouse
        draw.rectangle([x, y, x + s, y + s], fill=(232, 224, 200))
        draw.polygon([(x + 4, y + 20), (x + s // 2, y + 6), (x + s - 4, y + 20)],
                     fill=(150, 60, 50))
        for cx in (x + 10, x + 24, x + 38):
            draw.rectangle([cx, y + 22, cx + 6, y + 48], fill=(240, 236, 224))
        draw.rectangle([x + 6, y + 48, x + s - 6, y + 53], fill=(120, 110, 96))
    elif kind == 8:  # chip
        draw.rectangle([x, y, x + s, y + s], fill=(16, 32, 48))
        draw.rectangle([x + 14, y + 14, x + s - 14, y + s - 14], fill=(30, 90, 60))
        for i in range(4):
            draw.line([x + 14 + i * 9, y + 6, x + 14 + i * 9, y + 14], fill=GOLD, width=2)
            draw.line([x + 14 + i * 9, y + s - 14, x + 14 + i * 9, y + s - 6],
                      fill=GOLD, width=2)
        draw.rectangle([x + 22, y + 22, x + s - 22, y + s - 22], fill=(212, 175, 55))
    elif kind == 9:  # shield
        draw.rectangle([x, y, x + s, y + s], fill=NAVY)
        draw.polygon([(x + 10, y + 10), (x + s - 10, y + 10), (x + s - 10, y + 32),
                      (x + s // 2, y + 50), (x + 10, y + 32)], fill=(240, 240, 236))
        draw.polygon([(x + 29, y + 18), (x + 31, y + 24), (x + 38, y + 24),
                      (x + 32, y + 28), (x + 34, y + 34), (x + 29, y + 31),
                      (x + 24, y + 34), (x + 26, y + 28), (x + 20, y + 24),
                      (x + 27, y + 24)], fill=RED)
    elif kind == 10:  # falling chart
        draw.rectangle([x, y, x + s, y + s], fill=(255, 255, 255))
        draw.line([x + 8, y + 14, x + 20, y + 22, x + 32, y + 20, x + 44, y + 40,
                   x + 50, y + 46], fill=RED, width=3)
        draw.polygon([(x + 44, y + 40), (x + 52, y + 40), (x + 48, y + 48)], fill=RED)
    elif kind == 11:  # AWACS plane
        draw.rectangle([x, y, x + s, y + s], fill=(180, 210, 235))
        draw.ellipse([x + 10, y + 20, x + 48, y + 38], fill=(255, 255, 255),
                     outline=(40, 60, 90), width=1)
        draw.polygon([(x + 40, y + 24), (x + 52, y + 14), (x + 50, y + 26)],
                     fill=(255, 255, 255))
        draw.polygon([(x + 22, y + 36), (x + 30, y + 46), (x + 34, y + 36)],
                     fill=(230, 235, 240))
        draw.ellipse([x + 24, y + 14, x + 34, y + 19], fill=(200, 200, 200),
                     outline=(40, 60, 90), width=1)
        for wx in (x + 16, x + 22, x + 28):
            draw.rectangle([wx, y + 25, wx + 3, y + 29], fill=(40, 60, 90))
    else:  # 12: tanker + mine
        draw.rectangle([x, y, x + s, y + s], fill=(16, 42, 66))
        draw.polygon([(x + 6, y + 32), (x + s - 6, y + 32), (x + s - 12, y + 42),
                      (x + 12, y + 42)], fill=(40, 40, 44))
        draw.rectangle([x + 30, y + 24, x + 40, y + 32], fill=(200, 200, 190))
        draw.ellipse([x + 8, y + 12, x + 18, y + 22], fill=(230, 140, 30))
        for ang in range(0, 360, 45):
            import math
            rx = 13 + int(5 * math.cos(math.radians(ang)))
            ry = 17 + int(5 * math.sin(math.radians(ang)))
            draw.line([x + rx, y + ry, x + 13, y + 17], fill=(230, 140, 30), width=1)


# ---------------------------------------------------------------- sections

HEROES = [
    {
        "num": 1,
        "kicker": "UKRAINE \u00b7 GULF OF FINLAND",
        "headline": "Ukraine drones hit Russian cargo ship in Gulf of Finland",
        "deck": "Zelenskiy confirms the strike on the Sparta II; allies in Norway urge caution as Moscow vows a reply.",
        "art": hero_ship,
    },
    {
        "num": 2,
        "kicker": "SAUDI ARABIA \u00b7 RIYADH",
        "headline": "Houthi drone hits Riyadh\u2019s tallest tower; 11 hurt",
        "deck": "Civil defence says 11 people were injured in the strike on the tower; the Houthis press on toward Aden.",
        "art": hero_tower,
    },
    {
        "num": 3,
        "kicker": "UNITED STATES \u00b7 WASHINGTON",
        "headline": "Trump gives the Medal of Freedom to Rudy Giuliani",
        "deck": "The president honours his longtime ally at the White House on the eve of Thanksgiving.",
        "art": hero_medal,
    },
]

TIMELINE = [
    ("02:00", "Zelenskiy confirms ship strike"),
    ("06:00", "Houthi drone hits Riyadh tower"),
    ("09:30", "Anthropic slips below IPO $83"),
    ("13:00", "EU unveils new Russia sanctions"),
    ("16:00", "Sarkozy trial ordered in Paris"),
    ("20:00", "England win the T20I by 8 wickets"),
]

NUMBERS = [
    ("11", "injured in Riyadh"),
    ("60 km", "Houthis from Aden"),
    ("5.6", "Nepal quake"),
    ("~$200bn", "Anthropic lost"),
    ("8 wkt", "England win"),
    ("185", "runs chased"),
    ("3", "tankers mined"),
    ("1 Apr \u201927", "Sarkozy hearing"),
]

BRIEFS = [
    (4, "Putin retaliation \u201cinevitable\u201d after refinery strikes",
     "Moscow vows a reply after Ukraine hits its oil refineries.", "REPORTED", GREEN),
    (5, "Houthis 60 km from Aden; army: city will not fall",
     "Government forces hold the line as the advance closes in.", "REPORTED", GREEN),
    (6, "Trump pardons Thanksgiving turkeys \u201cFreedom\u201d and \u201cFeathers\u201d",
     "The two birds get the traditional presidential reprieve.", "REPORTED", GREEN),
    (7, "Sarkozy corruption trial ordered; hearing 1 April 2027",
     "A French court sends the ex-president and Carla Bruni to trial.", "REPORTED", GREEN),
    (8, "Huawei guilty of trade-secret theft, cleared of racketeering",
     "A US court splits the verdict in the long-running case.", "REPORTED", GREEN),
    (9, "CIA and ODNI hit by cyber breach; unclassified data leaked",
     "US intelligence agencies report a security breach.", "REPORTED", GREEN),
    (10, "Anthropic falls below IPO price of $83; ~$200bn wiped out",
     "The AI darling slides as the market turns on the sector.", "REPORTED", GREEN),
    (11, "NATO to deploy early-warning aircraft in Poland",
     "The alliance steps up its watch on the eastern flank.", "REPORTED", GREEN),
    (12, "Iran: three tankers hit by sea mines in the Strait of Hormuz",
     "The IRGC navy blames mines for the blasts at the chokepoint.", "CLAIM", ORANGE),
]

REST = [
    (13, "Nepal quake, magnitude 5.6, shakes Koshi province"),
    (14, "BJP and Akali Dal reunite for Punjab 2027 polls"),
    (15, "England beat Australia by 8 wickets, chasing 185"),
    (16, "25 Nov: Int\u2019l Day to End Violence Against Women"),
    (17, "Dell raises outlook after record AI server quarter"),
    (18, "UN highlights the humanitarian situation in Gaza"),
    (19, "EU announces further sanctions on Russia"),
    (20, "Iraq PM seeks federal control of Kurdish oil fields; Kurds reject it"),
    (21, "Trump ready to unveil new tariffs after probe"),
    (22, "Nepal PM Balendra Shah\u2019s state visit to India"),
    (23, "Fort Hood shooter Hasan seeks execution delay"),
    (24, "Libya: a frozen, messy conflict; Kyiv sank a ship there Sunday"),
    (25, "Radar outage delays flights at Chicago O\u2019Hare"),
    (26, "GTA 6 released 19 Nov"),
    (27, "Sooryavanshi hits fastest List A double hundred"),
    (28, "New Zealand hold India to a draw in first Test"),
    (29, "Sweden: parliament votes Kristersson stays PM"),
    (30, "Tankers and shipping in the Black Sea"),
    (31, "Oil and energy prices in focus"),
    (32, "Asian stocks weaken; Sensex down 1,484"),
    (33, "India A vs Sri Lanka A cricket"),
    (34, "Sheikh Khaled visits IIT Abu Dhabi"),
    (35, "Ras Al Khaimah road crash kills 11"),
    (36, "Houthis: dead and missing after Saudi strikes in SW Yemen"),
    (37, "Venezuela public debt at $237.5 billion"),
    (38, "Man Utd and Pochettino protest Yoro red card"),
    (39, "Fort Hood hearing"),
    (40, "The world on 25 Nov \u2014 on one page"),
]

# Land masses as ellipses in normalised map coordinates (cx, cy, rx, ry).
LAND = [
    (0.13, 0.42, 0.11, 0.26),  # North America
    (0.25, 0.72, 0.05, 0.20),  # South America
    (0.50, 0.28, 0.04, 0.16),  # Europe
    (0.51, 0.62, 0.05, 0.24),  # Africa
    (0.68, 0.32, 0.16, 0.20),  # Asia
    (0.86, 0.72, 0.05, 0.12),  # Australia
]

PINS = [
    (1, "GULF OF FINLAND", 0.555, 0.14, 1, -8),
    (2, "RIYADH", 0.600, 0.50, 1, 10),
    (3, "WASHINGTON", 0.220, 0.28, 1, -8),
    (4, "MOSCOW", 0.600, 0.24, 1, 10),
    (5, "ADEN", 0.585, 0.66, 1, 10),
    (6, "WHITE HOUSE", 0.260, 0.48, 1, 10),
    (7, "PARIS", 0.465, 0.22, -1, -8),
    (8, "U.S. COURT", 0.300, 0.62, 1, 10),
    (9, "LANGLEY", 0.190, 0.52, -1, 10),
    (10, "SAN FRANCISCO", 0.080, 0.30, -1, -8),
    (11, "POLAND", 0.515, 0.38, -1, 10),
    (12, "HORMUZ", 0.640, 0.55, 1, -8),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=LIGHTBLUE)
    # dot-matrix land
    step = 7
    for gy in range(y + 4, y + h - 3, step):
        for gx in range(x + 4, x + w - 3, step):
            nx = (gx - x) / w
            ny = (gy - y) / h
            on_land = False
            for cx, cy, rx, ry in LAND:
                if ((nx - cx) / rx) ** 2 + ((ny - cy) / ry) ** 2 <= 1:
                    on_land = True
                    break
            if on_land:
                draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(90, 130, 110))
            else:
                draw.point((gx, gy), fill=(170, 190, 205))
    pin_font = load_font(bold=True, size=8)
    label_font = load_font(bold=True, size=8)
    for num, label, nx, ny, side, dy in PINS:
        px = x + int(nx * w)
        py = y + int(ny * h)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], outline=(255, 255, 255), width=1)
        nlabel = str(num)
        tw = draw.textlength(nlabel, font=pin_font)
        draw.text((px - tw / 2, py - 5), nlabel, font=pin_font, fill=(255, 255, 255))
        lw = draw.textlength(label, font=label_font)
        if side > 0:
            lx = px + 9
        else:
            lx = px - 9 - lw
        ly = py + dy
        if lx < x + 2:
            lx = x + 2
        if lx + lw > x + w - 2:
            lx = x + w - 2 - lw
        draw.text((lx, ly), label, font=label_font, fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead
    title_font = load_font(bold=True, serif=True, size=54)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 10), title, font=title_font, fill=INK)
    sub_font = load_font(bold=True, size=15)
    sub = "WEDNESDAY, 25 NOVEMBER 2026"
    sw = draw.textlength(sub, font=sub_font)
    draw.text(((W - sw) / 2, 70), sub, font=sub_font, fill=RED)
    tag_font = load_font(size=11)
    tag = "40 stories from the wires \u00b7 one day \u00b7 drawn from scratch"
    gw = draw.textlength(tag, font=tag_font)
    draw.text(((W - gw) / 2, 90), tag, font=tag_font, fill=MUTED)
    draw.line([MARGIN, 106, W - MARGIN, 106], fill=RED, width=3)

    # ---- hero panels
    hero_w = (CW - 20) // 3
    hero_x = [MARGIN, MARGIN + hero_w + 10, MARGIN + 2 * (hero_w + 10)]
    hy, img_h = 114, 120
    for hero, hx in zip(HEROES, hero_x):
        hero["art"](draw, hx, hy, hero_w, img_h)
        draw.rectangle([hx, hy, hx + hero_w, hy + img_h], outline=RULE, width=1)
        number_disc(draw, hx + 18, hy + 18, hero["num"])
        cy = hy + img_h + 7
        kicker_font = load_font(bold=True, size=10)
        draw.text((hx, cy), hero["kicker"], font=kicker_font, fill=RED)
        badge(draw, hx + hero_w - 62, cy - 1, "REPORTED", GREEN)
        head_font = load_font(bold=True, size=15)
        lines = wrap(draw, hero["headline"], head_font, hero_w)
        cy = text_block(draw, hx, cy + 16, lines[:2], head_font, leading=18)
        deck_font = load_font(size=10)
        deck_lines = wrap(draw, hero["deck"], deck_font, hero_w)
        text_block(draw, hx, cy + 2, deck_lines[:2], deck_font, fill=(60, 56, 48), leading=12)

    # ---- timeline
    ty = 326
    tl_font = load_font(bold=True, size=12)
    draw.text((MARGIN, ty), "THE DAY IN UTC", font=tl_font, fill=INK)
    note_font = load_font(size=9)
    note = "times approximate \u00b7 UTC"
    nw = draw.textlength(note, font=note_font)
    draw.text((W - MARGIN - nw, ty + 2), note, font=note_font, fill=MUTED)
    line_y = ty + 34
    draw.line([MARGIN + 10, line_y, W - MARGIN - 10, line_y], fill=(180, 170, 150), width=2)
    time_font = load_font(bold=True, size=11)
    lab_font = load_font(size=9)
    for i, (time, label) in enumerate(TIMELINE):
        cx = MARGIN + 60 + i * 172
        draw.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill=RED)
        twd = draw.textlength(time, font=time_font)
        draw.text((cx - twd / 2, line_y - 22), time, font=time_font, fill=RED)
        lab_lines = wrap(draw, label, lab_font, 150)
        ly = line_y + 10
        for line in lab_lines:
            lw = draw.textlength(line, font=lab_font)
            draw.text((cx - lw / 2, ly), line, font=lab_font, fill=INK)
            ly += 12

    # ---- numbers strip
    ny = 398
    draw.rectangle([MARGIN, ny, W - MARGIN, ny + 44], fill=(18, 18, 18))
    num_lab_font = load_font(bold=True, size=11)
    draw.text((MARGIN + 10, ny + 15), "BY THE NUMBERS", font=num_lab_font, fill=GOLD)
    val_font = load_font(bold=True, size=17)
    lab2_font = load_font(size=8)
    slot_w = (CW - 150) // len(NUMBERS)
    for i, (value, label) in enumerate(NUMBERS):
        cx = MARGIN + 150 + i * slot_w + slot_w // 2
        vw = draw.textlength(value, font=val_font)
        draw.text((cx - vw / 2, ny + 5), value, font=val_font, fill=(255, 255, 255))
        lw = draw.textlength(label, font=lab2_font)
        draw.text((cx - lw / 2, ny + 27), label, font=lab2_font, fill=(190, 185, 170))

    # ---- briefs grid 3x3
    brief_font = load_font(bold=True, size=11)
    brief_deck_font = load_font(size=9)
    bw = (CW - 20) // 3
    bh = 74
    by0 = 450
    for idx, (num, headline, deck, tag_label, tag_fill) in enumerate(BRIEFS):
        row, col = divmod(idx, 3)
        bx = MARGIN + col * (bw + 10)
        by = by0 + row * (bh + 6)
        draw.rectangle([bx, by, bx + bw, by + bh], outline=(200, 190, 170), width=1)
        thumb(draw, bx + 6, by + 8, 58, num)
        tx = bx + 72
        lines = wrap(draw, headline, brief_font, bw - 80)
        text_block(draw, tx, by + 5, lines[:2], brief_font, leading=13)
        deck_lines = wrap(draw, deck, brief_deck_font, bw - 80)
        text_block(draw, tx, by + 32, deck_lines[:2], brief_deck_font,
                   fill=(60, 56, 48), leading=11)
        badge(draw, bx + bw - 62, by + bh - 16, tag_label, tag_fill)

    # ---- map
    my = 690
    draw.text((MARGIN, my), "THE WORLD, PINNED \u2014 STORIES 1\u201312",
              font=tl_font, fill=INK)
    draw_map(draw, MARGIN, my + 20, CW, 84)

    # ---- rest of the day 13-40
    ly0 = 800
    draw.text((MARGIN, ly0), "THE REST OF THE DAY \u2014 13\u201340",
              font=tl_font, fill=INK)
    draw.line([MARGIN, ly0 + 18, W - MARGIN, ly0 + 18], fill=RULE, width=1)
    list_font = load_font(size=10)
    col_w = (CW - 20) // 2
    row_h = 9
    for i, (num, text) in enumerate(REST):
        col, row = divmod(i, 14)
        lx = MARGIN + col * (col_w + 20)
        ly = ly0 + 24 + row * row_h
        num_label = f"{num}."
        draw.text((lx, ly), num_label, font=list_font, fill=RED)
        draw.text((lx + 24, ly), text, font=list_font, fill=INK)

    # ---- footer: date check
    fy = 956
    draw.text((MARGIN, fy), "DATE CHECK", font=tl_font, fill=RED)
    foot_font = load_font(size=10)
    foot = ("Left out on purpose: the Merkury sinking off Libya happened on Sunday "
            "and is reported again today, not as new; the Sarkozy hearing date "
            "(1 Apr 2027) is a future date, not today\u2019s news; Nepal PM Shah\u2019s "
            "India visit was 22\u201323 Nov, included as context.")
    foot_lines = wrap(draw, foot, foot_font, CW)
    text_block(draw, MARGIN, fy + 17, foot_lines, foot_font,
               fill=(60, 56, 48), leading=12)
    legend_font = load_font(size=9)
    legend = ("REPORTED = confirmed by officials or wires \u00b7 CLAIM = one side\u2019s "
              "account \u00b7 FORECAST = a plan or proposal \u00b7 Sources: Reuters, AP, "
              "AFP, Saudi civil defence, wire reports of 25 Nov 2026.")
    legend_lines = wrap(draw, legend, legend_font, CW)
    text_block(draw, MARGIN, fy + 17 + len(foot_lines) * 12 + 4, legend_lines,
               legend_font, fill=MUTED, leading=11)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG", optimize=True)


if __name__ == "__main__":
    main()
