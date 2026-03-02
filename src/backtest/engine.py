import pandas as pd


from src.risk.manager import RiskManager


def run_backtest(
    df: pd.DataFrame,
    strategy,
    initial_balance: float = 10000,
    risk_manager: RiskManager | None = None,
) -> dict:
    if risk_manager is None:
        risk_manager = RiskManager()

    signals = strategy.generate_signals(df).fillna(0)
    prices = df["close"].reset_index(drop=True)

    equity = float(initial_balance)
    peak_equity = equity
    max_drawdown = 0.0

    in_position = False
    side = 0  # 1 long, -1 short
    units = 0.0
    entry_price = 0.0
    stop_price = 0.0
    take_profit_price = 0.0

    trades = 0
    wins = 0

    for i in range(1, len(prices)):
        price = float(prices.iloc[i])
        signal = int(signals.iloc[i - 1])  # avoid look-ahead

        # Exit logic for open position
        if in_position:
            exit_now = False
            pnl = 0.0

            if side == 1:  # long
                if price <= stop_price or price >= take_profit_price:
                    pnl = units * (price - entry_price)
                    exit_now = True
            else:  # short
                if price >= stop_price or price <= take_profit_price:
                    pnl = units * (entry_price - price)
                    exit_now = True

            if exit_now:
                equity += pnl
                trades += 1
                if pnl > 0:
                    wins += 1
                in_position = False
                side = 0
                units = 0.0

        # Entry logic (only when flat)
        if not in_position and signal in (1, -1):
            notional = risk_manager.position_notional(equity=equity, entry_price=price)
            if notional > 0:
                units = notional / price
                side = signal
                entry_price = price
                if side == 1:
                    stop_price = entry_price * (1 - risk_manager.stop_loss_pct)
                    take_profit_price = entry_price * (1 + risk_manager.take_profit_pct)
                else:
                    stop_price = entry_price * (1 + risk_manager.stop_loss_pct)
                    take_profit_price = entry_price * (1 - risk_manager.take_profit_pct)
                in_position = True

        # Mark-to-market for drawdown tracking
        mtm_equity = equity
        if in_position:
            if side == 1:
                mtm_equity += units * (price - entry_price)
            else:
                mtm_equity += units * (entry_price - price)

        peak_equity = max(peak_equity, mtm_equity)
        if peak_equity > 0:
            dd = (peak_equity - mtm_equity) / peak_equity
            max_drawdown = max(max_drawdown, dd)

    # Close open position at final price
    if in_position:
        final_price = float(prices.iloc[-1])
        pnl = units * (final_price - entry_price) if side == 1 else units * (entry_price - final_price)
        equity += pnl
        trades += 1
        if pnl > 0:
            wins += 1

    total_return = (equity / initial_balance) - 1
    win_rate = (wins / trades * 100) if trades else 0.0

    return {
        "initial_balance": round(initial_balance, 2),
        "final_balance": round(float(equity), 2),
        "total_return_pct": round(float(total_return * 100), 2),
        "max_drawdown_pct": round(float(max_drawdown * 100), 2),
        "trades": int(trades),
        "win_rate_pct": round(float(win_rate), 2),
        "risk_per_trade_pct": round(risk_manager.risk_per_trade * 100, 2),
        "stop_loss_pct": round(risk_manager.stop_loss_pct * 100, 2),
        "take_profit_pct": round(risk_manager.take_profit_pct * 100, 2),
    }
