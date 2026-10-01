"""Build the Whatnot show cover mockups (1080x1920).

Run:  python3 make_covers.py
Makes a PNG per show plus a preview sheet showing them at phone-feed size
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
SERIF = str(FONTS / "PlayfairDisplay-Regular.ttf")
SERIF_I = str(FONTS / "PlayfairDisplay-Italic.ttf")  # variable: pick a weight with variation=

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
# Second Premium Contemporary cover: same look, new photo and brands, no fall line.
SHOWS["premium-contemporary-2"] = dict(
    SHOWS["premium-contemporary"], footer=None, template=False,
    brands=["FREE PEOPLE", "ANTHROPOLOGIE", "ARITZIA"],
    photo=HERE / "photos" / "contemporary-2.webp", crop=(160, 0, 939, 900),
)
# Premium Activewear, full-frame: the photo fills the top and melts into the blue,
# title and $1 badge below (bright version of the cover-photo format).
SHOWS["premium-activewear-2"] = dict(
    SHOWS["premium-activewear"], layout="full", template=False,
    # cherry + blush: warmer than pool blue, picks up the red top and lip color
    bg="#B0122F", ink="#FFFFFF", accent="#FFC9D3", badge_ink="#B0122F", logo="#FFFFFF",
    photo=HERE / "photos" / "activewear-friends.jpg", photo_y=150, badge_at=(250, 1090),
    lift=dict(brightness=1.1, contrast=1.08, color=1.12, sharpness=1.15),
)
# The Mini Edit (kids): full-frame photo, background blurred beforehand
# (photos/kids-mini-edit-blur.jpg), $1 badge over the blurred table on the right.
SHOWS["the-mini-edit"] = dict(
    layout="full", template=False,
    # butter + blue: cheerful, picks up the blue sweater
    bg="#F8D66D", ink="#1E3F9A", accent="#2E5BC9", badge_ink="#FFFFFF", logo="#FFFFFF",
    head_font=DISPLAY, head_scale=1.0, badge_font=DISPLAY, top="THE", main="MINI EDIT",
    brands=["HANNA ANDERSSON", "ZARA KIDS", "DESIGNER"], brand_font=SANS_B, brand_text=0.58,
    photo=HERE / "photos" / "kids-mini-edit-blur.jpg", photo_y=150, badge_at=(860, 800),
    lift=dict(brightness=1.08, contrast=1.06, color=1.1, sharpness=1.1),
)
# The Elevated Edit: the luxe look (champagne gold on a full-bleed, brightened photo).
SHOWS["the-elevated-edit"] = dict(
    style="luxe", layout="full", bg="#1E1712", bg_edge="#080706", ink="#FFFFFF", band="#0B0908",
    accent="#EBCB8B", gold=("#C29A5B", "#F6E2AE", "#FFF6DC", "#D9B271"), badge_ink="#1A140F",
    photo_bg="#211A15", figure="#3A3029", top="THE", main="Elevated", last="EDIT",
    brands=["ANTHROPOLOGIE", "QUINCE", "FREE PEOPLE"], brand_font=SERIF, brand_spacing=10,
    start="$5", photo=HERE / "photos" / "elevated-edit.jpg", crop=None, warm=0.03, focus=(0.47, 0.30),
    lift=dict(brightness=1.18, contrast=1.1, color=1.15, sharpness=1.2),
)


def text_img(text, font_path, size, fill, x_scale=1.0, spacing=0, variation=None):
    """Render text to its own transparent image; x_scale < 1 condenses it."""
    font = ImageFont.truetype(font_path, size)
    if variation:
        font.set_variation_by_name(variation)
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
    return text_img(brand, s["brand_font"], int(height * s.get("brand_text", 0.5)), fill,
                    spacing=s.get("brand_spacing", 4))


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


def fit_photo(s, bw, bh):
    """The show's photo cropped (around "crop" if set) to fill a bw x bh slot."""
    ph = Image.open(s["photo"]).convert("RGBA")
    if s.get("crop"):
        # grow the crop box to the photo slot's shape, centered on it
        cx0, cy0, cx1, cy1 = s["crop"]
        cw, chh = cx1 - cx0, cy1 - cy0
        if cw / chh > bw / bh:
            chh = cw * bh / bw
        else:
            cw = chh * bw / bh
        mx, my = (cx0 + cx1) / 2, (cy0 + cy1) / 2
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
    return ph


