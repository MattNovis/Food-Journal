#!/usr/bin/env python3
"""Snapshot the Thailand itinerary from atlas-trip-studio into data/trip.json.

The journal never reads Atlas at runtime: this copies just what the site needs
(dates, where you were, the plan for each day) so the repo stays self-contained.

Usage: python3 scripts/sync_trip.py [path/to/atlas-trip-studio]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATLAS = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "atlas-trip-studio"
TRIP = ATLAS / "data/trips/thailand-solo"

# Region keys drive colour and grouping in the site. First match wins, checked
# against the *destination* end of a travel day ("Bangkok → Chiang Mai" = Chiang Mai).
REGIONS = [
    ("transit", ["In transit"]),
    ("chiang-rai", ["Chiang Rai"]),
    ("doi-inthanon", ["Doi Inthanon"]),
    ("chiang-mai", ["Chiang Mai"]),
    ("koh-lanta", ["Koh Lanta", "Lanta", "Krabi"]),
    ("bangkok", ["Bangkok", "home"]),
]
REGION_NAMES = {
    "transit": "Travel",
    "bangkok": "Bangkok",
    "chiang-mai": "Chiang Mai",
    "chiang-rai": "Chiang Rai",
    "doi-inthanon": "Doi Inthanon",
    "koh-lanta": "Koh Lanta",
}


def region_for(location: str) -> str:
    dest = location.split("→")[-1].strip()
    for key, needles in REGIONS:
        if any(n.lower() in dest.lower() for n in needles):
            return key
    return "transit"


FOOD_WORDS = re.compile(r"cooking|food|dinner|seafood|market|walking street|breakfast|lunch", re.I)


def food_hint(day: dict):
    """First itinerary sentence that mentions food — shown on days with no entries yet."""
    for k in ("morning", "afternoon", "evening"):
        for s in re.split(r"(?<=[.;\n])\s+", day.get(k, "")):
            if FOOD_WORDS.search(s):
                return s.strip().rstrip(";")
    return None


# Legs of the trip, mirroring the travel planner's share page
# (atlas-trip-studio/scripts/share-page.js → LEGS['thailand-solo']). Update both together.
LEGS = [
    {"name": "Getting there", "from": "2026-11-22", "to": "2026-11-23", "region": "transit"},
    {"name": "Chiang Mai & Yi Peng", "from": "2026-11-24", "to": "2026-11-27", "region": "chiang-mai"},
    {"name": "Doi Inthanon", "from": "2026-11-28", "to": "2026-11-29", "region": "doi-inthanon"},
    {"name": "Chiang Mai & Monk Chat", "from": "2026-11-30", "to": "2026-11-30", "region": "chiang-mai"},
    {"name": "Koh Lanta", "from": "2026-12-01", "to": "2026-12-05", "region": "koh-lanta"},
    {"name": "Bangkok & home", "from": "2026-12-06", "to": "2026-12-08", "region": "bangkok"},
]


def first_line(text: str) -> str:
    return (text or "").split("\n")[0].strip()


def main():
    meta = json.loads((TRIP / "meta.json").read_text())
    days = json.loads((TRIP / "days.json").read_text())
    out_days = []
    for date in sorted(days):
        d = days[date]
        loc = d.get("location", "")
        out_days.append({
            "date": date,
            "location": loc,
            "region": region_for(loc),
            "foodHint": food_hint(d),
            "plan": {k: first_line(d.get(k, "")) for k in ("morning", "afternoon", "evening")},
        })
    trip = {
        "name": meta["name"],
        "country": meta["country"],
        "start": meta["start"],
        "end": meta["end"],
        "regions": REGION_NAMES,
        "legs": LEGS,
        "days": out_days,
    }
    (ROOT / "data/trip.json").write_text(json.dumps(trip, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote data/trip.json — {len(out_days)} days, {trip['start']} → {trip['end']}")


if __name__ == "__main__":
    main()
