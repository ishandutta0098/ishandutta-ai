from crewai.flow.flow import Flow, listen, start, router
from models import ContentState, ContentBrief
from crews.research_crew import create_research_crew
from crews.writing_crew import create_writing_crew
from crews.qa_crew import create_qa_crew
import re


class ContentPipelineFlow(Flow[ContentState]):

    @start()
    def research_topic(self):
        print(f"[Flow] Starting research on: {self.state.brief.topic}")
        self.state.status = "researching"
        research_crew = create_research_crew()
        result = research_crew.kickoff(
            inputs={
                "topic": self.state.brief.topic,
                "content_type": self.state.brief.content_type,
                "target_audience": self.state.brief.target_audience,
            }
        )
        self.state.research = result.raw
        print(f"[Flow] Research complete: {len(self.state.research)} chars")
        return self.state.research

    @listen(research_topic)
    def write_content(self):
        print(f"[Flow] Writing content (revision #{self.state.revision_count})")
        self.state.status = "writing"

        revision_instructions = ""
        if self.state.revision_count > 0:
            revision_instructions = (
                f"REVISION REQUIRED. This is revision #{self.state.revision_count}. "
                f"Previous feedback:\n{self.state.feedback}\n"
                f"Previous draft to improve:\n{self.state.draft}"
            )

        writing_crew = create_writing_crew()
        result = writing_crew.kickoff(
            inputs={
                "topic": self.state.brief.topic,
                "content_type": self.state.brief.content_type,
                "target_audience": self.state.brief.target_audience,
                "tone": self.state.brief.tone,
                "word_count": str(self.state.brief.word_count),
                "research": self.state.research,
                "revision_instructions": revision_instructions,
            }
        )
        self.state.draft = result.raw
        print(f"[Flow] Draft complete: {len(self.state.draft)} chars")
        return self.state.draft

    @router(write_content)
    def evaluate_quality(self):
        print("[Flow] Evaluating content quality...")
        self.state.status = "reviewing"

        qa_crew = create_qa_crew()
        result = qa_crew.kickoff(inputs={"draft": self.state.draft})

        score_match = re.search(r"\b(\d{1,3})\b", result.raw.split("\n")[0])
        self.state.quality_score = int(score_match.group(1)) if score_match else 50
        self.state.feedback = result.raw

        print(f"[Flow] Quality score: {self.state.quality_score}")

        if self.state.quality_score >= 75:
            return "publish"
        if self.state.revision_count >= self.state.max_revisions:
            print(f"[Flow] Max revisions reached. Publishing with score {self.state.quality_score}")
            return "publish"

        self.state.revision_count += 1
        return "revise"

    @listen("publish")
    def publish_content(self):
        print(f"[Flow] Publishing content with score {self.state.quality_score}")
        self.state.status = "published"
        self.state.final_content = self.state.draft
        return self.state.final_content

    @listen("revise")
    def revise_content(self):
        print(f"[Flow] Revision #{self.state.revision_count} needed")
        self.state.status = "revising"
        return self.write_content()
