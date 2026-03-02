# Gold Trading Bot (XAUUSD)

A starter Python project for building, backtesting, and running a gold trading bot.

## Scope (v0)
- Data ingestion (historical + live placeholders)
- Strategy interface + sample MA crossover strategy
- Risk management hooks
- Paper trading executor
- Simple backtest runner

## Quick start
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.main --mode backtest
```

## Next milestones
1. Connect broker/data provider
2. Add robust position sizing + SL/TP rules
3. Add logging, metrics, and reports
4. Add live paper-trading loop
5. Add tests for strategy and risk modules

## Disclaimer
This code is for education/research. Trading is risky. Use paper trading first.
