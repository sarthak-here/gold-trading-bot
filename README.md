# Gold Trading Bot (XAUUSD)

A starter Python project for building, backtesting, and running a gold trading bot.

## Scope (v0)
- Data ingestion (historical + live placeholders)
- Strategy interface + sample MA crossover strategy
- Risk manager (position sizing + SL/TP)
- Paper trading executor
- Simple backtest runner

## Quick start
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.main --mode backtest --source yfinance
```

## Next milestones
1. Connect broker/data provider
2. Add robust position sizing + SL/TP rules
3. Add logging, metrics, and reports
4. Add live paper-trading loop
5. Add tests for strategy and risk modules

## Risk settings (.env)
- `RISK_PER_TRADE` (e.g. 0.01 = 1% equity risk per trade)
- `STOP_LOSS_PCT` (e.g. 0.01 = 1% stop)
- `TAKE_PROFIT_PCT` (e.g. 0.02 = 2% target)
- `MAX_POSITION_NOTIONAL_PCT` (cap exposure, 1.0 = 100% equity)

## Disclaimer
This code is for education/research. Trading is risky. Use paper trading first.
