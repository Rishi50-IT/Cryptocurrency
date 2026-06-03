import streamlit as st
from PIL import Image
from lib.ui import inject, sidebar_user
from streamlit_extras.let_it_rain import rain


inject()
sidebar_user()
rain(
    emoji="🪙",
    font_size=50,
    falling_speed=5,
    animation_length="6s",
) 


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
st.header("CryptoPredictor – AI-Powered Cryptocurrency Analytics Platform")


st.markdown("**CryptoPredictor is a modern cryptocurrency analytics and prediction platform built with Streamlit, Machine Learning, MongoDB, and real-time market data APIs. The platform helps traders and investors monitor market trends, analyze cryptocurrency performance, manage portfolios, and generate AI-based price forecasts through an interactive dashboard.**")
img = Image.open("cry.png", mode="r")

# Width same, height smaller
img = img.resize((1600, 600))

st.image(img, use_container_width=True)
st.markdown("""### Key Features:
- **Live Candlestick Charts**: Real-time interactive charts with moving averages and volume indicators.
- **AI Price Forecasting**: Machine learning models (Random Forest, Linear Regression) to predict future price movements.
- **Portfolio Management**: Track your cryptocurrency holdings and performance over time.
- **Watchlist**: Create and manage a personalized watchlist of cryptocurrencies.
- **User Authentication**: Secure login system with MongoDB to save user data and preferences.           
""")
st.markdown("""### Project Goal:

The goal of CryptoPredictor is to provide traders, investors, and crypto enthusiasts with an intelligent platform that combines real-time market analytics, portfolio management, and machine learning predictions to support better investment decisions in the cryptocurrency market.""")

st.markdown("""### Tech Stack:
- **Frontend**: Streamlit for building the interactive user interface.  
- **Backend**: Python for data processing, machine learning, and API integration.
- **Database**: MongoDB for storing user data, watchlists, and portfolio information.
- **Machine Learning**: Scikit-learn for building predictive models.
- **APIs**: CoinGecko API for fetching real-time cryptocurrency market data.
- **Deployment**: Local deployment and Streamlit cloud deployment with Streamlit, with potential for future cloud deployment.""")
if st.button("Login"):
     
     st.switch_page("pages/Login.py")
   