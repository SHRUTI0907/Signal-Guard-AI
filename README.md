# SignalGuard AI — Corporate Distress & Early-Warning Intelligence

A portfolio-grade decision-support application combining structured SEC financial data,
transparent risk analytics, filing-text retrieval, optional LLM analysis, and scenario stress testing.

**Business question:** Is a company showing signs of financial deterioration, which signals are
driving the warning, what filing evidence is relevant, and how sensitive is the profile to stress?

## Product flow
Ticker → SEC Company Facts → Financial Features → Early-Warning Engine → SEC Filing →
Evidence Retrieval → AI Analyst Brief → Scenario Stress Lab

## Features
- Live U.S. public-company lookup
- SEC XBRL financial facts
- Liquidity, leverage, debt-service, profitability and cash-flow features
- Transparent 0–100 screening score
- Risk-driver contribution view
- Historical trend charts
- Latest 10-K/10-Q retrieval
- Local TF-IDF evidence retrieval
- Optional OpenAI memo with no-key fallback
- Stress-test sliders
- Unit tests
- Streamlit deployment-ready

## Run locally
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SEC_USER_AGENT="SignalGuard-AI-Portfolio your-real-email@example.com"
streamlit run app.py
```

Optional AI:
```powershell
$env:OPENAI_API_KEY="your-key"
```

Tests:
```powershell
pytest
```

## Important limitation
The current 0–100 result is a transparent early-warning screening score. It is not a bankruptcy
probability or validated credit rating. A true supervised ML layer requires point-in-time historical
features, defensible distress labels, time-aware validation, calibration and model governance.
