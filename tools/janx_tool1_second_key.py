"""
JANX TOOL 1 - gate second key for JinxForge production 3MF files.
Check word for Jinx's desk: ANVIL

An independent second reading of a production file's own bytes, against
the house laws. It is meant to run beside the crew's gate, not instead of it.

Usage
  python janx_second_key.py piece.3mf --colours 4 --printer AD5X --kind panel
  python janx_second_key.py --project-config project_settings.config \
      --model-config model_settings.config --colours 4 --printer AD5X --kind panel

  --colours  the design's colour count (the palette law: 1 to 4)
  --printer  AD5X (Big Forge) or 5M (Little Forge)
  --kind     panel (no supports) or figure (the house six support settings)

Verdicts
  FAIL  breaks a house law: the file does not go on the GOOD shelf
  WARN  differs from a house number or looks unusual: a person decides
  NOTE  information only; no known effect on the print
  PASS  checked and matches
Exit code 1 if any FAIL, else 0.

House laws checked (from Jinx's briefing, 30 Oct 2026)
  - flushing multiplier 1.0 on every filament
  - prime tower on, width 45, brim 3 (multicolour files)
  - supports as designed: panel = off; figure = tree, plate only,
    threshold 55, top distance 0.60, sideways distance 1.0
  - christened for the right printer (printer_model and preset name)
  - the filament law (Janx proposal, adopted 30 Oct): the count of distinct
    filaments assigned to parts equals the design's colour count
  - multicolour only on the AD5X, automatic changes (manual change off)
House numbers warned on: PLA nozzle 220 first layer then 215, bed 60;
PETG nozzle 240, bed 70. Prime tower must sit inside the bed.

Limits
  Colour painted onto a part (rather than separate parts) is not counted;
  the tool says so when it finds painted regions in a .3mf.
  It reads settings only; geometry checks belong to the mesh tool.

Needs: Python 3.8+, standard library only.
"""
import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET

PRINTERS = {
    "AD5X": {"model": "Flashforge AD5X", "preset_token": "AD5X", "multicolour": True},
    "5M": {"model": "Flashforge Adventurer 5M", "preset_token": "Adventurer 5M", "multicolour": False},
}
FIGURE_SUPPORT = {
    "enable_support": "1",
    "support_on_build_plate_only": "1",
    "support_threshold_angle": "55",
    "support_top_z_distance": "0.6",
    "support_object_xy_distance": "1.0",
}
HOUSE_TEMPS = {
    "PLA": {"nozzle_first": 220, "nozzle": 215, "bed": 60},
    "PETG": {"nozzle_first": 240, "nozzle": 240, "bed": 70},
}
PLATE_KEYS = ["hot_plate_temp", "textured_plate_temp", "cool_plate_temp", "eng_plate_temp"]
EXPECTED_PRESENT = ["machine_start_gcode", "machine_end_gcode", "nozzle_diameter"]


class Report:
    def __init__(self):
        self.rows = []

    def add(self, status, check, detail):
        self.rows.append((status, check, detail))

    def count(self, status):
        return sum(1 for r in self.rows if r[0] == status)


def as_list(v):
    return v if isinstance(v, list) else [v]


def num(v):
    try:
        return float(str(v).strip().rstrip("%"))
    except (TypeError, ValueError):
        return None


def same_number(v, target):
    n = num(v)
    return n is not None and abs(n - float(target)) < 1e-6


def load(args):
    painted = None
    if args.file:
        with zipfile.ZipFile(args.file) as z:
            names = z.namelist()
            proj = json.loads(z.read("Metadata/project_settings.config").decode("utf-8"))
            model = z.read("Metadata/model_settings.config").decode("utf-8")
            painted = 0
            for n in names:
                if n.startswith("3D/") and n.endswith(".model"):
                    data = z.read(n)
                    painted += data.count(b"paint_color") + data.count(b"mmu_segmentation")
    else:
        with open(args.project_config, encoding="utf-8") as f:
            proj = json.load(f)
        with open(args.model_config, encoding="utf-8") as f:
            model = f.read()
    return proj, model, painted


def part_assignments(model_xml):
    root = ET.fromstring(model_xml)
    parts = []
    for obj in root.iter("object"):
        obj_ext = "1"
        obj_name = obj.get("id")
        for md in obj.findall("metadata"):
            if md.get("key") == "extruder":
                obj_ext = md.get("value")
            if md.get("key") == "name":
                obj_name = md.get("value")
        for part in obj.findall("part"):
            if part.get("subtype", "normal_part") != "normal_part":
                continue
            name, ext = part.get("id"), obj_ext
            for md in part.findall("metadata"):
                if md.get("key") == "name":
                    name = md.get("value")
                if md.get("key") == "extruder":
                    ext = md.get("value")
            parts.append((obj_name, name, ext))
    return parts


