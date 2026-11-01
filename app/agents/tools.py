from app.services.retrieval import RegulationRetriever


_retriever = None


def get_retriever():
    global _retriever

    if _retriever is None:
        _retriever = RegulationRetriever()

    return _retriever


def search_corpus(query: str) -> list[dict]:
    """
    Search the indexed electricity regulations.
    """
    return get_retriever().search(
        query=query,
        top_k=5,
    )


def lookup_clause(
    document_id: str,
    clause_identifier: str,
) -> list[dict]:
    """
    Find a clause by its recorded identifier.

    The current index does not yet guarantee reliable
    clause-level parsing. Return only exact matches
    in stored metadata until that parser is implemented.
    """
    chunks = get_retriever().chunks

    matches = []

    for chunk in chunks:
        if chunk["document_id"] != document_id:
            continue

        if chunk.get("clause_id") == clause_identifier:
            matches.append(chunk)

    return matches


def lookup_request_fields(
    complaint: dict,
) -> dict:
    """
    Return facts explicitly supplied by the consumer.
    """
    allowed_fields = [
        "consumer_reference",
        "complaint_text",
        "premises_type",
        "connected_load_kw",
        "current_tariff_category",
        "complaint_type",
    ]

    return {
        key: complaint.get(key)
        for key in allowed_fields
        if key in complaint
    }