import streamlit as st
import plotly.graph_objects as go
from lib.ui import inject, sidebar_user
from lib.auth import require_login
from lib.data import COINS, load_history
from lib.ml import train_and_predict

inject(); sidebar_user(); require_login()

st.title("🤖 AI Price Prediction")
st.caption("Educational only. Not financial advice.")

c1, c2, c3 = st.columns(3)
coin = c1.selectbox("Cryptocurrency", list(COINS.keys()))
horizon = c2.slider("Forecast horizon (days)", 3, 30, 7)
model_name = c3.selectbox("Model", ["Random Forest", "Linear Regression"])

symbol = COINS[coin]
df = load_history(symbol, period="2y", interval="1d")
if df.empty:
    st.error("No data available."); st.stop()

with st.spinner("Training model…"):
    try:
        res = train_and_predict(df, horizon=horizon, model_name=model_name)
    except ValueError as e:
        st.error(str(e)); st.stop()

m1, m2, m3 = st.columns(3)
m1.metric("Test MAE", f"${res['mae']:,.2f}")
m2.metric("Test R²", f"{res['r2']:.3f}")
m3.metric("Next-day forecast", f"${res['forecast']['Forecast'].iloc[0]:,.2f}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="History",
                         line=dict(color="#e8ecf3", width=1.2)))
fig.add_trace(go.Scatter(x=res["test"]["Date"], y=res["test"]["Predicted"],
                         name="Backtest predicted", line=dict(color="#00d4ff", width=1.6, dash="dot")))
fig.add_trace(go.Scatter(x=res["forecast"]["Date"], y=res["forecast"]["Forecast"],
                         name=f"Forecast ({horizon}d)", line=dict(color="#ffb800", width=2.4)))
fig.update_layout(template="plotly_dark", height=560,
                  paper_bgcolor="#0b0f1a", plot_bgcolor="#0b0f1a",
                  margin=dict(l=10, r=10, t=30, b=10),
                  legend=dict(orientation="h", y=1.05))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Forecast table")
st.dataframe(res["forecast"], use_container_width=True)
