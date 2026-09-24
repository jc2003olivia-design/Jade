# Whatnot Cover Photos

Show thumbnails for KennyShop. Every cover shows **$1 STARTS**.

## Research: what gets people to click
- **The thumbnail matters more than anything else.** Sellers report 2–3x more clicks just from changing the thumbnail.
- **Put a real person in it.** A good photo of you with a color block and your logo does better than a flat-lay, and it's how people start recognizing you.
- **Say the price.** "$1 starts" gives people a reason to tap in, much more than a vague "Sunday live."
- **High contrast, 2–3 colors, same layout every time.** Keep the logo in the same corner so regulars spot you in the feed.
- **It has to read at phone size.** In the feed the card is about 180px wide, so only the category name and $1 are big. The brand list is small print for people who look closer.
- **Size:** portrait 3:4, 1080 × 1440. Keep the text away from the very bottom and the edges, and check the crop in Whatnot's preview before going live. (A page banner is 750 × 424 if you ever need one.)

## Current style: "sticker story" (based on Jade's own past covers)
A full-bleed, real photo, with brand logos as white sticker tiles scattered around the photo at slight tilts (6 max, never over the face or outfit) and rounded "pill" text stickers. One font (Fredoka) and one pill style, so the covers look like a set.

- **Top-right:** **$1 STARTS** (biggest, pink) and **10 SEC SD** (sudden death), placed over open background so they never cover the outfit.
- **Bottom-right:** category, KENNYSHOP, and LIVE day/time.
- **6 logos per cover, max.** More than that turns to noise at feed size.

| Cover | Photo | Logos (`logos/<name>.png`) |
|---|---|---|
| `out/contemporary.png` (Premium Contemporary, live Fri 7 PM EST) | `photos/contemporary-orange-mirror.jpg` | anthropologie, free-people, aritzia, skims, polo (Ralph Lauren) ✓ · revolve still needed |
| `out/activewear.png` | *needed: an activewear photo* | alo, lululemon, fp-movement, nike, white-fox, patagonia |

Any logo file that isn't in `logos/` yet shows as a typed placeholder tile. The activewear LIVE pill still needs its day and time.

## Shot list (take these on your phone, vertical)
No filters and no beauty mode. Stand near a big window with daylight hitting your face, or shoot outside in shade/golden hour. Leave open space (sky, wall) on the upper right: that is where $1 STARTS goes.

**Premium Activewear**, in a matching set (Alo or Lululemon read best):
1. Mid-thigh up, smiling at the camera, one hand holding a folded item or a hanger.
2. Full body, mid-step or walking toward the camera, relaxed and not posed.
3. Seated on a bench/step, laughing, with a rack of activewear behind you.
4. Holding up one hero piece (Alo jacket, Lulu Define) next to your face.

**Premium Contemporary**, in a Free People/Aritzia/Skims outfit:
5. Waist up, soft smile, warm-toned wall or plants behind you.
6. By the clothing rack, flipping through hangers and looking over your shoulder at the camera.
7. Full body with a coffee or tote, a relaxed "outfit of the day" shot.

Plain backgrounds (white wall, rack, outdoors) beat busy rooms.

## How to make the final PNGs
Put the photos in `photos/`, then run:
```
node render.mjs photos/contemporary-denim-dress.jpg photos/<activewear-photo>.jpg
``` The PNGs go to `out/`. This needs `playwright-core` installed (`npm i playwright-core`).
