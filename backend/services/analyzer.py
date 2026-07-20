from services.pylint_service import run_pylint
from services.bandit_service import run_bandit
from services.radon_service import run_radon
from services.report_parser import (
    extract_pylint_score,
    count_bandit_issues,
    compute_radon_grade,
)


def analyze_file(file_path):
    """
    Runs Pylint, Bandit and Radon on the uploaded file and builds a
    combined report with a dynamic summary.

    Each individual tool runner (run_pylint / run_bandit / run_radon)
    already guarantees it never raises - failures are reported back as
    "ERROR: ..." strings instead. This function additionally wraps each
    call so that even a completely unexpected failure in one tool can
    never prevent the other two from running or crash the /upload
    endpoint.
    """

    try:
        pylint_output = run_pylint(file_path)
    except Exception as exc:
        pylint_output = f"ERROR: Pylint analysis failed unexpectedly: {exc}"

    try:
        bandit_output = run_bandit(file_path)
    except Exception as exc:
        bandit_output = f"ERROR: Bandit analysis failed unexpectedly: {exc}"

    try:
        radon_output = run_radon(file_path)
    except Exception as exc:
        radon_output = f"ERROR: Radon analysis failed unexpectedly: {exc}"

    # ---------- Security issue count ----------
    if bandit_output.startswith("ERROR"):
        security_issues = "N/A"
    else:
        security_issues = count_bandit_issues(bandit_output)

    # ---------- Pylint quality score ----------
    if pylint_output.startswith("ERROR"):
        quality_score = "N/A"
    else:
        quality_score = extract_pylint_score(pylint_output)

    # ---------- Radon complexity grade ----------
    # compute_radon_grade() picks the WORST grade across every function
    #/class Radon reported, rather than naively matching whichever
    # letter happens to appear first in the raw text (the previous
    # implementation checked " A " before " B "/" C "/" D ", so it could
    # report a file as low-complexity even when it also contained a
    # high-complexity block, simply because an "A" grade occurred
    # somewhere earlier in the text).
    radon_summary = compute_radon_grade(radon_output)

    if radon_summary["grade"] == "N/A":
        complexity = radon_summary["label"]
    else:
        complexity = f"{radon_summary['grade']} - {radon_summary['label']}"

    return {
        "summary": {
            "quality_score": quality_score,
            "security_issues": security_issues,
            "complexity": complexity,
            "average_complexity": radon_summary["average_complexity"],
            "functions_analyzed": radon_summary["blocks_analyzed"],
        },
        "pylint": pylint_output,
        "bandit": bandit_output,
        "radon": radon_output,
    }