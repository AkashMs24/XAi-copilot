# 🤖 XAI Copilot — Explainable AI for Loan Credit Risk

> **SHAP-powered loan decisions · Bias detection · Counterfactual appeals · LLM copilot in plain English**

[![Live App](https://img.shields.io/badge/Live%20App-Vercel-black?style=for-the-badge&logo=vercel)](https://xai-copilot.vercel.app)
[![API Docs](https://img.shields.io/badge/API%20Docs-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://xai-copilot-2.onrender.com/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

## 📌 Overview

XAI Copilot is a production-grade **Explainable AI system for loan credit risk assessment**. It goes beyond a black-box prediction — every decision is backed by SHAP feature attribution, bias fairness analysis, counterfactual reasoning, and a plain-English LLM copilot that explains outcomes to applicants and analysts alike.

Built as a full-stack deployment (React + FastAPI), this system addresses three real-world gaps in AI lending:
- **Opacity** — why was the loan rejected?
- **Fairness** — is the model discriminating by gender, ethnicity, or region?
- **Recourse** — what can the applicant change to get approved?

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Predict & Explain** | Submit a loan application → get an AI decision + SHAP waterfall chart showing each feature's impact |
| 🛡️ **Bias Detection** | Analyze model fairness across gender, ethnicity, and zip region using demographic parity metrics |
| 📋 **Decision Appeal** | Counterfactual analysis — shows the minimum changes needed to flip a rejection to approval |
| 💬 **AI Copilot Chat** | Ask anything in plain English about the decision, powered by LLaMA 3.3 70B via Groq |

---

## 🛠️ Tech Stack

### Frontend
- **React + Vite** — fast SPA build
- **Tailwind CSS** — utility-first styling
- **Recharts** — SHAP visualization charts
- **Deployed on Vercel**

### Backend
- **FastAPI (Python 3.11)** — REST API with async support
- **scikit-learn** — Gradient Boosting Classifier
- **SHAP (TreeExplainer)** — model explainability
- **Groq API (LLaMA 3.3 70B)** — LLM copilot
- **Deployed on Render**

---

## 🧠 ML Model

| Property | Detail |
|---|---|
| Algorithm | Gradient Boosting Classifier |
| Hyperparameters | 200 estimators, max depth 4 |
| Explainability | SHAP TreeExplainer (feature-level attribution) |
| Input Features | Age, Annual Income, Loan Amount, Credit Score, Employment Years, Debt-to-Income Ratio, Credit Lines, Delinquencies |
| Training Data | 10,000 synthetic loan applications with demographic bias patterns modeled on published lending discrimination research |

> **Why synthetic data?** Real loan datasets are proprietary and heavily regulated. Synthetic generation with controlled bias patterns allows rigorous fairness testing — a standard practice in responsible AI research (cf. IBM AIF360, Google What-If Tool).

---

## 📁 Project Structure

```
XAi-copilot/
├── frontend/
│   ├── src/
│   │   ├── pages/          # Dashboard, Predict, Bias, Appeal, Copilot
│   │   ├── components/     # Reusable UI components
│   │   └── services/       # Axios API calls
│   └── vercel.json         # SPA routing config
├── backend/
│   ├── app/
│   │   ├── api/            # Routes: predict, explain, bias, appeal, chat
│   │   ├── core/           # Model loader & config
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # groq_service (LLM)
│   ├── train_model.py      # Trains model & saves artifacts
│   └── requirements.txt
└── render.yaml
```

---

## 🚀 Run Locally

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python train_model.py        # generates ML artifacts
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Environment Variables

```bash
# frontend/.env
VITE_API_URL=http://localhost:8000/api/v1

# backend/.env
GROQ_API_KEY=gsk_...
```

---

## 🌐 Deployment

### Backend — Render

| Setting | Value |
|---|---|
| Runtime | Python 3.11.9 |
| Build Command | `pip install -r requirements.txt && python train_model.py` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Env: PYTHON_VERSION | `3.11.9` |
| Env: GROQ_API_KEY | `gsk_...` |

### Frontend — Vercel

| Setting | Value |
|---|---|
| Root Directory | `frontend` |
| Framework | Vite |
| Env: VITE_API_URL | `https://xai-copilot-2.onrender.com/api/v1` |

---

## 🎯 Why This Project Matters

Most credit risk ML models are black boxes — they give a score but no reasoning. Regulators (EU AI Act, US ECOA) increasingly require **explainability and fairness audits** for AI-driven financial decisions. XAI Copilot demonstrates:

- **Explainability** via SHAP — not just a score, but *why*
- **Fairness auditing** — detecting protected-attribute bias before deployment
- **Recourse mechanisms** — counterfactuals give applicants actionable feedback
- **Human-AI collaboration** — LLM copilot bridges the gap between model output and human understanding

---

## 👤 Author

**Akash M S** — Data Science & AI, Presidency University Bangalore  
[GitHub](https://github.com/AkashMs24) · [Portfolio](https://portfolioakashms.vercel.app)

---

*MIT License · Built for real-world responsible AI research and portfolio demonstration*
