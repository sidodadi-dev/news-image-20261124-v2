#!/usr/bin/env python3
"""Draw the v2 poster for Tuesday 24 November 2026 world news.

A newspaper front page: masthead with the day, two illustrated lead
stories, nine region-tagged story tiles, a long list of further
headlines, a Champions League results strip and a markets strip.
Every story was reported on 24 November 2026. Deterministic output:
no randomness, no clock, no network. Run: python3 poster.py
writes poster.png (1024x1024) next to this file.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (22, 35, 63)
MUTED = (90, 96, 110)
RULE = (22, 35, 63)
CARD = (255, 253, 247)
GREEN = (34, 120, 66)
RED = (158, 42, 32)
BLUE = (31, 78, 121)
AMBER = (166, 102, 0)
PURPLE = (91, 45, 142)
TEAL = (14, 110, 110)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width, using textwrap on word boundaries."""
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def draw_text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = fnt.size + 4
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, color):
    f = font(12, bold=True)
    tw = draw.textlength(label, font=f)
    draw.rounded_rectangle([x, y, x + tw + 14, y + 20], radius=4, fill=color)
    draw.text((x + 7, y + 3), label, font=f, fill=(255, 255, 255))
    return x + tw + 14


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin

    # ---------- masthead ----------
    d.text((m, 14), "THE WORLD IN ONE DAY", font=font(52, bold=True), fill=INK)
    d.text((m, 76), "TUESDAY  24  NOVEMBER  2026", font=font(30, bold=True),
           fill=RED)
    d.text((W - m - 250, 84), "31 stories  ·  10 regions",
           font=font(15), fill=MUTED)
    d.line([(m, 116), (W - m, 116)], fill=RULE, width=4)
    d.line([(m, 122), (W - m, 122)], fill=RULE, width=1)

    # ---------- lead row: two big cards ----------
    lead_y, lead_h = 132, 190
    cw = (W - 2 * m - 16) // 2
    # Card A: AI rally
    ax, ay = m, lead_y
    d.rounded_rectangle([ax, ay, ax + cw, ay + lead_h], radius=8, fill=CARD,
                        outline=RULE, width=1)
    d.rectangle([ax, ay, ax + cw, ay + 6], fill=GREEN)
    tag(d, ax + 12, ay + 16, "MARKETS · ASIA", GREEN)
    d.text((ax + 12, ay + 44), "AI RALLY ROARS ON", font=font(27, bold=True),
           fill=INK)
    d.text((ax + 12, ay + 76), "IN ASIA", font=font(27, bold=True), fill=INK)
    sub = ("Nikkei +3.9% · Kospi +7% · Taiex +9.1% as Huang's return "
           "revives the AI trade; S&P 500 −0.95%.")
    draw_text_block(d, ax + 12, ay + 110, wrap(d, sub, font(14), cw - 24),
                    font(14), MUTED, leading=19)
    # rising chart illustration, bottom right of card A
    chart = [(ax + cw - 190, ay + 176), (ax + cw - 150, ay + 162),
             (ax + cw - 112, ay + 166), (ax + cw - 74, ay + 148),
             (ax + cw - 36, ay + 142)]
    d.line(chart, fill=GREEN, width=4, joint="curve")
    d.polygon([(ax + cw - 48, ay + 132), (ax + cw - 24, ay + 132),
               (ax + cw - 36, ay + 146)], fill=GREEN)
    for (px, py) in chart:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GREEN)
    d.text((ax + 12, ay + 170), "+31.5% Nvidia on Monday",
           font=font(13, bold=True), fill=GREEN)

    # Card B: Nepal quake
    bx = m + cw + 16
    d.rounded_rectangle([bx, ay, bx + cw, ay + lead_h], radius=8, fill=CARD,
                        outline=RULE, width=1)
    d.rectangle([bx, ay, bx + cw, ay + 6], fill=RED)
    tag(d, bx + 12, ay + 16, "DISASTER · SOUTH ASIA", RED)
    d.text((bx + 12, ay + 44), "M5.3 QUAKE SHAKES", font=font(27, bold=True),
           fill=INK)
    d.text((bx + 12, ay + 76), "NEPAL", font=font(27, bold=True), fill=INK)
    sub2 = ("Koshi province, 7:02 a.m., depth 10 km; tremors felt in "
            "India, Bhutan, Bangladesh and China. No casualties reported.")
    draw_text_block(d, bx + 12, ay + 110, wrap(d, sub2, font(14), cw - 24),
                    font(14), MUTED, leading=19)
    # mountains + seismograph illustration, kept clear of the text above
    base = ay + 186
    d.polygon([(bx + cw - 210, base), (bx + cw - 150, ay + 152),
               (bx + cw - 90, base)], fill=(120, 140, 165))
    d.polygon([(bx + cw - 130, base), (bx + cw - 70, ay + 162),
               (bx + cw - 10, base)], fill=(90, 110, 140))
    d.polygon([(bx + cw - 160, ay + 162), (bx + cw - 150, ay + 152),
               (bx + cw - 140, ay + 162)], fill=(255, 255, 255))
    seis = [(bx + 12, ay + 158), (bx + 60, ay + 158), (bx + 74, ay + 146),
            (bx + 88, ay + 172), (bx + 102, ay + 152), (bx + 116, ay + 168),
            (bx + 130, ay + 146), (bx + 144, ay + 172), (bx + 158, ay + 158),
            (bx + 200, ay + 158)]
    d.line(seis, fill=RED, width=3, joint="curve")
    d.text((bx + 12, ay + 172), "2.3m people within 100 km",
           font=font(12, bold=True), fill=RED)

    # ---------- nine story tiles ----------
    tiles = [
        ("EUROPE", BLUE, "Spain amnesties Puigdemont",
         "Supreme Court ends the 2017 independence cases."),
        ("MIDDLE EAST", RED, "Riyadh tower hit, 11 hurt",
         "Houthis strike the capital's tallest tower, again."),
        ("MIDDLE EAST", RED, "Eisenkot's first coalition deal",
         "Israel's Yashar party agrees a pact with Lieberman."),
        ("ASIA", GREEN, "China probes Politburo member",
         "Shanghai chief Chen Jining under investigation."),
        ("AFRICA", AMBER, "Senegal's AFCON title restored",
         "Top sports court overturns the ruling that stripped it."),
        ("AMERICAS", PURPLE, "Trump to meet NATO chief Rutte",
         "Talks set for Wednesday in Florida over Ukraine."),
        ("EUROPE", BLUE, "UK inquiry into nuclear veterans",
         "Panel to examine the impact of weapons tests."),
        ("ASIA", GREEN, "Bangladesh garment workers clash",
         "Police fire tear gas as pay protests shut factories."),
        ("WAR", RED, "Zaporizhzhia strike kills two",
         "Overnight attack hits a flat block; 40 wounded."),
    ]
    ty = lead_y + lead_h + 12
    th = 112
    tw = (W - 2 * m - 2 * 12) // 3
    for i, (region, color, head, body) in enumerate(tiles):
        r, c = divmod(i, 3)
        x = m + c * (tw + 12)
        y = ty + r * (th + 8)
        d.rounded_rectangle([x, y, x + tw, y + th], radius=6, fill=CARD,
                            outline=(200, 192, 172), width=1)
        tag(d, x + 10, y + 8, region, color)
        draw_text_block(d, x + 10, y + 34,
                        wrap(d, head, font(17, bold=True), tw - 20),
                        font(17, bold=True), INK, leading=20)
        draw_text_block(d, x + 10, y + 76,
                        wrap(d, body, font(12), tw - 20),
                        font(12), MUTED, leading=15)

    # ---------- also today: one-line headlines ----------
    ay2 = ty + 3 * th + 2 * 8 + 12
    d.text((m, ay2), "ALSO TODAY", font=font(18, bold=True), fill=INK)
    d.line([(m + 130, ay2 + 12), (W - m, ay2 + 12)], fill=RULE, width=2)
    more = [
        ("Russia warns Estonia of open war over border closures", "EUROPE"),
        ("Russian jets enter S. Korea's defence zone; islanders shelter", "ASIA"),
        ("Lukashenko offers to fly with Zelenskyy to Moscow for talks", "EUROPE"),
        ("Leak points to up to 700,000 Russian military deaths", "WAR"),
        ("Gaza strike kills Hamas security chief and six others", "MIDEAST"),
        ("Houthis 60 km from Aden; Yemen army says city will hold", "MIDEAST"),
        ("US consumer confidence 103.3 in November", "AMERICAS"),
        ("Abrego Garcia to leave the US voluntarily, US media say", "AMERICAS"),
        ("US court clears army to detonate toxic explosives in Iowa", "AMERICAS"),
        ("Trump set to unveil new tariffs after capacity probe", "AMERICAS"),
        ("~175 migrants missing after boat from Senegal loses contact", "AFRICA"),
        ("Hasina plans return to Bangladesh on 16 December", "ASIA"),
        ("Indonesia seizes 405 t of missile chemical from a ship", "ASIA"),
        ("Lahore the world's most polluted major city, AQI 538", "ASIA"),
        ("Tajikistan begins process of leaving the ICC", "ASIA"),
        ("PKK pulls out of 14 more bases in northern Iraq", "MIDEAST"),
        ("Bus crash in Ras Al Khaimah, UAE: 13 killed, 14 hurt", "MIDEAST"),
        ("Bomb threats hit hundreds of schools in Denmark, Germany", "EUROPE"),
        ("Brazil cuts its 2027 growth forecast as the real weakens", "AMERICAS"),
        ("Australia plans duty-of-care fines for tech firms", "OCEANIA"),
    ]
    col_w = (W - 2 * m) // 2
    ly = ay2 + 28
    for i, (headline, region) in enumerate(more):
        col, row = divmod(i, 10)
        x = m + col * col_w
        y = ly + row * 19
        d.text((x, y), "▸", font=font(13, bold=True), fill=RED)
        d.text((x + 16, y), headline, font=font(13), fill=INK)

    # ---------- Champions League strip ----------
    sy = ly + 10 * 19 + 8
    d.rounded_rectangle([m, sy, W - m, sy + 40], radius=6, fill=INK)
    d.text((m + 12, sy + 11), "CHAMPIONS LEAGUE",
           font=font(15, bold=True), fill=(255, 210, 80))
    d.text((m + 210, sy + 11),
           "Real Madrid 5–1 PSV  ·  Arsenal 1–1 Dortmund  ·  "
           "Man City 2–2 Napoli  ·  Galatasaray 1–0 Aston Villa",
           font=font(14), fill=(255, 255, 255))

    # ---------- markets strip ----------
    ny = sy + 40 + 8
    d.text((m, ny), "MARKETS", font=font(15, bold=True), fill=INK)
    nums = ("Nikkei +3.91%    Kospi +7%    S&P 500 7,168 (−0.95%)    "
            "Brent $87.51    Gold $3,649    Bitcoin $61,137")
    d.text((m + 96, ny), nums, font=font(15), fill=MUTED)

    # ---------- footer ----------
    fy = ny + 28
    d.line([(m, fy), (W - m, fy)], fill=(200, 192, 172), width=1)
    d.text((m, fy + 8),
           "Sources: Reuters, AP, EMSC, Xinhua, UEFA, Conference Board, "
           "UK Health Security Agency — all reported 24 Nov 2026.",
           font=font(11), fill=MUTED)

    img.save("poster.png", optimize=True)
    print("poster.png written:", img.size)


if __name__ == "__main__":
    main()
