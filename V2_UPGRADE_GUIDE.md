# SignalGuard AI V2 — Upgrade Guide

## What changed

1. **Risk Engine 2.0** — keeps the transparent five snapshot indicators and adds small comparable-period deterioration signals when SEC history supports them.
2. **Filing Intelligence 2.0** — smaller evidence chunks, hybrid word/character TF-IDF retrieval, section metadata, and heuristic Adverse/Neutral/Supportive triage.
3. **AI Analyst 2.0** — stricter Gemini grounding prompt that avoids calling the score a bankruptcy probability, credit rating, or proof of financial health.
4. **Scenario Intelligence** — shows which scoring components changed under stress and can generate a short Gemini scenario explanation.
5. **UI modernization** — risk gauge, signal cards, expanded coverage metrics, and replacement of deprecated `use_container_width` calls.

## Run locally

1. Copy your existing private `.env` into the project root. Never commit it.
2. Activate your virtual environment.
3. Install/update packages: `python -m pip install -r requirements.txt`
4. Run tests: `python -m pytest`
5. Start: `python -m streamlit run app.py`

## Expected test result

`7 passed`

## Important methodology language

SignalGuard is a transparent **early-warning screening system**. Its score is not a bankruptcy probability, validated credit rating, lending decision, or investment recommendation. Evidence stance labels are heuristic triage and must be checked against the source excerpt.
