import subprocess


def run_pylint(file_path):
    """
    Runs Pylint analysis on a Python file.
    """

    result = subprocess.run(
        [
            "pylint",
            file_path,
            "--output-format=text"
        ],
        capture_output=True,
        text=True
    )

    return result.stdout