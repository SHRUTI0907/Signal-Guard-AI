from __future__ import annotations

from analytics.financials import derive_metrics

BASE_MAX = 20.0
TREND_MAX = 10.0


def _part(name, points, reason, value, max_points=BASE_MAX, signal_type="snapshot"):
    return {
        "component": name,
        "risk_points": float(points),
        "max_points": float(max_points),
        "reason": reason,
        "value": value,
        "signal_type": signal_type,
    }


def _pct_change(frame):
    if frame is None or len(frame) < 2:
        return None
    prev = float(frame.iloc[-2]["value"])
    latest = float(frame.iloc[-1]["value"])
    if prev == 0:
        return None
    return (latest - prev) / abs(prev)


def _best_series(bundle):
    """Prefer comparable quarterly data, then annual, then point-in-time."""
    for key in ("quarterly", "annual", "instant"):
        frame = bundle.get(key)
        if frame is not None and len(frame) >= 2:
            return frame, key
    return None, None


def trend_risk_components(trends):
    """Create small, transparent deterioration signals from comparable SEC series."""
    if not trends:
        return []

    components = []
    specs = [
        ("revenue", "Revenue Trend", False),
        ("operating_income", "Operating Income Trend", False),
        ("operating_cash_flow", "Cash Flow Trend", False),
        ("cash", "Cash Balance Trend", False),
        ("liabilities", "Liabilities Trend", True),
    ]

    for key, name, higher_is_riskier in specs:
        bundle = trends.get(key, {})
        frame, scope = _best_series(bundle)
        change = _pct_change(frame)
        if change is None:
            continue

        risk_change = change if higher_is_riskier else -change
        if risk_change >= 0.25:
            pts, severity = 10, "sharp deterioration"
        elif risk_change >= 0.10:
            pts, severity = 7, "meaningful deterioration"
        elif risk_change >= 0.03:
            pts, severity = 4, "mild deterioration"
        elif risk_change > -0.03:
            pts, severity = 2, "broadly stable"
        else:
            pts, severity = 0, "improvement"

        direction = "increase" if change >= 0 else "decline"
        components.append(
            _part(
                name,
                pts,
                f"Latest comparable {scope} observation shows a {abs(change):.1%} {direction}; this is classified as {severity}.",
                change,
                max_points=TREND_MAX,
                signal_type="trend",
            )
        )

    return components


def score_snapshot(s, trends=None):
    m = derive_metrics(s)
    p = []

    cr = m["current_ratio"]
    if cr is not None:
        p.append(_part(
            "Liquidity",
            20 if cr < .8 else 16 if cr < 1 else 8 if cr < 1.5 else 2,
            "Current ratio indicates " + ("severe pressure." if cr < .8 else "weak liquidity." if cr < 1 else "moderate liquidity." if cr < 1.5 else "a stronger liquidity cushion."),
            cr,
        ))

    lev = m["liabilities_to_assets"]
    if lev is not None:
        p.append(_part(
            "Leverage",
            20 if lev > .9 else 15 if lev > .75 else 9 if lev > .6 else 3,
            "Balance-sheet leverage is " + ("very high." if lev > .9 else "elevated." if lev > .75 else "worth monitoring." if lev > .6 else "relatively contained."),
            lev,
        ))

    ic = m["interest_coverage"]
    if ic is not None:
        p.append(_part(
            "Debt Service",
            20 if ic < 1 else 17 if ic < 1.5 else 9 if ic < 3 else 2,
            "Interest coverage is " + ("below 1x." if ic < 1 else "weak." if ic < 1.5 else "moderate." if ic < 3 else "stronger."),
            ic,
        ))

    ocfa = m["operating_cash_flow_to_assets"]
    ocf = s.get("operating_cash_flow")
    if ocfa is not None:
        pts = 20 if ocf is not None and ocf < 0 else 14 if ocfa < .03 else 7 if ocfa < .08 else 2
        p.append(_part(
            "Cash Flow",
            pts,
            "Operating cash generation is " + ("negative." if ocf is not None and ocf < 0 else "weak." if ocfa < .03 else "moderate." if ocfa < .08 else "stronger."),
            ocfa,
        ))

    margin = m["operating_margin"]
    if margin is not None:
        p.append(_part(
            "Profitability",
            20 if margin < 0 else 13 if margin < .05 else 7 if margin < .12 else 2,
            "Operating profitability is " + ("negative." if margin < 0 else "thin." if margin < .05 else "moderate." if margin < .12 else "stronger."),
            margin,
        ))

    snapshot_components = list(p)
    trend_components = trend_risk_components(trends)
    p.extend(trend_components)

    max_available = sum(x["max_points"] for x in p)
    score = round(sum(x["risk_points"] for x in p) / max_available * 100) if max_available else 0
    label = "High" if score >= 65 else "Medium" if score >= 35 else "Low"
    p = sorted(p, key=lambda x: x["risk_points"] / x["max_points"], reverse=True)

    return {
        "score": score,
        "label": label,
        "components": p,
        "snapshot_components": snapshot_components,
        "trend_components": trend_components,
        "metrics": m,
        "coverage": len(snapshot_components),
        "trend_coverage": len(trend_components),
        "max_available_points": max_available,
    }


def build_rule_summary(company, result):
    drivers = "; ".join(x["reason"] for x in result["components"][:3])
    return (
        f"{company} receives a {result['label'].lower()} early-warning screening score "
        f"of {result['score']}/100. The current screening framework's main signals are: {drivers} "
        "This is a transparent screening score, not a bankruptcy probability, credit rating, or investment recommendation."
    )
