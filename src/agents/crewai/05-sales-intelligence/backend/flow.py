from crewai.flow.flow import Flow, listen, start, router
from models import LeadFlowState, LeadInput, LeadStatus
from crews.enrichment_crew import create_enrichment_crew
from crews.scoring_crew import create_scoring_crew
from crews.outreach_crew import create_outreach_crew
import re


class LeadProcessingFlow(Flow[LeadFlowState]):

    @start()
    def enrich_lead(self):
        print(f"[Flow] Enriching lead: {self.state.lead.name} at {self.state.lead.company}")
        self.state.status = LeadStatus.ENRICHING

        enrichment_crew = create_enrichment_crew()
        result = enrichment_crew.kickoff(
            inputs={
                "name": self.state.lead.name,
                "company": self.state.lead.company,
                "title": self.state.lead.title,
                "linkedin_url": self.state.lead.linkedin_url,
                "notes": self.state.lead.notes,
            }
        )
        self.state.enrichment.company_description = result.raw
        print(f"[Flow] Enrichment complete: {len(result.raw)} chars")
        return result.raw

    @listen(enrich_lead)
    def score_lead(self):
        print(f"[Flow] Scoring lead: {self.state.lead.name}")
        self.state.status = LeadStatus.SCORING

        scoring_crew = create_scoring_crew()
        result = scoring_crew.kickoff(
            inputs={
                "name": self.state.lead.name,
                "title": self.state.lead.title,
                "company": self.state.lead.company,
                "enrichment_data": self.state.enrichment.company_description,
            }
        )

        scores = re.findall(r"(\d{1,3})", result.raw)
        int_scores = [int(s) for s in scores if 0 <= int(s) <= 100]
        if len(int_scores) >= 4:
            self.state.score.fit_score = int_scores[0]
            self.state.score.intent_score = int_scores[1]
            self.state.score.engagement_score = int_scores[2]
            self.state.score.overall_score = int_scores[3]
        elif int_scores:
            self.state.score.overall_score = int_scores[-1]

        self.state.score.scoring_rationale = result.raw
        print(f"[Flow] Lead scored: {self.state.score.overall_score}/100")
        return self.state.score.overall_score

    @router(score_lead)
    def route_by_score(self):
        score = self.state.score.overall_score
        if score >= 70:
            print(f"[Flow] High score ({score}) — routing to outreach")
            return "generate_outreach"
        print(f"[Flow] Low score ({score}) — archiving lead")
        return "archive_lead"

    @listen("archive_lead")
    def archive(self):
        print(f"[Flow] Archiving lead: {self.state.lead.name} (score: {self.state.score.overall_score})")
        self.state.status = LeadStatus.ARCHIVED
        return "archived"

    @listen("generate_outreach")
    def generate_email(self):
        print(f"[Flow] Generating outreach email (attempt #{self.state.revision_count + 1})")
        self.state.status = LeadStatus.GENERATING_OUTREACH

        revision_instructions = ""
        if self.state.revision_count > 0:
            revision_instructions = (
                f"REVISION #{self.state.revision_count}: Previous email did not meet quality standards. "
                f"Feedback: {self.state.email_feedback}\n"
                f"Previous email to improve:\n{self.state.email.body}"
            )

        outreach_crew = create_outreach_crew()
        result = outreach_crew.kickoff(
            inputs={
                "name": self.state.lead.name,
                "title": self.state.lead.title,
                "company": self.state.lead.company,
                "enrichment_data": self.state.enrichment.company_description,
                "overall_score": str(self.state.score.overall_score),
                "scoring_rationale": self.state.score.scoring_rationale,
                "revision_instructions": revision_instructions,
            }
        )

        email_text = result.raw
        subject_match = re.search(r"Subject:\s*(.+)", email_text, re.IGNORECASE)
        self.state.email.subject = subject_match.group(1).strip() if subject_match else "Outreach"

        body_start = email_text.find("\n", email_text.lower().find("subject:")) + 1 if "subject:" in email_text.lower() else 0
        self.state.email.body = email_text[body_start:].strip() if body_start > 0 else email_text

        hooks = re.findall(r"\d+\.\s*(.+)", email_text.split("Personalization hooks")[-1]) if "personalization hooks" in email_text.lower() else []
        self.state.email.personalization_hooks = hooks[:3]

        return email_text

    @router(generate_email)
    def evaluate_email_quality(self):
        email_text = f"{self.state.email.subject}\n{self.state.email.body}"
        word_count = len(email_text.split())
        has_personalization = len(self.state.email.personalization_hooks) >= 1
        is_concise = word_count <= 250
        has_subject = len(self.state.email.subject) > 5

        quality_checks = [has_personalization, is_concise, has_subject, word_count >= 30]
        quality_score = int((sum(quality_checks) / len(quality_checks)) * 100)
        self.state.email.quality_score = quality_score

        print(f"[Flow] Email quality: {quality_score}/100")

        if quality_score >= 75:
            return "ready_for_review"
        if self.state.revision_count >= self.state.max_revisions:
            print("[Flow] Max revisions reached. Proceeding with current email.")
            return "ready_for_review"

        self.state.revision_count += 1
        issues = []
        if not has_personalization:
            issues.append("missing personalization")
        if not is_concise:
            issues.append("too long (>250 words)")
        if not has_subject:
            issues.append("missing subject line")
        if word_count < 30:
            issues.append("too short (<30 words)")

        self.state.email_feedback = f"Quality score: {quality_score}/100. Issues: {', '.join(issues)}"
        return "revise_email"

    @listen("revise_email")
    def revise(self):
        print(f"[Flow] Revising email (revision #{self.state.revision_count})")
        return self.generate_email()

    @listen("ready_for_review")
    def submit_for_approval(self):
        print("[Flow] Email ready for human review")
        self.state.status = LeadStatus.PENDING_APPROVAL
        return "pending_approval"
