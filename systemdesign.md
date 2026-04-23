# Gold Trading Bot — System Design

## What It Does
An AI-powered trading system for gold (XAUUSD). It forecasts gold prices using time-series models, generates entry/exit signals with risk-adjusted position sizing, and displays everything in a Streamlit dashboard with backtesting metrics and confidence bands.

---

## Architecture

```
Data Source (gold price OHLCV)
        |
        v
+--------------------------------------------------+
|          Data Pipeline                           |
|  - Fetch historical XAUUSD prices                |
|  - Technical indicator computation               |
|    (SMA, EMA, RSI, MACD, ATR, Bollinger)        |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|          Forecasting Engine                      |
|  Time-series model(s):                           |
|  - ARIMA / SARIMA                                |
|  - Prophet                                       |
|  - LSTM / ML ensemble                            |
|  Output: price forecast + confidence bands       |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|          Signal Generator                        |
|  Combine: forecast direction + technical signals |
|  Output: BUY / SELL / HOLD                       |
|  Risk management:                                |
|  - Stop loss: ATR-based                          |
|  - Position size: % risk per trade               |
|  - Confidence threshold gating                  |
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|     Streamlit Dashboard (app.py)                 |
|  - Gold price chart + forecast overlay           |
|  - Confidence bands                              |
|  - Signal history table                          |
|  - Backtest metrics (Sharpe, drawdown, win rate) |
|  - Position sizing calculator                    |
+--------------------------------------------------+
```

---

## Input

| Input | Detail |
|---|---|
| Gold price data | XAUUSD OHLCV (yfinance or CSV upload) |
| Forecast horizon | Configurable via Streamlit slider (1-30 days) |
| Capital & risk % | User inputs for position sizing |
| Model selection | ARIMA / Prophet / ensemble |

---

## Data Flow

```
XAUUSD price data (daily OHLCV)
        |
  Technical indicators:
  SMA(20), EMA(50), RSI(14), MACD, ATR(14),
  Bollinger Bands, Volume SMA
        |
  Forecasting:
    ARIMA: fit on closing prices -> N-day forecast
    Prophet: trend + seasonality decomposition
    Confidence bands: 80% and 95% prediction intervals
        |
  Signal logic:
    IF forecast_direction == UP AND RSI < 70:
      -> BUY signal
    IF forecast_direction == DOWN AND RSI > 30:
      -> SELL signal
    ELSE:
      -> HOLD
        |
  Risk management:
    stop_loss  = entry - 2 x ATR(14)
    position   = (capital x risk_pct) / (entry - stop_loss)
    confidence = model confidence score (0-1)
    IF confidence < threshold: suppress signal
        |
  Backtester:
    Walk-forward: train on first N days, test on next M
    Metrics: Sharpe ratio, max drawdown, win rate, P&L
        |
  Streamlit renders:
    Plotly chart (price + forecast + bands)
    Signal table, backtest summary, position size output
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| Confidence bands in forecast | Communicates model uncertainty; suppresses low-confidence signals |
| ATR-based stop loss | Volatility-adjusted stops prevent being stopped out by normal gold fluctuation |
| Walk-forward backtest | Avoids look-ahead bias; simulates real trading conditions |
| Multiple model support | No single model dominates across all market regimes |
| Confidence threshold gating | High uncertainty = no trade; preserves capital during unclear conditions |

---

## Interview Conclusion

The gold trading bot addresses one of the hardest problems in quantitative finance: forecasting prices in a noisy, non-stationary market. The architecture separates forecasting (what will the price be?) from signal generation (should I trade?) from risk management (how much should I risk?). This separation is important because each component has different failure modes: the forecast can be wrong about direction but the risk management still limits losses. The confidence band visualization is a key design choice — it forces the user to understand that the model is uncertain, and the confidence threshold gating automatically suppresses trades when the uncertainty is too high. The walk-forward backtester is critical for honest evaluation: a backtest that uses future data to train will always look profitable even on a random strategy. If I were deploying this to live trading, I would add a broker API integration (Interactive Brokers or Zerodha), implement paper trading for a minimum 30-day live validation period, and add circuit breakers that halt the bot if daily drawdown exceeds 2%.
