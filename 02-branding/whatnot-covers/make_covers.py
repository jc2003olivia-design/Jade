"""Build the two Whatnot show cover mockups (1080x1920).

Run:  python3 make_covers.py
Makes a PNG per show plus a preview sheet showing both at phone-feed size
with the safe zone marked. With no photo, a grey figure stands in (the
template). Put a photo in photos/ and set "photo" + "crop" on a show to get
the finished cover in final/ (photos/ and final/ are kept out of git).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = Path(__file__).parent
W, H = 1080, 1920
# Keep everything important inside this box: Whatnot crops the edges.
SAFE = (86, 192, 994, 1728)

# Google fonts (SIL Open Font License, see fonts/OFL-*.txt)
FONTS = HERE / "fonts"
SERIF_B = str(FONTS / "PlayfairDisplay-Bold.ttf")
DISPLAY = str(FONTS / "Anton-Regular.ttf")
SANS_B = str(FONTS / "Montserrat-ExtraBold.ttf")
SANS = str(FONTS / "Montserrat-Medium.ttf")

SHOWS = {
    "premium-contemporary": dict(
        bg="#1F2E4A", ink="#FFFFFF", accent="#F6D776", badge_ink="#1F2E4A",
        photo_bg="#1A273F", figure="#62718A",
        head_font=SERIF_B, head_scale=1.0, top="PREMIUM", main="CONTEMPORARY",
        brands=["FREE PEOPLE", "POLO RALPH LAUREN", "PREMIUM DENIM"], footer="FALL THEMED",
        photo=HERE / "photos" / "contemporary-fall.jpg", crop=(215, 440, 865, 1270), brand_font=SANS_B,
    ),
    "premium-activewear": dict(
        # bright poolside blue + hot pink
        bg="#12B5EA", ink="#FFFFFF", accent="#FF3D8B", badge_ink="#FFFFFF", logo="#FFFFFF",
        photo_bg="#0F9CCB", figure="#6FD3F3",
        head_font=DISPLAY, head_scale=1.0, badge_font=DISPLAY, top="PREMIUM", main="ACTIVEWEAR",
        brands=["FREE PEOPLE MOVEMENT", "LULULEMON", "NIKE"], brand_font=SANS_B,
        photo=HERE / "photos" / "activewear-2.webp", crop=(200, 0, 1110, 1052),
    ),
}
# Third Premium Activewear cover: same look, new photo (mauve ribbed set).
SHOWS["premium-activewear-3"] = dict(
    SHOWS["premium-activewear"], template=False,
    photo=HERE / "photos" / "activewear-3.webp", crop=(150, 20, 798, 1160),
)
# Second Premium Contemporary cover: same look, new photo and brands, no fall line.
SHOWS["premium-contemporary-2"] = dict(
    SHOWS["premium-contemporary"], footer=None, template=False,
    brands=["FREE PEOPLE", "ANTHROPOLOGIE", "ARITZIA"],
    photo=HERE / "photos" / "contemporary-2.webp", crop=(160, 0, 939, 900),
)


def text_img(text, font_path, size, fill, x_scale=1.0, spacing=0):
    """Render text to its own transparent image; x_scale < 1 condenses it."""
    font = ImageFont.truetype(font_path, size)
    widths = [font.getlength(c) for c in text]
    w = int(sum(widths) + spacing * (len(text) - 1)) + 4
    asc, desc = font.getmetrics()
    im = Image.new("RGBA", (w, asc + desc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 0
    for c, cw in zip(text, widths):
        d.text((x, 0), c, font=font, fill=fill)
        x += cw + spacing
    bbox = im.getbbox()
    im = im.crop(bbox)
    if x_scale != 1.0:
        im = im.resize((max(1, int(im.width * x_scale)), im.height), Image.LANCZOS)
    return im


def logo_file(brand):
    """logos/<brand-slug>.png or .svg, e.g. logos/polo-ralph-lauren.png"""
    slug = brand.lower().replace(" ", "-")
    for ext in ("png", "svg"):
        f = HERE / "logos" / f"{slug}.{ext}"
        if f.exists():
            return f
    return None


def logo_img(path, height, fill):
    """Load a logo, trim it, recolor it to one flat color, scale to height."""
    if path.suffix == ".svg":
        import io
        import cairosvg
        png = cairosvg.svg2png(url=str(path), output_height=height * 6)
        im = Image.open(io.BytesIO(png)).convert("RGBA")
    else:
        im = Image.open(path).convert("RGBA")
    alpha = im.getchannel("A")
    if alpha.getextrema() == (255, 255):
        # no transparency: anything darker than the white background is logo
        alpha = im.convert("L").point(lambda v: 0 if v > 235 else min(255, (235 - v) * 4))
    im = im.crop(alpha.getbbox())
    alpha = alpha.crop(alpha.getbbox())
    flat = Image.new("RGBA", im.size, fill)
    flat.putalpha(alpha)
    return flat.resize((max(1, int(flat.width * height / flat.height)), height), Image.LANCZOS)


# some logos read smaller/larger than others at the same height
LOGO_SCALE = {"free-people-movement": 1.2, "lululemon": 1.15, "nike": 0.75,
              "free-people": 0.9, "polo-ralph-lauren": 1.6,
              "anthropologie": 0.4, "skims": 0.75, "ralph-lauren": 0.9}  # noqa


def brand_img(brand, height, s, fill=None):
    fill = fill or s["ink"]
    f = logo_file(brand)
    if f:
        return logo_img(f, int(height * LOGO_SCALE.get(f.stem, 1.0)), fill)
    # no logo file: bold wordmark sized to sit level with the logos
    return text_img(brand, s["brand_font"], int(height * 0.5), fill, spacing=4)


BAND = 140  # runner height
# nudge individual logos up (-) or down (+) inside the runner
RUNNER_NUDGE = {"free-people": -10, "polo-ralph-lauren": 8}


def runner(c, s, y, shift=0.0, start=0):
    """Edge-to-edge ticker band of the show's brands, repeating.

    The band runs off both sides on purpose; Whatnot's side crop only
    trims repeats. shift offsets the sequence so the two bands differ.
    """
    fill = s["badge_ink"]
    d = ImageDraw.Draw(c)
    d.rectangle((0, y, W, y + BAND), fill=s["accent"])
    room = BAND - 16
    items = []
    for br in s["brands"]:
        i = brand_img(br, 88, s, fill)
        if i.height > room:
            i = i.resize((int(i.width * room / i.height), room), Image.LANCZOS)
        f = logo_file(br)
        items.append((i, RUNNER_NUDGE.get(f.stem if f else "", 0)))
    items = items[start:] + items[:start]
    gap, dot = 44, 7
    period = sum(i.width for i, _ in items) + len(items) * (2 * gap + 2 * dot)
    x = 24 - int(period * shift)
    cy = y + BAND // 2
    while x < W:
        for i, nudge in items:
            iy = y + (BAND - i.height) // 2 + nudge
            iy = max(y + 2, min(iy, y + BAND - i.height - 2))
            if x + i.width > 0 and x < W:
                if x >= 0:
                    c.alpha_composite(i, (x, iy))
                else:
                    c.alpha_composite(i.crop((-x, 0, i.width, i.height)), (0, iy))
            x += i.width + gap
            d.ellipse((x, cy - dot, x + 2 * dot, cy + dot), fill=fill)
            x += 2 * dot + gap


def fit_text(text, font_path, max_w, start, fill, x_scale=1.0, spacing=0):
    size = start
    while True:
        im = text_img(text, font_path, size, fill, x_scale, spacing)
        if im.width <= max_w or size < 20:
            return im
        size -= 4


def paste_center(canvas, im, y):
    canvas.alpha_composite(im, ((W - im.width) // 2, y))
    return y + im.height


def draw_photo(canvas, s, box):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(canvas)
    photo = s.get("photo")
    if photo and Path(photo).exists():
        ph = Image.open(photo).convert("RGBA")
        bw, bh = x1 - x0, y1 - y0
        if s.get("crop"):
            # grow the crop box to the photo slot's shape, centered on it
            cx0, cy0, cx1, cy1 = s["crop"]
            cw, chh = cx1 - cx0, cy1 - cy0
            if cw / chh > bw / bh:
                chh = cw * bh / bw
            else:
                cw = chh * bw / bh
            mx, my = (cx0 + cx1) / 2, (cy0 + cy1) / 2
            pad = int(max(0, cw / 2 - mx, mx + cw / 2 - ph.width))
            if pad:
                # crop is wider than the photo: stretch the edge columns of
                # the plain backdrop out to the sides so the whole outfit fits
                wide = Image.new("RGBA", (ph.width + 2 * pad, ph.height))
                wide.paste(ph.crop((0, 0, 4, ph.height)).resize((pad, ph.height)), (0, 0))
                wide.paste(ph.crop((ph.width - 4, 0, ph.width, ph.height))
                           .resize((pad, ph.height)), (pad + ph.width, 0))
                wide.paste(ph, (pad, 0))
                ph, mx = wide, mx + pad
            ph = ph.crop((int(mx - cw / 2), int(my - chh / 2),
                          int(mx + cw / 2), int(my + chh / 2)))
        r = max(bw / ph.width, bh / ph.height)
        ph = ph.resize((int(ph.width * r), int(ph.height * r)), Image.LANCZOS)
        ph = ph.crop(((ph.width - bw) // 2, (ph.height - bh) // 2,
                      (ph.width - bw) // 2 + bw, (ph.height - bh) // 2 + bh))
        if s.get("warm"):
            # fall grade: a little less green/blue, amber wash
            ph = ImageEnhance.Color(ph).enhance(0.85)
            amber = Image.new("RGBA", ph.size, (214, 120, 50, 255))
            ph = Image.blend(ph, amber, s["warm"])
        mask = Image.new("L", ph.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw, bh), 36, fill=255)
        canvas.paste(ph, (x0, y0), mask)
        return
    d.rounded_rectangle(box, 36, fill=s["photo_bg"])
    cx = (x0 + x1) // 2
    # waist-up figure placeholder
    d.ellipse((cx - 110, y0 + 150, cx + 110, y0 + 400), fill=s["figure"])
    d.rounded_rectangle((cx - 250, y0 + 420, cx + 250, y1 + 60), 180, fill=s["figure"])
    d.rectangle((x0, y1 - 1, x1, y1 + 80), fill=s["bg"])  # clip figure bottom
    label = text_img("YOUR PHOTO HERE", SANS_B, 40, s["ink"], spacing=4)
    canvas.alpha_composite(label, (cx - label.width // 2, y1 - 150))
    sub = text_img("waist-up · wearing the hero piece · eye contact", SANS, 26, s["ink"])
    canvas.alpha_composite(sub, (cx - sub.width // 2, y1 - 90))


def badge(canvas, s, cx, cy, r):
    d = ImageDraw.Draw(canvas)
    d.ellipse((cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), fill=s["bg"])
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=s["accent"])
    big = text_img("$1", s.get("badge_font", SANS_B), 150, s["badge_ink"])
    small = text_img("STARTS", SANS_B, 44, s["badge_ink"], spacing=6)
    total = big.height + 18 + small.height
    y = cy - total // 2
    canvas.alpha_composite(big, (cx - big.width // 2, y))
    canvas.alpha_composite(small, (cx - small.width // 2, y + big.height + 18))


def build(name, s, out=None):
    c = Image.new("RGBA", (W, H), s["bg"])
    sx0, sy0, sx1, sy1 = SAFE
    inner = sx1 - sx0 - 40
    runner(c, s, sy0)
    runner(c, s, sy1 - BAND, start=1)
    y = sy0 + BAND + 34
    y = paste_center(c, text_img("KENNY SHOP", SANS_B, 38, s.get("logo", s["accent"]), spacing=10), y) + 34
    y = paste_center(c, text_img(s["top"], s["head_font"], 60, s["ink"], s["head_scale"], spacing=18), y) + 20
    y = paste_center(c, fit_text(s["main"], s["head_font"], inner, 170, s["ink"], s["head_scale"]), y) + 40
    footer = None
    if s.get("footer"):
        footer = text_img(s["footer"], SANS_B, 40, s["accent"], spacing=12)
    footer_h = footer.height + 52 if footer else 0
    photo_box = (sx0 + 40, y, sx1 - 40, sy1 - BAND - 36 - footer_h)
    draw_photo(c, s, photo_box)
    badge(c, s, photo_box[2] - 175, photo_box[1] + 185, 145)
    if footer:
        fy = photo_box[3] + (sy1 - BAND - photo_box[3] - footer.height) // 2
        c.alpha_composite(footer, ((W - footer.width) // 2, fy))
    if out is None:
        final = s.get("photo") and Path(s["photo"]).exists()
        out = HERE / "final" / f"{name}.png" if final else HERE / f"{name}.png"
        out.parent.mkdir(exist_ok=True)
    c.convert("RGB").save(out, optimize=True)
    return c


def preview(covers, out="preview-feed-size.png"):
    """Both covers at feed-card size (270x480) with the safe zone dashed."""
    tw, th, pad = 270, 480, 40
    sheet = Image.new("RGB", (pad * 3 + tw * 2, th + pad * 2 + 50), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    k = tw / W
    for i, (name, c) in enumerate(covers.items()):
        x = pad + i * (tw + pad)
        sheet.paste(c.convert("RGB").resize((tw, th), Image.LANCZOS), (x, pad))
        sx0, sy0, sx1, sy1 = [int(v * k) for v in SAFE]
        for a, b in (((sx0, sy0), (sx1, sy0)), ((sx0, sy1), (sx1, sy1)),
                     ((sx0, sy0), (sx0, sy1)), ((sx1, sy0), (sx1, sy1))):
            n = 24
            for j in range(0, n, 2):
                p = (x + a[0] + (b[0] - a[0]) * j / n, pad + a[1] + (b[1] - a[1]) * j / n)
                q = (x + a[0] + (b[0] - a[0]) * (j + 1) / n, pad + a[1] + (b[1] - a[1]) * (j + 1) / n)
                d.line((p, q), fill="#FF3D8B", width=2)
        d.text((x, pad + th + 12), name, fill="#111111", font=ImageFont.truetype(SANS, 18))
    sheet.save(HERE / out, optimize=True)


if __name__ == "__main__":
    templates = {n: build(n, dict(s, photo=None)) for n, s in SHOWS.items() if s.get("template", True)}
    preview(templates)
    finals = {n: build(n, s) for n, s in SHOWS.items() if s.get("photo") and Path(s["photo"]).exists()}
    if finals:
        preview(finals, "final/preview-feed-size.png")
    covers = dict(templates, **finals)
    print("done:", ", ".join(covers))
