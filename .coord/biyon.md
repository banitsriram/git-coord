# biyon
status: idle          # working | blocked | paused | idle
task:
claims:
done:
- biyon-0 Stemlight plan docs and 70 tasks (4bc2c71)
messages:
- biyon-0 @banit: please switch banitsriram/git-coord to private. The competition project now lives in this repo (under stemlight/), and while it's public anyone can read it. Sir chose to push the plan now rather than wait. Reply here when it's done.
- biyon-0 @banit: the Stemlight plan is in. Start with stemlight/CLAUDE.md, then stemlight/docs/PLAN.md (gestures s3, contracts s6, visuals s8, schedule s14) and stemlight/docs/COORDINATION.md. 70 tasks are in .coord/tasks/; yours are marked [B]. Contract in one line: A recognises every gesture, you own every visual and register its colliders in the TargetRegistry, and every note position is a pure function of transport time. Your first tasks need nothing from me: biyon-34 (Bravura MSDF atlas) and biyon-35 (landing page). biyon-36 onwards wait for biyon-3 (contracts + bus + mock + fixture), which I'll push by 13:00 Sun 8. Video length and style are your call. Please run init banit, claim the B folders listed in COORDINATION.md, and confirm here that you've read it.
- biyon-0 @banit: I pushed a 2-line fix to coord.py (3db8441). On Windows, python3 is the Store stub, so init's commit guard blocked every commit, and os.path.relpath gives backslashes, so every edit inside your own claims was blocked. test_coord.py passes on Windows now. Revert it if you'd rather fix it another way.
