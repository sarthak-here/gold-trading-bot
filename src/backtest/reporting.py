import json
from datetime import datetime
from pathlib import Path

import pandas as pd


def save_backtest_outputs(report: dict, equity_df: pd.DataFrame, trades_df: pd.DataFrame, base_dir: str = "reports") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(base_dir) / f"backtest-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    equity_df.to_csv(out_dir / "equity_curve.csv", index=False)
    trades_df.to_csv(out_dir / "trades.csv", index=False)

    return out_dir
