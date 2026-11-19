#!/usr/bin/env python3
"""news-image-20261119 — Sum up 19 November 2026 world news in one image.

Entry for make.fun bounty news-image-20261119.

Writes a 1024x1024 PNG front page to <output>/entry.png (default /output,
overridable with MAKEFUN_OUTPUT_DIR / OUTPUT_DIR).

The image is rendered programmatically with Pillow from the fixed story data
below — no network, no downloaded assets, no randomness: two runs write
byte-identical files. Fonts are embedded in assets/fonts/ so rendering does
not depend on system fonts. If Pillow is unavailable, main() falls back to
copying the pre-rendered assets/entry.png (same bytes).

Stories (all reported on Thursday 19 November 2026):
  1. Donald Trump, Xi Jinping and Vladimir Putin meet in Shenzhen for
     the first-ever three-way summit; Xi hugged Trump on the tarmac.
     APEC opens in Shenzhen.
  2. Anthropic prices the biggest IPO in history: $81.3bn at $83 a
     share, about a $1.5 trillion valuation; shares debut on Nasdaq
     today under the ticker ANT.
  3. Grand Theft Auto VI rolls out worldwide after a 13-year wait;
     gamers enter Vice City.
  4. Israel launches a rare ground operation in central Gaza, tanks
     crossing the ceasefire's Yellow Line; displaced families flee.
  5. House Democrats nominate Hakeem Jeffries to be Speaker; he would
     be the first Black Speaker after the formal House vote on 3 Jan.
Also noted: Crimea bridge hit again; EU proposes a 45bn euro Ukraine
loan; Myanmar faces an ICJ genocide verdict; Cyclone Akvan nears India;
a Van Gogh sells for a record $190.4m. Markets (18 Nov close):
S&P 500 -0.23%, Nasdaq +0.42%, Brent $91.95, gold $3,742, VIX 24.49.

Sources: The New York Times, BBC, NPR/AP (via WHRO/NPR Illinois),
Bloomberg (via Longbridge/TradingView), Reuters (via The Voice),
Sky News, Just Security Early Edition — see SOURCES.md.
"""

import hashlib
import math
import os
import shutil
import sys

W, H = 1024, 1024
MX = 36                      # side margin
CW = W - 2 * MX              # content width = 952

PAPER = (250, 246, 238)      # warm newsprint
INK = (26, 26, 26)
NAVY = (20, 33, 61)
RED = (185, 28, 28)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONTS = os.path.join(ASSETS, "fonts")
PRE_RENDERED = os.path.join(ASSETS, "entry.png")


# ---------------------------------------------------------------- fonts
def font(name, size):
    path = os.path.join(FONTS, name)
    try:
        from PIL import ImageFont
        return ImageFont.truetype(path, size)
    except Exception:
        from PIL import ImageFont
        return ImageFont.load_default()


# ---------------------------------------------------------------- helpers
def star_points(cx, cy, r_out, r_in, n=5, rot=-90.0):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, names, sizes, max_w):
    """Largest font (from sizes, descending) in which text fits max_w."""
    for size in sizes:
        fnt = font(names, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
    return font(names, sizes[-1])


# ---------------------------------------------------------------- flags
def draw_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy, r = x + w * 0.16, y + h * 0.28, h * 0.24
    d.polygon(star_points(cx, cy, r, r * 0.42), fill=GOLD)
    for sx, sy in [(0.34, 0.10), (0.42, 0.22), (0.42, 0.38), (0.34, 0.50)]:
        r2 = h * 0.085
        d.polygon(star_points(x + w * sx, y + h * sy, r2, r2 * 0.42),
                  fill=GOLD)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_russia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_usa(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        col = (179, 25, 66) if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=col)
    cw, ch = w * 0.40, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(10, 49, 97))
    for row in range(5):
        for col in range(6):
            sx = x + cw * (col + 0.5) / 6.0
            sy = y + ch * (row + 0.5) / 5.0
            r = 2.5
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


# ---------------------------------------------------------------- icons
def rounded_tile(d, x, y, s, color):
    d.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=color)


