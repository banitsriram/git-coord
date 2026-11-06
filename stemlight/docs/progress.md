# Progress

Newest entry first. Each session reads this, then `PLAN.md`, then `features.json`. Strata's history is in `docs/archive/`.

## 7 Nov 2026 (night): build-ready plan approved, coordination set up, no app code

**State**
- `PLAN.md` refined into a build-ready plan and approved by sir. It covers:
  - the exact gesture spec, the visual system and the music pipeline
  - `contracts.ts` (section 6)
  - the any-song roadmap, with a beta on 15 Feb 2027
- `TASKS.md` holds 70 tasks (each ≤0.5 day, with owner, blockers, acceptance and files). `features.json` now has F01–F41, all `passes: false`.
- Coordination: `banitsriram/git-coord`, app in `stemlight/`. See `COORDINATION.md`.
  - git-coord hooks are installed in `~/.claude/settings.json` (backed up first).
  - The skill is cloned to `~/.claude/skills/git-coord` and the working clone is at `~/projects/stemlight`, agent name `biyon`.
- Pushed to banit's repo:
  - `3db8441`, a 2-line Windows fix to `coord.py`: commit guard via `sys.executable`, edit-hook paths normalised to `/`.
  - `.coord/biyon.md`, with an @banit request to make the repo private.
- Team is sir and banit only.

**Verified on 7 Nov**
- Live rules and judging page re-read and still match the methodology. Vercel or GitHub Pages hosting is allowed.
- git-coord `test_coord.py`: failed on Windows before the fix (`python3` stub, then backslash paths). It passes after the fix, which also works in real use: init published and the edit hook allowed `.coord/biyon.md`.
- Sources:
  - Dvořák 9 mvt 4: full orchestra on **Mutopia #1793, CC BY-SA 3.0**, so we no longer write our own Dvořák.
  - Trepak: no licensed file anywhere, so we still write our own.
  - Bravura is OFL-1.1 and sfizz is BSD-2. Beethoven on Mutopia #941 is PD.
- IWER has a `fist` preset, per-finger curl and tracking-loss toggles. The IWSDK MCP has **no hand-pose tool**, so we use a dev-only `DevHandPose` component (task 4).

**Not verified**
- Anything on a headset. There is none, so frame rate and hand feel stay unverified.
- Sound quality of the renders, and `sfizz_render` in WSL.
- Decoded audio memory on Quest (estimate about 230 MB for the Dvořák excerpt).
- Start membership and Developer Access (F41, by Wed 11).

**Next**
1. Sun 8: task 1 (membership), tasks 2–5 (A), tasks 34–35 then 36 (B). Contracts and mock pushed by 13:00 so B is unblocked.
2. banit: make the repo private, `init banit`, claim B folders, read `stemlight/docs/PLAN.md`.
3. Wed 11 18:00 load checkpoint; Tue 10 18:00 Trepak gate.

## 7 Nov 2026 (later): council add-ons approved

- Council Session 9 (log: `~/projects/shared_reasoning.md`) reviewed 12 add-on ideas and ruled to keep the plan, plus **glowing hands** (F30) and a **colour-blind palette with shape cues** (F31), about 1 day. Sir approved.
- It was a fragile ruling (68.5 vs 67 for no change). Kill rule and stretch gate are in `PLAN.md` section 12.
- New rival found: **Maestro** (Quest, Oct 2024), hand-tracked conducting. Added to `PLAN.md` section 1. We never add conducting gestures.

## 7 Nov 2026: pivot to Stemlight, plan written, no code

**State**
- The team agreed to replace Strata with **Stemlight**: a hands-only VR music visualiser where you reach in and silence, reshape, cut and replace instruments while real notes float around you.
- Entertainment, New Experience, IWSDK. No headset: emulator (IWER) only.
- `PLAN.md` and `features.json` rewritten. Strata's files moved to `docs/archive/`.
- No app code yet.

**Verified on 7 Nov**
- VSCO 2 Community Edition is **CC0-1.0** (GitHub licence API). It has string sections, harp, full brass and woodwinds, timpani, orchestral percussion, glockenspiel, xylophone, marimba and upright piano. SFZ on the `sfz` branch.
- VCSL is CC0 and adds concert harp, vibraphone and tubular bells. **No celesta in either library.**
- Beethoven 5th mvt 1: full orchestra on Mutopia, **Public Domain**, MIDI + LilyPond.
- Dvořák 9 mvt 4 and the Trepak: no trustworthy free full-orchestra file found, so we write our own arrangements from the IMSLP PD scores.
- "Stemlight": no existing app or VR product found by web search on 7 Nov. The Quest store wasn't searched directly.
- IWER emulates hands in Chrome: hold the mouse to pinch, drag to move, scroll for depth. Pinches can be scripted.
- Prior art to differentiate from: Google's Inside Music (2017, stems around you as toggles), Hyperspace Music, Chromesthesia.

**Not verified**
- Anything on a real headset.
- How the rendered orchestra sounds.
- The Bravura MSDF pipeline, and IWSDK performance with ~1,500 instanced notes.

**Next**
1. Sun 8: scaffold IWSDK; render Beethoven stems; spike 9 synced stems + fist-to-silence in IWER.
2. Start the Dvořák and Trepak arrangements (Account C checks the sources).
3. Confirm the Representative's Start membership is still in order.
