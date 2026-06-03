import streamlit as st

'''CSS = """
<style>
:root {
  --bg: #0b0f1a;
  --panel: #121829;
  --accent: #ffb800;
  --accent2: #00d4ff;
  --text: #e8ecf3;
}
.stApp { background: radial-gradient(1200px 600px at 10% 0%, #1a2240 0%, var(--bg) 60%) !important; color: var(--text); }
.block-container { padding-top: 2rem; }
.hero {
  padding: 56px 40px; border-radius: 20px;
  background: linear-gradient(135deg, rgba(255,184,0,0.12), rgba(0,212,255,0.08));
  border: 1px solid rgba(255,255,255,0.08);
}
.hero h1 {
  font-size: 3.2rem; line-height: 1.05; margin: 0 0 12px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { font-size: 1.1rem; opacity: 0.85; max-width: 640px; }
.card {
  background: var(--panel); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px; padding: 18px;
}
.metric-big { font-size: 2rem; font-weight: 700; }
.up { color: #2ecc71; } .down { color: #ff5e6c; }
.badge {
  display:inline-block; padding:4px 10px; border-radius:999px;
  background: rgba(0,212,255,0.12); color: var(--accent2);
  font-size: .75rem; letter-spacing: .08em; text-transform: uppercase;
}
section[data-testid="stSidebar"] { background: #0a0f1c; }
</style>
"""'''
CSS = """
<style>

:root{
    --bg:#050816;
    --panel:#111827;
    --panel2:#1E293B;

    --blue:#00D4FF;
    --purple:#8B5CF6;
    --pink:#EC4899;
    --green:#22C55E;
    --orange:#F59E0B;
    --red:#EF4444;

    --text:#F8FAFC;
}

.stApp{
    background:
    radial-gradient(circle at top left,#1E3A8A 0%,transparent 35%),
    radial-gradient(circle at top right,#7C3AED 0%,transparent 35%),
    radial-gradient(circle at bottom,#EC4899 0%,transparent 30%),
    #050816 !important;

    color:var(--text);
}

.block-container{
    padding-top:1rem;
}

/* HERO */

.hero{
    padding:60px;
    border-radius:25px;

    background:
    linear-gradient(
    135deg,
    rgba(0,212,255,.20),
    rgba(139,92,246,.20),
    rgba(236,72,153,.20));

    backdrop-filter:blur(20px);

    border:1px solid rgba(255,255,255,.15);

    box-shadow:
    0 0 30px rgba(0,212,255,.2),
    0 0 60px rgba(139,92,246,.1);
}

.hero h1{
    font-size:4rem;
    font-weight:900;

    background:
    linear-gradient(
    90deg,
    #00D4FF,
    #8B5CF6,
    #EC4899);

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p{
    color:#CBD5E1;
    font-size:1.2rem;
}

/* CARD */

.card{
    background:rgba(17,24,39,.75);

    backdrop-filter:blur(15px);

    border:1px solid rgba(255,255,255,.08);

    border-radius:20px;

    padding:20px;

    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px);

    box-shadow:
    0 0 25px rgba(0,212,255,.25);
}

/* METRICS */

.metric-big{
    font-size:2.5rem;
    font-weight:800;
    color:#00D4FF;
}

.up{
    color:#22C55E;
    font-weight:700;
}

.down{
    color:#EF4444;
    font-weight:700;
}

/* BADGE */

.badge{
    background:
    linear-gradient(
    90deg,
    #00D4FF,
    #8B5CF6);

    color:white;

    padding:8px 15px;

    border-radius:50px;

    font-weight:700;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
    180deg,
    #0B1120,
    #111827);
}

/* BUTTONS */

.stButton button{
    background:
    linear-gradient(
    90deg,
    #00D4FF,
    #8B5CF6);

    color:white;

    border:none;

    border-radius:12px;

    font-weight:bold;

    transition:0.3s;
}

.stButton button:hover{
    transform:scale(1.05);
    box-shadow:0 0 20px rgba(0,212,255,.4);
}

/* DATAFRAME */

[data-testid="stDataFrame"]{
    border-radius:20px;
    overflow:hidden;
}

/* SCROLLBAR */

::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-thumb{
    background:#00D4FF;
    border-radius:10px;
}

</style>
"""

def inject():
    st.set_page_config(page_title="Crypto Predictor", page_icon="🪙", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)

def sidebar_user():
    from .auth import current_user, signout
    u = current_user()
    with st.sidebar:
        st.markdown("### 🪙 Crypto Predictor")
        if u:
            st.success(f"Signed in as **{u['username']}**")
            if st.button("Sign out", use_container_width=True):
                signout(); st.rerun()
        else:
            st.info("Not signed in")
        st.caption("Educational use only — not financial advice.")
