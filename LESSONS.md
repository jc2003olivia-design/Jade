# Lessons

Things learned while working, so the same mistake doesn't happen twice.
Claude reads this before every task and adds to it as it goes (see
`CLAUDE.md`). Jade can edit or delete anything here too.

## Jade's preferences

- Sold comps come from Claude in Chrome on Jade's computer (`sold-comps` skill,
  saves `comps.md` per item, or a Google Doc in the Drive folder "Sold comps" if
  it can't push to GitHub). Cloud sessions can't read the marketplaces.

- Listing workflow lives in `.claude/skills/listing-workflow/`; photos go in
  `08-to-be-listed/<number>/`, last photo = measurements.
- Price only from web facts (sold/asking comps online), never from Jade's own
  sales history. Skip Mercari. Don't list shipping fields in reports.
- Price to sell within ~30 days, off sold comps, allowing for her offers.
- Every piece should clear $20 profit after fees + typical offer; flag any
  that don't.
- Keep pricing rules, offer settings and fees private. They live in the Drive
  folder "Pricing rules", never in this public repo.
- In Nifty set only the Depop price; titles and descriptions get notes, not edits.

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
- Items in 08-to-be-listed may not be in Nifty yet. Price them anyway and
  do the Nifty steps once Jade adds them.
- Nifty's AI can misread handwritten measurement cards (it read sleeve 21"
  as 27"). Always compare the card to the description.
- The Nifty connector can't read the automated-offer settings. Read the
  Drive "Pricing rules" screenshots with `read_file_content` (it reads the
  text in PNG files).

- The Google Drive connector can't delete files. Use Chrome: the "⋮" menu
  on the file row, then "Move to trash". A raw Delete keypress gets blocked.
- Video files are ignored by git (`.gitignore`), so they never get pushed.
  Keep them in Drive or on the computer.
