import streamlit as st
from lib.ui import inject, sidebar_user
from lib.auth import require_login, current_user
from lib.db import watchlists
from lib.data import COINS, latest_quote

inject(); sidebar_user(); require_login()
user = current_user()

st.title("⭐ Watchlist")

doc = watchlists().find_one({"username": user["username"]}) or {"username": user["username"], "coins": []}
coins = doc.get("coins", [])

c1, c2 = st.columns([3, 1])
add = c1.selectbox("Add coin", [c for c in COINS if COINS[c] not in coins])
if c2.button("➕ Add", use_container_width=True):
    coins.append(COINS[add])
    watchlists().update_one({"username": user["username"]}, {"$set": {"coins": coins}}, upsert=True)
    st.rerun()

if not coins:
    st.info("Your watchlist is empty.")
else:
    inv = {v: k for k, v in COINS.items()}
    for sym in coins:
        q = latest_quote(sym)
        cc = st.columns([3, 2, 2, 1])
        cc[0].markdown(f"**{inv.get(sym, sym)}**  \n`{sym}`")
        cc[1].metric("Price", f"${q.get('price', 0):,.2f}")
        cc[2].metric("24h %", f"{q.get('pct', 0):+.2f}%")
        if cc[3].button("✖", key=f"rm_{sym}"):
            coins.remove(sym)
            watchlists().update_one({"username": user["username"]}, {"$set": {"coins": coins}})
            st.rerun()
