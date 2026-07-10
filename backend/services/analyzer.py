from services.pylint_service import run_pylint
from services.bandit_service import run_bandit


def analyze_file(file_path):
    """
    Runs all available analyzers on a Python file.
    """

    pylint_report = run_pylint(file_path)
    bandit_report = run_bandit(file_path)

    return {
        "pylint": pylint_report,
        "bandit": bandit_report
    }