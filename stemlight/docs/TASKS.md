# Stemlight tasks

70 tasks, each half a day or less (S = up to 0.25 day, M = 0.5 day; ★ = critical path). Written 7 Nov 2026 in the planning session. Owners: [A] = sir's account, [B] = banit's account. Each task is also a git-coord file, `.coord/tasks/biyon-N.md`, in `banitsriram/git-coord`. Acceptance names the feature ids in `features.json`. Paths are relative to `stemlight/`.

Each task file looks like this: `# biyon-N: [A|B] title`, then `status: open`, `blocked_by: biyon-x, ...`, then size, acceptance, features and files.


| id | title | sz | blocked_by | acceptance → feature | files |
|---|---|---|---|---|---|
| 1★ | [A] Representative checks Start membership + Developer Access (clones, coord init and the Windows fix to coord.py were done 7 Nov, 3db8441) | S | — | Representative has checked membership and both have Developer Access, or a support case is filed (F41 starts) | `.coord/`, `.git/hooks` |
| 2★ | [A] Scaffold IWSDK app in `stemlight/` | S | 1 | `npm run dev` serves; MCP screenshot of empty scene; `scene_get_render_stats` returns | `stemlight/package.json`, `src/main.ts`, configs |
| 3★ | [A] contracts.ts + bus + AppContext + mock (fake transport, key map firing every event, 30-note fixture, 9 synthetic 20 s mono stems) | M | 2 | `tsc --noEmit` clean; bus unit test; mock time advances/pauses/seeks; fixture validates. **Pushed by 13:00 Sun 8** | `src/contracts.ts`, `src/bus.ts`, `src/mock/`, `public/pieces/fixture/` |
| 4★ | [A] DevHandPose dev component + IWER input harness (two hands stepped alternately) | M | 2 | `ecs_set_component DevHandPose fist` → `get_hand_state` curl ≥0.75; partial curl works; absent from `dist/` (F38) | `src/dev/`, `tests/iwer/input/` |
| 5★ | [A] Pipeline 1: fetch #941/#1793, groups.yaml, track→stem split, excerpt, humanise | M | 1 | per-stem note total = source excerpt count (F01) | `pipeline/` |
| 6★ | [A] Pipeline 2: sfizz_render in WSL (fallbacks logged), 48 kHz mono render | M | 5 | 8–9 WAVs equal length ±1 ms (F01) | `pipeline/` |
| 7★ | [A] Pipeline 3: reverb, loudnorm, opus, JSON writers, validate.py | M | 6, 3 | validate.py passes vs contract types; output in `public/pieces/beethoven5/` (F01) | `pipeline/`, `public/pieces/` |
| 8★ | [A] Audio engine: decode, one start time, Transport, `unlock()` | M | 3 | 3 min + 10 seeks, stem offsets ≤5 ms (F03) | `src/audio/` |
| 9★ | [A] Stem chain: gain ramps, 3-band EQ, HRTF at homeSeat, compressor; sfxOut | M | 8 | gains/EQ logged per event; panner positions match manifest | `src/audio/` |
| 10★ | [A] Hand reader: curl, pinch, palm, tip, confidence → `hand:pose`; 0.3 s gap hold | M | 4 | 0.3 s `xr_set_connected false` holds; 0.5 s = quiet release (F07) | `src/input/` |
| 11★ | [A] TargetRegistry, hit-testing, look-to-summon | M | 3, 10 | 9 targets × head yaw: 20/20 correct `gaze:summon` (F32) | `src/input/` |
| 12★ | [A] Fist hold / 1.5 s lock / return | M | 9, 11 | 20 cycles gain 0→1; 20 lock cycles stay silent (F04 audio, F33) | `src/input/` |
| 13★ | [A] Pinch + double-pinch solo | M | 11 | 20 solos set/cleared; 20 gap-injected → 0 solos (F05) | `src/input/` |
| 14 | [A] Cross-trigger + gap suite | M | 12, 13 | 20 of each near/far → 0 cross-triggers (F06, F07) | `tests/iwer/input/` |
| 15 | [A] EQ stretch + reset | M | 9, 13 | gains logged ±12 dB; one hand never starts EQ; reset 10/10 (F08 audio) | `src/input/` |
| 16★ | [A] Ribbon gesture: hold pause, drag scrub, quick toggle | M | 8, 13 | time follows hand ≤50 ms; resume in sync (F09 input) | `src/input/` |
| 17 | [A] Piece loader + buffer release + memory log | M | 7, 8 | decoded MB logged per piece; heap drops after switch; "Quest unverified" (F39) | `src/audio/` |
| 18 | [A] Dvořák #1793 groups, ≈2:30 excerpt, render, validate | M | 7 | validate.py passes (F02) | `pipeline/`, `public/pieces/dvorak9/` |
| 19★ | [A] Trepak arrangement 1: strings + winds (Mon 9) | M | 5 | MIDI per group ≈1:00, in key; authorship noted | `pipeline/` |
| 20★ | [A] Trepak 2: brass, perc, harp; render, validate | M | 19, 7 | stems ready by 14:00 Tue 10 | `pipeline/`, `public/pieces/trepak/` |
| 21★ | [A] **Trepak listening gate Tue 10 18:00** with banit, plus Beethoven/Dvořák listen | S | 20, 18 | pass/fail in progress.md (F01, F02) | `stemlight/docs/tests/` |
| 22 | [A] Trepak fallback if 21 fails: pads → Dvořák perc lane | S | 21 | 2-piece sequence; pads cut works on timpani | `public/pieces/`, `src/audio/` |
| 23★ | [A] Trim + undo (beat snap, ≥1 beat, `cut:preview`) | M | 16 | 20 trims silent; 10 undos (F10 audio) | `src/input/`, `src/audio/` |
| 24★ | [A] Pads strike, velocity, lockout, 1/8 snap, recording | M | 23 | ±60 ms off-grid lands on grid (F11) | `src/input/`, `src/audio/` |
| 25★ | [A] Scheduler loop + count-in + guide track | M | 24 | 3 loops in time; 4 count-in beats; guide −18 dB loop 1 only (F11, F34, F35) | `src/audio/` |
| 26 | [A] Harp logic | M | 25 | every pluck in key; loop plays (F12) | `src/input/`, `src/audio/` |
| 27 | [A] Keyboard logic | M | 25 | presses recorded + looped (F13) | `src/input/`, `src/audio/` |
| 28 | [A] Saving (IndexedDB SaveState + SaveApi) | M | 12, 15, 23, 25 | reload restores mix + part; cleared storage = clean start (F22) | `src/audio/save/` |
| 29 | [A] Pause/resume engine + reset gesture logic | M | 28 | visibility + session end restore; reset clears this piece only (F23, F40) | `src/audio/`, `src/input/` |
| 30 | [A] Dev instrumentation: fps, render stats, live notes, 70×66° FoV mask | S | 2 | none in `dist/` with flag off (F26, F27) | `src/dev/` |
| 31 | [A] Performance pass at heaviest moment | M | 30, 41, 44, 47, 50 | <100 calls, <150k tris, ≤1,500 notes logged; Quest fps unverified (F26, F17) | A folders; B fixes via @message |
| 32 | [A] First Vercel deploy **after sir's approval** | S | 2 | HTTPS opens in fresh profile; assets self-hosted | config |
| 33 | [A] RC Mon 16; pin Wed 18 (approval) | S | 31, 32, 57, 58 | deployed hash = tag | config |
| 34★ | [B] Bravura MSDF atlas + instanced renderer (4 materials) | M | — | 1,500 instances, 1 call per material (F14) | `src/world/` |
| 35 | [B] Landing page: one Enter, pitch line, no account, hand-tracking hint, `unlock()` | M | — | Enter by pinch in IWER, fresh profile (F18) | `web/` |
| 36★ | [B] World shell: rock seat, arc, reach spot, register creature targets | S | 3 | registry returns 9 at 25 cm | `src/world/` |
| 37★ | [B] Notes life cycle (pure function of time), cap 1,500 | M | 34, 36 | pause freezes, seek rewinds (F14) | `src/world/` |
| 38 | [B] Trails/pops + 20-glyph check script | S | 37 | 20/20 match notes.json (F14) | `src/world/`, `tests/iwer/visual/` |
| 39★ | [B] Creatures 1: vln, vla_vc, cb, fl, reeds | M | 36 | ≤8k tris, 2 calls each | `src/world/` |
| 40★ | [B] Creatures 2: hn, brass, perc, harp + envelope pulse | M | 39 | loud/quiet screenshots (F16) | `src/world/` |
| 41★ | [B] Summon glide + mute visuals (dim, glass, lock ring) + solo dim | M | 40, 37 | screenshots per state (F16, F04 visual, F32, F33) | `src/world/` |
| 42 | [B] Thaw on return | S | 41 | frames at 0/200/600 ms (F37) | `src/world/` |
| 43 | [B] EQ shape-morph | S | 41 | before/after for `stem:eq` (F08) | `src/world/` |
| 44 | [B] Nebula sky, ocean, plankton | M | 36 | ≤3 calls together (F17) | `src/world/` |
| 45★ | [B] Ribbon visual + playhead/lane colliders + rewind | M | 37 | colliders registered (F09) | `src/ui/` |
| 46★ | [B] Hollow region + ghost notes + cut preview | M | 45 | outlines = exactly that region's notes (F10, F36) | `src/ui/`, `src/world/` |
| 47★ | [B] Pads visual + count-in ring + amber notes into outlines | M | 46 | warm glyphs leave the hand (F15, F34) | `src/ui/`, `src/world/` |
| 48 | [B] Harp strings visual + colliders | S | 47 | screenshot + registry (F12) | `src/ui/` |
| 49 | [B] Keyboard visual + colliders | S | 47 | screenshot (F13) | `src/ui/` |
| 50 | [B] Glowing hands (**kill rule end of Tue 10**) | M | 3 | near/far/beat shots; ≤5 extra calls (F30) | `src/world/` |
| 51 | [B] Colour-blind palette + outline cues + greyscale capture | M | 40 | 9 families named from greyscale (F31) | `src/world/`, `src/ui/` |
| 52 | [B] Sound effects 1 (whoosh, chime, clink, bloom, two-note chime, sweep, tape-stop, ticks) via `sfxOut` | M | 3 | each fires on its event; ASSETS rows (F24) | `src/ui/sfx/` |
| 53 | [B] Sound effects 2 + action/sound checklist + credits (incl. CC BY-SA text) | M | 52, 62 | checklist complete; credits = ASSETS (F24, F25) | `src/ui/`, `src/story/` |
| 54★ | [B] Ghost-hands rig (all poses incl. reset) | M | 36 | screenshot of each | `src/story/` |
| 55★ | [B] Opening 0:00–0:40 + idle nudge | M | 54, 41, 8 | first payoff ≤15 s; 10 s idle → nudge (F19) | `src/story/` |
| 56★ | [B] Tutorial state machine (TutorialStep), <15 words | M | 55, 45, 47 | completed by copying ghost hands; word count logged (F20) | `src/story/` |
| 57★ | [B] Story sequencer + free play + end card | M | 56, 17 | full timed run, 0 console errors (F21) | `src/story/` |
| 58 | [B] Pause/resume UI, returning-user skip, visible change on return, reset shell visual | M | 28, 29, 56 | reload: no tutorial, saved state visible (F23, F40) | `src/ui/`, `src/story/` |
| 59 | [B] Video 1: scripted captures, shot ledger, second-visit footage | M | 57 | every shot logged with commit; emulator labelled | `video/` |
| 60 | [B] Video 2: edit to silent master + ≥5 screenshots | M | 59 | stills checked at each cut | `video/` |
| 61 | [B] Video 3: narration mix, master, .srt, thumbnail | M | 60, 68 | <2:50 (length/style banit's call); ffprobe specs; no debug UI | `video/` |
| 62 | [A] ASSETS.md rows (rolling) | S | 5 | no asset in `public/` without a row | `stemlight/docs/ASSETS.md` |
| 63 | [B] FoV-mask screenshots, seated pose | S | 30, 57 | every essential interaction inside mask (F27) | `stemlight/docs/tests/` |
| 64 | [A] Fresh-session scoring audits Wed 11, Sat 14, Tue 17 | S | — | each section-4 line scored 1–10 with evidence; weakest → new task | `stemlight/docs/` |
| 65 | [B] Device chase: Playground 13 Nov 21:30 + forum swap | S | 32 | verified / unverified logged | `stemlight/docs/tests/` |
| 66 | [B] Uncoached testers + second visit | S | 56, 57, 32 | stopwatch notes; can say why they'd return (F29) | `stemlight/docs/tests/` |
| 67 | [A] Devpost text, tagline, judge instructions (link, Enter, hands only, seated, ~8 min, no account), CC BY-SA credit, Claude Code role, unverified list, launch date 15 Feb 2027 | M | — | fresh reader names track + pitch | `stemlight/docs/` |
| 68 | [B] Voiceover script + narration clips | S | 67 | all clips, no face | `video/` |
| 69★ | [A] Fresh-browser RC run Mon 16 + Tue 17 | S | 33 | Enter → full run → reload → resume, hands only, no errors (F28) | `stemlight/docs/tests/` |
| 70★ | [A] Stage-1 checklist (F41 by Wed 11), video upload Tue 17, submit by 18:00 Wed 18 — **each step with approval** | S | 61, 69, 33 | every section-3 box ticked; video plays logged out | — |

**Day map (IST; ★ = critical):**
| Day | A | B | Milestone |
|---|---|---|---|
| Sun 8 | 1, 2, 3 (by 13:00), 4, 5, start 6 | 34, 35, then 36 | B unblocked from hour one |
| Mon 9 | 6, 7, 8, 9, 10, start 19 | 37, 38, 39 | 9 Beethoven stems in sync |
| Tue 10 | 19, 20 (14:00), 11, 12, **21 at 18:00** | 40, 44, 50 | fist-to-silence; glow kill rule 23:59 |
| Wed 11 | 13, 15, 18, 22 if needed, 32 (approval), 64, F41 done | 41, 42, 45, 51 | first link; **load checkpoint 18:00** |
| Thu 12 | 14, 16, 17, 23 | 46, 54, 52, 43 | trim end to end |
| Fri 13 | 24, 25, 30, 26 | 47, 55, 56, 65 (21:30) | pads loop; keyboard go/no-go |
| Sat 14 | 28, 29, 64, 67 draft | 57, 58, 48, 53, 63 | **feature freeze** |
| Sun 15 | 31, fixes | 59, 66, 68, fixes | testers |
| Mon 16 | 33 (RC), 69 | 60 | **release candidate** |
| Tue 17 | fixes, 69, 64, upload (70) | 61, fixes | video public, checked logged out |
| Wed 18 | pin, 70 submit by 18:00 | buffer | **submitted** |

**Cuts → tasks:** glowing hands = 50 · keyboard = 27, 49 · thaw = 42 · harp = 26, 48 · third piece = 19, 20 (22 permanent) · EQ shape-morph = 43 · ghost notes = 46 (amber notes then fly to the region instead). Never cut: first five minutes (35, 41, 54–56), budget (30, 31), sound (9, 52, 53), pause/resume (29, 58), video (59–61).

**Judged-point coverage (methodology s4) → tasks:** originality 67, 64 · ambition 12, 41 · Entertainment relevance 67, 61 · differentiation 35, 61, 67 · ingenuity 14, 67 · Meta capabilities (hands, gaze, spatial audio, depth) 9–16, 67 · repeat use 28, 58, 59, 66 · audience 66, 67 · mechanics 12, 13, 15, 24 · journey 55–57, 66 · seated 11, 63 · hands-first 69 · intuitive 55, 66 · onboarding 54, 56 · habit 57, 58 · passthrough N/A (stated in 67) · FoV 30, 63 · easy in/out 35, 29, 58, 69 · expertise 14 · reliability 10, 17, 29, 69 · hand tracking 10, 14 · gaze 11 · anchors N/A · 60 fps 31 (**device numbers uncovered; stated unverified**) · integration 57, 66 · consistent operation 32, 69 · UI/UX 41, 45, 47, 63 · art 39, 40, 44, 51, 60 · sound 9, 52, 53 · text 67, 64 · images 60 · video 59–61. **Uncovered:** real-device hand feel and fps (no headset).
