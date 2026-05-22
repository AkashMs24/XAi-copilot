from fastapi import APIRouter, HTTPException
import numpy as np
import pandas as pd
from app.models.schemas import BiasReport
from app.core.model_loader import get_model, get_scaler, get_data_path, FEATURE_COLS

router = APIRouter()

DEMOGRAPHIC_COLS = ["gender", "ethnicity", "zip_region"]

SENSITIVE_GROUPS = {
    "gender":     ["Female"],
    "ethnicity":  ["Black", "Hispanic"],
    "zip_region": ["Rural"],
}


@router.get("/bias-report", response_model=BiasReport)
def bias_report():
    """
    Run bias analysis on the full training dataset.
    NOTE: The Kaggle cs-training.csv has no demographic columns.
    Bias report uses synthetic demographic labels attached to the dataset
    for demonstration purposes (not real applicant demographics).
    """
    import os

    data_path = get_data_path()
    if not os.path.exists(data_path):
        raise HTTPException(
            status_code=503,
            detail="Training data not found. Run train_model.py first."
        )

    df = pd.read_csv(data_path)
    model  = get_model()
    scaler = get_scaler()

    X_sc = scaler.transform(df[FEATURE_COLS])
    df["predicted_approval"] = (model.predict_proba(X_sc)[:, 1] < 0.5).astype(int)

    # Kaggle dataset has no demographic columns — attach synthetic ones for bias demo
    rng = np.random.default_rng(42)
    n   = len(df)

    if "gender" not in df.columns:
        df["gender"]     = rng.choice(["Male", "Female"],     n, p=[0.55, 0.45])
    if "ethnicity" not in df.columns:
        df["ethnicity"]  = rng.choice(["White", "Black", "Hispanic", "Asian", "Other"],
                                       n, p=[0.60, 0.13, 0.18, 0.06, 0.03])
    if "zip_region" not in df.columns:
        df["zip_region"] = rng.choice(["Urban", "Suburban", "Rural"], n, p=[0.45, 0.40, 0.15])

    demographic_breakdown: dict = {}
    flagged_attributes:    list = []
    disparate_impact:      dict = {}
    bias_scores:           list = []

    for col in DEMOGRAPHIC_COLS:
        group_rates = df.groupby(col)["predicted_approval"].mean().to_dict()
        demographic_breakdown[col] = {k: round(v, 4) for k, v in group_rates.items()}

        max_rate = max(group_rates.values()) if group_rates else 1.0
        col_di: dict = {}

        for group, rate in group_rates.items():
            di = rate / max_rate if max_rate > 0 else 1.0
            col_di[group] = round(di, 4)
            if group in SENSITIVE_GROUPS.get(col, []) and di < 0.8:
                flagged_attributes.append(f"{col}:{group} (DI={di:.2f})")
                bias_scores.append(1 - di)

        disparate_impact[col] = col_di

    overall = round(float(np.mean(bias_scores)) if bias_scores else 0.0, 4)
    detected = overall > 0.05

    recommendation = (
        f"Bias detected in {len(flagged_attributes)} demographic segment(s). "
        "Consider fairness-aware retraining, re-weighting, or removing proxy features."
        if detected else
        "No significant bias detected. Continue monitoring with incoming data."
    )

    return BiasReport(
        bias_detected=detected,
        overall_bias_score=overall,
        disparate_impact=disparate_impact,
        demographic_breakdown=demographic_breakdown,
        flagged_attributes=flagged_attributes,
        recommendation=recommendation,
    )
