from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_PATH = PROJECT_ROOT / "datasets"

GROUND_TRUTH_PATH = PROJECT_ROOT / "ground_truth"

RESULT_PATH = PROJECT_ROOT / "results"

REPORT_PATH = PROJECT_ROOT / "reports"


# Evaluation Thresholds


DECISION_PASS_SCORE = 1.0

MIN_CONFIDENCE = 0.90

MAX_HALLUCINATION = 0.05

MIN_TOOL_ACCURACY = 0.95

MIN_RAG_RECALL = 0.90

MIN_RAG_PRECISION = 0.85

MIN_GROUNDEDNESS = 0.95

# Reports

EXCEL_REPORT = REPORT_PATH / "evaluation_report.xlsx"

HTML_REPORT = REPORT_PATH / "dashboard.html"

DRIFT_REPORT = REPORT_PATH / "drift_report.xlsx"

# Logging

LOG_LEVEL = "INFO"

LOG_FILE = REPORT_PATH / "eval.log"

GROUND_TRUTH_FOLDER = PROJECT_ROOT / "ground_truth"