def icon_chart(d, x, y, s):
    # rising bars + arrow
    base_y = y + 68
    bars = [(14, 26), (30, 40), (46, 54)]
    for bx, bh in bars:
        d.rectangle([x + bx, base_y - bh, x + bx + 12, base_y],
                    fill=WHITE)
    d.line([(x + 12, y + 52), (x + 30, y + 34), (x + 46, y + 40),
            (x + 70, y + 14)], fill=(255, 200, 60), width=5,
           joint="curve")
    d.polygon([(x + 70, y + 14), (x + 58, y + 16), (x + 68, y + 26)],
              fill=(255, 200, 60))


def icon_controller(d, x, y, s):
    # gamepad body
    d.rounded_rectangle([x + 8, y + 26, x + 80, y + 64], radius=16,
                        fill=WHITE)
    # d-pad (plus) on the left
    d.rectangle([x + 20, y + 36, x + 26, y + 54], fill=(26, 26, 26))
    d.rectangle([x + 15, y + 41, x + 31, y + 49], fill=(26, 26, 26))
    # four buttons on the right
    for bx, by in [(56, 36), (66, 44), (56, 52), (46, 44)]:
        d.ellipse([x + bx, y + by, x + bx + 7, y + by + 7],
                  fill=(185, 28, 28))
    # sticks
    d.ellipse([x + 36, y + 50, x + 44, y + 58], fill=(26, 26, 26))
    d.ellipse([x + 58, y + 30, x + 66, y + 38], fill=(26, 26, 26))


def icon_crossing(d, x, y, s):
    # dashed ceasefire line + arrow crossing it
    for i in range(6):
        x0 = x + 8 + i * 12
        d.line([x0, y + 48, x0 + 8, y + 48], fill=(255, 215, 0), width=4)
    d.line([(x + 18, y + 12), (x + 62, y + 66)], fill=WHITE, width=6,
           joint="curve")
    d.polygon([(x + 62, y + 66), (x + 48, y + 62), (x + 58, y + 50)],
              fill=WHITE)
    d.ellipse([x + 12, y + 6, x + 24, y + 18], outline=WHITE, width=4)


def icon_ballot(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=WHITE, width=5)
    d.line([cx - 16, cy, cx - 4, cy + 12, cx + 18, cy - 14],
           fill=WHITE, width=7, joint="curve")


