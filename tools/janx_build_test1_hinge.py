"""
JANX BUILD TEST 1 - orca jaw hinge: pin and cradle socket, built by construction.
Check word for Jinx's desk: CRADLE

Spec (from Jinx, letter four):
  pin    cylinder, diameter 4.395 mm, length 16 mm, axis along Y
  socket block 24 (X) x 16 (Y) x 18 (Z) mm, bore 4.893 mm cut through along Y, centred
  bore is a cradle: two wall arcs of about 80 degrees each, set opposite;
  the rest of the circle is open into the motion channel
  no wall thinner than 2 mm anywhere

Assumption chosen for the cradle (Janx):
  - The two 80-degree wall arcs are centred straight up (+Z) and straight down (-Z).
  - The two open 100-degree sectors face +X and -X. Each is a wedge-shaped
    channel cut from the bore out to radius 6.0 mm from the axis, running the
    full 16 mm along Y.
  - The channels stop at radius 6.0 so the block stays one solid piece: the
    material from radius 6 out to the block's side faces (6 mm thick at the
    midline) ties the upper and lower cradle arcs together. A channel cut all
    the way out to the side faces would split the block in two.
  - Pin and bore share the axis X = 0, Z = 0 (block centre). The pin sits in
    the bore for the measurement, centres coincident.

Output: hinge_pin.stl, hinge_socket.stl, and a measured report on screen.
Needs: Python 3, numpy, trimesh, manifold3d (boolean engine), shapely.
"""
import numpy as np
import trimesh
from shapely.geometry import Polygon

PIN_D, PIN_L = 4.395, 16.0
BORE_D = 4.893
BLOCK = (24.0, 16.0, 18.0)          # X, Y, Z
ARC_DEG = 80.0                      # each wall arc
CHANNEL_R = 6.0                     # radial reach of the open channels
SECTIONS = 512                      # facets around each circle


def cylinder_along_y(diameter, length):
    c = trimesh.creation.cylinder(radius=diameter / 2, height=length, sections=SECTIONS)
    c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    return c


def wedge_along_y(centre_deg, span_deg, radius, length):
    """Prism whose cross-section is a circular sector, extruded along Y."""
    a0, a1 = np.radians(centre_deg - span_deg / 2), np.radians(centre_deg + span_deg / 2)
    angles = np.linspace(a0, a1, 64)
    pts = [(0.0, 0.0)] + [(radius * np.cos(a), radius * np.sin(a)) for a in angles]
    w = trimesh.creation.extrude_polygon(Polygon(pts), height=length)
    # polygon is drawn in X-Y and extruded along Z; turn it so the section is X-Z, extrusion Y
    w.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    w.apply_translation([0, length / 2, 0])
    return w


def build():
    pin = cylinder_along_y(PIN_D, PIN_L)
    block = trimesh.creation.box(extents=BLOCK)
    over = BLOCK[1] + 2.0  # cutters run past both faces
    bore = cylinder_along_y(BORE_D, over)
    open_span = (360.0 - 2 * ARC_DEG) / 2          # 100 degrees each
    ch_pos = wedge_along_y(0.0, open_span, CHANNEL_R, over)
    ch_neg = wedge_along_y(180.0, open_span, CHANNEL_R, over)
    socket = trimesh.boolean.difference([block, bore, ch_pos, ch_neg], engine="manifold")
    return pin, socket


def fit_circle(xz):
    """Least-squares circle through points (Kasa fit). Returns centre, radius."""
    x, z = xz[:, 0], xz[:, 1]
    A = np.c_[2 * x, 2 * z, np.ones(len(x))]
    b = x ** 2 + z ** 2
    cx, cz, c = np.linalg.lstsq(A, b, rcond=None)[0]
    return np.array([cx, cz]), float(np.sqrt(c + cx ** 2 + cz ** 2))


