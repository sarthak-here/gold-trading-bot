import argparse
from src.config import Settings
from src.data.feed import get_mock_data, get_yfinance_data
from src.strategy.ma_crossover import MovingAverageCrossover
from src.backtest.engine import run_backtest


def main() -> None:
    parser = argparse.ArgumentParser(description="Gold trading bot starter")
    parser.add_argument("--mode", choices=["backtest", "paper"], default="backtest")
    parser.add_argument("--source", choices=["auto", "yfinance", "mock"], default="auto")
    args = parser.parse_args()

    settings = Settings.from_env()

    if args.mode == "backtest":
        source = args.source if args.source != "auto" else settings.data_provider

        if source == "yfinance":
            df = get_yfinance_data(
                symbol=settings.yfinance_symbol,
                timeframe=settings.timeframe,
                period=settings.yfinance_period,
            )
            print(f"Using yfinance data: {settings.yfinance_symbol}, tf={settings.timeframe}, period={settings.yfinance_period}")
        else:
            df = get_mock_data()
            print("Using mock data")

        strategy = MovingAverageCrossover(short_window=20, long_window=50)
        report = run_backtest(df=df, strategy=strategy, initial_balance=settings.initial_balance)
        print("=== Backtest Report ===")
        for k, v in report.items():
            print(f"{k}: {v}")
    else:
        print("Paper mode scaffold ready. Live loop integration is next.")


if __name__ == "__main__":
    main()
