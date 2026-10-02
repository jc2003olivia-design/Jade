"""Make 4x6" Whatnot show cards as one PDF, one card per page.

Each card: run number and sale type, brand and item, the price to call,
original retail, what it sells for secondhand, what to say, and blank
lines to write the condition and measurements on. Black and white so it
prints on the thermal label printer.

Usage:
    python3 04-online-selling/whatnot-cards/make_cards.py cards.json -o cards.pdf

cards.json is a list like:
    [{"n": 1, "type": "FLASH SALE", "sku": "0910-03",
      "brand": "Free People", "item": "We The Free Fuji Thermal", "size": "XS",
      "price": "$22.40", "price_note": "full $28 · 20% off · 30 sec",
      "retail": "$68", "retail_src": "Poshmark sellers' tags",
      "resale": "$12–34, usually ~$22", "resale_src": "Poshmark sold, last 12 mo",
      "say": "Free People Fuji thermal, tag size XS ...",
      "tip": "Buyers search 'Fuji'. Say the style name."}]

Script / reminder cards use {"kind": "script", "head": "OPEN", "time": "0:00",
"title": "...", "say": "paragraph\\nparagraph", "checklist": [...], "tip": "..."}.
Any card can carry "run" (its place in the show) and "time" (shown top right).

Needs reportlab (pip install reportlab).
"""

import argparse
import json
from pathlib import Path

from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONTS = Path(__file__).resolve().parents[2] / "02-branding/whatnot-covers/fonts"
registerFont(TTFont("Bold", FONTS / "Montserrat-ExtraBold.ttf"))
registerFont(TTFont("Medium", FONTS / "Montserrat-Medium.ttf"))

W, H = 4 * inch, 6 * inch
M = 0.2 * inch
INNER = W - 2 * M


def wrap(text, font, size, width=INNER):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if stringWidth(trial, font, size) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def fit(text, font, largest, width=INNER, smallest=7):
    size = largest
    while size > smallest and stringWidth(text, font, size) > width:
        size -= 0.5
    return size


def label(c, x, y, text):
    c.setFont("Bold", 6.5)
    c.drawString(x, y, text.upper())


def draw_card(c, it):
    y = H - M

    # Header bar: run number + sale type, white on black.
    bar = 0.32 * inch
    c.setFillGray(0)
    c.rect(M, y - bar, INNER, bar, stroke=0, fill=1)
    c.setFillGray(1)
    right = it.get("time") or it.get("sku") or ""
    room = INNER - 16 - stringWidth(right, "Medium", 9)
    head = f"#{it['n']}  {it['type']}"
    if it.get("run"):
        head = f"{it['run']}.  " + head
    c.setFont("Bold", fit(head, "Bold", 13, room))
    c.drawString(M + 6, y - bar + 7, head)
    c.setFont("Medium", 9)
    c.drawRightString(W - M - 6, y - bar + 8, right)
    c.setFillGray(0)
    y -= bar + 4

    # Brand, then item + size.
    size = fit(it["brand"], "Bold", 22)
    y -= size
    c.setFont("Bold", size)
    c.drawString(M, y, it["brand"])
    line = f"{it['item']} · {it['size']}"
    if it.get("time") and it.get("sku"):
        line += f" · {it['sku']}"
    size = fit(line, "Medium", 12)
    y -= size + 3
    c.setFont("Medium", size)
    c.drawString(M, y, line)

    # Price to call.
    y -= 8
    box = 0.5 * inch
    c.setLineWidth(2)
    c.rect(M, y - box, INNER, box)
    c.setFont("Bold", 26)
    c.drawString(M + 8, y - box + 11, it["price"])
    px = M + 14 + stringWidth(it["price"], "Bold", 26)
    note_lines = wrap(it.get("price_note", ""), "Medium", 8.5, W - M - 6 - px)
    ny = y - box / 2 + (len(note_lines) - 1) * 5 - 3
    c.setFont("Medium", 8.5)
    for nl in note_lines:
        c.drawString(px, ny, nl)
        ny -= 10
    y -= box + 6

    # Retail | secondhand, side by side.
    half = (INNER - 6) / 2
    top = y
    for i, (key, head) in enumerate((("retail", "Original retail"),
                                     ("resale", "Sells secondhand"))):
        x = M + i * (half + 6)
        yy = top - 7
        label(c, x, yy, head)
        vs = 12
        lines = wrap(it[key], "Bold", vs, half)
        while len(lines) > 2 and vs > 8:
            vs -= 0.5
            lines = wrap(it[key], "Bold", vs, half)
        c.setFont("Bold", vs)
        for ln in lines:
            yy -= vs + 2
            c.drawString(x, yy, ln)
        c.setFont("Medium", 6.5)
        for ln in wrap(it[key + "_src"], "Medium", 6.5, half):
            yy -= 8
            c.drawString(x, yy, ln)
        y = min(y, yy)
    y -= 8
    c.setLineWidth(1)
    c.line(M, y, W - M, y)

    # Write-in lines, reserved at the bottom.
    foot_h = 0.95 * inch
    tip_lines = wrap("TIP: " + it["tip"], "Medium", 7.5) if it.get("tip") else []
    foot_h += len(tip_lines) * 9.5

    # What to say: as large as fits the space left.
    y -= 9
    label(c, M, y, "Say")
    room = y - 4 - (M + foot_h)
    for size in [x / 2 for x in range(26, 15, -1)]:
        lines = wrap(it["say"], "Medium", size)
        lead = size * 1.28
        if len(lines) * lead <= room:
            break
    c.setFont("Medium", size)
    y -= 4
    for ln in lines:
        y -= lead
        c.drawString(M, y, ln)

    # Footer: write-in lines, then the tip.
    y = M + foot_h - 4
    c.setLineWidth(0.6)
    c.line(M, y + 2, W - M, y + 2)
    for left, right in (("Condition", "Flaws"),
                        ("Pit to pit", "Length"),
                        ("Waist", "Other")):
        y -= 18
        label(c, M, y + 2, left)
        c.line(M + 52, y, M + half, y)
        label(c, M + half + 6, y + 2, right)
        c.line(M + half + 46, y, W - M, y)
    y -= 6
    c.setFont("Medium", 7.5)
    for ln in tip_lines:
        y -= 9.5
        c.drawString(M, y, ln)


