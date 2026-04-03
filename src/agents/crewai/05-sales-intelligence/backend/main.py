from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"))

from models import LeadRequest, LeadResponse, LeadInput, LeadFlowState, LeadStatus
from flow import LeadProcessingFlow

app = FastAPI(title="Sales Intelligence System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

leads_store: dict[str, dict] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/process-lead", response_model=LeadResponse)
def process_lead(request: LeadRequest):
    lead_id = str(uuid.uuid4())[:8]
    lead_input = LeadInput(
        name=request.name,
        email=request.email,
        company=request.company,
        title=request.title,
        linkedin_url=request.linkedin_url,
        notes=request.notes,
    )

    initial_state = LeadFlowState(lead=lead_input)
    flow = LeadProcessingFlow()
    flow.state = initial_state
    flow.kickoff()

    state = flow.state
    lead_data = {
        "lead_id": lead_id,
        "name": request.name,
        "company": request.company,
        "status": state.status.value,
        "overall_score": state.score.overall_score,
        "email_subject": state.email.subject,
        "email_body": state.email.body,
        "scoring_rationale": state.score.scoring_rationale,
        "enrichment_summary": state.enrichment.company_description[:500],
    }
    leads_store[lead_id] = lead_data
    return LeadResponse(**lead_data)


@app.get("/leads")
def list_leads():
    return {"leads": list(leads_store.values())}


@app.post("/approve/{lead_id}")
def approve_lead(lead_id: str):
    if lead_id not in leads_store:
        raise HTTPException(status_code=404, detail="Lead not found")
    leads_store[lead_id]["status"] = LeadStatus.APPROVED.value
    return {"message": "Lead approved", "lead": leads_store[lead_id]}


@app.post("/reject/{lead_id}")
def reject_lead(lead_id: str):
    if lead_id not in leads_store:
        raise HTTPException(status_code=404, detail="Lead not found")
    leads_store[lead_id]["status"] = LeadStatus.REJECTED.value
    return {"message": "Lead rejected", "lead": leads_store[lead_id]}
