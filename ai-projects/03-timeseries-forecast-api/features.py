import pandas as pd


def make_lag_features(series: pd.Series, lags: int = 3) -> pd.DataFrame:
    df = pd.DataFrame({"y": series})
    for i in range(1, lags + 1):
        df[f"lag_{i}"] = df["y"].shift(i)
    return df.dropna().reset_index(drop=True)
