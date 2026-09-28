# Lessons

Things learned while working, so the same mistake doesn't happen twice.
Claude reads this before every task and adds to it as it goes (see
`CLAUDE.md`). Jade can edit or delete anything here too.

## Jade's preferences

- **Never go into Google Drive.** Get item photos straight from Nifty
  (`get_item_images`). This applies to pricing rules and comps too.
- Sold comps come from Claude in Chrome on Jade's computer (`sold-comps` skill,
  saves `08-to-be-listed/comps/<brand>-<item>.md`). Cloud sessions can't read
  the marketplaces.

- Listing workflow lives in `.claude/skills/listing-workflow/`. Photos come
  from Nifty (`get_item_images`), not Drive or the repo; batch = Nifty drafts
  with no SKU. Last photo = measurements.
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
- Storage boxes are Nifty labels "BOX A"–"BOX H". Jade says which box a batch
  goes in; add that label to each item with `add_labels_action`.
- After the labels are sent, clear that batch: delete its `08-to-be-listed/<SKU>/`
  folders and `comps/` files.

## Listings and product research

- Measurement cards have a "check description" box. If it's ticked, flaws
  must be written in the description.

- Nifty's AI fills the Depop brand field on its own and can get it wrong
  (it tagged an "a blissful state of mind" tee as Coin 1804). Check it against
  the neck label.
- Nifty drafts may have no measurements photo. Flag it in the report; never
  guess measurements.
- Always check brand, category and NWT-vs-used against the photos, not old
  notes. Earlier passes called underwear a "nightgown" and a one-piece
  romper a "2-piece set".
- Sizing swimsuits from flat measurements: double pit-to-pit and waist for
  the relaxed circumference; stretch fabric fits bodies ~2–4" bigger. 16"
  pit-to-pit + 11–13" waist + 22" neckline-to-crotch = Small (US 6–8).

## Pricing

- Nifty: Depop is the source price, and Nifty's rules set the Poshmark and
  eBay prices from it.

## Branding and covers

## Whatnot shows

- Whatnot: run Premium Activewear and Premium Contemporary as two separate
  shows (~50 pieces each), not one combined show.
- Whatnot shows run under one generic listing with $1 starts (Jade calls it
  "random pull"). Delist from Depop/Poshmark before going live.
- Show playbook (scripts, item counts, timers, giveaway rules) is
  `04-online-selling/whatnot.md`. Tag each claim [Whatnot]/[Study]/[Math]/[Test];
  Jade wants only proven facts, so label anything that isn't.
- Whatnot requires condition said out loud and "NO PURCHASE NECESSARY" every
  time a giveaway is promoted. No follow-my-socials or spend-to-enter rules.

## Customer support

## Videos

## Tools and gotchas

- Every session starts from `main`, so a change to a skill or LESSONS.md is
  lost to later sessions until its branch is merged. Tell Jade to merge the PR
  when a workflow change is done. (The Sep 27 Nifty-drafts workflow sat
  unmerged and new sessions fell back to the old folder-photos workflow.)
- help.whatnot.com pages return 403 to WebFetch. Use the Zendesk API instead:
  `curl https://help.whatnot.com/api/v2/help_center/en-us/articles/<id>.json`
  (search: `.../api/v2/help_center/articles/search.json?query=...`). Whatnot's
  blog (blog.teamwhatnot.com) fetches fine with curl.

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
- Nifty `get_item_images` returns at most 4 photos per call; check
  `totalPictures` and page with `offset` to see the rest.
- Nifty's AI can misread handwritten measurement cards (it read sleeve 21"
  as 27"). Always compare the card to the description.
- The Nifty connector can't read the automated-offer settings. Ask Jade.
- Items may already be live with a SKU and price. Keep the existing SKU, and
  if the price is already right, don't edit or apply (applying republishes).
- Check each marketplace listing's own Brand attribute, not just the item's.
  Depop got "Unique Vintage" for a Mainstream swimsuit.

- Video files are ignored by git (`.gitignore`), so they never get pushed.
  Keep them on the computer.
