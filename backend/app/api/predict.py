from fastapi import APIRouter
import numpy as np
import pandas as pd
from app.models.schemas import LoanApplication, PredictionResult
from app.core.model_loader import get_model, get_scaler, FEATURE_COLS

router = APIRouter()


def build_features(application: LoanApplication) -> pd.DataFrame:
    data = {col: getattr(application, col) for col in FEATURE_COLS}
    return pd.DataFrame([data])


@router.post("/predict", response_model=PredictionResult)
def predict(application: LoanApplication):
    model = get_model()
    scaler = get_scaler()

    X = build_features(application)
    X_sc = scaler.transform(X)

    prob_default = model.predict_proba(X_sc)[0][1]
    decision = "Rejected" if prob_default >= 0.5 else "Approved"
    risk_score = round(prob_default * 100, 1)

    if prob_default < 0.3:
        confidence = "High"
    elif prob_default < 0.5:
        confidence = "Medium"
    else:
        confidence = "High" if prob_default > 0.7 else "Medium"

    importances = model.feature_importances_
    top_factors = sorted(
        [{"feature": f, "importance": round(float(imp), 4)}
         for f, imp in zip(FEATURE_COLS, importances)],
        key=lambda x: x["importance"], reverse=True
    )[:5]

    return PredictionResult(
        decision=decision,
        probability_default=round(float(prob_default), 4),
        risk_score=risk_score,
        confidence=confidence,
        top_factors=top_factors
    )
