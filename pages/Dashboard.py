import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from lib.ui import inject, sidebar_user
from lib.auth import require_login
from lib.data import COINS, load_history, latest_quote

inject(); sidebar_user(); require_login()

st.title("📊 Dashboard")

c1, c2, c3 = st.columns([2, 1, 1])
coin = c1.selectbox("Cryptocurrency", list(COINS.keys()))
period = c2.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
interval = c3.selectbox("Interval", ["1d", "1h", "1wk"], index=0)

symbol = COINS[coin]
df = load_history(symbol, period=period, interval=interval)
if df.empty:
    st.error("No data returned. Try a different period/interval.")
    st.stop()

q = latest_quote(symbol)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Price (USD)", f"${q['price']:,.2f}", f"{q['pct']:+.2f}%")
m2.metric("24h Change", f"${q['change']:+,.2f}")
m3.metric("Period High", f"${df['High'].max():,.2f}")
m4.metric("Period Low", f"${df['Low'].min():,.2f}")

df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25],
                    vertical_spacing=0.03)
fig.add_trace(go.Candlestick(
    x=df["Date"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
    name=coin, increasing_line_color="#2ecc71", decreasing_line_color="#ff5e6c"
), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["MA20"], name="MA20",
                         line=dict(color="#ffb800", width=1.4)), row=1, col=1)
fig.add_trace(go.Scatter(x=df["Date"], y=df["MA50"], name="MA50",
                         line=dict(color="#00d4ff", width=1.4)), row=1, col=1)
fig.add_trace(go.Bar(x=df["Date"], y=df["Volume"], name="Volume",
                     marker_color="rgba(0,212,255,0.4)"), row=2, col=1)
fig.update_layout(
    template="plotly_dark", height=640, margin=dict(l=10, r=10, t=30, b=10),
    xaxis_rangeslider_visible=False, paper_bgcolor="#0b0f1a", plot_bgcolor="#0b0f1a",
    legend=dict(orientation="h", y=1.05)
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Raw data"):
    st.dataframe(df.tail(100), use_container_width=True)
