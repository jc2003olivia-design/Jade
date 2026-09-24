"""Build the two Whatnot show cover mockups (1080x1920).

Run:  python3 make_covers.py
Makes a PNG per show plus a preview sheet showing both at phone-feed size
with the safe zone marked. The grey figure is a placeholder: swap in a
waist-up photo of you wearing the hero piece (in Canva, or edit PHOTO below).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
W, H = 1080, 1920
# Keep everything important inside this box: Whatnot crops the edges.
SAFE = (86, 192, 994, 1728)
PHOTO = None  # e.g. HERE / "me-activewear.jpg"

F = "/usr/share/fonts/truetype/"
SERIF_B = F + "liberation/LiberationSerif-Bold.ttf"
SANS_B = F + "dejavu/DejaVuSans-Bold.ttf"
SANS = F + "liberation/LiberationSans-Regular.ttf"

SHOWS = {
    "premium-contemporary": dict(
        bg="#1F2E4A", ink="#FFFFFF", accent="#F6D776", badge_ink="#1F2E4A",
        photo_bg="#1A273F", figure="#62718A",
        head_font=SERIF_B, head_scale=1.0, top="PREMIUM", main="CONTEMPORARY",
        brands="ARITZIA · FREE PEOPLE · REFORMATION", brand_font=F + "liberation/LiberationSans-Bold.ttf",
    ),
    "premium-activewear": dict(
        bg="#1F3FD1", ink="#FFFFFF", accent="#D4FF3A", badge_ink="#1F3FD1",
        photo_bg="#1A35B1", figure="#6278DF",
        head_font=SANS_B, head_scale=0.78, top="PREMIUM", main="ACTIVEWEAR",
        brands="LULULEMON · ALO · VUORI", brand_font=SANS_B,
    ),
}


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
    if PHOTO and Path(PHOTO).exists():
        ph = Image.open(PHOTO).convert("RGBA")
        bw, bh = x1 - x0, y1 - y0
        r = max(bw / ph.width, bh / ph.height)
        ph = ph.resize((int(ph.width * r), int(ph.height * r)), Image.LANCZOS)
        ph = ph.crop(((ph.width - bw) // 2, (ph.height - bh) // 2,
                      (ph.width - bw) // 2 + bw, (ph.height - bh) // 2 + bh))
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
    big = text_img("$1", SANS_B, 150, s["badge_ink"])
    small = text_img("STARTS", SANS_B, 44, s["badge_ink"], spacing=6)
    total = big.height + 18 + small.height
    y = cy - total // 2
    canvas.alpha_composite(big, (cx - big.width // 2, y))
    canvas.alpha_composite(small, (cx - small.width // 2, y + big.height + 18))


def build(name, s, out=None):
    c = Image.new("RGBA", (W, H), s["bg"])
    sx0, sy0, sx1, sy1 = SAFE
    inner = sx1 - sx0 - 40
    y = sy0 + 40
    y = paste_center(c, text_img("KURATED BY KENNY", SANS_B, 34, s.get("logo", s["accent"]), spacing=10), y) + 40
    y = paste_center(c, text_img(s["top"], s["head_font"], 64, s["ink"], s["head_scale"], spacing=18), y) + 22
    y = paste_center(c, fit_text(s["main"], s["head_font"], inner, 180, s["ink"], s["head_scale"]), y) + 50
    photo_box = (sx0 + 40, y, sx1 - 40, sy1 - 190)
    draw_photo(c, s, photo_box)
    badge(c, s, photo_box[2] - 175, photo_box[1] + 185, 145)
    d = ImageDraw.Draw(c)
    ly = sy1 - 150
    d.line((sx0 + 160, ly, sx1 - 160, ly), fill=s["accent"], width=4)
    paste_center(c, fit_text(s["brands"], s["brand_font"], inner, 52, s["ink"], spacing=3), ly + 36)
    out = out or HERE / f"{name}.png"
    c.convert("RGB").save(out, optimize=True)
    return c


def preview(covers):
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
    sheet.save(HERE / "preview-feed-size.png", optimize=True)


if __name__ == "__main__":
    covers = {n: build(n, s) for n, s in SHOWS.items()}
    preview(covers)
    print("done:", ", ".join(covers))
