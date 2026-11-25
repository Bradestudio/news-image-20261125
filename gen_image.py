"""Draw the front page that sums up Wednesday 25 November 2026.

Pillow only, no network, no clock, no randomness: two runs of this file
produce byte-identical PNGs. The page is a newspaper front page built
around three illustrated hero panels, a UTC timeline, a numbers strip,
nine briefs with drawn thumbnails, a dot-matrix world map and a numbered
list of the rest of the day's stories. 40 distinct facts, all drawn from
the wire research for 25 November 2026; nothing else invented.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 22

INK = (24, 24, 26)
PAPER = (250, 247, 238)
RULE_RED = (176, 32, 28)
MUTED = (96, 90, 82)
PANEL = (255, 255, 255)
PANEL_EDGE = (206, 198, 186)
TAG_GREEN = (28, 110, 66)
TAG_AMBER = (166, 96, 8)
TAG_BLUE = (28, 84, 150)
SKY_NIGHT = (18, 26, 48)
SEA = (16, 58, 86)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    """Load a TrueType font, falling back to Pillow's built-in bitmap font
    when the file is missing (e.g. a minimal container without DejaVu)."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def shrink_to_fit(draw, text, path, size, max_w, min_size=7):
    """Largest font size <= size whose text fits max_w, else the smallest."""
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, f, max_w, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis when clipped."""
    lines = wrap(draw, text, f, max_w)
    if len(lines) <= max_lines:
        return lines
    clipped = lines[:max_lines]
    last = clipped[-1]
    while last and draw.textlength(last + "…", font=f) > max_w:
        last = last[:-1]
    clipped[-1] = last + "…"
    return clipped


def tag_chip(draw, x, y, label, fill):
    """A small coloured certainty tag; returns the width it used."""
    f = font(SANS_B, 9)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    draw.text((x + 5, y + 3), label, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories

HEROES = [
    {
        "no": 1,
        "kicker": "UKRAINE · GULF OF FINLAND",
        "head": "Ukraine drones hit Russian cargo ship in Gulf of Finland",
        "body": "Zelenskyy confirms the strike on the Sparta II; allies in "
                "Norway urge caution as Moscow vows a reply.",
        "tag": "REPORTED",
        "art": "ship",
    },
    {
        "no": 2,
        "kicker": "SAUDI ARABIA · RIYADH",
        "head": "Houthi drone hits Riyadh's tallest tower; 11 hurt",
        "body": "Civil defence says 11 people were injured in the strike on "
                "the tower; the Houthis press on toward Aden.",
        "tag": "REPORTED",
        "art": "tower",
    },
    {
        "no": 3,
        "kicker": "UNITED STATES · WASHINGTON",
        "head": "Trump gives the Medal of Freedom to Rudy Giuliani",
        "body": "The president honours his longtime ally at the White House "
                "on the eve of Thanksgiving.",
        "tag": "REPORTED",
        "art": "medal",
    },
]

BRIEFS = [
    {
        "no": 4, "head": "Putin: retaliation “inevitable” after refinery strikes",
        "body": "Moscow vows a reply after Ukraine hit its oil refineries.",
        "tag": "REPORTED", "art": "kremlin",
    },
    {
        "no": 5, "head": "Houthis 60 km from Aden; army: city will not fall",
        "body": "Government forces hold the line as the advance closes in.",
        "tag": "REPORTED", "art": "flag",
    },
    {
        "no": 6, "head": "Trump pardons Thanksgiving turkeys “Freedom” and “Feathers”",
        "body": "The two birds get the traditional presidential reprieve.",
        "tag": "REPORTED", "art": "turkey",
    },
    {
        "no": 7, "head": "Sarkozy corruption trial ordered; hearing 1 April 2027",
        "body": "A French court sends the ex-president and Carla Bruni to trial.",
        "tag": "REPORTED", "art": "court",
    },
    {
        "no": 8, "head": "Huawei guilty of trade-secret theft, cleared of racketeering",
        "body": "A US court splits the verdict in the long-running case.",
        "tag": "REPORTED", "art": "chip",
    },
    {
        "no": 9, "head": "CIA and ODNI hit by cyber breach; unclassified data leaked",
        "body": "US intelligence agencies report a security breach.",
        "tag": "REPORTED", "art": "shield",
    },
    {
        "no": 10, "head": "Anthropic falls below IPO price of $83; ~$200bn wiped out",
        "body": "The AI darling slides as the market turns on the sector.",
        "tag": "REPORTED", "art": "market",
    },
    {
        "no": 11, "head": "NATO to deploy early-warning aircraft in Poland",
        "body": "The alliance steps up its watch on the eastern flank.",
        "tag": "REPORTED", "art": "plane",
    },
    {
        "no": 12, "head": "Iran: three tankers hit by sea mines in the Strait of Hormuz",
        "body": "The IRGC navy blames mines for the blasts at the chokepoint.",
        "tag": "CLAIM", "art": "tanker",
    },
]

REST = [
    (13, "Nepal quake, magnitude 5.6, shakes Koshi province"),
    (14, "BJP and Shiromani Akali Dal reunite for Punjab 2027"),
    (15, "England beat Australia by 8 wickets, chasing 185"),
    (16, "25 Nov: Intl Day for the Elimination of Violence Against Women"),
    (17, "Dell raises outlook after a record AI server quarter"),
    (18, "Nvidia shares fall 7%"),
    (19, "UN highlights the humanitarian situation in Gaza"),
    (20, "EU announces additional sanctions on Russia"),
    (21, "Iraq PM orders federal control of Kurdish oil fields"),
    (22, "Kurds reject Baghdad's oil-field order"),
    (23, "Trump administration ready to announce new tariffs"),
    (24, "Tariffs follow a factory overcapacity probe"),
    (25, "Nepal PM Balendra Shah's state visit to India"),
    (26, "Fort Hood shooter Hasan seeks an execution delay"),
    (27, "Libya: a frozen, messy conflict"),
    (28, "Ukraine sank a Russian ship in a Libyan port on Sunday"),
    (29, "Radar outage delays flights at Chicago O'Hare"),
    (30, "Sooryavanshi hits the fastest List A double hundred"),
    (31, "New Zealand hold India to a draw in the first Test"),
    (32, "Zelenskyy confirms the Gulf of Finland strike"),
    (33, "Norway urges caution after the strike"),
    (34, "Saudi civil defence: 11 injured in Riyadh"),
    (35, "Huawei verdict: trade secrets yes, racketeering no"),
    (36, "Anthropic: ~$200bn in value wiped out"),
    (37, "NATO's AWACS watch moves east to Poland"),
    (38, "Three tankers hit; Hormuz shipping on edge"),
    (39, "Sarkozy hearing set for 1 April 2027"),
    (40, "Thanksgiving turkeys named Freedom and Feathers"),
]

TIMELINE = [
    ("02:00", "Zelenskyy confirms ship strike"),
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
    ("1 Apr '27", "Sarkozy hearing"),
]

# (x, y) in a 0..100 map grid, label, label offset (dx, dy), story no.
PINS = [
    (55, 18, "GULF OF FINLAND", (-112, -4), 1),
    (61, 44, "RIYADH", (10, 4), 2),
    (11, 36, "WASHINGTON", (8, -16), 3),
    (59, 13, "MOSCOW", (10, -4), 4),
    (59, 57, "ADEN", (10, 4), 5),
    (17, 42, "WHITE HOUSE", (10, 10), 6),
    (46, 31, "PARIS", (-62, -4), 7),
    (23, 32, "U.S. COURT", (10, -14), 8),
    (14, 48, "LANGLEY", (-52, 10), 9),
    (6, 33, "SAN FRANCISCO", (-10, 12), 10),
    (50, 28, "POLAND", (10, 4), 11),
    (66, 43, "HORMUZ", (8, -14), 12),
]

TAG_FILL = {"REPORTED": TAG_GREEN, "CLAIM": TAG_AMBER, "FORECAST": TAG_BLUE}


# ------------------------------------------------------- hero illustrations

def art_ship(draw, x, y, w, h):
    """A Russian cargo ship burning in the Gulf of Finland at night,
    a Ukrainian drone closing in from above."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_NIGHT)
    draw.ellipse([x + w - 52, y + 12, x + w - 16, y + 48], fill=(238, 228, 190))
    for sx, sy in [(14, 12), (44, 22), (90, 8), (140, 18), (190, 10), (240, 16)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # sea
    draw.rectangle([x, y + h - 44, x + w, y + h], fill=(14, 44, 70))
    for wy in range(y + h - 38, y + h - 2, 9):
        draw.line([x + 6, wy, x + w - 6, wy], fill=(34, 84, 120), width=1)
    # drone: quadcopter with a dotted approach path
    dx, dy = x + 42, y + 18
    draw.line([x + 8, y + 8, dx, dy], fill=(200, 200, 210), width=1)
    draw.rectangle([dx - 9, dy - 4, dx + 9, dy + 4], fill=(220, 224, 230))
    draw.line([dx - 14, dy - 6, dx + 14, dy - 6], fill=(180, 184, 192), width=2)
    draw.line([dx - 14, dy + 6, dx + 14, dy + 6], fill=(180, 184, 192), width=2)
    draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 60, 40))
    # cargo ship: hull, containers, bridge tower
    hx, hy = x + 48, y + h - 76
    draw.polygon([(hx, hy + 26), (hx + 190, hy + 26), (hx + 178, hy + 44),
                  (hx + 14, hy + 44)], fill=(52, 54, 62))
    draw.rectangle([hx + 8, hy + 4, hx + 52, hy + 26], fill=(176, 60, 40))
    draw.rectangle([hx + 56, hy + 4, hx + 100, hy + 26], fill=(40, 110, 70))
    draw.rectangle([hx + 104, hy + 4, hx + 148, hy + 26], fill=(200, 150, 40))
    draw.rectangle([hx + 152, hy - 14, hx + 178, hy + 26], fill=(220, 222, 228))
    for wy in range(hy - 10, hy + 24, 8):
        draw.rectangle([hx + 156, wy, hx + 174, wy + 4], fill=(60, 70, 90))
    # fire bursting from the containers
    cx = hx + 78
    for r, col in [(24, (255, 90, 20)), (16, (255, 150, 30)), (9, (255, 210, 80))]:
        draw.polygon([
            (cx - r, hy + 6), (cx - r * 0.55, hy - 26),
            (cx - r * 0.2, hy - 2), (cx + r * 0.15, hy - 32),
            (cx + r * 0.5, hy - 4), (cx + r * 0.85, hy - 18),
            (cx + r, hy + 6),
        ], fill=col)
    # smoke, kept inside the panel
    for px, py, pr in [(cx - 26, hy - 34, 10), (cx + 2, hy - 42, 11),
                       (cx + 28, hy - 32, 9)]:
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(70, 76, 88))
    # bow wake
    draw.line([hx + 178, hy + 44, x + w - 8, hy + 44], fill=(180, 200, 220), width=2)