def draw_script(c, it):
    """A reminder / script card: header, title, what to say, a checklist."""
    y = H - M
    bar = 0.32 * inch
    c.setFillGray(0)
    c.rect(M, y - bar, INNER, bar, stroke=0, fill=1)
    c.setFillGray(1)
    right = it.get("time", "")
    head = (f"{it['run']}.  " if it.get("run") else "") + it["head"]
    c.setFont("Bold", fit(head, "Bold", 13, INNER - 16 - stringWidth(right, "Medium", 9)))
    c.drawString(M + 6, y - bar + 7, head)
    c.setFont("Medium", 9)
    c.drawRightString(W - M - 6, y - bar + 8, right)
    c.setFillGray(0)
    y -= bar + 4

    size = fit(it["title"], "Bold", 22)
    y -= size
    c.setFont("Bold", size)
    c.drawString(M, y, it["title"])
    y -= 8
    c.setLineWidth(1)
    c.line(M, y, W - M, y)

    tip_lines = wrap("TIP: " + it["tip"], "Medium", 7.5) if it.get("tip") else []
    bottom = M + len(tip_lines) * 9.5 + (8 if tip_lines else 0)
    paras = [p for p in it.get("say", "").split("\n") if p.strip()]
    checks = it.get("checklist", [])

    def layout(sz):
        lead, csz = sz * 1.28, sz * 0.82
        out, h = [], 0
        if paras:
            h += 13
            for p in paras:
                ls = wrap(p, "Medium", sz)
                out.append(("p", ls))
                h += len(ls) * lead + sz * 0.45
        if checks:
            h += 15
            for ch in checks:
                ls = wrap(ch, "Medium", csz, INNER - 14)
                out.append(("c", ls))
                h += len(ls) * csz * 1.28 + 3
        return out, h, lead, csz

    for sz in [x / 2 for x in range(28, 13, -1)]:
        out, h, lead, csz = layout(sz)
        if h <= y - bottom:
            break
    first_c = True
    if paras:
        y -= 9
        label(c, M, y, it.get("say_label", "Say"))
        y -= 4
    for kind, ls in out:
        if kind == "p":
            c.setFont("Medium", sz)
            for ln in ls:
                y -= lead
                c.drawString(M, y, ln)
            y -= sz * 0.45
        else:
            if first_c:
                y -= 11
                label(c, M, y, it.get("check_label", "Do"))
                y -= 2
                first_c = False
            c.setFont("Medium", csz)
            for i, ln in enumerate(ls):
                y -= csz * 1.28
                if i == 0:
                    c.setLineWidth(0.8)
                    c.rect(M, y - 1, csz * 0.75, csz * 0.75)
                c.drawString(M + 14, y, ln)
            y -= 3

    y = bottom - 4
    c.setFont("Medium", 7.5)
    for ln in tip_lines:
        c.drawString(M, y, ln)
        y -= 9.5


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("cards", help="JSON file of cards")
    parser.add_argument("-o", "--out", required=True, help="PDF to write")
    args = parser.parse_args()

    cards = json.loads(Path(args.cards).read_text())
    c = canvas.Canvas(args.out, pagesize=(W, H))
    c.setTitle("Whatnot show cards")
    for it in cards:
        (draw_script if it.get("kind") == "script" else draw_card)(c, it)
        c.showPage()
    c.save()
    print(f"{len(cards)} cards -> {args.out}")


if __name__ == "__main__":
    main()
