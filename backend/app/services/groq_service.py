import os
from groq import AsyncGroq
from typing import List, Dict, Any

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama3-70b-8192"

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


async def generate_explanation(application, shap_contributions: List[Dict], decision: str, risk_score: float) -> str:
    top3 = shap_contributions[:3]
    factors_text = "\n".join([
        f"- {c['feature'].replace('_', ' ').title()}: value={c['value']}, "
        f"{'INCREASES' if c['shap_value'] > 0 else 'DECREASES'} risk by {abs(c['shap_value']):.3f}"
        for c in top3
    ])

    prompt = f"""A loan applicant has been {decision.upper()}.

Applicant Profile:
- Age: {application.age}
- Annual Income: ${application.annual_income:,.0f}
- Loan Amount: ${application.loan_amount:,.0f}
- Credit Score: {application.credit_score}
- Employment Years: {application.employment_years}
- Debt-to-Income Ratio: {application.debt_to_income_ratio:.2%}
- Past Delinquencies: {application.num_delinquencies}

AI Risk Score: {risk_score}/100

Top factors driving this decision (SHAP analysis):
{factors_text}

Please explain this decision in plain English to the applicant. Be empathetic, specific, and constructive.
If rejected, briefly mention 1–2 actionable things they could improve."""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=500
    )
    return response.choices[0].message.content


async def generate_appeal_response(original_application, appeal_reason: str, original_decision: str,
                                    appeal_decision: str, changed: bool, counterfactuals: List[Dict]) -> str:
    cf_text = "\n".join([f"- {cf['change']}" for cf in counterfactuals[:3]]) if counterfactuals else "- No simple single-factor changes identified"

    prompt = f"""A loan applicant is appealing their {original_decision.upper()} decision.

Their appeal reason: "{appeal_reason}"

After reviewing the appeal, the updated decision is: {appeal_decision.upper()}
Decision changed: {'YES' if changed else 'NO'}

What would flip the decision (counterfactual analysis):
{cf_text}

Please write a professional, empathetic response to this appeal that:
1. Acknowledges their appeal reason
2. Explains the outcome
3. Provides the specific actions they can take to qualify in the future
4. Is written for a non-technical business audience"""

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=600
    )
    return response.choices[0].message.content


async def chat_with_copilot(user_message: str, application_context, conversation_history: List[Dict[str, str]]) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if application_context:
        context_str = f"""Current application context:
- Age: {application_context.age}
- Income: ${application_context.annual_income:,.0f}
- Loan: ${application_context.loan_amount:,.0f}
- Credit Score: {application_context.credit_score}
- DTI: {application_context.debt_to_income_ratio:.2%}
- Employment: {application_context.employment_years} years
- Delinquencies: {application_context.num_delinquencies}
"""
        messages.append({"role": "system", "content": context_str})

    for turn in conversation_history[-6:]:
        messages.append(turn)

    messages.append({"role": "user", "content": user_message})

    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=600
    )
    return response.choices[0].message.content
