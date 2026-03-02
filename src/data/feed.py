import numpy as np
import pandas as pd


def get_mock_data(rows: int = 500) -> pd.DataFrame:
    """Generate synthetic OHLC-like close data for scaffolding."""
    np.random.seed(42)
    returns = np.random.normal(loc=0.0002, scale=0.005, size=rows)
    price = 2000 * (1 + returns).cumprod()
    df = pd.DataFrame({"close": price})
    return df
