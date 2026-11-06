# git-coord

A Claude Code skill that lets several Claude agents (separate accounts, machines or sessions) work on the same repo without stepping on each other. Git is the only infrastructure: no server, no database, no MCP.

- **Claims.** Each agent claims files, folders or globs before editing them. Hooks block edits and commits outside your claims or inside someone else's. If two agents claim the same path, whoever pushed first wins, decided from git history.
- **Status.** One command shows who is doing what, claim conflicts, ready tasks, messages for you and others' recent commits. It runs automatically at session start.
- **Task queue.** One file per task, with blockers, so agents pull the next ready task themselves.
- **Messages.** `@name` or `@all` messages, shown automatically on your next prompt.
- **Stale detection.** Based on push times, not timestamps the agent types in.

See [SKILL.md](SKILL.md) for the protocol the agents follow.

## Install (each Claude account)

```bash
git clone https://github.com/banitsriram/git-coord.git ~/.claude/skills/git-coord
```

Add the hooks to `~/.claude/settings.json`. Merge them into any `hooks` you already have:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [{ "type": "command", "command": "python3 ~/.claude/skills/git-coord/coord.py edit-hook" }]
      }
    ],
    "SessionStart": [
      { "hooks": [{ "type": "command", "command": "python3 ~/.claude/skills/git-coord/coord.py session-hook" }] }
    ],
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "python3 ~/.claude/skills/git-coord/coord.py prompt-hook" }] }
    ]
  }
}
```

The hooks do nothing in repos that don't use git-coord, so they're safe to install globally. They need `python3` (3.9+) and `git`.

Update with `git -C ~/.claude/skills/git-coord pull`.

## Set up a shared project

1. Give each agent its own clone. Never run two agents in one folder.
2. Add this line to the project's CLAUDE.md:
   `This repo is shared with other Claude agents. Use the git-coord skill.`
3. In each clone, run `python3 ~/.claude/skills/git-coord/coord.py init <name>`, or let the agent do it. This also installs a git pre-commit guard, which catches edits made through the shell and by humans.

## Limits

- **Up to ~30 seconds behind.** The edit hook fetches at most every 30 seconds, so a claim pushed in that window may not be seen until the next fetch. Commits are checked against the same data.
- **One shared branch.** It's designed for trunk-based work on one shared branch with roughly 2 to 8 agents. Past that, push contention on that branch and status length grow.
- **Path claims only.** Two agents can still break each other through an interface change in unclaimed code. That's what messages are for.

## Test

```bash
python3 test_coord.py
```
