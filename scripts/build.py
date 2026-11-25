#!/usr/bin/env python3
"""Validate the journal data and bundle it for the site.

Reads data/trip.json + data/entries.json, checks every entry, and writes
site/data.js (window.JOURNAL = {...}). The page loads data.js and photos/*.

Usage: python3 scripts/build.py
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Food score rubric: each question 1–10; dish score = weighted average (also 1–10).
# Ambiance is recorded per meal but never counts toward the food scores.
# Weights are percent of the score (sum 100). Order = the order questions are asked/sent.
RUBRIC = {"flavour": 50, "texture": 20, "value": 20, "presentation": 10}


def dish_score(qs, eid, label):
    missing = [k for k in RUBRIC if not isinstance(qs.get(k), (int, float))]
    if missing:
        fail(f"{eid}: {label} scores missing {missing}")
    for k, v in qs.items():
        if k not in RUBRIC:
            fail(f"{eid}: unknown {label} score '{k}' (use {list(RUBRIC)})")
        if not 1 <= v <= 10:
            fail(f"{eid}: {label}.{k} must be 1–10")
    # Round half up to one decimal — must match weighted() in site/index.html.
    return math.floor(sum(qs[k] * w for k, w in RUBRIC.items()) * 10 / sum(RUBRIC.values()) + 0.5) / 10


# Local currency per US dollar (approximate, fixed for the trip). THB from the Atlas plan (Nov 11);
# TWD from converters around Nov 19, 2026. Add a currency here before using it in an entry.
FX = {"USD": 1, "THB": 33.5, "TWD": 32.9}


def check_amount(v, eid, label):
    if not isinstance(v, (int, float)) or v < 0:
        fail(f"{eid}: {label} must be a non-negative number")


MEALS = {"breakfast", "lunch", "dinner", "snack", "dessert", "drink", "market"}


def avg_score(vals):
    # Round half up to one decimal — must match avg() in site/index.html.
    return math.floor(sum(vals) * 10 / len(vals) + 0.5) / 10


def fail(msg):
    sys.exit(f"build: {msg}")


def main():
    trip = json.loads((ROOT / "data/trip.json").read_text())
    entries = json.loads((ROOT / "data/entries.json").read_text())
    dates = {d["date"]: d for d in trip["days"]}
    ids = set()
    for e in entries:
        eid = e.get("id") or fail(f"entry without id: {e}")
        if eid in ids:
            fail(f"duplicate id {eid}")
        ids.add(eid)
        if e.get("date") not in dates:
            fail(f"{eid}: date {e.get('date')} is not a trip day")
        if not e.get("dish"):
            fail(f"{eid}: missing dish")
        if e.get("meal") and e["meal"] not in MEALS:
            fail(f"{eid}: meal must be one of {sorted(MEALS)}")
        sc = e.get("scores") or {}
        if e.get("meal") == "drink":
            # Drinks: ONE overall score, no four-question rubric.
            if "main" in sc:
                fail(f"{eid}: drinks take one overall score — use scores.overall, not scores.main")
            if "overall" in sc:
                if not isinstance(sc["overall"], (int, float)) or not 1 <= sc["overall"] <= 10:
                    fail(f"{eid}: scores.overall must be 1–10")
                e["rating"] = sc["overall"]
        elif "overall" in sc:
            fail(f"{eid}: scores.overall is for drinks only (meal: drink)")
        if e.get("meal") == "market":
            # Street market: many small items, each ONE flat 1–10 score + a blurb.
            # The market's score is the average of its scored items.
            if sc:
                fail(f"{eid}: markets score each item (items[].rating), not scores")
            items = e.get("items")
            if not isinstance(items, list) or not items:
                fail(f"{eid}: a market needs items: [{{name, rating?, note?}}]")
            seen = set()
            for it in items:
                if not isinstance(it, dict) or not it.get("name"):
                    fail(f"{eid}: market items must be objects with a name")
                if it["name"] in seen:
                    fail(f"{eid}: duplicate market item {it['name']}")
                seen.add(it["name"])
                ir = it.get("rating")
                if ir is not None and not (isinstance(ir, (int, float)) and 1 <= ir <= 10):
                    fail(f"{eid}: market item '{it['name']}' rating must be 1–10")
            rs = [it["rating"] for it in items if isinstance(it.get("rating"), (int, float))]
            if rs:
                e["rating"] = avg_score(rs)
        elif "items" in e:
            fail(f"{eid}: items are for markets only (meal: market)")
        if "main" in sc:
            e["rating"] = dish_score(sc["main"], eid, "main")
        if "sides" in sc:
            fail(f"{eid}: sides take one overall score — use sides.rating, not scores.sides")
        a = e.get("ambiance")
        if a is not None and not (1 <= a <= 10):
            fail(f"{eid}: ambiance must be 1–10")
        r = e.get("rating")
        if r is not None and not (0 <= r <= 10):
            fail(f"{eid}: rating must be 0–10")
        sides = e.get("sides")
        if sides is not None:
            if not isinstance(sides.get("items", []), list):
                fail(f"{eid}: sides.items must be a list")
            # Items are plain names, or {"name", "rating"?, "note"?} for noteworthy sides.
            for it in sides.get("items", []):
                if isinstance(it, dict):
                    if not it.get("name"):
                        fail(f"{eid}: side item without a name")
                    ir = it.get("rating")
                    if ir is not None and not (1 <= ir <= 10):
                        fail(f"{eid}: side '{it['name']}' rating must be 1–10")
                elif not isinstance(it, str):
                    fail(f"{eid}: side items must be names or objects")
            sr = sides.get("rating")
            if sr is not None and not (0 <= sr <= 10):
                fail(f"{eid}: sides.rating must be 0–10")
        # Dessert: like sides but ONE overall score — {"rating"?, "items": [names], "note"?}.
        dz = e.get("dessert")
        if dz is not None:
            if not isinstance(dz.get("items", []), list) or not all(isinstance(x, str) for x in dz.get("items", [])):
                fail(f"{eid}: dessert.items must be a list of names")
            dr = dz.get("rating")
            if dr is not None and not (1 <= dr <= 10):
                fail(f"{eid}: dessert.rating must be 1–10")
        # Legacy single price in baht → per-item price object.
        if "priceThb" in e:
            e.setdefault("price", {"currency": "THB", "main": e.pop("priceThb")})
            if e.get("priceNote"):
                e["price"]["note"] = e.pop("priceNote")
        pr = e.get("price")
        if pr is not None:
            if pr.get("currency") not in FX:
                fail(f"{eid}: price.currency must be one of {list(FX)}")
            if "main" in pr:
                check_amount(pr["main"], eid, "price.main")
            for n, a in (pr.get("sides") or {}).items():
                check_amount(a, eid, f"price.sides[{n}]")
        for p in e.get("photos", []):
            if not re.fullmatch(r"photos/[a-z0-9-]+\.jpg", p["src"]):
                fail(f"{eid}: bad photo path {p['src']}")
            if not (ROOT / p["src"]).exists():
                fail(f"{eid}: photo missing on disk {p['src']}")
        # Region defaults to the itinerary's region for that day.
        e.setdefault("region", dates[e["date"]]["region"])
        if e["region"] not in trip["regions"]:
            fail(f"{eid}: unknown region {e['region']}")
    order = {m: i for i, m in enumerate(["breakfast", "lunch", "snack", "dinner", "market", "dessert", "drink"])}
    entries.sort(key=lambda e: (e["date"], e.get("time") or "", order.get(e.get("meal"), 9)))
    bundle = {"trip": trip, "rubric": RUBRIC, "fx": FX, "entries": entries}
    js = "window.JOURNAL = " + json.dumps(bundle, ensure_ascii=False, indent=1) + ";\n"
    (ROOT / "site/data.js").write_text(js)
    print(f"build: {len(entries)} entries, {sum(len(e.get('photos', [])) for e in entries)} photos → site/data.js")


if __name__ == "__main__":
    main()
