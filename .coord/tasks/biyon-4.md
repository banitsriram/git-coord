# biyon-4: [A] DevHandPose dev component + IWER input harness (two hands stepped alternately)
status: open
blocked_by: biyon-2
owner: A (biyon)
size: M (0.5 day) | critical path
features: F38
files: `src/dev/`, `tests/iwer/input/`

Acceptance: `ecs_set_component DevHandPose fist` → `get_hand_state` curl ≥0.75; partial curl works; absent from `dist/` (F38)

Spec: stemlight/docs/PLAN.md (gestures s3, pipeline s4, contracts s6, visuals s8). Schedule and cut order: PLAN s14.
