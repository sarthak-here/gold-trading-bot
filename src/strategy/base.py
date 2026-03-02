from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """Return signal series with values in {-1, 0, 1}."""
