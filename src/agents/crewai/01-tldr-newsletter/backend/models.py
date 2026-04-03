from pydantic import BaseModel


class NewsletterRequest(BaseModel):
    topic: str
    num_stories: int = 5


class NewsletterResponse(BaseModel):
    topic: str
    newsletter: str
    status: str = "completed"
