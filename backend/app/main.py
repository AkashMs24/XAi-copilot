from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict, explain, bias, appeal, chat, whatif
from app.core.model_loader import load_artifacts


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_artifacts()   # runs once at startup
    yield


app = FastAPI(
    title="Explainable AI Copilot — Loan Credit Risk",
    description="XAI system with SHAP explanations, bias detection, appeal engine, and What-If simulator.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(explain.router, prefix="/api/v1", tags=["Explanation"])
app.include_router(whatif.router,  prefix="/api/v1", tags=["What-If Simulator"])
app.include_router(bias.router,    prefix="/api/v1", tags=["Bias Detection"])
app.include_router(appeal.router,  prefix="/api/v1", tags=["Decision Appeal"])
app.include_router(chat.router,    prefix="/api/v1", tags=["AI Copilot Chat"])


@app.get("/")
def health():
    return {"status": "ok", "message": "XAI Copilot API is running ✅"}
