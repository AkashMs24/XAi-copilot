# XAI Copilot — Explainable AI for Credit Risk

An enterprise-grade Explainable AI system for loan credit risk assessment with bias detection, decision appeals, and an AI-powered copilot chat.

## 🚀 Live Demo

| Service | URL |
|---|---|
| **Frontend** | https://xai-copilot.vercel.app |
| **Backend API** | https://xai-copilot-2.onrender.com |
| **API Docs (Swagger)** | https://xai-copilot-2.onrender.com/docs |

## ✨ Features

- **Predict & Explain** — Submit a loan application and get an AI decision with SHAP-powered plain-English explanation
- **Bias Detection** — Analyze model fairness across gender, ethnicity, and zip region
- **Decision Appeal** — Appeal a rejected decision with counterfactual analysis
- **AI Copilot Chat** — Ask anything about loan decisions in plain English, powered by LLaMA 3.3 70B via Groq

## 🛠️ Tech Stack

### Frontend
- React + Vite
- Tailwind CSS
- Recharts (SHAP visualizations)
- Deployed on **Vercel**

### Backend
- FastAPI (Python 3.11)
- scikit-learn (Gradient Boosting Classifier)
- SHAP (Explainability)
- Groq API — LLaMA 3.3 70B Versatile
- Deployed on **Render**

## 📁 Project Structure

```
XAi-copilot/
├── frontend/          # React + Vite frontend
│   ├── src/
│   │   ├── pages/     # Dashboard, Predict, Bias, Appeal, Copilot
│   │   ├── components/
│   │   └── services/  # API calls
│   └── vercel.json    # SPA routing config
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/       # predict, explain, bias, appeal, chat
│   │   ├── core/      # model loader
│   │   ├── models/    # schemas
│   │   └── services/  # groq_service
│   ├── train_model.py # Generates ML artifacts
│   └── requirements.txt
└── render.yaml        # Render deployment config
```

## 🏃 Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python train_model.py       # Train model & generate artifacts
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
npm run dev
```

## 🌐 Deployment

### Backend (Render)
- **Runtime:** Python 3.11.9
- **Build Command:** `pip install -r requirements.txt && python train_model.py`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Env Vars:** `GROQ_API_KEY`, `PYTHON_VERSION=3.11.9`

### Frontend (Vercel)
- **Root Directory:** `frontend`
- **Framework:** Vite
- **Env Vars:** `VITE_API_URL=https://xai-copilot-2.onrender.com/api/v1`

## 📊 ML Model

- **Algorithm:** Gradient Boosting Classifier (200 estimators)
- **Features:** Age, Annual Income, Loan Amount, Credit Score, Employment Years, Debt-to-Income Ratio, Credit Lines, Delinquencies
- **Explainability:** SHAP TreeExplainer
- **Training Data:** 3,000 synthetic loan applications with realistic bias patterns

## 📝 License

MIT
