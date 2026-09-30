---
name: listing-workflow
description: Jade's listing workflow for Kurated by Kenny. Use when Jade says "start listing workflow" or "price the to be listed items". Takes the new Nifty drafts, reads their photos from Nifty, researches the piece (brand, retail, era, fabric, demand), tries niche titles, pulls sold comps (Poshmark from the cloud, eBay via SerpApi when set), gives quick-sale / market / premium prices and sets the Depop price in Nifty, suggests a title in Jade's format, checks measurements, and reports per item. Also use when Jade says "make labels" after listing: sends a PDF of 4x4 SKU labels, then clears the batch's report folders.
---

# Listing workflow

Items and photos come from **Nifty**, not the repo. **Never open Google
Drive** (Jade's rule), not for photos, comps or pricing rules. The
batch is every Nifty draft with no SKU yet: `search_inventory` with
filterType `drafted`, keep the ones with the `MISSING_SKU` warning, and work
oldest first (`createdAt`). Drafts that already have a SKU were done in an
earlier batch; skip them unless Jade names them. If Jade names items, do
only those. Finish each item (steps 1–7) before starting the next. Read
`LESSONS.md` first.

Each item gets a working folder `08-to-be-listed/<SKU>/` (made in step 4)
for its `report.md`. Photos are not saved to the repo.

## 1. Look at the photos
- Load the photos with Nifty `get_item_images` (`maxImages` 4). If
  `totalPictures` is more than you got, call again with `offset` 4, 8...
  until you've seen them all.
- Get from the photos: brand, item type, size, color, material, condition
  (NWT / like new / used + flaws), style number if on the tag.
- Read every tag closely, since it drives the research in step 2: style
  name or number, fabric content, made-in country, RN or CA number,
  retail price sticker, union label or old-style care tag (era clues), and
  line or sub-label (e.g. "Jude Cloth", "Lauren" vs "Polo").
- The measurements photo is usually the last one. Read the measurements off
  it exactly. If a value is unclear, say so. Never guess. If there's no
  measurements photo, say so in the report.

## 2. Research the piece
Know exactly what it is before pricing it. Guessing the wrong line, era or
fabric is what throws prices off. Use WebSearch (and WebFetch on brand or
reference pages) for:
- **Identity:** brand, line or sub-label, style name or number, and the
  season or year if findable. Search the style number and tag text.
- **Original retail (MSRP):** brand site, retailer listings, or the
  retail most Poshmark sellers typed (the script in step 3 shows it).
- **Brand tier:** fast fashion / mall / contemporary / boutique /
  designer, and who buys it secondhand (preppy, Y2K, vintage, outdoor...).
- **Era (vintage):** tag style, made-in country, RN number, union label.
  Say how sure you are, and don't call something vintage without a clue.
- **Fabric:** fiber content from the tag. Silk, cashmere, wool, linen,
  leather and heavy 100% cotton add value; acrylic and thin poly don't.
- **Buyer search words:** the names buyers actually use (style name,
  print name, "coastal", "gorpcore"...). Pull them from sold titles.
- **What moves the price for this piece:** NWT vs used, print vs solid,
  size, color, season. Check the sold comps for it.

This goes in the report's "About the piece" section (step 7) and sets the
search words for step 2b and step 3.

## 2b. Niche titles (before pricing)
Buyers who search niche words pay more than buyers who search "top". Find
the niche this piece fits before pulling comps, so the comps and the title
aim at the buyers who pay the most.
- Write **3–4 niche title variants** in Jade's title format (step 5), each
  leaning on a different angle: era ("80s", "Y2K", "2010s"), style/line/
  print name ("Very Berry Paisley", "Catarina", "Doudoune Legere"),
  aesthetic ("coquette", "whimsigoth", "indie sleaze", "gorpcore"), and
  standout detail ("exposed button fly", "ribbon fringe", "made in USA").
  Only use words the photos and tags back up.
- Turn each variant into a short search (brand or style words + the niche
  words, no filler words) and run it through `posh_sold.py` and WebSearch
  in step 3.
- In the report, say which niche searches found higher sold prices or
  faster sales, and pick the **suggested title** from the one that did.
  That niche also sets the *premium* price (step 3).

## 3. Research pricing comps
Goal: price from what actually *sold*, and give Jade three prices: quick
sale, market value and premium (see "Picking the price").
Don't scrape sites that block cloud sessions (eBay, Etsy, Mercari,
Grailed, The RealReal, WorthPoint) or try to get around their bot
protection.

