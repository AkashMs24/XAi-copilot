import joblib
import os

_artifacts = {}

FEATURE_COLS = [
    "revolving_utilization",
    "age",
    "late_30_59_days",
    "debt_ratio",
    "monthly_income",
    "open_credit_lines",
    "late_90_days",
    "real_estate_loans",
    "late_60_89_days",
    "num_dependents",
]

FEATURE_DESCRIPTIONS = {
    "revolving_utilization": "Revolving lines utilization (0–1, e.g. 0.35 = 35%)",
    "age":                   "Applicant age in years",
    "late_30_59_days":       "Times 30–59 days past due (last 2 yrs)",
    "debt_ratio":            "Monthly debt payments ÷ monthly gross income",
    "monthly_income":        "Monthly gross income in USD",
    "open_credit_lines":     "Number of open credit lines & loans",
    "late_90_days":          "Number of times 90+ days past due",
    "real_estate_loans":     "Number of real estate loans or lines of credit",
    "late_60_89_days":       "Times 60–89 days past due (last 2 yrs)",
    "num_dependents":        "Number of dependents (excl. self & spouse)",
}

FEATURE_RANGES = {
    "revolving_utilization": {"min": 0.0,   "max": 1.0,    "step": 0.01, "type": "float"},
    "age":                   {"min": 18,    "max": 100,    "step": 1,    "type": "int"},
    "late_30_59_days":       {"min": 0,     "max": 20,     "step": 1,    "type": "int"},
    "debt_ratio":            {"min": 0.0,   "max": 5.0,    "step": 0.01, "type": "float"},
    "monthly_income":        {"min": 0,     "max": 50000,  "step": 100,  "type": "float"},
    "open_credit_lines":     {"min": 0,     "max": 60,     "step": 1,    "type": "int"},
    "late_90_days":          {"min": 0,     "max": 20,     "step": 1,    "type": "int"},
    "real_estate_loans":     {"min": 0,     "max": 20,     "step": 1,    "type": "int"},
    "late_60_89_days":       {"min": 0,     "max": 20,     "step": 1,    "type": "int"},
    "num_dependents":        {"min": 0,     "max": 20,     "step": 1,    "type": "int"},
}


def _data_dir() -> str:
    return os.path.join(os.path.dirname(__file__), "..", "..", "data")


def load_artifacts():
    base = _data_dir()
    files = {
        "model":    "loan_model.joblib",
        "scaler":   "scaler.joblib",
        "imputer":  "imputer.joblib",
        "explainer":"shap_explainer.joblib",
    }
    for key, filename in files.items():
        path = os.path.join(base, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing artifact: {path}\n"
                "Run 'python train_model.py' inside the backend/ directory first."
            )
        _artifacts[key] = joblib.load(path)
    print("✅ ML artifacts loaded successfully.")


def get_model():      return _artifacts["model"]
def get_scaler():     return _artifacts["scaler"]
def get_imputer():    return _artifacts["imputer"]
def get_explainer():  return _artifacts["explainer"]
def get_data_path():  return os.path.join(_data_dir(), "loan_data.csv")
