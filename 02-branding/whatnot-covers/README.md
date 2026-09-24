# Whatnot Cover Photos

Show thumbnails for KennyShop. Every cover shows **$1 STARTS**.

## Research: what gets people to click
- **The thumbnail matters more than anything else.** Sellers report 2–3x more clicks just from changing the thumbnail.
- **Put a real person in it.** A good photo of you with a color block and your logo does better than a flat-lay, and it's how people start recognizing you.
- **Say the price.** "$1 starts" gives people a reason to tap in, much more than a vague "Sunday live."
- **High contrast, 2–3 colors, same layout every time.** Keep the logo in the same corner so regulars spot you in the feed.
- **It has to read at phone size.** In the feed the card is about 180px wide, so only the category name and $1 are big. The brand list is small print for people who look closer.
- **Size:** portrait 3:4, 1080 × 1440. Keep the text away from the very bottom and the edges, and check the crop in Whatnot's preview before going live. (A page banner is 750 × 424 if you ever need one.)

## The cover template
Every cover has the same look. Only the photo, the category and 3 brands change.

**Fixed on every cover**
- **$1 STARTS**: top-right, big and hot pink.
- **100+ ITEMS**: the hot-pink pill under it.
- **Bottom-right:** the category (PREMIUM CONTEMPORARY / PREMIUM ACTIVEWEAR), then KENNYSHOP, then the live time.
- Hot pink `#ff2d6f`, white, black, Fredoka font. 1080 × 1440.

**Changes each time**
- **Photo:** one of me, or an item flat-lay.
  - Tall photos fill the cover.
  - Square or wide photos (like flat-lays) show the whole item, and the photo's own background extends above and below.
- **3 brands:** big logo stickers in a zigzag: top-left, middle-right, lower-left.

### How to ask for a new cover
Send: **the photo + the category (contemporary or activewear) + 3 brands.**

### How to make one
```
node make-cover.mjs --category contemporary --photo photos/x.jpg \
  --brands free-people,anthropologie,aritzia --out out/2026-10-03-contemporary.png
```
Options:
- `--live "LIVE FRIDAY 7 PM EST"`: change the live line. Contemporary defaults to Friday 7 PM EST.
- `--fit fill|whole`: force a photo mode. It's automatic by default.
- `--pos "center 40%"` / `--zoom 118%`: frame a filled photo.
- `--nudge B:0,-80`: move sticker A, B or C by x,y pixels if it covers something.

It needs `playwright-core` (`npm i playwright-core`).

**Examples:** `out/example-contemporary-wethefree.png` (flat-lay), `out/example-contemporary-denim.png` (photo of me).

### Logos (`logos/<name>.png`)
- **Saved:** anthropologie, free-people, aritzia, skims, polo (Ralph Lauren).
- **Still needed:** revolve, alo, lululemon, fp-movement, nike, white-fox, patagonia. Until they're added, these show as typed stickers.
- Logos on a black background automatically get a black sticker.

## Shot list (take these on your phone, vertical)
No filters and no beauty mode. Stand near a big window with daylight hitting your face, or shoot outside in shade/golden hour. Leave open space (sky, wall) on the upper right: that is where $1 STARTS goes. Flat-lays on a plain background work too.

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
