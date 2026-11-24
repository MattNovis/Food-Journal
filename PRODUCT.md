# Product: Dishspatch (Thailand food journal)

Name: **Dishspatch**, dish + dispatch: "dispatches from Thailand, one dish at a time".

**What:** A visual journal of every dish eaten on the Thailand trip (22 Nov – 8 Dec 2026, two travelers),
published as a private claude.ai Artifact. This repo is the data source.

**Who:** Matt, posting from a phone mid-trip, and later anyone he shares the link with.

**Job:** Send Claude a photo + a quick line ("khao soi at X, 60 baht, 9/10"). Claude turns it into a
complete, beautiful entry in seconds. Afterwards the page reads like a food memoir of the trip.

**Each entry:** photo(s), dish (English + Thai if known), description in Matt's words,
place/vendor, price in THB (USD shown at ~33.5), rating out of 10, date and meal. City and day come from the itinerary.

**Itinerary source:** `atlas-trip-studio/data/trips/thailand-solo` → snapshot in `data/trip.json`.

**Brand:** tropical, kept simple (palette only, no decorative motifs). See DESIGN.md.
**Layout:** a hamburger menu at the top right of a sticky bar opens four views: **Home** (leg strip, Top 3 meals, scoring chart) ·
**Legs** (leg strip, then dishes grouped by leg) · **Day by day** (numbered day buttons, then every day) ·
**Best to worst** (ranked list of main dishes or sides, filtered by location and meal). The URL hash drives the
view (#home, #legs, #leg-N, #days, #d-YYYY-MM-DD, #rank), so the phone's back button works. No totals or spend
dashboard on the front (Matt's call).

**Legs** (from the real bookings, defined in scripts/sync_trip.py): Getting there (Nov 22–23, incl. Taipei) ·
Bangkok (Nov 24) · Chiang Mai (Nov 25–29, incl. Chiang Rai + Doi Inthanon) · Koh Lanta (Nov 30 – Dec 5) ·
Bangkok (Dec 6–8) · Seoul / return travel (Dec 9). On travel days a dish goes to the leg matching where it was eaten.
**Surface mode:** Experience (gallery). Thailand only (no multi-trip).
