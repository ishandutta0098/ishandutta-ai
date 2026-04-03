from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"))

from models import CompanyQuery, ReportResponse
from crew import FinancialResearchCrew
from callbacks import get_execution_log, clear_execution_log

app = FastAPI(title="Financial Research Report Generator")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/research", response_model=ReportResponse)
def generate_research_report(query: CompanyQuery):
    clear_execution_log()
    crew_instance = FinancialResearchCrew()
    result = crew_instance.crew().kickoff(inputs={
        "company": query.company,
        "ticker": query.ticker or query.company[:4].upper(),
    })
    return ReportResponse(
        company=query.company,
        ticker=query.ticker or query.company[:4].upper(),
        report=result.raw,
        rating="Hold",
        generated_at=__import__("datetime").datetime.now().isoformat(),
        execution_log=get_execution_log(),
    )

@app.get("/logs")
def get_logs():
    return {"logs": get_execution_log()}