def check(proj, model_xml, painted, colours, printer, kind):
    r = Report()
    pr = PRINTERS[printer]
    filament_colour = as_list(proj.get("filament_colour", []))

    # 1. filament law
    parts = part_assignments(model_xml)
    used = sorted({p[2] for p in parts}, key=lambda x: int(x) if x.isdigit() else 99)
    listing = ", ".join(f"{n}=F{e}" for _, n, e in parts)
    if not parts:
        r.add("FAIL", "filament law", "no printable parts found in model settings")
    elif len(used) == colours:
        r.add("PASS", "filament law", f"{len(used)} distinct filaments on {len(parts)} parts = design {colours} ({listing})")
    else:
        r.add("FAIL", "filament law", f"{len(used)} distinct filaments on parts, design says {colours} ({listing})")
    bad = [e for e in used if not e.isdigit() or int(e) > len(filament_colour)]
    if bad:
        r.add("FAIL", "filament range", f"parts use filament(s) {bad} but the file defines {len(filament_colour)}")
    if painted:
        r.add("WARN", "painted colour", f"{painted} painted-region markers found: painted colours are not counted by this tool")

    # 2. palette law vs printer
    if colours > 1 and not pr["multicolour"]:
        r.add("FAIL", "palette law", f"{colours}-colour design on the {printer}, which is single colour")
    if colours > 4:
        r.add("FAIL", "palette law", f"{colours} colours: a fifth colour is lawful only as separate inlay parts")

    # 3. christening
    model = proj.get("printer_model", "")
    preset = proj.get("printer_settings_id", "")
    if model == pr["model"]:
        r.add("PASS", "printer model", model)
    else:
        r.add("FAIL", "printer model", f"file says '{model}', expected '{pr['model']}'")
    if pr["preset_token"] in str(preset) and not (printer == "5M" and "Pro" in str(preset)):
        r.add("PASS", "printer preset", preset)
    else:
        r.add("FAIL", "printer preset", f"file says '{preset}', expected a {printer} preset")
    compat = [c for c in as_list(proj.get("print_compatible_printers", [])) if c]
    if compat and not all(pr["preset_token"] in c for c in compat):
        r.add("WARN", "compatible printers", f"process preset lists {sorted(set(compat))}")

    # 4. flushing multiplier
    fm = as_list(proj.get("flush_multiplier", []))
    if fm and all(same_number(v, 1) for v in fm):
        r.add("PASS", "flushing multiplier", f"1 on all {len(fm)} filaments")
    else:
        r.add("FAIL", "flushing multiplier", f"values {fm}, house law is 1 on every filament")

    # 5. prime tower
    if colours > 1:
        if str(proj.get("enable_prime_tower")) == "1":
            r.add("PASS", "prime tower on", "enabled")
        else:
            r.add("FAIL", "prime tower on", f"enable_prime_tower = {proj.get('enable_prime_tower')}")
        if same_number(proj.get("prime_tower_width"), 45):
            r.add("PASS", "prime tower width", "45")
        else:
            r.add("FAIL", "prime tower width", f"{proj.get('prime_tower_width')}, house law is 45")
        if same_number(proj.get("prime_tower_brim_width"), 3):
            r.add("PASS", "prime tower brim", "3")
        else:
            r.add("FAIL", "prime tower brim", f"{proj.get('prime_tower_brim_width')}, house law is 3")
        tx = num(as_list(proj.get("wipe_tower_x", [None]))[0])
        tw = num(proj.get("prime_tower_width"))
        area = as_list(proj.get("printable_area", []))
        xs = [num(p.split("x")[0]) for p in area if "x" in p]
        if tx is not None and tw is not None and xs:
            if min(xs) <= tx and tx + tw <= max(xs):
                r.add("PASS", "tower on bed", f"x {tx:g} to {tx + tw:g} inside bed {min(xs):g} to {max(xs):g}")
            else:
                r.add("WARN", "tower on bed", f"x {tx:g} to {tx + tw:g} vs bed {min(xs):g} to {max(xs):g}")
    else:
        r.add("NOTE", "prime tower", "single-colour design: tower not required")

    # 6. multicolour mechanics on the AD5X
    if colours > 1 and printer == "AD5X":
        if str(proj.get("manual_filament_change", "0")) == "0":
            r.add("PASS", "automatic changes", "manual_filament_change = 0")
        else:
            r.add("FAIL", "automatic changes", "manual_filament_change = 1: changes would wait for hands")
        if str(proj.get("single_extruder_multi_material", "1")) == "1":
            r.add("PASS", "one nozzle, many filaments", "single_extruder_multi_material = 1")
        else:
            r.add("FAIL", "one nozzle, many filaments", "single_extruder_multi_material is off")
    fmap = as_list(proj.get("filament_map", []))
    if fmap and any(str(v) != "1" for v in fmap):
        r.add("WARN", "nozzle map", f"filament_map {fmap}: this machine has one nozzle")
    elif fmap:
        r.add("NOTE", "nozzle map", "filament_map is all 1 = every filament to the one nozzle (not the slot map)")

    # 7. supports as designed
    if kind == "panel":
        if str(proj.get("enable_support")) == "0":
            r.add("PASS", "supports", "off (panel)")
        else:
            r.add("FAIL", "supports", f"enable_support = {proj.get('enable_support')} on a panel")
    else:
        stype = str(proj.get("support_type", ""))
        if stype.startswith("tree"):
            r.add("PASS", "support type", stype)
        else:
            r.add("FAIL", "support type", f"{stype}, house figure setting is tree")
        for key, want in FIGURE_SUPPORT.items():
            got = proj.get(key)
            ok = str(got) == want if key in ("enable_support", "support_on_build_plate_only") else same_number(got, want)
            r.add("PASS" if ok else "FAIL", key, f"{got}" + ("" if ok else f", house figure setting is {want}"))

    # 8. house temperatures (advice, not law)
    types = sorted(set(as_list(proj.get("filament_type", []))))
    if len(types) > 1:
        r.add("WARN", "filament types", f"mixed {types}")
    for t in types:
        h = HOUSE_TEMPS.get(t)
        if not h:
            r.add("NOTE", "temperatures", f"no house numbers held for {t}")
            continue
        first = as_list(proj.get("nozzle_temperature_initial_layer", []))
        rest = as_list(proj.get("nozzle_temperature", []))
        if all(same_number(v, h["nozzle_first"]) for v in first) and all(same_number(v, h["nozzle"]) for v in rest):
            r.add("PASS", f"{t} nozzle", f"first layer {h['nozzle_first']}, then {h['nozzle']}")
        else:
            r.add("WARN", f"{t} nozzle", f"first layer {first}, then {rest}; house is {h['nozzle_first']} then {h['nozzle']}")
        beds = {k: as_list(proj.get(k, [])) for k in PLATE_KEYS if k in proj}
        off = {k: v for k, v in beds.items() if not all(same_number(x, h["bed"]) for x in v)}
        if beds and not off:
            r.add("PASS", f"{t} bed", f"{h['bed']} on every plate type")
        elif off:
            r.add("WARN", f"{t} bed", f"house is {h['bed']}; differs on {off}")

    # 9. carry-overs and gaps (information for a person)
    ec = as_list(proj.get("extruder_colour", []))
    if ec and filament_colour and [c.upper() for c in ec] != [c.upper() for c in filament_colour]:
        r.add("NOTE", "extruder colour", f"extruder_colour {ec} differs from filament_colour {filament_colour}; looks like a carry-over")
    missing = [k for k in EXPECTED_PRESENT if k not in proj]
    if missing:
        r.add("WARN", "keys absent", f"{missing} not in this file; the slicer must supply them from elsewhere")
    return r


