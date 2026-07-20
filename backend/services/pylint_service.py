import subprocess

PYLINT_TIMEOUT_SECONDS = 60


def run_pylint(file_path):
    """
    Runs Pylint analysis on a Python file and returns its raw text
    report.

    This function never raises. On any failure (Pylint missing,
    timeout, or an unexpected error) it returns a string prefixed with
    "ERROR:" so callers can detect and surface the failure without
    crashing.
    """

    try:
        result = subprocess.run(
            [
                "pylint",
                file_path,
                "--output-format=text",
            ],
            capture_output=True,
            text=True,
            timeout=PYLINT_TIMEOUT_SECONDS,
        )

        return result.stdout or result.stderr or "Pylint produced no output."

    except FileNotFoundError:
        return "ERROR: Pylint is not installed or not available on the system PATH."

    except subprocess.TimeoutExpired:
        return f"ERROR: Pylint analysis timed out after {PYLINT_TIMEOUT_SECONDS} seconds."

    except Exception as exc:
        return f"ERROR: Unexpected error while running Pylint: {exc}"