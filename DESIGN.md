---
name: Dishspatch
description: Simple tropical brand kit for a Thailand food photo journal.
colors:
  paper: "#f4eedb"
  paper-raised: "#fffaec"
  paper-sunk: "#e9e1c7"
  ink: "#12251a"
  ink-soft: "#435747"
  ink-faint: "#6d7c68"
  rule: "#cfc5a5"
  hibiscus: "#d8432e"
  mango: "#f0a32f"
  pandan: "#a9cf5b"
  fern: "#2e6a45"
  lagoon: "#1b8c93"
  region-bangkok: "#d8432e"
  region-chiang-mai: "#d9861c"
  region-chiang-rai: "#3566c8"
  region-doi-inthanon: "#4f8d5d"
  region-koh-lanta: "#1b8c93"
  region-transit: "#7b826f"
typography:
  display:
    fontFamily: "Gloock, Iowan Old Style, Georgia, serif"
    fontSize: "clamp(3.5rem, 13vw, 6rem)"
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Gloock, Georgia, serif"
    fontSize: "2.25rem"
    fontWeight: 400
    lineHeight: 1.05
  title:
    fontFamily: "Gloock, Georgia, serif"
    fontSize: "1.625rem"
    fontWeight: 400
  body:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
    fontFeature: "tnum"
  label:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 600
  thai:
    fontFamily: "Sarabun, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 500
rounded:
  lg: "14px"
  md: "10px"
  sm: "6px"
  pill: "999px"
spacing:
  s1: "4px"
  s2: "8px"
  s3: "12px"
  s4: "16px"
  s5: "24px"
  s6: "32px"
  s7: "48px"
  s8: "72px"
components:
  dish-photo:
    rounded: "{rounded.lg}"
    backgroundColor: "{colors.paper-sunk}"
  rating-badge:
    backgroundColor: "{colors.paper-raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  rating-badge-top:
    backgroundColor: "{colors.hibiscus}"
    textColor: "{colors.paper-raised}"
    rounded: "{rounded.sm}"
  chip:
    backgroundColor: "{colors.paper-raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.6em 1em"
  chip-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
---

# Dishspatch design system

The live source of truth is `site/brand.css` (CSS custom properties). This file explains them.
A visual version is at `site/brand.html` (published alongside the journal at `brand.html`; the page has no footer link).

## Overview

**Simple, tropical, photo-led.** The food photos are the hero. The tropical feel comes from the
palette alone (warm paper, jungle-green ink, a hibiscus accent), not from decorative motifs.
Keep it restrained: no illustrations, patterns or ornamental shapes.
Surface mode: **Experience** (a gallery). The interface recedes so the dishes lead.

**Light only.** Warm paper `#f4eedb`, canopy ink `#12251a`. There is no dark mode and no theme toggle
(Matt's call). Don't add one back.

Name: **Dishspatch**, dish + dispatch. Tagline: "Matt's food reviews from his trip to Thailand!" Set in Gloock, no subtitle.

## Colors

- **Hibiscus**: the one loud accent. Used for the top-rated badge, focus rings and link underlines. Never use it for body text.
- **Fern / Pandan**: the jungle greens. Used for the active tab and sort control, score bars and text selection.
- **Mango / Lagoon**: supporting accents only.
- **Region colours** give each stop its own hue, used only as a small dot and on the "Day N" label:
  Bangkok = chili red · Chiang Mai = lantern orange (Yi Peng) · Chiang Rai = Blue Temple sapphire ·
  Doi Inthanon = misty fern · Koh Lanta = Andaman lagoon · Transit = stone.
- Secondary text is tinted green (`ink-soft`, `ink-faint`), never grey.

## Typography

- **Gloock** (display/headings): juicy, high-contrast serif, set large. Max 6rem.
- **Hanken Grotesk** (body/labels): tabular numerals on, so prices and ratings line up.
- **Sarabun** for Thai script (dish names in Thai).
- No eyebrow or kicker labels above headings.

## Layout

- Max width 1180px, with a 16px gutter on phones and 32px from 720px.
- Days run in trip order. Each day has a heading row with a thin neutral rule, then a dish grid
  (1 column on phones, 2 from 560px, 3 from 940px).
- "Best bites so far" (top 3 by rating) appears once 3 or more dishes are rated.
- Upcoming days collapse into a "Still to come" list showing food plans from the Atlas itinerary.
- The filter bar sticks to the top. On phones the sort toggle wraps to its own row.

## Elevation & Depth

Two soft shadows, both green-tinted and always offset (`--shadow-1` rest, `--shadow-2` hover/dialog).
No hard offset shadows and no glow.

## Shapes

Plain, consistent rounding: 14px on photos and dialogs, 10px on panels, 6px on badges, and pills for chips
and the sort toggle. Region dots are circles. No decorative shapes.

## Components

- **Dish card**: a rounded photo (4:5, or 1:1 on phones) with a rating badge bottom-left, then the dish name (Gloock), Thai name,
  place + region tag, a 3-line description, then price (฿ + $) and meal. Tapping it opens the lightbox.
- **Rating**: a plain number /10 (one decimal). Computed from the rubric (Flavour 50%, Texture 20%, Value 20%, Presentation 10%). Weights are always shown to people as % of the score, never as multipliers. The lightbox shows the breakdown as a small table. Ambiance is shown separately and never affects the score. No meters or icons.
- **Lightbox**: a `<dialog>` with the photo left and details right (stacked on phones), and thumbnails when there are several photos.
- **Icons**: authored inline SVG, 1.8px stroke. No emoji standing in for icons.

## Do's and Don'ts

- Do let the photos be big, uncropped in the lightbox and never filtered.
- Do keep motion minimal: a quiet hover lift on cards and a soft fade-in on the dialog.
- Don't use gradient text, glassy cards, eyebrow labels or stat-tile heroes. The ledger stays a sentence.
- Don't add decorative motifs (leaves, fronds, patterns, illustrations).
- Don't add new colours without adding them to `brand.css` and this file.
