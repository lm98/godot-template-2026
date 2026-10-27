import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
WATCHED = (".gd", ".tscn", ".tres")
RUNTIME_ERRORS = ("SCRIPT ERROR", "Failed to load")
SYNTAX_ERRORS = ("Parse Error",)
SMOKE_FRAMES = "120"
TAIL_LINES = 60


def run(cmd: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return result.returncode, result.stdout + result.stderr


def godot(binary: str, *args: str) -> tuple[int, str]:
    return run([binary, "--headless", "--path", str(ROOT), *args])


def changed_game_files() -> list[str]:
    _, out = run(["git", "status", "--porcelain", "--untracked-files=all"])
    paths = [line[3:].split(" -> ")[-1].strip('"') for line in out.splitlines()]
    return [p for p in paths if p.endswith(WATCHED) and (ROOT / p).exists()]


def contains(output: str, markers: tuple[str, ...]) -> bool:
    return any(marker in output for marker in markers)


def tail(text: str) -> str:
    return "\n".join(text.splitlines()[-TAIL_LINES:])


def fail(stage: str, output: str) -> int:
    print(f"Godot verification failed at {stage}. Fix before finishing:\n{tail(output)}", file=sys.stderr)
    return 2


def main() -> int:
    payload = json.load(sys.stdin)
    if payload.get("stop_hook_active"):
        return 0
    changed = changed_game_files()
    if not changed:
        return 0

    binary = os.environ.get("GODOT_BIN") or shutil.which("godot")
    if binary is None:
        return 0

    _, out = godot(binary, "--import")
    if contains(out, RUNTIME_ERRORS):
        return fail("headless import", out)

    for script in (p for p in changed if p.endswith(".gd")):
        _, out = godot(binary, "--check-only", "-s", f"res://{script}")
        if contains(out, SYNTAX_ERRORS):
            return fail(f"syntax check of {script}", out)

    _, out = godot(binary, "--quit-after", SMOKE_FRAMES)
    if contains(out, RUNTIME_ERRORS):
        return fail("smoke run of the main scene", out)

    if (ROOT / "addons" / "gut").is_dir():
        code, out = godot(
            binary, "-s", "addons/gut/gut_cmdln.gd", "-gdir=res://test", "-ginclude_subdirs", "-gexit"
        )
        if code != 0:
            return fail("GUT tests", out)

    return 0


if __name__ == "__main__":
    sys.exit(main())