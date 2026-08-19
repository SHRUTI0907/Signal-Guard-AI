import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ai.analyst import generate_ai_brief, generate_scenario_brief
from ai.retrieval import retrieve_evidence
from analytics.risk_engine import score_snapshot
from analytics.scenario import apply_stress
from analytics.trends import trend_bundle, latest_direction
from data.filing_client import fetch_filing_text
from data.sec_client import latest_financial_snapshot
from ui.style import inject_css

st.set_page_config(page_title="SignalGuard AI", page_icon="◈", layout="wide")
inject_css(st)

st.markdown("""<div class="hero"><div class="eyebrow">MASTER'S PORTFOLIO · AI + FINANCIAL ANALYTICS</div>
<h1>SignalGuard AI</h1><div class="hero-sub">Corporate Distress & Early-Warning Intelligence</div>
<div class="small-note">Turn public SEC data into an explainable risk screen, filing evidence, an AI analyst brief, and scenario-based decision support.</div></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Analyze a company")
    ticker = st.text_input("U.S. public-company ticker", value="AAPL").strip().upper()
    form = st.selectbox("Filing for text intelligence", ["10-Q", "10-K"])
    analyze = st.button("Run Early-Warning Analysis", type="primary", width="stretch")
    st.markdown("---")
    st.caption("Portfolio demonstration · U.S. public companies · SEC data")

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "scenario_brief" not in st.session_state:
    st.session_state.scenario_brief = None

if analyze:
    try:
        with st.spinner("Building SEC financial intelligence..."):
            snap = latest_financial_snapshot(ticker)
            trends = trend_bundle(ticker)
            risk = score_snapshot(snap, trends=trends)
        filing = None
        evidence = []
        filing_error = None
        try:
            with st.spinner("Retrieving SEC filing evidence..."):
                filing = fetch_filing_text(ticker, form)
                evidence = retrieve_evidence(filing["text"], top_k=5)
        except Exception as exc:
            filing_error = str(exc)
        with st.spinner("Preparing grounded analyst brief..."):
            brief = generate_ai_brief(snap["company"], ticker, risk, evidence)
        st.session_state.analysis = {
            "snapshot": snap, "risk": risk, "trends": trends, "filing": filing,
            "evidence": evidence, "filing_error": filing_error, "brief": brief,
        }
        st.session_state.scenario_brief = None
    except Exception as exc:
        st.error("Analysis failed.")
        st.code(str(exc))

d = st.session_state.analysis
if not d:
    st.info("Enter a ticker and run the analysis. Try **AAPL**, **MSFT**, **F**, or **UAL**.")
    st.stop()

snap = d["snapshot"]
risk = d["risk"]

st.markdown(
    '<div class="section-kicker">Company intelligence</div>',
    unsafe_allow_html=True,
)
st.subheader(f"{snap['company']} · {snap['ticker']}")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Early-Warning Score", f"{risk['score']}/100")
c2.metric("Risk Band", risk["label"])
c3.metric("Snapshot Coverage", f"{risk['coverage']}/5")
c4.metric("Trend Signals", risk.get("trend_coverage", 0))
c5.metric("Latest SEC Period", snap.get("period") or "N/A")
st.caption("A transparent screening score based on current financial indicators and comparable-period trends.")

tabs = st.tabs(["Executive Snapshot", "Financial Trends", "Filing Intelligence", "AI Analyst", "Scenario Lab", "Methodology"])

with tabs[0]:
    left, right = st.columns([1, 1.25])
    with left:
        st.markdown("### Risk gauge")
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=risk["score"], number={"suffix": "/100"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"thickness": 0.28},
                   "steps": [{"range": [0, 35]}, {"range": [35, 65]}, {"range": [65, 100]}]},
        ))
        gauge.update_layout(height=285, margin=dict(l=25, r=25, t=25, b=10))
        st.plotly_chart(gauge, width="stretch")
        st.caption("Screening score only — not a bankruptcy probability or credit rating.")
    with right:
        st.markdown("### Highest-priority signals")
        for item in risk["components"][:5]:
            kind = "Trend" if item.get("signal_type") == "trend" else "Snapshot"
            st.markdown(f"**{item['component']} · {kind} · {item['risk_points']:.0f}/{item['max_points']:.0f}**")
            st.caption(item["reason"])

    st.markdown("### Explainable risk drivers")
    drivers = pd.DataFrame([{
        "Signal": x["component"], "Type": x.get("signal_type", "snapshot").title(),
        "Risk Points": x["risk_points"], "Maximum": x["max_points"], "Reason": x["reason"]
    } for x in risk["components"]])
    if not drivers.empty:
        st.dataframe(drivers, width="stretch", hide_index=True)
        fig = px.bar(drivers, x="Risk Points", y="Signal", color="Type", orientation="h",
                     title="Contribution to Current Screening Score")
        fig.update_layout(height=380, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="stretch")

    labels = {"current_ratio": "Current Ratio", "liabilities_to_assets": "Liabilities / Assets",
              "cash_to_current_liabilities": "Cash / Current Liabilities",
              "operating_cash_flow_to_assets": "Operating Cash Flow / Assets",
              "operating_margin": "Operating Margin", "net_margin": "Net Margin",
              "interest_coverage": "Interest Coverage"}
    st.markdown("### Key financial ratios")
    st.dataframe(pd.DataFrame([{"Metric": label, "Value": None if risk["metrics"].get(k) is None
        else round(risk["metrics"][k], 4)} for k, label in labels.items()]), width="stretch", hide_index=True)

with tabs[1]:
    st.markdown("### Financial Trend Intelligence")
    st.caption("Reporting periods are normalized before comparison: quarterly with quarterly, annual with annual, and balance-sheet metrics as point-in-time observations.")
    for key, bundle in d["trends"].items():
        label = bundle["label"]
        st.markdown("---")
        st.markdown(f"### {label}")
        for scope_key, scope_label, x_label in [
            ("instant", "Point-in-Time Trend", "Reporting Date"),
            ("quarterly", "Quarterly Trend", "Quarter End"),
            ("annual", "Annual Trend", "Fiscal Year End"),
        ]:
            frame = bundle[scope_key]
            if frame.empty:
                continue
            direction = latest_direction(frame)
            direction_text = "Change unavailable" if direction is None else f"{direction:+.1%} vs prior comparable observation"
            st.markdown(f"**{scope_label} · {direction_text}**")
            plot_df = frame.copy()
            fig = px.line(plot_df, x="end", y="value", markers=True)
            fig.update_layout(xaxis_title=x_label, yaxis_title="Reported Value", height=290,
                              margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig, width="stretch")

with tabs[2]:
    st.markdown("### SEC Filing Intelligence")
    if d["filing_error"]:
        st.warning(d["filing_error"])
    elif d["filing"]:
        f = d["filing"]
        st.write(f"Using **{f['form']}** filed **{f['filing_date']}** (report date {f['report_date']}).")
        st.caption("Search the latest SEC filing for passages related to liquidity, debt, cash flow, financing, and other risk topics. Evidence labels are screening aids, not conclusions.")
        q = st.text_input("Investigate another filing topic", value="liquidity debt refinancing covenant cash flow financing risk")
        evidence_now = retrieve_evidence(f["text"], query=q, top_k=5)
        for e in evidence_now:
            badge = {"Adverse": "🔺", "Supportive": "✓", "Neutral": "•"}.get(e["stance"], "•")
            with st.expander(f"{badge} Evidence {e['rank']} · {e['stance']} · {e['section']} · relevance {e['score']:.3f}"):
                st.write(e["excerpt"])
                st.caption("Read the source excerpt directly; the stance label is only a screening heuristic.")
        st.link_button("Open source filing on SEC.gov", f["url"])

with tabs[3]:
    st.markdown("### AI Analyst Brief")
    st.caption(f"Generation mode: {d['brief']['mode']}")
    st.markdown(d["brief"]["text"])
    st.markdown("### How the AI brief is grounded")
    st.write("Gemini summarizes the calculated financial signals together with numbered SEC filing excerpts. It is instructed not to treat the screening score as a probability or make unsupported distress claims.")

with tabs[4]:
    st.markdown("### Scenario Stress Lab")
    a, b = st.columns(2)
    with a:
        rd = st.slider("Revenue decline", 0, 60, 15, 5, format="%d%%")
        od = st.slider("Operating income decline", 0, 100, 25, 5, format="%d%%")
    with b:
        cd = st.slider("Cash decline", 0, 80, 20, 5, format="%d%%")
        cli = st.slider("Current liabilities increase", 0, 80, 15, 5, format="%d%%")

    scen = apply_stress(snap, rd, od, cd, cli, trends=d["trends"])
    s1, s2, s3 = st.columns(3)
    s1.metric("Current Score", risk["score"])
    s2.metric("Stressed Score", scen["result"]["score"], delta=scen["result"]["score"] - risk["score"], delta_color="inverse")
    s3.metric("Stressed Risk Band", scen["result"]["label"])

    st.markdown("### What changed the score?")
    if scen["impacts"]:
        impact_df = pd.DataFrame(scen["impacts"])
        impact_df.columns = ["Risk Component", "Before", "After", "Point Change"]
        st.dataframe(impact_df, width="stretch", hide_index=True)
    else:
        st.info("These assumptions did not cross any component scoring thresholds. Try a stronger stress to see threshold effects.")

    assumptions = {"revenue_decline_pct": rd, "operating_income_decline_pct": od,
                   "cash_decline_pct": cd, "current_liabilities_increase_pct": cli}
    if st.button("Explain this scenario with AI", width="stretch"):
        with st.spinner("Interpreting stress scenario..."):
            st.session_state.scenario_brief = generate_scenario_brief(
                snap["company"], snap["ticker"], risk, scen, assumptions
            )
    if st.session_state.scenario_brief:
        st.caption(f"Scenario explanation mode: {st.session_state.scenario_brief['mode']}")
        st.write(st.session_state.scenario_brief["text"])
    st.caption("Scenario inputs are hypothetical sensitivities, not forecasts.")

with tabs[5]:
    st.markdown("### How SignalGuard Works")
    st.markdown("""<div class="how-grid">
<div class="how-card"><div class="how-num">01</div><div class="how-title">SEC Data</div><div class="how-copy">Pull standardized financial facts and the latest 10-K or 10-Q.</div></div>
<div class="how-card"><div class="how-num">02</div><div class="how-title">Risk Signals</div><div class="how-copy">Calculate transparent liquidity, leverage, profitability, cash-flow and trend signals.</div></div>
<div class="how-card"><div class="how-num">03</div><div class="how-title">Filing Evidence</div><div class="how-copy">Search filings for passages relevant to financial-risk topics.</div></div>
<div class="how-card"><div class="how-num">04</div><div class="how-title">AI Brief</div><div class="how-copy">Gemini summarizes calculated signals together with retrieved SEC evidence.</div></div>
<div class="how-card"><div class="how-num">05</div><div class="how-title">Stress Test</div><div class="how-copy">Explore how hypothetical financial deterioration changes the screening score.</div></div>
</div>""", unsafe_allow_html=True)
    st.markdown("**Stack:** Python · SEC EDGAR/XBRL · pandas · Plotly · TF-IDF · Gemini API · Streamlit")
    st.warning("SignalGuard is an educational early-warning screening system. It is not a validated credit-rating model, bankruptcy-probability model, lending decision system, or investment recommendation.")
