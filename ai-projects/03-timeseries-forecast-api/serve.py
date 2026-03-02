from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Time-Series Forecast API")


class ForecastRequest(BaseModel):
    values: list[float]


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/forecast")
def forecast(req: ForecastRequest):
    if not req.values:
        return {"forecast": None, "error": "empty series"}
    # Stub: naive forecast = last value
    return {"forecast": req.values[-1], "method": "naive_last"}
