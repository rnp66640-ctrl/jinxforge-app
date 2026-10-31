# Improvements log — jinxforge-app

The two-key ledger: every improvement proposed, agreed, built, or killed
under Richard's grant of 2026-10-30 (Janx agrees in a letter + Jinx agrees
at his desk; silence is not agreement; owner rulings override the grant;
nothing here spends money, sends outward, or changes a rule).

## 2026-10-30 — Round 0 (owner present)
- BUILT (two-key): Voice rung for Room Zero — Janx proposed (Web Speech),
  Jinx keyed and built: VOICE TEST button + spoken export confirmation.
  Live on Pages the same night.
- KILLED (owner ruling, same night): VOICE IS KILLED FOR NOW. Richard:
  the Quest browser's speech chokes in immersive sessions; voice and
  audio are handled externally by phone/earbud; all confirmations stay
  visual (HUD text). Voice code removed from Room Zero in the v2 pass.
- OWNER-APPROVED (I1): AD5X bed footprint 220 x 220 mm into Room Zero.
  Built in v2: translucent plate + amber border at room centre.
- OWNER-APPROVED (I2): the 165.1 mm figure ghost, baseline reference.
  Built in v2: stacked-proportion ghost figure standing on the plate,
  not grabbable.
- OWNER-APPROVED (I3): this log.
- OWNER-APPROVED (I4): snapshot button, local viewport captures.
  Built in v2: SNAPSHOT saves the current view as a PNG, local only.
- WATCHLIST (owner, for the rung builds): (1) grab/release must not
  jitter or throw the part off-grid — v2 answers with a dampened
  settle: flat rest + position quantized to whole mm + heading to
  whole degrees on every release; (2) snap increments 1/5/10 mm must
  stay 1:1 with Manifold space — v2 floor quantization is whole-mm;
  steps arrive with the rungs; (3) EXPORT STL from inside an immersive
  session must not eject the user — v1 keeps export on the browser
  view; the in-session export path is a named rung-build problem,
  to be settled at Richard's first stand and designed from evidence.

## 2026-10-31 — Round 1 (owner at the table)
- DELIVERED overnight (Janx): Forge Room v2 (rungs on Room Zero v2's
  base, dummy aboard) and v3 (P1 auto-save, P2 floaters red on export,
  P3 bed-fit warnings) — both desk-verified byte-exact by the watch.
- OWNER RULING: MERGE THE ROOMS — one room only. Executed at Jinx's
  desk: Janx's v3 (which already carried Room Zero v2's laws verbatim)
  is the base; it now serves at the Room Zero address as THE FORGE
  ROOM. Room Zero v2 and Janx's untouched v3 are archived under
  docs/vr/archive/. Headless boot verified: kernel ready, full
  toolbar, zero errors. Headset behaviour still awaits his stand.
- OWNER RULING (sound): UI sound effects are IN; an AI talking in the
  room stays OUT (no Web Speech — voice is external, phone/earbud).
  Jinx's merge pass added a small WebAudio layer (sfx): grab tick,
  two-hand tick, settle thunk, export success pair / warning low /
  failure low. SFX flag mutes it. The haptic tick rides as built.
- STILL OPEN for the owner: mirror-after-restore behaviour,
  vidIQ pack word, haptics keep-or-cut (riding as built meanwhile).

## 2026-10-31 — Round 2 (first stand graded by the owner's hands)
- FIRST STAND (owner, morning): the room PROVED itself (dummy, ghost,
  plate all seen; "super duper cool") — the CONTROL PACKAGE failed:
  wrist panel read his palm backwards (showed palm-down, hid palm-up),
  glitched at the old test's edge, hung off his left unfaced; table
  stood too tall for his chair. Session cut short by dead controller
  batteries. His orders: refine the controls; start a hand-free path.
- BUILT (Janx, Q29): Control Package v2 as a diff on the file of
  record — head-relative palm test (hand-to-head in the hand's own
  frame, axis -X default per his hand's report) with a teach gesture
  (hold left stick click 1 s = whatever pose he shows becomes the
  panel pose, saved); deadband 0.80/120 ms show, 0.50/250 ms hide;
  panel anchored at the fist, facing the eye, third row UNDO/TOOL;
  adjustable table (amber handle pull or desktop buttons, 0.45-1.10 m
  in 1 cm steps, remembered, default 0.85; parts ride the table);
  hand-tracking path beside the controllers (pinch = trigger,
  pinch-hold = grab, open left palm to face = panel; HANDS flag
  disables; controllers stay primary).
- VERIFIED + PUBLISHED (Jinx): diff and tests downloaded byte-exact;
  base hash and patched hash reproduced EXACTLY (58,295 B,
  1e1e8189...); desk publish adds only the two stale-comment
  corrections from Round 1 (58,420 B). Headless boot: kernel ready,
  TABLE buttons aboard, zero errors. NOT proven: everything inside
  a headset — his next stand on fresh batteries is the grade.

## 2026-10-31 — Round 3 (second stand; the workshop opens)
- SECOND STAND (owner, 11:24 ET, rulings given in Janx's chat):
  grabbing and moving FELT GOOD. The wrist panel failed again (did
  not show on the turn; faced wrong when it did) — his order: move
  it to a WALL PANEL on his LEFT. Mirror OFF by default. Resize was
  undiscoverable. "The tools are a go."
- BUILT (Janx): Workshop v1 on the CP2 file — wrist panel removed
  entire (palm test, teach, pin gone); fixed wall board 1.2 m left
  at 1.25 m, 44 x 66 cm, 8 big buttons (MIRROR, BED, EXPORT, REF,
  UNDO, REDO, RECALL, TOOLS HOME) + readout; press by ray or by
  poke (once per approach); dummy stepped back 35 cm. Mirror starts
  OFF; save format v4 keeps his last setting; older saves restore
  OFF (their ON was the old default). Resize: second hand's grip
  ANYWHERE starts two-hand scale (was: ray had to hit the part);
  one-hand way added — hold a part, stick up/down steps 5%, snaps
  on release, one undo step. TOOL BENCH on his right, top riding
  the table height: 5 stock tools (carry to the plate, let go,
  becomes a part; bench restocks), CHISEL (cut toggle), PIN (solo),
  HAMMER (delete; undo restores). Dropped tools fall 0.7 s then
  glide home; within 12 cm they snap home. RECALL (stick click or
  wall button) flies the last tool to the hand. Tools are furniture,
  never parts, never exported. WORKSHOP flag removes the bench.
- VERIFIED + PUBLISHED (Jinx): base, diff and tests byte-exact;
  Jinx's own patch application reproduced her claimed result
  exactly (73,233 B, SHA-256 095778f8...6871) — second witness to
  the watch's reproduction. Headless boot: kernel ready, MIRROR OFF
  showing, zero errors. Her 44 tests + trimesh STL check stand as
  her runs. One slip named to her: the check word ANVIL does not
  appear in the published file (TRESTLE did, in hers).
  NOT proven: hand-joint frames, poke distance feel, recall grip
  angle (one constant, CANON). His next stand grades it.
- NEXT (Janx, after that stand): the sculpt bench — clay
  add/carve/smooth, the day-or-two piece.
