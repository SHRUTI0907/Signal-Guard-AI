def safe_div(a, b):
    if a is None or b in (None, 0):
        return None
    return a / b

def derive_metrics(s):
    interest = s.get("interest_expense")
    op = s.get("operating_income")
    coverage = None if interest in (None,0) or op is None else op / abs(interest)
    return {
        "current_ratio": safe_div(s.get("current_assets"), s.get("current_liabilities")),
        "liabilities_to_assets": safe_div(s.get("liabilities"), s.get("assets")),
        "cash_to_current_liabilities": safe_div(s.get("cash"), s.get("current_liabilities")),
        "operating_cash_flow_to_assets": safe_div(s.get("operating_cash_flow"), s.get("assets")),
        "operating_margin": safe_div(s.get("operating_income"), s.get("revenue")),
        "net_margin": safe_div(s.get("net_income"), s.get("revenue")),
        "interest_coverage": coverage,
    }
