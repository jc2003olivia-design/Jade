# Lessons

Things learned while working, so the same mistake doesn't happen twice.
Claude reads this before every task and adds to it as it goes (see
`CLAUDE.md`). Jade can edit or delete anything here too.

## Jade's preferences

- Listing workflow lives in `.claude/skills/listing-workflow/`; photos go in
  `08-to-be-listed/<number>/`, last photo = measurements.
- Price to sell within ~30 days, off sold comps, allowing for her offers.
- Every piece should clear $20 profit after fees + typical offer; flag any
  that don't.
- Keep pricing rules, offer settings and fees private. They live in the Drive
  folder "Pricing rules", never in this public repo.
- In Nifty set only the Depop price; titles and descriptions get notes, not edits.

## Listings and product research

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
- Nifty SKUs look like `0914-18` (MMDD-NN).
- The Nifty connector can't read the automated-offer settings. Read the
  Drive "Pricing rules" screenshots with `read_file_content` (it reads the
  text in PNG files).

- The Google Drive connector can't delete files. Use Chrome: the "⋮" menu
  on the file row, then "Move to trash". A raw Delete keypress gets blocked.
- Video files are ignored by git (`.gitignore`), so they never get pushed.
  Keep them in Drive or on the computer.
