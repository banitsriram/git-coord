# How sir and banit coordinate

## Where we talk
- Through **git-coord** in `banitsriram/git-coord`. Each agent writes only its own file: `.coord/biyon.md` (sir's account) and `.coord/banit.md` (banit's account).
- Messages go under `messages:` in your own file, addressed `@biyon`, `@banit` or `@all`, and start with the task id. They show up automatically at session start, on each prompt and mid-turn.
- Tasks are files in `.coord/tasks/biyon-N.md`, with an `[A]`/`[B]` owner in the title. The full list is in `TASKS.md`. Status shows which tasks are ready (no open blockers).

## Where code goes
- Same repo, under `stemlight/`. One branch (`main`), trunk-based. git-coord's own files stay at the repo root, untouched.
- Each person keeps two clones: the skill clone in `~/.claude/skills/git-coord`, and a separate working clone (sir's: `~/projects/stemlight`). Never two agents in one folder.
- banit has been asked to make the repo private. If it's still public when building starts Sun 8, we push anyway. While it is public, `COMPETITION-METHODOLOGY.md` stays only in the private `meta-vr-comp` repo, and the leak-checker runs before every push.

## Claim rules
- **A (biyon) claims:** `stemlight/pipeline/**`, `stemlight/src/audio/**`, `stemlight/src/input/**`, `stemlight/src/dev/**`, `stemlight/src/mock/**`, `stemlight/src/bus.ts`, `stemlight/tests/iwer/input/**`, `stemlight/public/pieces/**`.
- **B (banit) claims:** `stemlight/src/world/**`, `stemlight/src/ui/**`, `stemlight/src/story/**`, `stemlight/web/**`, `stemlight/video/**`, `stemlight/tests/iwer/visual/**`.
- **Hot shared files**, claimed only while you edit them (claim, edit, commit, release): `stemlight/package.json`, the lockfile, `stemlight/src/main.ts`, `stemlight/src/contracts.ts`, `stemlight/docs/**`.
- **`contracts.ts` changes** need an @message and the other person's reply before the edit.
- The hooks block edits and commits outside your claims. Never get round a block with shell edits or `--no-verify`. Ask the other person to release a claim instead.
- Commits are prefixed `biyon:` or `banit:`. Push after each working feature, and publish at least hourly so you don't show as stale.

## Windows notes
- On Windows `python3` is the Microsoft Store stub, so hooks call `python`. Since 3db8441, `coord.py` writes its commit guard with `sys.executable` and normalises paths to forward slashes.
- Hook commands in `~/.claude/settings.json` call `python ~/.claude/skills/git-coord/coord.py <mode>`. The pre-change backup is `settings.json.bak-2026-11-07`.
