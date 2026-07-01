import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.documents import Document

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def web_search(state):

    question = state["question"]

    response = client.search(
        query=question,
        max_results=5,
        search_depth="advanced"
    )

    web_docs = []

    for result in response["results"]:

        content = result.get("content", "")

        if content:
            web_docs.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": result.get("url")
                    }
                )
            )

    print("\n========== WEB SEARCH ==========")
    print("Retrieved:", len(web_docs))

    return {
        **state,
        "documents": web_docs
    }