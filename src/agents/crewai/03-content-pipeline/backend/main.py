from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"))

from models import ContentRequest, ContentResponse, ContentBrief, ContentState
from flow import ContentPipelineFlow

app = FastAPI(title="Content Marketing Pipeline")
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


@app.post("/create-content", response_model=ContentResponse)
def create_content(request: ContentRequest):
    brief = ContentBrief(
        topic=request.topic,
        target_audience=request.target_audience,
        content_type=request.content_type,
        tone=request.tone,
        word_count=request.word_count,
    )
    initial_state = ContentState(brief=brief)
    flow = ContentPipelineFlow()
    flow.state = initial_state
    flow.kickoff()

    return ContentResponse(
        topic=request.topic,
        content=flow.state.final_content or flow.state.draft,
        quality_score=flow.state.quality_score,
        revision_count=flow.state.revision_count,
        status=flow.state.status,
    )
