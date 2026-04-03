from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"))

from models import NewsletterRequest, NewsletterResponse
from crew import TLDRNewsletterCrew

app = FastAPI(title="TLDR Newsletter Agent")
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


@app.post("/generate", response_model=NewsletterResponse)
def generate_newsletter(request: NewsletterRequest):
    crew_instance = TLDRNewsletterCrew()
    result = crew_instance.crew().kickoff(inputs={"topic": request.topic})
    return NewsletterResponse(topic=request.topic, newsletter=result.raw)
