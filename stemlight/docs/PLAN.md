# Stemlight: project plan

Replaces Strata (archived in `docs/archive/`), with the team's agreement on 7 Nov 2026. Refined into a build-ready plan on 7 Nov (planning session, approved by sir). Rules come first, in this order: the live competition rules, then `COMPETITION-METHODOLOGY.md`, then this file.

Internal deadline **Wed 18 Nov 2026 18:00 IST**. Hard deadline Thu 19 Nov 01:30 IST.

**Team:** sir (Account A) and banit (Account B). Nobody else. Coordination and code: `banitsriram/git-coord`, app in `stemlight/` (see `COORDINATION.md`).

## 1. Pitch

**One line, used word for word in the build, the video and the write-up:**
*The music you can reach into: silence it, reshape it, play your own part, while every real note floats around you.*

- **What it is:** a seated, hands-only VR music visualiser.
  - A piece of music is split into its instruments.
  - Each instrument becomes a glowing creature around you.
  - Every real note leaves it as a floating notation symbol.
  - With bare hands you can silence, solo, EQ, cut and replace any part, and play your own replacement on pads, a harp or a keyboard.
- **Inspired by** stem splitters and DAW-style editing, turned into something you sit inside. **Internal only:** the inspiring apps (Ultimate Vocal Remover, Moises, LALAL.ai, Ableton Live) and rivals are never named, shown or imitated in the build, the video or the Devpost text (rules ban brand names).
- **Track:** Entertainment ("music visualization" is named in the track description, rechecked 7 Nov). **Division:** New Experience. **Build path:** IWSDK.
- **Audience:** adults who love music but don't play, at home in the evening, seated, about 10 minutes. Second: players curious how an orchestra fits together.
- **What only this does** (the line we repeat): you *reach in and remake* real, separated parts. Rivals either let you watch or let you conduct:
  - **Maestro** (Quest, Oct 2024) is the closest rival: a hand-tracked orchestra you *conduct*. Stemlight never conducts. You take parts apart and remake them, and every note is visible.
  - Google's Inside Music (2017) placed stems around you as toggles. Electronauts remixes by hover-and-click. Hyperspace Music and Chromesthesia are visualisers.

## 2. Core loop and the first ten minutes

**Loop:** listen → look at an instrument (it comes to you) → reach in (silence / solo / stretch) → hear the change → cut a part → play your own → hear it loop back in.

| Time | What happens | Purpose |
|---|---|---|
| Before XR | Landing page, one big Enter, works by pinch. Pitch line. No sign-up. One line if hand tracking is off | Easy in |
| 0:00 | Dark ocean-space, silence. A violin jelly waits at the reach spot. A ghost hand shows a pinch, and that pinch starts the audio | Payoff in under 15 s, and the gesture unlocks audio |
| 0:15–1:30 | **Beethoven 5th** opening (≈1:20). The orchestra blooms family by family. Ghost hands teach **look = summon**, **fist = silence**, **open = return**, **hold = lock**, **double-pinch = solo** | Signature action learned by copying, no text |
| 1:30–4:00 | **Dvořák New World, 4th mvt** (≈2:30 excerpt). The score ribbon appears: **pinch the playhead = pause, drag = scrub**. Then **two-hand stretch = EQ** on the horns | Hero piece |
| 4:00–6:30 | **Tchaikovsky, Russian Dance (Trepak)** (≈1:00, looped). Pinch two points on the percussion lane to **cut**. Ghost notes show the hole. A one-bar **count-in**, **pads** rise, you drum, it snaps to the beat, loops in, and your amber notes fill the ghost outlines. Harp (and keyboard if shipped) unlock | Play your own part |
| 6:30+ | Free play: any piece, any tool. Mix and parts saved. End card: "any song, coming" | Reason to return, shows what's next |

- If the Trepak fails its Tue 10 listening gate, it is dropped and the cut-and-drum moment moves to Dvořák's timpani lane.
- A tester who does nothing gets a nudge after 10 s. No failure state.
- Pause and resume: system button, headset off and session end all restore state and audio without repeating the tutorial. Returning users skip the teaching and see their saved mix. A quiet reset is always available (section 3).

## 3. Hand interactions (exact spec)

Seated, within a 2 ft radius, hands only. Every action has a sound and a visual. All numbers are our calls, tuned in IWER, re-tuned on a device if one is found.

**Verbs, as the write-up frames them:** grab (fist), pinch (pinch, double-pinch, stretch, ribbon, cut, reset), touch (pads, harp, keys), plus gaze (look to summon).

