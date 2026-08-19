from copy import deepcopy
from analytics.risk_engine import score_snapshot


def apply_stress(snapshot, revenue_drop_pct=0, operating_income_drop_pct=0,
                 cash_drop_pct=0, current_liabilities_increase_pct=0, trends=None):
    s = deepcopy(snapshot)
    if s.get("revenue") is not None:
        s["revenue"] *= max(0, 1 - revenue_drop_pct / 100)
    if s.get("operating_income") is not None:
        s["operating_income"] *= 1 - operating_income_drop_pct / 100
    if s.get("cash") is not None:
        s["cash"] *= max(0, 1 - cash_drop_pct / 100)
    if s.get("current_liabilities") is not None:
        s["current_liabilities"] *= 1 + current_liabilities_increase_pct / 100

    result = score_snapshot(s, trends=trends)
    base = score_snapshot(snapshot, trends=trends)
    base_map = {x["component"]: x for x in base["snapshot_components"]}
    stressed_map = {x["component"]: x for x in result["snapshot_components"]}
    impacts = []
    for name in sorted(set(base_map) | set(stressed_map)):
        before = base_map.get(name, {}).get("risk_points", 0.0)
        after = stressed_map.get(name, {}).get("risk_points", 0.0)
        delta = after - before
        if delta != 0:
            impacts.append({"component": name, "before": before, "after": after, "delta": delta})
    impacts.sort(key=lambda x: abs(x["delta"]), reverse=True)

    return {"snapshot": s, "result": result, "base_result": base, "impacts": impacts}
