import re


def validate_score_range(result) -> tuple[bool, str]:
    text = result.raw
    scores = re.findall(r"\b(\d{1,3})\b", text)
    int_scores = [int(s) for s in scores if 0 <= int(s) <= 100]
    if not int_scores:
        return (
            False,
            "No valid scores found. Provide scores as numbers between 0-100 for fit, intent, engagement, and overall.",
        )
    return (True, result.raw)


def validate_email_quality(result) -> tuple[bool, str]:
    text = result.raw
    if len(text.strip()) < 100:
        return (False, "Email is too short. Write a substantive outreach email with at least 100 characters.")

    placeholders = ["[NAME]", "[COMPANY]", "[INSERT", "[TODO", "XXXX", "[YOUR"]
    found = [p for p in placeholders if p.lower() in text.lower()]
    if found:
        return (
            False,
            f"Email contains unfilled placeholders: {', '.join(found)}. Replace all placeholders with personalized content.",
        )

    if "subject:" not in text.lower() and "subject line:" not in text.lower():
        return (False, "Email must include a subject line. Start with 'Subject: ...' followed by the email body.")

    return (True, result.raw)
