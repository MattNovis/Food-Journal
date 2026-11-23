#!/usr/bin/env python3
"""Prepare a food photo for the journal.

- Reads EXIF first (capture time + GPS) and prints it so the entry can use it.
- Fixes rotation, resizes to 1600px on the long edge, saves a JPEG (q=80).
- Strips ALL metadata from the saved copy (no GPS published in the artifact).

Usage: python3 scripts/add_photo.py <source-image> <slug>
       -> photos/<slug>.jpg, prints JSON {path, width, height, takenAt, gps}
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps
from PIL.ExifTags import GPSTAGS, TAGS

ROOT = Path(__file__).resolve().parent.parent
LONG_EDGE = 1600


def exif_info(img):
    info = {"takenAt": None, "gps": None}
    try:
        exif = img.getexif()
    except Exception:
        return info
    tags = {TAGS.get(k, k): v for k, v in exif.items()}
    sub = exif.get_ifd(0x8769) if hasattr(exif, "get_ifd") else {}
    taken = {TAGS.get(k, k): v for k, v in sub.items()}.get("DateTimeOriginal") or tags.get("DateTime")
    if taken:
        info["takenAt"] = str(taken).replace(":", "-", 2).replace(" ", "T")
    gps_raw = exif.get_ifd(0x8825) if hasattr(exif, "get_ifd") else {}
    gps = {GPSTAGS.get(k, k): v for k, v in gps_raw.items()}

    def to_deg(v, ref):
        d, m, s = (float(x) for x in v)
        deg = d + m / 60 + s / 3600
        return -deg if ref in ("S", "W") else deg

    if "GPSLatitude" in gps and "GPSLongitude" in gps:
        try:
            info["gps"] = {
                "lat": round(to_deg(gps["GPSLatitude"], gps.get("GPSLatitudeRef", "N")), 5),
                "lng": round(to_deg(gps["GPSLongitude"], gps.get("GPSLongitudeRef", "E")), 5),
            }
        except Exception:
            pass
    return info


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, slug = Path(sys.argv[1]), sys.argv[2]
    img = Image.open(src)
    info = exif_info(img)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)
    out = ROOT / "photos" / f"{slug}.jpg"
    out.parent.mkdir(exist_ok=True)
    img.save(out, "JPEG", quality=80, optimize=True, progressive=True)  # no exif= → metadata dropped
    print(json.dumps({
        "path": f"photos/{slug}.jpg",
        "width": img.width,
        "height": img.height,
        "kb": round(out.stat().st_size / 1024),
        **info,
    }))


if __name__ == "__main__":
    main()
