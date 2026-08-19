# Architecture

```text
                 ┌──────────────────┐
                 │   Streamlit UI   │
                 │  SignalGuard AI  │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
 ┌────────────────────┐    ┌────────────────────┐
 │ SEC Company Facts  │    │ SEC 10-K / 10-Q    │
 │ Structured XBRL    │    │ Filing Text        │
 └─────────┬──────────┘    └─────────┬──────────┘
           ▼                         ▼
 ┌────────────────────┐    ┌────────────────────┐
 │ Financial Features │    │ Chunk + TF-IDF     │
 │ Ratios / Trends    │    │ Evidence Retrieval │
 └─────────┬──────────┘    └─────────┬──────────┘
           ▼                         │
 ┌────────────────────┐              │
 │ Transparent Risk   │              │
 │ Screening Engine   │              │
 └──────┬─────────────┘              │
        ├──────────────┬─────────────┘
        ▼              ▼
 ┌──────────────┐  ┌─────────────────────┐
 │ Scenario Lab │  │ Evidence-Grounded   │
 │ Stress Test  │  │ AI Analyst Memo     │
 └──────────────┘  └─────────────────────┘
```
