"""
Risk Management Engine for the IHSG swing trading system.

Provides ATR-based position sizing, stop-loss calculation, and
chandelier trailing stop management. All risk calculations are
deterministic and based on the ATR volatility measure.

Key rules:
  - Initial stop-loss: 1.5x ATR below entry price
  - Trailing stop: 2x ATR below highest high since entry (chandelier)
  - Position size: (Capital x Risk%) / Risk-per-share
  - Risk per share: Entry - Stop-loss
  - All share counts are rounded DOWN to IDX lot size (100 shares)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from config.settings import (
    IDX_LOT_SIZE,
    MAX_RISK_PER_TRADE_PCT,
    REGIME_RISK_MULTIPLIER,
    STOP_LOSS_ATR_MULTIPLIER,
    TRAILING_STOP_ATR_MULTIPLIER,
)

logger = logging.getLogger(__name__)


# ─── Data Structures ─────────────────────────────────────────────────────────


@dataclass
class TradeRisk:
    """Complete risk profile for a proposed trade."""

    ticker: str
    entry_price: float
    stop_loss: float
    trailing_stop: float
    position_size: int  # shares (rounded to lot size)
    risk_per_share: float
    risk_amount: float  # total IDR at risk
    risk_pct: float  # actual risk as % of capital
    capital: float
    regime: str
    regime_adjusted_risk_pct: float  # risk % after regime adjustment
    reward_target: float | None = None  # optional take-profit level
    reward_risk_ratio: float | None = None

    def __str__(self) -> str:
        lines = [
            f"--- Trade Risk: {self.ticker} ---",
            f"  Entry:          IDR {self.entry_price:>12,.0f}",
            f"  Stop-Loss:      IDR {self.stop_loss:>12,.0f}  "
            f"({self.risk_per_share:,.0f}/share)",
            f"  Trailing Stop:  IDR {self.trailing_stop:>12,.0f}",
            f"  Position Size:  {self.position_size:>12,} shares  "
            f"({self.position_size // IDX_LOT_SIZE} lots)",
            f"  Position Value: IDR {self.entry_price * self.position_size:>12,.0f}",
            f"  Risk Amount:    IDR {self.risk_amount:>12,.0f}  "
            f"({self.risk_pct:.2f}% of capital)",
            f"  Regime:         {self.regime}  "
            f"(risk adj: {self.regime_adjusted_risk_pct:.2f}%)",
        ]
        if self.reward_target and self.reward_risk_ratio:
            lines.append(
                f"  Target:         IDR {self.reward_target:>12,.0f}  "
                f"(R:R = {self.reward_risk_ratio:.1f})"
            )
        return "\n".join(lines)


# ─── Risk Manager ────────────────────────────────────────────────────────────


class RiskManager:
    """
    ATR-based risk management engine.

    All calculations are pure — they take inputs and return results
    without side effects. The Portfolio class handles state.

    Usage:
        rm = RiskManager()
        risk = rm.calculate_trade_risk(
            ticker="BBCA", entry_price=7000, atr_value=150,
            capital=100_000_000, regime="BULL",
        )
        print(risk)
    """

    # ── Stop-Loss ─────────────────────────────────────────────────────

    @staticmethod
    def calculate_stop_loss(
        entry_price: float,
        atr_value: float,
        multiplier: float = STOP_LOSS_ATR_MULTIPLIER,
    ) -> float:
        """
        Calculate the initial stop-loss level.

        Stop = Entry - (ATR x Multiplier)

        Parameters
        ----------
        entry_price : float
            Planned entry price.
        atr_value : float
            Current ATR(14) value.
        multiplier : float
            ATR multiplier (default 1.5).

        Returns
        -------
        float
            Stop-loss price level.
        """
        stop = entry_price - (atr_value * multiplier)
        return max(stop, 0)  # stop can't be negative

    # ── Trailing Stop (Chandelier Exit) ───────────────────────────────

    @staticmethod
    def calculate_trailing_stop(
        highest_high: float,
        atr_value: float,
        multiplier: float = TRAILING_STOP_ATR_MULTIPLIER,
    ) -> float:
        """
        Calculate the chandelier trailing stop level.

        Trail = Highest High Since Entry - (ATR x Multiplier)

        The trailing stop only moves UP, never down. The caller is
        responsible for tracking whether the new stop is higher than
        the current stop.

        Parameters
        ----------
        highest_high : float
            Highest price since position was opened.
        atr_value : float
            Current ATR value.
        multiplier : float
            ATR multiplier (default 2.0).

        Returns
        -------
        float
            New trailing stop level.
        """
        trail = highest_high - (atr_value * multiplier)
        return max(trail, 0)

    # ── Position Sizing ───────────────────────────────────────────────

    @staticmethod
    def calculate_position_size(
        capital: float,
        entry_price: float,
        stop_loss: float,
        risk_pct: float,
        lot_size: int = IDX_LOT_SIZE,
    ) -> int:
        """
        Calculate the number of shares to buy.

        Shares = (Capital x Risk%) / Risk-per-share
        Result is rounded DOWN to the nearest lot size.

        Parameters
        ----------
        capital : float
            Total available capital.
        entry_price : float
            Planned entry price.
        stop_loss : float
            Stop-loss price level.
        risk_pct : float
            Risk as a percentage of capital (e.g., 2.0 for 2%).
        lot_size : int
            IDX lot size (default 100).

        Returns
        -------
        int
            Number of shares (rounded to lot size).
        """
        risk_per_share = entry_price - stop_loss
        if risk_per_share <= 0:
            logger.warning(
                "Invalid risk_per_share: %.2f (entry=%.2f, stop=%.2f)",
                risk_per_share, entry_price, stop_loss,
            )
            return 0

        risk_budget = capital * (risk_pct / 100.0)
        raw_shares = risk_budget / risk_per_share

        # Round down to lot size
        lots = int(raw_shares // lot_size)
        return lots * lot_size

    # ── Regime-Adjusted Risk ──────────────────────────────────────────

    @staticmethod
    def adjust_risk_for_regime(
        base_risk_pct: float = MAX_RISK_PER_TRADE_PCT,
        regime: str = "BULL",
    ) -> float:
        """
        Adjust risk percentage based on market regime.

        BULL:    100% of base risk (2.0%)
        CAUTION:  50% of base risk (1.0%)
        BEAR:     25% of base risk (0.5%)

        Returns
        -------
        float
            Regime-adjusted risk percentage.
        """
        multiplier = REGIME_RISK_MULTIPLIER.get(regime.upper(), 0.5)
        return base_risk_pct * multiplier

    # ── Reward:Risk Ratio ─────────────────────────────────────────────

    @staticmethod
    def calculate_reward_risk_ratio(
        entry_price: float,
        stop_loss: float,
        target_price: float,
    ) -> float:
        """
        Calculate the Reward:Risk ratio.

        Returns 0.0 if risk is zero or negative.
        """
        risk = entry_price - stop_loss
        reward = target_price - entry_price
        if risk <= 0:
            return 0.0
        return reward / risk

    # ── Complete Trade Risk Profile ───────────────────────────────────

    def calculate_trade_risk(
        self,
        ticker: str,
        entry_price: float,
        atr_value: float,
        capital: float,
        regime: str = "BULL",
        target_price: float | None = None,
    ) -> TradeRisk:
        """
        Calculate the complete risk profile for a proposed trade.

        This is the main entry point that combines all risk calculations
        into a single TradeRisk object.

        Parameters
        ----------
        ticker : str
            Stock ticker code.
        entry_price : float
            Planned entry price.
        atr_value : float
            Current ATR(14) value.
        capital : float
            Available capital.
        regime : str
            Current market regime ("BULL", "CAUTION", "BEAR").
        target_price : float | None
            Optional take-profit target for R:R calculation.

        Returns
        -------
        TradeRisk
            Complete risk profile.
        """
        # Regime-adjusted risk
        adjusted_risk_pct = self.adjust_risk_for_regime(
            MAX_RISK_PER_TRADE_PCT, regime
        )

        # Stop-loss
        stop_loss = self.calculate_stop_loss(entry_price, atr_value)

        # Trailing stop (initially same as stop-loss area, uses wider multiplier)
        trailing_stop = self.calculate_trailing_stop(entry_price, atr_value)

        # Position size
        position_size = self.calculate_position_size(
            capital, entry_price, stop_loss, adjusted_risk_pct
        )

        # Actual risk
        risk_per_share = entry_price - stop_loss
        risk_amount = position_size * risk_per_share
        actual_risk_pct = (risk_amount / capital * 100) if capital > 0 else 0

        # R:R ratio
        rr_ratio = None
        if target_price and target_price > entry_price:
            rr_ratio = self.calculate_reward_risk_ratio(
                entry_price, stop_loss, target_price
            )

        trade_risk = TradeRisk(
            ticker=ticker,
            entry_price=entry_price,
            stop_loss=round(stop_loss, 2),
            trailing_stop=round(trailing_stop, 2),
            position_size=position_size,
            risk_per_share=round(risk_per_share, 2),
            risk_amount=round(risk_amount, 2),
            risk_pct=round(actual_risk_pct, 4),
            capital=capital,
            regime=regime,
            regime_adjusted_risk_pct=adjusted_risk_pct,
            reward_target=target_price,
            reward_risk_ratio=round(rr_ratio, 2) if rr_ratio else None,
        )

        logger.debug(
            "[%s] Risk: entry=%s stop=%s size=%d risk=IDR %s (%.2f%%)",
            ticker, entry_price, stop_loss, position_size,
            f"{risk_amount:,.0f}", actual_risk_pct,
        )

        return trade_risk
