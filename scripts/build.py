#!/usr/bin/env python3
"""Validate the journal data and bundle it for the site.

Reads data/trip.json + data/entries.json, checks every entry, and writes
site/data.js (window.JOURNAL = {...}). The page loads data.js and photos/*.

Usage: python3 scripts/build.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEALS = {"breakfast", "lunch", "dinner", "snack", "dessert", "drink"}


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
        r = e.get("rating")
        if r is not None and not (0 <= r <= 10):
            fail(f"{eid}: rating must be 0–10")
        if e.get("priceThb") is not None and e["priceThb"] < 0:
            fail(f"{eid}: negative price")
        for p in e.get("photos", []):
            if not re.fullmatch(r"photos/[a-z0-9-]+\.jpg", p["src"]):
                fail(f"{eid}: bad photo path {p['src']}")
            if not (ROOT / p["src"]).exists():
                fail(f"{eid}: photo missing on disk {p['src']}")
        # Region defaults to the itinerary's region for that day.
        e.setdefault("region", dates[e["date"]]["region"])
        if e["region"] not in trip["regions"]:
            fail(f"{eid}: unknown region {e['region']}")
    order = {m: i for i, m in enumerate(["breakfast", "lunch", "snack", "dinner", "dessert", "drink"])}
    entries.sort(key=lambda e: (e["date"], e.get("time") or "", order.get(e.get("meal"), 9)))
    bundle = {"trip": trip, "entries": entries}
    js = "window.JOURNAL = " + json.dumps(bundle, ensure_ascii=False, indent=1) + ";\n"
    (ROOT / "site/data.js").write_text(js)
    print(f"build: {len(entries)} entries, {sum(len(e.get('photos', [])) for e in entries)} photos → site/data.js")


if __name__ == "__main__":
    main()
