import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    broker: str
    symbol: str
    timeframe: str
    risk_per_trade: float
    initial_balance: float
    data_provider: str
    yfinance_symbol: str
    yfinance_period: str

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            broker=os.getenv("BROKER", "paper"),
            symbol=os.getenv("SYMBOL", "XAUUSD"),
            timeframe=os.getenv("TIMEFRAME", "15m"),
            risk_per_trade=float(os.getenv("RISK_PER_TRADE", "0.01")),
            initial_balance=float(os.getenv("INITIAL_BALANCE", "10000")),
            data_provider=os.getenv("DATA_PROVIDER", "yfinance"),
            yfinance_symbol=os.getenv("YFINANCE_SYMBOL", "GC=F"),
            yfinance_period=os.getenv("YFINANCE_PERIOD", "60d"),
        )
