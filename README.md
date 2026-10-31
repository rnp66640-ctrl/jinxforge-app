# jinxforge-app

The shared workshop between Jinx (the shop desk) and Janx (Claude), and the home of the
picture-to-model app for JinxForge.

## House rules (read first)
- This repository is PRIVATE. Nothing here is public, posted, or listed anywhere.
- No secrets in this repository, ever: no passwords, tokens, keys, codes, or card numbers.
  Access is granted through account settings by the owner's own hands only.
- Keep every file under 100 MB. Zip large meshes. No Git LFS for now (unconfirmed on Janx's side).
- Franchise and licensed-character pieces are personal/display only: never for sale,
  never listed, never posted.
- Verdicts flow Janx -> Jinx -> Richard. Richard's grade is the only grade that ships anything.

## Layout
- tools/     — Janx's gate and grading tools, plus build tests (each script declares its dependencies at the top)
- pipeline/  — the app's steps and trial protocols
- exchange/  — model files moving between the desks: to-janx/ and to-jinx/
- docs/      — standing orders as text, the licence register, shared references
