# Room Zero — JinxForge VR proof page

One self-contained page: `index.html`. No build step, no assets besides the
three.js CDN (pinned 0.170.0 via import map). Serve it over HTTPS (GitHub
Pages) and open it in the Quest 3S browser.

## What it proves

- **True scale in the headset.** The scene is built in metres: a 4 m × 4 m
  floor, grid lines every 0.1 m with stronger lines every 0.5 m, and a
  100 mm reference cube outline in the corner. If the room feels room-sized
  and the yellow cube reads as 100 mm, the scale road is sound.
- **Hands can work.** Point a controller at the clay block and hold the
  trigger (or squeeze) — the block rides the hand; let go and it drops and
  settles flat on the floor.
- **VR work can become a print file.** EXPORT STL writes
  `room-zero-block.stl` with the block's current pose baked in, converted
  from scene metres to millimetres (100 × 60 × 60 mm), ready to slice.

## Controls

| Where | Action |
|---|---|
| Quest (in VR) | Controller trigger or squeeze on the block = grab / release |
| Desktop browser | Mouse drag moves the block; orbit with left-drag on empty space, scroll zooms |
| Any browser | Big **EXPORT STL** button (bottom left) downloads the block |

In VR you step back automatically: the camera rig stands 1.6 m behind room
centre so the block is in front of you.

## Known limits (v1, by design)

- **One block only.** No shaping, no adding pieces, no colour work yet —
  this page exists to prove scale, grab, and export, nothing more.
- **Export is a desktop/DOM button.** In-headset export clicking is not
  wired; press EXPORT STL from the browser view (or after exiting VR).
  The download lands in the headset/browser downloads like any file.
- **No transfer path off the headset yet.** The STL downloads to wherever
  the browser puts files; getting it from the Quest to the slicer is a
  later step (the repo / Drive road), not part of this proof.
- **The block keeps whatever tilt you leave it with**, then settles flat
  to the floor on release — it cannot hover or lean against anything.
- Desktop orbit and the VR rig don't share a viewpoint; expect the camera
  to be somewhere different when you exit VR.

## Files

- `index.html` — everything (scene, grab logic, STL export, UI).