**Look to summon.** Creatures wait in a 100° front arc at 1.4–2.6 m, two tiers like orchestra seating. Head direction within 12° of one for 0.5 s glides it to the **reach spot** (0.45 m ahead, 0.15 m below eye) in 0.6 s, and the previous one drifts back. Only the summoned creature takes fist, pinch and EQ. Quest 3/3S have no eye tracking, so head direction is the gaze; the write-up says so.

**Fist.** Hold = silent, open = back. Held 1.5 s, the glass fully forms with a clink and **locks**, so the part stays silent after the hand opens. A fist on a locked creature returns it.

| Gesture | Enter | Exit / hysteresis | Tracking gap (≤0.3 s holds; longer = quiet release, no action) | Conflicts resolved by | Sound / visual | IWER test |
|---|---|---|---|---|---|---|
| Summon | head ray within 12° for 0.5 s | looking away does not dismiss; the next summon replaces | n/a | one summoned at a time | soft whoosh; glide in | head yaw to each of 9, 20× correct |
| Fist (silence) | 3 of 4 fingers curl ≥0.75, palm inside the summoned creature's 25 cm sphere, 80 ms debounce | curl ≤0.45 | hold | pinch requires other fingers curl ≤0.6, so the two can't overlap | glassy chime; notes freeze to glass; lock ring fills over 1.5 s, clink | 20 fist/open cycles with gain checked; 20 lock cycles |
| Return | open before 1.5 s, or fist again on a locked one | — | hold | — | thaw: glass cracks into sparkles, warm bloom | as above |
| Pinch | thumb–index tips ≤1.5 cm, other fingers curl ≤0.6 | ≥3.0 cm | hold | fist rule above | tick | 20×, zero fist triggers |
| Double-pinch (solo) | 2 pinch-downs, same hand, ≤450 ms, moved <4 cm, tracking unbroken, other hand idle | a second double-pinch clears | a gap cancels it | EQ needs both hands | rising two-note chime; others dim to 25 % | 20×; 20 with an injected gap → 0 solos |
| EQ stretch | both hands pinch inside the creature within 0.5 s | releasing either commits | hold | one hand never starts EQ | filter sweep; creature widens (bass) or stretches tall (treble), ±12 dB | scripted stretch, filter gains logged |
| EQ reset | both pinched hands brought within 6 cm | — | — | — | click, creature snaps to rest | 10× |
| Ribbon pause / scrub | pinch the playhead (6 cm collider): hold = pause, drag = scrub, release = resume; a pinch under 250 ms and 1 cm toggles pause | — | hold | ribbon colliders are separate from creature spheres | tape-stop; scrub ticks; notes rewind | time follows the hand within 50 ms; resumes in sync |
| Trim | both hands pinch the same lane within 0.6 s; region snaps to beats, at least 1 beat | release | hold | lane vs playhead colliders | glass snip; region hollow; ghost notes | 20×, region silent |
| Undo trim | pinch a hollow region and pull it ≥10 cm off the ribbon | — | — | — | reverse snip | 10× |
| Pads | index tip crosses the pad plane at ≥0.4 m/s; 0.4–2.5 m/s maps to velocity 30–127; 90 ms lockout; snap to 1/8 | — | a gap means no hit | shown only after a percussion cut | the hit, plus an amber note from the fingertip | strikes ±60 ms off-grid land on the grid; 3 loops |
| Harp | index tip crosses one of 8 strings tuned to the piece's scale | — | — | shown after a melodic cut | pluck, plus an amber note | every note in key |
| Keyboard | index tip moves down through a key top at ≥0.15 m/s; 8 big keys (5 cm) on the scale; 90 ms lockout | — | — | shown after a melodic cut | key note, plus an amber note | presses recorded and looped |
| Quiet reset | pinch and hold the small glowing shell beside the right knee for 2 s | release early cancels | hold | shell collider is apart from everything else | ring fills; soft reset chime | resets this piece's mix only, 10× |

**Testing hands without a headset.** IWER has preset poses including `fist`, writable `poseId` and per-finger curl (`setFingerPose`), and `connected` toggles tracking loss. The IWSDK MCP tools (0.5.3) have no hand-pose command, so A builds a dev-only `DevHandPose` component that tests flip with `ecs_set_component`; it never ships. Simultaneous two-hand moves are unverified in IWER, so two-hand tests step the hands alternately each frame. Emulator results never prove hand feel.

