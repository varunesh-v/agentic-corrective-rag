from langgraph.graph import StateGraph, END

from graph.state import GraphState
from graph.retrieve import retrieve
from graph.grade_documents import grade_documents
from graph.rewrite_query import rewrite_query
from graph.web_search import web_search
from graph.generate import generate

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade", grade_documents)
workflow.add_node("rewrite", rewrite_query)
workflow.add_node("web", web_search)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")

workflow.add_edge(
    "retrieve",
    "grade"
)


def route(state):

    if state["route"] == "local":
        return "generate"

   
    return "rewrite"


workflow.add_conditional_edges(
    "grade",
    route,
    {
        "generate": "generate",
        "rewrite": "rewrite"
    }
)

workflow.add_edge(
    "rewrite",
    "web"
)

workflow.add_edge(
    "web",
    "generate"
)

workflow.add_edge(
    "generate",
    END
)

app = workflow.compile()