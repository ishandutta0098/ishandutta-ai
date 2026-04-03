from pydantic import BaseModel, Field


class ApplicationRequest(BaseModel):
    resume_text: str = Field(..., description="The candidate's resume text")
    job_url: str = Field("", description="URL of the job posting")
    job_description: str = Field("", description="Job description text")
    company_name: str = Field("", description="Company name")


class CompanyProfile(BaseModel):
    company_name: str = ""
    industry: str = ""
    company_size: str = ""
    culture_values: list[str] = []
    tech_stack: list[str] = []
    recent_news: list[str] = []
    key_requirements: list[str] = []


class TailoredResume(BaseModel):
    optimized_summary: str = ""
    highlighted_skills: list[str] = []
    keyword_matches: list[str] = []
    suggestions: list[str] = []
    match_score: int = Field(0, ge=0, le=100)


class CoverLetter(BaseModel):
    subject_line: str = ""
    body: str = ""
    key_talking_points: list[str] = []


class ApplicationPackage(BaseModel):
    company_profile: CompanyProfile = Field(default_factory=CompanyProfile)
    tailored_resume: TailoredResume = Field(default_factory=TailoredResume)
    cover_letter: CoverLetter = Field(default_factory=CoverLetter)
    overall_match_score: int = Field(0, ge=0, le=100)
