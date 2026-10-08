from fastapi import FastAPI
from pydantic import BaseModel

from app.analyzer import analyze_log
from app.ai_analyzer import analyze_with_ai


app = FastAPI(
    title="AI DevOps Incident Analyzer",
    description="AI-powered DevOps incident analysis API",
    version="1.0.0",
)


class LogRequest(BaseModel):
    log: str


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze(request: LogRequest):
    incident = analyze_log(request.log)

    ai_result = analyze_with_ai(incident)

    return {
        "incident": incident,
        "ai_analysis": ai_result,
    }