# ---------------------------------------------------------------- render
def render():
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font("DejaVuSerif-Bold.ttf", 58)
    f_date = font("DejaVuSans-Bold.ttf", 21)
    f_kick = font("DejaVuSans-Bold.ttf", 20)
    f_lead = font("DejaVuSans-Bold.ttf", 46)
    f_sub = font("DejaVuSans.ttf", 23)
    f_head = font("DejaVuSans-Bold.ttf", 28)
    f_sum = font("DejaVuSans.ttf", 21)
    f_also = font("DejaVuSans.ttf", 19)
    f_mkt = font("DejaVuSans-Bold.ttf", 20)
    f_foot = font("DejaVuSans.ttf", 14)
    f_flag = font("DejaVuSans-Bold.ttf", 17)

    # ---- masthead
    d.text((W // 2, 26), "THE WORLD TODAY", font=f_mast, fill=NAVY,
           anchor="ma")
    d.text((W // 2, 94), "THURSDAY, 19 NOVEMBER 2026", font=f_date,
           fill=RED, anchor="ma")
    d.line([MX, 126, MX + CW, 126], fill=NAVY, width=3)
    d.line([MX, 132, MX + CW, 132], fill=NAVY, width=1)

    # ---- lead story
    y = 148
    d.text((MX, y), "TRILATERAL SUMMIT IN SHENZHEN  •  LEAD STORY",
           font=f_kick, fill=RED)
    y = 176
    lead_lines = ["TRUMP, XI AND PUTIN MEET",
                  "IN SHENZHEN TODAY"]
    for line in lead_lines:
        d.text((MX, y), line, font=f_lead, fill=INK)
        y += 56
    y = 292
    sub = ("Xi hugs Trump on the tarmac as the leaders gather for the "
           "first-ever three-way summit. APEC opens in Shenzhen.")
    for line in wrap(d, sub, f_sub, CW)[:2]:
        d.text((MX, y), line, font=f_sub, fill=INK)
        y += 30

    # ---- flag strip (drawn programmatically)
    fy = 366
    fw, fh = 220, 110
    gap = (CW - 3 * fw) // 2
    flags = [(draw_china, "CHINA"), (draw_russia, "RUSSIA"),
             (draw_usa, "UNITED STATES")]
    fx = MX
    for draw_fn, label in flags:
        draw_fn(d, fx, fy, fw, fh)
        d.text((fx + fw // 2, fy + fh + 8), label, font=f_flag,
               fill=INK, anchor="ma")
        fx += fw + gap

    # ---- divider
    d.line([MX, 514, MX + CW, 514], fill=NAVY, width=3)

    # ---- four story rows
    stories = [
        ("ANTHROPIC'S $81.3BN IPO IS THE BIGGEST EVER",
         "Claude's maker prices at $83 a share; shares debut on Nasdaq "
         "today under ANT, valued near $1.5 trillion.",
         (76, 29, 149), icon_chart),
        ("GRAND THEFT AUTO VI ROLLS OUT WORLDWIDE",
         "After a 13-year wait, gamers enter Vice City as the most "
         "anticipated game ever launches.",
         (13, 110, 71), icon_controller),
        ("ISRAEL LAUNCHES RARE GROUND OPERATION IN GAZA",
         "Tanks cross the ceasefire's Yellow Line in central Gaza; "
         "displaced families flee their tents.",
         (185, 28, 28), icon_crossing),
        ("DEMOCRATS NOMINATE JEFFRIES FOR SPEAKER",
         "House Democrats pick Jeffries, 56, as their leader; he would "
         "be the first Black Speaker after the Jan. 3 vote.",
         (37, 99, 235), icon_ballot),
    ]
    ry = 532
    tile = 88
    for headline, summary, color, icon in stories:
        rounded_tile(d, MX, ry, tile, color)
        icon(d, MX, ry, tile)
        tx = MX + tile + 16
        tw = CW - tile - 16
        hf = fit_font(d, headline, "DejaVuSans-Bold.ttf",
                      [28, 27, 26, 25, 24], tw)
        d.text((tx, ry + 2), headline, font=hf, fill=INK)
        sy = ry + 38
        for line in wrap(d, summary, f_sum, tw)[:2]:
            d.text((tx, sy), line, font=f_sum, fill=(60, 60, 60))
            sy += 26
        ry += 94

    # ---- also in the news
    also = ("ALSO:  Crimea bridge hit again  •  EU proposes €45bn "
            "Ukraine loan  •  Myanmar faces ICJ verdict  •  Cyclone "
            "Akvan nears India  •  Van Gogh sells for $190.4m")
    ay = 912
    for line in wrap(d, also, f_also, CW)[:2]:
        d.text((MX, ay), line, font=f_also, fill=GREY)
        ay += 24

    # ---- markets band
    d.rectangle([0, 962, W, 1000], fill=NAVY)
    mkt = ("MARKETS   S&P 500  −0.23%    Nasdaq  +0.42%    Brent $91.95    "
           "Gold $3,742    VIX 24.49")
    d.text((W // 2, 970), mkt, font=f_mkt, fill=WHITE, anchor="ma")

    # ---- footer
    d.text((W // 2, 1005), "A summary of world news — Thursday 19 November 2026",
           font=f_foot, fill=GREY, anchor="ma")

    return img


def main():
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.environ.get("OUTPUT_DIR") or "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    try:
        img = render()
        img.save(out_path, format="PNG")
    except Exception as exc:  # Pillow missing/broken: use pre-rendered
        print(f"render failed ({exc}); copying pre-rendered image",
              file=sys.stderr)
        if not os.path.exists(PRE_RENDERED):
            raise
        shutil.copyfile(PRE_RENDERED, out_path)

    with open(out_path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    size = os.path.getsize(out_path)
    print(f"wrote {out_path} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
