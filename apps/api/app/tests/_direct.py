import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def bootstrap_project_root() -> None:
    project_root = str(PROJECT_ROOT)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def ensure_project_python(file_path: str, *, is_main: bool) -> None:
    if not is_main:
        return

    current_python = Path(sys.executable).absolute()
    candidates = [
        PROJECT_ROOT / "venv" / "bin" / "python",
        PROJECT_ROOT / ".venv" / "bin" / "python",
    ]

    for candidate in candidates:
        if not candidate.exists():
            continue
        absolute_candidate = candidate.absolute()
        if current_python == absolute_candidate:
            return
        os.execv(
            str(absolute_candidate),
            [str(absolute_candidate), str(Path(file_path).resolve()), *sys.argv[1:]],
        )


def run_current_test_file(file_path: str) -> int:
    resolved = Path(file_path).resolve()

    print(f"Running test file: {resolved.name}", flush=True)
    print(f"Resolved path: {resolved}", flush=True)
    print("Default pytest flags: -vv", flush=True)
    print("Tip: pass -s to see print() output from the test.", flush=True)
    if os.environ.get("KALPZERO_TEST_VERBOSE_HTTP") == "1":
        print("HTTP request/response logging: enabled", flush=True)
    else:
        print("HTTP request/response logging: disabled", flush=True)

    current_python = str(Path(sys.executable).absolute())
    args = [current_python, "-m", "pytest", str(resolved), "-vv", *sys.argv[1:]]
    os.execv(current_python, args)
    return 1
