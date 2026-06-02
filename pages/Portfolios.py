import streamlit as st
import pandas as pd
from lib.ui import inject, sidebar_user
from lib.auth import require_login, current_user
from lib.db import portfolios
from lib.data import COINS, latest_quote

inject(); sidebar_user(); require_login()
user = current_user()

st.title("💼 Portfolio")

with st.form("add_holding"):
    c1, c2, c3, c4 = st.columns(4)
    coin = c1.selectbox("Coin", list(COINS.keys()))
    qty = c2.number_input("Quantity", min_value=0.0, step=0.01, format="%.6f")
    buy = c3.number_input("Buy price (USD)", min_value=0.0, step=0.01, format="%.2f")
    submit = c4.form_submit_button("➕ Add holding", use_container_width=True)
    if submit and qty > 0 and buy > 0:
        portfolios().insert_one({"username": user["username"], "symbol": COINS[coin],
                                 "coin": coin, "qty": qty, "buy": buy})
        st.success("Added."); st.rerun()

holdings = list(portfolios().find({"username": user["username"]}))
if not holdings:
    st.info("No holdings yet.")
    st.stop()

rows, total_cost, total_value = [], 0.0, 0.0
for h in holdings:
    price = latest_quote(h["symbol"]).get("price", 0.0)
    value = price * h["qty"]; cost = h["buy"] * h["qty"]
    pnl = value - cost; pnl_pct = (pnl / cost * 100) if cost else 0
    total_cost += cost; total_value += value
    rows.append({"Coin": h["coin"], "Qty": h["qty"], "Buy": h["buy"],
                 "Now": price, "Value": value, "P&L": pnl, "P&L %": pnl_pct,
                 "_id": str(h["_id"])})

df = pd.DataFrame(rows)
m1, m2, m3 = st.columns(3)
m1.metric("Total cost", f"${total_cost:,.2f}")
m2.metric("Current value", f"${total_value:,.2f}")
m3.metric("Total P&L", f"${total_value-total_cost:+,.2f}",
          f"{((total_value-total_cost)/total_cost*100 if total_cost else 0):+.2f}%")

st.dataframe(df.drop(columns=["_id"]).style.format({
    "Buy": "${:,.2f}", "Now": "${:,.2f}", "Value": "${:,.2f}",
    "P&L": "${:+,.2f}", "P&L %": "{:+.2f}%", "Qty": "{:.6f}"
}), use_container_width=True)

st.subheader("Remove a holding")
for _, r in df.iterrows():
    cc = st.columns([4, 1])
    cc[0].write(f"{r['Coin']} — {r['Qty']} @ ${r['Buy']:.2f}")
    if cc[1].button("Delete", key=f"del_{r['_id']}"):
        from bson import ObjectId
        portfolios().delete_one({"_id": ObjectId(r["_id"])})
        st.rerun()
