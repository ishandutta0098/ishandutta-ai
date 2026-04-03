# 02 — Job Application Toolkit

> **Case Study:** [Teal](https://tealhq.com/) — the AI career platform that helps users tailor resumes and cover letters to specific job postings by analyzing job descriptions and matching skills.

## What This Project Does

A hierarchical CrewAI crew where a Career Coach Manager delegates to 3 specialist agents:
1. **Company Researcher** — researches the target company's culture, tech stack, and values
2. **Resume Tailor** — analyzes the job description and optimizes the resume with matching keywords
3. **Cover Letter Writer** — crafts a personalized cover letter using company research and resume analysis

All outputs are structured Pydantic models for clean, type-safe data.

## Architecture

```
User → [resume + job URL] → FastAPI → Hierarchical Crew
                                          ├── Manager (delegates)
                                          ├── Company Researcher (ScrapeWebsiteTool)
                                          ├── Resume Tailor (ResumeParserTool, parse_job_description)
                                          └── Cover Letter Writer
                                       → Application Package → React UI
```

## CrewAI Features Used

| Feature | Where |
|---------|-------|
| Process.hierarchical | `backend/crew.py` |
| manager_llm | `backend/crew.py` |
| allow_delegation | `backend/config/agents.yaml` |
| Custom tool (@tool) | `backend/tools.py` — parse_job_description |
| Custom tool (BaseTool) | `backend/tools.py` — ResumeParserTool |
| output_pydantic | All 3 tasks |
| task.context linking | Resume task depends on research; cover letter depends on both |
| Task callbacks | `on_task_complete` function |
| Multi-model per agent | Different LLMs configurable per agent |
| ScrapeWebsiteTool | Company researcher |

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API key (set in root `.env` as `OPENROUTER_API_KEY`)

## Setup

### Backend
```bash
cd src/agents/crewai/02-job-application-toolkit
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
02-job-application-toolkit/
├── requirements.txt
├── README.md
├── backend/
│   ├── main.py              # FastAPI server
│   ├── crew.py              # Hierarchical crew with manager
│   ├── models.py            # Pydantic models (CompanyProfile, TailoredResume, CoverLetter)
│   ├── tools.py             # Custom tools (ResumeParserTool, parse_job_description)
│   └── config/
│       ├── agents.yaml      # 4 agents including manager
│       └── tasks.yaml       # 3 tasks with context linking
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx           # React UI with tabbed output
        └── App.css           # Teal-themed styles
```

## How Hierarchical Process Works

Unlike sequential process where tasks run in order, hierarchical process uses a **Manager Agent** who:
1. Receives all tasks and available agents
2. Decides which agent should handle which task
3. Delegates tasks based on agent capabilities
4. Can reassign if an agent's output is insufficient
5. Coordinates the final output

The `manager_llm` parameter specifies which LLM the manager uses for coordination decisions.
