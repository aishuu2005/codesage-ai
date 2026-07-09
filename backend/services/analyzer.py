import subprocess


def run_pylint(file_path):
    print("=" * 50)
    print("Running Pylint on:", file_path)
    print("=" * 50)

    result = subprocess.run(
        [
            "pylint",
            file_path,
            "--output-format=text"
        ],
        capture_output=True,
        text=True
    )

    print("Return Code:", result.returncode)
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)

    return result.stdout