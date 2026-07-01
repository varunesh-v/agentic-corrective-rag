from llm import invoke_llm
from prompts.rag_prompt import RAG_PROMPT


def generate(state):

    question = state["question"]
    documents = state["documents"]

    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    answer = invoke_llm(
        RAG_PROMPT,
        f"""
Question:
{question}

Context:
{context}
"""
    )

    print("\n========== GENERATION ==========")

    return {
    "answer": answer,
    "route": state["route"],
    "retrieval_score": state["retrieval_score"]
}