"""
JANX TOOL 0 - fine-feature survival check for flat colour panel rasters.
Check word for Jinx's desk: TERRACE

What it does
  For every colour in a flat (classified) panel image, it finds:
    - tiny islands: separate specks of a colour smaller than a floor area
    - thin runs: stretches of a shape narrower than a floor width
  It prints a table per colour and writes an overlay picture:
    yellow = thin runs, cyan = tiny islands, everything else dimmed.

Units
  Without --mm-per-px it works in pixels (floors: width 3 px, area 9 px).
  With --mm-per-px it works in millimetres from the nozzle size:
    thin floor  = nozzle width          (default 0.4 mm)
    island floor = (2 x nozzle) squared  (default 0.64 mm^2)
  mm-per-px = panel height in mm / raster height in pixels.

Usage
  python janx_survival_check.py panel.png overlay.png
  python janx_survival_check.py panel.png overlay.png --mm-per-px 0.23 --nozzle 0.4
  python janx_survival_check.py panel.png overlay.png --exclude "89,89,94;52,52,57"
    (--exclude skips backdrop colours that are not part of the print)

Method
  Thin runs are the parts of a colour that a square "pen" as wide as the
  floor cannot sweep through. Square corners pass; diagonal strokes err
  toward being flagged. Self-tested on lines of known width: at 0.25 mm/px
  with a 0.4 mm nozzle, a 1 px line (0.25 mm) is flagged and 2-5 px lines
  pass; a solid square raises nothing.

Needs: Python 3, numpy, scipy, Pillow.
Run it on the build raster itself (the classified picture the crew builds
from), at its true resolution. A screen export or an upscaled crop will
report its own pixel steps, not the panel's.
"""
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def parse_colours(text):
    out = set()
    if not text:
        return out
    for part in text.split(";"):
        part = part.strip()
        if part:
            out.add(tuple(int(v) for v in part.split(",")))
    return out


def analyse(path, overlay_path, exclude, min_width_px, min_area_px):
    im = np.array(Image.open(path).convert("RGB"))
    colours, counts = np.unique(im.reshape(-1, 3), axis=0, return_counts=True)
    overlay = (im * 0.35).astype(np.uint8)
    eight = np.ones((3, 3), dtype=bool)
    rows = []
    for colour, count in zip(colours, counts):
        key = tuple(int(v) for v in colour)
        if key in exclude:
            continue
        mask = np.all(im == colour, axis=-1)
        labels, n_regions = ndi.label(mask, structure=eight)
        areas = ndi.sum(mask, labels, index=np.arange(1, n_regions + 1))
        tiny_ids = np.where(areas < min_area_px)[0] + 1
        # thin runs: parts of the shape a square "pen" of the floor width
        # cannot sweep through (morphological opening). Square corners
        # survive the pen; diagonal strokes err toward being flagged.
        side = max(2, int(np.ceil(min_width_px)))
        pen = np.ones((side, side), dtype=bool)
        removed = mask & ~ndi.binary_opening(mask, structure=pen)
        rlab, rn = ndi.label(removed, structure=eight)
        rareas = ndi.sum(removed, rlab, index=np.arange(1, rn + 1))
        keep = np.where(rareas >= 2 * side)[0] + 1
        thin_zone = np.isin(rlab, keep)
        n_thin = len(keep)
        overlay[thin_zone] = (255, 255, 0)
        overlay[np.isin(labels, tiny_ids)] = (0, 255, 255)
        rows.append((key, int(count), int(n_regions), len(tiny_ids), int(n_thin)))
    Image.fromarray(overlay).save(overlay_path)
    return im.shape[1], im.shape[0], rows


def main():
    ap = argparse.ArgumentParser(description="Fine-feature survival check")
    ap.add_argument("image")
    ap.add_argument("overlay")
    ap.add_argument("--exclude", default="", help='backdrop colours, e.g. "89,89,94;52,52,57"')
    ap.add_argument("--mm-per-px", type=float, default=None)
    ap.add_argument("--nozzle", type=float, default=0.4, help="nozzle width in mm")
    a = ap.parse_args()

    if a.mm_per_px:
        min_width_px = a.nozzle / a.mm_per_px
        min_area_px = (2 * a.nozzle) ** 2 / (a.mm_per_px ** 2)
        units = f"mm mode: {a.mm_per_px} mm/px, nozzle {a.nozzle} mm"
    else:
        min_width_px, min_area_px = 3.0, 9.0
        units = "pixel mode (no mm scale given)"

    w, h, rows = analyse(a.image, a.overlay, parse_colours(a.exclude), min_width_px, min_area_px)
    print("JANX TOOL 0 - survival check - check word TERRACE")
    print(f"image {w} x {h} px; {units}")
    print(f"floors: thin < {min_width_px:.2f} px wide, island < {min_area_px:.1f} px area")
    print(f"{'colour':18} {'pixels':>8} {'regions':>8} {'islands':>8} {'thin runs':>10}")
    for key, count, regions, tiny, thin in rows:
        print(f"{str(key):18} {count:8d} {regions:8d} {tiny:8d} {thin:10d}")
    print(f"overlay written: {a.overlay} (yellow = thin runs, cyan = islands)")


if __name__ == "__main__":
    main()
