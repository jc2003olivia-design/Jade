# Label Printer / Label Maker

## Printer
- Model:
- Label size: 4" × 4" thermal
- App / software:

## Label types
- Shipping labels:
- Price tags (pop-ups):
- Inventory / SKU labels: 4×4 thermal, PDF, one label per page.
  SKU in big bold type at the top, then the item title, then the date it
  was first listed. Made by `make_labels.py` at the end of the listing
  workflow; PDFs are saved in `labels/`.

## Setup notes
- Make labels by hand:
  `python3 06-label-printer/make_labels.py items.json -o labels.pdf`
  (see the top of the script for the `items.json` format).
