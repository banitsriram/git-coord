# git-coord

A Claude Code skill that lets two or more Claude agents work on the same repo without stepping on each other. Git is the message bus: each agent keeps a status file in `.coord/<name>.md` with its task, claimed files and messages, and claims files before editing them. See [SKILL.md](SKILL.md).

## Install

On each Claude account, clone this repo into its skills folder:

```bash
git clone https://github.com/banitsriram/git-coord.git ~/.claude/skills/git-coord
```

Update later with `git -C ~/.claude/skills/git-coord pull`.

Or install it per project: copy `SKILL.md` to `<project>/.claude/skills/git-coord/SKILL.md` and commit it, so both accounts get it on pull.

## Use in a project

1. Give each agent its own clone of the project. Never run two agents in one folder.
2. Add this line to the project's CLAUDE.md:
   `This repo is shared with other Claude agents. Use the git-coord skill.`
3. On first run, each agent asks for its name and saves it with `git config coord.agent <name>`.
