import streamlit as st
from lib.ui import inject, sidebar_user
from lib.auth import signin, signup, current_user, signout
from lib.db import ping

inject()
#sidebar_user()

ok, msg = ping()
if not ok:
    st.error(f"MongoDB not reachable: {msg}. Start `mongod` or set MONGO_URI in .env.")

# Hero
st.markdown("""
<div class="hero">
  <span class="badge">AI · Realtime · Open-source</span>
  <h1>Predict the next move<br/>of the crypto market.</h1>
  <p>Track live candlestick charts, build a watchlist, monitor your portfolio,
  and get machine-learning forecasts for top cryptocurrencies — all in one local app.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card"><b>📈 Live Candlesticks</b><br/><span style="opacity:.7">Plotly charts with MA & volume.</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><b>🤖 AI Forecast</b><br/><span style="opacity:.7">Random Forest & Linear models.</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><b>💼 Portfolio + Watchlist</b><br/><span style="opacity:.7">Saved in MongoDB per user.</span></div>', unsafe_allow_html=True)

st.write("---")

user = current_user()
if user:
    st.subheader(f"Welcome back, {user['username']} 👋")
    st.write("Use the sidebar to open the **Dashboard**, **AI Prediction**, **Watchlist**, **Portfolio**, **Market**, or **Settings**.")
else:
    tab1, tab2 = st.tabs(["🔐 Sign in", "✨ Sign up"])
    with tab1:
        with st.form("signin"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Sign in", use_container_width=True):
                ok, m = signin(u, p)
                (st.success if ok else st.error)(m)
                if ok: st.rerun()
    with tab2:
        with st.form("signup"):
            u = st.text_input("Choose a username")
            e = st.text_input("Email")
            p = st.text_input("Choose a password", type="password")
            if st.form_submit_button("Create account", use_container_width=True):
                ok, m = signup(u, e, p)
                (st.success if ok else st.error)(m)
