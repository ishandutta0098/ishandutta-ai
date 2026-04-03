from crewai import Agent, Crew, Process, Task, LLM
import os


def create_writing_crew():
    llm = LLM(
        model="openrouter/openai/gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    writer = Agent(
        role="Senior Content Writer",
        goal="Write compelling, on-brand {content_type} content about {topic} that engages {target_audience}",
        backstory=(
            "You are an award-winning content writer who specializes in creating "
            "engaging, well-structured content. You always follow the brand style guide "
            "and write in a way that resonates with the target audience. "
            "You have a talent for making complex topics accessible."
        ),
        llm=llm,
        verbose=True,
    )

    writing_task = Task(
        description=(
            "Using the research provided, write a {content_type} about '{topic}' "
            "for {target_audience}. The tone should be {tone}. "
            "Target approximately {word_count} words. "
            "Follow the brand style guide carefully. "
            "\n\nResearch to incorporate:\n{research}"
            "\n\n{revision_instructions}"
        ),
        expected_output=(
            "A complete, polished {content_type} that: follows the brand style guide, "
            "incorporates research and data, is approximately {word_count} words, "
            "has clear headings and structure, includes a hook and call-to-action, "
            "and is ready for editorial review."
        ),
        agent=writer,
    )

    return Crew(
        agents=[writer],
        tasks=[writing_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
    )
