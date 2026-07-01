from llm import invoke_llm
from prompts.rewrite_prompt import REWRITE_PROMPT


def rewrite_query(state):

    question = state["question"]

    rewritten = invoke_llm(
        REWRITE_PROMPT,
        question
    )

    print("\n========== QUERY REWRITE ==========")
    print("Original:", question)
    print("Rewritten:", rewritten)

    return {
        **state,
        "question": rewritten
    }