def measure(pin, socket):
    rep = {}
    pv = pin.vertices[:, [0, 2]]
    pv = pv[np.hypot(pv[:, 0], pv[:, 1]) > PIN_D / 4]   # drop the end-cap centre points
    p_c, p_r = fit_circle(pv)
    rep["pin_diameter"] = 2 * p_r
    rep["pin_centre"] = p_c
    # bore wall vertices: socket vertices near the bore radius, not on the channel faces
    sv = socket.vertices
    r = np.hypot(sv[:, 0], sv[:, 2])
    near = np.abs(r - BORE_D / 2) < 0.05
    b_c, b_r = fit_circle(sv[near][:, [0, 2]])
    rep["bore_diameter"] = 2 * b_r
    rep["bore_centre"] = b_c
    rep["clearance"] = b_r - p_r
    rep["centre_offset"] = float(np.hypot(*(b_c - p_c)))
    ang = np.degrees(np.arctan2(sv[near][:, 2], sv[near][:, 0])) % 360
    rep["arc_up"] = (ang[(ang > 0) & (ang < 180)].min(), ang[(ang > 0) & (ang < 180)].max())
    rep["arc_down"] = (ang[ang > 180].min(), ang[ang > 180].max())
    for name, m in (("pin", pin), ("socket", socket)):
        rep[f"{name}_watertight"] = bool(m.is_watertight)
        rep[f"{name}_volume"] = float(m.volume)
        rep[f"{name}_bodies"] = len(m.split(only_watertight=False))
        rep[f"{name}_extents"] = m.extents
    # thinnest wall: erode the mid-length cross-section by 1 mm; any wall under
    # 2 mm vanishes and splits or shrinks the section into extra pieces
    sec = socket.section(plane_origin=[0, 0, 0], plane_normal=[0, 1, 0])
    planar, _ = sec.to_2D()
    rings = sorted((Polygon(p.exterior) for p in planar.polygons_closed if p is not None),
                   key=lambda p: p.area, reverse=True)
    poly = rings[0]
    for hole in rings[1:]:
        poly = poly.difference(hole)
    rep["section_pieces"] = 1 if poly.geom_type == "Polygon" else len(poly.geoms)
    eroded = poly.buffer(-1.0)
    rep["eroded_pieces"] = 1 if eroded.geom_type == "Polygon" else len(eroded.geoms)
    return rep


def main():
    pin, socket = build()
    pin.export("hinge_pin.stl")
    socket.export("hinge_socket.stl")
    m = measure(pin, socket)
    ok = lambda b: "yes" if b else "NO"
    print("JANX BUILD TEST 1 - orca jaw hinge - check word CRADLE")
    print(f"pin diameter     {m['pin_diameter']:.4f} mm   (spec 4.395, band +/-0.05)")
    print(f"bore diameter    {m['bore_diameter']:.4f} mm   (spec 4.893, band +/-0.05)")
    print(f"radial clearance {m['clearance']:.4f} mm   (spec 0.249, band 0.20-0.30)")
    print(f"centre offset    {m['centre_offset']:.4f} mm   (spec within 0.003)")
    print(f"wall arcs        up {m['arc_up'][0]:.1f} to {m['arc_up'][1]:.1f} deg, "
          f"down {m['arc_down'][0]:.1f} to {m['arc_down'][1]:.1f} deg")
    print(f"pin    watertight {ok(m['pin_watertight'])}, bodies {m['pin_bodies']}, "
          f"volume {m['pin_volume']:.2f} mm3, extents {np.round(m['pin_extents'], 3)}")
    print(f"socket watertight {ok(m['socket_watertight'])}, bodies {m['socket_bodies']}, "
          f"volume {m['socket_volume']:.2f} mm3, extents {np.round(m['socket_extents'], 3)}")
    print(f"2 mm wall check  mid-section pieces {m['section_pieces']}, "
          f"after 1 mm erosion {m['eroded_pieces']} (1 = no neck under 2 mm)")


if __name__ == "__main__":
    main()
