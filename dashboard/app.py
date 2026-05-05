import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
API_BASE = "https://abdulqayyum360-custoemer-churn-prediction.hf.space"

st.set_page_config(
    page_title="ChurnIQ — Intelligence Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL STYLES — Corporate Glowing Glassmorphism
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Figtree:wght@300;400;500;600&display=swap');

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
div[data-testid="stHeader"] {visibility: hidden;}

:root {
  --bg-deep:       #020509;
  --glass-bg:      rgba(8, 20, 40, 0.55);
  --glass-border:  rgba(56, 140, 255, 0.18);
  --glass-hover:   rgba(56, 140, 255, 0.32);
  --glow-blue:     #3b82f6;
  --glow-cyan:     #06b6d4;
  --glow-violet:   #8b5cf6;
  --glow-emerald:  #10b981;
  --glow-rose:     #f43f5e;
  --glow-amber:    #f59e0b;
  --text-primary:  #e2eaf8;
  --text-muted:    #4a6080;
  --text-dim:      #2a3850;
}

@keyframes glow-pulse {
  0%,100% { opacity:.65; } 50% { opacity:1; }
}
@keyframes border-glow {
  0%,100% { border-color:rgba(56,140,255,.15); box-shadow:0 0 12px rgba(56,140,255,.07); }
  50%     { border-color:rgba(56,140,255,.38); box-shadow:0 0 24px rgba(56,140,255,.18); }
}
@keyframes float-up {
  from { opacity:0; transform:translateY(14px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes shimmer-line {
  0%   { left:-100%; }
  100% { left:200%;  }
}

html,body,[class*="css"] { font-family:'Figtree',sans-serif !important; color:var(--text-primary); }

.stApp {
  background:
    radial-gradient(ellipse 80% 50% at 15% -5%,  rgba(59,130,246,.13) 0%,transparent 58%),
    radial-gradient(ellipse 55% 45% at 85% 95%,  rgba(139,92,246,.10) 0%,transparent 58%),
    radial-gradient(ellipse 45% 55% at 92% 18%,  rgba(6,182,212,.07)  0%,transparent 55%),
    #020509;
  min-height:100vh;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background:rgba(3,8,18,.85) !important;
  backdrop-filter:blur(28px) !important;
  border-right:1px solid rgba(56,140,255,.10) !important;
  box-shadow:4px 0 48px rgba(59,130,246,.05) !important;
}
[data-testid="stSidebar"] * { color:var(--text-primary) !important; }

.sb-logo {
  padding:30px 20px 22px;
  border-bottom:1px solid rgba(56,140,255,.09);
  margin-bottom:4px;
  background:linear-gradient(135deg,rgba(59,130,246,.07) 0%,transparent 65%);
  position:relative; overflow:hidden;
}
.sb-pill {
  display:inline-flex; align-items:center; gap:5px;
  background:rgba(59,130,246,.10);
  border:1px solid rgba(59,130,246,.28);
  border-radius:20px; padding:4px 12px;
  font-size:11px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
  color:#60a5fa !important; margin-bottom:11px;
  box-shadow:0 0 14px rgba(59,130,246,.14);
}
.sb-wordmark {
  font-family:'Outfit',sans-serif !important;
  font-size:32px !important; font-weight:900 !important; letter-spacing:-.6px;
  background:linear-gradient(105deg,#e2eaf8 30%,#60a5fa 65%,#a78bfa 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text; display:block; margin-bottom:3px;
}
.sb-tagline {
  font-size:12px !important; color:var(--text-muted) !important;
  letter-spacing:2px; text-transform:uppercase; font-weight:500 !important;
}
.nav-label {
  font-size:12px !important; font-weight:700 !important; letter-spacing:2px;
  text-transform:uppercase; color:var(--text-dim) !important;
  padding:22px 20px 8px; display:block;
}
.sb-stat {
  display:flex; justify-content:space-between; align-items:center;
  padding:12px 20px; border-bottom:1px solid rgba(56,140,255,.05);
  font-size:14px;
}
.sb-stat-lbl { color:var(--text-muted) !important; font-weight:400; }
.sb-stat-val { font-weight:700; font-family:'Outfit',sans-serif; }

/* ── RADIO NAV ── */
.stRadio > div { gap:5px !important; }
.stRadio > div > label {
  border-radius:10px !important; padding:8px 12px !important;
  transition:all .2s !important; border:1px solid transparent !important;
  cursor:pointer !important; background:transparent !important;
}
.stRadio > div > label:hover {
  background:rgba(59,130,246,.08) !important;
  border-color:rgba(59,130,246,.18) !important;
}
.stRadio > div > label:has(input:checked) {
  background:rgba(59,130,246,.12) !important;
  border-color:rgba(59,130,246,.35) !important;
  box-shadow:0 0 18px rgba(59,130,246,.12) inset,0 0 8px rgba(59,130,246,.08) !important;
}
.stRadio > div > label p {
  font-family: 'Font Awesome 6 Free', 'Figtree', sans-serif !important;
  font-weight: 900 !important;
  font-size: 12px !important;
}

/* ── PAGE HEADER ── */
.pg-header { animation:float-up .45s ease both; padding:10px 0 26px; }
.pg-title {
  font-family:'Outfit',sans-serif; font-size:30px; font-weight:900; letter-spacing:-.8px;
  background:linear-gradient(110deg,#e2eaf8 35%,#60a5fa 70%,#a78bfa 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  margin:0 0 6px; line-height:1.1;
}
.pg-sub { font-size:13px; color:var(--text-muted); font-weight:400; letter-spacing:.2px; }

/* ── METRIC CARDS ── */
.mc-wrap {
  background:var(--glass-bg);
  border:1px solid var(--glass-border);
  border-radius:18px; padding:22px 20px 18px;
  position:relative; overflow:hidden;
  backdrop-filter:blur(18px);
  transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease;
  animation:border-glow 4s ease-in-out infinite;
}
.mc-wrap:hover {
  transform:translateY(-3px);
  border-color:var(--glass-hover);
  box-shadow:0 10px 44px rgba(59,130,246,.14),0 0 0 1px rgba(59,130,246,.10);
}
.mc-wrap::after {
  content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,var(--mc-glow,#3b82f6),transparent);
  opacity:.75;
}
.mc-wrap::before {
  content:''; position:absolute;
  top:-60%; left:-30%; width:60%; height:220%;
  background:radial-gradient(ellipse,rgba(255,255,255,.025) 0%,transparent 70%);
  pointer-events:none;
}
.mc-blue    { --mc-glow:#3b82f6; box-shadow:0 0 32px rgba(59,130,246,.09);  }
.mc-rose    { --mc-glow:#f43f5e; box-shadow:0 0 32px rgba(244,63,94,.09);   animation-delay:.4s; }
.mc-amber   { --mc-glow:#f59e0b; box-shadow:0 0 32px rgba(245,158,11,.09);  animation-delay:.8s; }
.mc-emerald { --mc-glow:#10b981; box-shadow:0 0 32px rgba(16,185,129,.09);  animation-delay:1.2s; }
.mc-violet  { --mc-glow:#8b5cf6; box-shadow:0 0 32px rgba(139,92,246,.09);  animation-delay:1.6s; }

.mc-icon {
  font-size:22px; margin-bottom:14px; display:block;
  filter:drop-shadow(0 0 8px var(--mc-glow,#3b82f6));
  animation:glow-pulse 3s ease-in-out infinite;
  color:var(--mc-glow,#3b82f6);
}
.mc-icon i { vertical-align:middle; }
.mc-val {
  font-family:'Outfit',sans-serif; font-size:34px; font-weight:900;
  color:#f0f6ff; line-height:1; margin-bottom:5px; letter-spacing:-1.2px;
}
.mc-lbl {
  font-size:10px; font-weight:700; color:var(--text-muted);
  text-transform:uppercase; letter-spacing:1.8px;
}
.mc-delta {
  display:inline-flex; align-items:center; gap:4px;
  font-size:10px; font-weight:600; padding:3px 9px;
  border-radius:20px; margin-top:10px;
}
.d-up  { background:rgba(16,185,129,.12); color:#34d399; border:1px solid rgba(16,185,129,.22); }
.d-dn  { background:rgba(244,63,94,.12);  color:#fb7185; border:1px solid rgba(244,63,94,.22);  }
.d-neu { background:rgba(74,96,128,.14);  color:#7a9abc; border:1px solid rgba(74,96,128,.18); }

/* ── SECTION DIVIDER ── */
.sec-div {
  display:flex; align-items:center; gap:14px; margin:32px 0 18px;
}
.sec-div h2 {
  font-family:'Outfit',sans-serif; font-size:15px; font-weight:800;
  color:#c0cce8; margin:0; white-space:nowrap; letter-spacing:-.2px;
}
.sec-icon { font-size:15px; filter:drop-shadow(0 0 9px #3b82f6); color:#60a5fa; }
.sec-icon i { vertical-align:middle; }
.sec-line { flex:1; height:1px; background:linear-gradient(90deg,rgba(59,130,246,.22),transparent); }

/* ── BUTTONS — GLOWING GLASS ── */
.stButton > button {
  font-family:'Outfit',sans-serif !important;
  font-size:13px !important; font-weight:700 !important; letter-spacing:.4px !important;
  border-radius:12px !important; padding:10px 22px !important;
  border:1px solid rgba(59,130,246,.32) !important;
  background:rgba(59,130,246,.09) !important;
  color:#93c5fd !important;
  backdrop-filter:blur(14px) !important;
  box-shadow:0 0 16px rgba(59,130,246,.14),0 1px 0 rgba(255,255,255,.04) inset !important;
  transition:all .22s ease !important;
  position:relative; overflow:hidden;
}
.stButton > button:hover {
  background:rgba(59,130,246,.20) !important;
  border-color:rgba(59,130,246,.60) !important;
  color:#dbeafe !important;
  box-shadow:0 0 32px rgba(59,130,246,.32),0 0 64px rgba(59,130,246,.12),0 1px 0 rgba(255,255,255,.06) inset !important;
  transform:translateY(-1px) !important;
}
.stButton > button:active { transform:translateY(0) !important; }

.stButton > button[kind="primary"] {
  background:linear-gradient(135deg,rgba(59,130,246,.30),rgba(139,92,246,.20)) !important;
  border-color:rgba(100,162,255,.52) !important;
  color:#dbeafe !important;
  box-shadow:0 0 28px rgba(59,130,246,.26),0 0 60px rgba(59,130,246,.10),0 1px 0 rgba(255,255,255,.05) inset !important;
}
.stButton > button[kind="primary"]:hover {
  background:linear-gradient(135deg,rgba(59,130,246,.44),rgba(139,92,246,.30)) !important;
  border-color:rgba(100,162,255,.82) !important;
  box-shadow:0 0 48px rgba(59,130,246,.42),0 0 90px rgba(59,130,246,.16),0 0 130px rgba(139,92,246,.10) !important;
}

/* ── FORM INPUTS ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label {
  font-family:'Outfit',sans-serif !important;
  font-size:10px !important; font-weight:700 !important;
  color:var(--text-dim) !important; text-transform:uppercase !important;
  letter-spacing:1.5px !important;
}
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
  background:rgba(5,14,28,.72) !important;
  border:1px solid rgba(56,140,255,.16) !important;
  border-radius:10px !important; color:#c8d8f0 !important;
  font-family:'Figtree',sans-serif !important; font-size:13px !important;
  backdrop-filter:blur(10px) !important;
  transition:border-color .2s,box-shadow .2s !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus {
  border-color:rgba(59,130,246,.55) !important;
  box-shadow:0 0 18px rgba(59,130,246,.16) !important;
}

/* ── FORM CARD ── */
.form-card {
  background:rgba(5,12,26,.68);
  border:1px solid rgba(56,140,255,.15);
  border-radius:20px; padding:28px 26px 22px;
  backdrop-filter:blur(20px);
  box-shadow:0 0 70px rgba(0,0,0,.30),0 0 28px rgba(59,130,246,.05) inset;
}
.form-section {
  font-family:'Outfit',sans-serif; font-size:10px; font-weight:700;
  color:var(--text-dim); text-transform:uppercase; letter-spacing:2px;
  margin:18px 0 10px; padding-bottom:8px;
  border-bottom:1px solid rgba(56,140,255,.08);
}

/* ── DATAFRAME ── */
.stDataFrame {
  border:1px solid rgba(56,140,255,.12) !important;
  border-radius:14px !important; overflow:hidden !important;
}
[data-testid="stDataFrame"] thead tr th {
  background:rgba(6,16,34,.85) !important;
  font-family:'Outfit',sans-serif !important; font-size:10px !important;
  font-weight:700 !important; text-transform:uppercase !important;
  letter-spacing:1.5px !important; color:#4a6080 !important;
}

/* ── RESULT BANNERS ── */
.banner {
  border-radius:14px; padding:18px 22px;
  display:flex; align-items:flex-start; gap:14px;
  margin-top:18px; backdrop-filter:blur(14px);
  animation:float-up .3s ease both;
}
.banner-ok {
  background:rgba(16,185,129,.07); border:1px solid rgba(16,185,129,.26);
  box-shadow:0 0 28px rgba(16,185,129,.09);
}
.banner-err {
  background:rgba(244,63,94,.07); border:1px solid rgba(244,63,94,.26);
  box-shadow:0 0 28px rgba(244,63,94,.09);
}
.b-icon { font-size:22px; flex-shrink:0; }
.b-icon i { vertical-align:middle; }
.b-head { font-family:'Outfit',sans-serif; font-size:15px; font-weight:800; margin-bottom:4px; }
.b-body { font-size:12px; color:var(--text-muted); line-height:1.5; }

/* ── DELETE PREVIEW ── */
.del-preview {
  background:rgba(244,63,94,.06); border:1px solid rgba(244,63,94,.20);
  border-radius:16px; padding:22px 24px; margin:14px 0;
  backdrop-filter:blur(14px); box-shadow:0 0 34px rgba(244,63,94,.07);
}
.del-stat { display:inline-block; margin-right:28px; margin-bottom:4px; }
.del-lbl { font-size:9px; color:rgba(244,63,94,.55); text-transform:uppercase; letter-spacing:2px; font-weight:700; display:block; }
.del-val { font-family:'Outfit',sans-serif; font-size:20px; font-weight:800; color:#f0f4ff; }

/* ── CURRENT STATE STRIP ── */
.state-strip {
  background:rgba(5,12,26,.62); border:1px solid rgba(56,140,255,.12);
  border-radius:14px; padding:16px 24px; margin:12px 0 20px;
  display:flex; gap:32px; align-items:center;
  backdrop-filter:blur(12px);
}
.state-lbl { font-size:9px; color:#2a3850; text-transform:uppercase; letter-spacing:2px; font-weight:700; margin-bottom:4px; }
.state-val { font-family:'Outfit',sans-serif; font-size:20px; font-weight:800; }

/* ── MISC OVERRIDES ── */
.block-container { padding-top:22px !important; padding-bottom:44px !important; }
hr { border-color:rgba(56,140,255,.09) !important; }
.stAlert { border-radius:12px !important; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:rgba(0,0,0,.2); }
::-webkit-scrollbar-thumb { background:rgba(59,130,246,.28); border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:rgba(59,130,246,.48); }
.stCheckbox > label { font-family:'Figtree',sans-serif !important; font-size:13px !important; color:#5a7a9c !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#4a6080", family="Figtree"),
    margin=dict(l=8, r=8, t=34, b=8),
    title_font=dict(family="Outfit", size=12, color="#6a80a0"),
)
GRID = dict(gridcolor="rgba(56,140,255,.07)", zerolinecolor="rgba(56,140,255,.10)")

C = dict(blue="#3b82f6", cyan="#06b6d4", violet="#8b5cf6",
         emerald="#10b981", rose="#f43f5e", amber="#f59e0b", pink="#ec4899")

YES_NO   = ["Yes","No"]
GENDER   = ["Male","Female"]
INTERNET = ["DSL","Fiber optic","No"]
CONTRACT = ["Month-to-month","One year","Two year"]
LINES    = ["No","Yes","No phone service"]
ADDSVC   = ["No","Yes","No internet service"]
PAYMENT  = ["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"]


@st.cache_data(ttl=1)
def fetch_customers():
    try:
        r = requests.get(f"{API_BASE}/customers", timeout=5)
        if r.status_code == 200:
            return pd.DataFrame(r.json())
    except Exception:
        pass
    return pd.DataFrame()

def invalidate(): fetch_customers.clear()

def api_post(path, payload):
    try:
        r = requests.post(f"{API_BASE}{path}", json=payload, timeout=10)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"detail": str(e)}

def api_put(path, payload):
    try:
        r = requests.put(f"{API_BASE}{path}", json=payload, timeout=10)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"detail": str(e)}

def api_delete(path):
    try:
        r = requests.delete(f"{API_BASE}{path}", timeout=5)
        return r.status_code, r.json()
    except Exception as e:
        return 500, {"detail": str(e)}




def metric_card(icon, value, label, delta=None, dtype="neu", variant="blue"):
    d = f'<span class="mc-delta d-{dtype}">{delta}</span>' if delta else ""
    return f"""
    <div class="mc-wrap mc-{variant}">
      <span class="mc-icon">{icon}</span>
      <div class="mc-val">{value}</div>
      <div class="mc-lbl">{label}</div>
      {d}
    </div>"""

def section_header(icon, title):
    st.markdown(f"""
    <div class="sec-div">
      <span class="sec-icon">{icon}</span>
      <h2>{title}</h2>
      <div class="sec-line"></div>
    </div>""", unsafe_allow_html=True)

def page_header(title, sub):
    st.markdown(f"""
    <div class="pg-header">
      <div class="pg-title">{title}</div>
      <div class="pg-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def banner_ok(head, body=""):
    st.markdown(f"""
    <div class="banner banner-ok">
      <span class="b-icon" style="color:#34d399"><i class="fa-solid fa-circle-check"></i></span>
      <div><div class="b-head" style="color:#34d399">{head}</div><div class="b-body">{body}</div></div>
    </div>""", unsafe_allow_html=True)

def banner_err(head, body=""):
    st.markdown(f"""
    <div class="banner banner-err">
      <span class="b-icon" style="color:#fb7185"><i class="fa-solid fa-circle-xmark"></i></span>
      <div><div class="b-head" style="color:#fb7185">{head}</div><div class="b-body">{body}</div></div>
    </div>""", unsafe_allow_html=True)


def customer_form(prefix="", defaults=None):
    d = defaults or {}
    st.markdown(f'<div class="form-section">◈ Identity & Demographics</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: gender   = st.selectbox("Gender",          GENDER,   index=GENDER.index(d.get("gender","Male")),      key=f"{prefix}gender")
    with c2: senior   = st.selectbox("Senior Citizen",  [0,1],    index=d.get("SeniorCitizen",0),                  key=f"{prefix}senior")
    with c3: partner  = st.selectbox("Partner",         YES_NO,   index=YES_NO.index(d.get("Partner","No")),       key=f"{prefix}partner")
    c4,c5,c6 = st.columns(3)
    with c4: deps     = st.selectbox("Dependents",      YES_NO,   index=YES_NO.index(d.get("Dependents","No")),    key=f"{prefix}dep")
    with c5: tenure   = st.number_input("Tenure (months)", 0, 72, int(d.get("tenure",12)),                         key=f"{prefix}tenure")
    with c6: phone    = st.selectbox("Phone Service",   YES_NO,   index=YES_NO.index(d.get("PhoneService","Yes")), key=f"{prefix}phone")

    st.markdown(f'<div class="form-section">◈ Services</div>', unsafe_allow_html=True)
    c7,c8,c9 = st.columns(3)
    with c7: multi    = st.selectbox("Multiple Lines",    LINES,   index=LINES.index(d.get("MultipleLines","No")),         key=f"{prefix}multi")
    with c8: internet = st.selectbox("Internet Service",  INTERNET,index=INTERNET.index(d.get("InternetService","DSL")),   key=f"{prefix}internet")
    with c9: security = st.selectbox("Online Security",   ADDSVC,  index=ADDSVC.index(d.get("OnlineSecurity","No")),       key=f"{prefix}sec")
    c10,c11,c12 = st.columns(3)
    with c10: backup  = st.selectbox("Online Backup",     ADDSVC,  index=ADDSVC.index(d.get("OnlineBackup","No")),         key=f"{prefix}backup")
    with c11: device  = st.selectbox("Device Protection", ADDSVC,  index=ADDSVC.index(d.get("DeviceProtection","No")),     key=f"{prefix}device")
    with c12: tech    = st.selectbox("Tech Support",      ADDSVC,  index=ADDSVC.index(d.get("TechSupport","No")),          key=f"{prefix}tech")
    c13,c14 = st.columns(2)
    with c13: tv     = st.selectbox("Streaming TV",     ADDSVC, index=ADDSVC.index(d.get("StreamingTV","No")),     key=f"{prefix}tv")
    with c14: movies = st.selectbox("Streaming Movies", ADDSVC, index=ADDSVC.index(d.get("StreamingMovies","No")), key=f"{prefix}movies")

    st.markdown(f'<div class="form-section">◈ Billing & Contract</div>', unsafe_allow_html=True)
    c15,c16,c17 = st.columns(3)
    with c15: contract = st.selectbox("Contract Type",      CONTRACT, index=CONTRACT.index(d.get("Contract","Month-to-month")),        key=f"{prefix}contract")
    with c16: billing  = st.selectbox("Paperless Billing",  YES_NO,   index=YES_NO.index(d.get("PaperlessBilling","Yes")),             key=f"{prefix}bill")
    with c17: payment  = st.selectbox("Payment Method",     PAYMENT,  index=PAYMENT.index(d.get("PaymentMethod","Electronic check")), key=f"{prefix}pay")
    c18,c19 = st.columns(2)
    with c18: monthly = st.number_input("Monthly Charges ($)",  0.0, 200.0,  float(d.get("MonthlyCharges",50.0)),  step=0.5, key=f"{prefix}monthly")
    with c19: total   = st.number_input("Total Charges ($)",    0.0, 12000.0,float(d.get("TotalCharges",600.0)),   step=1.0,  key=f"{prefix}total")

    return dict(gender=gender, SeniorCitizen=senior, Partner=partner, Dependents=deps,
                tenure=tenure, PhoneService=phone, MultipleLines=multi, InternetService=internet,
                OnlineSecurity=security, OnlineBackup=backup, DeviceProtection=device,
                TechSupport=tech, StreamingTV=tv, StreamingMovies=movies, Contract=contract,
                PaperlessBilling=billing, PaymentMethod=payment, MonthlyCharges=monthly, TotalCharges=total)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
      <div class="sb-pill"><i class="fa-solid fa-microchip" style="margin-right:4px"></i> AI · Live Intelligence</div>
      <div class="sb-wordmark">ChurnIQ</div>
      <div class="sb-tagline">Customer Intelligence Platform</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<span class="nav-label">Navigation</span>', unsafe_allow_html=True)
    page = st.radio("", options=[
        "  Dashboard",
        "  All Customers",
        "  Add Customer",
        "  Update Customer",
        "  Delete Customer",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<span class="nav-label">Live Statistics</span>', unsafe_allow_html=True)
    df_sb = fetch_customers()
    if not df_sb.empty:
        t = len(df_sb)
        ch = int((df_sb.get("prediction", pd.Series(dtype=str)) == "Yes").sum())
        hr = int((df_sb["probability"] > 0.70).sum()) if "probability" in df_sb.columns else 0
        am = f"${df_sb['MonthlyCharges'].mean():.0f}" if "MonthlyCharges" in df_sb.columns else "—"
        st.markdown(f"""
        <div class="sb-stat"><span class="sb-stat-lbl">Total Customers</span><span class="sb-stat-val" style="color:#60a5fa">{t:,}</span></div>
        <div class="sb-stat"><span class="sb-stat-lbl">Likely Churn</span><span class="sb-stat-val" style="color:#fb7185">{ch:,}</span></div>
        <div class="sb-stat"><span class="sb-stat-lbl">Retention Rate</span><span class="sb-stat-val" style="color:#34d399">{(t-ch)/t*100:.1f}%</span></div>
        <div class="sb-stat"><span class="sb-stat-lbl">High-Risk (&gt;70%)</span><span class="sb-stat-val" style="color:#fbbf24">{hr:,}</span></div>
        <div class="sb-stat" style="border:none"><span class="sb-stat-lbl">Avg Monthly</span><span class="sb-stat-val" style="color:#c084fc">{am}</span></div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:12px 20px;font-size:12px;color:#2a3850">No data loaded.</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄  Refresh Data", use_container_width=True):
        invalidate(); st.rerun()
    st.markdown("""
    <div style="padding:20px 20px 6px;text-align:center">
      <p style="font-size:9px;color:#1a2840;letter-spacing:1.5px;text-transform:uppercase;margin:0">
        ChurnIQ v1.0 · FastAPI + RandomForest ML
      </p>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ◈  DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if page == "  Dashboard":
    page_header('<i class="fa-solid fa-gauge-high"></i> Intelligence Dashboard',
                "Real-time churn analytics — updates automatically after every operation")
    df = fetch_customers()
    if df.empty:
        st.warning("No customer records found. Add customers to populate the dashboard.")
        st.stop()

    total    = len(df)
    churned  = int((df.get("prediction", pd.Series(dtype=str)) == "Yes").sum())
    retained = total - churned
    cr       = churned / total * 100
    avg_ch   = df["MonthlyCharges"].mean() if "MonthlyCharges" in df.columns else 0
    avg_tn   = df["tenure"].mean() if "tenure" in df.columns else 0
    hr       = int((df["probability"] > 0.70).sum()) if "probability" in df.columns else 0

    # KPI row
    cols = st.columns(5)
    kpis = [
        ('<i class="fa-solid fa-users"></i>',           f"{total:,}",    "Total Customers",   "Live",              "neu","blue"),
        ('<i class="fa-solid fa-triangle-exclamation"></i>', f"{hr:,}",      "High-Risk >70%",    "Needs attention",   "dn", "rose"),
        ('<i class="fa-solid fa-user-xmark"></i>',      f"{churned:,}",  "Predicted Churn",   f"{cr:.1f}% rate",   "dn", "amber"),
        ('<i class="fa-solid fa-user-check"></i>',      f"{retained:,}", "Retained",           f"{100-cr:.1f}% safe","up","emerald"),
        ('<i class="fa-solid fa-dollar-sign"></i>',     f"${avg_ch:.0f}","Avg Monthly Charge", f"Avg {avg_tn:.0f}mo tenure","neu","violet"),
    ]
    for col,(icon,val,lbl,delta,dtype,var) in zip(cols,kpis):
        with col: st.markdown(metric_card(icon,val,lbl,delta,dtype,var), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1
    section_header('<i class="fa-solid fa-chart-pie"></i>',"Churn Overview")
    r1a,r1b,r1c = st.columns(3)

    with r1a:
        fig = go.Figure(go.Pie(labels=["Churned","Retained"],values=[churned,retained],hole=.68,
            marker=dict(colors=[C["rose"],C["emerald"]],line=dict(color="rgba(0,0,0,0)",width=0)),textinfo="none"))
        fig.add_annotation(text=f"<b>{cr:.1f}%</b>",x=.5,y=.55,showarrow=False,font=dict(size=22,color="#e2eaf8",family="Outfit"))
        fig.add_annotation(text="churn rate",x=.5,y=.40,showarrow=False,font=dict(size=10,color="#4a6080",family="Figtree"))
        fig.update_layout(**PLOT,height=268,title="Churn Distribution",
            legend=dict(orientation="h",y=-.06,x=.5,xanchor="center",font=dict(color="#4a6080",size=10)))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with r1b:
        if "probability" in df.columns:
            fig = px.histogram(df,x="probability",nbins=22,color_discrete_sequence=[C["blue"]],title="Probability Distribution")
            fig.update_traces(marker_line_color="rgba(0,0,0,0)",opacity=.84)
            fig.add_vline(x=.5,line_dash="dot",line_color=C["amber"],line_width=1.4,
                          annotation_text=" 50%",annotation_font_color=C["amber"],annotation_font_size=10)
            fig.update_layout(**PLOT,height=268,xaxis=dict(**GRID,title="Probability"),yaxis=dict(**GRID,title="Customers"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with r1c:
        if "Contract" in df.columns:
            cdf = df.groupby(["Contract","prediction"]).size().reset_index(name="n")
            fig = px.bar(cdf,x="Contract",y="n",color="prediction",barmode="group",title="Churn by Contract",
                         color_discrete_map={"Yes":C["rose"],"No":C["emerald"]})
            fig.update_traces(marker_line_color="rgba(0,0,0,0)")
            fig.update_layout(**PLOT,height=268,xaxis=dict(**GRID),yaxis=dict(**GRID),
                legend=dict(title="Churn",font=dict(color="#4a6080",size=10)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    # Row 2
    section_header('<i class="fa-solid fa-users-viewfinder"></i>',"Customer Segments")
    r2a,r2b = st.columns(2)

    with r2a:
        if "tenure" in df.columns and "MonthlyCharges" in df.columns:
            fig = px.scatter(df,x="tenure",y="MonthlyCharges",color="prediction",opacity=.72,
                             color_discrete_map={"Yes":C["rose"],"No":C["cyan"]},title="Tenure vs Monthly Charges",
                             hover_data=["Contract"] if "Contract" in df.columns else None)
            fig.update_traces(marker=dict(size=7,line=dict(width=0)))
            fig.update_layout(**PLOT,height=298,xaxis=dict(**GRID,title="Tenure (months)"),
                yaxis=dict(**GRID,title="Monthly Charges ($)"),
                legend=dict(title="Churn",font=dict(color="#4a6080",size=10)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with r2b:
        if "InternetService" in df.columns:
            idf = df.groupby(["InternetService","prediction"]).size().reset_index(name="n")
            fig = px.bar(idf,x="InternetService",y="n",color="prediction",barmode="stack",title="Churn by Internet Service",
                         color_discrete_map={"Yes":C["rose"],"No":C["violet"]})
            fig.update_traces(marker_line_color="rgba(0,0,0,0)")
            fig.update_layout(**PLOT,height=298,xaxis=dict(**GRID),yaxis=dict(**GRID),
                legend=dict(title="Churn",font=dict(color="#4a6080",size=10)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    # Row 3
    section_header('<i class="fa-solid fa-diagram-project"></i>',"Demographic Breakdown")
    r3a,r3b,r3c = st.columns(3)

    with r3a:
        if "PaymentMethod" in df.columns:
            pmc = df[df["prediction"]=="Yes"].groupby("PaymentMethod").size().reset_index(name="n")
            fig = px.bar(pmc.sort_values("n"),x="n",y="PaymentMethod",orientation="h",
                         color="n",color_continuous_scale=["#0d1828",C["rose"]],title="Churned by Payment Method")
            fig.update_traces(marker_line_color="rgba(0,0,0,0)")
            fig.update_layout(**PLOT,height=258,xaxis=dict(**GRID),yaxis=dict(**GRID),coloraxis_showscale=False)
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with r3b:
        if "gender" in df.columns:
            gdf = df.groupby(["gender","prediction"]).size().reset_index(name="n")
            fig = px.bar(gdf,x="gender",y="n",color="prediction",barmode="group",title="Churn by Gender",
                         color_discrete_map={"Yes":C["violet"],"No":C["cyan"]})
            fig.update_traces(marker_line_color="rgba(0,0,0,0)")
            fig.update_layout(**PLOT,height=258,xaxis=dict(**GRID),yaxis=dict(**GRID),
                legend=dict(title="Churn",font=dict(color="#4a6080",size=10)))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with r3c:
        if "SeniorCitizen" in df.columns:
            df["_sr"] = df["SeniorCitizen"].map({0:"Non-Senior",1:"Senior"})
            fig = px.pie(df[df["prediction"]=="Yes"],names="_sr",hole=.44,title="Churned: Seniority",
                         color_discrete_sequence=[C["amber"],C["pink"]])
            fig.update_traces(textinfo="percent+label",textfont=dict(size=10,color="#c0cce8"))
            fig.update_layout(**PLOT,height=258,legend=dict(font=dict(color="#4a6080",size=10),
                orientation="h",y=-.10,x=.5,xanchor="center"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    # High-risk table
    section_header('<i class="fa-solid fa-bolt-lightning"></i>',"High-Risk Customers  ( probability ≥ 70% )")
    if "probability" in df.columns:
        hr_df = df[df["probability"] >= .70].sort_values("probability",ascending=False)
        if hr_df.empty:
            st.success("No high-risk customers detected at this time.")
        else:
            show = [c for c in ["id","gender","tenure","Contract","InternetService","MonthlyCharges","prediction","probability"] if c in hr_df.columns]
            disp = hr_df[show].copy()
            if "probability"    in disp: disp["probability"]    = disp["probability"].apply(lambda x: f"{x*100:.1f}%")
            if "MonthlyCharges" in disp: disp["MonthlyCharges"] = disp["MonthlyCharges"].apply(lambda x: f"${x:.2f}")
            st.dataframe(disp.reset_index(drop=True),use_container_width=True,hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ◉  ALL CUSTOMERS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "  All Customers":
    page_header('<i class="fa-solid fa-address-book"></i> Customer Registry',"Browse and filter every customer record with live data")
    df = fetch_customers()
    if df.empty:
        st.warning("No customer records found."); st.stop()

    fc1,fc2,fc3,fc4 = st.columns([2,2,2,1])
    with fc1: fp = st.selectbox("Prediction",["All","Churn (Yes)","Retained (No)"])
    with fc2:
        cts = ["All"]+(sorted(df["Contract"].dropna().unique()) if "Contract" in df.columns else [])
        fc = st.selectbox("Contract",cts)
    with fc3:
        its = ["All"]+(sorted(df["InternetService"].dropna().unique()) if "InternetService" in df.columns else [])
        fi = st.selectbox("Internet",its)
    with fc4:
        st.markdown("<br>",unsafe_allow_html=True)
        sr = st.checkbox("Sort by Risk")

    filt = df.copy()
    if fp == "Churn (Yes)":     filt = filt[filt["prediction"]=="Yes"]
    elif fp == "Retained (No)": filt = filt[filt["prediction"]=="No"]
    if fc != "All" and "Contract" in filt.columns:        filt = filt[filt["Contract"]==fc]
    if fi != "All" and "InternetService" in filt.columns: filt = filt[filt["InternetService"]==fi]
    if sr and "probability" in filt.columns:              filt = filt.sort_values("probability",ascending=False)

    st.markdown(f'<div style="margin:10px 0 14px;font-size:12px;color:#4a6080">Showing <b style="color:#60a5fa;font-family:Outfit">{len(filt):,}</b> of <b style="color:#60a5fa;font-family:Outfit">{len(df):,}</b> records</div>',unsafe_allow_html=True)

    show = [c for c in ["id","gender","SeniorCitizen","tenure","Contract","InternetService","MonthlyCharges","TotalCharges","prediction","probability"] if c in filt.columns]
    disp = filt[show].copy()
    if "probability"    in disp: disp["probability"]    = disp["probability"].apply(lambda x: f"{x*100:.1f}%")
    if "MonthlyCharges" in disp: disp["MonthlyCharges"] = disp["MonthlyCharges"].apply(lambda x: f"${x:.2f}")
    if "TotalCharges"   in disp: disp["TotalCharges"]   = disp["TotalCharges"].apply(lambda x: f"${x:.2f}")
    st.dataframe(disp.reset_index(drop=True),use_container_width=True,hide_index=True)

    if "prediction" in df.columns:
        mc = df["prediction"].value_counts().reset_index(); mc.columns=["prediction","count"]
        fig = px.bar(mc,x="prediction",y="count",color="prediction",title="Prediction Summary",
                     color_discrete_map={"Yes":C["rose"],"No":C["emerald"]})
        fig.update_traces(marker_line_color="rgba(0,0,0,0)",width=.38)
        fig.update_layout(**PLOT,height=196,showlegend=False,xaxis=dict(**GRID),yaxis=dict(**GRID))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ✦  ADD CUSTOMER
# ─────────────────────────────────────────────────────────────────────────────
elif page == "  Add Customer":
    page_header('<i class="fa-solid fa-user-plus"></i> Add New Customer',"Enter customer details — ML churn prediction fires automatically on save")

    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    form_data = customer_form(prefix="add_")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn,_ = st.columns([1,3])
    with col_btn:
        submitted = st.button("💾  Save & Predict Churn", type="primary", use_container_width=True)

    if submitted:
        with st.spinner("Running ML inference…"):
            time.sleep(0.25)
            status, resp = api_post("/customers", form_data)
        if status == 200:
            pred = resp.get("prediction","N/A"); prob = resp.get("probability",0)
            pc = "#fb7185" if pred=="Yes" else "#34d399"
            invalidate()
            banner_ok(
                f"Customer #{resp.get('customer_id')} created successfully",
                f"Churn Prediction: <b style='color:{pc}'>{('⚡' if pred=='Yes' else '✦')} {pred}</b>"
                f"&nbsp; · &nbsp;Probability: <b style='color:{pc}'>{prob*100:.1f}%</b>"
            )
        else:
            banner_err("Failed to create customer", resp.get("detail","Unknown error"))


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ⟳  UPDATE CUSTOMER
# ─────────────────────────────────────────────────────────────────────────────
elif page == "  Update Customer":
    page_header('<i class="fa-solid fa-user-pen"></i> Update Customer',"Edit any attribute — prediction re-runs automatically")
    df_all = fetch_customers()
    if df_all.empty:
        st.warning("No customers available."); st.stop()

    ids = df_all["id"].tolist() if "id" in df_all.columns else []
    col_id,_ = st.columns([1,3])
    with col_id: sel_id = st.selectbox("Select Customer ID", ids)

    existing = df_all[df_all["id"]==sel_id].iloc[0].to_dict() if sel_id else {}

    if existing:
        cp = existing.get("prediction","N/A"); cb = float(existing.get("probability",0))
        pc = "#fb7185" if cp=="Yes" else "#34d399"
        st.markdown(f"""
        <div class="state-strip">
          <div><div class="state-lbl">Current Prediction</div>
               <div class="state-val" style="color:{pc}">{('⚡' if cp=="Yes" else '✦')} {cp}</div></div>
          <div><div class="state-lbl">Probability</div>
               <div class="state-val" style="color:{pc}">{cb*100:.1f}%</div></div>
          <div><div class="state-lbl">Tenure</div>
               <div class="state-val" style="color:#e2eaf8">{existing.get("tenure","—")} mo</div></div>
          <div><div class="state-lbl">Contract</div>
               <div class="state-val" style="color:#60a5fa">{existing.get("Contract","—")}</div></div>
          <div><div class="state-lbl">Monthly</div>
               <div class="state-val" style="color:#c084fc">${existing.get("MonthlyCharges",0):.0f}</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    form_data = customer_form(prefix="upd_", defaults=existing)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn,_ = st.columns([1,3])
    with col_btn: upd_btn = st.button("🔄  Update & Re-Predict", type="primary", use_container_width=True)

    if upd_btn and sel_id:
        with st.spinner("Updating and re-running prediction…"):
            time.sleep(0.25)
            status, resp = api_put(f"/customers/{sel_id}", form_data)
        if status == 200:
            np_ = resp.get("prediction","N/A"); nb_ = resp.get("probability",0)
            pc  = "#fb7185" if np_=="Yes" else "#34d399"
            invalidate()
            banner_ok(f"Customer #{sel_id} updated successfully",
                f"New Prediction: <b style='color:{pc}'>{('⚡' if np_=='Yes' else '✦')} {np_}</b>"
                f"&nbsp; · &nbsp;Probability: <b style='color:{pc}'>{nb_*100:.1f}%</b>")
        else:
            banner_err("Update failed", resp.get("detail","Unknown error"))


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ✕  DELETE CUSTOMER
# ─────────────────────────────────────────────────────────────────────────────
elif page == "  Delete Customer":
    page_header('<i class="fa-solid fa-user-minus"></i> Delete Record',"Remove customer from database — this action is permanent")
    df_all = fetch_customers()
    if df_all.empty:
        st.warning("No customers to delete."); st.stop()

    ids = df_all["id"].tolist() if "id" in df_all.columns else []
    col_id,_ = st.columns([1,3])
    with col_id: del_id = st.selectbox("Select Customer ID", ids)

    if del_id:
        row  = df_all[df_all["id"]==del_id].iloc[0].to_dict()
        pred = row.get("prediction","N/A"); prob = float(row.get("probability",0))
        pc   = "#fb7185" if pred=="Yes" else "#34d399"

        st.markdown(f"""
        <div class="del-preview">
          <div style="font-family:Outfit;font-size:9px;font-weight:700;color:rgba(244,63,94,.52);
                      text-transform:uppercase;letter-spacing:2px;margin-bottom:18px">
            ⚠ &nbsp; Deletion Preview — This action is irreversible
          </div>
          <div class="del-stat"><span class="del-lbl">Customer ID</span><span class="del-val">#{del_id}</span></div>
          <div class="del-stat"><span class="del-lbl">Gender</span><span class="del-val">{row.get("gender","—")}</span></div>
          <div class="del-stat"><span class="del-lbl">Tenure</span><span class="del-val">{row.get("tenure","—")} mo</span></div>
          <div class="del-stat"><span class="del-lbl">Contract</span><span class="del-val">{row.get("Contract","—")}</span></div>
          <div class="del-stat">
            <span class="del-lbl">Churn Prediction</span>
            <span style="font-family:Outfit;font-size:20px;font-weight:800;color:{pc}">
              {"⚡" if pred=="Yes" else "✦"} {pred} ({prob*100:.1f}%)
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

        col_chk,_ = st.columns([2,2])
        with col_chk: confirmed = st.checkbox(f"I confirm permanent deletion of Customer #{del_id}")

        if confirmed:
            col_del,_ = st.columns([1,3])
            with col_del: del_btn = st.button("🗑️  Delete Permanently", type="primary", use_container_width=True)
            if del_btn:
                with st.spinner("Deleting…"):
                    status, resp = api_delete(f"/customers/{del_id}")
                if status == 200:
                    invalidate()
                    banner_ok(f"Customer #{del_id} permanently deleted",
                              "The record and associated ML prediction have been removed.")
                    time.sleep(1); st.rerun()
                else:
                    banner_err("Deletion failed", resp.get("detail","Unknown error"))