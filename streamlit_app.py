import io
from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Gold Price Forecast Dashboard", layout="wide")


@dataclass
class ForecastResult:
    forecast_df: pd.DataFrame
    residual_std: float
    model: Ridge


def _infer_price_column(df: pd.DataFrame) -> str:
    candidates = ["close", "price", "adj close", "adj_close", "last"]
    lower_map = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lower_map:
            return lower_map[c]

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric column found for price.")
    return numeric_cols[0]


def _build_features(series: pd.Series, idx: int, lags: list[int]) -> np.ndarray:
    # idx is the position to forecast/build features for.
    t = float(idx)

    feat = [
        t,
        t**2,
        np.sin(2 * np.pi * t / 7),
        np.cos(2 * np.pi * t / 7),
        np.sin(2 * np.pi * t / 30),
        np.cos(2 * np.pi * t / 30),
        np.sin(2 * np.pi * t / 365),
        np.cos(2 * np.pi * t / 365),
    ]

    for lag in lags:
        feat.append(float(series.iloc[idx - lag]))

    return np.array(feat, dtype=float)


def train_and_forecast(data: pd.DataFrame, horizon: int, alpha: float = 1.0) -> ForecastResult:
    data = data.copy()
    data = data.sort_values("date").reset_index(drop=True)
    series = data["price"].astype(float)

    lags = [1, 2, 3, 7, 14]
    min_idx = max(lags)

    X, y = [], []
    for i in range(min_idx, len(series)):
        X.append(_build_features(series, i, lags))
        y.append(series.iloc[i])

    X = np.array(X)
    y = np.array(y)

    if len(X) < 25:
        raise ValueError(
            "Not enough rows to train. Please provide at least ~40 rows of data for better forecasting."
        )

    model = Ridge(alpha=alpha)
    model.fit(X, y)

    train_pred = model.predict(X)
    residual_std = float(np.std(y - train_pred))

    # Recursive future forecasting
    extended = series.copy()
    preds = []
    for step in range(horizon):
        idx = len(extended)
        x_next = _build_features(extended, idx, lags).reshape(1, -1)
        yhat = float(model.predict(x_next)[0])
        preds.append(yhat)
        extended = pd.concat([extended, pd.Series([yhat])], ignore_index=True)

    last_date = data["date"].max()
    freq = pd.infer_freq(data["date"])
    if freq is None:
        # Fallback: guess daily if no clear frequency
        freq = "D"

    future_dates = pd.date_range(start=last_date, periods=horizon + 1, freq=freq)[1:]

    z = 1.96
    pred_arr = np.array(preds)
    ci_width = z * residual_std

    forecast_df = pd.DataFrame(
        {
            "date": future_dates,
            "forecast": pred_arr,
            "lower": pred_arr - ci_width,
            "upper": pred_arr + ci_width,
        }
    )

    return ForecastResult(forecast_df=forecast_df, residual_std=residual_std, model=model)


def quick_backtest(data: pd.DataFrame, test_size: int = 30) -> tuple[float, float] | tuple[None, None]:
    data = data.sort_values("date").reset_index(drop=True)
    if len(data) < test_size + 40:
        return None, None

    train = data.iloc[:-test_size].copy()
    test = data.iloc[-test_size:].copy()

    result = train_and_forecast(train, horizon=test_size)
    y_true = test["price"].values
    y_pred = result.forecast_df["forecast"].values

    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return float(mae), float(rmse)


def plot_history(data: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["price"],
            mode="lines",
            name="Historical Price",
            line=dict(width=2),
        )
    )
    fig.update_layout(
        title="Historical Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_forecast(data: pd.DataFrame, forecast_df: pd.DataFrame):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["price"],
            mode="lines",
            name="Historical",
            line=dict(color="#1f77b4", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["date"],
            y=forecast_df["forecast"],
            mode="lines",
            name="Forecast",
            line=dict(color="#ff7f0e", width=2, dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["date"],
            y=forecast_df["upper"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df["date"],
            y=forecast_df["lower"],
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(255,127,14,0.2)",
            line=dict(width=0),
            name="95% CI",
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        title="Future Price Forecast",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=520,
    )
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title("🥇 Gold Price Forecast Dashboard")
    st.caption("Upload gold price data or fetch from Yahoo ticker (default: GC=F), then visualize and forecast future prices.")

    with st.sidebar:
        st.header("Data Source")
        source = st.radio("Choose source", ["Upload CSV", "Ticker (Yahoo Finance)"])
        horizon = st.slider("Forecast horizon (periods)", min_value=5, max_value=180, value=30)
        ridge_alpha = st.slider("Model regularization (alpha)", min_value=0.0, max_value=20.0, value=1.0)

    data = None

    if source == "Upload CSV":
        uploaded = st.file_uploader("Upload CSV (must include a date column and a price column)", type=["csv"])
        if uploaded is not None:
            raw = pd.read_csv(io.BytesIO(uploaded.getvalue()))
            date_candidates = [c for c in raw.columns if "date" in c.lower() or "time" in c.lower()]
            date_col = date_candidates[0] if date_candidates else raw.columns[0]
            price_col = _infer_price_column(raw)

            parsed = pd.DataFrame(
                {
                    "date": pd.to_datetime(raw[date_col], errors="coerce"),
                    "price": pd.to_numeric(raw[price_col], errors="coerce"),
                }
            ).dropna()

            data = parsed.sort_values("date").drop_duplicates(subset=["date"]).reset_index(drop=True)
            st.success(f"Loaded {len(data)} rows. Date: '{date_col}', Price: '{price_col}'")

    else:
        ticker = st.text_input("Ticker", value="GC=F")
        period = st.selectbox("History period", ["6mo", "1y", "2y", "5y", "10y"], index=2)
        if st.button("Fetch data"):
            try:
                import yfinance as yf

                df = yf.download(ticker, period=period, interval="1d", auto_adjust=False, progress=False)
                if df.empty:
                    st.error("No data returned. Check ticker symbol.")
                else:
                    df = df.reset_index()
                    price_col = "Close" if "Close" in df.columns else df.select_dtypes(include=[np.number]).columns[0]
                    data = pd.DataFrame({"date": pd.to_datetime(df["Date"]), "price": pd.to_numeric(df[price_col])}).dropna()
                    st.success(f"Fetched {len(data)} rows for {ticker}.")
            except Exception as e:
                st.error(f"Failed to fetch ticker data: {e}")

    if data is None:
        st.info("Provide data to begin forecasting.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", len(data))
    c2.metric("Latest Price", f"{data['price'].iloc[-1]:.2f}")
    c3.metric("Date Range", f"{data['date'].min().date()} → {data['date'].max().date()}")

    plot_history(data)

    try:
        result = train_and_forecast(data, horizon=horizon, alpha=ridge_alpha)
        plot_forecast(data, result.forecast_df)

        mae, rmse = quick_backtest(data, test_size=min(30, max(10, len(data) // 8)))
        if mae is not None and rmse is not None:
            st.subheader("Backtest Metrics")
            m1, m2 = st.columns(2)
            m1.metric("MAE", f"{mae:.4f}")
            m2.metric("RMSE", f"{rmse:.4f}")

        st.subheader("Forecast Table")
        st.dataframe(result.forecast_df, use_container_width=True)

        csv = result.forecast_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download forecast CSV",
            data=csv,
            file_name="forecast.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Forecasting failed: {e}")


if __name__ == "__main__":
    main()
