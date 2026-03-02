# 03 — Time-Series Forecast API

## Goal
Forecast demand/price using historical sequences, exposed via API.

## Stack
- Python, FastAPI
- pandas, numpy
- statsmodels (ARIMA)
- Prophet or LightGBM (optional)

## Math / Core concepts
- Stationarity & differencing
- ARIMA(p,d,q)
- MAE, RMSE, MAPE metrics
- Rolling-window validation

## Planned files
- `features.py`
- `train.py`
- `serve.py`
