"""Check each hard eval case against its reference result.

Run with: python3 tests/check_eval_references.py

`tests/eval-references/<case>/` holds the files that a proper answer to the case
adds or changes. For each case, this script copies the case's fixture into a
temporary directory and lays the reference result over it. Then it checks two
invariants.

1. Every `file_exists` grader and every `regex` grader that reads a file passes,
   so a proper answer can satisfy the graders.
2. The command in `run.sh` succeeds. The reference tests mark each planted bug as
   an expected failure that must fail, so the command fails when a fixture loses
   a bug or gains one.

The script does not check the graders that an LLM judges.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "plugins" / "testing-toolkit" / "evals"
FLAGS = {"i": re.I, "s": re.S, "m": re.M}


def failed_graders(case: str, work: Path) -> list[str]:
    """Return the names of the file and regex graders that fail in `work`."""
    failed = []
    for path in sorted((EVALS / case / "graders").glob("*.md")):
        _, front, body = path.read_text().split("---", 2)
        meta = dict(line.split(": ", 1) for line in front.strip().splitlines())
        if meta["type"] == "file_exists":
            ok = (work / meta["path"]).exists()
        elif meta["type"] == "regex" and "path:" in meta.get("target", ""):
            target = work / meta["target"].split("path:")[1].strip(" }")
            flags = sum(FLAGS[letter] for letter in meta.get("flags", ""))
            found = target.exists() and re.search(body.strip(), target.read_text(), flags)
            ok = bool(found) == (meta["match"] == "contains")
        else:
            continue
        if not ok:
            failed.append(path.name)
    return failed


def main() -> int:
    status = 0
    for reference in sorted((ROOT / "tests" / "eval-references").iterdir()):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            shutil.copytree(EVALS / reference.name / "fixture", work, dirs_exist_ok=True)
            shutil.copytree(reference, work, dirs_exist_ok=True)
            failed = failed_graders(reference.name, work)
            run = subprocess.run(["bash", "run.sh"], cwd=work, capture_output=True, text=True)
        if failed or run.returncode:
            status = 1
            print(f"FAIL - {reference.name}: graders {failed or 'pass'}, run.sh exit {run.returncode}")
            print(run.stdout[-1500:] + run.stderr[-500:])
        else:
            print(f"ok   - {reference.name}")
    return status


if __name__ == "__main__":
    sys.exit(main())
