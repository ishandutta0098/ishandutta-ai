def validate_word_count(result) -> tuple[bool, str]:
    word_count = len(result.raw.split())
    if word_count < 200:
        return (
            False,
            f"Content is too short ({word_count} words). Expand to at least 200 words with more detail and examples.",
        )
    return (True, result.raw)


def validate_no_placeholders(result) -> tuple[bool, str]:
    placeholders = ["[INSERT", "[TODO", "[PLACEHOLDER", "Lorem ipsum", "TBD", "[YOUR", "XXXX"]
    text = result.raw
    found = [p for p in placeholders if p.lower() in text.lower()]
    if found:
        return (
            False,
            f"Content contains placeholders: {', '.join(found)}. Replace all placeholders with actual content.",
        )
    return (True, result.raw)
