# Lessons

Things learned while working, so the same mistake doesn't happen twice.
Claude reads this before every task and adds to it as it goes (see
`CLAUDE.md`). Jade can edit or delete anything here too.

## Jade's preferences

- **Never go into Google Drive.** Get item photos straight from Nifty
  (`get_item_images`). This applies to pricing rules and comps too.
- Sold comps come from Claude in Chrome on Jade's computer (`sold-comps` skill,
  saves `comps.md` per item). Cloud sessions can't read the marketplaces.

- Listing workflow lives in `.claude/skills/listing-workflow/`. The batch is
  the newest pieces in Nifty; the last photo is usually the measurements card.
- "Make labels" means the newly listed pieces in Nifty, even if they never
  had folders or reports here.
- Price only from web facts (sold/asking comps online), never from Jade's own
  sales history. Skip Mercari. Don't list shipping fields in reports.
- Price to sell within ~30 days, off sold comps, allowing for her offers.
- Every piece should clear $20 profit after fees + typical offer; flag any
  that don't.
- Keep pricing rules, offer settings and fees private, never in this public
  repo. Ask Jade for the offer steps if needed (Drive is off-limits).
- In Nifty set only the Depop price; titles and descriptions get notes, not edits.
- SKU labels: 4×4" thermal PDF, bold SKU on top, title under it, no date
  (the SKU has it). Make them only when Jade says "make labels" after she
  lists, using the current Nifty titles (`06-label-printer/make_labels.py`).
- After the labels are sent, empty any `08-to-be-listed/` folders for those
  items (keep the numbered folders).

## Listings and product research

- Measurement cards have a "check description" box. If it's ticked, flaws
  must be written in the description.

- Always check brand, category and NWT-vs-used against the photos, not old
  notes. Earlier passes called underwear a "nightgown" and a one-piece
  romper a "2-piece set".

## Pricing

- Nifty: Depop is the source price, and Nifty's rules set the Poshmark and
  eBay prices from it.

## Branding and covers

## Customer support

## Videos

## Tools and gotchas

- Nifty connector can't edit shipping, category, brand/size/color or photos.
  Only title, description, condition, SKU, cost, quantity and price. List
  blank shipping fields for Jade to fill in the Nifty app.
- SKU format is `MMDD-NN` (date + that day's item number, e.g. `0924-02`). Set it in Nifty for every item.
- Marketplace sites (eBay, Depop, Mercari, Grailed) block automated requests
  from cloud sessions with bot protection. Don't try to get around it. Use
  WebSearch snippets (labelled asking prices) or sold data Jade provides.
  Claude in Chrome on Jade's computer gets through fine (`sold-comps` skill).
- Poshmark sold search: add `&sort_by=added_desc`, or relevance shows sales
  from years ago. Sold dates aren't shown; a listing ID's first 8 hex digits
  are the date it was listed (Unix time), and it sold after that.
- Depop search has no Sold filter (only "On sale", which means discounted), so
  sold comps can't come from Depop.
- WebSearch for "sold" marketplace listings mostly returns active asking
  prices. Don't count them as sold comps.
- On Jade's Mac, `git push` from the terminal has no GitHub login. Commit
  locally, then have Jade click "Push origin" in GitHub Desktop (the Jade
  folder is added there). Never ask her to paste tokens.
- Items in 08-to-be-listed may not be in Nifty yet. Price them anyway and
  do the Nifty steps once Jade adds them.
- Items may already be live with a SKU and price. Keep the existing SKU, and
  if the price is already right, don't edit or apply (applying republishes).
- Check each marketplace listing's own Brand attribute, not just the item's.
  Depop got "Unique Vintage" for a Mainstream swimsuit.
- Nifty's AI can misread handwritten measurement cards (it read sleeve 21"
  as 27"). Always compare the card to the description.
- The Nifty connector can't read the automated-offer settings. Ask Jade.

- Video files are ignored by git (`.gitignore`), so they never get pushed.
  Keep them on the computer.
