# Whatnot Cover Photos

Show thumbnails for Kurated by Kenny. Every cover shows **$1 STARTS**.

## Research: what gets people to click
- **The thumbnail matters more than anything else.** Sellers report 2–3x more clicks just from changing the thumbnail.
- **Put a real person in it.** A good photo of you with a color block and your logo does better than a flat-lay, and it's how people start recognizing you.
- **Say the price.** "$1 starts" gives people a reason to tap in, much more than a vague "Sunday live."
- **High contrast, 2–3 colors, same layout every time.** Keep the logo in the same corner so regulars spot you in the feed.
- **It has to read at phone size.** In the feed the card is about 180px wide, so only the category name and $1 are big. The brand list is small print for people who look closer.
- **Size:** portrait 3:4, 1080 × 1440. Keep the text away from the very bottom and the edges, and check the crop in Whatnot's preview before going live. (A page banner is 750 × 424 if you ever need one.)

## The 4 designs (`preview-all-4.png`)
| File | Category | Look |
|---|---|---|
| `aw-a` | Premium Activewear | Full-bleed photo, dark fade, lime $1 tag. Sporty, stands out most. |
| `aw-b` | Premium Activewear | Photo in a rounded frame, forest-green $1 sticker. Softer, "Alo" feel. |
| `mc-a` | Modern Contemporary | Magazine cover: serif title up top, burgundy $1 tag. |
| `mc-b` | Modern Contemporary | Photo over a cream band, burgundy $1 circle. Aritzia/Anthro feel. |

Colors: activewear = charcoal + lime (or forest green); contemporary = cream + burgundy + warm brown.

## Shot list (take these on your phone, vertical)
No filters and no beauty mode. Stand near a big window with daylight hitting your face, or shoot outside in shade/golden hour. Leave room above your head: the text sits at the **top** on mc-a and at the **bottom** on the others.

**Premium Activewear**, in a matching set (Alo or Lululemon read best):
1. Mid-thigh up, smiling at the camera, one hand holding a folded item or a hanger. *(aw-a)*
2. Full body, mid-step or walking toward the camera, relaxed and not posed. *(aw-a)*
3. Seated on a bench/step, laughing, with a rack of activewear behind you. *(aw-b)*
4. Holding up one hero piece (Alo jacket, Lulu Define) next to your face. *(aw-b)*

**Modern Contemporary**, in a Free People/Aritzia/Skims outfit:
5. Waist up, soft smile, warm-toned wall or plants behind you. *(mc-a)*
6. By the clothing rack, flipping through hangers and looking over your shoulder at the camera. *(mc-b)*
7. Full body with a coffee or tote, a relaxed "outfit of the day" shot. *(mc-a/mc-b)*

Plain backgrounds (white wall, rack, outdoors) beat busy rooms.

## How to make the final PNGs
Put the photos in `photos/`, then run:
```
node render.mjs photos/1.jpg photos/3.jpg photos/5.jpg photos/6.jpg
```
The order is aw-a, aw-b, mc-a, mc-b. The PNGs go to `out/`. This needs `playwright-core` installed (`npm i playwright-core`).
