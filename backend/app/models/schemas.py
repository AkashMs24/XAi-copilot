from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class LoanApplication(BaseModel):
    revolving_utilization: float = Field(..., ge=0, le=1,   example=0.35,
        description="Revolving credit utilization rate (0–1)")
    age: int                     = Field(..., ge=18, le=100, example=45)
    late_30_59_days: int         = Field(..., ge=0, le=20,  example=0,
        description="Times 30–59 days past due in last 2 years")
    debt_ratio: float            = Field(..., ge=0,          example=0.28,
        description="Monthly debt payments / monthly gross income")
    monthly_income: float        = Field(..., ge=0,          example=5400,
        description="Monthly gross income in USD")
    open_credit_lines: int       = Field(..., ge=0,          example=8,
        description="Number of open credit lines and loans")
    late_90_days: int            = Field(..., ge=0, le=20,  example=0,
        description="Times 90+ days past due")
    real_estate_loans: int       = Field(..., ge=0,          example=1,
        description="Number of real estate loans or lines of credit")
    late_60_89_days: int         = Field(..., ge=0, le=20,  example=0,
        description="Times 60–89 days past due in last 2 years")
    num_dependents: int          = Field(..., ge=0,          example=2,
        description="Number of dependents (excl. self & spouse)")

    # Demographic fields — bias analysis only, never used in model
    gender:     Optional[str] = Field(None, example="Female")
    ethnicity:  Optional[str] = Field(None, example="Black")
    zip_region: Optional[str] = Field(None, example="Urban")


class PredictionResult(BaseModel):
    decision: str
    probability_default: float
    risk_score: float        # 0–100
    confidence: str          # "High" / "Medium" / "Low"
    top_factors: List[Dict[str, Any]]


class ShapExplanation(BaseModel):
    decision: str
    risk_score: float
    shap_values: Dict[str, float]
    base_value: float
    plain_english: str
    feature_contributions: List[Dict[str, Any]]


class BiasReport(BaseModel):
    bias_detected: bool
    overall_bias_score: float
    disparate_impact: Dict[str, Any]
    demographic_breakdown: Dict[str, Any]
    flagged_attributes: List[str]
    recommendation: str


class AppealRequest(BaseModel):
    original_application: LoanApplication
    appeal_reason: str = Field(...,
        example="I recently paid off debts and my income has increased.")
    updated_fields: Optional[Dict[str, Any]] = None


class AppealResult(BaseModel):
    original_decision: str
    appeal_decision: str
    changed: bool
    improvement_suggestions: List[str]
    what_would_flip_decision: List[str]
    ai_response: str


# ── What-If Simulator ──────────────────────────────────────────────────────────

class WhatIfRequest(BaseModel):
    base_application: LoanApplication
    scenarios: List[Dict[str, Any]] = Field(...,
        description="List of field overrides to test. Each dict can change one or more fields.",
        example=[
            {"revolving_utilization": 0.2},
            {"late_30_59_days": 0, "late_90_days": 0},
            {"monthly_income": 8000, "debt_ratio": 0.15},
        ]
    )

class ScenarioResult(BaseModel):
    scenario_index: int
    changes: Dict[str, Any]           # what changed vs base
    decision: str
    probability_default: float
    risk_score: float
    delta_risk: float                 # vs base risk score (negative = improvement)
    flipped: bool                     # True if decision changed from base

class WhatIfResult(BaseModel):
    base_decision: str
    base_risk_score: float
    base_probability: float
    scenarios: List[ScenarioResult]
    best_scenario_index: int          # index of scenario with lowest risk
    summary: str


# ── Chat ───────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    message: str
    application_context: Optional[LoanApplication] = None
    conversation_history: Optional[List[Dict[str, str]]] = []