## 4. How the music is made (owner A)

**Sources**
- **Beethoven 5th, mvt 1:** Mutopia #941, full orchestra, **Public Domain**, MIDI + LilyPond (Breitkopf & Härtel 1862–65).
- **Dvořák 9, mvt 4:** Mutopia #1793, full orchestra, **CC BY-SA 3.0** (Simrock 1894 edition, maintained by Keith OHara). Our stems and `notes.json` made from it are released under CC BY-SA 3.0, with credit in the app, the video description and the Devpost text. The app code is unaffected.
- **Trepak:** no licensed file exists (checked 7 Nov), so **our own arrangement** (≈1:00) from the IMSLP public-domain score, written by Claude as `pretty_midi` code per group. Listening gate Tue 10 18:00 IST, both of us.

**Steps** (Python in WSL2 Ubuntu; times are estimates)
1. Fetch sources and save the piece-page links in `ASSETS.md` (0.5 h).
2. `groups.yaml` per piece maps MIDI tracks to stem ids (2 h). Beethoven and Dvořák use 8 stems (no harp in either), the Trepak 9.
3. Excerpt by bar range to seconds via the tempo map (1 h).
4. Humanise: ±8 ms onset jitter, velocity curve per family (1 h).
5. Render each group with `sfizz_render` and **VSCO 2 CE** (CC0; VCSL for harp and bells) to 48 kHz **mono** WAV (3 h with the WSL build; unverified until Sun 8).
6. One shared CC0 convolution reverb, then per-stem loudness normalising with ffmpeg `loudnorm` (2 h).
7. Encode `stems/<id>.opus`, 96 kbps mono (0.5 h).
8. Write `notes.json`, `beats.json`, `envelopes.json` (RMS per stem at 30 Hz, 0–1) and `manifest.json` (2 h).
9. Validate: note count against the source excerpt, all stems equal length ±1 ms, listen-through (1 h).

Once the pipeline exists: Beethoven about 1 h, Dvořák about 2 h, Trepak 4–6 h of arranging plus 1 h of rendering.

**Memory (estimate, unverified on Quest):** mono stems decoded at 48 kHz take about 230 MB for the 2:30 Dvořák excerpt. The previous piece's buffers are released on every change, and decoded size is logged per piece.

**Fallbacks:** synthetic sound → more reverb, simpler voicing, velocity layers. Trepak fails the gate → drop it, pads move to Dvořák's timpani. sfizz won't build in WSL → the sfizz Windows release, else FluidSynth with an SF2 conversion (licence check first).

## 5. Audio engine (owner A)

- Web Audio. Stems are decoded once and all started on one shared context time, so they never drift.
- **Chain per stem:** gain (mute/solo, 30 ms ramps) → 3-band EQ (lowshelf / peaking / highshelf) → HRTF panner at the creature's seat → master compressor.
- **Pause / seek:** restart the sources at an offset. `Transport.time()` comes from the AudioContext clock.
- **Trim:** gain automation over the cut region.
- **User parts:** a look-ahead scheduler fires small CC0 one-shots (drum hits, harp pluck, glock or piano), looped over the cut region.
- **Count-in:** one bar of soft ticks and `countin` events before the cut region.
- **Guide track:** on your first loop only, the original part plays under yours at −18 dB.

## 6. Contracts between A and B (`stemlight/src/contracts.ts`)

**Principle:** A recognises every gesture; B owns every visual and its collider geometry. B registers colliders in a shared target registry; A hit-tests the hands against it and emits events with target ids. Visuals never read audio nodes, and audio never reads meshes. Changed only by agreement: an @message and the other's reply first.

