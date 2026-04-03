# 05 — Sales Intelligence System

> **Case Study:** [Clay](https://clay.com/) — the $1.3B sales intelligence platform that enriches leads from CRM data, researches companies, scores prospects, and generates hyper-personalized outreach with human review gates.

## What This Project Does

An end-to-end CrewAI Flow that processes sales leads through a full pipeline:
1. **Enrichment Crew** — researches the company and contact person
2. **Scoring Crew** — scores the lead on fit, intent, and engagement (with guardrails)
3. **Outreach Crew** — generates a personalized email with a self-evaluation quality loop
4. **Human Approval** — email is held for review before sending

High-score leads (>= 70) get outreach; low-score leads are archived. The outreach email goes through a self-evaluation loop (max 2 revisions) before human review.

## Architecture

```
User → [lead data] → FastAPI → Lead Processing Flow
                                  ├── @start: Enrichment Crew (2 agents)
                                  ├── @listen: Scoring Crew (guardrails)
                                  ├── @router: Route by score
                                  │     ├── score >= 70 → Outreach Crew
                                  │     └── score < 70 → Archive
                                  ├── Outreach Crew → Self-eval loop
                                  │     ├── quality >= 75 → Human Review
                                  │     └── quality < 75 → Revise (max 2x)
                                  └── Human Review (approve/reject API)
                               → Dashboard → React UI
```

## CrewAI Features Used

| Feature | Where |
|---------|-------|
| Flows (@start, @listen, @router) | `backend/flow.py` |
| Flow state (Pydantic BaseModel) | `backend/models.py` — LeadFlowState |
| Multi-crew orchestration | 3 crews in `backend/crews/` |
| Self-evaluation loop | Outreach → quality check → revise or approve |
| Guardrails | `backend/guardrails.py` — validate_score_range, validate_email_quality |
| Memory | Outreach crew — `memory=True` |
| Structured Pydantic outputs | All models in `backend/models.py` |
| Conditional routing | Score-based and quality-based routing |
| Human-in-the-loop | `/approve/{id}` and `/reject/{id}` endpoints |
| Docker deployment | `Dockerfile` + `docker-compose.yml` |
| SerperDevTool | Enrichment crew |
| ScrapeWebsiteTool | Enrichment crew |

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API key (set in root `.env` as `OPENROUTER_API_KEY`)
- Serper API key (set as `SERPER_API_KEY`)
- Docker (optional, for containerized deployment)

## Setup

### Local Development

#### Backend
```bash
cd src/agents/crewai/05-sales-intelligence
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8004
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment
```bash
cd src/agents/crewai/05-sales-intelligence
docker compose up --build
```

## Project Structure

```
05-sales-intelligence/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── backend/
│   ├── main.py              # FastAPI with process/approve/reject endpoints
│   ├── flow.py              # LeadProcessingFlow with routing + self-eval
│   ├── models.py            # LeadFlowState, LeadScore, OutreachEmail, etc.
│   ├── guardrails.py        # validate_score_range, validate_email_quality
│   └── crews/
│       ├── enrichment_crew.py  # Company + person research (2 agents)
│       ├── scoring_crew.py     # Lead scoring with guardrails
│       └── outreach_crew.py    # Email generation with memory
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx           # Dashboard with lead cards + approve/reject
        └── App.css           # Clay-orange dark theme
```

## How the Self-Evaluation Loop Works

1. Outreach Crew generates a personalized email
2. `evaluate_email_quality` router checks:
   - Has personalization hooks? (from enrichment data)
   - Is concise? (< 250 words)
   - Has a subject line?
   - Has sufficient content? (> 30 words)
3. If quality >= 75 → route to human review
4. If quality < 75 and revisions remain → route back to outreach with feedback
5. After max revisions → proceed to human review regardless
