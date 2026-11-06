#!/usr/bin/env python3
"""End-to-end test: three agents on a throwaway remote. Run: python3 test_coord.py"""
import json
import os
import subprocess
import sys
import tempfile
import time

COORD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coord.py")
ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
           GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
ENV.pop("COORD_AGENT", None)


def sh(cwd, *cmd, env=None, check=True):
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True, env=env or ENV)


def cli(clone, *args):
    r = sh(clone, sys.executable, COORD, *args, check=False)
    return r.returncode, r.stdout + r.stderr


def fresh(clone):
    """Pretend the last fetch was long ago, so hooks see the latest pushes."""
    fh = os.path.join(clone, ".git", "FETCH_HEAD")
    if os.path.exists(fh):
        os.remove(fh)


def hook(mode, clone, **payload):
    fresh(clone)
    payload.setdefault("cwd", clone)
    r = subprocess.run([sys.executable, COORD, mode], input=json.dumps(payload),
                       capture_output=True, text=True, env=ENV)
    return r.returncode, r.stdout + r.stderr


def edit(clone, rel):
    return hook("edit-hook", clone, tool_input={"file_path": os.path.join(clone, rel)})


def write(clone, rel, text):
    p = os.path.join(clone, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)


def set_file(clone, name, status="working", task="", claims=(), messages=()):
    body = f"# {name}\nstatus: {status}\ntask: {task}\nclaims:\n"
    body += "".join(f"- {c}\n" for c in claims) + "done:\nmessages:\n" + "".join(f"- {m}\n" for m in messages)
    write(clone, f".coord/{name}.md", body)
    code, out = cli(clone, "publish", "test")
    assert code == 0, out