def art_tower(draw, x, y, w, h):
    """Riyadh at night: the Kingdom Centre tower with its great arch,
    a drone strike flashing near the top."""
    draw.rectangle([x, y, x + w, y + h], fill=(14, 18, 38))
    for sx, sy in [(16, 10), (52, 20), (96, 8), (150, 14), (210, 10), (268, 18)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    draw.ellipse([x + 22, y + 10, x + 48, y + 36], fill=(238, 228, 190))
    # city skyline
    base = y + h
    for bx, bw, bh in [(0, 34, 34), (38, 26, 48), (68, 30, 28), (232, 30, 40),
                       (266, 28, 30), (298, 26, 44)]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(30, 34, 52))
        for wy in range(base - bh + 6, base - 4, 10):
            draw.rectangle([x + bx + 5, wy, x + bx + 9, wy + 4], fill=(255, 214, 130))
    # the tower: two legs and the great inverted arch opening
    tx = x + w // 2 - 34
    draw.polygon([(tx, base), (tx, y + 14), (tx + 68, y + 14), (tx + 68, base)],
                 fill=(52, 58, 78))
    draw.polygon([(tx + 10, y + 22), (tx + 34, y + 22), (tx + 34, y + 58),
                  (tx + 10, y + 58)], fill=(14, 18, 38))
    # lit windows in two columns
    for wy in range(y + 66, base - 6, 12):
        draw.rectangle([tx + 6, wy, tx + 12, wy + 5], fill=(255, 214, 130))
        draw.rectangle([tx + 56, wy, tx + 62, wy + 5], fill=(255, 214, 130))
    # crown lights
    draw.rectangle([tx, y + 14, tx + 68, y + 18], fill=(255, 200, 60))
    # strike flash at the arch: starburst + smoke
    fx, fy = tx + 34, y + 40
    for r, col in [(26, (255, 120, 30)), (16, (255, 190, 60)), (8, (255, 240, 160))]:
        draw.polygon([
            (fx - r, fy), (fx - r * 0.4, fy - r * 0.4), (fx, fy - r),
            (fx + r * 0.4, fy - r * 0.4), (fx + r, fy),
            (fx + r * 0.4, fy + r * 0.4), (fx, fy + r),
            (fx - r * 0.4, fy + r * 0.4),
        ], fill=col)
    for px, py, pr in [(fx - 24, fy - 14, 9), (fx + 26, fy - 10, 10),
                       (fx + 4, fy - 26, 8)]:
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(70, 76, 88))
    # the drone, small and dark, leaving the frame
    dx, dy = x + w - 34, y + 22
    draw.rectangle([dx - 8, dy - 3, dx + 8, dy + 3], fill=(20, 20, 26))
    draw.line([dx - 12, dy - 5, dx + 12, dy - 5], fill=(140, 144, 152), width=2)
    draw.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 60, 40))


