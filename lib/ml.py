import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["Return"] = d["Close"].pct_change()
    d["MA5"] = d["Close"].rolling(5).mean()
    d["MA10"] = d["Close"].rolling(10).mean()
    d["MA20"] = d["Close"].rolling(20).mean()
    d["STD10"] = d["Close"].rolling(10).std()
    d["Momentum"] = d["Close"] - d["Close"].shift(5)
    d["Vol_chg"] = d["Volume"].pct_change()
    for lag in (1, 2, 3, 5, 7):
        d[f"Lag_{lag}"] = d["Close"].shift(lag)
    d = d.dropna().reset_index(drop=True)
    return d

FEATURES = ["MA5", "MA10", "MA20", "STD10", "Momentum", "Vol_chg",
            "Lag_1", "Lag_2", "Lag_3", "Lag_5", "Lag_7"]

def train_and_predict(df: pd.DataFrame, horizon: int = 7, model_name: str = "Random Forest"):
    feat = build_features(df)
    if len(feat) < 60:
        raise ValueError("Not enough data to train (need ~60+ rows).")

    X = feat[FEATURES].values
    y = feat["Close"].values

    split = int(len(feat) * 0.85)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = RandomForestRegressor(n_estimators=300, random_state=42) \
        if model_name == "Random Forest" else LinearRegression()
    model.fit(X_train, y_train)

    y_pred_test = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_pred_test))
    r2 = float(r2_score(y_test, y_pred_test))

    # Iterative forecast
    last_row = feat.iloc[-1].copy()
    history_close = list(feat["Close"].values)
    future = []
    for _ in range(horizon):
        feats = {
            "MA5": np.mean(history_close[-5:]),
            "MA10": np.mean(history_close[-10:]),
            "MA20": np.mean(history_close[-20:]),
            "STD10": np.std(history_close[-10:]),
            "Momentum": history_close[-1] - history_close[-5],
            "Vol_chg": 0.0,
            "Lag_1": history_close[-1],
            "Lag_2": history_close[-2],
            "Lag_3": history_close[-3],
            "Lag_5": history_close[-5],
            "Lag_7": history_close[-7],
        }
        x = np.array([[feats[f] for f in FEATURES]])
        pred = float(model.predict(x)[0])
        future.append(pred)
        history_close.append(pred)

    test_df = pd.DataFrame({
        "Date": feat["Date"].iloc[split:].values,
        "Actual": y_test,
        "Predicted": y_pred_test,
    })
    future_dates = pd.date_range(
        start=pd.to_datetime(feat["Date"].iloc[-1]) + pd.Timedelta(days=1),
        periods=horizon, freq="D"
    )
    forecast_df = pd.DataFrame({"Date": future_dates, "Forecast": future})

    return {"mae": mae, "r2": r2, "test": test_df, "forecast": forecast_df}
