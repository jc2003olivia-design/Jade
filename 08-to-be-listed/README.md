# To Be Listed

Drop product photos here, one folder per clothing piece, named by number:

```
08-to-be-listed/
├── 1/          IMG_0001.jpg, IMG_0002.jpg, ... (last photo = measurements)
├── 2/
└── 3/
```

- **One folder per item**, named with just a number (`1`, `2`, `3`...).
- **Last photo is always the measurements photo** (ruler / tape on the item).
- Add the Nifty SKU to the folder name if you have it, e.g. `1 - 0924-01`.
  That makes matching to Nifty exact. Otherwise Claude matches by photos.
- JPG or PNG works best. iPhone HEIC photos are OK but slower.
- This repo is public, so only put product photos here: no faces, addresses
  or order info.

Optional but best: on your computer (Claude desktop app with Claude in
Chrome), say **"pull sold comps"**. It saves real sold prices to each
folder as `comps.md`.

Then tell Claude **"start listing workflow"**. For each numbered folder,
Claude writes a `report.md` next to the photos with the comps, price,
title notes and measurement check. After you list the items and say
**"make labels"**, Claude sends the labels and then empties these folders
(photos, comps, reports) so they're ready for the next batch. Git keeps the
history.
