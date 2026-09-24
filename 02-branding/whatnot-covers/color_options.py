"""Side-by-side color options for each show, at phone-feed size.

Run:  python3 color_options.py   ->  options-contemporary.png, options-activewear.png
To use one: copy its colors into SHOWS in make_covers.py.
"""
from PIL import Image, ImageDraw, ImageFont
from make_covers import HERE, SHOWS, SANS, SANS_B, build


def shade(hex_, f):
    """f < 1 darkens, f > 1 lightens toward white."""
    r, g, b = (int(hex_[i:i + 2], 16) for i in (1, 3, 5))
    if f <= 1:
        c = [int(v * f) for v in (r, g, b)]
    else:
        c = [int(v + (255 - v) * (f - 1)) for v in (r, g, b)]
    return "#%02X%02X%02X" % tuple(c)


# name: (background, text, badge, badge text[, logo color if badge color is hard to read])
CONTEMPORARY = {
    "1 Navy + Butter": ("#1F2E4A", "#FFFFFF", "#F6D776", "#1F2E4A"),
    "2 Denim + Rust": ("#2F4A6D", "#F5EFE6", "#C8693A", "#F5EFE6"),
    "3 Chocolate + Butter": ("#4A2E23", "#FFF6D6", "#F2D675", "#4A2E23"),
    "4 Burgundy + Blush": ("#6B1E2E", "#FBE9EC", "#F4A7B9", "#6B1E2E"),
    "5 Sage + Terracotta": ("#A3B18A", "#1F2A1C", "#B85C38", "#FFFFFF"),
    "6 Espresso + Pink": ("#2B1E1A", "#F6E7DF", "#E8B4B0", "#2B1E1A"),
}
ACTIVEWEAR = {
    "1 Pool Blue + Hot Pink": ("#16A5DD", "#FFFFFF", "#FF3D8B", "#FFFFFF", "#FFFFFF"),
    "2 Cobalt + Neon Lime": ("#1F3FD1", "#FFFFFF", "#D4FF3A", "#1F3FD1"),
    "3 Hot Pink + Red": ("#FF4FA3", "#FFFFFF", "#E0112B", "#FFFFFF", "#FFFFFF"),
    "4 Lavender + Orange": ("#B9A6F2", "#1B1B3A", "#FF6A2B", "#FFFFFF"),
    "5 Teal + Coral": ("#0F9E94", "#FFFFFF", "#FF7A66", "#FFFFFF"),
    "6 Black + Neon Lime": ("#111111", "#FFFFFF", "#C6FF3D", "#111111"),
}


def sheet(show, options, out):
    base = SHOWS[show]
    tw, th, pad, cols = 300, 533, 36, 3
    rows = (len(options) + cols - 1) // cols
    im = Image.new("RGB", (pad + cols * (tw + pad), pad + rows * (th + 64)), "#FFFFFF")
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(SANS_B, 20)
    fs = ImageFont.truetype(SANS, 15)
    for i, (label, (bg, ink, badge, badge_ink, *logo)) in enumerate(options.items()):
        dark = sum(int(bg[j:j + 2], 16) for j in (1, 3, 5)) < 384
        s = dict(base, bg=bg, ink=ink, accent=badge, badge_ink=badge_ink, logo=(logo or [badge])[0],
                 photo_bg=shade(bg, 0.85 if dark else 0.9),
                 figure=shade(bg, 1.3) if dark else shade(bg, 0.75))
        cover = build(show, s, out=HERE / "_tmp.png")
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + 64)
        im.paste(cover.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 8), label, fill="#111111", font=f)
        d.text((x, y + th + 34), f"bg {bg} · text {ink} · badge {badge}", fill="#555555", font=fs)
    (HERE / "_tmp.png").unlink()
    im.save(HERE / out, optimize=True)


if __name__ == "__main__":
    sheet("premium-contemporary", CONTEMPORARY, "options-contemporary.png")
    sheet("premium-activewear", ACTIVEWEAR, "options-activewear.png")
    print("done")
