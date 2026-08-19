# SignalGuard AI

### Corporate Distress & Early-Warning Intelligence

SignalGuard AI is an AI-powered financial analytics application that uses public SEC data to identify early signs of corporate financial deterioration and explain the factors driving the risk.

### 🚀 [Try the Live Application](https://signalguard-ai.streamlit.app)

---

## What It Does

Enter a U.S. public-company ticker such as `AAPL`, `MSFT`, `F`, or `UAL`.

SignalGuard automatically:

- Retrieves financial data from SEC EDGAR
- Analyzes liquidity, leverage, profitability, cash flow, and financial trends
- Generates an explainable **Early-Warning Score**
- Retrieves relevant evidence from 10-K / 10-Q filings
- Uses **Google Gemini** to generate an evidence-grounded analyst brief
- Lets users stress-test the company under adverse financial scenarios

---

## How It Works

```text
Company Ticker
      ↓
SEC Financial Data
      ↓
Risk + Trend Analysis
      ↓
SEC Filing Evidence
      ↓
Gemini AI Analyst
      ↓
Scenario Stress Testing
```

---

## Tech Stack

**Python · Streamlit · Pandas · Plotly · SEC EDGAR/XBRL · TF-IDF · Google Gemini API · pytest**

---

## Why I Built It

Financial warning signs are often scattered across financial statements, historical trends, and lengthy regulatory filings.

SignalGuard brings these signals together into one explainable workflow to answer:

**What is changing? What is driving the risk? What evidence supports it? What could happen under stress?**

---

## Important Note

SignalGuard is an educational early-warning screening tool developed as a portfolio project. Its score is **not** a bankruptcy probability, credit rating, investment recommendation, or lending decision.

---

## Links

🚀 **[Live Demo](https://signalguard-ai.streamlit.app)**  
💻 **[Source Code](https://github.com/SHRUTI0907/Signal-Guard-AI)**
