import pandas as pd


def run_backtest(df: pd.DataFrame, strategy, initial_balance: float = 10000) -> dict:
    signals = strategy.generate_signals(df)
    returns = df["close"].pct_change().fillna(0)

    # position is previous signal to avoid look-ahead bias
    position = signals.shift(1).fillna(0)
    strategy_returns = position * returns

    equity_curve = initial_balance * (1 + strategy_returns).cumprod()
    total_return = (equity_curve.iloc[-1] / initial_balance) - 1
    max_drawdown = ((equity_curve.cummax() - equity_curve) / equity_curve.cummax()).max()

    return {
        "initial_balance": round(initial_balance, 2),
        "final_balance": round(float(equity_curve.iloc[-1]), 2),
        "total_return_pct": round(float(total_return * 100), 2),
        "max_drawdown_pct": round(float(max_drawdown * 100), 2),
        "trading_rows": int(len(df)),
    }
