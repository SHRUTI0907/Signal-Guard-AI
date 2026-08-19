from __future__ import annotations

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_QUERY = (
    "liquidity debt refinancing covenant going concern cash flow borrowing "
    "material weakness default credit risk financing obligations"
)

RISK_TERMS = {
    "adverse": [
        "default", "going concern", "material weakness", "covenant breach", "liquidity pressure",
        "unable to", "insufficient liquidity", "substantial doubt", "impairment", "restructuring",
        "adverse", "deterioration", "decline", "loss", "shortfall", "refinancing risk",
    ],
    "supportive": [
        "sufficient liquidity", "strong cash flow", "cash generated", "available liquidity",
        "no material", "compliance with", "adequate liquidity", "cash and cash equivalents",
    ],
}

SECTION_PATTERNS = [
    ("Risk Factors", r"\bitem\s+1a\.?\s+risk factors\b"),
    ("MD&A", r"\bitem\s+2\.?\s+management['’]s discussion and analysis\b"),
    ("Financial Statements", r"\bitem\s+1\.?\s+financial statements\b"),
    ("Controls & Procedures", r"\bitem\s+4\.?\s+controls and procedures\b"),
]


def _clean(text):
    return re.sub(r"\s+", " ", text or " ").strip()


def _section_name(chunk):
    low = chunk.lower()
    found = []
    for name, pattern in SECTION_PATTERNS:
        m = re.search(pattern, low, flags=re.I)
        if m:
            found.append((m.start(), name))
    return min(found)[1] if found else "Filing excerpt"


def chunk_text(text, chunk_words=170, overlap_words=35):
    """Create smaller, more readable chunks while preserving overlap."""
    words = _clean(text).split()
    chunks = []
    step = max(1, chunk_words - overlap_words)
    for i in range(0, len(words), step):
        c = words[i:i + chunk_words]
        if len(c) >= 45:
            chunks.append(" ".join(c))
    return chunks


def classify_evidence(excerpt):
    low = excerpt.lower()
    adverse_hits = sum(term in low for term in RISK_TERMS["adverse"])
    supportive_hits = sum(term in low for term in RISK_TERMS["supportive"])
    if adverse_hits > supportive_hits and adverse_hits:
        return "Adverse"
    if supportive_hits > adverse_hits and supportive_hits:
        return "Supportive"
    return "Neutral"


def retrieve_evidence(text, query=DEFAULT_QUERY, top_k=5):
    chunks = chunk_text(text)
    if not chunks:
        return []

    # Hybrid lexical retrieval: word n-grams + character n-grams.
    # This remains fully local/free while improving robustness to phrasing variation.
    word_vec = TfidfVectorizer(stop_words="english", max_features=16000, ngram_range=(1, 2), sublinear_tf=True)
    char_vec = TfidfVectorizer(analyzer="char_wb", max_features=12000, ngram_range=(3, 5), sublinear_tf=True)
    word_mat = word_vec.fit_transform([query] + chunks)
    char_mat = char_vec.fit_transform([query] + chunks)
    word_scores = cosine_similarity(word_mat[0:1], word_mat[1:]).flatten()
    char_scores = cosine_similarity(char_mat[0:1], char_mat[1:]).flatten()
    scores = 0.75 * word_scores + 0.25 * char_scores

    ranked = scores.argsort()[::-1][:top_k]
    output = []
    for rank, i in enumerate(ranked, start=1):
        excerpt = _clean(chunks[i])
        output.append({
            "rank": rank,
            "score": float(scores[i]),
            "excerpt": excerpt,
            "section": _section_name(excerpt),
            "stance": classify_evidence(excerpt),
        })
    return output
