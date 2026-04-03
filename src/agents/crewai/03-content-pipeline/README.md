# 03 — Content Marketing Pipeline

> **Case Study:** [Jasper](https://jasper.ai/) — the $1.5B AI content platform used by marketing teams to create on-brand content at scale, with built-in brand voice, style guides, and approval workflows.

## What This Project Does

A CrewAI Flow orchestrating 3 separate Crews with conditional routing:
1. **Research Crew** — searches the web for supporting data and sources
2. **Writing Crew** — writes the article using research, brand style guide (knowledge), and memory
3. **QA Crew** — reviews quality, checks guardrails, routes to publish or revise

If the QA score is below 75, the Flow routes back to the Writing Crew for revision (max 2 times).

## Architecture

```
User → [content brief] → FastAPI → Content Flow
                                      ├── @start: Research Crew
                                      ├── @listen: Writing Crew (memory + knowledge)
                                      ├── @router: QA Crew (guardrails)
                                      │     ├── score >= 75 → publish
                                      │     └── score < 75 → revise (loop back)
                                      └── @listen("publish"): Final Content
                                   → Content → React UI
```

## CrewAI Features Used

| Feature | Where |
|---------|-------|
| Flows (@start, @listen, @router) | `backend/flow.py` |
| Flow state (Pydantic BaseModel) | `backend/models.py` — ContentState |
| Multi-crew orchestration | 3 separate crews in `backend/crews/` |
| Memory system | Writing crew — `memory=True` |
| Knowledge / RAG | `backend/knowledge/style_guide.txt` |
| Guardrails | `backend/guardrails.py` — validate_word_count, validate_no_placeholders |
| Conditional routing | QA crew routes to publish or revise |
| SerperDevTool | Research crew |
| ScrapeWebsiteTool | Research crew |
| Template variables | All crews use brief parameters |

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API key (set in root `.env` as `OPENROUTER_API_KEY`)
- Serper API key (set as `SERPER_API_KEY`)

## Setup

### Backend
```bash
cd src/agents/crewai/03-content-pipeline
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8002
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
03-content-pipeline/
├── requirements.txt
├── README.md
├── backend/
│   ├── main.py              # FastAPI server
│   ├── flow.py              # ContentPipelineFlow (start → write → router → publish/revise)
│   ├── models.py            # ContentState, ContentBrief, request/response
│   ├── guardrails.py        # validate_word_count, validate_no_placeholders
│   ├── knowledge/
│   │   └── style_guide.txt  # Brand style guide for RAG
│   └── crews/
│       ├── research_crew.py # Web research with SerperDev + Scraper
│       ├── writing_crew.py  # Content writing with memory + knowledge
│       └── qa_crew.py       # Quality review with guardrails
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx           # React UI with pipeline visualization
        └── App.css           # Jasper-purple themed styles
```

## How the Flow Works

1. `@start research_topic` — Research Crew searches the web and compiles a research brief
2. `@listen write_content` — Writing Crew uses research + style guide (knowledge) + memory to write content
3. `@router evaluate_quality` — QA Crew scores the content (1-100):
   - Score >= 75 → routes to `"publish"`
   - Score < 75 and revisions remaining → routes to `"revise"`
   - Max revisions reached → routes to `"publish"` regardless
4. `@listen("publish")` — Sets final content and marks as published
5. `@listen("revise")` — Loops back to writing with feedback from QA
