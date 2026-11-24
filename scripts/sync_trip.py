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


# Legs of the trip, from the confirmed bookings (Matt's emails, Nov 2026):
#   Nov 22 FAI→SEA→TPE→BKK, lands Nov 24 12:35 · Bangkok hotel nights Nov 23–24
#   Nov 25 PG1201 BKK→CNX · Nov 30 DD123/DD542 CNX→DMK→KBV · Dec 6 FD4401 KBV→BKK
#   Dec 8 21:40 KE658 BKK→ICN (11h25 Seoul layover) → KE41 SEA → AS656 FAI, Dec 9.
# from/to = days a leg's dishes can fall on (travel days overlap two legs; a dish goes to the
# leg matching its region). own = the days the leg owns, so each day is listed once.
# regions = which dish regions belong to the leg; region = the leg's colour.
# abbr = label on phones, where the leg's slice of the strip is too thin for the full name.
LEGS = [
    {"name": "Getting there", "abbr": "Out", "from": "2026-11-22", "to": "2026-11-24", "own": ["2026-11-22", "2026-11-23"],
     "regions": ["transit"], "region": "transit"},
    {"name": "Bangkok", "abbr": "BKK", "from": "2026-11-24", "to": "2026-11-25", "own": ["2026-11-24", "2026-11-24"],
     "regions": ["bangkok"], "region": "bangkok"},
    {"name": "Chiang Mai", "from": "2026-11-25", "to": "2026-11-30", "own": ["2026-11-25", "2026-11-29"],
     "regions": ["chiang-mai", "chiang-rai", "doi-inthanon"], "region": "chiang-mai"},
    {"name": "Koh Lanta", "from": "2026-11-30", "to": "2026-12-06", "own": ["2026-11-30", "2026-12-05"],
     "regions": ["koh-lanta"], "region": "koh-lanta"},
    {"name": "Bangkok", "from": "2026-12-06", "to": "2026-12-08", "own": ["2026-12-06", "2026-12-08"],
     "regions": ["bangkok"], "region": "bangkok"},
    {"name": "Seoul / return travel", "abbr": "SEL", "from": "2026-12-08", "to": "2026-12-09", "own": ["2026-12-09", "2026-12-09"],
     "regions": ["transit"], "region": "transit"},
]

# Journal-only days after the planner's last day (the flight home crosses into Dec 9).
EXTRA_DAYS = [
    {"date": "2026-12-09", "location": "Seoul → home", "foodHint": None,
     "plan": {"morning": "Land at Seoul Incheon early (KE658); ~11.5 h layover, out through customs.",
              "afternoon": "KE41 Seoul → Seattle, then AS656 → Fairbanks.", "evening": "Home ~3 PM."}},
]


def owning_leg(date):
    for leg in LEGS:
        if leg["own"][0] <= date <= leg["own"][1]:
            return leg
    return None


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
            # Day colour comes from the leg that owns the day (the planner's wording can lag the bookings).
            "region": (owning_leg(date) or {}).get("region") or region_for(loc),
            "foodHint": food_hint(d),
            "plan": {k: first_line(d.get(k, "")) for k in ("morning", "afternoon", "evening")},
        })
    have = {d["date"] for d in out_days}
    for extra in EXTRA_DAYS:
        if extra["date"] not in have:
            out_days.append({**extra, "region": owning_leg(extra["date"])["region"]})
    out_days.sort(key=lambda d: d["date"])
    trip = {
        "name": meta["name"],
        "country": meta["country"],
        "start": meta["start"],
        "end": max(meta["end"], out_days[-1]["date"]),
        "regions": REGION_NAMES,
        "legs": LEGS,
        "days": out_days,
    }
    (ROOT / "data/trip.json").write_text(json.dumps(trip, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote data/trip.json — {len(out_days)} days, {trip['start']} → {trip['end']}")


if __name__ == "__main__":
    main()
