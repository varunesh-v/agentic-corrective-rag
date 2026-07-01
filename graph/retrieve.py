def retrieve(state):

    question = state["question"]

    current_db = state["vector_db"]

    results = current_db.similarity_search_with_relevance_scores(
        question,
        k=10
    )

    docs = []
    scores = []

    for doc, score in results:
        docs.append(doc)
        scores.append(score)

    best_score = max(scores) if scores else 0

    print("\n========== RETRIEVAL ==========")
    print("Question:", question)
    print("Retrieved docs:", len(docs))
    print("Best score:", best_score)

    return {
        "question": question,
        "documents": docs,
        "retrieval_score": best_score,
        "vector_db": current_db
    }