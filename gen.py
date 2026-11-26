#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125 (nurz v2).

Concept: "BY THE NUMBERS" -- a data-led front page for Wednesday
25 November 2026. Six giant-number panels, a market bar chart, a dense
42-story list in two columns, and a UTC timeline strip. All text is drawn
with PIL from the story list below; no external assets.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (11, 31, 58)
PAPER = (244, 241, 234)
INK = (22, 22, 22)
MUTED = (90, 90, 88)
RED = (192, 57, 43)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
GREEN = (30, 122, 52)
BLUE = (31, 78, 121)
PURPLE = (91, 44, 138)
DARKRED = (142, 31, 31)
TEAL = (14, 110, 110)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def fit_one_line(draw, text, fnt, max_w, min_size=10):
    """Shrink font until text fits on one line; return (font, text)."""
    size = fnt.size
    f = fnt
    while size > min_size and draw.textlength(text, font=f) > max_w:
        size -= 1
        f = ImageFont.truetype(f.path, size)
    if draw.textlength(text, font=f) > max_w:
        while draw.textlength(text + "\u2026", font=f) > max_w and len(text) > 4:
            text = text[:-1]
        text += "\u2026"
    return f, text


# ---------------------------------------------------------------- stories
# (tag, headline) -- every item verified from news reported 25 Nov 2026.
STORIES = [
    ("HORMUZ", "Iran: two oil tankers hit naval mines, catch fire"),
    ("RIYADH", "Houthi drone hits tower; 11 people injured"),
    ("RAS TANURA", "Houthis say they struck Saudi Arabia's biggest refinery"),
    ("GAZA", "Israel kills Hamas security chief Abuelouf and family"),
    ("ISRAEL", "Judges urge dropping one Netanyahu bribery case"),
    ("YEMEN", "Saudi coalition tells civilians to leave Hodeidah port"),
    ("UKRAINE", "Drones set two Rosneft refineries ablaze in Samara"),
    ("RUSSIA", "490,334 soldiers dead since 2022, leaked data show"),
    ("ODESA", "Russian strike kills two, hits Kyiv apartment block"),
    ("POLAND", "Seeks permanent US base after two airspace incursions"),
    ("BERLIN", "Merz defends Ukraine aid, warns of Russian escalation"),
    ("BRUSSELS", "EU to join next round of Ukraine peace talks"),
    ("KYIV", "Zelensky: Ukraine needs \u20ac115bn foreign aid for 2027"),
    ("SPAIN", "Puigdemont declares Dec 12 return, new independence push"),
    ("SEOUL", "KOSPI plunges 6.2%; Samsung \u22129.9%, SK Hynix \u221211.1%"),
    ("TOKYO", "Nikkei falls 2.8% as SoftBank slides 14.8%"),
    ("WALL ST", "Dow closes above 50,000 for the first time"),
    ("TARIFFS", "US plans new duties on 16 partners incl. China, EU"),
    ("BRAZIL", "US proposes 10% duty on Brazilian aircraft imports"),
    ("DELL", "Record $54.9bn sales; AI backlog hits $132.3bn"),
    ("NVIDIA", "Huang: no succession plan; shares slide about 5%"),
    ("FED", "Markets price 97% chance of a December rate hike"),
    ("HUAWEI", "US jury convicts Huawei on 10 of 12 counts"),
    ("AI", "Staff at Anthropic, OpenAI doubt models can ship safely"),
    ("ENERGY", "US-led group agrees to buy Lukoil assets"),
    ("SPACE", "Shenzhou-24 launches with Pakistan's first astronaut"),
    ("TIANGONG", "Shenzhou-24 docks 3.5 hours after lift-off"),
    ("CLIMATE", "Pope Leo XIV laments COP31 talks ending with no deal"),
    ("SUDAN", "RSF drone strikes kill 19 civilians in two cities"),
    ("CONGO", "UN evacuates Ebola workers trapped by fighting"),
    ("SENEGAL", "Reinstated as AFCON champions after CAS appeal"),
    ("CAIRO", "Fuel-tanker fire kills at least 31 on ring road"),
    ("EGYPT", "Ten die in bus-truck crash in the south"),
    ("PACIFIC", "Australia\u2013Solomons treaty bars foreign military bases"),
    ("INDONESIA", "Six dead, about 20 trapped in flooded Bogor gold mine"),
    ("SYDNEY", "Inflation hits 4.9%; central bank expected to hold"),
    ("COLOMBIA", "Hostages freed in Cartagena supermarket siege"),
    ("CUBA", "WHO chief urges end to US fuel blockade"),
    ("USA", "Second judge blocks Trump's birthright-citizenship order"),
    ("USA", "Macy's Thanksgiving parade postponed by weather"),
    ("FOOTBALL", "Liverpool 3\u20130 Brugge; Bar\u00e7a 4\u20131 Sabah; PSG 2\u20132 Roma"),
    ("FOOTBALL", "Lille stun Bayern 2\u20131; Inter beat Stuttgart 2\u20130"),
]

