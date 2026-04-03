from crewai.tools import tool, BaseTool
from pydantic import BaseModel, Field


class ResumeInput(BaseModel):
    resume_text: str = Field(..., description="Raw resume text to parse")


class ResumeParserTool(BaseTool):
    name: str = "Resume Parser"
    description: str = (
        "Parses raw resume text and extracts structured sections "
        "like skills, experience, education, and summary."
    )
    args_schema: type[BaseModel] = ResumeInput

    def _run(self, resume_text: str) -> str:
        sections = {"skills": [], "experience": [], "education": [], "summary": ""}
        current_section = "summary"

        for line in resume_text.strip().split("\n"):
            line_lower = line.lower().strip()
            if not line.strip():
                continue
            if any(kw in line_lower for kw in ["skill", "technologies", "tech stack"]):
                current_section = "skills"
                continue
            elif any(kw in line_lower for kw in ["experience", "work history", "employment"]):
                current_section = "experience"
                continue
            elif any(kw in line_lower for kw in ["education", "degree", "university"]):
                current_section = "education"
                continue

            if current_section == "summary":
                sections["summary"] += line.strip() + " "
            else:
                sections[current_section].append(line.strip())

        result = f"Summary: {sections['summary'].strip()}\n"
        result += f"Skills: {', '.join(sections['skills']) if sections['skills'] else 'Not explicitly listed'}\n"
        result += f"Experience: {'; '.join(sections['experience'][:5]) if sections['experience'] else 'Not found'}\n"
        result += f"Education: {'; '.join(sections['education'][:3]) if sections['education'] else 'Not found'}\n"
        return result


@tool("Parse Job Description")
def parse_job_description(job_description: str) -> str:
    """Extracts key requirements, qualifications, and responsibilities from a job description."""
    sections = {
        "requirements": [],
        "responsibilities": [],
        "qualifications": [],
        "benefits": [],
    }
    current = "requirements"

    for line in job_description.strip().split("\n"):
        line_lower = line.lower().strip()
        if not line.strip():
            continue
        if any(kw in line_lower for kw in ["requirement", "must have", "required"]):
            current = "requirements"
            continue
        elif any(kw in line_lower for kw in ["responsibilit", "duties", "you will"]):
            current = "responsibilities"
            continue
        elif any(kw in line_lower for kw in ["qualificat", "preferred", "nice to have"]):
            current = "qualifications"
            continue
        elif any(kw in line_lower for kw in ["benefit", "perk", "we offer"]):
            current = "benefits"
            continue
        sections[current].append(line.strip())

    result = ""
    for section, items in sections.items():
        if items:
            result += f"\n{section.upper()}:\n" + "\n".join(f"  - {item}" for item in items[:8]) + "\n"
    return result if result else "Could not parse structured sections. Analyze the raw text directly."
