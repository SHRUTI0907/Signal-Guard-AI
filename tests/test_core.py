from analytics.financials import derive_metrics
from analytics.risk_engine import score_snapshot
from analytics.scenario import apply_stress

S={"current_assets":80.0,"current_liabilities":100.0,"liabilities":900.0,
   "assets":1000.0,"cash":20.0,"operating_cash_flow":-10.0,
   "operating_income":8.0,"interest_expense":10.0,"revenue":100.0,"net_income":-2.0}

def test_metrics():
    m=derive_metrics(S)
    assert round(m["current_ratio"],2)==0.80
    assert round(m["liabilities_to_assets"],2)==0.90

def test_risk():
    r=score_snapshot(S)
    assert r["score"]>=60

def test_stress():
    base=score_snapshot(S)
    stressed=apply_stress(S,cash_drop_pct=50,current_liabilities_increase_pct=50)["result"]
    assert stressed["score"]>=base["score"]
