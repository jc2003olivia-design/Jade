# Thumbnail Maker

Whatnot show covers for the two $1-start series: **Premium Contemporary** and
**Premium Activewear**. Mockups are in `whatnot-covers/`.

## Specs
- Size: **1080 × 1920** (tall, 9:16).
- Whatnot crops the edges in the feed. Keep your face, text, badge and logo inside the
  **center safe zone**: about 86 px in from the sides and 192 px from the top and bottom
  (the pink dashed box in `whatnot-covers/preview-feed-size.png`).
- Before uploading, check it against Whatnot's official show thumbnail template and
  safe-zone checker (Seller Academy → Resources).

## What gets the most views
1. **Be in it.** Wear the best piece of the night and look at the camera. Faces with
   eye contact get noticeably more clicks than product-only shots (about 20–42% in
   thumbnail studies), and buyers want to see how it fits.
2. **One outfit, cropped tight.** A single focus beats a collage.
3. **3–6 words, bold, high contrast.** If it takes more than a glance to read, it's too much.
4. **No plain white backdrop.** It blends in and gets scrolled past.
5. **Say the category and brands.** The top $1 activewear shows lead with brand names
   ("$1 NWT LULULEMON, ALO & MORE").
6. **Same template every week.** Only swap the photo and the brand line, so repeat
   buyers recognize you in the feed.

## Style

### Shared layout (both shows)
Top to bottom, all inside the safe zone:
1. `KENNY SHOP`: small, spaced-out letters in the accent color
2. `PREMIUM` + show name: the big headline
3. Your photo: waist-up, wearing the hero piece, smiling at the camera (~60% of the frame)
4. `$1 STARTS`: a round badge by your shoulder
5. A thin accent line, then 2–3 brand logos, large and well spaced (wraps to 2 rows if needed)

### Premium Contemporary
- Background: navy, soft window light
- Colors: navy `#1F2E4A` · white `#FFFFFF` (headline, logos) · butter yellow `#F6D776` (Kenny Shop, $1 badge, "FALL THEMED")
- Fonts: elegant serif headline (Canva: Playfair Display or Bodoni), clean bold sans for brands
- Text: `PREMIUM CONTEMPORARY` · `$1 STARTS` · Free People + Polo Ralph Lauren logos · `PREMIUM DENIM` · `FALL THEMED` at the very bottom
- Outfit: one elevated piece, like a knit set, slip dress, or blazer + tailored trousers

### Premium Activewear: bold and high-energy
- Background: cobalt blue, bright even light
- Colors: cobalt `#1F3FD1` · white `#FFFFFF` (headline, brands) · neon lime `#D4FF3A` (logo + $1 badge, with cobalt text)
- Fonts: heavy condensed sans (Canva: Anton, Bebas Neue, or League Gothic)
- Text: `PREMIUM ACTIVEWEAR` · `$1 STARTS` · `FREE PEOPLE MOVEMENT · LULULEMON · NIKE` (add `NWT` if new with tags)
- Outfit: a matching set (Align, Define, Alo) in a color that pops against cobalt (white, black, pink, lime). Avoid blue sets.

## Templates
- Main cover photo (blank templates): `whatnot-covers/premium-contemporary.png`, `whatnot-covers/premium-activewear.png`
- Finished covers with your photos: `whatnot-covers/final/`. These and the photos in
  `whatnot-covers/photos/` stay on this computer only and are kept out of git, because the repo is public.
- Feed-size check: `whatnot-covers/preview-feed-size.png`
- Other color options considered: `whatnot-covers/options-contemporary.png`, `whatnot-covers/options-activewear.png`
- Bundle / lot photo:
- Sale / promo photo:

## Brand logos
- Logo files go in `whatnot-covers/logos/`, named after the brand: `nike.svg`,
  `lululemon.png`, `free-people.png`, `free-people-movement.png`, `polo-ralph-lauren.png`.
- PNG with a transparent background works best. A plain white background is OK too.
  Logos are recolored to the cover's text color automatically.
- If a brand has no logo file, its name shows as big bold text instead (like "DENIM").
- Have so far: Nike (Simple Icons), Lululemon (circle mark only; the wordmark is too small at cover size),
  Free People Movement (the file sent was cut off after "MOVEME", so the "NT" was redrawn to match),
  Free People, Polo Ralph Lauren.

## Photo shoot checklist
- [ ] Phone at chest height, vertical, back camera, wipe the lens
- [ ] Face a window, or use a ring light. No overhead-only light.
- [ ] Waist-up, leave headroom for the headline above you
- [ ] Look into the lens and smile. Take 10+ shots and pick the best.
- [ ] Hero piece steamed, tags tucked (or showing, if it's NWT)
- [ ] Leave space by one shoulder for the $1 badge

## Before every show
- [ ] Swap in tonight's top 2–3 brands
- [ ] Look at it at phone-feed size. Can you read it in 2 seconds?
- [ ] Nothing important outside the safe zone
- [ ] Track viewers per show. Test one change at a time (photo, color, brand line).

## Tools used
- Canva (free): rebuild the layout from the mockups with the fonts above
- `whatnot-covers/make_covers.py`: regenerates the covers. Put a photo in `photos/` and set its
  `photo` + `crop` on the show in `SHOWS`.

## Sources
- [Atlas: Whatnot Thumbnail Design Guide](https://www.atlasmktg.us/blog/whatnot-thumbnail-design-guide)
- [Whatnot Seller Academy: Go Live Guide](https://selleracademy.whatnot.com/guide/) · [Resources](https://selleracademy.whatnot.com/resources)
- [Whatnot thumbnail size discussion (1080×1920, center crop)](https://www.facebook.com/groups/1437763413860819/posts/1474883140148846/)
- [Faces in thumbnails](https://thumbnailtest.com/guides/face-in-youtube-thumbnail/)
- [BundleLive: more viewers on Whatnot](https://bundlelive.com/blog/how-to-get-more-viewers-on-whatnot) · [LeLiveBoost](https://leliveboost.com/blog/how-to-get-more-viewers-whatnot)
- Live $1 shows used as examples: [Lululemon tag](https://www.whatnot.com/tag/lululemon) · [Women's Fashion tag](https://www.whatnot.com/tag/womens_fashion)
