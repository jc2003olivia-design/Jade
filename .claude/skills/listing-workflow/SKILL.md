---
name: listing-workflow
description: Jade's listing workflow for Kurated by Kenny. Use when Jade says "start listing workflow", "price the to be listed items", or adds photos to 08-to-be-listed/. Researches sold comps, sets the Depop price in Nifty, checks titles and measurements, and reports per item.
---

# Listing workflow

Items live in `08-to-be-listed/<number>/`, one folder per clothing piece.
The last photo in each folder is the measurements photo. Work through
every numbered folder in order and finish each item (steps 1–6) before
starting the next. Read `LESSONS.md` first.

## 1. Look at the photos
- Open every photo with the Read tool. Resize big ones first with Pillow
  (longest side ~1600px, into the scratchpad) so they fit.
- Get from the photos: brand, item type, size, color, material, condition
  (NWT / like new / used + flaws), style number if on the tag.
- Read the measurements off the last photo exactly. If a value is unclear,
  say so. Never guess.

## 2. Research pricing comps
Goal: **priced to sell within ~30 days**, based on what actually *sold*.
Marketplace sites block automated reading, so don't scrape them or try to
get around their bot protection. Use these sources, best first:

1. **eBay sold data via SerpApi** (only if `SERPAPI_KEY` is set in the
   environment): call `https://serpapi.com/search.json?engine=ebay` with
   `_nkw=<brand + item + key detail>` and `show_only=Sold`. Take the last
   90 days, match brand, item type and era; size and condition come second.
2. **Jade's own sales** (always): `search_orders` for the same brand or
   category (e.g. "sweatshirt", "Free People"). Her real sale prices show
   what *her* buyers pay. Compare them with her listing prices on
   `get_inventory_item` to see how much offers took off.
3. **Terapeak / sold screenshots Jade drops in the item folder** (any file
   named `comps*` in `08-to-be-listed/<n>/`, or the Drive folder
   "Sold comps"). Read the sold prices off them.
4. **WebSearch snippets** (fallback): eBay and Poshmark results sometimes
   show "Sold" prices. Label anything else as an asking price.

**Picking the price:**
- Build a comps table: source, title, price, date, sold or asking.
- Start from the **median sold price** of close matches. If there are no
  sold comps, use about 70–80% of the median asking price, since asking
  prices run higher than sales.
- Adjust for condition (flaws, stains or missing tags → lower half of the
  range) and season (sweatshirts up in fall, swim down).
- Check the $20-profit rule (see "Pricing settings").
- Give a **confidence rating** in the report:
  - **High:** 3+ sold comps of a close match in the last 90 days
  - **Medium:** 1–2 sold comps, or good matches that are only asking prices
  - **Low:** no close matches. Tell Jade to pull Terapeak before listing.

## 3. Update Nifty — Depop price only
- Find the item in Nifty (`search_inventory`, filterType `all`): by SKU if
  the folder name has one, else by brand/type/color, then confirm by
  comparing the listing photo (`pictureUrl`) with the folder photos.
  If there's no match or more than one, stop on that item and ask Jade.
- **SKU:** set `sku` to `MMDD-NN`: the date it's processed plus a 2-digit
  item number for that day, where NN is the folder number (folder `2` on
  Sep 24 → `0924-02`). Before using it, search Nifty SKUs for that `MMDD`
  so you don't reuse a number. If the day already has items, continue from
  the highest one.
- Depop is the source marketplace. Set only `price` (the Depop price) with
  `edit_item`, then `apply_item_edits_action`. Nifty's price rules set
  eBay and Poshmark from it. Never set those by hand.
- If the item is live (LISTED), applying republishes it; that's expected.
- Shipping: fill any blank shipping fields. The Nifty connector **cannot
  edit shipping fields**, so list the blank ones in the report for Jade
  to fill in the Nifty app, with suggested values from past listings
  (Depop: "Depop shipping", parcel size by weight; Poshmark: discounted
  shipping option; eBay: package weight + "Standard" shipping policy).

## 4. Title check — note only, do not change
- Compare the Nifty title with what the photos show and with the title
  format in Nifty's seller instructions (`get_edit_item_instructions`):
  `[Brand] [Item Type] [Style name/number] [Color] [Size] [Aesthetic]`,
  ~65 chars. Note wrong brand, type, color, size, typos, or missing
  keywords. **Do not edit the title.**

## 5. Measurements check — note only
- If the last photo has measurements, check that every one is typed in the
  Nifty description, with the same numbers. Note what's missing or wrong.
  Don't edit the description unless Jade asks.

## 6. Report for the item
Write `08-to-be-listed/<number>/report.md` and send Jade a short message:
- Item + Nifty SKU, Depop price set (and the eBay/Poshmark prices Nifty
  derived).
- Pricing explanation: comps found (platform, price, sold date, link),
  how the price was picked, how it plays with offers/discounts.
- Profit math per platform (see "$20 profit rule"). **FLAG** any item that
  won't clear $20 profit after a typical offer.
- Title notes, measurement notes, shipping fields Jade must fill.

At the end, give a one-line-per-item summary and commit the reports.

## Pricing settings (private — kept in Google Drive, not in this repo)
Jade's Nifty price rules and automated offers are screenshots in her Google
Drive folder **"Pricing rules"**. Before pricing a batch:
1. `search_files` for the folder (`title contains 'Pricing rules'`), list its
   files (`parentId = '<id>'`), and `read_file_content` each screenshot.
   That tool reads the text in PNG files.
2. From them, get the Depop→Poshmark/eBay markups and the offer steps
   (% off, days listed, price band) for each platform.
3. Use them in the scratchpad only. **Never write these numbers into the
   repo** (it's public). Reports should show the math for each item, not
   the full rule tables.

**$20 profit rule:** every piece should clear $20 profit after that
platform's fees, COGS (from Nifty; assume $1 if blank) and the offer it's
likely to have hit by ~30 days. If the price the comps support won't clear
$20, set the realistic price and FLAG it with the math. Don't inflate
the price.
