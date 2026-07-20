import subprocess
import sys

RADON_TIMEOUT_SECONDS = 60


def run_radon(file_path):
    """
    Runs Radon cyclomatic complexity analysis on a Python file and
    returns its raw text report.

    This function never raises. On any failure (Radon missing, timeout,
    a non-zero exit code, or an unexpected error) it returns a string
    prefixed with "ERROR:" so callers can detect and surface the
    failure without crashing.
    """

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "radon",
                "cc",
                file_path,
                "-s",
            ],
            capture_output=True,
            text=True,
            timeout=RADON_TIMEOUT_SECONDS,
        )

    except FileNotFoundError:
        return "ERROR: Radon is not installed or not available on the system PATH."

    except subprocess.TimeoutExpired:
        return f"ERROR: Radon analysis timed out after {RADON_TIMEOUT_SECONDS} seconds."

    except Exception as exc:
        return f"ERROR: Unexpected error while running Radon: {exc}"

    if result.returncode != 0:
        return f"ERROR:\n{result.stderr.strip() or 'Radon exited with a non-zero status.'}"

    output = result.stdout.strip()

    if not output:
        return "No functions or classes found to analyze."

    return output