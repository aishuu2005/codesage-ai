import re


def extract_pylint_score(report):
    """
    Extracts the overall Pylint score from the report.
    """

    match = re.search(
        r"rated at ([0-9.]+/10)",
        report
    )

    if match:
        return match.group(1)

    return "Not Available"


def count_bandit_issues(report):
    """
    Counts the number of Bandit issues.
    """

    return report.count(">> Issue:")