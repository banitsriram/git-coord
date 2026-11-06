#!/usr/bin/env python3
"""git-coord: coordinate several Claude agents working in one git repo.

Commands (run inside a clone):
  coord.py init <name>    name this clone's agent, create .coord/<name>.md, install the pre-commit guard, publish
  coord.py status         who is doing what, claim conflicts, messages for you, ready tasks, others' commits
  coord.py publish [msg]  commit your .coord file and .coord/tasks/, rebase, push (retries)

Hooks:
  coord.py edit-hook      Claude PreToolUse: block edits outside your published claims or inside someone else's
  coord.py session-hook   Claude SessionStart: print status
  coord.py prompt-hook    Claude UserPromptSubmit: print messages for you that you haven't seen yet
  coord.py tool-hook      Claude PostToolUse: same, mid-turn, after any tool call (fetches in the background)
  coord.py pre-commit     git pre-commit: the edit rule, for every staged file (catches shell edits too)

Everything is read from the upstream branch, i.e. what everyone has pushed.
Outside repos that use git-coord, every hook does nothing.
"""
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import time

FETCH_EVERY = 30        # seconds between fetches
STALE_AFTER = 2 * 3600  # not idle and no pushes for this long = stale
SELF = os.path.realpath(__file__)
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,30}$")
TEMPLATE = """# {name}
status: idle          # working | blocked | paused | idle
task:
claims:
done:
messages:
"""


def git(cwd, *args):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def parse(text):
    """`key: value` scalars, and `key:` followed by `- item` lines as lists."""
    d, key = {}, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("- "):
            if key:
                d[key].append(s[2:].strip())
        elif ":" in s and not s.startswith("#"):
            k, v = s.split(":", 1)
            k, v = k.strip().lower(), v.split(" #")[0].strip()
            if v:
                d[k], key = v, None
            else:
                d[k], key = [], k
        elif s and not s.startswith("#"):
            key = None
    return d


def val(d, k):
    v = d.get(k, "")
    return v if isinstance(v, str) else ""


def items(d, k):
    v = d.get(k, [])
    if isinstance(v, str):
        return [v] if v else []
    return v


def claims(d):
    out = (c.split(" #")[0].strip().rstrip("/") for c in items(d, "claims"))
    return [c for c in out if c]


def task_id(d):
    t = val(d, "task")
    return re.split(r"[\s:]", t, 1)[0] if t else ""


def blockers(d):
    return [b for b in re.split(r"[,\s]+", " ".join(items(d, "blocked_by"))) if b]


def covers(claim, rel):
    if any(ch in claim for ch in "*?["):
        return fnmatch.fnmatchcase(rel, claim)
    return rel == claim or rel.startswith(claim + "/")


def ago(sec):
    for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
        if sec >= n:
            return f"{int(sec // n)}{unit} ago"
    return "just now"