```ts
export type PieceId = 'beethoven5' | 'dvorak9' | 'trepak';
export type StemId = 'vln'|'vla_vc'|'cb'|'fl'|'reeds'|'hn'|'brass'|'perc'|'harp';
export type Glyph = 'whole'|'half'|'dotted_half'|'quarter'|'dotted_quarter'|'eighth'|'sixteenth'|'beamed_eighths'|'beamed_sixteenths';
export type Hand = 'left'|'right';
export type MuteState = 'on'|'held'|'locked';
export type Vec3 = [number, number, number];
export type Instrument = 'pads'|'harp'|'keys';
export type TutorialStep = 'summon'|'silence'|'return'|'lock'|'solo'|'ribbon'|'eq'|'cut'|'pads'|'free';

export interface NoteEvent { id: number; t: number; dur: number; pitch: number; vel: number; stem: StemId; glyph: Glyph; beat: number } // notes.json = NoteEvent[], sorted by t
export interface Beats { tempo: { t: number; bpm: number }[]; beats: number[]; downbeats: number[] } // beats.json, seconds
export interface Envelopes { rate: 30; stems: Partial<Record<StemId, number[]>> }                   // envelopes.json, 0..1
export interface PieceManifest {
  id: PieceId; title: string; composer: string; durationSec: number;
  stems: { id: StemId; file: string; homeSeat: Vec3; pitchRange: [number, number] }[];
  scale: { tonic: number; steps: number[] };              // harp and keyboard tuning
  replace: { stem: StemId; instrument: Instrument }[];
  credits: { text: string; licence: string; url: string }[];
}
export interface Cut { id: string; stem: StemId; t0: number; t1: number }  // beat-snapped seconds
export interface UserHit { tOffset: number; pitch: number; vel: number }
export interface UserPart { cutId: string; instrument: Instrument; hits: UserHit[] }
export interface MixState { mute: Record<StemId, MuteState>; solo: StemId|null; eq: Record<StemId, { low: number; mid: number; high: number }>; cuts: Cut[]; parts: UserPart[] }
export interface SaveState { version: 1; tutorialDone: boolean; perPiece: Partial<Record<PieceId, MixState>>; palette: 'default'|'cb' }

export type TargetKind = 'creature'|'playhead'|'lane'|'region'|'pad'|'string'|'key'|'reset';
export interface Target { id: string; kind: TargetKind; stem?: StemId; center: Vec3; radius: number; extra?: Record<string, number> } // B registers, A reads
export interface TargetRegistry { set(t: Target): void; remove(id: string): void; all(): Target[] }

export interface Transport { time(): number; playing(): boolean; play(): void; pause(): void; seek(t: number): void; duration(): number } // A implements
export interface AudioApi { unlock(): Promise<void>; context(): AudioContext; sfxOut(pos: Vec3): AudioNode } // B plays sound effects through sfxOut
export interface SaveApi { load(): SaveState; patch(p: Partial<SaveState>): void }

export interface Events {
  'piece:load': { id: PieceId }; 'piece:ready': { id: PieceId; manifest: PieceManifest }; 'piece:end': { id: PieceId };
  'transport:state': { playing: boolean; t: number }; 'transport:seek': { t: number };
  'beat': { index: number; t: number; downbeat: boolean };
  'hand:pose': { hand: Hand; tracked: boolean; confidence: number; palm: Vec3; tip: Vec3; curl: number; pinching: boolean };
  'hand:near': { hand: Hand; targetId: string; dist: number };
  'gaze:summon': { stem: StemId };
  'stem:mute': { stem: StemId; state: MuteState; lockProgress: number };   // lockProgress 0..1 while held
  'stem:solo': { stem: StemId|null };
  'stem:eq': { stem: StemId; low: number; mid: number; high: number };     // dB
  'cut:preview': { stem: StemId; t0: number; t1: number } | null;
  'cut:add': { cut: Cut }; 'cut:remove': { id: string };
  'countin': { cutId: string; beatsLeft: number };
  'part:hit': { cutId: string; instrument: Instrument; pitch: number; vel: number; t: number; from: Vec3 };
  'reset:progress': { progress: number }; 'app:reset': { piece: PieceId };
  'app:pause': {}; 'app:resume': {};
  'tutorial:step': { step: TutorialStep };                                 // B emits; A may gate gestures
}
export interface Bus { on<K extends keyof Events>(k: K, f: (e: Events[K]) => void): () => void; emit<K extends keyof Events>(k: K, e: Events[K]): void }
export interface AppContext { bus: Bus; transport: Transport; registry: TargetRegistry; audio: AudioApi; save: SaveApi } // built in main.ts, passed to each module's init(ctx)
```

- `src/bus.ts` (A) implements `Bus`. `src/mock/` (A, first task on Sun 8, pushed by 13:00) gives B a fake transport, a key map that fires every event, a 30-note fixture and 9 synthetic 20 s mono stems, so B builds from hour one.
- **Rule:** B computes every note position as `f(transport.time() − note.t, note)`. Pause freezes notes and scrubbing rewinds them, with no extra state.

## 7. Architecture and build path

