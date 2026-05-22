import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import shap

SEED = 42
np.random.seed(SEED)

DATA_PATH = "data/loan_data.csv"
MODEL_PATH = "data/loan_model.joblib"
SCALER_PATH = "data/scaler.joblib"
EXPLAINER_PATH = "data/shap_explainer.joblib"

os.makedirs("data", exist_ok=True)


def generate_synthetic_data(n=3000):
    ages = np.random.randint(22, 65, n)
    incomes = np.random.lognormal(10.8, 0.5, n).astype(int)
    loan_amounts = np.random.randint(5000, 50000, n)
    credit_scores = np.clip(np.random.normal(680, 80, n).astype(int), 300, 850)
    employment_years = np.clip(np.random.exponential(4, n), 0, 30).astype(int)
    debt_to_income = np.clip(np.random.beta(2, 5, n) * 0.8, 0.01, 0.9)
    num_credit_lines = np.random.randint(1, 15, n)
    num_delinquencies = np.random.poisson(0.3, n)
    genders = np.random.choice(["Male", "Female"], n, p=[0.55, 0.45])
    ethnicities = np.random.choice(
        ["White", "Black", "Hispanic", "Asian", "Other"],
        n, p=[0.6, 0.13, 0.18, 0.06, 0.03]
    )
    zip_regions = np.random.choice(["Urban", "Suburban", "Rural"], n, p=[0.45, 0.40, 0.15])

    log_odds = (
        -3.5
        + 0.015 * (700 - credit_scores)
        + 0.000012 * (35000 - incomes)
        + 0.000008 * (loan_amounts - 15000)
        + 1.5 * debt_to_income
        - 0.05 * employment_years
        + 0.3 * num_delinquencies
        - 0.02 * num_credit_lines
    )
    log_odds += np.where(genders == "Female", 0.18, 0)
    log_odds += np.where(ethnicities == "Black", 0.22, 0)
    log_odds += np.where(ethnicities == "Hispanic", 0.15, 0)
    log_odds += np.where(zip_regions == "Rural", 0.12, 0)

    probs = 1 / (1 + np.exp(-log_odds))
    defaults = (np.random.random(n) < probs).astype(int)

    return pd.DataFrame({
        "age": ages,
        "annual_income": incomes,
        "loan_amount": loan_amounts,
        "credit_score": credit_scores,
        "employment_years": employment_years,
        "debt_to_income_ratio": debt_to_income.round(3),
        "num_credit_lines": num_credit_lines,
        "num_delinquencies": num_delinquencies,
        "gender": genders,
        "ethnicity": ethnicities,
        "zip_region": zip_regions,
        "default": defaults
    })


def train():
    print("Generating synthetic loan dataset...")
    df = generate_synthetic_data(3000)
    df.to_csv(DATA_PATH, index=False)
    print(f"Dataset saved: {DATA_PATH} | Shape: {df.shape}")
    print(f"Default rate: {df['default'].mean():.2%}")

    feature_cols = [
        "age", "annual_income", "loan_amount", "credit_score",
        "employment_years", "debt_to_income_ratio", "num_credit_lines",
        "num_delinquencies"
    ]

    X = df[feature_cols]
    y = df["default"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    print("Training Gradient Boosting model...")
    model = GradientBoostingClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.8, random_state=SEED
    )
    model.fit(X_train_sc, y_train)

    y_pred = model.predict(X_test_sc)
    y_prob = model.predict_proba(X_test_sc)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    print(f"AUC-ROC: {auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["Approved", "Rejected"]))

    print("Computing SHAP explainer...")
    explainer = shap.TreeExplainer(model)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(explainer, EXPLAINER_PATH)
    print("All artifacts saved. Training complete!")


if __name__ == "__main__":
    train()
