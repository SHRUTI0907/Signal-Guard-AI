from ai.retrieval import retrieve_evidence
def test_retrieval():
    text=("Ordinary product operations. "*100)+("Liquidity pressure refinancing borrowing obligations. "*100)
    out=retrieve_evidence(text,query="liquidity refinancing borrowing",top_k=1)
    assert out and "Liquidity" in out[0]["excerpt"]
