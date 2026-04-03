# 01 — TLDR Newsletter Agent

> **Case Study:** [TLDR](https://tldr.tech/) — the curated tech newsletter with 5M+ subscribers that delivers the most important tech news in 5 minutes.

## What This Project Does

A CrewAI-powered agent system that replicates TLDR's core workflow:
1. **Researcher** searches the web for trending tech stories on any topic
2. **Writer** distills each story into a 2-3 sentence TLDR-style summary
3. **Editor** organizes everything into a polished newsletter with sections

## Architecture

```
User → [topic] → FastAPI → Sequential Crew
                              ├── Researcher (SerperDev + Scraper)
                              ├── Writer
                              └── Editor
                           → Newsletter → React UI
```

## CrewAI Features Used

| Feature | Where |
|---------|-------|
| Agent (role/goal/backstory) | `backend/config/agents.yaml` |
| Task (description/expected_output) | `backend/config/tasks.yaml` |
| Crew (Process.sequential) | `backend/crew.py` |
| @CrewBase decorator | `backend/crew.py` |
| YAML configuration | `backend/config/` |
| SerperDevTool | Researcher agent |
| ScrapeWebsiteTool | Researcher agent |
| Template variables ({topic}) | Tasks config |
| Verbose mode | All agents |

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API key (set in root `.env` as `OPENROUTER_API_KEY`)
- Serper API key (set as `SERPER_API_KEY`) — get one free at [serper.dev](https://serper.dev)

## Setup

### Backend
```bash
cd src/agents/crewai/01-tldr-newsletter
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
01-tldr-newsletter/
├── requirements.txt
├── README.md
├── backend/
│   ├── main.py              # FastAPI server
│   ├── crew.py              # CrewAI crew definition
│   ├── models.py            # Pydantic request/response models
│   └── config/
│       ├── agents.yaml      # Agent definitions (role, goal, backstory)
│       └── tasks.yaml       # Task definitions (description, expected_output)
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx           # React UI
        └── App.css           # Styles
```

## How It Works

1. User enters a topic in the React frontend
2. Frontend sends POST request to `/generate` with the topic
3. FastAPI instantiates the `TLDRNewsletterCrew` (3 agents, 3 tasks, sequential)
4. **Research Task:** Researcher agent uses SerperDevTool to search the web, ScrapeWebsiteTool to read articles, and compiles 5 key stories
5. **Write Task:** Writer agent takes the research and writes TLDR-style 2-3 sentence summaries for each story
6. **Edit Task:** Editor agent organizes the summaries into a newsletter format with Headlines, Deep Dives, and Quick Hits sections
7. The final newsletter is returned and rendered in the React UI with Markdown formatting
