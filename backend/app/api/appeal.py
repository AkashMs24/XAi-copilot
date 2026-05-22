from fastapi import APIRouter
import numpy as np
import pandas as pd
from app.models.schemas import AppealRequest, AppealResult, LoanApplication
from app.core.model_loader import get_model, get_scaler, FEATURE_COLS
from app.services.groq_service import generate_appeal_response

router = APIRouter()


def get_prediction(application: LoanApplication, model, scaler) -> tuple:
    data = {col: getattr(application, col) for col in FEATURE_COLS}
    X = pd.DataFrame([data])
    X_sc = scaler.transform(X)
    prob = model.predict_proba(X_sc)[0][1]
    decision = "Rejected" if prob >= 0.5 else "Approved"
    return decision, prob


def find_counterfactuals(application: LoanApplication, model, scaler) -> list:
    suggestions = []
    base_data = {col: getattr(application, col) for col in FEATURE_COLS}
    X_base = pd.DataFrame([base_data])
    X_sc = scaler.transform(X_base)
    base_prob = model.predict_proba(X_sc)[0][1]

    if base_prob < 0.5:
        return []

    for delta in [20, 40, 60, 80]:
        new_score = min(850, application.credit_score + delta)
        test = {**base_data, "credit_score": new_score}
        prob = model.predict_proba(scaler.transform(pd.DataFrame([test])))[0][1]
        if prob < 0.5:
            suggestions.append({
                "field": "credit_score",
                "current": application.credit_score,
                "needed": new_score,
                "change": f"Increase credit score by {delta} points (to {new_score})",
                "impact": "would flip to Approved"
            })
            break

    for delta in [0.05, 0.10, 0.15]:
        new_dti = max(0.01, application.debt_to_income_ratio - delta)
        test = {**base_data, "debt_to_income_ratio": round(new_dti, 3)}
        prob = model.predict_proba(scaler.transform(pd.DataFrame([test])))[0][1]
        if prob < 0.5:
            suggestions.append({
                "field": "debt_to_income_ratio",
                "current": application.debt_to_income_ratio,
                "needed": round(new_dti, 3),
                "change": f"Reduce debt-to-income ratio by {delta:.0%} (to {new_dti:.2f})",
                "impact": "would flip to Approved"
            })
            break

    for pct in [0.1, 0.2, 0.3]:
        new_amount = application.loan_amount * (1 - pct)
        test = {**base_data, "loan_amount": new_amount}
        prob = model.predict_proba(scaler.transform(pd.DataFrame([test])))[0][1]
        if prob < 0.5:
            suggestions.append({
                "field": "loan_amount",
                "current": application.loan_amount,
                "needed": round(new_amount),
                "change": f"Reduce loan amount by {pct:.0%} (to ${new_amount:,.0f})",
                "impact": "would flip to Approved"
            })
            break

    if application.num_delinquencies > 0:
        test = {**base_data, "num_delinquencies": 0}
        prob = model.predict_proba(scaler.transform(pd.DataFrame([test])))[0][1]
        if prob < 0.5:
            suggestions.append({
                "field": "num_delinquencies",
                "current": application.num_delinquencies,
                "needed": 0,
                "change": "Clear all past delinquencies from credit record",
                "impact": "would flip to Approved"
            })

    return suggestions


@router.post("/appeal", response_model=AppealResult)
async def appeal_decision(request: AppealRequest):
    model = get_model()
    scaler = get_scaler()

    original_decision, original_prob = get_prediction(request.original_application, model, scaler)

    updated_app = request.original_application.model_copy()
    if request.updated_fields:
        for field, value in request.updated_fields.items():
            if hasattr(updated_app, field):
                setattr(updated_app, field, value)

    appeal_decision_str, appeal_prob = get_prediction(updated_app, model, scaler)
    changed = original_decision != appeal_decision_str

    counterfactuals = find_counterfactuals(request.original_application, model, scaler)
    what_would_flip = [cf["change"] for cf in counterfactuals]

    improvement_suggestions = [
        "Work on improving your credit score over 6–12 months by paying bills on time",
        "Reduce existing debt balances to lower your debt-to-income ratio",
        "Consider requesting a smaller loan amount",
        "Build employment history if currently below 2 years",
        "Dispute any errors on your credit report"
    ]

    ai_response = await generate_appeal_response(
        original_application=request.original_application,
        appeal_reason=request.appeal_reason,
        original_decision=original_decision,
        appeal_decision=appeal_decision_str,
        changed=changed,
        counterfactuals=counterfactuals
    )

    return AppealResult(
        original_decision=original_decision,
        appeal_decision=appeal_decision_str,
        changed=changed,
        improvement_suggestions=improvement_suggestions,
        what_would_flip_decision=what_would_flip,
        ai_response=ai_response
    )
