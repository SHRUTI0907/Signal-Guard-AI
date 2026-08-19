from __future__ import annotations

import pandas as pd

from data.sec_client import concept_history


TREND_KEYS = [
    ("revenue", "Revenue"),
    ("operating_income", "Operating Income"),
    ("operating_cash_flow", "Operating Cash Flow"),
    ("cash", "Cash"),
    ("liabilities", "Liabilities"),
]


def trend_bundle(ticker: str, max_points: int = 10) -> dict:
    """
    Build normalized trend datasets.

    Flow variables:
        Revenue
        Operating Income
        Operating Cash Flow

    can contain annual and quarterly reporting periods.

    Balance-sheet variables:
        Cash
        Liabilities

    are point-in-time values.
    """

    output = {}

    for key, label in TREND_KEYS:

        history = concept_history(
            ticker,
            key,
            max_points=max_points,
        )

        output[key] = {
            "label": label,
            "annual": history["annual"],
            "quarterly": history["quarterly"],
            "instant": history["instant"],
            "concept": history["concept"],
        }

    return output


def latest_direction(df: pd.DataFrame):
    """
    Calculate percentage movement between the latest
    two comparable reporting observations.
    """

    if df is None or len(df) < 2:
        return None

    previous = float(df.iloc[-2]["value"])
    latest = float(df.iloc[-1]["value"])

    if previous == 0:
        return None

    return (latest - previous) / abs(previous)