import pandas as pd
from ai.retrieval import classify_evidence, retrieve_evidence
from analytics.risk_engine import score_snapshot
from analytics.scenario import apply_stress

S = {"current_assets": 120.0, "current_liabilities": 100.0, "liabilities": 650.0,
     "assets": 1000.0, "cash": 100.0, "operating_cash_flow": 90.0,
     "operating_income": 150.0, "interest_expense": 30.0, "revenue": 1000.0,
     "net_income": 100.0}


def frame(a, b):
    return pd.DataFrame({"value": [a, b]})


def test_trend_overlay_adds_deterioration_signal():
    trends = {
        "revenue": {"quarterly": frame(100, 75), "annual": pd.DataFrame(), "instant": pd.DataFrame()},
        "operating_income": {"quarterly": pd.DataFrame(), "annual": pd.DataFrame(), "instant": pd.DataFrame()},
        "operating_cash_flow": {"quarterly": pd.DataFrame(), "annual": pd.DataFrame(), "instant": pd.DataFrame()},
        "cash": {"quarterly": pd.DataFrame(), "annual": pd.DataFrame(), "instant": pd.DataFrame()},
        "liabilities": {"quarterly": pd.DataFrame(), "annual": pd.DataFrame(), "instant": pd.DataFrame()},
    }
    result = score_snapshot(S, trends=trends)
    assert result["trend_coverage"] == 1
    assert any(x["component"] == "Revenue Trend" for x in result["trend_components"])


def test_evidence_stance_and_metadata():
    assert classify_evidence("The company has sufficient liquidity and available liquidity.") == "Supportive"
    text = ("ordinary operations " * 100) + ("liquidity pressure and refinancing risk caused a shortfall " * 80)
    out = retrieve_evidence(text, query="liquidity refinancing risk", top_k=1)
    assert out[0]["stance"] == "Adverse"
    assert "section" in out[0]


def test_scenario_reports_component_impacts():
    out = apply_stress(S, cash_drop_pct=80, current_liabilities_increase_pct=80)
    assert out["result"]["score"] >= out["base_result"]["score"]
    assert isinstance(out["impacts"], list)
