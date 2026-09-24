"""Premium Contemporary live show cover (1080x1080).

Usage: python3 make_cover.py <photo> <out.jpg> <fonts_dir>
Fonts: Cormorant Garamond (+ Italic) and Montserrat variable TTFs from Google Fonts.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

photo_path, out_path, fonts = sys.argv[1], sys.argv[2], Path(sys.argv[3])

W = H = 1080
BG = (237, 229, 218)        # oatmeal
INK = (58, 46, 38)          # espresso
ACCENT = (176, 98, 66)      # terracotta
MUTED = (122, 104, 90)

def font(name, size, weight):
    f = ImageFont.truetype(str(fonts / name), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f

serif = lambda s, w=500: font("CormorantGaramond[wght].ttf", s, w)
serif_it = lambda s, w=500: font("CormorantGaramond-Italic[wght].ttf", s, w)
sans = lambda s, w=500: font("Montserrat[wght].ttf", s, w)

def tracked(draw, cx, y, text, f, fill, spacing):
    widths = [draw.textlength(c, font=f) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=f, fill=fill)
        x += w + spacing
    return total

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Thin inset frame
d.rectangle([28, 28, W - 29, H - 29], outline=(205, 190, 172), width=2)

# Header: LIVE pill + shop name
pill_f = sans(22, 700)
d.rounded_rectangle([W / 2 - 62, 62, W / 2 + 62, 102], radius=20, fill=ACCENT)
d.ellipse([W / 2 - 44, 76, W / 2 - 32, 88], fill=(255, 244, 236))
d.text((W / 2 + 10, 82), "LIVE", font=pill_f, fill=(255, 244, 236), anchor="mm")
tracked(d, W / 2, 118, "KURATED BY KENNY", sans(20, 500), MUTED, 7)

# Title
d.text((W / 2, 205), "Premium", font=serif_it(96, 500), fill=ACCENT, anchor="mm")
d.text((W / 2, 290), "CONTEMPORARY", font=serif(84, 600), fill=INK, anchor="mm")

# Arched photo
aw, ah = 520, 560
ax, ay = (W - aw) // 2, 352
photo = Image.open(photo_path).convert("RGB")
# Zoom in so the garment fills the arch
pw, ph = photo.size
photo = photo.crop((int(pw * 0.08), int(ph * 0.08), int(pw * 0.92), int(ph * 0.88)))
photo = ImageOps.fit(photo, (aw, ah), centering=(0.5, 0.5))
# Gentle warm tone to match the oatmeal palette
r, g, b = photo.split()
photo = Image.merge("RGB", (r.point(lambda v: min(255, v * 1.03)), g, b.point(lambda v: v * 0.96)))
mask = Image.new("L", (aw * 4, ah * 4), 0)
m = ImageDraw.Draw(mask)
m.ellipse([0, 0, aw * 4, aw * 4], fill=255)
m.rectangle([0, aw * 2, aw * 4, ah * 4], fill=255)
mask = mask.resize((aw, ah), Image.LANCZOS)

shadow = Image.new("L", (W, H), 0)
shadow.paste(mask, (ax + 10, ay + 14))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img = Image.composite(Image.new("RGB", (W, H), (200, 186, 168)), img, shadow.point(lambda v: v * 0.55))
img.paste(photo, (ax, ay), mask)
d = ImageDraw.Draw(img)
# arch outline offset
o = 16
d.arc([ax - o, ay - o, ax + aw + o, ay + aw + o], 180, 360, fill=ACCENT, width=2)
d.line([ax - o, ay + aw / 2, ax - o, ay + ah + o], fill=ACCENT, width=2)
d.line([ax + aw + o, ay + aw / 2, ax + aw + o, ay + ah + o], fill=ACCENT, width=2)
d.line([ax - o, ay + ah + o, ax + aw + o, ay + ah + o], fill=ACCENT, width=2)

# Brand row
bf = sans(26, 600)
brands = ["ANTHROPOLOGIE", "FREE PEOPLE", "LEVI'S"]
sp = 4
gap = 46
ws = [sum(d.textlength(c, font=bf) for c in b) + sp * (len(b) - 1) for b in brands]
total = sum(ws) + gap * (len(brands) - 1)
x = (W - total) / 2
by = 968
for i, (b, w) in enumerate(zip(brands, ws)):
    tracked(d, x + w / 2, by, b, bf, INK, sp)
    x += w
    if i < len(brands) - 1:
        d.ellipse([x + gap / 2 - 4, by + 12, x + gap / 2 + 4, by + 20], fill=ACCENT)
        x += gap

img.save(out_path, quality=95)
print("saved", out_path)
