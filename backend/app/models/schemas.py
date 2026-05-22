from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class LoanApplication(BaseModel):
    age: int = Field(..., ge=18, le=80, example=32)
    annual_income: float = Field(..., ge=0, example=65000)
    loan_amount: float = Field(..., ge=1000, example=20000)
    credit_score: int = Field(..., ge=300, le=850, example=680)
    employment_years: float = Field(..., ge=0, example=5)
    debt_to_income_ratio: float = Field(..., ge=0, le=1, example=0.32)
    num_credit_lines: int = Field(..., ge=0, example=4)
    num_delinquencies: int = Field(..., ge=0, example=0)
    gender: Optional[str] = Field(None, example="Female")
    ethnicity: Optional[str] = Field(None, example="Black")
    zip_region: Optional[str] = Field(None, example="Urban")


class PredictionResult(BaseModel):
    decision: str
    probability_default: float
    risk_score: float
    confidence: str
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
    appeal_reason: str = Field(..., example="I recently paid off two loans and my income increased.")
    updated_fields: Optional[Dict[str, Any]] = None


class AppealResult(BaseModel):
    original_decision: str
    appeal_decision: str
    changed: bool
    improvement_suggestions: List[str]
    what_would_flip_decision: List[str]
    ai_response: str


class ChatMessage(BaseModel):
    message: str
    application_context: Optional[LoanApplication] = None
    conversation_history: Optional[List[Dict[str, str]]] = []
