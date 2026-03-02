import pandas as pd
from src.strategy.base import Strategy


class MovingAverageCrossover(Strategy):
    def __init__(self, short_window: int = 20, long_window: int = 50) -> None:
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        price = df["close"]
        short_ma = price.rolling(self.short_window).mean()
        long_ma = price.rolling(self.long_window).mean()

        signal = (short_ma > long_ma).astype(int) - (short_ma < long_ma).astype(int)
        return signal.fillna(0)