def art_medal(draw, x, y, w, h):
    """A White House ceremony: a great gold Medal of Freedom on its
    ribbon, stars and bunting above a red carpet."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 36, 68))
    # bunting
    for i in range(7):
        bx = x + 12 + i * 42
        col = [(176, 32, 28), (255, 255, 255), (28, 84, 150)][i % 3]
        draw.polygon([(bx, y + 6), (bx + 30, y + 6), (bx + 15, y + 26)], fill=col)
    draw.line([x, y + 6, x + w, y + 6], fill=(200, 200, 210), width=1)
    # stars
    for sx, sy in [(20, 44), (280, 40), (60, 66), (240, 70), (150, 52)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 220, 120))
    # ribbon: a V of red, white and blue
    cx = x + w // 2
    draw.polygon([(cx - 52, y + 34), (cx - 34, y + 34), (cx, y + 78),
                  (cx - 18, y + 78)], fill=(176, 32, 28))
    draw.polygon([(cx + 52, y + 34), (cx + 34, y + 34), (cx, y + 78),
                  (cx + 18, y + 78)], fill=(28, 84, 150))
    draw.polygon([(cx - 34, y + 34), (cx - 16, y + 34), (cx, y + 78),
                  (cx - 18, y + 78)], fill=(255, 255, 255))
    draw.polygon([(cx + 34, y + 34), (cx + 16, y + 34), (cx, y + 78),
                  (cx + 18, y + 78)], fill=(255, 255, 255))
    # the medal: gold disc with a star
    my = y + h - 34
    draw.ellipse([cx - 26, my - 26, cx + 26, my + 26], fill=(255, 200, 60),
                 outline=(180, 130, 20), width=2)
    draw.ellipse([cx - 19, my - 19, cx + 19, my + 19], outline=(180, 130, 20), width=1)
    draw.polygon([
        (cx, my - 14), (cx + 4, my - 4), (cx + 14, my - 4), (cx + 6, my + 3),
        (cx + 9, my + 13), (cx, my + 7), (cx - 9, my + 13), (cx - 6, my + 3),
        (cx - 14, my - 4), (cx - 4, my - 4),
    ], fill=(176, 32, 28))
    # red carpet
    draw.rectangle([x, y + h - 10, x + w, y + h], fill=(140, 26, 24))
    draw.rectangle([x + 18, y + h - 10, x + w - 18, y + h], fill=(176, 32, 28))


HERO_ART = {"ship": art_ship, "tower": art_tower, "medal": art_medal}


# ------------------------------------------------------- brief thumbnails

def thumb(draw, x, y, s, kind):
    """A 44px square thumbnail drawn with plain shapes."""
    draw.rectangle([x, y, x + s, y + s], outline=PANEL_EDGE, width=1)
    if kind == "chip":
        draw.rectangle([x, y, x + s, y + s], fill=(16, 26, 44))
        draw.rectangle([x + 8, y + 14, x + 36, y + 30], fill=(34, 130, 90))
        for i in range(4):
            draw.line([x + 12 + i * 6, y + 18, x + 12 + i * 6, y + 26],
                      fill=(200, 230, 210), width=2)
        draw.line([x + 6, y + 34, x + 38, y + 34], fill=(255, 200, 60), width=3)
    elif kind == "court":
        draw.rectangle([x, y, x + s, y + s], fill=(232, 228, 216))
        draw.rectangle([x + 6, y + 34, x + 38, y + 38], fill=(90, 80, 66))
        for i in range(3):
            draw.rectangle([x + 9 + i * 11, y + 20, x + 13 + i * 11, y + 34],
                           fill=(110, 100, 84))
        draw.polygon([(x + 4, y + 20), (x + 22, y + 8), (x + 40, y + 20)],
                     fill=(140, 40, 34))
    elif kind == "market":
        draw.rectangle([x, y, x + s, y + s], fill=(245, 242, 234))
        draw.line([x + 6, y + 34, x + 14, y + 26, x + 22, y + 30, x + 30, y + 18,
                   x + 38, y + 12], fill=(176, 32, 28), width=3)
        draw.polygon([(x + 34, y + 8), (x + 40, y + 8), (x + 37, y + 15)],
                     fill=(176, 32, 28))
    elif kind == "tanker":
        draw.rectangle([x, y, x + s, y + s], fill=(18, 52, 78))
        draw.rectangle([x + 4, y + 24, x + 40, y + 32], fill=(40, 42, 48))
        draw.rectangle([x + 26, y + 16, x + 34, y + 24], fill=(70, 72, 80))
        for r, col in [(7, (255, 120, 20)), (4, (255, 200, 80))]:
            draw.ellipse([x + 12 - r, y + 14 - r, x + 12 + r, y + 14 + r], fill=col)
        draw.rectangle([x, y + 34, x + s, y + s], fill=(12, 40, 64))
    elif kind == "kremlin":
        draw.rectangle([x, y, x + s, y + s], fill=(120, 28, 24))
        draw.rectangle([x + 4, y + 32, x + 40, y + s - 4], fill=(90, 20, 18))
        for tx, th in [(8, 22), (20, 28), (32, 22)]:
            draw.rectangle([x + tx, y + 40 - th, x + tx + 6, y + 36], fill=(240, 230, 200))
            draw.polygon([(x + tx - 1, y + 40 - th), (x + tx + 3, y + 46 - th),
                          (x + tx + 7, y + 40 - th)], fill=(255, 200, 60))
        draw.ellipse([x + 19, y + 6, x + 25, y + 12], fill=(255, 200, 60))
    elif kind == "flag":
        draw.rectangle([x, y, x + s, y + s], fill=(255, 255, 255))
        draw.rectangle([x, y, x + s, y + 15], fill=(206, 32, 32))
        draw.rectangle([x, y + 29, x + s, y + s], fill=(30, 30, 32))
        draw.line([x, y + 15, x + s, y + 15], fill=(200, 200, 200), width=1)
        draw.line([x, y + 29, x + s, y + 29], fill=(200, 200, 200), width=1)
    elif kind == "turkey":
        draw.rectangle([x, y, x + s, y + s], fill=(245, 238, 220))
        # fanned tail feathers
        for i, ang in enumerate((-40, -20, 0, 20, 40)):
            fx = x + 22 + ang * 0.28
            draw.ellipse([fx - 5, y + 6, fx + 5, y + 24], fill=(150, 90, 40))
        draw.ellipse([x + 12, y + 20, x + 32, y + 38], fill=(110, 66, 30))
        draw.ellipse([x + 26, y + 10, x + 36, y + 20], fill=(110, 66, 30))
        draw.polygon([(x + 36, y + 14), (x + 42, y + 16), (x + 36, y + 18)],
                     fill=(255, 180, 60))
        draw.ellipse([x + 30, y + 12, x + 33, y + 15], fill=(24, 24, 26))
    elif kind == "shield":
        draw.rectangle([x, y, x + s, y + s], fill=(24, 48, 96))
        draw.polygon([(x + 10, y + 8), (x + 34, y + 8), (x + 34, y + 22),
                      (x + 22, y + 38), (x + 10, y + 22)], fill=(210, 220, 235))
        draw.polygon([(x + 22, y + 13), (x + 24, y + 18), (x + 29, y + 18),
                      (x + 25, y + 22), (x + 27, y + 27), (x + 22, y + 24),
                      (x + 17, y + 27), (x + 19, y + 22), (x + 15, y + 18),
                      (x + 20, y + 18)], fill=(176, 32, 28))
    else:  # plane
        draw.rectangle([x, y, x + s, y + s], fill=(160, 200, 230))
        draw.ellipse([x + 4, y + 20, x + 40, y + 30], fill=(240, 242, 246))
        draw.ellipse([x + 16, y + 12, x + 28, y + 20], fill=(240, 242, 246))
        draw.line([x + 16, y + 12, x + 28, y + 12], fill=(120, 130, 140), width=2)
        draw.polygon([(x + 34, y + 22), (x + 40, y + 16), (x + 40, y + 24)],
                     fill=(200, 205, 210))
        draw.polygon([(x + 18, y + 28), (x + 24, y + 36), (x + 28, y + 28)],
                     fill=(200, 205, 210))
        draw.rectangle([x + 6, y + 24, x + 12, y + 27], fill=(28, 84, 150))


# ------------------------------------------------------------- page sections

def draw_masthead(draw):
    title = "THE WORLD IN ONE DAY"
    tf = shrink_to_fit(draw, title, SERIF, 46, PAGE_W - 2 * MARGIN)
    draw.text(((PAGE_W - draw.textlength(title, font=tf)) / 2, 10),
              title, font=tf, fill=INK)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    df = font(SANS_B, 17)
    draw.text(((PAGE_W - draw.textlength(date, font=df)) / 2, 58),
              date, font=df, fill=RULE_RED)
    sub = "40 stories from the wires · one day · drawn from scratch"
    sf = font(SANS, 11)
    draw.text(((PAGE_W - draw.textlength(sub, font=sf)) / 2, 76),
              sub, font=sf, fill=MUTED)
    draw.rectangle([MARGIN, 94, PAGE_W - MARGIN, 97], fill=RULE_RED)


def draw_hero(draw, hero, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=PANEL_EDGE, width=1)
    art_h = 112
    HERO_ART[hero["art"]](draw, x + 1, y + 1, w - 2, art_h)
    ty = y + art_h + 8
    kf = font(SANS_B, 10)
    draw.text((x + 10, ty), hero["kicker"], font=kf, fill=RULE_RED)
    tag_chip(draw, x + w - 82, ty - 1, hero["tag"], TAG_FILL[hero["tag"]])
    hf = font(SERIF, 18)
    lines = fit_lines(draw, hero["head"], hf, w - 20, 2)
    hy = ty + 17
    for ln in lines:
        draw.text((x + 10, hy), ln, font=hf, fill=INK)
        hy += 20
    bf = font(SANS, 10)
    blines = fit_lines(draw, hero["body"], bf, w - 20, 2)
    by = hy + 3
    for ln in blines:
        draw.text((x + 10, by), ln, font=bf, fill=(52, 50, 48))
        by += 13
    # story number in a red disc, top-left over the art
    draw.ellipse([x + 8, y + 8, x + 32, y + 32], fill=RULE_RED)
    nf = font(SANS_B, 14)
    num = str(hero["no"])
    draw.text((x + 20 - draw.textlength(num, font=nf) / 2, y + 13),
              num, font=nf, fill=(255, 255, 255))


def draw_timeline(draw, y):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 66], fill=PANEL,
                   outline=PANEL_EDGE, width=1)
    tf = font(SANS_B, 11)
    draw.text((MARGIN + 10, y + 6), "THE DAY IN UTC", font=tf, fill=INK)
    note = "times approximate · UTC"
    nf = font(SANS, 9)
    draw.text((PAGE_W - MARGIN - 10 - draw.textlength(note, font=nf), y + 7),
              note, font=nf, fill=MUTED)
    line_y = y + 42
    draw.line([MARGIN + 16, line_y, PAGE_W - MARGIN - 16, line_y],
              fill=(180, 172, 158), width=2)
    slot_w = (PAGE_W - 2 * MARGIN - 32) / 6
    for i, (t, label) in enumerate(TIMELINE):
        cx = MARGIN + 16 + slot_w * i + slot_w / 2
        draw.ellipse([cx - 4, line_y - 4, cx + 4, line_y + 4], fill=RULE_RED)
        tf2 = font(SANS_B, 11)
        draw.text((cx - draw.textlength(t, font=tf2) / 2, line_y - 20),
                  t, font=tf2, fill=RULE_RED)
        lf = font(SANS, 8)
        for j, ln in enumerate(wrap(draw, label, lf, slot_w - 6)):
            draw.text((cx - draw.textlength(ln, font=lf) / 2, line_y + 8 + j * 10),
                      ln, font=lf, fill=(52, 50, 48))


def draw_numbers(draw, y):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 40], fill=INK)
    tf = font(SANS_B, 10)
    draw.text((MARGIN + 10, y + 4), "BY THE NUMBERS", font=tf, fill=(255, 210, 90))
    slot_w = (PAGE_W - 2 * MARGIN - 180) / len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        cx = MARGIN + 180 + slot_w * i + slot_w / 2
        nf = font(SANS_B, 14)
        draw.text((cx - draw.textlength(num, font=nf) / 2, y + 5),
                  num, font=nf, fill=(255, 255, 255))
        lf = font(SANS, 8)
        lab = label if draw.textlength(label, font=lf) <= slot_w - 4 else label[:12]
        draw.text((cx - draw.textlength(lab, font=lf) / 2, y + 24),
                  lab, font=lf, fill=(200, 196, 188))


def draw_briefs(draw, y):
    cols, rows = 3, 3
    cw = (PAGE_W - 2 * MARGIN - 2 * 10) // cols
    ch = 58
    for idx, b in enumerate(BRIEFS):
        r, c = divmod(idx, cols)
        bx = MARGIN + c * (cw + 10)
        by = y + r * (ch + 6)
        draw.rectangle([bx, by, bx + cw, by + ch], fill=PANEL,
                       outline=PANEL_EDGE, width=1)
        thumb(draw, bx + 6, by + 7, 44, b["art"])
        tx = bx + 56
        hf = shrink_to_fit(draw, b["head"], SANS_B, 11, cw - 62)
        hl = fit_lines(draw, b["head"], hf, cw - 62, 2)
        hy = by + 5
        for ln in hl:
            draw.text((tx, hy), ln, font=hf, fill=INK)
            hy += 13
        bf = font(SANS, 8)
        bl = fit_lines(draw, b["body"], bf, cw - 62, 2)
        if len(bl) == 2:
            # keep the second line clear of the tag chip at bottom-right
            second = bl[1]
            while second and draw.textlength(second + "…", font=bf) > cw - 62 - 78:
                second = second[:-1]
            bl[1] = second + "…" if second != bl[1] else second
        for ln in bl:
            draw.text((tx, hy), ln, font=bf, fill=(72, 68, 64))
            hy += 11
        tag_chip(draw, bx + cw - 74, by + ch - 18, b["tag"], TAG_FILL[b["tag"]])


# ------------------------------------------------------- map, list, footer

LAND = [
    # (cx, cy, rx, ry) ellipses in a 0..100 map grid: rough continents.
    (15, 32, 14, 13),   # North America
    (28, 64, 8, 10),    # South America
    (48, 27, 8, 10),    # Europe
    (56, 56, 10, 12),   # Africa
    (72, 28, 17, 13),   # Asia
    (80, 52, 6, 5),     # South-East Asia
    (60, 40, 6, 5),     # Middle East
    (88, 74, 8, 6),     # Australia / Oceania
]


def draw_map(draw, y, h):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + h], fill=PANEL,
                   outline=PANEL_EDGE, width=1)
    tf = font(SANS_B, 11)
    draw.text((MARGIN + 10, y + 5), "THE WORLD, PINNED — STORIES 1–12",
              font=tf, fill=INK)
    mx, my = MARGIN + 14, y + 24
    mw, mh = PAGE_W - 2 * MARGIN - 28, h - 32
    draw.rectangle([mx, my, mx + mw, my + mh], fill=(214, 230, 240))
    # dot-matrix continents: sample a fixed grid, keep dots inside ellipses
    step = 4
    for gy in range(0, 101, step):
        for gx in range(0, 101, step):
            inside = any(
                ((gx - cx) / rx) ** 2 + ((gy - cy) / ry) ** 2 <= 1
                for cx, cy, rx, ry in LAND
            )
            if inside:
                px = mx + gx / 100 * mw
                py = my + gy / 100 * mh
                draw.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5],
                             fill=(110, 140, 110))
    pf = font(SANS_B, 8)
    for gx, gy, label, (dx, dy), no in PINS:
        px = mx + gx / 100 * mw
        py = my + gy / 100 * mh
        lx, ly = px + dx, py + dy
        lw = draw.textlength(label, font=pf)
        lx = max(mx + 2, min(lx, mx + mw - lw - 2))
        ly = max(my + 1, min(ly, my + mh - 11))
        # leader line from the label to its pin when the label sits apart
        if abs(lx + lw / 2 - px) > 16 or abs(ly + 4 - py) > 12:
            draw.line([lx + lw / 2, ly + 4, px, py], fill=(120, 110, 100), width=1)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RULE_RED,
                     outline=(255, 255, 255), width=1)
        ns = str(no)
        nf2 = font(SANS_B, 7)
        draw.text((px - draw.textlength(ns, font=nf2) / 2, py - 5),
                  ns, font=nf2, fill=(255, 255, 255))
        draw.text((lx, ly), label, font=pf, fill=INK)


def draw_list(draw, y, h):
    tf = font(SANS_B, 11)
    draw.text((MARGIN, y), "THE REST OF THE DAY — 13–40", font=tf, fill=INK)
    draw.line([MARGIN, y + 16, PAGE_W - MARGIN, y + 16], fill=PANEL_EDGE, width=1)
    col_w = (PAGE_W - 2 * MARGIN - 16) // 2
    row_h = (h - 22) / 14
    lf = font(SANS, 8)
    bf = font(SANS_B, 8)
    for idx, (no, text) in enumerate(REST):
        col, row = divmod(idx, 14)
        lx = MARGIN + col * (col_w + 16)
        ly = y + 20 + row * row_h
        draw.text((lx, ly), f"{no}.", font=bf, fill=RULE_RED)
        tw = col_w - 24
        line = text
        while line and draw.textlength(line, font=lf) > tw:
            line = line[:-1]
        draw.text((lx + 22, ly), line, font=lf, fill=(40, 38, 36))


def draw_footer(draw, y):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + 50], fill=(238, 232, 220))
    tf = font(SANS_B, 10)
    draw.text((MARGIN + 10, y + 4), "DATE CHECK", font=tf, fill=RULE_RED)
    ff = font(SANS, 9)
    msg = ("Left out on purpose: the Merkury sinking off Libya happened on "
           "Sunday and is reported again today, not as new; the Sarkozy "
           "hearing date (1 Apr 2027) is a future date, not today's news; "
           "Nepal PM Shah's India visit was 22–23 Nov, included as context.")
    for i, ln in enumerate(fit_lines(draw, msg, ff, PAGE_W - 2 * MARGIN - 20, 2)):
        draw.text((MARGIN + 10, y + 17 + i * 11), ln, font=ff, fill=(52, 50, 48))
    lf = font(SANS, 8)
    legend = ("REPORTED = confirmed by officials or wires  ·  CLAIM = one side's "
              "account  ·  FORECAST = a plan or proposal  ·  Sources: Reuters, AP, "
              "AFP, Saudi civil defence, wire reports of 25 Nov 2026.")
    draw.text((MARGIN + 10, y + 40), legend, font=lf, fill=MUTED)


def build(path):
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    hero_y, hero_h = 104, 224
    hw = (PAGE_W - 2 * MARGIN - 2 * 10) // 3
    for i, hero in enumerate(HEROES):
        draw_hero(draw, hero, MARGIN + i * (hw + 10), hero_y, hw, hero_h)
    draw_timeline(draw, 336)
    draw_numbers(draw, 410)
    draw_briefs(draw, 458)
    draw_map(draw, 652, 132)
    draw_list(draw, 792, 170)
    draw_footer(draw, 970)
    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
