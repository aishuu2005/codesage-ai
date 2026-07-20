import re

# Radon severity order, from best to worst.
_RADON_GRADE_ORDER = ["A", "B", "C", "D", "E", "F"]

_RADON_GRADE_LABELS = {
    "A": "Low complexity (simple, easy to maintain)",
    "B": "Low complexity (well structured and stable)",
    "C": "Moderate complexity",
    "D": "More than moderate complexity (slightly complex)",
    "E": "High complexity (complex, needs attention)",
    "F": "Very high complexity (unstable, error-prone)",
}

# Matches Radon's "cc -s" per-block lines, e.g.:
#   "    F 12:0 my_function - A (3)"
#   "    M 5:4 MyClass.method - C (14)"
_RADON_BLOCK_PATTERN = re.compile(r"-\s*([A-F])\s*\((\d+)\)")


def extract_pylint_score(report):
    """
    Extracts the overall Pylint score (e.g. "7.50/10") from a Pylint
    text report. Returns "Not Available" if no score line is found.
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
    Counts the number of Bandit issues found in a Bandit text report.
    """

    return report.count(">> Issue:")


def compute_radon_grade(report):
    """
    Parses Radon's `cc -s` text output and determines the worst
    (highest-risk) complexity grade found across all functions/classes
    in the file, along with the average cyclomatic complexity score.

    Returns a dict:
        {
            "grade": "A".."F" or "N/A",
            "label": str,
            "average_complexity": float or None,
            "blocks_analyzed": int,
        }
    """

    if not report or report.startswith("ERROR"):
        return {
            "grade": "N/A",
            "label": "Unable to determine (Radon did not run successfully)",
            "average_complexity": None,
            "blocks_analyzed": 0,
        }

    matches = _RADON_BLOCK_PATTERN.findall(report)

    if not matches:
        return {
            "grade": "N/A",
            "label": "No functions or classes found to analyze",
            "average_complexity": None,
            "blocks_analyzed": 0,
        }

    scores = [int(score) for _, score in matches]
    worst_letter = max(
        (letter for letter, _ in matches),
        key=_RADON_GRADE_ORDER.index,
    )

    return {
        "grade": worst_letter,
        "label": _RADON_GRADE_LABELS.get(worst_letter, "Unknown"),
        "average_complexity": round(sum(scores) / len(scores), 2),
        "blocks_analyzed": len(matches),
    }