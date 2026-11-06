---
name: git-coord
description: Coordinate with other Claude agents working in the same git repo — see who is doing what, claim files before editing, take tasks from a shared queue, leave messages, and avoid overlapping commits. Use at session start, before starting any task, and before every commit or push in a repo that has a .coord/ directory, or whenever the user says another agent or Claude account is working on the same project.
---

# Git coordination between agents

Several agents share one repo and one branch. Git is the message bus. Each agent owns one file, `.coord/<name>.md`, and never edits anyone else's. Tasks live in `.coord/tasks/`. Everything is read from what has been **pushed**, so unpublished changes don't count.

All commands below use the script that sits next to this file:

```bash
python3 ~/.claude/skills/git-coord/coord.py <command>
```

If the skill is installed somewhere else, use that path instead. On Windows use `python` instead of `python3` (there `python3` is usually a Microsoft Store stub that fails), with the full path, e.g. `python C:/Users/<you>/.claude/skills/git-coord/coord.py <command>`.

## Setup (once per clone)

If `git config coord.agent` is empty, ask the user for a short name (`alpha`, `beta`, …) and run `coord.py init <name>`. That names the clone, creates your file, installs a git pre-commit guard and publishes. Every agent needs its own clone: never two agents in one folder.

## Status

`coord.py status` shows each agent's status, task, claims and last push, any claim conflicts, ready tasks, messages for you, and other agents' recent commits. It runs automatically at session start if the hooks are installed. Run it yourself before picking a task, before every push, and after finishing a task. Act on messages for you before continuing. If it says you're behind, run `git pull --rebase --autostash`.

## Your file

```markdown
# alpha
status: working        # working | blocked | paused | idle
task: alpha-3 Login form validation
claims:
- src/auth/
- src/components/LoginForm.tsx
- docs/*.md
done:
- alpha-2 Added /api/login route (a1b2c3d)
messages:
- alpha-3 @beta: renamed User.name -> User.displayName in src/types.ts, pull before using it
```

After any change to it, run `coord.py publish "<what changed>"`. This commits only your file and `.coord/tasks/`, rebases and pushes; your work in progress stays uncommitted.

## Claims

1. Run status. If a path you need is claimed by someone else, don't touch it. Pick other work, or message them asking them to release it.
2. Add your paths to `claims` (a file, a folder, or a glob like `src/**/*.test.ts`), set `task` and `status: working`, then publish.
3. If two agents claim the same path, whoever published first keeps it. Status prints `CONFLICT` and says who won. If it was them, remove yours and publish.

Claim the narrowest set of paths that covers the task. Hot shared files (package.json, lockfiles, route tables, shared type indexes) are claimed only for the moment you edit them: claim, edit, commit, release.

Need to edit a file you didn't plan on? Claim it first.

With the hooks installed this is enforced. Claude's edit tools and `git commit` are blocked for any file that is outside your published claims or claimed first by someone else. A block message tells you which rule you hit. Follow it. Never get around it with shell commands or `--no-verify` unless the user tells you to.

## Tasks

The shared queue is one file per task, `.coord/tasks/<id>.md`. Ids are `<your name>-<n>`, so two agents can never pick the same id.

```markdown
# alpha-4: Add logout button
status: open           # open | done
blocked_by: alpha-3
What to build, acceptance criteria, files it will likely touch.
```

- **Take a task:** pick one that status lists as `ready`, set `task: <id> <title>` and its claims, and publish. If status says someone took it first, pick another.
- **Add a task:** any time you find work outside your current task, write a task file instead of doing it now, then publish.
- **Finish a task:** set the task file to `status: done`, move the task to `done` with the commit hash, release its claims, and publish. Keep only the last ~5 `done` items.

If the repo has no tasks, take work from the user as usual. You still claim files.

## Commits

- Small, complete commits that build. Prefix every message with your name: `alpha: add login validation`. Status uses that prefix to show who did what.
- Push soon after each commit: `git pull --rebase --autostash && git push`.
- Rebase conflict in a file someone else claims: `git rebase --abort`, message them, tell the user. Conflict in your own claimed file: resolve it.
- Never force-push the shared branch, and never rewrite other agents' commits.

## Messages

- Write them in your own file under `messages`, addressed `@name`, or `@all` for everyone. Start a message with the task id it's about.
- Use them for interface changes others depend on, handoffs, requests to release a claim, and questions.
- Reply in your own file. Delete your own messages once the recipient has replied or acted on them.
- With the hooks installed, new messages for you appear automatically, both when the user sends a prompt and mid-turn after your tool calls. Read and act on them when they appear. Without the hooks you see them in status. Never loop waiting for a reply: work on something unblocked, or set `status: blocked` and tell the user.

## Stale agents

Status marks an agent `STALE` when it isn't idle and hasn't pushed in 2 hours. Its claims still hold. Tell the user and let them decide; never take over yourself. Publish at least hourly during long tasks, even just a progress note, so you don't look stale.

## Ending a session

Before you stop:
- push finished work;
- update `done`;
- release claims you won't come back to;
- set `status` to `idle`, or to `paused` with a short note about where you left off if you'll resume;
- answer messages for you;
- publish.

Never leave local commits unpushed.
