# Lessons

Things learned while working, so the same mistake doesn't happen twice.
Claude reads this before every task and adds to it as it goes (see
`CLAUDE.md`). Jade can edit or delete anything here too.

## Jade's preferences

## Listings and product research

- Always check brand, category and NWT-vs-used against the photos, not old
  notes. Earlier passes called underwear a "nightgown" and a one-piece
  romper a "2-piece set".

## Pricing

## Branding and covers

- New cover = new entry in `SHOWS` in `make_covers.py`, then run it. Don't hand-edit the PNGs.
- Quince has no logo file yet. It shows as bold "QUINCE" text until `logos/quince.png` is added.

## Customer support

## Videos

## Tools and gotchas

- `make_covers.py` needs `pip install cairosvg` for the Nike SVG logo.
- Brand websites (e.g. quince.com) are blocked from the cloud container, so logos can't be
  downloaded there. Ask Jade for the logo file instead.

- The Google Drive connector can't delete files. Use Chrome: the "⋮" menu
  on the file row, then "Move to trash". A raw Delete keypress gets blocked.
- Video files are ignored by git (`.gitignore`), so they never get pushed.
  Keep them in Drive or on the computer.
