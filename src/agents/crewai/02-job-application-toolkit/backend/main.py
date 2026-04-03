from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"))

from models import ApplicationRequest, ApplicationPackage, CompanyProfile, TailoredResume, CoverLetter
from crew import JobApplicationCrew

app = FastAPI(title="Job Application Toolkit")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/apply", response_model=ApplicationPackage)
def apply_to_job(request: ApplicationRequest):
    crew_instance = JobApplicationCrew()
    result = crew_instance.crew().kickoff(
        inputs={
            "resume_text": request.resume_text,
            "job_url": request.job_url,
            "job_description": request.job_description,
            "company_name": request.company_name or "the company",
        }
    )
    tasks_output = result.tasks_output
    company = tasks_output[0].pydantic if tasks_output[0].pydantic else CompanyProfile()
    resume = tasks_output[1].pydantic if tasks_output[1].pydantic else TailoredResume()
    cover = tasks_output[2].pydantic if tasks_output[2].pydantic else CoverLetter(body=result.raw)

    return ApplicationPackage(
        company_profile=company,
        tailored_resume=resume,
        cover_letter=cover,
        overall_match_score=resume.match_score,
    )
