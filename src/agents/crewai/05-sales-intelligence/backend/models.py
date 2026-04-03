from pydantic import BaseModel, Field
from enum import Enum


class LeadStatus(str, Enum):
    PENDING = "pending"
    ENRICHING = "enriching"
    SCORING = "scoring"
    GENERATING_OUTREACH = "generating_outreach"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class LeadInput(BaseModel):
    name: str = Field(..., description="Contact person name")
    email: str = Field("", description="Contact email")
    company: str = Field(..., description="Company name")
    title: str = Field("", description="Job title")
    linkedin_url: str = Field("", description="LinkedIn profile URL")
    notes: str = Field("", description="Additional context")


class EnrichedLead(BaseModel):
    company_description: str = ""
    industry: str = ""
    company_size: str = ""
    funding_stage: str = ""
    tech_stack: list[str] = []
    recent_news: list[str] = []
    pain_points: list[str] = []
    decision_maker: bool = False
    person_background: str = ""


class LeadScore(BaseModel):
    fit_score: int = Field(0, ge=0, le=100)
    intent_score: int = Field(0, ge=0, le=100)
    engagement_score: int = Field(0, ge=0, le=100)
    overall_score: int = Field(0, ge=0, le=100)
    scoring_rationale: str = ""
    recommended_action: str = ""


class OutreachEmail(BaseModel):
    subject: str = ""
    body: str = ""
    personalization_hooks: list[str] = []
    call_to_action: str = ""
    quality_score: int = 0


class LeadFlowState(BaseModel):
    lead: LeadInput = Field(default_factory=lambda: LeadInput(name="", company=""))
    enrichment: EnrichedLead = Field(default_factory=EnrichedLead)
    score: LeadScore = Field(default_factory=LeadScore)
    email: OutreachEmail = Field(default_factory=OutreachEmail)
    status: LeadStatus = LeadStatus.PENDING
    revision_count: int = 0
    max_revisions: int = 2
    email_feedback: str = ""


class LeadRequest(BaseModel):
    name: str
    email: str = ""
    company: str
    title: str = ""
    linkedin_url: str = ""
    notes: str = ""


class LeadResponse(BaseModel):
    lead_id: str
    name: str
    company: str
    status: str
    overall_score: int = 0
    email_subject: str = ""
    email_body: str = ""
    scoring_rationale: str = ""
    enrichment_summary: str = ""
