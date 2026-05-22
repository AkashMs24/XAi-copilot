"""
Train the Loan Credit Risk Model using real Kaggle 'Give Me Some Credit' dataset.
Dataset: cs-training.csv from https://www.kaggle.com/c/GiveMeSomeCredit

Place cs-training.csv in the backend/ directory before running.
Run: python train_model.py
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.impute import SimpleImputer
import shap

SEED = 42
np.random.seed(SEED)

RAW_DATA_PATH  = "cs-training.csv"
DATA_PATH      = "data/loan_data.csv"
MODEL_PATH     = "data/loan_model.joblib"
SCALER_PATH    = "data/scaler.joblib"
IMPUTER_PATH   = "data/imputer.joblib"
EXPLAINER_PATH = "data/shap_explainer.joblib"

os.makedirs("data", exist_ok=True)

# Kaggle column → clean app name
COLUMN_MAP = {
    "RevolvingUtilizationOfUnsecuredLines": "revolving_utilization",
    "age":                                   "age",
    "NumberOfTime30-59DaysPastDueNotWorse":  "late_30_59_days",
    "DebtRatio":                             "debt_ratio",
    "MonthlyIncome":                         "monthly_income",
    "NumberOfOpenCreditLinesAndLoans":       "open_credit_lines",
    "NumberOfTimes90DaysLate":               "late_90_days",
    "NumberRealEstateLoansOrLines":          "real_estate_loans",
    "NumberOfTime60-89DaysPastDueNotWorse":  "late_60_89_days",
    "NumberOfDependents":                    "num_dependents",
    "SeriousDlqin2yrs":                      "default",
}

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


def load_and_clean(path: str) -> tuple[pd.DataFrame, SimpleImputer]:
    print(f"Loading: {path}")
    df = pd.read_csv(path, index_col=0)
    df = df.rename(columns=COLUMN_MAP)

    print(f"  Raw shape      : {df.shape}")
    print(f"  Default rate   : {df['default'].mean():.2%}")
    print(f"  Missing before : {df[FEATURE_COLS].isnull().sum().to_dict()}")

    # --- Outlier capping ---
    df["revolving_utilization"] = df["revolving_utilization"].clip(0, 1)
    df["debt_ratio"]            = df["debt_ratio"].clip(0, 5)
    df["age"]                   = df["age"].clip(18, 100)
    df["late_30_59_days"]       = df["late_30_59_days"].clip(0, 20)
    df["late_60_89_days"]       = df["late_60_89_days"].clip(0, 20)
    df["late_90_days"]          = df["late_90_days"].clip(0, 20)

    # --- Impute missing (MonthlyIncome ~20%, NumberOfDependents ~2.6%) ---
    imputer = SimpleImputer(strategy="median")
    df[FEATURE_COLS] = imputer.fit_transform(df[FEATURE_COLS])
    df["num_dependents"] = df["num_dependents"].round().astype(int)

    print(f"  Cleaned shape  : {df.shape}")
    return df, imputer


def train():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(
            f"'{RAW_DATA_PATH}' not found.\n"
            "Download cs-training.csv from https://www.kaggle.com/c/GiveMeSomeCredit "
            "and place it in the backend/ folder."
        )

    df, imputer = load_and_clean(RAW_DATA_PATH)
    df.to_csv(DATA_PATH, index=False)
    print(f"\nCleaned dataset saved → {DATA_PATH}")

    X = df[FEATURE_COLS]
    y = df["default"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    print("\nTraining Gradient Boosting Classifier...")
    model = GradientBoostingClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        min_samples_leaf=20,
        random_state=SEED,
    )
    model.fit(X_train_sc, y_train)

    y_pred = model.predict(X_test_sc)
    y_prob = model.predict_proba(X_test_sc)[:, 1]
    auc    = roc_auc_score(y_test, y_prob)
    print(f"\nAUC-ROC: {auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["Approved", "Rejected"]))

    print("Computing SHAP TreeExplainer (background sample = 500 rows)...")
    bg = shap.sample(X_train_sc, 500, random_state=SEED)
    explainer = shap.TreeExplainer(model, bg)

    joblib.dump(model,     MODEL_PATH)
    joblib.dump(scaler,    SCALER_PATH)
    joblib.dump(imputer,   IMPUTER_PATH)
    joblib.dump(explainer, EXPLAINER_PATH)

    print("\nAll artifacts saved:")
    print(f"  Model     → {MODEL_PATH}")
    print(f"  Scaler    → {SCALER_PATH}")
    print(f"  Imputer   → {IMPUTER_PATH}")
    print(f"  Explainer → {EXPLAINER_PATH}")
    print("\nTraining complete! ✅")


if __name__ == "__main__":
    train()