Pull from every source below that's available, in this order.

**a. Chrome sold comps** from the `sold-comps` skill, saved in
`08-to-be-listed/comps/` (files name the brand and item, with the Nifty
title inside), or pasted by Jade in chat. Best source for eBay and Terapeak.

**b. Poshmark sold comps (always run this, it works from the cloud).**
```
python3 .claude/skills/listing-workflow/posh_sold.py "<brand> <item> <key detail>"
python3 .claude/skills/listing-workflow/posh_sold.py "<brand> <item>" --size <size>
python3 .claude/skills/listing-workflow/posh_sold.py "<style words, no brand>"   # obscure brands
```
It prints the last 90 days of sales: sold date, days to sell, first ask →
sold-at price, original retail, size, condition, link, plus how many are
listed now. Keep it light: a few searches per item, no fetching of listing
pages. If it fails, say so in the report and carry on with the others.
- "Sold at" is the last listed price. Poshmark hides accepted offers, so
  the buyer often paid a bit less.
- These are **Poshmark** prices. Nifty sets the Poshmark price higher than
  the Depop price, so don't copy them 1:1 onto Depop (see "Picking the
  price").

**c. WebSearch across platforms** for eBay, Depop, Etsy, Grailed, vintage
shops and retail. One search per platform, in parallel:
- `<brand> <item> <key detail> site:ebay.com` (also try adding "sold")
- `... site:depop.com`
- `... site:grailed.com OR site:etsy.com`
- one broad search without `site:` (vintage shops and retail price)

These are mostly **asking** prices. Mark them as asking.

**d. eBay sold data from SerpApi (run it whenever `SERPAPI_KEY` is set).**
This is the only way to get eBay *sold* prices from the cloud. Check with
`[ -n "$SERPAPI_KEY" ]` at the start of the batch. If it's set, run the main
search and the best niche search for every item:
`curl -s "https://serpapi.com/search.json?engine=ebay&_nkw=<query>&show_only=Sold&api_key=$SERPAPI_KEY"`
and read `organic_results` (title, price, condition, link). Never print or
write the key. If it isn't set, say "no eBay sold data (SERPAPI_KEY not
set)" in the report.

**e. Extras when available** (web facts only. Don't use Jade's own Nifty
sales history for pricing):
- Sold screenshots Jade adds to the Nifty item or drops in
  `08-to-be-listed/` (files named `comps*`), e.g. Terapeak.

If there are fewer than 3 close sold matches and the item may be worth
$40+, or it's vintage/Y2K/trend and there's no eBay sold data, tell Jade
to run "pull sold comps" on her computer.

**Grade every comp** against the item before using it:
- **Exact:** same brand and same style (name/number or clearly the same
  piece).
- **Close:** same brand and type, similar features, size and condition
  (e.g. another solid sleeveless Jude Connally shell, used).
- **Loose:** different brand in the same style, or same brand but a
  different type, NWT vs used, or a print vs solid gap. Context only.

**Picking the price:**
- Build the comps table: source, title, size, condition, match, price,
  sold date, days to sell, sold or asking, link.
- Use exact and close sold comps from the last 90 days. Ignore loose comps
  unless there's nothing else.
- Only asking prices? Use about 70–80% of their median, and never above
  the close sold comps if there are any.
- **Adjust** for condition (flaws, stains or no tags → lower; NWT → NWT
  comps only), size (XS and 2X+ often sell differently; check the
  size-filtered search), and season (sweatshirts up in fall, swim down).
- **Three prices, all as Depop prices:**
  - *Quick sale* (~1–2 weeks): the low end of the close comps, the ones
    that sold within 30 days. If supply is far bigger than sales or most
    sales needed price drops, *recommend* quick sale in the report, but
    still set market value unless Jade chose otherwise.
  - *Market value* (~30–60 days): the median to upper-middle of the exact
    and close sold comps across all 90 days.
  - *Premium* (waits for the niche buyer): the top of the close comps,
    or what the best niche search (step 2b) sold for.
