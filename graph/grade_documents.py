def grade_documents(state):

    score = state["retrieval_score"]

    LOCAL_THRESHOLD = 0.39

    route = (
        "local"
        if score >= LOCAL_THRESHOLD
        else "web"
    )

    print("\n========== CRAG EVALUATOR ==========")
    print(f"Retrieval Score: {score:.3f}")
    print(f"Threshold: {LOCAL_THRESHOLD}")
    print(f"Route: {route}")

    return {
        **state,
        "route": route
    }