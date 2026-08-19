from __future__ import annotations

from typing import List
from google import genai
from analytics.risk_engine import build_rule_summary
from config import GEMINI_API_KEY, GEMINI_MODEL


def _evidence_text(evidence: List[dict]) -> str:
    if not evidence:
        return "No SEC filing evidence was retrieved."
    parts = []
    for e in evidence:
        excerpt = e.get("excerpt", "")[:1300]
        parts.append(
            f"[Evidence {e['rank']}] | Section: {e.get('section','Filing excerpt')} | "
            f"Retrieval stance: {e.get('stance','Neutral')}\n{excerpt}"
        )
    return "\n\n".join(parts)


def deterministic_brief(company: str, result: dict, evidence: List[dict]) -> str:
    base = build_rule_summary(company, result)
    if evidence:
        return base + (
            "\n\nSEC filing intelligence identified passages relevant to financial-risk topics. "
            "Retrieval relevance and stance labels are screening aids, not proof of distress; review the source evidence directly."
        )
    return base


def generate_ai_brief(company: str, ticker: str, result: dict, evidence: List[dict]) -> dict:
    if not GEMINI_API_KEY:
        return {"mode": "Evidence-based fallback", "text": deterministic_brief(company, result, evidence)}

    component_text = "\n".join(
        f"- {item['component']} ({item.get('signal_type','snapshot')}): {item['reason']} "
        f"(risk points {item['risk_points']}/{item['max_points']})"
        for item in result["components"]
    )
    evidence_text = _evidence_text(evidence)

    prompt = f"""
You are a cautious corporate early-warning analyst. Use ONLY the supplied screening outputs and SEC excerpts.

COMPANY: {company} ({ticker})
SCREENING SCORE: {result['score']}/100
SCREENING BAND: {result['label']}
DATA COVERAGE: {result['coverage']}/5 snapshot indicators; {result.get('trend_coverage',0)} trend signals

QUANTITATIVE SIGNALS
{component_text}

SEC FILING EVIDENCE
{evidence_text}

NON-NEGOTIABLE RULES
- The score is NOT a bankruptcy probability, credit rating, investment recommendation, or proof of overall financial health.
- Say "the screening framework identifies" rather than claiming the company is objectively safe/healthy/distressed.
- Do not infer insolvency, default, fraud, going-concern risk, or covenant breach unless the supplied excerpt explicitly supports it.
- Debt issuance/repayment and financing activity alone are neutral unless context makes them adverse/supportive.
- Retrieval stance labels are heuristic metadata; independently interpret the actual excerpt.
- Cite every filing-derived statement with [Evidence #]. If no excerpt supports a claim, do not make it.
- If evidence is mixed or inconclusive, say so.
- Keep the memo concise and decision-oriented.

Use exactly these headings:
## Risk Assessment
## Key Quantitative Drivers
## SEC Filing Evidence
## Analyst Interpretation
## What to Monitor Next
## Limitations
"""

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        text = response.text
        if not text:
            raise ValueError("Gemini returned an empty response.")
        return {"mode": f"Gemini · {GEMINI_MODEL}", "text": text}
    except Exception as exc:
        return {
            "mode": "Fallback — Gemini unavailable",
            "text": deterministic_brief(company, result, evidence) + f"\n\nAI service note: {type(exc).__name__}.",
        }


def generate_scenario_brief(company: str, ticker: str, base_result: dict, scenario: dict, assumptions: dict) -> dict:
    impacts = scenario.get("impacts", [])
    impact_text = "\n".join(
        f"- {x['component']}: {x['before']:.0f} -> {x['after']:.0f} risk points (delta {x['delta']:+.0f})"
        for x in impacts
    ) or "- No component crossed a scoring threshold under this scenario."
    fallback = (
        f"The scenario moves the screening score from {base_result['score']} to {scenario['result']['score']} "
        f"and the band from {base_result['label']} to {scenario['result']['label']}. "
        f"Largest threshold effects: {impact_text.replace(chr(10), '; ')}"
    )
    if not GEMINI_API_KEY:
        return {"mode": "Deterministic scenario summary", "text": fallback}

    prompt = f"""
You are explaining a hypothetical corporate stress test for {company} ({ticker}).
This is scenario analysis, not a forecast.
Assumptions: {assumptions}
Base screening: {base_result['score']}/100 ({base_result['label']})
Stressed screening: {scenario['result']['score']}/100 ({scenario['result']['label']})
Component threshold changes:
{impact_text}

Write 3 short paragraphs: (1) what changed, (2) which assumptions/components matter most, (3) what an analyst should validate next.
Do not call this a bankruptcy probability, prediction, credit rating, or investment recommendation.
"""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return {"mode": f"Gemini · {GEMINI_MODEL}", "text": response.text or fallback}
    except Exception:
        return {"mode": "Deterministic scenario summary", "text": fallback}
