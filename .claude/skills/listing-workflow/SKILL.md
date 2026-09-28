---
name: listing-workflow
description: Jade's listing workflow for Kurated by Kenny. Use when Jade says "start listing workflow" or "price the to be listed items", or has added new pieces in Nifty. Reads each item's photos straight from Nifty, researches sold comps, sets the Depop price, checks titles and measurements, and reports per item. Also use when Jade says "make labels": sends a PDF of 4x4 SKU labels for the new pieces.
---

# Listing workflow

Items live in **Nifty**. Photos come straight from Nifty, never from Google
Drive. **Don't open Google Drive at all** (Jade's rule). The batch is
the new pieces Jade has added: find them with `search_inventory`
(filterType `all`, sort `created_at` desc). Take the newest ones added since
the last batch, and check the count with Jade if it isn't clear. Work
through them in SKU order and finish each item (steps 1–6) before starting
the next. Read `LESSONS.md` first.

Older batches may still have photos in `08-to-be-listed/<number>/`. Use
those only if the item isn't in Nifty yet.

## 1. Look at the photos (from Nifty)
- Load them with `get_item_images` (up to 4 per call; page through with
  `offset` until you've seen all `totalPictures`). The measurements card
  is usually the last photo.
- Get from the photos: brand, item type, size, color, material, condition
  (NWT / like new / used + flaws), style number if on the tag.
- Read the measurements off the last photo exactly. If a value is unclear,
  say so. Never guess.

## 2. Research pricing comps
Goal: **priced to sell within ~30 days**, based on what actually *sold*.
Marketplace sites block automated reading, so don't scrape them or try to
get around their bot protection.

**Best source: sold comps from the `sold-comps` skill** (Claude in Chrome
on Jade's computer), saved as `08-to-be-listed/<SKU or number>/comps.md`.
If it's there, price from it first; with 3+ close sold matches, confidence
is **High**. If there's no `comps.md` and the item may be worth $40+ (or you'd
rate it Low), tell Jade to run "pull sold comps" on her computer.

**Otherwise: WebSearch across every platform.** For each item, run one
search per platform (in parallel):
- `<brand> <item> <key detail> site:ebay.com` (also try adding "sold")
- `... site:poshmark.com`
- `... site:depop.com`
- `... site:grailed.com OR site:etsy.com`
- one broad search without `site:` (vintage shops and retail price)

Try a second wording if the first is thin: drop the brand and keep the style
("90s Tennessee seal crewneck"), or add the size. Collect every price you
can see: platform, title, size, price, and whether it's **sold** or
**asking**.

**Extra sources when available** (web facts only. Don't use Jade's own
Nifty sales history for pricing):
- **Sold screenshots** Jade drops in the item folder (files named `comps*`),
  e.g. Terapeak or the "sold" filter on Depop or Poshmark.
- **SerpApi eBay sold data**, only if `SERPAPI_KEY` is set:
  `https://serpapi.com/search.json?engine=ebay&_nkw=<query>&show_only=Sold`.

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
- **SKU:** if the item already has an `MMDD-NN` SKU, keep it. Otherwise set
  `sku` to `MMDD-NN`: the date it's processed plus that day's 2-digit item
  number (`0924-02`). Search Nifty SKUs for that `MMDD` first so you don't
  reuse a number, and continue from the highest one.
- Depop is the source marketplace. Set only `price` (the Depop price) with
  `edit_item`, then `apply_item_edits_action`. Nifty's price rules set
  eBay and Poshmark from it. Never set those by hand.
- If the item is live (LISTED), applying republishes it; that's expected.
  If the price is already right, don't edit or apply.
- Shipping: the connector can't edit it, and Jade handles it in the app.
  Don't mention it in reports.

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
Write `08-to-be-listed/<SKU>/report.md` and send Jade a short message:
- Item + Nifty SKU, Depop price set (and the eBay/Poshmark prices Nifty
  derived).
- Pricing explanation: comps found (platform, price, sold date, link),
  how the price was picked, how it plays with offers/discounts.
- Profit math per platform (see "$20 profit rule"). **FLAG** any item that
  won't clear $20 profit after a typical offer.
- Title notes and measurement notes. (Don't list shipping fields; Jade
  handles those.)

At the end, give a one-line-per-item summary and commit the reports. Tell
Jade to say "make labels" once she has listed the items.

## SKU labels (only when Jade asks, after she lists)
Don't make labels at the end of the workflow. Jade lists the items first
so the titles are final, then says "make labels". Make one PDF of 4×4"
thermal labels for the batch and send it to her.
- The batch is the newly listed pieces in Nifty (`search_inventory`, sort
  `created_at` desc), even if they never went through this workflow.
  Confirm the count if Jade gave one.
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
Empty the folders so Jade can drop in the next batch's photos. Git keeps
the history, so nothing is lost.
- In `08-to-be-listed/`, for every item that got a label and has a folder
  there, delete everything in its folder: photos, `comps*`, `report.md`, and any other files. Keep
  the numbered folder and its `.gitkeep`. If the folder name has a SKU
  (`1 - 0924-01`), rename it back to just the number.
- Leave any folder whose item was skipped for labels (no SKU / not in
  Nifty yet) as it is, and tell Jade which ones are still there.
- Don't touch Google Drive.
- Keep the label PDF in `06-label-printer/labels/`. Don't touch Nifty.
- Commit and push ("Clear listed batch <YYYY-MM-DD>"), then tell Jade the
  folders are empty and ready for new photos.

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
