from functools import lru_cache
import re
import requests
from bs4 import BeautifulSoup
from config import SEC_USER_AGENT
from data.sec_client import latest_filings, resolve_ticker, SECError

HEADERS = {"User-Agent": SEC_USER_AGENT, "Accept-Encoding": "gzip, deflate"}

def filing_url(cik, accession_number, primary_document):
    return (
        f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
        f"{accession_number.replace('-','')}/{primary_document}"
    )

@lru_cache(maxsize=64)
def fetch_filing_text(ticker, form="10-Q"):
    meta = resolve_ticker(ticker)
    df = latest_filings(ticker, forms=(form,), limit=1)
    if df.empty:
        df = latest_filings(ticker, forms=("10-K","10-Q"), limit=1)
    if df.empty:
        raise SECError(f"No recent 10-K/10-Q found for {ticker}.")
    row = df.iloc[0].to_dict()
    url = filing_url(meta["cik"], row["accessionNumber"], row["primaryDocument"])
    try:
        r = requests.get(url, headers=HEADERS, timeout=45)
        r.raise_for_status()
    except requests.RequestException as exc:
        raise SECError(f"Could not download filing: {exc}") from exc
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script","style","noscript"]):
        tag.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    return {"ticker":ticker.upper(), "form":row.get("form"),
            "filing_date":row.get("filingDate"), "report_date":row.get("reportDate"),
            "url":url, "text":text}