- **Which one to set:** set **market value** unless Jade says "quick sale"
  or "premium" for the batch or an item. Her automatic offers bring the
  price down over time, so don't set below market value by default.
- **Where the Depop price comes from:**
  - *Vintage, Y2K, band/graphic tees, trend and aesthetic pieces:*
    Depop buyers pay more for these than Poshmark buyers. Anchor on **eBay
    sold** (SerpApi or Chrome comps) and check against Depop asking prices
    (WebSearch `site:depop.com`, graded as asking). Only fall back to
    Poshmark if there's no eBay sold data, and say so.
  - *Mall, workwear, designer kids, basics:* anchor on Poshmark sold and
    convert: find the Depop price whose Nifty-derived Poshmark price lands
    on the Poshmark anchor. Read the Depop→Poshmark markup from a recent
    item's listings (`get_inventory_item`) and work it out in the
    scratchpad (never write the markup in the repo).
  - If platforms disagree, say so and explain which one you followed.
- Check the $20-profit rule at the price you set (see "Pricing settings").
- Give a **confidence rating** in the report:
  - **High:** 3+ exact or close sold comps in the last 90 days that agree
    (spread within about ±30% of the median)
  - **Medium:** 1–2 close sold comps, or 3+ that disagree, or only good
    asking matches
  - **Low:** no close sold comps. Tell Jade to run "pull sold comps" (and
    Terapeak) before listing.

## 4. Update Nifty — SKU and Depop price
- You already have the item from the batch list, so no matching is needed.
- **SKU:** set `sku` to `MMDD-NN`: the date it's processed plus a 2-digit
  item number for that day (items 1, 2, 3... in batch order; Sep 24 →
  `0924-01`, `0924-02`). First search Nifty SKUs for that `MMDD`
  (`searchType` `sku`, filterType `all`). If the day already has items,
  continue from the highest one.
- Make the item's folder `08-to-be-listed/<SKU>/` for its report.
- Depop is the source marketplace. Set `sku` and `price` (the Depop price)
  with `edit_item`, then `apply_item_edits_action`. Nifty's price rules set
  eBay and Poshmark from it. Never set those by hand.
- If the item is live (LISTED), applying republishes it; that's expected.
- Shipping: the connector can't edit it, and Jade handles it in the app.
  Don't mention it in reports.

## 5. Title — suggest in Jade's format, do not change
Jade's title format (set 2026-09-30 from the titles she listed that day).
It replaces the ~65-char format in Nifty's seller instructions:

`[Decade if known] [Brand] [Item type + style/line/print name] [Color] [Details/fabric] [Aesthetic] [Size]`

- Use most of eBay's 80 characters (aim for ~70–80). Pack in the words
  buyers search; don't flag a title for being over 65.
- Lead with the decade when the tags back it up ("80s", "2010s", "Y2K").
  Skip it for current-season pieces.
