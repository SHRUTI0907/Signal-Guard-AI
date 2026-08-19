import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "SignalGuard AI"
APP_SUBTITLE = "Corporate Distress & Early-Warning Intelligence"
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "SignalGuard-AI-Portfolio your-email@example.com")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

CORE_CONCEPTS = {
    "assets": ["Assets"],
    "current_assets": ["AssetsCurrent"],
    "current_liabilities": ["LiabilitiesCurrent"],
    "liabilities": ["Liabilities"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet", "Revenues"],
    "operating_income": ["OperatingIncomeLoss"],
    "interest_expense": ["InterestExpenseNonOperating", "InterestAndDebtExpense"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "stockholders_equity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
}
