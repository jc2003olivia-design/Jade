"""Make 4x4" thermal SKU labels as one PDF, one label per page.

Each label: SKU in big bold type at the top, the item title under it,
then the date the item was first listed.

Usage:
    python3 06-label-printer/make_labels.py items.json -o labels.pdf

items.json is a list like:
    [{"sku": "0924-02",
      "title": "Nutmeg Tennessee Vols Crewneck Sweatshirt Seal Gray XL 90s",
      "listed": "2026-09-24T22:41:04.511Z"}]

"listed" can be a plain date (2026-09-24) or Nifty's createdAt timestamp,
which is converted to US Eastern time before the date is printed.

Needs reportlab (pip install reportlab).
"""

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONTS = Path(__file__).resolve().parent.parent / "02-branding/whatnot-covers/fonts"
registerFont(TTFont("Bold", FONTS / "Montserrat-ExtraBold.ttf"))
registerFont(TTFont("Medium", FONTS / "Montserrat-Medium.ttf"))

SIZE = 4 * inch
MARGIN = 0.25 * inch
WIDTH = SIZE - 2 * MARGIN
TZ = ZoneInfo("America/New_York")


def listed_date(value):
    if len(value) == 10:
        d = date.fromisoformat(value)
    else:
        d = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(TZ).date()
    return f"{d.month}/{d.day}/{d.year}"


def fit_size(text, font, largest, smallest=8):
    size = largest
    while size > smallest and stringWidth(text, font, size) > WIDTH:
        size -= 1
    return size


def wrap(text, font, size):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if stringWidth(trial, font, size) <= WIDTH or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def draw_label(c, item):
    top = SIZE - MARGIN

    # SKU: as big as fits the width, capped so long SKUs still sit well.
    sku = item["sku"]
    sku_size = fit_size(sku, "Bold", 64)
    y = top - sku_size * 0.8
    c.setFont("Bold", sku_size)
    c.drawCentredString(SIZE / 2, y, sku)

    y -= 0.18 * inch
    c.setLineWidth(3)
    c.line(MARGIN, y, SIZE - MARGIN, y)

    # Listing date sits at the bottom; the title fills the space between.
    date_size = 18
    date_y = MARGIN
    c.setFont("Medium", date_size)
    c.drawCentredString(SIZE / 2, date_y, f"Listed {listed_date(item['listed'])}")

    room = y - 0.2 * inch - (date_y + date_size + 0.2 * inch)
    for size in range(26, 9, -1):
        lines = wrap(item["title"], "Medium", size)
        leading = size * 1.25
        if len(lines) * leading <= room:
            break
    c.setFont("Medium", size)
    y -= 0.2 * inch + size
    for line in lines:
        c.drawCentredString(SIZE / 2, y, line)
        y -= leading


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("items", help="JSON file with sku, title, listed")
    parser.add_argument("-o", "--out", required=True, help="PDF to write")
    args = parser.parse_args()

    items = json.loads(Path(args.items).read_text())
    c = canvas.Canvas(args.out, pagesize=(SIZE, SIZE))
    c.setTitle("SKU labels")
    for item in items:
        draw_label(c, item)
        c.showPage()
    c.save()
    print(f"{len(items)} labels -> {args.out}")


if __name__ == "__main__":
    main()
