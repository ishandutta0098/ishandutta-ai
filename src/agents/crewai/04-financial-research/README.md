# Project 4: Financial Research Report Generator

**Case Study: [Finchat.io](https://finchat.io)** — AI platform for institutional-grade equity research reports with data integration.

## Architecture

```
User Query (Company Name + Ticker)
            │
            ▼
    ┌───────────────┐
    │  AgentPlanner  │  ← planning=True decomposes the query
    │   (CrewAI)     │
    └───────┬───────┘
            │
    ┌───────▼────────┐     ┌──────────────┐
    │ Data Collector  │────▶│ SerperDevTool │
    │    Agent        │────▶│ ScrapeWebsite │
    └───────┬────────┘     └──────────────┘
            │
    ┌───────▼────────┐
    │   Financial     │
    │   Analyst       │
    └───────┬────────┘
            │
    ┌───────▼────────┐
    │ Report Writer   │──▶ Professional Equity Research Report
    └────────────────┘
            │
    step_callback ──▶ Execution Log
    task_callback ──▶ Task Completion Tracking
    output_log_file ──▶ crew_execution.log
```

## CrewAI Features Covered

| Feature | Description |
|---------|-------------|
| `planning=True` | AgentPlanner automatically decomposes complex research queries into sub-steps before execution |
| `step_callback` | Fires after each agent reasoning step for real-time observability |
| `task_callback` | Fires after each task completes, capturing outputs and timing |
| `output_log_file` | Persists full execution trace to `crew_execution.log` |
| `output_pydantic` | Structured Pydantic models for type-safe report data |
| Multi-Agent Sequential | Three specialist agents in a sequential pipeline |
| Production Architecture | FastAPI backend, React frontend, YAML configs, modular code |

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenRouter API key (set in root `.env` as `OPENROUTER_API_KEY`)
- Serper API key (optional, for live web search — set as `SERPER_API_KEY`)

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Running

### Start Backend (port 8003)

```bash
cd backend
uvicorn main:app --reload --port 8003
```

### Start Frontend (port 3003)

```bash
cd frontend
npm run dev
```

Open [http://localhost:3003](http://localhost:3003) in your browser.

## Project Structure

```
04-financial-research/
├── requirements.txt
├── README.md
├── backend/
│   ├── config/
│   │   ├── agents.yaml       # Agent role, goal, backstory definitions
│   │   └── tasks.yaml        # Task descriptions and expected outputs
│   ├── models.py             # Pydantic models (query, report, response)
│   ├── callbacks.py          # Step and task callbacks for observability
│   ├── crew.py               # CrewBase crew with planning mode
│   └── main.py               # FastAPI application
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx           # React app with report UI
        └── App.css           # Bloomberg-terminal-inspired styling
```

## How Planning Mode Works

When `planning=True` is set on a Crew, CrewAI activates the **AgentPlanner** before task execution begins. The planner:

1. Receives the full list of tasks and their descriptions
2. Analyzes dependencies between tasks
3. Creates an optimized execution plan with sub-steps
4. Each agent receives its portion of the plan as additional context

This results in more coherent output because agents understand the full research pipeline, not just their individual task.

## Callbacks and Logging

### Step Callback

Fires after every internal reasoning step an agent takes. Useful for monitoring agent "thinking" in real-time:

```python
def step_callback(step_output):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] Step: {str(step_output)[:150]}"
    execution_log.append(log_entry)
```

### Task Callback

Fires when an entire task completes. Captures the task description and output summary:

```python
def task_callback(task_output):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] Task completed: {task_output.description[:80]}..."
    execution_log.append(log_entry)
```

### Output Log File

The `output_log_file="crew_execution.log"` parameter persists the full verbose execution trace to disk, useful for post-run debugging and auditing.

## Production Architecture Patterns

- **YAML-driven configuration**: Agents and tasks defined declaratively, separating config from logic
- **Pydantic models**: Type-safe request/response schemas with validation
- **Callback observability**: Real-time execution monitoring piped to the frontend
- **FastAPI backend**: Production-grade async API with CORS, health checks
- **Modular structure**: Clean separation of concerns (models, callbacks, crew, API)
