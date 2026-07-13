from services.pylint_service import run_pylint
from services.bandit_service import run_bandit
from services.report_parser import (
    extract_pylint_score,
    count_bandit_issues
)


def analyze_file(file_path):
    """
    Runs all analyzers and returns both
    raw reports and a summarized report.
    """

    pylint_report = run_pylint(file_path)
    bandit_report = run_bandit(file_path)

    summary = {
        "quality_score": extract_pylint_score(
            pylint_report
        ),
        "security_issues": count_bandit_issues(
            bandit_report
        )
    }

    return {
        "summary": summary,
        "pylint": pylint_report,
        "bandit": bandit_report
    }