# (big number, label, colour) -- the six numbers that defined the day.
PANELS = [
    ("\u22126.16%", "KOSPI plunges as Asia's chip rout deepens; Samsung \u22129.9%, SK Hynix \u221211.1%", RED),
    ("50,019", "Dow closes above 50,000 for the first time in history", GREEN),
    ("$54.9B", "Dell posts a record quarter; AI-server sales $22B, up 291% \u2014 shares still fall", BLUE),
    ("2", "Oil tankers hit by naval mines and left ablaze in the Strait of Hormuz", DARKRED),
    ("31", "People killed in a fuel-tanker fire on a highway near Cairo", INK),
    ("1st", "Pakistani in orbit: Shenzhou-24 carries Muhammad Zeeshan Ali to Tiangong", PURPLE),
]

# (label, value %) -- Wednesday's market rout, for the bar chart.
BARS = [
    ("KOSPI", -6.2),
    ("TAIEX", -5.0),
    ("NIKKEI", -2.8),
    ("NASDAQ-100 FUT.", -2.2),
]

# (time, event) -- the day in UTC.
TIMELINE = [
    ("00:18 UTC", "Shenzhou-24 launches from Jiuquan"),
    ("03:56 UTC", "Shenzhou-24 docks with Tiangong"),
    ("MORNING", "Two tankers reported hit by mines in Hormuz"),
    ("AFTERNOON", "Australia\u2013Solomons security treaty signed"),
    ("EVENING", "Champions League: Liverpool 3\u20130, Bar\u00e7a 4\u20131"),
]

