from dataclasses import dataclass


@dataclass
class RiskManager:
    risk_per_trade: float = 0.01
    stop_loss_pct: float = 0.01
    take_profit_pct: float = 0.02
    max_position_notional_pct: float = 1.0

    def position_notional(self, equity: float, entry_price: float) -> float:
        """Capital allocation based on risk per trade and stop-loss distance."""
        if entry_price <= 0 or self.stop_loss_pct <= 0:
            return 0.0

        risk_amount = equity * self.risk_per_trade
        notional_from_risk = risk_amount / self.stop_loss_pct
        capped_notional = min(notional_from_risk, equity * self.max_position_notional_pct)
        return max(capped_notional, 0.0)