IWSDK + TypeScript (Three.js under IWSDK's ECS). Static build. All paths below sit under `stemlight/` in `banitsriram/git-coord`.

| Folder | Contents | Owner |
|---|---|---|
| `pipeline/` | Python: score → groups → sfizz render → opus + JSON | A |
| `src/audio/` (+ `save/`) | Engine, transport, trim, scheduler, user parts, saving | A |
| `src/input/` | Gesture recognisers, hysteresis, gap tolerance, summon, hit-testing | A |
| `src/dev/`, `src/mock/`, `src/bus.ts` | DevHandPose, fps / render stats / FoV mask behind a dev flag; mocks; bus | A |
| `src/world/` | Creatures, notes (instanced Bravura MSDF), sky, ocean, plankton, hand glow | B |
| `src/ui/`, `src/story/` | Ribbon, ghost notes, pads/harp/keys visuals, sound effects, ghost hands, tutorial, sequencer, credits, pause/resume UI | B |
| `web/`, `video/` | Landing page; video project | B |
| `tests/iwer/input/`, `tests/iwer/visual/` | Scripted IWER tests | A, B |
| `src/contracts.ts`, `src/main.ts`, `package.json` | Shared hot files: claim, edit, commit, release | A+B |

- **Saving:** IndexedDB `SaveState` (mix, recorded parts, tutorial done, palette).
- **Performance budget** (estimates; draw calls / triangles): sky cubemap 1 / 12 · ocean 1 / 2k · plankton 1 · creatures 9 × 2 = 18 / ≤8k each · notes instanced MSDF (normal, glass, ghost, amber) 4 / 3k · hands + glow 4 / 10k · ribbon 3 / 2k · pads/harp 3 / 4k · ghost hands 2 / 10k · labels 2 · sparks 1. **Total ≈40 calls, ≈105k triangles** against caps of 100 and 150k. At most 1,500 live notes, no post-processing, fixed foveation, glow from additive sprites. The fps counter sits behind a dev flag only.
- **FoV:** essential targets (the summoned creature, ribbon, replace instruments, reset shell) sit inside 70×66°. The 100° waiting arc is ambience; the write-up says so.
- **Hosting:** Vercel free plan, deployed by CLI from sir's laptop. **Ask sir before the first deploy.** "Auto-deploy off" means no deploy after the pin.
- **Testing:** IWER in Chrome, scripted hands and head through the IWSDK MCP / headless mode (`npx iwsdk dev up --ai-mode agent`; screenshots, `scene_get_render_stats`).

## 8. Art and sound

- **Space:** you sit on a low glowing rock at the edge of a seabed. Nebula gas drifts overhead, deep ocean lies below, plankton specks hang in the air. Mostly dark and calm.
- **Palette:** void #07060F, violet #2A1B4A, teal #0E5F6B, highlight cyan #6FF3FF. The user's own notes are warm amber #FFB547 (colour-blind palette: #D55E00).
- **Creatures** (shape is the main cue, colour the second; B finalises values, and the greyscale test is the gate):

| Stem | Family | Silhouette | Accent | Colour-blind accent |
|---|---|---|---|---|
| vln | violins | tall slender bell jelly, many fine threads | #5EE6FF | #56B4E9 |
| vla_vc | violas + cellos | wide bell jelly, thick ribbon tendrils | #2FC6B0 | #009E73 |
| cb | basses | heavy manta, slow wing beats, low | #3D6BFF | #0072B2 |
| fl | flutes / piccolo | bead-chain siphonophore, darting, high | #C9B6FF | light #CC79A7 |
| reeds | oboes / clarinets / bassoon | coiled nautilus spiral | #E05BD8 | #CC79A7 |
| hn | horns | curled ammonite with a glowing flare | #7CF0A0 | #F0E442 |
| brass | trumpets / trombones / tuba | branching coral fan, bright tips | #F4F1C9 | #E69F00 |
| perc | timpani / percussion | anemone sphere that pulses on hits | #EEF2FF | #FFFFFF |
| harp | harp / glock (Trepak) | comb jelly with shimmering cilia rows | #FF8FC8 | light #D55E00 |

  Glyph outlines differ per family (solid, ring, double ring, dotted) as a second shape cue.
- **Notes, the anti-slop rule:** every symbol is a real note from the score.
  - Born at the creature's mouth at note-on. The glyph matches the real length. Height = pitch (±0.4 m over the stem's range). Size and brightness = loudness.
  - They drift outward along the family's flow path with slow curl noise. Long notes trail, short notes pop. Everything swells 8 % on the beat and 15 % on downbeats.
  - They fade and shrink after 4 s or past 3 m. Hard cap of 1,500 live, oldest culled first. Font: **Bravura** (OFL-1.1, confirmed), rendered with MSDF.
