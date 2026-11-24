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
**Pages:** Home (the tally and per-stop totals, top 3 meals, how scoring works, links to every day) and
Journal (filters + every day's dishes). **Surface mode:** Experience (gallery). Thailand only (no multi-trip).
