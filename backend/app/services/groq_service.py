import os
from groq import AsyncGroq
from typing import List, Dict, Any, Optional

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are an Explainable AI Copilot for a loan credit risk assessment system.
Your role is to help business users — especially non-technical ones — understand AI decisions in plain English.

Guidelines:
- Explain AI decisions clearly without jargon
- Be empathetic when explaining rejections
- Always reference specific data points from the application
- Never make up data. Only reference what is provided.
- Keep responses concise (2–4 paragraphs max)
- When discussing bias, be factual and constructive
- You are NOT a financial advisor — clarify this when needed
"""


def _app_summary(application) -> str:
    return f"""Applicant Profile:
- Age: {application.age}
- Monthly Income: ${application.monthly_income:,.0f}
- Revolving Credit Utilization: {application.revolving_utilization:.0%}
- Debt Ratio: {application.debt_ratio:.2f}
- Open Credit Lines: {application.open_credit_lines}
- Real Estate Loans: {application.real_estate_loans}
- Times 30–59 Days Late: {application.late_30_59_days}
- Times 60–89 Days Late: {application.late_60_89_days}
- Times 90+ Days Late: {application.late_90_days}
- Dependents: {application.num_dependents}"""


async def generate_explanation(
    application,
    shap_contributions: List[Dict],
    decision: str,
    risk_score: float,
) -> str:
    top3 = shap_contributions[:3]
    factors_text = "\n".join([
        f"- {c['feature'].replace('_', ' ').title()}: value={c['value']}, "
        f"{'INCREASES' if c['shap_value'] > 0 else 'DECREASES'} risk by {abs(c['shap_value']):.3f}"
        for c in top3
    ])

    prompt = f"""A loan applicant has been {decision.upper()}.

{_app_summary(application)}

AI Risk Score: {risk_score}/100

Top factors driving this decision (SHAP analysis):
{factors_text}

Please explain this decision in plain English to the applicant.
Be empathetic, specific, and constructive.
If rejected, briefly mention 1–2 actionable improvements."""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.4,
        max_tokens=500,
    )
    return response.choices[0].message.content


async def generate_appeal_response(
    original_application,
    appeal_reason: str,
    original_decision: str,
    appeal_decision: str,
    changed: bool,
    counterfactuals: List[Dict],
) -> str:
    cf_text = (
        "\n".join([f"- {cf['change']}" for cf in counterfactuals[:3]])
        if counterfactuals
        else "- No simple single-factor change identified"
    )

    prompt = f"""A loan applicant is appealing their {original_decision.upper()} decision.

{_app_summary(original_application)}

Their appeal reason: "{appeal_reason}"

After reviewing the appeal, the updated decision is: {appeal_decision.upper()}
Decision changed: {'YES' if changed else 'NO'}

What would flip the decision (counterfactual analysis):
{cf_text}

Please write a professional, empathetic response that:
1. Acknowledges their appeal reason
2. Explains the outcome clearly
3. Provides the specific actions they can take to qualify in future
4. Is written for a non-technical audience"""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.4,
        max_tokens=600,
    )
    return response.choices[0].message.content


async def chat_with_copilot(
    user_message: str,
    application_context,
    conversation_history: List[Dict[str, str]],
) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if application_context:
        messages.append({
            "role":    "system",
            "content": f"Current application context:\n{_app_summary(application_context)}",
        })

    for turn in conversation_history[-6:]:
        messages.append(turn)

    messages.append({"role": "user", "content": user_message})

    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=600,
    )
    return response.choices[0].message.content
