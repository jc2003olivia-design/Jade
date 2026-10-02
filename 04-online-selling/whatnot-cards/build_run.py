"""Build the Oct 2 run of show: item cards in running order plus script cards.

    python3 04-online-selling/whatnot-cards/build_run.py

Reads 2026-10-02-show.json, writes 2026-10-02-run-of-show.json. Then:
    python3 make_cards.py 2026-10-02-run-of-show.json -o 2026-10-02-run-of-show.pdf

Times are a guide only [Test]: about 45 s per regular piece, 60 s per flash
sale, 90 s per hero (whatnot.md).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
items = {c["n"]: c for c in json.load(open(HERE / "2026-10-02-show.json"))}

NEXT_SHOW = ("[Day] at [time] is Premium Activewear night: Lululemon, "
             "Free People Movement, Nike")
GIVEAWAY_RULE = ("Whatnot rule: say NO PURCHASE NECESSARY every time you "
                 "mention a giveaway, and say the prize before it runs.")

S = lambda **k: dict(kind="script", **k)

PRE = S(head="BEFORE YOU GO LIVE", time="before", title="Pre-show checklist",
    checklist=[
        "Delist every piece from Depop, Poshmark and eBay (the 6 flash pieces are live there now)",
        "Flash timers set to 30 sec; Condition filled in on every Whatnot listing",
        "2 follower-only giveaways set up: Reoria bodysuit (M) and Havaianas slides (7/8)",
        "Giveaway Official Rules pasted in Show Notes (template in whatnot.md)",
        "Pieces racked in card order, measurement card clipped to each",
        "Fill in start prices, sizes and condition on the cards",
        "Phone on tripod, two lights on, Live Analytics open on laptop",
        "Post-its and pen for winner names",
    ],
    tip="Pull #11 (bra) unless it has never been worn. #15 is the old generic Levi's card: skip it, #28–31 cover each pair.")

OPEN = S(head="OPEN", title="Opening (60–90 sec)",
    say=("Hey, welcome in! I'm Jade, this is Kenny Shop, and tonight is Premium Contemporary. "
         "Auctions start at [one dollar], and I've got 20%-off flash sales running all night. "
         "I hand-pick every piece: Free People, Anthropologie, Citizens of Humanity, AGOLDE, "
         "Levi's, Michael Kors, and I check every piece for flaws before it goes on camera.\n"
         "[@name], welcome back! Thank you all for being here. Two follower giveaways tonight, "
         "the first in about 15 minutes. No purchase necessary. What size are you hunting tonight? Drop it in "
         "the chat. First piece coming right now!"),
    tip="Get the first piece on camera by 1:30. Only say 'I check every piece' if you did.")

SHIP = S(head="SAY ONCE NOW", title="Shipping line",
    say=("Everything you win tonight ships together in one box, and once your box is between "
         "1 and 5 pounds, shipping stays at $7.75 no matter how many pieces you add."),
    tip="Say it again around the 30-min mark. If you set a shipping cap, say 'Shipping maxes out at $[cap] tonight' instead.")

def repeat(extra, tip):
    return S(head="REPEAT BLOCK", title="New viewers (30 sec)",
        say=("If you just joined, welcome! I'm Jade, this is Kenny Shop, Premium Contemporary. "
             "[@repeat buyer], thank you! If you're new, tap follow. " + extra +
             "\nCan't stay? Tap the shop: the Buy It Now tab has the flash-sale pieces at full price right now."),
        tip=tip)

R1 = repeat("Follower giveaway in 5 minutes. No purchase necessary.",
            "Also do a repeat block any time a raid comes in or viewers jump.")
R2 = repeat("Next giveaway in about 10 minutes. No purchase necessary.",
            "Check Live Analytics: rising or falling? Note it in the show log.")
R3 = repeat("Giveaway starting right now. No purchase necessary.",
            "Then go straight into the giveaway card.")

def giveaway(prize, when):
    return S(head="GIVEAWAY", title=f"Follower giveaway {when}",
        say=("Giveaway is live! Tap Enter at the top of your screen. NO PURCHASE NECESSARY. "
             f"The prize is {prize}. You have to be in the show when it draws, in [five] minutes. "
             "Full rules are in the show notes."),
        checklist=["Start the giveaway in the app", "Keep auctioning while it runs (allowed)",
                   "Shout out the winner by name", "Never change the prize after it's drawn"],
        tip=GIVEAWAY_RULE + " You pay its shipping from your Whatnot balance.")

G1 = giveaway("a Reoria deep V bodysuit, rust, size medium, pre-owned [condition]", "#1")
G2 = giveaway("Havaianas slide sandals, women's 7/8, chevron strap with gold trim, pre-owned [condition]", "#2")

PROMO = S(head="PROMOTE NEXT SHOW", title="Bookmark the next show",
    say=(f"Quick thing before the next piece: {NEXT_SHOW}. Tap my profile and hit bookmark on that "
         "show, you'll get a notification the second I go live.\n"
         "And if you're new, tap follow so you see every show I schedule."),
    checklist=["If viewers are at their peak, Boost the next hero (Citizens of Humanity, #27)",
               "Say the shipping line again"],
    tip="Fill in the day/time before printing. Bookmark prompts are one of Whatnot's top-seller habits.")

TEASE = S(head="HEADS UP", title="Tease the last hero",
    say=("Stay right here: the last big piece of the night is a Michael Kors crossbody, "
         "coming up in a few minutes. Don't leave yet!"),
    tip="Say this while the piece before it is running. It keeps viewers to the end.")

CLOSE = S(head="CLOSE", title="Closing (2–3 min)",
    say=("That's the show! Thank you so much, [@top buyers], [@new buyers]. Every order ships within "
         f"two business days.\nTap bookmark on my next show: {NEXT_SHOW}. "
         "You'll get a notification the second I go live.\n"
         "Now we're raiding my friend [@seller]. Go say hi!"),
    tip="Raiding ends your stream and sends your viewers to them.")

POST = S(head="AFTER THE SHOW", time="after", title="Post-show checklist",
    checklist=["Ship within 2 business days; scan each box with the Whatnot app at drop-off",
               "Check cancellation requests (buyers have 24 hours)",
               "Relist unsold pieces on Depop, Poshmark and eBay, or keep them for the next show",
               "Clip your best moment and post it with the next show link",
               "Log the show in whatnot.md from Seller Analytics (keeps 30 days only)",
               "Tell Claude what sold and for how much, to tighten next show's prices"])

# Running order. Ints are item cards; heroes about every 8-10 min.
ORDER = [PRE, OPEN,
         20, 13, SHIP, 1, 16, 26, 10,
         22,                      # hero: Daily Practice $118 NWT
         9, 2, 30, 21,
         R1, 14,                  # hero: AGOLDE Parker Long
         19, 3,                   # flash: FP cowl, strongest fall piece, right before giveaway
         G1, 28, 7, 4, 24,
         17,                      # hero: VS PJ set NWT (gift angle)
         R2, PROMO, 31, 25, 5, 23,
         27,                      # hero: Citizens of Humanity Annina
         29, 11, 32, 6,
         R3, G2, 33, 18, 35, TEASE, 8,
         34,                      # hero: Michael Kors bag, last
         CLOSE, POST]

HERO = {22, 14, 17, 27, 34, 3}
SECS = lambda c: 90 if c in HERO else (60 if items[c]["type"].startswith("FLASH") else 45)
SCRIPT_SECS = {"OPEN": 90, "SAY ONCE NOW": 20, "REPEAT BLOCK": 30, "GIVEAWAY": 40,
               "PROMOTE NEXT SHOW": 30, "HEADS UP": 15, "CLOSE": 150}

out, t = [], 0
for i, c in enumerate(ORDER):
    card = dict(items[c]) if isinstance(c, int) else dict(c)
    card["run"] = i
    if "time" not in card:
        card["time"] = f"~{t // 60}:{t % 60:02d}"
    if isinstance(c, int):
        if c in HERO and "HERO" not in card["type"]:
            card["type"] += " · HERO"
        t += SECS(c)
    else:
        t += SCRIPT_SECS.get(card["head"], 0)
    out.append(card)

json.dump(out, open(HERE / "2026-10-02-run-of-show.json", "w"), indent=1, ensure_ascii=False)
used = {c for c in ORDER if isinstance(c, int)}
print(len(out), "cards;", len(used), "pieces; show ends ~", t // 60, "min")
print("not in run:", sorted(set(items) - used))
