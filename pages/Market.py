import streamlit as st
import plotly.graph_objects as go
from lib.ui import inject, sidebar_user
from lib.auth import require_login
from lib.data import COINS, load_history, latest_quote

inject(); sidebar_user(); require_login()
st.title("🌐 Market Overview")

cols = st.columns(3)
for i, (name, sym) in enumerate(COINS.items()):
    df = load_history(sym, period="1mo", interval="1d")
    if df.empty: continue
    q = latest_quote(sym)
    with cols[i % 3]:
        spark = go.Figure(go.Scatter(x=df["Date"], y=df["Close"], mode="lines",
                                     line=dict(color="#00d4ff", width=2)))
        spark.update_layout(height=110, margin=dict(l=0, r=0, t=10, b=0),
                            paper_bgcolor="#121829", plot_bgcolor="#121829",
                            xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.markdown(f"<div class='card'><b>{name}</b><br/>"
                    f"<span class='metric-big'>${q['price']:,.2f}</span> "
                    f"<span class='{ 'up' if q['pct']>=0 else 'down' }'>{q['pct']:+.2f}%</span></div>",
                    unsafe_allow_html=True)
        st.plotly_chart(spark, use_container_width=True, config={"displayModeBar": False})