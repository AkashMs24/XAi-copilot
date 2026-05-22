from fastapi import APIRouter, HTTPException
import pandas as pd
from app.models.schemas import LoanApplication, WhatIfRequest, WhatIfResult, ScenarioResult
from app.core.model_loader import get_model, get_scaler, FEATURE_COLS

router = APIRouter()


def _predict_prob(app_dict: dict, model, scaler) -> float:
    X = pd.DataFrame([{col: app_dict[col] for col in FEATURE_COLS}])
    return float(model.predict_proba(scaler.transform(X))[0][1])


@router.post("/whatif", response_model=WhatIfResult)
def whatif(request: WhatIfRequest):
    model  = get_model()
    scaler = get_scaler()

    base   = request.base_application.model_dump()
    base_p = _predict_prob(base, model, scaler)
    base_r = round(base_p * 100, 1)
    base_d = "Rejected" if base_p >= 0.5 else "Approved"

    if not request.scenarios:
        raise HTTPException(status_code=400, detail="Provide at least one scenario.")

    results: list[ScenarioResult] = []

    for i, changes in enumerate(request.scenarios):
        # Validate field names
        invalid = [k for k in changes if k not in FEATURE_COLS]
        if invalid:
            raise HTTPException(
                status_code=422,
                detail=f"Scenario {i}: unknown fields {invalid}. Valid: {FEATURE_COLS}"
            )

        scenario_data = {**base, **changes}
        prob  = _predict_prob(scenario_data, model, scaler)
        risk  = round(prob * 100, 1)
        dec   = "Rejected" if prob >= 0.5 else "Approved"

        results.append(ScenarioResult(
            scenario_index=i,
            changes=changes,
            decision=dec,
            probability_default=round(prob, 4),
            risk_score=risk,
            delta_risk=round(risk - base_r, 1),
            flipped=dec != base_d,
        ))

    best_idx = min(range(len(results)), key=lambda i: results[i].risk_score)
    best     = results[best_idx]
    flipped  = [r for r in results if r.flipped]

    if flipped:
        summary = (
            f"{len(flipped)} of {len(results)} scenario(s) would flip the decision to Approved. "
            f"Best scenario reduces risk by {abs(best.delta_risk):.1f} points "
            f"(from {base_r} → {best.risk_score})."
        )
    else:
        summary = (
            f"No scenario flips the decision. "
            f"Best scenario reduces risk by {abs(best.delta_risk):.1f} points "
            f"(from {base_r} → {best.risk_score}). More significant changes are needed."
        )

    return WhatIfResult(
        base_decision=base_d,
        base_risk_score=base_r,
        base_probability=round(base_p, 4),
        scenarios=results,
        best_scenario_index=best_idx,
        summary=summary,
    )
