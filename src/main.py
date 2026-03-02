import argparse
from src.config import Settings
from src.data.feed import get_mock_data
from src.strategy.ma_crossover import MovingAverageCrossover
from src.backtest.engine import run_backtest


def main() -> None:
    parser = argparse.ArgumentParser(description="Gold trading bot starter")
    parser.add_argument("--mode", choices=["backtest", "paper"], default="backtest")
    args = parser.parse_args()

    settings = Settings.from_env()

    if args.mode == "backtest":
        df = get_mock_data()
        strategy = MovingAverageCrossover(short_window=20, long_window=50)
        report = run_backtest(df=df, strategy=strategy, initial_balance=settings.initial_balance)
        print("=== Backtest Report ===")
        for k, v in report.items():
            print(f"{k}: {v}")
    else:
        print("Paper mode scaffold ready. Live loop integration is next.")


if __name__ == "__main__":
    main()