- **What each change looks like:**

| Change | Visual | Sound |
|---|---|---|
| Summon | creature glides in, others ease back | whoosh from its position |
| Silence (held) | creature dims to 20 %; notes in flight freeze to glass; new notes are born as still glass; lock ring fills over 1.5 s | glassy chime; clink on lock |
| Return | **thaw**: glass cracks and shatters into sparkles, notes resume | warm bloom, crackle |
| Solo | others dim to 25 % | rising two-note chime |
| EQ | creature widens and sinks (bass) or stretches tall with tip sparkles (treble) | filter sweep |
| Pause / scrub | notes stop mid-air while plankton keeps drifting; scrubbing rewinds notes along their paths | tape-stop; scrub ticks |
| Trim | lane region turns hollow; **ghost notes** show that region's original notes as hollow outlines | glass snip |
| Count-in | a ring around the replace instrument fills over one bar, with 4 soft pulses | soft ticks |
| Your hit | an amber glyph flies from the fingertip into the matching ghost outline | the hit |
| Tracking weak | hand glow fades | none |

- **Glowing hands** (council Session 9): soft light that brightens near targets and pulses on the beat, fading when tracking is weak. At most 5 extra draw calls.
- **Colour-blind palette** (council Session 9): a toggle swaps to the palette above. Families are told apart by shape, never by colour alone.
- **Sound identity:** every action has a spatial sound from its source. Effects are code-synthesised or CC0, each with an `ASSETS.md` row.
- **Signature moments for stills and video:** the first fist freezing the violins to glass; the thaw; the Dvořák brass entry with a full field of notes; amber notes filling ghost outlines.
- **References** sir chose on 7 Nov: the purple-teal palette, nebula clouds, glowing creature forms and dark empty space, from the ArtStation "bioluminescent" and "nebula environment" boards. Skip anything tagged Generative AI.

## 9. Interaction ideas borrowed from stem splitters and DAWs (no names or looks)

| Pattern | Stemlight hand action |
|---|---|
| Mute | fist on the creature (hold; a long hold locks) |
| Solo | double-pinch |
| 3-band EQ | two-hand stretch: wide = bass, tall = treble; squeeze together = flat |
| Transport | pinch the ribbon playhead: hold = pause, drag = scrub |
| Region cut | two-hand pinch on a ribbon lane |
| Undo region | pinch the hollow region and pull it away |
| Punch-in recording | count-in ring, then play pads / harp / keys, which loop over the cut |
| Reference track | guide track quietly under your first loop |
| Stem isolation | look to summon brings one part close |

