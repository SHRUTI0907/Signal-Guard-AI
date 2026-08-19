from functools import lru_cache
import pandas as pd
import requests
from config import CORE_CONCEPTS, SEC_USER_AGENT

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
HEADERS = {"User-Agent": SEC_USER_AGENT, "Accept-Encoding": "gzip, deflate"}

class SECError(RuntimeError):
    pass

def _get_json(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=35)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as exc:
        raise SECError(f"SEC request failed: {exc}") from exc

@lru_cache(maxsize=1)
def ticker_map():
    raw = _get_json(TICKERS_URL)
    return {
        row["ticker"].upper(): {
            "cik": str(row["cik_str"]).zfill(10),
            "company": row["title"],
        }
        for row in raw.values()
    }

def resolve_ticker(ticker):
    ticker = ticker.upper().strip()
    m = ticker_map()
    if ticker not in m:
        raise SECError(f"Ticker '{ticker}' was not found in the SEC ticker list.")
    return {"ticker": ticker, **m[ticker]}

@lru_cache(maxsize=64)
def company_facts(cik):
    return _get_json(FACTS_URL.format(cik=cik))

@lru_cache(maxsize=64)
def submissions(cik):
    return _get_json(SUBMISSIONS_URL.format(cik=cik))

def _rows(payload, concept):
    node = payload.get("facts", {}).get("us-gaap", {}).get(concept, {})
    return node.get("units", {}).get("USD", [])

def _latest(payload, concepts):
    for concept in concepts:
        rows = [r for r in _rows(payload, concept)
                if r.get("val") is not None and r.get("form") in {"10-K","10-Q"}]
        if rows:
            rows.sort(key=lambda r: (r.get("filed",""), r.get("end","")), reverse=True)
            r = rows[0]
            return float(r["val"]), r.get("end"), concept
    return None, None, None

def latest_financial_snapshot(ticker):
    meta = resolve_ticker(ticker)
    payload = company_facts(meta["cik"])
    result = {"ticker": meta["ticker"], "company": meta["company"], "cik": meta["cik"]}
    periods = []
    for key, concepts in CORE_CONCEPTS.items():
        value, end, concept = _latest(payload, concepts)
        result[key] = value
        result[f"{key}_concept"] = concept
        if end:
            periods.append(end)
    result["period"] = max(periods) if periods else None
    return result
def _concept_rows(payload: dict, concept: str):
    """
    Return SEC XBRL rows for a given US-GAAP concept.
    """

    facts = payload.get("facts", {}).get("us-gaap", {})
    node = facts.get(concept, {})
    units = node.get("units", {})

    rows = units.get("USD")

    if rows is None:
        return []

    return rows

def concept_history(ticker: str, key: str, max_points: int = 12) -> dict:
    """
    Returns comparable SEC financial observations separated by reporting scope.

    Duration-based concepts such as revenue are split into:
    - quarterly: roughly 70-110 days
    - annual: roughly 300-390 days

    Instant concepts such as cash/assets are treated as point-in-time observations.
    """

    meta = resolve_ticker(ticker)
    payload = company_facts(meta["cik"])
    concepts = CORE_CONCEPTS[key]

    rows = []
    concept_used = None

    for concept in concepts:
        candidate_rows = _concept_rows(payload, concept)

        valid = [
            r for r in candidate_rows
            if r.get("val") is not None
            and r.get("form") in {"10-K", "10-Q"}
            and r.get("end")
        ]

        if valid:
            rows = valid
            concept_used = concept
            break

    empty = pd.DataFrame(
        columns=[
            "start",
            "end",
            "filed",
            "form",
            "fy",
            "fp",
            "value",
            "concept",
            "duration_days",
        ]
    )

    if not rows:
        return {
            "annual": empty.copy(),
            "quarterly": empty.copy(),
            "instant": empty.copy(),
            "concept": None,
        }

    df = pd.DataFrame(rows)

    for col in ["start", "end", "filed"]:
        if col not in df.columns:
            df[col] = None
        df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in ["fy", "fp", "form"]:
        if col not in df.columns:
            df[col] = None

    df["value"] = pd.to_numeric(df["val"], errors="coerce")
    df["concept"] = concept_used

    # Calculate reporting-period length.
    df["duration_days"] = (df["end"] - df["start"]).dt.days

    df = df.dropna(subset=["end", "value"])

    # Later filings frequently repeat earlier facts.
    # Keep the most recently filed version of each fact.
    df = (
        df.sort_values(["end", "filed"])
        .drop_duplicates(
            subset=["start", "end", "form", "fy", "fp"],
            keep="last",
        )
    )

    # -------------------------
    # POINT-IN-TIME CONCEPTS
    # -------------------------
    instant = df[df["start"].isna()].copy()

    instant = (
        instant.sort_values(["end", "filed"])
        .drop_duplicates(subset=["end"], keep="last")
        .sort_values("end")
        .tail(max_points)
        .reset_index(drop=True)
    )

    # -------------------------
    # QUARTERLY FLOW CONCEPTS
    # -------------------------
    # Approximately one quarter.
    quarterly = df[
        df["duration_days"].between(70, 110, inclusive="both")
    ].copy()

    quarterly = (
        quarterly.sort_values(["end", "filed"])
        .drop_duplicates(subset=["end"], keep="last")
        .sort_values("end")
        .tail(max_points)
        .reset_index(drop=True)
    )

    # -------------------------
    # ANNUAL FLOW CONCEPTS
    # -------------------------
    # Approximately one fiscal year.
    annual = df[
        df["duration_days"].between(300, 390, inclusive="both")
    ].copy()

    annual = (
        annual.sort_values(["end", "filed"])
        .drop_duplicates(subset=["end"], keep="last")
        .sort_values("end")
        .tail(max_points)
        .reset_index(drop=True)
    )

    columns = [
        "start",
        "end",
        "filed",
        "form",
        "fy",
        "fp",
        "value",
        "concept",
        "duration_days",
    ]

    def clean(frame):
        if frame.empty:
            return empty.copy()

        available = [c for c in columns if c in frame.columns]
        return frame[available].copy()

    return {
        "annual": clean(annual),
        "quarterly": clean(quarterly),
        "instant": clean(instant),
        "concept": concept_used,
    }

def latest_filings(ticker, forms=("10-K","10-Q"), limit=8):
    meta = resolve_ticker(ticker)
    recent = submissions(meta["cik"]).get("filings", {}).get("recent", {})
    if not recent:
        return pd.DataFrame()
    df = pd.DataFrame(recent)
    df = df[df["form"].isin(forms)].copy()
    cols = [c for c in ["accessionNumber","filingDate","reportDate","form","primaryDocument"] if c in df.columns]
    return df[cols].head(limit).reset_index(drop=True)
