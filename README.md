# Jade — KennyShop / Kurated by Kenny

Business workspace, organized by area.

## Folder map

```
Jade
├── 01-product-research/         Research, pricing, sourcing
│   └── product-research-pricing-sourcing.md
├── 02-branding/                 Look and feel of the shop
│   ├── brand-ideas-planning.md
│   ├── thumbnail-maker.md
│   ├── titles.md
│   └── whatnot-covers/          Whatnot show cover mockups
│       ├── color_options.py
│       ├── for-the-girls.png
│       ├── fonts/
│       │   ├── Anton-Regular.ttf
│       │   ├── Montserrat-ExtraBold.ttf
│       │   ├── Montserrat-Medium.ttf
│       │   ├── OFL-Anton.txt
│       │   ├── OFL-Montserrat.txt
│       │   ├── OFL-PlayfairDisplay.txt
│       │   ├── PlayfairDisplay-Bold.ttf
│       │   └── PlayfairDisplay-Regular.ttf
│       ├── logos/
│       │   ├── anthropologie.png
│       │   ├── free-people-movement.png
│       │   ├── free-people.png
│       │   ├── lululemon.png
│       │   ├── nike.svg
│       │   ├── polo-ralph-lauren.png
│       │   ├── ralph-lauren.png
│       │   └── skims.png
│       ├── logos-preview.png
│       ├── make_covers.py
│       ├── options-activewear.png
│       ├── options-contemporary.png
│       ├── options-for-the-girls.png
│       ├── premium-activewear.png
│       ├── premium-contemporary.png
│       └── preview-feed-size.png
├── 03-customer-support/         Messages, returns, problem orders
│   └── customer-support.md
├── 04-online-selling/           One file per marketplace
│   ├── depop.md
│   ├── ebay.md
│   ├── poshmark.md
│   └── whatnot.md           How to run the Whatnot shows (with sources)
├── 05-pop-up-markets/           In-person markets (add a file per event)
│   └── planning.md
├── 06-label-printer/            Label printer setup and templates
│   ├── label-printer.md
│   ├── labels/                  Printed label PDFs saved here
│   │   ├── .gitkeep
│   │   ├── sku-labels-2026-09-24.pdf
│   │   └── sku-labels-2026-09-28.pdf
│   └── make_labels.py
├── 07-videos/                   All videos, one folder per video
│   └── 01 video
├── 08-to-be-listed/             Reports + comps for items being listed (photos are in Nifty)
│   ├── 1/                       (one <SKU> folder per item)
│   │   └── .gitkeep
│   ├── 2/
│   │   └── .gitkeep
│   ├── 3/
│   │   └── .gitkeep
│   ├── 4/
│   │   └── .gitkeep
│   ├── 5/
│   │   └── .gitkeep
│   ├── 6/
│   │   └── .gitkeep
│   ├── 7/
│   │   └── .gitkeep
│   ├── 8/
│   │   └── .gitkeep
│   ├── 9/
│   │   └── .gitkeep
│   └── 10/
│       └── .gitkeep
├── CLAUDE.md                    Rules Claude follows in this workspace
├── LESSONS.md                   What Claude has learned; grows as it works
├── .gitignore                   Tells git to skip video files
└── .claude/                     Behind the scenes: Claude's tools
    └── skills/video-use/        The video editing tool
```

Folders also have a `README.md` describing what goes in them (not shown above).

## Where videos go
Every video lives in `07-videos/`, whatever it's for: a Depop listing, a
TikTok for branding, a pop-up recap. Name the folder after what it is, e.g.
`07-videos/2026-10-depop-nike-jacket/`. The video editing tool itself is
in `.claude/` and works on any of them.
