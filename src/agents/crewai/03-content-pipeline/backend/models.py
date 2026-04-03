from pydantic import BaseModel, Field


class ContentBrief(BaseModel):
    topic: str
    target_audience: str = "tech professionals"
    content_type: str = "blog post"
    tone: str = "professional yet approachable"
    word_count: int = 800


class ContentState(BaseModel):
    brief: ContentBrief = Field(default_factory=lambda: ContentBrief(topic=""))
    research: str = ""
    draft: str = ""
    quality_score: int = 0
    feedback: str = ""
    revision_count: int = 0
    max_revisions: int = 2
    status: str = "pending"
    final_content: str = ""


class ContentRequest(BaseModel):
    topic: str
    target_audience: str = "tech professionals"
    content_type: str = "blog post"
    tone: str = "professional yet approachable"
    word_count: int = 800


class ContentResponse(BaseModel):
    topic: str
    content: str
    quality_score: int
    revision_count: int
    status: str
