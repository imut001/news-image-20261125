"""Draw entry.png for make.fun news-image-20261125.

One 1024x1024 newspaper-style image summing up Wednesday 25 November 2026.
Run: python3 generate_image.py  ->  entry.png (deterministic, < 1 MiB).
Only Pillow + the standard library are used; no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
CANVAS = (1024, 1024)

# --- typefaces (DejaVu, shipped with the system) ---
def _typeface(name, size):
    return ImageFont.truetype(
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

SERIF_BOLD = lambda s: _typeface("DejaVuSerif-Bold", s)
SANS_BOLD = lambda s: _typeface("DejaVuSans-Bold", s)
SANS = lambda s: _typeface("DejaVuSans", s)

# --- palette ---
INK = (17, 24, 32)
PAPER = (246, 241, 231)
NAVY = (15, 42, 68)
NAVY2 = (18, 58, 92)
CARD_LINE = (220, 210, 190)
GREY = (55, 65, 75)
FAINT = (90, 95, 100)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
GOLD = (212, 175, 55)
TEAL = (14, 110, 110)
ORANGE = (214, 105, 30)
SEA = (27, 98, 148)
SKY = (190, 220, 240)


def wrap_text(draw, text, face, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    out, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def paragraph(draw, x, y, text, face, width, fill, gap=6):
    """Draw a wrapped paragraph; returns the y below its last line."""
    for line in wrap_text(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += face.size + gap
    return y


def card(draw, box, accent):
    """White card with a thin border and a coloured top bar."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=WHITE, outline=CARD_LINE, width=2)
    draw.rectangle([x0, y0, x1, y0 + 8], fill=accent)


def sea_mines(draw, spots):
    """Little spiked naval mines floating on the water."""
    for mx, my in spots:
        draw.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=(30, 30, 30))
        for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12),
                       (-9, -9), (9, -9), (-9, 9), (9, 9)):
            draw.line([mx, my, mx + dx, my + dy], fill=(30, 30, 30), width=2)


# Layout grid (1024x1024, 48px side margins):
#   masthead 0-156, lead story 178-452, Ukraine band 478-648,
#   three columns 672-868, footer strip 892-976, credit line 990.
# The drawing is fully deterministic: same code, same bytes, every run.
def main():
    img = Image.new("RGB", CANVAS, PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, 1024, 150], fill=NAVY)
    d.rectangle([0, 150, 1024, 156], fill=GOLD)
    d.text((48, 18), "WEDNESDAY  \u2022  25 NOVEMBER 2026",
           font=SANS_BOLD(21), fill=GOLD)
    d.text((48, 52), "THE WORLD IN ONE DAY",
           font=SERIF_BOLD(52), fill=WHITE)
    # date badge, top right
    d.ellipse([852, 22, 976, 146], outline=GOLD, width=4)
    d.ellipse([870, 40, 958, 128], fill=TEAL)
    d.text((892, 58), "25", font=SERIF_BOLD(42), fill=WHITE)
    d.text((892, 102), "NOV", font=SANS_BOLD(17), fill=WHITE)

    # ---------- lead story ----------
    d.text((48, 178), "TOP STORY  \u2014  STRAIT OF HORMUZ  /  GULF",
           font=SANS_BOLD(19), fill=RED)
    d.text((48, 206), "MINES IN THE STRAIT",
           font=SERIF_BOLD(40), fill=INK)
    d.text((48, 258), "AS GULF WAR WIDENS",
           font=SERIF_BOLD(40), fill=INK)
    paragraph(d, 48, 328,
              "Iran says tankers hit mines in Hormuz. Houthis strike "
              "a Riyadh tower, wounding 11; the Saudi coalition hits "
              "Hodeidah.",
              SANS(22), 560, GREY, gap=5)

    # lead illustration: tanker, blast and mines on a strait
    d.rectangle([640, 178, 976, 452], fill=SEA)
    d.rectangle([640, 178, 976, 452], outline=NAVY, width=3)
    d.rectangle([640, 178, 976, 280], fill=SKY)
    cx, cy = 880, 235
    for r, col in ((48, (255, 190, 60)), (35, (255, 140, 40)),
                   (22, (255, 90, 30))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # tanker hull and superstructure
    d.polygon([(660, 345), (955, 345), (915, 395), (695, 395)],
              fill=(20, 30, 45))
    d.rectangle([700, 310, 830, 345], fill=(20, 30, 45))
    d.rectangle([745, 288, 775, 310], fill=(20, 30, 45))
    d.rectangle([850, 318, 905, 345], fill=(20, 30, 45))
    sea_mines(d, [(700, 415), (790, 425), (920, 412)])
    for wy in (400, 418):
        for wx in range(650, 970, 40):
            d.arc([wx, wy, wx + 36, wy + 18], start=180, end=360,
                  fill=WHITE, width=3)
    d.text((658, 425), "STRAIT OF HORMUZ", font=SANS_BOLD(17), fill=WHITE)

    # ---------- second story: Ukraine ----------
    d.rectangle([48, 478, 976, 648], fill=WHITE, outline=CARD_LINE, width=2)
    d.rectangle([48, 478, 58, 648], fill=RED)
    d.text((78, 494), "UKRAINE  \u2014  PUTIN VOWS RETALIATION",
           font=SANS_BOLD(19), fill=RED)
    paragraph(d, 78, 524,
              "Moscow vows payback for Kyiv's refinery strikes. Ukraine "
              "claims a Baltic ship hit; Latvia weighs closing its border.",
              SERIF_BOLD(27), 880, INK, gap=4)
    d.text((78, 612), "Norway pledges at least $7bn for Ukraine in 2027.",
           font=SANS(19), fill=FAINT)

    # ---------- three columns ----------
    columns = [
        ("AI SELL-OFF", RED,
         "Nvidia falls ~7% and the Nikkei drops 2.76% as doubts over "
         "the AI boom return; Nasdaq slides 2%."),
        ("DEMOCRATS TAKE HOUSE", NAVY2,
         "Democrats clinch at least 259 House seats \u2014 their biggest "
         "majority since 1990."),
        ("SPACE  \u2014  PAKISTAN", TEAL,
         "Pakistan's first astronaut reaches China's space station as "
         "Shenzhou-24 launches."),
    ]
    for i, (title, accent, body) in enumerate(columns):
        x = 48 + i * (288 + 24)
        card(d, [x, 672, x + 288, 868], accent)
        paragraph(d, x + 16, 694, title, SANS_BOLD(18), 288 - 32,
                  accent, gap=2)
        paragraph(d, x + 16, 736, body, SANS(19), 288 - 32, INK, gap=5)

    # ---------- footer strip ----------
    d.rectangle([48, 892, 976, 976], fill=NAVY)
    d.text((68, 908),
           "ALSO:  Cartagena hostages freed  \u2022  Senegal regains Africa Cup title",
           font=SANS_BOLD(20), fill=WHITE)
    d.text((68, 942),
           "Bangladesh raises textile wage 36%  \u2022  Dozens trapped in Indonesian mine",
           font=SANS(18), fill=(200, 215, 230))
    d.text((48, 990), "25 NOV 2026  \u2022  Summary of the day's world news",
           font=SANS(14), fill=(120, 120, 115))

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(f"saved {out} {img.size} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
