import streamlit as st
from lib.ui import inject, sidebar_user
from lib.auth import signin, signup, current_user, signout
from lib.db import ping




inject()
sidebar_user()

ok, msg = ping()
if not ok:
    st.error(f"MongoDB not reachable: {msg}. Start `mongod` or set MONGO_URI in .env.")
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
                st.switch_page("pages/Dashboard.py")
    with tab2:
        with st.form("signup"):
            u = st.text_input("Choose a username")
            e = st.text_input("Email")
            p = st.text_input("Choose a password", type="password")
            if st.form_submit_button("Create account", use_container_width=True):
                ok, m = signup(u, e, p)
                (st.success if ok else st.error)(m)