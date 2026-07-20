import subprocess
import sys


def run_bandit(file_path):
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "bandit",
                "-r",
                file_path
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        return result.stdout if result.stdout else result.stderr

    except subprocess.TimeoutExpired:
        return "ERROR: Bandit analysis timed out."

    except Exception as e:
        return f"ERROR: Unexpected error while running Bandit: {e}"