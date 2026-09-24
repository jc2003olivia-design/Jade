---
name: sold-comps
description: Pull real SOLD comps for Jade's to-be-listed items using Claude in Chrome on her computer (eBay, Poshmark, Depop, optionally Terapeak), and save them to each item's folder for the listing-workflow to price from. Use when Jade says "pull sold comps", "get comps", or "run the comps step".
---

# Sold comps (runs on Jade's computer with Claude in Chrome)

This step needs **Claude in Chrome**: the Claude desktop app or Cowork,
with the Chrome extension connected, running on Jade's computer. The
marketplaces block cloud sessions, but her own browser works. If Chrome
tools aren't available, stop and tell Jade to open this from the desktop
app with the extension on.

Read `LESSONS.md` first.

## Rules
- **Look only.** Never buy, make offers, like, follow, message, or change
  anything on any site.
- Never type passwords or log in for Jade. If a site asks her to log in or
  shows a captcha, pause and ask her to handle it, then continue.
- Only save public listing info (title, size, condition, price, date, link).
  No buyer or seller usernames.

## 1. Pick the items
Every numbered folder in `08-to-be-listed/` that has photos but no
`comps.md` yet. If Jade names specific folders, do only those.

## 2. Build the search
Look at the item's photos (or its report, if one exists) and write:
- **Main search:** brand + item type + key detail, e.g.
  `nutmeg tennessee crewneck`, `mainstream swimsuit one piece`.
- **Wide search:** style without the brand (for obscure brands), e.g.
  `90s tennessee seal sweatshirt`, `vintage black textured swimsuit`.
Leave the size out of the search. Note it when reading the results instead.

## 3. Search each platform's SOLD listings
Replace `QUERY` with the search (spaces as `+`). Sort by most recent where
you can. If a link doesn't land on sold results, use the site's own
**Sold** filter.

| Platform | Sold search |
|---|---|
| eBay | `https://www.ebay.com/sch/i.html?_nkw=QUERY&LH_Sold=1&LH_Complete=1&_sop=13` |
| Poshmark | `https://poshmark.com/search?query=QUERY&availability=sold_out` |
| Depop | `https://www.depop.com/search/?q=QUERY`, then turn on the **Sold items** filter |
| Terapeak (optional, if Jade is logged in to eBay) | `https://www.ebay.com/sh/research?marketplace=EBAY-US&keywords=QUERY&dayRange=90&tabName=SOLD` |

On each results page, read (screenshot and zoom if needed) up to **10 of
the closest matches** from the **last 90 days**. Skip lots, bundles, and
anything clearly a different item. If the main search gets fewer than 3
matches on a platform, try the wide search there too.

For eBay, use the green "Sold" price. Crossed-out prices are the old list
price. A "Best offer accepted" sale may have gone for less than the price
shown, so mark it.

## 4. Save `08-to-be-listed/<n>/comps.md`

```markdown
# Sold comps — <item> (pulled <YYYY-MM-DD>)
Searches: "<main>", "<wide>"

| Platform | Title | Size | Condition | Sold price | Sold date | Link |
|---|---|---|---|---|---|---|
| eBay | ... | XL | used, flaws | $34.99 | 2026-09-10 | https://... |

**Summary:** <n> sold comps · median $<x> · range $<low>–$<high>
**Closest match:** <one line on the best comp and why>
**Notes:** anything useful, e.g. "clean ones sell $50+, flawed ones ~$35",
"no Depop sales", "Best offer accepted on 2 of 4 eBay sales"
```

Write only comps, no pricing decision. The listing-workflow sets the price
using Jade's private pricing rules.

## 5. Save and hand off
- **If this folder is a git clone of the Jade repo** (`git remote -v` shows
  `jc2003olivia-design/Jade`): commit the `comps.md` files and push to
  `main`, so the cloud listing-workflow can see them.
- **If it isn't a clone, or the push fails:** save each item's comps to
  Google Drive instead, as a Google Doc in the folder **"Sold comps"**
  (create the folder if it's missing) named `comps <folder #> - <item>`,
  e.g. `comps 2 - Nutmeg Tennessee crewneck`. Use the Drive connector's
  `create_file` with `contentMimeType: "text/plain"`. Then tell Jade the
  comps are in Drive.
- Tell Jade in one line per item: number of comps, median, range.
- Then she says **"start listing workflow"** (in the cloud or here), and it
  prices from these comps.
