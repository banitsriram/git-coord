---
name: git-coord
description: Coordinate with another Claude agent working in the same git repo — see who is doing what, claim files before editing, leave messages, and avoid overlapping commits. Use at session start, before starting any task, and before every commit or push in a repo that has a .coord/ directory, or whenever the user says another agent or Claude account is working on the same project.
---

# Git coordination between agents

Several agents share one repo and one branch. Git is the message bus. Each agent owns exactly one file, `.coord/<name>.md`, and never edits anyone else's, so the coordination files themselves never conflict.

## Identity

Your name is `git config coord.agent`. If it's empty, ask the user for a short name (e.g. `alpha`, `beta`) and run `git config coord.agent <name>`. Every agent works in its own clone: never two agents in one folder.

## Sync

```bash
git pull --rebase --autostash -q; for f in .coord/*.md; do echo "=== $f"; cat "$f"; done; git log --oneline -15
```

Run it at session start, before claiming, before every push, and after finishing each task. Each time, read the other agents' files: their `claims`, their `status`, and any message addressed to `@<your name>`. Act on messages for you before continuing.

## Your status file

`.coord/<name>.md`. Keep it short:

```markdown
# alpha
updated: 2026-11-06 14:05 UTC
status: working          # working | blocked | idle
task: Login form validation
claims:
- src/auth/
- src/components/LoginForm.tsx
done:
- Added /api/login route (a1b2c3d)
messages:
- 14:05 @beta: renamed User.name -> User.displayName in src/types.ts, pull before using it
```

## Publish your file

After every change to your file:

```bash
n=$(git config coord.agent); git add ".coord/$n.md" && git commit -qm "coord($n): <what changed>" -- ".coord/$n.md" && git pull --rebase --autostash -q && git push -q
```

This commits only your coord file; your work in progress stays uncommitted. If the push is rejected, run the last two steps again.

## Claim before you edit

1. Sync.
2. If a path you need is in another agent's `claims` (the same file, or inside a claimed folder), don't touch it. Pick a different task, or post `@them` asking them to release it or make the change, and tell the user.
3. Otherwise add your paths to `claims`, set `task`, `status: working` and `updated`, then publish.
4. Sync again. If another agent claimed an overlapping path at the same moment, the claim whose commit comes later in `git log` loses: remove yours, publish, and pick something else.

Claim the narrowest set of paths that covers the task. Hot shared files (package.json, lockfiles, route tables, shared type indexes) are claimed only for the moment you edit them: claim, edit, commit, release.

Need to edit a file you didn't plan on? Claim it first, same steps.

If the `check_claims.py` hook is installed, it enforces this: an edit is blocked unless the file is in your *published* claims and in no one else's. A block message names the rule you hit. Follow it; don't try to get around it with shell commands.

## Commit and push work

- Small, complete commits that build. Prefix messages with your name: `alpha: add login validation`.
- Push soon after each commit; don't sit on local commits:
  ```bash
  git pull --rebase --autostash && git push
  ```
- Rebase conflict in a file another agent claims: `git rebase --abort`, message them, tell the user. Conflict in your own claimed file: resolve it.
- Never force-push the shared branch. Never rewrite another agent's commits.

## Finishing a task

Move it to `done` with the commit hash, remove its claims, set `status: idle` (or the next `task` and its claims), and publish. Keep only the last ~5 `done` items.

## Messages

- Write them in your own file under `messages`, addressed `@name`. Use them for interface changes others depend on, handoffs, requests to release a claim, and questions.
- Reply in your own file. Delete your own messages once the recipient has replied or acted on them.
- The other agent only sees a message at its next sync. Never loop waiting for a reply: keep working on something unblocked, or set `status: blocked` and tell the user.

## Stale claims

If another agent's `updated` is more than 2 hours old and its status isn't `idle`, its claims may be abandoned. Don't override them yourself: tell the user and let them decide.

## First use in a repo

If `.coord/` doesn't exist, create your file and publish it. Suggest the user add this line to the repo's CLAUDE.md so every agent loads this skill: `This repo is shared with other Claude agents. Use the git-coord skill.`
