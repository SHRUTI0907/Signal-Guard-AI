def inject_css(st):
    st.markdown(r'''<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    :root{--bg:#F8F9FA;--surface:#FFFFFF;--navy:#101827;--muted:#687386;--line:rgba(16,24,39,.10);--accent:#6D28D9;--accent2:#7C3AED;}
    html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--navy)}
    .stApp{background:radial-gradient(circle at 78% 4%,rgba(109,40,217,.08),transparent 24rem),linear-gradient(180deg,#fff 0%,#F8F9FA 32%,#F8F9FA 100%)}
    .block-container{padding-top:2rem;padding-bottom:4rem;max-width:1320px}
    h1,h2,h3{letter-spacing:-.035em;color:var(--navy)}
    h1{font-family:'Playfair Display',serif!important}
    h2{font-size:2rem!important} h3{font-size:1.35rem!important;margin-top:1.35rem}
    .hero{position:relative;overflow:hidden;padding:2.8rem 3rem;border:1px solid var(--line);border-radius:26px;margin-bottom:2rem;background:linear-gradient(135deg,rgba(255,255,255,.96),rgba(246,243,255,.88));box-shadow:0 22px 60px rgba(16,24,39,.08)}
    .hero:after{content:'';position:absolute;width:240px;height:240px;border-radius:50%;right:-70px;top:-100px;background:radial-gradient(circle,rgba(109,40,217,.20),rgba(109,40,217,0) 68%)}
    .eyebrow{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);font-weight:700}
    .hero h1{margin:.45rem 0 .45rem;font-size:4rem;line-height:.98;position:relative;z-index:1}
    .hero-sub{font-size:1.18rem;font-weight:600;margin-top:.85rem;position:relative;z-index:1}
    .small-note{color:var(--muted);font-size:.95rem;max-width:760px;margin-top:.45rem;position:relative;z-index:1}
    [data-testid="stSidebar"]{background:#111827;border-right:1px solid rgba(255,255,255,.08)}
    [data-testid="stSidebar"] *{color:#F8F9FA}
    [data-testid="stSidebar"] input,[data-testid="stSidebar"] [data-baseweb="select"] *{color:#111827!important}
    [data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.12)}
    [data-testid="stMetric"]{border:1px solid var(--line);padding:1.05rem 1.15rem;border-radius:18px;background:rgba(255,255,255,.82);box-shadow:0 12px 30px rgba(16,24,39,.055);backdrop-filter:blur(10px);transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
    [data-testid="stMetric"]:hover{transform:translateY(-3px);box-shadow:0 18px 38px rgba(16,24,39,.09);border-color:rgba(109,40,217,.28)}
    [data-testid="stMetricValue"]{font-size:2rem;line-height:1.1;font-weight:650;letter-spacing:-.035em}
    [data-testid="stMetricLabel"]{font-size:.78rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
    .stButton>button,[data-testid="stLinkButton"] a{border-radius:12px!important;font-weight:700!important;transition:transform .18s ease,filter .18s ease,box-shadow .18s ease!important}
    .stButton>button[kind="primary"]{background:var(--accent)!important;border-color:var(--accent)!important;color:white!important;box-shadow:0 10px 24px rgba(109,40,217,.22)}
    .stButton>button:hover,[data-testid="stLinkButton"] a:hover{transform:scale(1.02);filter:brightness(1.04)}
    button[data-baseweb="tab"]{font-weight:650!important;padding:.8rem .8rem!important;transition:color .2s ease,background .2s ease}
    button[data-baseweb="tab"][aria-selected="true"]{color:var(--accent)!important}
    [data-testid="stDataFrame"],details{border-radius:16px!important;overflow:hidden;border:1px solid var(--line)!important;background:rgba(255,255,255,.84)!important;box-shadow:0 10px 28px rgba(16,24,39,.04)}
    details{transition:transform .2s ease,box-shadow .2s ease} details:hover{transform:translateY(-2px);box-shadow:0 15px 34px rgba(16,24,39,.075)}
    [data-testid="stPlotlyChart"]{background:rgba(255,255,255,.72);border:1px solid var(--line);border-radius:18px;padding:.4rem;box-shadow:0 10px 28px rgba(16,24,39,.035)}
    .section-kicker{color:var(--accent);font-size:.72rem;font-weight:800;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.2rem}
    .soft-panel{padding:1.25rem 1.4rem;border-radius:18px;border:1px solid var(--line);background:rgba(255,255,255,.70);box-shadow:0 12px 30px rgba(16,24,39,.04)}
    .how-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:.75rem;margin:1.2rem 0 1.5rem}.how-card{padding:1rem;border:1px solid var(--line);border-radius:16px;background:white;box-shadow:0 8px 20px rgba(16,24,39,.04)}.how-num{color:var(--accent);font-weight:800;font-size:.78rem}.how-title{font-weight:750;margin:.25rem 0}.how-copy{color:var(--muted);font-size:.82rem;line-height:1.45}
    @media(max-width:900px){.hero{padding:2rem 1.5rem}.hero h1{font-size:3rem}.how-grid{grid-template-columns:1fr}.block-container{padding-left:1rem;padding-right:1rem}}
    </style>''', unsafe_allow_html=True)
