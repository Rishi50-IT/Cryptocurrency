import streamlit as st
from lib.ui import inject, sidebar_user
from lib.auth import require_login, current_user, check_pw, hash_pw, signout
from lib.db import users, watchlists, portfolios

inject(); sidebar_user(); require_login()
user = current_user()
st.title("⚙️ Settings")

st.subheader("Account")
st.write(f"**Username:** {user['username']}")
st.write(f"**Email:** {user.get('email','—')}")

st.subheader("Change password")
with st.form("pw"):
    cur = st.text_input("Current password", type="password")
    new = st.text_input("New password", type="password")
    if st.form_submit_button("Update password"):
        u = users().find_one({"username": user["username"]})
        if not u or not check_pw(cur, u["password"]):
            st.error("Current password is incorrect.")
        elif len(new) < 6:
            st.error("New password must be at least 6 characters.")
        else:
            users().update_one({"username": user["username"]}, {"$set": {"password": hash_pw(new)}})
            st.success("Password updated.")

st.subheader("Danger zone")
if st.checkbox("I understand this permanently deletes my account and data."):
    if st.button("Delete my account", type="primary"):
        un = user["username"]
        users().delete_one({"username": un})
        watchlists().delete_one({"username": un})
        portfolios().delete_many({"username": un})
        signout(); st.success("Account deleted."); st.rerun()