TAG_COLORS = {
    "HORMUZ": DARKRED, "RIYADH": DARKRED, "RAS TANURA": DARKRED,
    "GAZA": DARKRED, "ISRAEL": DARKRED, "YEMEN": DARKRED,
    "UKRAINE": (120, 60, 10), "RUSSIA": (120, 60, 10),
    "ODESA": (120, 60, 10), "POLAND": (120, 60, 10),
    "BERLIN": (120, 60, 10), "BRUSSELS": (120, 60, 10),
    "KYIV": (120, 60, 10), "SPAIN": (120, 60, 10),
    "SEOUL": RED, "TOKYO": RED, "WALL ST": RED, "TARIFFS": RED,
    "BRAZIL": RED, "DELL": RED, "NVIDIA": RED, "FED": RED,
    "HUAWEI": BLUE, "AI": BLUE, "ENERGY": BLUE,
    "SPACE": PURPLE, "TIANGONG": PURPLE, "CLIMATE": TEAL,
    "SUDAN": (110, 70, 0), "CONGO": (110, 70, 0),
    "SENEGAL": (110, 70, 0), "CAIRO": (110, 70, 0),
    "EGYPT": (110, 70, 0),
    "PACIFIC": TEAL, "INDONESIA": TEAL, "SYDNEY": TEAL,
    "COLOMBIA": GREEN, "CUBA": GREEN, "USA": GREEN,
    "FOOTBALL": (40, 40, 40),
}


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top accent bar + header band
    d.rectangle([0, 0, W, 6], fill=RED)
    d.rectangle([0, 6, W, 112], fill=NAVY)
    f_date = font(BOLD, 42)
    d.text((16, 16), "WEDNESDAY, 25 NOVEMBER 2026", font=f_date, fill=WHITE)
    f_sub = font(BOLD, 19)
    d.text((16, 72), "THE WORLD IN ONE DAY  \u00b7  BY THE NUMBERS",
           font=f_sub, fill=GOLD)
    d.text((W - 16, 74), "42 STORIES",
           font=font(BOLD, 15), fill=(180, 195, 215), anchor="ra")

    # ---- six big-number panels (2 rows x 3)
    px, py = 12, 120
    pw, ph, gap = 324, 112, 8
    for i, (num, label, color) in enumerate(PANELS):
        x = px + (i % 3) * (pw + gap)
        y = py + (i // 3) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=6, fill=WHITE)
        d.rectangle([x, y + 6, x + 6, y + ph - 6], fill=color)
        f_num = font(BOLD, 44)
        d.text((x + 18, y + 8), num, font=f_num, fill=color)
        f_lab = font(REG, 13)
        lines = wrap(d, label, f_lab, pw - 32)
        ly = y + 58
        for ln in lines[:3]:
            d.text((x + 18, ly), ln, font=f_lab, fill=INK)
            ly += 16

    # ---- market bar chart
    cy = 360
    d.text((12, cy), "MARKETS \u2014 WEDNESDAY'S ROUT",
           font=font(BOLD, 16), fill=INK)
    d.text((W - 12, cy + 2), "Asia sinks; US futures follow",
           font=font(REG, 12), fill=MUTED, anchor="ra")
    d.line([12, cy + 26, W - 12, cy + 26], fill=(200, 196, 188), width=1)
    bx, by = 12, cy + 34
    bar_h, bar_gap = 17, 6
    max_v = 7.0
    bar_max_w = 760
    for i, (lab, val) in enumerate(BARS):
        y = by + i * (bar_h + bar_gap)
        d.text((bx, y + 1), lab, font=font(BOLD, 13), fill=INK)
        bw = int(abs(val) / max_v * bar_max_w)
        d.rectangle([bx + 150, y, bx + 150 + bw, y + bar_h], fill=RED)
        d.text((bx + 150 + bw + 8, y + 1), f"{val:.1f}%",
               font=font(BOLD, 13), fill=RED)

    # ---- story list
    ly = 490
    d.text((12, ly), "THE DAY IN 42 STORIES",
           font=font(BOLD, 17), fill=INK)
    d.line([12, ly + 26, W - 12, ly + 26], fill=INK, width=2)
    rows = 21
    row_h = 16.8
    col_w = 488
    col_x = [12, 524]
    y0 = ly + 34
    for idx, (tag, head) in enumerate(STORIES):
        col = idx // rows
        row = idx % rows
        x = col_x[col]
        y = y0 + row * row_h
        f_tag = font(BOLD, 12)
        d.text((x, y), tag, font=f_tag, fill=TAG_COLORS.get(tag, INK))
        tw = d.textlength(tag, font=f_tag)
        f_head = font(REG, 12)
        f_head, head2 = fit_one_line(d, head, f_head, col_w - tw - 8)
        d.text((x + tw + 7, y), head2, font=f_head, fill=INK)

    # ---- timeline strip
    ty = 884
    d.rectangle([0, ty, W, ty + 72], fill=NAVY)
    d.text((12, ty + 6), "THE DAY IN UTC",
           font=font(BOLD, 13), fill=GOLD)
    chip_w = 196
    for i, (t, ev) in enumerate(TIMELINE):
        x = 12 + i * (chip_w + 4)
        d.text((x, ty + 26), t, font=font(BOLD, 13), fill=WHITE)
        f_ev = font(REG, 11)
        lines = wrap(d, ev, f_ev, chip_w - 4)
        ey = ty + 44
        for ln in lines[:2]:
            d.text((x, ey), ln, font=f_ev, fill=(200, 210, 225))
            ey += 13

    # ---- footer
    fy = 964
    d.text((W // 2, fy), "All events of Wednesday 25 November 2026, as reported that day.",
           font=font(REG, 12), fill=MUTED, anchor="ma")
    d.text((W // 2, fy + 18),
           "Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 UEFA \u00b7 Xinhua \u00b7 Just Security \u00b7 make.fun news-image-20261125",
           font=font(REG, 11), fill=MUTED, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {img.size}")


if __name__ == "__main__":
    draw()