def draw_photo(canvas, s, box):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(canvas)
    photo = s.get("photo")
    if photo and Path(photo).exists():
        bw, bh = x1 - x0, y1 - y0
        ph = fit_photo(s, bw, bh)
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


# --- luxe style (The Elevated Edit) ---------------------------------------

def gold_fill(im, s):
    """Swap a text/logo image's flat color for a diagonal champagne-gold sheen."""
    import numpy as np
    stops = np.array([Image.new("RGB", (1, 1), c).getpixel((0, 0)) for c in s["gold"]], float)
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w]
    pos = (xx / max(w - 1, 1) * 0.65 + yy / max(h - 1, 1) * 0.35) * (len(stops) - 1)
    k = np.clip(pos.astype(int), 0, len(stops) - 2)
    u = (pos - k)[..., None]
    rgb = stops[k] * (1 - u) + stops[k + 1] * u
    sheen = Image.fromarray(rgb.astype("uint8"), "RGB").convert("RGBA")
    sheen.putalpha(im.getchannel("A"))
    return sheen


def luxe_bg(s):
    """Espresso background, a touch lighter in the middle (soft spotlight)."""
    c = Image.new("RGBA", (W, H), s["bg_edge"])
    glow = Image.radial_gradient("L").resize((int(W * 1.6), int(H * 1.15)))
    glow = glow.point(lambda v: 255 - v)  # radial_gradient is dark in the center
    mid = Image.new("RGBA", glow.size, s["bg"])
    mid.putalpha(glow)
    c.alpha_composite(mid, ((W - glow.width) // 2, (H - glow.height) // 2))
    return c


def diamond(d, cx, cy, r, fill):
    d.polygon(((cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)), fill=fill)


def luxe_runner(c, s, y, start=0):
    """Dark band with double gold hairlines and gold logos, separated by diamonds."""
    d = ImageDraw.Draw(c)
    gold = s["accent"]
    d.rectangle((0, y, W, y + BAND), fill=s["band"])
    for ly in (y, y + 7, y + BAND - 8, y + BAND - 1):
        d.line((0, ly, W, ly), fill=gold, width=1 if ly in (y + 7, y + BAND - 8) else 2)
    room = BAND - 44
    items = []
    for br in s["brands"]:
        i = brand_img(br, 84, s, gold)
        if i.height > room:
            i = i.resize((int(i.width * room / i.height), room), Image.LANCZOS)
        f = logo_file(br)
        items.append((gold_fill(i, s), RUNNER_NUDGE.get(f.stem if f else "", 0)))
    items = items[start:] + items[:start]
    gap, dot = 46, 7
    x = 30
    cy = y + BAND // 2
    while x < W:
        for i, nudge in items:
            iy = y + (BAND - i.height) // 2 + nudge
            iy = max(y + 12, min(iy, y + BAND - i.height - 12))
            if x + i.width > 0 and x < W:
                c.alpha_composite(i, (x, iy))
            x += i.width + gap
            diamond(d, x + dot, cy, dot, gold)
            x += 2 * dot + gap


def arch_mask(w, h):
    """Arched-window shape: half-circle top, straight sides and bottom."""
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((0, 0, w - 1, w - 1), fill=255)
    d.rectangle((0, w // 2, w - 1, h - 1), fill=255)
    return m


def arch_outline(c, box, fill, width):
    x0, y0, x1, y1 = box
    w = x1 - x0
    d = ImageDraw.Draw(c)
    d.arc((x0, y0, x1, y0 + w), 180, 360, fill=fill, width=width)
    d.line((x0 + width // 2, y0 + w // 2, x0 + width // 2, y1), fill=fill, width=width)
    d.line((x1 - (width + 1) // 2, y0 + w // 2, x1 - (width + 1) // 2, y1), fill=fill, width=width)
    d.line((x0, y1 - width // 2, x1, y1 - width // 2), fill=fill, width=width)


def luxe_photo(c, s, box):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    slot = Image.new("RGBA", (bw, bh), s["photo_bg"])
    photo = s.get("photo")
    if photo and Path(photo).exists():
        slot = fit_photo(s, bw, bh)
    else:
        d = ImageDraw.Draw(slot)
        cx = bw // 2
        d.ellipse((cx - 105, 250, cx + 105, 490), fill=s["figure"])
        d.rounded_rectangle((cx - 240, 510, cx + 240, bh + 200), 180, fill=s["figure"])
        label = text_img("YOUR PHOTO HERE", SANS_B, 38, s["accent"], spacing=6)
        slot.alpha_composite(label, (cx - label.width // 2, bh - 150))
        sub = text_img("waist-up · wearing the hero piece · eye contact", SANS, 25, s["ink"])
        slot.alpha_composite(sub, (cx - sub.width // 2, bh - 92))
    c.paste(slot, (x0, y0), arch_mask(bw, bh))
    # fine gold frame floating just outside the photo
    g = 16
    arch_outline(c, (x0 - g, y0 - g, x1 + g, y1 + g), s["accent"], 2)


def luxe_badge(c, s, cx, cy, r):
    d = ImageDraw.Draw(c)
    d.ellipse((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), fill=s["bg"])
    d.ellipse((cx - r - 7, cy - r - 7, cx + r + 7, cy + r + 7), outline=s["accent"], width=2)
    disc = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill="#FFFFFF")
    c.alpha_composite(gold_fill(disc, s), (cx - r, cy - r))
    ring = r - 12
    d.ellipse((cx - ring, cy - ring, cx + ring, cy + ring), outline=s["badge_ink"], width=2)
    big = text_img(s["start"], SERIF_B, 124, s["badge_ink"])
    small = text_img("STARTS", SANS_B, 27, s["badge_ink"], spacing=7)
    total = big.height + 16 + small.height
    y = cy - total // 2 - 4
    c.alpha_composite(big, (cx - big.width // 2, y))
    c.alpha_composite(small, (cx - small.width // 2, y + big.height + 16))


def build_luxe(s):
    c = luxe_bg(s)
    sx0, sy0, sx1, sy1 = SAFE
    luxe_runner(c, s, sy0)
    luxe_runner(c, s, sy1 - BAND, start=1)
    y = sy0 + BAND + 34
    y = paste_center(c, text_img("KENNY SHOP", SANS_B, 30, s["accent"], spacing=14), y) + 34
    # THE / Elevated / — EDIT —
    the = text_img(s["top"], SERIF, 44, s["ink"], spacing=22)
    main = gold_fill(fit_text(s["main"], SERIF_I, sx1 - sx0 - 60, 210, "#FFFFFF"), s)
    edit = text_img(s["last"], SERIF, 64, s["ink"], spacing=30)
    y = paste_center(c, the, y) + 6
    y = paste_center(c, main, y) + 16
    d = ImageDraw.Draw(c)
    ey = y + edit.height // 2
    rule = 120
    ex0, ex1 = (W - edit.width) // 2, (W + edit.width) // 2
    d.line((ex0 - 40 - rule, ey, ex0 - 40, ey), fill=s["accent"], width=2)
    d.line((ex1 + 40, ey, ex1 + 40 + rule, ey), fill=s["accent"], width=2)
    diamond(d, ex0 - 40 - rule - 10, ey, 6, s["accent"])
    diamond(d, ex1 + 40 + rule + 10, ey, 6, s["accent"])
    y = paste_center(c, edit, y) + 56
    photo_box = (sx0 + 70, y, sx1 - 70, sy1 - BAND - 52)
    luxe_photo(c, s, photo_box)
    luxe_badge(c, s, photo_box[2] - 70, photo_box[1] + 330, 128)
    return c


def shade(c, y0, y1, a0, a1, color=(10, 8, 6)):
    """Dark see-through band fading from alpha a0 at y0 to a1 at y1, for text to read on a photo."""
    h = y1 - y0
    grad = Image.linear_gradient("L").resize((1, 256)).resize((W, h))
    grad = grad.point(lambda v: int(a0 + (a1 - a0) * v / 255))
    band = Image.new("RGBA", (W, h), color + (0,))
    band.putalpha(grad)
    c.alpha_composite(band, (0, y0))


def glow(im, radius=10, alpha=170):
    """Soft dark halo behind text so it holds up on a busy photo."""
    from PIL import ImageFilter
    pad = radius * 3
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = Image.new("L", out.size, 0)
    a.paste(im.getchannel("A"), (pad, pad))
    a = a.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: min(255, v * alpha // 100))
    out.putalpha(a)
    out.alpha_composite(im, (pad, pad))
    return out, pad


def full_photo(s):
    """The show photo filling the whole cover, brightened so it pops."""
    photo = s.get("photo")
    if not (photo and Path(photo).exists()):
        c = luxe_bg(s)
        d = ImageDraw.Draw(c)
        d.ellipse((W // 2 - 150, 520, W // 2 + 150, 880), fill=s["figure"])
        d.rounded_rectangle((W // 2 - 330, 910, W // 2 + 330, H + 300), 240, fill=s["figure"])
        label = text_img("YOUR PHOTO HERE · FULL FRAME", SANS_B, 34, s["accent"], spacing=5)
        c.alpha_composite(label, ((W - label.width) // 2, 1000))
        return c
    ph = Image.open(photo).convert("RGB")
    r = max(W / ph.width, H / ph.height) * s.get("zoom", 1.0)
    ph = ph.resize((int(ph.width * r), int(ph.height * r)), Image.LANCZOS)
    fx, fy = s.get("focus", (0.5, 0.5))
    x = min(max(int(ph.width * fx - W / 2), 0), ph.width - W)
    y = min(max(int(ph.height * fy - H * 0.35), 0), ph.height - H)
    ph = ph.crop((x, y, x + W, y + H))
    ph = lifted(ph, s)
    if s.get("warm"):
        ph = Image.blend(ph, Image.new("RGB", ph.size, (230, 160, 90)), s["warm"])
    return ph.convert("RGBA")


def build_luxe_full(s):
    """Magazine-cover layout: photo edge to edge, brand bands and title over it."""
    c = full_photo(s)
    sx0, sy0, sx1, sy1 = SAFE
    shade(c, 0, 560, 200, 0)
    shade(c, 1080, H, 0, 235)
    luxe_runner(c, s, sy0)
    luxe_runner(c, s, sy1 - BAND, start=1)
    k, pad = glow(text_img("KENNY SHOP", SANS_B, 32, s["accent"], spacing=14), 8, 220)
    c.alpha_composite(k, ((W - k.width) // 2, sy0 + BAND + 30 - pad))
    # title block sits on the lower third, just above the bottom band
    the = text_img(s["top"], SERIF, 50, s["ink"], spacing=24)
    main = gold_fill(fit_text(s["main"], SERIF_I, sx1 - sx0 - 40, 230, "#FFFFFF"), s)
    edit = text_img(s["last"], SERIF, 72, s["ink"], spacing=32)
    total = the.height + 8 + main.height + 18 + edit.height
    y = sy1 - BAND - 46 - total
    for im, gap in ((the, 8), (main, 18), (edit, 0)):
        g, pad = glow(im, 12, 160)
        c.alpha_composite(g, ((W - g.width) // 2, y - pad))
        if im is edit:
            d = ImageDraw.Draw(c)
            ey = y + edit.height // 2
            ex0, ex1, rule = (W - edit.width) // 2, (W + edit.width) // 2, 120
            d.line((ex0 - 40 - rule, ey, ex0 - 40, ey), fill=s["accent"], width=3)
            d.line((ex1 + 40, ey, ex1 + 40 + rule, ey), fill=s["accent"], width=3)
            diamond(d, ex0 - 40 - rule - 10, ey, 7, s["accent"])
            diamond(d, ex1 + 40 + rule + 10, ey, 7, s["accent"])
        y += im.height + gap
    bx, by = s.get("badge_at", (sx0 + 150, 720))
    luxe_badge(c, s, bx, by, 138)
    return c


def lifted(ph, s):
    """Brightness / contrast / color / sharpness boost from the show's "lift"."""
    lift = s.get("lift", {})
    for name, fn in (("brightness", ImageEnhance.Brightness), ("contrast", ImageEnhance.Contrast),
                     ("color", ImageEnhance.Color), ("sharpness", ImageEnhance.Sharpness)):
        if name in lift:
            ph = fn(ph).enhance(lift[name])
    return ph


def build_bright_full(s):
    """Full-width photo across the top, fading into the show color; title and badge over the fade."""
    c = Image.new("RGBA", (W, H), s["bg"])
    sx0, sy0, sx1, sy1 = SAFE
    ph = lifted(Image.open(s["photo"]).convert("RGB"), s).convert("RGBA")
    ph = ph.resize((W, int(ph.height * W / ph.width)), Image.LANCZOS)
    py = s.get("photo_y", 150)
    c.alpha_composite(ph, (0, py))
    rgb = Image.new("RGB", (1, 1), s["bg"]).getpixel((0, 0))
    fade_end = py + ph.height
    # melt the photo's edges into the show color: short at the top (under the runner),
    # longer at the bottom so the title sits on clean color
    c.paste(s["bg"], (0, 0, W, py))
    shade(c, py, sy0 + BAND, 255, 0, rgb)
    shade(c, fade_end - 470, fade_end - 150, 0, 255, rgb)
    c.paste(s["bg"], (0, fade_end - 150, W, H))
    runner(c, s, sy0)
    runner(c, s, sy1 - BAND, start=1)
    k, pad = glow(text_img("KENNY SHOP", SANS_B, 36, s.get("logo", s["accent"]), spacing=12), 8, 200)
    c.alpha_composite(k, ((W - k.width) // 2, sy0 + BAND + 28 - pad))
    top = text_img(s["top"], s["head_font"], 66, s["ink"], s["head_scale"], spacing=20)
    main = fit_text(s["main"], s["head_font"], sx1 - sx0 - 20, 200, s["ink"], s["head_scale"])
    y = sy1 - BAND - 40 - main.height - 14 - top.height
    light_ink = sum(Image.new("RGB", (1, 1), s["ink"]).getpixel((0, 0))) > 384
    for im, gap in ((top, 14), (main, 0)):
        # dark halo only helps light text; dark text sits on the clean color
        g, pad = glow(im, 14, 120) if light_ink else (im, 0)
        c.alpha_composite(g, ((W - g.width) // 2, y - pad))
        y += im.height + gap
    bx, by = s.get("badge_at", (sx0 + 150, 1000))
    badge(c, s, bx, by, 140)
    return c


def build(name, s, out=None):
    if s.get("style") == "luxe":
        made = build_luxe_full(s) if s.get("layout") == "full" else build_luxe(s)
        return save(name, s, made, out)
    if s.get("layout") == "full" and s.get("photo") and Path(s["photo"]).exists():
        return save(name, s, build_bright_full(s), out)
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
    return save(name, s, c, out)


def save(name, s, c, out=None):
    if out is None:
        final = s.get("photo") and Path(s["photo"]).exists()
        out = HERE / "final" / f"{name}.png" if final else HERE / f"{name}.png"
        out.parent.mkdir(exist_ok=True)
    c.convert("RGB").save(out, optimize=True)
    return c


def preview(covers, out="preview-feed-size.png"):
    """Every cover at feed-card size (270x480) with the safe zone dashed."""
    tw, th, pad = 270, 480, 40
    n = len(covers)
    sheet = Image.new("RGB", (pad * (n + 1) + tw * n, th + pad * 2 + 50), "#FFFFFF")
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
