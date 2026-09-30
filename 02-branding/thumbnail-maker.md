# Thumbnail Maker

Whatnot show covers for the $1-start series: **Premium Contemporary**,
**Premium Activewear**, **Kids Vintage** and **Kids Modern**. Mockups are in `whatnot-covers/`.

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
1. **Logo runner**: an edge-to-edge band in the accent color with the show's brand logos
   repeating, separated by dots (like a ticker). It runs off both sides on purpose.
2. `KENNY SHOP`: small, spaced-out letters in the accent color
3. `PREMIUM` + show name: the big headline
4. Your photo: wearing the hero piece, smiling at the camera, filling most of the frame
5. `$1 STARTS`: a round badge by your shoulder
6. (Contemporary) `FALL THEMED` in the accent color
7. **Logo runner** again at the bottom, starting on the next brand so it doesn't mirror the top one

Runner logos are large enough to read in the feed. Free People sits slightly high and Polo
slightly low in the strip (`RUNNER_NUDGE` in `make_covers.py`).

### Premium Contemporary
- Background: navy, soft window light
- Colors: navy `#1F2E4A` · white `#FFFFFF` (headline) · butter yellow `#F6D776` (runners, Kenny Shop, $1 badge, "FALL THEMED"); logos in the runners are navy
- Fonts: Playfair Display Bold headline, Montserrat ExtraBold for Kenny Shop, badge and brand text
- Text: `PREMIUM CONTEMPORARY` · `$1 STARTS` · `FALL THEMED` · runners: Free People logo · Polo Ralph Lauren logo · `PREMIUM DENIM`
- Outfit: one elevated piece, like a knit set, slip dress, or blazer + tailored trousers

### Premium Activewear: bright and poolside
- Background: bright poolside blue, bright even light
- Colors: poolside blue `#12B5EA` · hot pink `#FF3D8B` (runners, $1 badge) · white `#FFFFFF` (headline, Kenny Shop, runner logos, badge text)
- Fonts: Anton for the headline and $1, Montserrat ExtraBold for Kenny Shop and "STARTS"
- Text: `PREMIUM ACTIVEWEAR` · `$1 STARTS` · runners: Free People Movement · Lululemon · Nike logos
- Outfit: a matching set (Align, Define, Alo) in a color that pops against bright blue (orange, black, white, lime). Avoid blue sets.

### Kids Vintage: 70s green + orange
- Colors: forest green `#2F6B4F` · cream `#FFEFD2` (headline, sizes) · orange `#F2913D` (runners, Kenny Shop, $1 badge) · dark green `#2F3B2A` (runner and badge text)
- Fonts: Shrikhand for "KIDS VINTAGE" (retro script, one line), Titan One for the $1, sizes and runners
- Text: `KIDS VINTAGE` · `$1 STARTS` · runners: `OVERALLS` · `DENIM` · `DESIGNER` (categories, not brands)
- Photo: a little one wearing a vintage hero piece (patchwork overalls, a character tee)
- Other colors tried (mustard + cherry was the first version): `whatnot-covers/options-kids-vintage.png`

### Kids Modern: soft mint + tangerine
- Colors: mint `#9ED8C6` · navy `#1E3A5F` (headline, Kenny Shop, runner and badge text) · tangerine `#FF8A5B` (runners, $1 badge)
- Fonts: Fredoka Bold (rounded) for everything big
- Text: `KIDS MODERN` · `$1 STARTS` · runners: Hanna Andersson · Mini Boden · Zara
- Photo: a little one wearing a current-season piece. The $1 badge sits bottom-left here so it
  stays off her face (`badge="bottom-left"`).

Both kids covers put the headline on one line (`one_line`) so the photo slot is taller and the
whole outfit fits. Each kids show has two covers, one per size run, with the sizes in big type under the photo:
`BABY · NB–24M` and `TODDLER & KIDS · 2T–16` (16 = kids' XL). They're in `final/` as
`kids-vintage-baby`, `kids-vintage-kids`, `kids-modern-baby`, `kids-modern-kids`.
To use a different photo, put it in `photos/` and change `KID_PHOTOS` in `make_covers.py`.

### October Clear Out: 70% off clearance
- For running eBay listings and randoms at 70% off, all sizes (kids, women's, men's).
- Colors: clearance red `#E3262E` · white `#FFFFFF` (headline, footer) · yellow `#FFD83D` (runners, Kenny Shop, badge) · near-black `#1A1A1A` (runner logos and badge text)
- Fonts: Anton for the headline and "70%", Montserrat ExtraBold for everything else
- Text: `OCTOBER CLEAR OUT` · badge `70% OFF` · `ALL SIZES · KIDS · WOMEN'S · MEN'S` · runners: Nike logo · Ralph Lauren logo · `VINTAGE`
- Photo: you holding or wearing the best steal of the night. Finished cover:
  `final/october-clear-out-photo.png` (badge bottom-right so it stays off your face).

## Templates
- Main cover photo (blank templates): `whatnot-covers/premium-contemporary.png`, `whatnot-covers/premium-activewear.png`,
  `whatnot-covers/kids-vintage.png`, `whatnot-covers/kids-modern.png`, `whatnot-covers/october-clear-out.png`
- Finished covers with your photos: `whatnot-covers/final/` (includes `premium-contemporary-2.png`, a second Contemporary cover with no fall line and Free People · Anthropologie · Aritzia in the runners; Anthropologie and Aritzia show as text until their logo files are added). These and the photos in
  `whatnot-covers/photos/` stay on this computer only and are kept out of git, because the repo is public.
- Feed-size check: `whatnot-covers/preview-feed-size.png`
- Other color options considered: `whatnot-covers/options-contemporary.png`, `whatnot-covers/options-activewear.png`
- Bundle / lot photo:
- Sale / promo photo:

## Brand logos
- Logo files go in `whatnot-covers/logos/`, named after the brand: `nike.svg`,
  `lululemon.png`, `free-people.png`, `free-people-movement.png`, `polo-ralph-lauren.png`.
- PNG with a transparent background works best. A plain white background is OK too.
  Logos are recolored to the runner's logo color automatically.
- If a brand has no logo file, its name shows as big bold text instead (like "DENIM").
- Have so far (see `whatnot-covers/logos-preview.png`): Free People, Free People Movement,
  Anthropologie, Polo Ralph Lauren, Ralph Lauren, Skims, Lululemon, Nike.
  - Lululemon: circle mark only (the wordmark is too small at cover size).
  - Free People Movement: the file sent was cut off after "MOVEME", so the "NT" was redrawn to match.
  - Anthropologie: the file sent was too small (16 px tall) to enlarge cleanly, so the wordmark is
    redrawn in Playfair Display with the same spaced capitals.
- Still need: Aritzia (shows as bold text until then).

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
- Fonts: Playfair Display, Anton, Montserrat, Shrikhand, Titan One and Fredoka (free Google fonts, in `whatnot-covers/fonts/`).
  The same fonts are in Canva if you rebuild a cover there.
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
