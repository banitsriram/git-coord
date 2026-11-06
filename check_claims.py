#!/usr/bin/env python3
"""git-coord PreToolUse hook: block edits that break the claim rules.

Blocks an Edit/Write when the file is claimed by another agent, is not in your
own published claims, or is another agent's .coord file. Claims are read from
the upstream branch (e.g. origin/main), i.e. what everyone has pushed.
Does nothing outside repos that use git-coord.
"""
import json
import os
import subprocess
import sys
import time

FETCH_EVERY = 30  # seconds between fetches of others' claims


def git(*args, cwd):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def parse_claims(text):
    out, inside = [], False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("claims:"):
            inside = True
        elif inside and s.startswith("- "):
            out.append(s[2:].split("#")[0].strip().rstrip("/"))
        elif inside:
            inside = False
    return [c for c in out if c]


def covers(claim, rel):
    return rel == claim or rel.startswith(claim + "/")


def block(msg):
    print(f"git-coord: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    tool_input = json.load(sys.stdin).get("tool_input", {})
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return
    path = os.path.realpath(path)
    d = os.path.dirname(path)
    while not os.path.isdir(d):
        d = os.path.dirname(d)
    root = git("rev-parse", "--show-toplevel", cwd=d)
    if not root:
        return
    root = os.path.realpath(root)
    me = git("config", "coord.agent", cwd=root)
    upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", cwd=root)
    if not me or not upstream:
        return
    rel = os.path.relpath(path, root)
    if rel == f".coord/{me}.md" or git("check-ignore", "-q", rel, cwd=root) is not None:
        return

    # ponytail: throttled fetch, others' claims can be up to FETCH_EVERY seconds stale
    fetch_head = os.path.join(git("rev-parse", "--absolute-git-dir", cwd=root), "FETCH_HEAD")
    if not os.path.exists(fetch_head) or time.time() - os.path.getmtime(fetch_head) > FETCH_EVERY:
        subprocess.run(["git", "fetch", "-q"], cwd=root, capture_output=True)

    files = git("ls-tree", "--name-only", upstream, ".coord/", cwd=root)
    if not files:
        return  # git-coord not in use on this branch yet

    if rel.startswith(".coord/"):
        block(f"{rel} belongs to another agent. Only edit your own .coord/{me}.md.")

    mine = []
    for f in files.splitlines():
        if not f.endswith(".md"):
            continue
        name = os.path.basename(f)[:-3]
        claims = parse_claims(git("show", f"{upstream}:{f}", cwd=root) or "")
        if name == me:
            mine = claims
            continue
        hit = next((c for c in claims if covers(c, rel)), None)
        if hit:
            block(f"{rel} is claimed by {name} ({hit}). Don't edit it: pick another task, "
                  f"or post @{name} in your .coord file asking them to release it. "
                  f"If you both claim it, whoever's claim commit is later in git log removes theirs.")

    if not any(covers(c, rel) for c in mine):
        block(f"{rel} is not in your published claims. Add it to claims in .coord/{me}.md, "
              f"publish (git-coord skill), then retry.")


if __name__ == "__main__":
    main()
