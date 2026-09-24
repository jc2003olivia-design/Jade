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
│   ├── whatnot-covers/          Whatnot show cover mockups
│   └── titles.md
├── 03-customer-support/         Messages, returns, problem orders
│   └── customer-support.md
├── 04-online-selling/           One file per marketplace
│   ├── depop.md
│   ├── ebay.md
│   └── poshmark.md
├── 05-pop-up-markets/           In-person markets (add a file per event)
│   └── planning.md
├── 06-label-printer/            Label printer setup and templates
│   ├── label-printer.md
│   ├── labels/                  Printed label PDFs saved here
│   └── make_labels.py
├── 07-videos/                   All videos, one folder per video
│   └── 01 video
├── 08-to-be-listed/             Product photos waiting to be priced/listed
│                                (one numbered folder per item)
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
