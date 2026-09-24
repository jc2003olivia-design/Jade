# Label Printer / Label Maker

## Printer
- Model:
- Label size: 4" × 4" thermal
- App / software:

## Label types
- Shipping labels:
- Price tags (pop-ups):
- Inventory / SKU labels: 4×4 thermal, PDF, one label per page.
  SKU in big bold type at the top, then the item title (no date; the SKU
  has it). Say "make labels" after listing a batch; Claude pulls the
  current titles from Nifty and runs `make_labels.py`. PDFs are saved in
  `labels/`.

## Setup notes
- Make labels by hand:
  `python3 06-label-printer/make_labels.py items.json -o labels.pdf`
  (see the top of the script for the `items.json` format).
