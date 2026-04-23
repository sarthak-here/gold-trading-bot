# Gold Trading Bot - System Design

## What It Does
An AI-powered trading system for gold (XAUUSD). Forecasts gold prices using time-series
models, generates entry/exit signals with ATR-based stop-losses and risk-adjusted
position sizing, and presents everything in a Streamlit dashboard with backtesting.

---

## Architecture

```
XAUUSD price data (OHLCV)
        |
        v
+--------------------------------------------------+
|          Data Pipeline                           |
|  Fetch historical XAUUSD via yfinance            |
|  Technical indicators: SMA, EMA, RSI,           |
|  MACD, ATR, Bollinger Bands                     |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|          Forecasting Engine                      |
|  Time-series models:                             |
|  - ARIMA / SARIMA                                |
|  - Prophet (trend + seasonality)                 |
|  - LSTM / ML ensemble                            |
|  Output: N-day forecast + confidence bands       |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|          Signal Generator                        |
|  Combine: forecast direction + technical signals |
|  Output: BUY / SELL / HOLD                       |
|  Risk management:                                |
|  - stop_loss = entry - 2 x ATR(14)               |
|  - position  = (capital x risk%) / risk_per_share|
|  - Confidence gating: suppress low-conf signals  |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|     Streamlit Dashboard                          |
|  Price chart + forecast overlay                  |
|  Confidence bands (80% and 95%)                  |
|  Signal history, backtest metrics               |
|  Sharpe ratio, max drawdown, win rate            |
|  Position sizing calculator                      |
+--------------------------------------------------+
```

---

## Data Flow

```
XAUUSD OHLCV (daily)
        |
  Technical indicators (SMA20, EMA50, RSI14, MACD, ATR14, BBands)
        |
  Forecasting:
    ARIMA:   fit on closing prices -> N-day price forecast
    Prophet: trend + seasonality decomposition
    Confidence bands: 80% and 95% prediction intervals
        |
  Signal logic:
    IF forecast UP AND RSI < 70  -> BUY
    IF forecast DOWN AND RSI > 30 -> SELL
    ELSE                          -> HOLD
    IF confidence < threshold     -> suppress signal
        |
  Risk management:
    stop_loss = entry - 2 x ATR(14)
    position  = (capital x risk_pct) / (entry - stop_loss)
        |
  Walk-forward backtest:
    Train on first N days -> test on next M days
    Roll forward; compute Sharpe, drawdown, win rate
        |
  Streamlit renders:
    Plotly chart + forecast bands + signal table + backtest summary
```

---

## Key Design Decisions

| Decision                        | Reason                                           |
|---------------------------------|--------------------------------------------------|
| Confidence bands in forecast    | Shows uncertainty; suppresses low-confidence signals|
| ATR-based stop-loss             | Volatility-adjusted; avoids normal fluctuation stops|
| Walk-forward backtest           | No look-ahead bias; simulates real trading       |
| Multiple model support          | No single model dominates all market regimes     |
| Confidence threshold gating     | High uncertainty = no trade; preserves capital   |

---

## Interview Conclusion

The gold trading bot separates three concerns: forecasting (what will the price be?),
signal generation (should I trade?), and risk management (how much to risk?). This
separation is important because each component has different failure modes: the forecast
can be wrong about direction but risk management still limits losses. Confidence bands
force the user to understand model uncertainty, and the threshold gate automatically
suppresses trades when uncertainty is too high. The walk-forward backtester is critical
for honest evaluation -- a standard backtest using future data to train will always look
profitable on any strategy. Live trading improvements: broker API integration (Zerodha),
30-day paper trading period for live validation, and circuit breakers halting the bot
if daily drawdown exceeds 2%.
