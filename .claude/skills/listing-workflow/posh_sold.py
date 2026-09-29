#!/usr/bin/env python3
"""Poshmark sold comps for one search, printed as a markdown table.

Reads Poshmark's public search page (sold filter, newest listings first)
and pulls the listing data that page already contains. Looks only: no
login, no listing pages, a few pages per search.

    python3 posh_sold.py "jude connally sleeveless top"
    python3 posh_sold.py "nutmeg tennessee crewneck" --size XL --days 120
    python3 posh_sold.py "mainstream swimsuit" --pages 2 --json out.json

Columns: sold date, days to sell, first asking price -> last listed price,
original retail (as the seller typed it), size, condition, title, link.
Poshmark hides accepted offers, so "sold at" is the last listed price.
The real sale was often a bit lower.
"""
import argparse
import json
import statistics
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = "JadeListingResearch/1.0 (+https://github.com/jc2003olivia-design/Jade)"
CONDITION = {"nwt": "NWT", "ret": "NWT (boutique)", "not_nwt": "used",
             "uln": "like new", "ug": "good", "uf": "fair"}


def fetch(query, availability, page):
    params = {"query": query, "availability": availability,
              "sort_by": "added_desc"}
    if page > 1:
        params["max_id"] = page
    url = "https://poshmark.com/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", "replace")
    i = html.find("__INITIAL_STATE__")
    if i < 0:
        raise RuntimeError("no listing data on the page (blocked or changed?)")
    state, _ = json.JSONDecoder().raw_decode(html[html.find("{", i):])
    grid = state["$_search"]["gridData"]
    return grid.get("data", []), grid.get("more", {}).get("total")


def money(obj):
    try:
        v = float((obj or {}).get("val") or 0)
    except (TypeError, ValueError):
        return None
    return v or None


def when(s):
    return datetime.fromisoformat(s) if s else None


def parse(it):
    inv = it.get("inventory") or {}
    listed = when(it.get("first_published_at"))
    sold = when(inv.get("status_changed_at")) if inv.get("status") == "sold_out" else None
    return {
        "title": " ".join((it.get("title") or "").split()),
        "brand": it.get("brand") or "",
        "size": (it.get("size_obj") or {}).get("display") or "",
        "condition": CONDITION.get(it.get("condition"), it.get("condition") or "?"),
        "first_price": money(it.get("first_user_price_amount")),
        "price": money(it.get("price_amount")),
        "retail": money(it.get("original_price_amount")),
        "listed": listed.date().isoformat() if listed else "",
        "sold": sold.date().isoformat() if sold else "",
        "days_to_sell": (sold - listed).days if sold and listed else None,
        "likes": (it.get("aggregates") or {}).get("likes"),
        "link": f"https://poshmark.com/listing/{it.get('id')}",
        "_sold_dt": sold,
    }


def fmt(v):
    return f"${v:,.0f}" if v else "—"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query")
    ap.add_argument("--days", type=int, default=90, help="only sales this recent (default 90)")
    ap.add_argument("--pages", type=int, default=2, help="sold pages to read, 48 per page (default 2, max 4)")
    ap.add_argument("--size", help="only keep this size (e.g. S, XL, 8)")
    ap.add_argument("--json", help="also save the rows to this JSON file")
    a = ap.parse_args()

    rows, sold_total = [], None
    for p in range(1, min(a.pages, 4) + 1):
        data, total = fetch(a.query, "sold_out", p)
        sold_total = sold_total or total
        rows += [parse(x) for x in data]
        if len(data) < 48:
            break
        time.sleep(2)
    time.sleep(2)
    _, active_total = fetch(a.query, "available", 1)

    now = datetime.now(timezone.utc)
    rows = [r for r in rows if r["_sold_dt"] and (now - r["_sold_dt"]).days <= a.days]
    if a.size:
        rows = [r for r in rows if r["size"].strip().lower() == a.size.strip().lower()]
    rows.sort(key=lambda r: r["_sold_dt"], reverse=True)

    print(f"### Poshmark sold: \"{a.query}\"" + (f" (size {a.size})" if a.size else ""))
    print(f"Pulled {now.date()} · sold in last {a.days} days: {len(rows)} · "
          f"all-time sold matching: {sold_total} · listed now: {active_total}\n")
    print("| Sold | Days to sell | First ask → sold at | Retail | Size | Cond. | Title | Link |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        dts = "" if r["days_to_sell"] is None else r["days_to_sell"]
        print(f"| {r['sold']} | {dts} | {fmt(r['first_price'])} → {fmt(r['price'])} | "
              f"{fmt(r['retail'])} | {r['size']} | {r['condition']} | "
              f"{r['title'][:70].replace('|', '/')} | {r['link']} |")

    prices = [r["price"] for r in rows if r["price"]]
    if prices:
        days = [r["days_to_sell"] for r in rows if r["days_to_sell"] is not None]
        fast = [r["price"] for r in rows if r["price"] and r["days_to_sell"] is not None
                and r["days_to_sell"] <= 30]
        drops = [1 - r["price"] / r["first_price"] for r in rows
                 if r["price"] and r["first_price"] and r["first_price"] > r["price"]]
        print(f"\n**All rows:** {len(prices)} sold · median {fmt(statistics.median(prices))} · "
              f"range {fmt(min(prices))}–{fmt(max(prices))}")
        if fast:
            print(f"**Sold within 30 days of listing:** {len(fast)} · median {fmt(statistics.median(fast))}")
        if days:
            print(f"**Median days to sell:** {statistics.median(days):.0f}")
        if drops:
            print(f"**Price drops:** {len(drops)} of {len(prices)} dropped before selling, "
                  f"median drop {statistics.median(drops):.0%}")
        retail = [r["retail"] for r in rows if r["retail"]]
        if retail:
            print(f"**Original retail (seller-typed):** median {fmt(statistics.median(retail))}")
    print("\nThese are all rows for the search. Mark each as exact / close / loose "
          "against the item before pricing; price from exact and close only.")

    if a.json:
        with open(a.json, "w") as f:
            json.dump([{k: v for k, v in r.items() if not k.startswith("_")} for r in rows], f, indent=1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # keep the workflow moving; the caller falls back to other sources
        print(f"posh_sold.py failed: {e}", file=sys.stderr)
        sys.exit(1)
