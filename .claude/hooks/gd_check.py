import json
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = ("gdformat", "gdlint")


def main() -> int:
    payload = json.load(sys.stdin)
    path = Path(payload.get("tool_input", {}).get("file_path", ""))
    if path.suffix != ".gd" or not path.exists():
        return 0

    problems = []
    for tool in TOOLS:
        exe = shutil.which(tool)
        if exe is None:
            continue
        result = subprocess.run([exe, str(path)], capture_output=True, text=True)
        if result.returncode != 0:
            problems.append(f"{tool} {path.name}:\n{result.stdout}{result.stderr}".strip())

    if problems:
        print("\n\n".join(problems), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())