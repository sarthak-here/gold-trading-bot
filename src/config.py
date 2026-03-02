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

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            broker=os.getenv("BROKER", "paper"),
            symbol=os.getenv("SYMBOL", "XAUUSD"),
            timeframe=os.getenv("TIMEFRAME", "15m"),
            risk_per_trade=float(os.getenv("RISK_PER_TRADE", "0.01")),
            initial_balance=float(os.getenv("INITIAL_BALANCE", "10000")),
        )
