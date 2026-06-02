import streamlit as st

CSS = """
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
