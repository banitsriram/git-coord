#!/usr/bin/env python3
"""Runs check_claims.py against a throwaway remote with two agents. Run: python3 test_check_claims.py"""
import json
import os
import subprocess
import sys
import tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_claims.py")


def sh(cwd, *cmd):
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)


def hook(path):
    r = subprocess.run([sys.executable, HOOK], input=json.dumps({"tool_input": {"file_path": path}}),
                       capture_output=True, text=True)
    return r.returncode, r.stderr


def publish(clone, name, body):
    os.makedirs(os.path.join(clone, ".coord"), exist_ok=True)
    with open(os.path.join(clone, ".coord", f"{name}.md"), "w") as f:
        f.write(body)
    sh(clone, "git", "add", "-A")
    sh(clone, "git", "commit", "-qm", f"coord({name})")
    sh(clone, "git", "pull", "-q", "--rebase")
    sh(clone, "git", "push", "-q")


with tempfile.TemporaryDirectory() as t:
    t = os.path.realpath(t)
    remote, a, b, plain = (os.path.join(t, x) for x in ("remote.git", "a", "b", "plain"))
    sh(t, "git", "init", "-q", "--bare", "-b", "main", remote)
    sh(t, "git", "clone", "-q", remote, a)
    for k, v in {"user.name": "t", "user.email": "t@t", "coord.agent": "alpha"}.items():
        sh(a, "git", "config", k, v)
    with open(os.path.join(a, ".gitignore"), "w") as f:
        f.write("build/\n")
    sh(a, "git", "add", "-A")
    sh(a, "git", "commit", "-qm", "init")
    sh(a, "git", "push", "-q", "-u", "origin", "main")
    sh(t, "git", "clone", "-q", remote, b)
    for k, v in {"user.name": "t", "user.email": "t@t", "coord.agent": "beta"}.items():
        sh(b, "git", "config", k, v)

    assert hook(f"{b}/src/x.py")[0] == 0, "no .coord on upstream yet: allow"

    publish(a, "alpha", "# alpha\nstatus: working\nclaims:\n- src/auth/   # login work\n- README.md\nmessages:\n- hi\n")
    publish(b, "beta", "# beta\nstatus: working\nclaims:\n- src/ui/\n")

    assert hook(f"{a}/src/auth/login.py")[0] == 0, "own claimed folder"
    assert hook(f"{a}/src/auth/new/deep/file.py")[0] == 0, "new file in own claimed folder"
    assert hook(f"{a}/README.md")[0] == 0, "own claimed file"
    assert hook(f"{a}/.coord/alpha.md")[0] == 0, "own coord file"
    assert hook(f"{b}/build/out.js")[0] == 0, "gitignored file"
    assert hook(f"{b}/src/ui/button.tsx")[0] == 0, "beta's own claim"

    code, err = hook(f"{b}/src/auth/login.py")
    assert code == 2 and "claimed by alpha" in err, err
    code, err = hook(f"{b}/src/authz.py")
    assert code == 2 and "not in your published claims" in err, "prefix must not leak: " + err
    code, err = hook(f"{b}/.coord/alpha.md")
    assert code == 2 and "belongs to another agent" in err, err
    os.remove(os.path.join(a, ".git", "FETCH_HEAD"))  # alpha's last fetch predates beta's claim; force a refetch
    code, err = hook(f"{a}/src/ui/button.tsx")
    assert code == 2 and "claimed by beta" in err, err

    sh(t, "git", "init", "-q", plain)
    assert hook(f"{plain}/anything.py")[0] == 0, "repo without git-coord"
    assert hook("/tmp/not-a-repo/file.py")[0] == 0, "outside any repo"

print("ok")