Rejected: A–B loop (it would share trim's gesture), conducting gestures of any kind.

## 10. Risks and fallbacks

| Risk | Fallback |
|---|---|
| Trepak arrangement sounds poor | Tue 10 18:00 gate; drop it and move the pads to Dvořák's timpani |
| Rendered samples sound synthetic | Reverb, humanising, simple well-voiced parts |
| **No headset** (confirmed 7 Nov): hand feel, comfort, jitter and frame rate unproven | Big targets, hysteresis, gap tolerance. Try the 13 Nov Playground and the forum test swap. The write-up and video say plainly what's unverified |
| IWER can't script a fist through MCP | `DevHandPose` dev component (task 4) |
| Decoded audio too big for Quest Browser | Mono stems, 2:30 excerpt, buffers released, memory logged per piece |
| Fist / pinch confusion | Curl thresholds that can't overlap, plus a 20× cross-trigger suite |
| Quest Browser performance | Instancing, note cap, baked sky, no post-processing |
| A is overloaded (≈14 task-days against ≈12 for B before the freeze, estimate) | **Checkpoint Wed 11 18:00 IST:** if A is more than a day behind, take cuts 1–2 then |
| Start membership not confirmed (7 Nov) | Representative checks on Sun 8; support case after about 24 h (F41, done by Wed 11) |
| Crowded category and prior art | Lead with reaching in and remaking, plus real notes |
| Reads as a game | No score and no win state |
| Judges see it as "Maestro again" | Never add conducting gestures |
| CC BY-SA attribution missed | Credits, video description and Devpost text all carry it (task 53, 67) |

## 11. Any-song mode: roadmap (after the competition)

Researched 7 Nov (sources in the planning session; estimates labelled).

- **Separation:** Demucs v4 (htdemucs, 4 stems, SDR about 9.0 dB) is the practical choice. The code is MIT, but **the weight licence is unclear** (reportedly research-only), and the repo has been archived since Jan 2025. The 6-stem model adds piano and guitar, but its piano is weak. No public model separates orchestral instruments.
- **Where it runs:** a WebGPU ONNX build of htdemucs (126 MB) runs at about 8–22× real time on a desktop GPU. WebGPU in Quest Browser is still marked experimental, and WebXR + WebGPU was reported not working on Quest 3S in Jan 2026. So a laptop or desktop browser splits the song and the Quest plays it.
- **Notes:** Spotify's basic-pitch (Apache-2.0, `@spotify/basic-pitch`) works best on one instrument at a time, which is one stem at a time. Avoid essentia.js (AGPL). Beat detection uses an MIT library.
- **Cost:** free on-device. A server fallback (Modal's free $30 a month, about $0.005–0.01 per song, estimate) isn't needed for the beta.
- **Legal (assessment, not legal advice):** processing on the user's own device, local storage only, no export or sharing, and an "I have the rights to this file" checkbox. Non-commercial while the weight licence is unclear.
- **Phases (estimates):** P1 spike (3 weeks) → P2 laptop-to-Quest hand-off (3 weeks) → P3 quality and UX (3 weeks) → P4 beta and legal (2 weeks).
- **Target launch date (sir confirmed 7 Nov): public beta on 15 Feb 2027.** Scope: 4 stems, split on the user's own laptop or desktop browser, played on Quest, non-commercial.

Also out of scope: exporting audio, multiplayer, passthrough or room use, controllers, live AI, accounts.

## 12. Agent design

None at runtime.

## 13. Who does what

| Who | Owns |
|---|---|
| **Account A, sir** | Pipeline, audio engine, all gesture recognition, trim/replace logic, saving, pause/resume engine, performance, dev tools, deploys (with approval), `ASSETS.md`, fresh-session scoring audits, Devpost text, RC runs, submission (with approval) |
| **Account B, banit** | Creatures, notes, sky, hand glow, ribbon visuals and colliders, ghost notes, thaw, landing page, sound effects, tutorial and ghost hands, sequencer, credits, pause/resume UI, colour-blind palette, FoV screenshots, testers, device chase, voiceover, **video (length and style are banit's call)** |

**Git:** see `COORDINATION.md`. Building accounts never edit each other's claimed folders. Stage explicit paths. Commit and push after each working feature.

## 14. Schedule (IST) and tasks

The 70 tasks (each half a day or less, with owner, blockers, acceptance and files) are in `.coord/tasks/biyon-1.md` … `biyon-70.md` in the coordination repo, and listed in `TASKS.md`.

| Day | A | B | Milestone |
|---|---|---|---|
| **Sun 8** | 1 clones + init, 2 scaffold, 3 contracts + mock (by 13:00), 4 DevHandPose, 5 pipeline 1, start 6 | 34 MSDF atlas, 35 landing page, then 36 world shell | B unblocked from hour one. Membership check |
| **Mon 9** | 6, 7 pipeline, 8 engine, 9 stem chain, 10 hand reader, start 19 Trepak | 37 notes life cycle, 38 glyph check, 39 creatures 1 | 9 Beethoven stems in sync |
| **Tue 10** | 19, 20 Trepak (stems by 14:00), 11 summon, 12 fist + lock, **21 listening gate 18:00** | 40 creatures 2, 44 sky, 50 glowing hands | Fist-to-silence. Glow kill rule at 23:59 |
| **Wed 11** | 13 solo, 15 EQ, 18 Dvořák, 22 if needed, 32 first deploy (approval), 64 audit, F41 done | 41 summon + mute visuals, 42 thaw, 45 ribbon, 51 palette | First link. **Load checkpoint 18:00** |
| **Thu 12** | 14 cross-trigger suite, 16 ribbon gesture, 17 loader + memory, 23 trim | 46 ghost notes, 54 ghost hands, 52 sfx 1, 43 shape-morph | Trim end to end |
| **Fri 13** | 24 pads, 25 scheduler + count-in + guide, 30 dev tools, 26 harp | 47 pads visual, 55 opening, 56 tutorial, 65 Playground 21:30 | Pads loop. Keyboard go/no-go |
| **Sat 14** | 28 saving, 29 pause/resume engine + reset, 64 audit, 67 text draft | 57 sequencer, 58 pause UI, 48 harp visual, 53 sfx 2 + credits, 63 FoV shots | **Feature freeze** |
| **Sun 15** | 31 performance pass, fixes | 59 capture, 66 testers, 68 voiceover, fixes | First-time testers |
| **Mon 16** | 33 release candidate, 69 RC run | 60 edit | **Release candidate** |
| **Tue 17** | fixes, 69 run 2, 64 audit, video upload (approval) | 61 master, fixes | Video public, checked logged out |
| **Wed 18** | Pin build; **with approval, submit by 18:00** | buffer | Submitted |

**Council add-ons (Session 9, 7 Nov):** glowing hands and the colour-blind palette are in. Kill rule: drop the glow if it isn't working in IWER by the end of 10 Nov, breaks the draw-call limit, or the first five minutes are unfinished on 13 Nov (keep the palette if it's done). Stretch only: "step inside an instrument", and only if the whole never-cut list is done by 13 Nov 18:00.

**Cut order:** glowing hands (50) → keyboard (27, 49) → thaw (42) → harp (26, 48) → third piece (19, 20; 22 becomes permanent) → EQ shape-morph (43) → ghost notes (46; amber notes then fly to the region instead). **Never cut:** first five minutes, frame-rate budget, sound, pause/resume, video.

## 15. Submission kit

All drafts. Results are filled in only after they're measured. Nothing is published without approval.

**Tagline:** The music you can reach into.

### Description draft
- *Stemlight is a seated, hands-only music visualiser. Look at any instrument and it comes to you; close your fist and it falls silent; stretch it to reshape its sound; cut its part and play your own.*
- Use the judging criteria's own words as headings where true.
- What it is and who it's for: Entertainment, music visualisation; the audience in section 1.
- Why only on Quest: the flat-screen test.
- How we built it: IWSDK, the offline score-to-stems pipeline, the fist-vs-pinch problem and its fix, look-to-summon from head direction (no eye tracking on Quest 3/3S), IWER testing with a dev hand-pose switch. Claude Code's role disclosed plainly.
- Attribution: Dvořák from Mutopia #1793, CC BY-SA 3.0. Beethoven from Mutopia #941, public domain. VSCO 2 CE and VCSL, CC0. Bravura, OFL.
- What's unverified: frame rate and hand feel on a real Quest (no headset).
- What's next: any song, **public beta 15 Feb 2027**.
- No brand names anywhere.

### Video (owner banit; length and hook style are his call)
- Follows `~/.claude/references/DEMO-VIDEO-METHODOLOGY.md`: capture → measure → Remotion → ffmpeg, chapter cards, the five transitions, callouts aimed at measured positions, and the 5.11 checklist.
- Fixed by the rules: Stemlight's dark palette instead of cream and coral; no "Powered by" chips naming a brand (IWSDK only, or none); emulator footage labelled; no AI video; under 3:00 (cap 2:50); every shot logged with its commit; second-visit footage for the return hook.
- Open for banit: about 2:00 or 2:30–2:45, and whether the hook is real fist-to-glass footage or text on black.

### Screenshots
At least 5, same colour treatment, real build.

### Judge instructions
Link → Enter → hands only, seated, about 8 minutes, no account.

## 16. Decisions made

**7 Nov, with sir (pivot):** replaces Strata · IWSDK · scores rendered per instrument · Beethoven → Dvořák → Trepak · hero action reach-in-silence · all four tools in (mute, EQ, trim/replace, transport) · pads > harp > keyboard · guided then free · purple-teal nebula/ocean, creatures, real notes · glowing hands + colour-blind palette (council Session 9) · saved on device · any-song as roadmap · emulator only · name Stemlight.

**7 Nov, planning session:** code and coordination in `banitsriram/git-coord` under `stemlight/`, banit asked to make it private (push anyway on Sun 8 if not) · look to summon · fist hold with a 1.5 s lock · ghost notes and thaw in · Dvořák from Mutopia #1793 (CC BY-SA) · own Trepak with a Tue 10 gate, pads to Dvořák if it fails · Dvořák excerpt about 2:30, mono stems · count-in and simplified guide track in, A–B loop out · git-coord hooks installed (`python`, not `python3`) · team is sir and banit only · emulator only, no headset · any-song beta 15 Feb 2027 · video is banit's call.

## 17. Still open

| Item | Who decides |
|---|---|
| Video length and hook style | banit |
| Repo made private | banit |
| Start membership and Developer Access confirmed (F41, by Wed 11) | the Representative |
| First deploy, video upload, submission | sir, each in chat |
| A real-device run (none expected; 13 Nov Playground) | banit (task 65) |