- Style, line or print names go right after the item type ("Hipster
  Crossbody Bag Very Berry Paisley", "Bombshell Push Up Teddy").
- Size goes last, as on the tag ("M", "Small", "24", "4T").
- Her examples:
  - `80s St Anna Pink Sheer Lace Bodysuit V Neck High Cut Lingerie Teddy Medium`
  - `Altar'd State Lace Trim Tie Front Top Pastel Yellow Ribbed Coquette Blouse M`
  - `Abercrombie & Fitch Distressed Denim Shorts Low Rise Exposed Button Fly 24`

Check the Nifty title against the photos (wrong brand, type, print, color,
size, typos) and write a **suggested title** in this format from the best
niche in step 2b. **Do not edit the title in Nifty** unless Jade asks.

## 6. Measurements check — note only
- If there's a measurements photo, check that every one is typed in the
  Nifty description, with the same numbers. Note what's missing or wrong.
  Don't edit the description unless Jade asks.

## 7. Report for the item
Write `08-to-be-listed/<SKU>/report.md` in this layout (keep the headings;
cut a section only if it truly has nothing):

```markdown
# <SKU> — <brand> <item>, <size>

**Depop price set: $X — <tier>** (Nifty derived Poshmark $Y, eBay $Z). <Draft/Live>.
**Confidence: High/Medium/Low.** <n> exact/close sold comps, median $<m> on <platform>.
**Prices (Depop):** quick sale $<a> · market value $<b> · premium $<c>
**Suggested title:** <title in Jade's format>
**eBay sold data:** yes (SerpApi / Chrome) · no (SERPAPI_KEY not set)

## About the piece
- **What it is:** brand + line, style name/number, era, made in, fabric.
- **Brand and market:** tier, original retail $<r> (source), who buys it.
- **Condition:** NWT / like new / used, with any flaws and the photo number.
- **Demand:** <sold in 90 days> sold vs <listed now> listed on Poshmark,
  median <d> days to sell, <k> of <n> dropped price first. Season note.
- **What moves the price:** e.g. "NWT sells ~$35–48; used solids $15–23;
  prints sell faster than solids".
- **Buyer search words:** 3–6 terms from sold titles.

## Niche titles tried
| Niche title | Search used | Sold found | Median sold | Notes |
|---|---|---|---|---|

## Pricing
<how each of the three prices was picked: the anchor comps, which platform
anchored the Depop price and why, adjustments, any platform disagreement,
how it plays with offers>

| Platform | Title | Size | Cond. | Match | Price | Sold date | Days to sell | Sold/asking | Link |
|---|---|---|---|---|---|---|---|---|---|

(exact and close comps first, up to ~10; loose ones only if used)

## Profit after a typical ~30-day offer
<table per platform + FLAG if any platform won't clear $20>

## Title (not changed)
<suggested title again, plus anything wrong in the current Nifty title>
## Measurements
```

Then send Jade a short message per item: SKU, Depop price set and its
tier, the three prices, the suggested title, confidence,
two or three lines from "About the piece" (what it is, retail, demand),
the anchor comps with links, and any FLAG. Title and measurement notes in
one line each. (Don't list shipping fields; Jade handles those.)

At the end, give a one-line-per-item summary and commit the reports. Tell
Jade to say "make labels" once she has listed the items.

## SKU labels (only when Jade asks, after she lists)
Don't make labels at the end of the workflow. Jade lists the items first
so the titles are final, then says "make labels". Make one PDF of 4×4"
thermal labels for the batch and send it to her.
- The batch is the newly listed pieces in Nifty (`search_inventory`,
  filterType `all`, sort `created_at` desc), even if they never went
  through this workflow. Confirm the count if Jade gave one.
- For each item, re-read Nifty now and take `sku` and the current `title`.
  Skip items with no SKU or not in Nifty yet, and say so.
- Write them to a JSON list in the scratchpad
  (`[{"sku": ..., "title": ...}]`) and run
  `python3 06-label-printer/make_labels.py <json> -o 06-label-printer/labels/sku-labels-<YYYY-MM-DD>.pdf`
  (`pip install reportlab` if it's missing).
- Look at one page (render it to PNG) to check nothing is cut off, then
  send the PDF with `SendUserFile`, and commit it.
- Then clear the batch (next section) right away. Don't wait to be asked.

## Clear the batch (right after the labels are sent)
Remove this batch's working files so the next batch starts clean. Git
keeps the history, so nothing is lost.
- In `08-to-be-listed/`, for every item that got a label, delete its
  `<SKU>/` folder and its file in `comps/`. Leftover numbered folders
  from the old photo setup can be emptied the same way; keep their
  `.gitkeep`.
- Leave any folder whose item was skipped for labels (no SKU yet) as it is, and tell Jade which ones are still there.
- Keep the label PDF in `06-label-printer/labels/`. Don't touch Nifty.
- Commit and push ("Clear listed batch <YYYY-MM-DD>"), then tell Jade the
  batch is cleared and ready for the next Nifty drafts.

## Pricing settings (private, never in this repo)
Don't read them from Google Drive. The Poshmark and eBay prices Nifty
derives are on each item's listings (`get_inventory_item`). The Nifty
connector can't read the automated-offer steps, so ask Jade for them once
per session if you need them. Use them in the scratchpad only. **Never write
the rule numbers into the repo** (it's public). Reports should show the math
for each item, not the full rule tables.

**$20 profit rule:** every piece should clear $20 profit after that
platform's fees, COGS (from Nifty; assume $1 if blank) and the offer it's
likely to have hit by ~30 days. If the price the comps support won't clear
$20, set the realistic price and FLAG it with the math. Don't inflate
the price.
