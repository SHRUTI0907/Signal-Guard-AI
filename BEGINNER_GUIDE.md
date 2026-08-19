# SignalGuard AI — Beginner Step-by-Step Guide

## 1. Software
**Python** runs the code.  
**VS Code** is your code editor.  
**Git** tracks code changes.  
**GitHub** hosts the project for recruiters.  
**Streamlit** turns Python into the web app.  
**SEC EDGAR** supplies public U.S. filing and XBRL data.  
**OpenAI API** is optional and powers only the analyst-writing layer.

## 2. Folder map
`app.py` — visible web product  
`config.py` — project settings  
`data/sec_client.py` — SEC structured data  
`data/filing_client.py` — filing download/cleaning  
`analytics/financials.py` — financial ratios  
`analytics/risk_engine.py` — transparent score  
`analytics/trends.py` — time-series charts  
`analytics/scenario.py` — stress testing  
`ai/retrieval.py` — filing evidence retrieval  
`ai/analyst.py` — AI memo / fallback  
`tests/` — automated checks

## 3. First run
1. Install Python 3.11 or 3.12.
2. Install VS Code.
3. Install Git.
4. Extract this ZIP.
5. VS Code → File → Open Folder → select `ai-corporate-distress-agent`.
6. VS Code → Terminal → New Terminal.
7. Run `python -m venv .venv`.
8. Run `.venv\Scripts\Activate.ps1`.
9. Run `pip install -r requirements.txt`.
10. Set your SEC identity:
   `$env:SEC_USER_AGENT="SignalGuard-AI-Portfolio your-real-email@example.com"`
11. Run `streamlit run app.py`.
12. Test AAPL first.

Do not configure OpenAI yet. Make the base app work first.

## 4. What happens when you click Analyze
1. Ticker is converted to SEC CIK.
2. Company Facts JSON is downloaded.
3. Standard financial facts are extracted.
4. Ratios are calculated.
5. Five risk components are scored.
6. Trend data is prepared.
7. Latest 10-Q/10-K is downloaded.
8. Filing is split into chunks.
9. TF-IDF ranks the most risk-relevant passages.
10. The analyst brief is generated.
11. Scenario sliders allow stress testing.

## 5. Add AI only after the base works
Set:
`$env:OPENAI_API_KEY="your-key"`
Then restart Streamlit. Never commit API keys.

## 6. GitHub
Create a repository called `signalguard-ai`, then:
```powershell
git init
git add .
git commit -m "Build SignalGuard AI MVP"
git branch -M main
```
GitHub will show the final commands for connecting and pushing your new repository.

## 7. Deploy with Streamlit Community Cloud
1. Sign in to Streamlit Community Cloud.
2. Connect GitHub.
3. Select your `signalguard-ai` repository.
4. Choose `app.py`.
5. Add secrets in Advanced Settings.
6. Deploy.
7. Test the public URL.

## 8. Recruiter presentation
Show one strong screenshot, the product flow, business problem, stack, methodology, limitations,
GitHub link, and live demo link.

## 9. Interview explanation
“I built an evidence-grounded corporate early-warning system combining SEC XBRL data,
interpretable financial risk screening, filing-text retrieval, optional LLM analysis and interactive
stress testing. I intentionally keep the MVP score transparent rather than calling it a bankruptcy
probability until a point-in-time labeled distress dataset is added.”
