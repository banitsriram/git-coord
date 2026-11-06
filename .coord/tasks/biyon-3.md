# biyon-3: [A] contracts.ts + bus + AppContext + mock (fake transport, key map firing every event, 30-note fixture, 9 synthetic 20 s mono stems)
status: open
blocked_by: biyon-2
owner: A (biyon)
size: M (0.5 day) | critical path
features: -
files: `src/contracts.ts`, `src/bus.ts`, `src/mock/`, `public/pieces/fixture/`

Acceptance: `tsc --noEmit` clean; bus unit test; mock time advances/pauses/seeks; fixture validates. **Pushed by 13:00 Sun 8**

Spec: stemlight/docs/PLAN.md (gestures s3, pipeline s4, contracts s6, visuals s8). Schedule and cut order: PLAN s14.