def main():
    ap = argparse.ArgumentParser(description="JinxForge gate second key")
    ap.add_argument("file", nargs="?", help="production .3mf")
    ap.add_argument("--project-config")
    ap.add_argument("--model-config")
    ap.add_argument("--colours", type=int, required=True)
    ap.add_argument("--printer", choices=sorted(PRINTERS), required=True)
    ap.add_argument("--kind", choices=["panel", "figure"], required=True)
    a = ap.parse_args()
    if not a.file and not (a.project_config and a.model_config):
        ap.error("give a .3mf, or both --project-config and --model-config")

    proj, model_xml, painted = load(a)
    rep = check(proj, model_xml, painted, a.colours, a.printer, a.kind)
    src = a.file or f"{a.project_config} + {a.model_config}"
    print("JANX TOOL 1 - gate second key - check word ANVIL")
    print(f"file: {src}")
    print(f"design: {a.colours} colour(s), {a.printer}, {a.kind}")
    for status in ("FAIL", "WARN", "PASS", "NOTE"):
        for s, name, detail in rep.rows:
            if s == status:
                print(f"{s:4}  {name}: {detail}")
    verdict = "NOT CLEARED" if rep.count("FAIL") else "CLEARED"
    print(f"verdict: {verdict} - {rep.count('FAIL')} fail, {rep.count('WARN')} warn, "
          f"{rep.count('PASS')} pass, {rep.count('NOTE')} note")
    sys.exit(1 if rep.count("FAIL") else 0)


if __name__ == "__main__":
    main()