class Coord:
    def __init__(self, cwd):
        self.root = self.me = self.up = None
        self.agents = {}
        root = git(cwd, "rev-parse", "--show-toplevel") if cwd and os.path.isdir(cwd) else None
        if not root:
            return
        self.root = os.path.realpath(root)
        self.me = os.environ.get("COORD_AGENT") or self.g("config", "coord.agent")
        self.up = self.g("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")

    def g(self, *args):
        return git(self.root, *args)

    def ok(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True).returncode == 0

    def gitpath(self, name):
        return os.path.join(self.root or "", self.g("rev-parse", "--git-path", name) or os.path.join(".git", name))

    def load(self, force=False, background=False):
        """Fetch (throttled) and read everyone's file. True if this repo uses git-coord.

        background=True starts the fetch without waiting and reads what's already fetched,
        so the result shows up on the next call instead of slowing this one down."""
        if not (self.root and self.up):
            return False
        # ponytail: throttled fetch, so the hooks may see claims up to FETCH_EVERY seconds old
        stamp = self.gitpath("coord-fetched")
        if force or not os.path.exists(stamp) or time.time() - os.path.getmtime(stamp) > FETCH_EVERY:
            open(stamp, "w").close()
            if background:
                subprocess.Popen(["git", "fetch", "-q"], cwd=self.root, start_new_session=True,
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(["git", "fetch", "-q"], cwd=self.root, capture_output=True)
        for f in (self.g("ls-tree", "--name-only", self.up, ".coord/") or "").splitlines():
            if f.endswith(".md"):
                self.agents[f[len(".coord/"):-3]] = parse(self.g("show", f"{self.up}:{f}") or "")
        return bool(self.agents)

    def tasks(self):
        out = {}
        for f in (self.g("ls-tree", "--name-only", self.up, ".coord/tasks/") or "").splitlines():
            if f.endswith(".md"):
                text = self.g("show", f"{self.up}:{f}") or ""
                head = text.splitlines()[0] if text else ""
                out[os.path.basename(f)[:-3]] = (head.lstrip("# ").split(":", 1)[-1].strip(), parse(text))
        return out

    def since(self, name, test):
        """Oldest commit of the unbroken recent run in which test(name's file) holds."""
        path, start = f".coord/{name}.md", None
        for h in (self.g("log", "--format=%H", "-n", "200", self.up, "--", path) or "").splitlines():
            if not test(parse(self.g("show", f"{h}:{path}") or "")):
                break
            start = h
        return start

    def winner(self, a, b, test):
        """Which of agents a, b made test() true first. Same answer whichever agent asks."""
        a, b = sorted((a, b))
        ca, cb = self.since(a, test), self.since(b, test)
        if not (ca and cb):
            return a if ca else b
        if self.ok("merge-base", "--is-ancestor", ca, cb):
            return a
        if self.ok("merge-base", "--is-ancestor", cb, ca):
            return b
        ta, tb = (int(self.g("log", "-1", "--format=%ct", c) or 0) for c in (ca, cb))
        return a if ta <= tb else b

    def last_active(self, name):
        ts = (self.g("log", "-1", "--format=%ct", self.up, "--", f".coord/{name}.md"),
              self.g("log", "-1", "--format=%ct", f"--grep=^{name}:", self.up))
        return max([int(t) for t in ts if t] or [0])

    def stale(self, name):
        return (val(self.agents.get(name, {}), "status") != "idle"
                and time.time() - self.last_active(name) > STALE_AFTER)

    def check(self, rel):
        """Why I may not edit rel, or None if I may."""
        if not self.me:
            return f"this repo uses git-coord but this clone has no agent name. Ask the user for one, then run: python3 {SELF} init <name>"
        if rel == f".coord/{self.me}.md" or rel.startswith(".coord/tasks/"):
            return None
        if rel.startswith(".coord/"):
            return f"{rel} isn't yours. Only edit .coord/{self.me}.md and .coord/tasks/."

        def has(d):
            return any(covers(c, rel) for c in claims(d))

        mine = has(self.agents.get(self.me, {}))
        for name, d in sorted(self.agents.items()):
            if name == self.me or not has(d):
                continue
            if mine and self.winner(self.me, name, has) == self.me:
                continue
            note = " They look stale (no pushes for 2h+): ask the user before taking it over." if self.stale(name) else ""
            if mine:
                return f"{rel}: you and {name} both claim it and {name} claimed first. Remove it from your claims and publish.{note}"
            return f"{rel} is claimed by {name}. Don't edit it: pick another task, or message @{name} asking them to release it.{note}"
        if not mine:
            return f"{rel} isn't in your published claims. Add it to claims in .coord/{self.me}.md, publish, then retry."
        return None

    def messages(self):
        """[(sender, text)] for messages from others addressed to @me or @all."""
        tag = re.compile(r"(?<![\w-])@(%s|all)(?![\w-])" % re.escape(self.me or "all"))
        return [(n, m) for n, d in sorted(self.agents.items()) if n != self.me
                for m in items(d, "messages") if tag.search(m)]

    def unseen(self):
        """Messages for me not shown before; remembers what was shown."""
        path = self.gitpath("coord-seen")
        try:
            with open(path) as f:
                seen = set(f.read().split())
        except OSError:
            seen = set()
        msgs = self.messages()
        keys = [hashlib.sha1(f"{n}\0{m}".encode()).hexdigest()[:16] for n, m in msgs]
        with open(path, "w") as f:
            f.write("\n".join(keys))
        return [msg for msg, k in zip(msgs, keys) if k not in seen]


def status_text(c):
    now, agents = time.time(), c.agents
    out = [f"git-coord: you are {c.me or '(no name yet: run init)'}, shared branch {c.up}"]
    behind = c.g("rev-list", "--count", f"HEAD..{c.up}")
    ahead = c.g("rev-list", "--count", f"{c.up}..HEAD")
    if behind not in (None, "0"):
        out.append(f"  {behind} new upstream commit(s): git pull --rebase --autostash")
    if ahead not in (None, "0"):
        out.append(f"  {ahead} local commit(s) not pushed")

    out.append("Agents:")
    for n, d in sorted(agents.items()):
        st, age = val(d, "status") or "?", now - c.last_active(n)
        flag = "  STALE" if st != "idle" and age > STALE_AFTER else ""
        you = " (you)" if n == c.me else ""
        out.append(f"  {n}{you}: {st} | {val(d, 'task') or 'no task'} | last push {ago(age)}{flag}")
        if claims(d):
            out.append("    claims: " + ", ".join(claims(d)))

    mine = claims(agents.get(c.me, {}))
    for n, d in sorted(agents.items()):
        if n == c.me:
            continue
        for x in mine:
            for y in claims(d):
                probe = y if covers(x, y) else x if covers(y, x) else None
                if probe is None:
                    continue
                w = c.winner(c.me, n, lambda dd, p=probe: any(covers(cc, p) for cc in claims(dd)))
                verdict = "you claimed first, carry on." if w == c.me else "they claimed first: remove yours and publish."
                out.append(f"CONFLICT: your claim {x} overlaps {n}'s {y}: {verdict}")

    tasks = c.tasks()
    if tasks:
        taken = {}
        for n, d in agents.items():
            if task_id(d) in tasks:
                taken.setdefault(task_id(d), []).append(n)
        done = {t for t, (_, d) in tasks.items() if val(d, "status") == "done"}
        for t, names in sorted(taken.items()):
            for n in names:
                if c.me in names and n != c.me and c.winner(c.me, n, lambda dd, t=t: task_id(dd) == t) != c.me:
                    out.append(f"CONFLICT: {n} took task {t} first. Pick another task and publish.")
        open_ = [t for t in sorted(tasks) if t not in done and t not in taken]
        ready = [t for t in open_ if all(b in done for b in blockers(tasks[t][1]))]
        out.append(f"Tasks: {len(ready)} ready, {len(taken)} in progress, {len(open_) - len(ready)} blocked, {len(done)} done")
        out += [f"  ready  {t}: {tasks[t][0]}" for t in ready[:10]]

    msgs = c.messages()
    c.unseen()
    if msgs:
        out.append("Messages for you:")
        out += [f"  from {n}: {m}" for n, m in msgs]

    log = (c.g("log", "-n", "40", "--format=%h %cr: %s", c.up) or "").splitlines()
    work = [l for l in log if not l.partition(": ")[2].startswith(("coord(", f"{c.me}:"))][:8]
    if work:
        out.append("Recent commits by others:")
        out += [f"  {l}" for l in work]
    return "\n".join(out)


def publish(c, msg):
    if not c.me:
        print("no agent name: run init <name> first")
        return 1
    paths = [f".coord/{c.me}.md"]
    if os.path.isdir(os.path.join(c.root, ".coord", "tasks")):
        paths.append(".coord/tasks")
    c.g("add", "-A", "--", *paths)
    if not c.ok("diff", "--cached", "--quiet", "--", *paths):
        r = subprocess.run(["git", "commit", "-q", "-m", f"coord({c.me}): {msg}", "--", *paths],
                           cwd=c.root, capture_output=True, text=True)
        if r.returncode:
            print(r.stderr or r.stdout)
            return 1
    for _ in range(3):
        r = subprocess.run(["git", "pull", "-q", "--rebase", "--autostash"], cwd=c.root, capture_output=True, text=True)
        if r.returncode:
            print(f"pull failed:\n{r.stderr}\nIf the conflict is in another agent's file: git rebase --abort, then message them.")
            return 1
        if c.ok("push", "-q"):
            print("published")
            return 0
    print("push kept getting rejected; run publish again")
    return 1


def init(name):
    if not NAME_RE.match(name or ""):
        print("usage: coord.py init <name>  (lowercase letters, digits and dashes)")
        return 1
    c = Coord(os.getcwd())
    if not c.root:
        print("not inside a git repo")
        return 1
    c.g("config", "coord.agent", name)
    c.me = name
    f = os.path.join(c.root, ".coord", f"{name}.md")
    if not os.path.exists(f):
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w") as fh:
            fh.write(TEMPLATE.format(name=name))
    hook, line = c.gitpath("hooks/pre-commit"), f'"{sys.executable}" "{SELF}" pre-commit || exit 1'
    if os.path.exists(hook):
        with open(hook) as fh:
            if SELF not in fh.read():
                print(f"A pre-commit hook already exists at {hook}. Add this line to it:\n  {line}")
    else:
        os.makedirs(os.path.dirname(hook), exist_ok=True)
        with open(hook, "w") as fh:
            fh.write(f"#!/bin/sh\n{line}\n")
        os.chmod(hook, 0o755)
    if not c.up:
        print("No upstream branch yet: push with `git push -u origin <branch>`, then run publish.")
        return 0
    return publish(c, "join")


def edit_hook(data):
    ti = data.get("tool_input", {})
    path = ti.get("file_path") or ti.get("notebook_path")
    if not path:
        return 0
    path = os.path.realpath(os.path.join(data.get("cwd") or os.getcwd(), path))
    d = os.path.dirname(path)
    while not os.path.isdir(d):
        d = os.path.dirname(d)
    c = Coord(d)
    if not c.load():
        return 0
    rel = os.path.relpath(path, c.root).replace(os.sep, "/")
    if c.ok("check-ignore", "-q", rel):
        return 0
    msg = c.check(rel)
    if msg:
        print(f"git-coord: {msg}", file=sys.stderr)
        return 2
    return 0


def pre_commit():
    c = Coord(os.getcwd())
    if not c.load():
        return 0
    staged = (c.g("diff", "--cached", "--name-only", "--no-renames") or "").splitlines()
    errs = [m for m in map(c.check, staged) if m]
    if errs:
        print("git-coord: commit blocked:\n  " + "\n  ".join(errs)
              + "\nOnly if the user says so: git commit --no-verify", file=sys.stderr)
        return 1
    return 0


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "status"
    data = {}
    if cmd.endswith("-hook"):
        try:
            data = json.load(sys.stdin)
        except ValueError:
            pass
    cwd = data.get("cwd") or os.getcwd()
    if cmd == "edit-hook":
        return edit_hook(data)
    if cmd == "pre-commit":
        return pre_commit()
    if cmd == "init":
        return init(argv[2] if len(argv) > 2 else "")
    c = Coord(cwd)
    if cmd == "session-hook":
        if c.load(force=True):
            print(status_text(c))
            print("This repo uses the git-coord skill: claim files before editing, publish after changing your .coord file.")
        return 0
    if cmd in ("prompt-hook", "tool-hook"):
        if c.load(background=cmd == "tool-hook") and c.me:
            new = c.unseen()
            if new:
                text = "git-coord: new messages for you:\n" + "\n".join(f"  from {n}: {m}" for n, m in new)
                if cmd == "prompt-hook":
                    print(text)
                else:
                    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": text}}))
        return 0
    if cmd == "status":
        if not c.load(force=True):
            print("Not a git-coord repo here (no upstream branch, or no .coord/ pushed to it).")
            return 1
        print(status_text(c))
        return 0
    if cmd == "publish":
        return publish(c, " ".join(argv[2:]) or "update")
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