with tempfile.TemporaryDirectory() as t:
    t = os.path.realpath(t)
    remote, a, b = (os.path.join(t, x) for x in ("remote.git", "a", "b"))
    sh(t, "git", "init", "-q", "--bare", "-b", "main", remote)
    sh(t, "git", "clone", "-q", remote, a)
    write(a, ".gitignore", "build/\n")
    sh(a, "git", "add", "-A")
    sh(a, "git", "commit", "-qm", "init")
    sh(a, "git", "push", "-q", "-u", "origin", "main")
    sh(t, "git", "clone", "-q", remote, b)

    # Not a coord repo yet: everything is a no-op.
    assert edit(b, "src/x.py")[0] == 0
    assert hook("session-hook", b) == (0, "")
    assert edit(t, "nowhere/x.py")[0] == 0, "outside any repo"

    # init: names the clone, installs the guard, publishes the file.
    assert cli(a, "init", "Bad Name")[0] == 1
    code, out = cli(a, "init", "alpha")
    assert code == 0 and "published" in out, out
    code, out = cli(b, "init", "beta")
    assert code == 0, out
    assert os.access(os.path.join(b, ".git", "hooks", "pre-commit"), os.X_OK)

    # A clone of a coord repo with no name is blocked until it runs init.
    c = os.path.join(t, "c")
    sh(t, "git", "clone", "-q", remote, c)
    code, err = edit(c, "src/x.py")
    assert code == 2 and "no agent name" in err, err

    set_file(a, "alpha", task="login", claims=["src/auth/   # login work", "README.md"])
    set_file(b, "beta", task="ui", claims=["src/ui/", "docs/*.md"])

    # Edit hook: own claims, own coord file, tasks, ignored files pass.
    for rel in ("src/auth/login.py", "src/auth/new/deep.py", "README.md", ".coord/alpha.md",
                ".coord/tasks/alpha-1.md", "build/out.js"):
        assert edit(a, rel)[0] == 0, rel
    code, err = edit(a, "src/ui/button.tsx")
    assert code == 2 and "claimed by beta" in err, err
    code, err = edit(a, "docs/guide.md")
    assert code == 2 and "claimed by beta" in err, "glob claim: " + err
    code, err = edit(a, "src/authz.py")
    assert code == 2 and "isn't in your published claims" in err, "prefix must not leak: " + err
    code, err = edit(a, ".coord/beta.md")
    assert code == 2 and "isn't yours" in err, err

    # Tie: both claim src/shared/, alpha first. Alpha passes, beta is told to back off. No deadlock.
    set_file(a, "alpha", task="login", claims=["src/auth/", "src/shared/"])
    set_file(b, "beta", task="ui", claims=["src/ui/", "src/shared/util.py"])
    assert edit(a, "src/shared/util.py")[0] == 0
    code, err = edit(b, "src/shared/util.py")
    assert code == 2 and "alpha claimed first" in err, err
    fresh(b)
    out = cli(b, "status")[1]
    assert "CONFLICT" in out and "they claimed first" in out, out
    fresh(a)
    assert "you claimed first" in cli(a, "status")[1]

    # Pre-commit guard catches files edited through the shell.
    write(b, "src/auth/hack.py", "x")
    sh(b, "git", "add", "src/auth/hack.py")
    r = sh(b, "git", "commit", "-qm", "beta: sneaky", check=False)
    assert r.returncode != 0 and "claimed by alpha" in r.stderr, r.stderr
    sh(b, "git", "reset", "-q", "HEAD", "src/auth/hack.py")
    os.remove(os.path.join(b, "src/auth/hack.py"))
    write(b, "src/ui/button.tsx", "ok")
    sh(b, "git", "add", "src/ui/button.tsx")
    sh(b, "git", "commit", "-qm", "beta: add button")
    sh(b, "git", "push", "-q")

    # Messages: status shows them; prompt-hook shows each new one once.
    set_file(b, "beta", task="ui", claims=["src/ui/"],
             messages=["14:05 @alpha: renamed User.name to displayName", "@all: deploy freeze at 5", "@alphabet: not you"])
    code, out = hook("prompt-hook", a)
    assert "renamed User.name" in out and "deploy freeze" in out and "alphabet" not in out, out
    assert hook("prompt-hook", a)[1] == "", "already seen"
    fresh(a)
    out = cli(a, "status")[1]
    assert "Messages for you" in out and "renamed User.name" in out, out
    assert "beta: add button" in out, "others' work commits shown: " + out

    # Tasks: ready queue respects blockers and claims.
    write(a, ".coord/tasks/alpha-1.md", "# alpha-1: Add login API\nstatus: open\n")
    write(a, ".coord/tasks/alpha-2.md", "# alpha-2: Add logout button\nstatus: open\nblocked_by: alpha-1\n")
    assert cli(a, "publish", "tasks")[0] == 0
    fresh(b)
    out = cli(b, "status")[1]
    assert "ready  alpha-1: Add login API" in out and "ready  alpha-2" not in out and "1 blocked" in out, out
    set_file(b, "beta", task="alpha-1 Add login API", claims=["src/ui/"])
    set_file(a, "alpha", task="alpha-1", claims=["src/auth/"])
    fresh(a)
    out = cli(a, "status")[1]
    assert "beta took task alpha-1 first" in out and "1 in progress" in out, out
    write(b, ".coord/tasks/alpha-1.md", "# alpha-1: Add login API\nstatus: done\n")
    set_file(b, "beta", status="idle", claims=[])
    fresh(a)
    assert "ready  alpha-2: Add logout button" in cli(a, "status")[1]

    # Stale: an agent that is working but hasn't pushed for 3h is flagged.
    sh(a, "git", "pull", "-q", "--rebase")
    write(a, ".coord/gamma.md", "# gamma\nstatus: working\nclaims:\n- lib/\n")
    sh(a, "git", "add", ".coord/gamma.md")
    old = dict(ENV, GIT_COMMITTER_DATE=f"@{int(time.time()) - 3 * 3600} +0000")
    sh(a, "git", "commit", "-qm", "gamma joins", "--no-verify", env=old)
    sh(a, "git", "push", "-q")
    fresh(b)
    assert "STALE" in cli(b, "status")[1]
    code, err = edit(b, "lib/x.py")
    assert code == 2 and "stale" in err, err

    # Session hook prints status in a coord repo.
    code, out = hook("session-hook", b)
    assert code == 0 and "Agents:" in out and "you are beta" in out, out

print("ok")
