import streamlit as st
import yfinance as yf
import pandas as pd

COINS = {
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Solana (SOL)": "SOL-USD",
    "BNB": "BNB-USD",
    "XRP": "XRP-USD",
    "Cardano (ADA)": "ADA-USD",
    "Dogecoin (DOGE)": "DOGE-USD",
    "Polygon (MATIC)": "MATIC-USD",
    "Polkadot (DOT)": "DOT-USD",
    "Avalanche (AVAX)": "AVAX-USD",
    "Chainlink (LINK)": "LINK-USD",
    "Litecoin (LTC)": "LTC-USD",
}

@st.cache_data(ttl=300, show_spinner=False)
def load_history(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=False)
    if df.empty:
        return df
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index().rename(columns=str.title)
    if "Date" not in df.columns and "Datetime" in df.columns:
        df = df.rename(columns={"Datetime": "Date"})
    return df

@st.cache_data(ttl=120, show_spinner=False)
def latest_quote(symbol: str) -> dict:
    df = load_history(symbol, period="5d", interval="1d")
    if df.empty:
        return {}
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else last
    price = float(last["Close"])
    change = price - float(prev["Close"])
    pct = (change / float(prev["Close"]) * 100) if float(prev["Close"]) else 0.0
    return {"price": price, "change": change, "pct": pct}
