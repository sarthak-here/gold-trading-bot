import numpy as np
import pandas as pd
import yfinance as yf


def get_mock_data(rows: int = 500) -> pd.DataFrame:
    """Generate synthetic OHLC-like close data for scaffolding."""
    np.random.seed(42)
    returns = np.random.normal(loc=0.0002, scale=0.005, size=rows)
    price = 2000 * (1 + returns).cumprod()
    return pd.DataFrame({"close": price})


def _interval_from_timeframe(timeframe: str) -> str:
    mapping = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "60m",
        "4h": "60m",
        "1d": "1d",
    }
    return mapping.get(timeframe, "15m")


def get_yfinance_data(symbol: str = "GC=F", timeframe: str = "15m", period: str = "60d") -> pd.DataFrame:
    """Fetch real market data from Yahoo Finance and normalize to a close-price DataFrame."""
    interval = _interval_from_timeframe(timeframe)
    df = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=True)

    if df.empty:
        raise ValueError(f"No data returned from yfinance for symbol={symbol}, interval={interval}, period={period}")

    if "Close" not in df.columns:
        raise ValueError("yfinance response missing 'Close' column")

    out = df[["Close"]].rename(columns={"Close": "close"}).dropna().reset_index(drop=True)
    if out.empty:
        raise ValueError("No usable close prices found after cleanup")
    return out
