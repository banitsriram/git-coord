# biyon
status: idle          # working | blocked | paused | idle
task:
claims:
done:
messages:
- biyon-0 @banit: please switch banitsriram/git-coord to private. We're putting the competition project in this repo (under stemlight/), and while it's public anyone can read it. Reply here when done. If it's still public when building starts Sun 8, we'll push anyway.
- biyon-0 @banit: I pushed a 2-line fix to coord.py (3db8441). On Windows, python3 is the Store stub, so init's commit guard blocked every commit, and os.path.relpath gives backslashes, so every edit inside your own claims was blocked. test_coord.py passes on Windows now. Revert it if you'd rather fix it another way.
