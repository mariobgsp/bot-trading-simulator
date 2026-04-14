"""
Markdown report generator for the IHSG swing trading system.

Converts the JSON tracking and portfolio data into human-readable
markdown files with clear explanations, tables, and commentary.

Generated files:
  - ``data/daily_tracking.md``  — daily scan + midday eval history
  - ``data/paper_portfolio.md`` — paper trading portfolio status + trade log

Both files are regenerated on every save, reflecting the latest data.
They are committed to the repo by GitHub Actions for easy reading on GitHub.
"""

from __future__ import annotations

import json
import logging
import math
from datetime import datetime
from pathlib import Path

from config.settings import PROJECT_ROOT

logger = logging.getLogger(__name__)

TRACKING_JSON = PROJECT_ROOT / "data" / "daily_tracking.json"
TRACKING_MD = PROJECT_ROOT / "data" / "daily_tracking.md"
PORTFOLIO_JSON = PROJECT_ROOT / "data" / "paper_portfolio.json"
PORTFOLIO_MD = PROJECT_ROOT / "data" / "paper_portfolio.md"


# ── Helpers ──────────────────────────────────────────────────────────────────


def _fmt_idr(value: float | None) -> str:
    """Format a number as IDR currency string."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    return f"IDR {value:,.0f}"


def _fmt_pct(value: float | None) -> str:
    """Format a percentage with sign."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    return f"{value:+.2f}%"


def _regime_badge(regime: str) -> str:
    """Return an emoji badge for the regime."""
    badges = {
        "BULL": "🟢 BULL",
        "CAUTION": "🟡 CAUTION",
        "BEAR": "🔴 BEAR",
    }
    return badges.get(regime, regime)


def _regime_explanation(regime: str) -> str:
    """Return a short explanation of what the regime means."""
    explanations = {
        "BULL": (
            "The market is in a bullish trend (Hurst > 0.55). "
            "All entry engines are active. Full position sizing applies."
        ),
        "CAUTION": (
            "The market shows mean-reverting behavior (Hurst < 0.45). "
            "Only selected engines are active (FVG, B.O.W., EMA, VCLR, QST, Wyckoff). "
            "Position sizes are halved."
        ),
        "BEAR": (
            "The market is range-bound or random-walk (Hurst 0.45–0.55). "
            "Only B.O.W. and Wyckoff Spring engines are active. "
            "Position sizes are quartered."
        ),
    }
    return explanations.get(regime, "Unknown regime.")


def _engine_explanation(engine: str) -> str:
    """Return a short explanation of the entry engine."""
    explanations = {
        "fvg_pullback": "📊 FVG Pullback — Price pulled back into a Fair Value Gap zone and bounced",
        "momentum_breakout": "🚀 Momentum Breakout — Price broke above a tight consolidation range on high volume",
        "buying_on_weakness": "📉 Buying on Weakness — Extreme capitulation detected, reversal candle with volume climax",
        "wyckoff_spring": "🔄 Wyckoff Spring — False breakdown below support with recovery, classic accumulation signal",
        "volume_climax_reversal": "💥 Volume Climax Reversal — Massive volume selling exhaustion followed by bullish reversal",
        "ema_crossover": "✨ EMA Crossover — Short-term EMA crossed above long-term EMA with momentum confirmation",
        "quick_swing_trade": "⚡ Quick Swing Trade — Short-term RSI momentum shift with EMA reclaim and volume",
    }
    return explanations.get(engine, engine)


def _exit_reason_explanation(reason: str) -> str:
    """Return a human-readable exit reason."""
    explanations = {
        "trailing_stop": "📉 Trailing Stop — Price fell below the Chandelier trailing stop level",
        "stop_loss": "🛑 Stop Loss — Price hit the initial stop-loss level (1.5x ATR below entry)",
        "take_profit": "🎯 Take Profit — Price reached the take-profit target (3x ATR above entry)",
        "reversal_exit": "🔄 Reversal Exit — Bearish reversal pattern detected within 20-day holding window",
        "profit_lock_exit": "🔒 Profit Lock — Peak profit eroded significantly, exiting to lock remaining gains",
    }
    return explanations.get(reason, reason)


def _condition_explanation(condition: str) -> str:
    """Explain a Wait bucket condition."""
    explanations = {
        "tight_consolidation": "Price is in a tight trading range — watching for breakout",
        "fvg_approach": "Price is approaching a Fair Value Gap zone — watching for pullback entry",
        "vsa_squat_candle": "Volume Spread Analysis detected a squat candle — high volume, narrow range, possible reversal setup",
        "wyckoff_phase_b": "Stock shows Wyckoff Phase B accumulation pattern — smart money building positions",
    }
    return explanations.get(condition, condition)


# ── Daily Tracking Markdown ──────────────────────────────────────────────────


def generate_tracking_markdown() -> Path:
    """
    Convert ``data/daily_tracking.json`` into a human-readable markdown file.

    The markdown is organized by date (most recent first) with clear sections
    for regime, trade signals, wait signals, paper trading, and midday evaluations.

    Returns
    -------
    Path
        Path to the generated markdown file.
    """
    if not TRACKING_JSON.exists():
        logger.warning("No tracking JSON found at %s", TRACKING_JSON)
        return TRACKING_MD

    try:
        data = json.loads(TRACKING_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read tracking JSON: %s", exc)
        return TRACKING_MD

    entries = data.get("entries", [])
    last_updated = data.get("last_updated", "unknown")

    lines: list[str] = []
    lines.append("# 📊 IHSG Swing Trading — Daily Tracking Report")
    lines.append("")
    lines.append(f"> **Last Updated:** {last_updated}")
    lines.append(f"> **Total Entries:** {len(entries)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## How to Read This Report")
    lines.append("")
    lines.append("This file is automatically generated from the daily scan and midday evaluation workflows. "
                 "Each section below represents one scan run, organized by date (most recent first).")
    lines.append("")
    lines.append("- **Daily Scan** entries show the full market analysis: regime, trade signals, wait list, and paper trading activity.")
    lines.append("- **Midday Eval** entries show the intraday health check: macro veto status and position safety checks.")
    lines.append("- Trade signals are stocks the system recommends buying right now.")
    lines.append("- Wait signals are stocks setting up — not ready yet, but on the watchlist.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group entries by date, most recent first
    entries_by_date: dict[str, list[dict]] = {}
    for entry in entries:
        date = entry.get("date", "unknown")
        entries_by_date.setdefault(date, []).append(entry)

    for date in sorted(entries_by_date.keys(), reverse=True):
        date_entries = entries_by_date[date]
        lines.append(f"## 📅 {date}")
        lines.append("")

        for entry in date_entries:
            entry_type = entry.get("type", "unknown")

            if entry_type == "daily_scan":
                lines.extend(_render_daily_scan_entry(entry))
            elif entry_type == "midday_eval":
                lines.extend(_render_midday_entry(entry))

        lines.append("---")
        lines.append("")

    # Write markdown
    TRACKING_MD.parent.mkdir(parents=True, exist_ok=True)
    TRACKING_MD.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Tracking markdown saved to %s", TRACKING_MD)
    return TRACKING_MD


def _render_daily_scan_entry(entry: dict) -> list[str]:
    """Render a daily_scan entry as markdown sections."""
    lines: list[str] = []
    regime = entry.get("regime", "UNKNOWN")
    regime_detail = entry.get("regime_detail", {})

    # ── Regime Section ────────────────────────────────────────────
    lines.append(f"### {_regime_badge(regime)} Market Regime — Daily Scan")
    lines.append("")
    lines.append(f"> {_regime_explanation(regime)}")
    lines.append("")

    if regime_detail:
        lines.append("| Indicator | Value |")
        lines.append("|-----------|-------|")
        lines.append(f"| IHSG Close | {_fmt_idr(regime_detail.get('close'))} |")
        lines.append(f"| SMA(50) | {_fmt_idr(regime_detail.get('sma_short'))} |")
        lines.append(f"| SMA(200) | {_fmt_idr(regime_detail.get('sma_long'))} |")
        lines.append(f"| ATR(14) | {_fmt_idr(regime_detail.get('atr_value'))} |")
        hurst = regime_detail.get("hurst")
        hurst_str = f"{hurst:.2f}" if hurst is not None else "—"
        lines.append(f"| Hurst Exponent | {hurst_str} |")
        lines.append("")

    # ── Scan Summary ──────────────────────────────────────────────
    scan = entry.get("scan_summary", {})
    if scan:
        lines.append("#### 📋 Scan Summary")
        lines.append("")
        lines.append(f"| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Scanned | {scan.get('total_scanned', 0)} |")
        lines.append(f"| With Data | {scan.get('total_with_data', 0)} |")
        lines.append(f"| ❌ Avoid (filtered) | {scan.get('avoid_count', 0)} |")
        lines.append(f"| ⏳ Wait (setting up) | {scan.get('wait_count', 0)} |")
        lines.append(f"| ✅ Trade (actionable) | {scan.get('trade_count', 0)} |")
        lines.append(f"| ⏭️ Skipped | {scan.get('skipped_count', 0)} |")
        lines.append("")

    # ── Trade Signals ─────────────────────────────────────────────
    trades = entry.get("trade_signals", [])
    if trades:
        lines.append("#### 🎯 Trade Signals (Buy Recommendations)")
        lines.append("")
        for i, trade in enumerate(trades, 1):
            ticker = trade.get("ticker", "?")
            engine = trade.get("engine", "?")
            price = trade.get("price")
            score = trade.get("score", 0)
            stop_loss = trade.get("stop_loss")
            position_size = trade.get("position_size")
            risk_pct = trade.get("risk_pct")

            lines.append(f"**{i}. {ticker}** — Score: {score:.2f}")
            lines.append("")
            lines.append(f"- {_engine_explanation(engine)}")
            lines.append(f"- **Entry Price:** {_fmt_idr(price)}")
            lines.append(f"- **Stop Loss:** {_fmt_idr(stop_loss)}")
            if position_size:
                lines.append(f"- **Position Size:** {position_size:,} shares ({position_size // 100} lots)")
            if risk_pct:
                lines.append(f"- **Risk:** {risk_pct:.2f}% of capital")
            lines.append("")
    else:
        lines.append("#### 🎯 Trade Signals")
        lines.append("")
        lines.append("_No trade signals today._")
        lines.append("")

    # ── Wait Signals ──────────────────────────────────────────────
    waits = entry.get("wait_signals", [])
    if waits:
        lines.append(f"#### ⏳ Wait List ({len(waits)} stocks setting up)")
        lines.append("")
        lines.append("| Ticker | Condition | Price |")
        lines.append("|--------|-----------|-------|")
        for w in waits:
            ticker = w.get("ticker", "?")
            condition = w.get("condition", "?")
            price = w.get("price")
            price_str = _fmt_idr(price) if price else "—"
            lines.append(f"| {ticker} | {_condition_explanation(condition)} | {price_str} |")
        lines.append("")

    # ── Paper Trading ─────────────────────────────────────────────
    paper = entry.get("paper_trading")
    if paper:
        lines.append("#### 📝 Paper Trading Activity")
        lines.append("")
        equity = paper.get("equity", 0)
        total_return = paper.get("total_return_pct", 0)
        open_pos = paper.get("open_positions", 0)

        return_emoji = "🟢" if total_return >= 0 else "🔴"
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Equity | {_fmt_idr(equity)} |")
        lines.append(f"| Total Return | {return_emoji} {_fmt_pct(total_return)} |")
        lines.append(f"| Open Positions | {open_pos} |")
        lines.append("")

        entered = paper.get("trades_entered", [])
        if entered:
            lines.append("**Trades Entered Today:**")
            lines.append("")
            lines.append("| Ticker | Shares | Entry Price | Stop Loss | Take Profit | Risk |")
            lines.append("|--------|--------|-------------|-----------|-------------|------|")
            for t in entered:
                lines.append(
                    f"| {t.get('ticker', '?')} "
                    f"| {t.get('shares', 0):,} "
                    f"| {_fmt_idr(t.get('entry_price'))} "
                    f"| {_fmt_idr(t.get('stop_loss'))} "
                    f"| {_fmt_idr(t.get('take_profit'))} "
                    f"| {_fmt_idr(t.get('risk_amount'))} |"
                )
            lines.append("")

        closed = paper.get("trades_closed", [])
        if closed:
            lines.append("**Trades Closed Today:**")
            lines.append("")
            lines.append("| Ticker | P&L | P&L % | Exit Reason | Held |")
            lines.append("|--------|-----|-------|-------------|------|")
            for t in closed:
                pnl = t.get("pnl", 0)
                pnl_emoji = "✅" if pnl > 0 else "❌"
                lines.append(
                    f"| {pnl_emoji} {t.get('ticker', '?')} "
                    f"| {_fmt_idr(pnl)} "
                    f"| {_fmt_pct(t.get('pnl_pct'))} "
                    f"| {_exit_reason_explanation(t.get('exit_reason', '?'))} "
                    f"| {t.get('holding_days', 0)} days |"
                )
            lines.append("")

    lines.append("")
    return lines


def _render_midday_entry(entry: dict) -> list[str]:
    """Render a midday_eval entry as markdown."""
    lines: list[str] = []
    lines.append("### 🕐 Midday Evaluation")
    lines.append("")

    macro_veto = entry.get("macro_veto", False)
    ihsg_change = entry.get("ihsg_daily_change_pct")

    if macro_veto:
        lines.append("> ⚠️ **MACRO VETO TRIGGERED** — IHSG is down significantly. All pending buys cancelled.")
    else:
        lines.append("> ✅ **No macro veto** — Market conditions are acceptable.")
    lines.append("")

    if ihsg_change is not None:
        change_emoji = "🟢" if ihsg_change >= 0 else "🔴"
        lines.append(f"- **IHSG Daily Change:** {change_emoji} {_fmt_pct(ihsg_change)}")
    lines.append("")

    gap_crap = entry.get("gap_and_crap_alerts", [])
    if gap_crap:
        lines.append("**⚠️ Gap-and-Crap Alerts:**")
        lines.append("")
        for alert in gap_crap:
            lines.append(
                f"- **{alert.get('ticker', '?')}**: "
                f"Closing Range = {alert.get('closing_range', 0):.2f} "
                f"(Gap: {_fmt_pct(alert.get('gap_pct'))})"
            )
        lines.append("")

    fakeouts = entry.get("fakeout_alerts", [])
    if fakeouts:
        lines.append("**🚫 Fakeout Breakout Vetoes:**")
        lines.append("")
        for alert in fakeouts:
            lines.append(
                f"- **{alert.get('ticker', '?')}**: "
                f"Projected Vol = {alert.get('projected_volume', 0):,} "
                f"< Avg = {alert.get('avg_volume_20d', 0):,}"
            )
        lines.append("")

    if not gap_crap and not fakeouts:
        lines.append("_No alerts triggered._")
        lines.append("")

    lines.append("")
    return lines


# ── Paper Portfolio Markdown ────────────────────────────────────────────────


def generate_portfolio_markdown() -> Path:
    """
    Convert ``data/paper_portfolio.json`` into a human-readable markdown file.

    Shows portfolio overview, open positions with risk details, closed
    trade history, and performance metrics.

    Returns
    -------
    Path
        Path to the generated markdown file.
    """
    if not PORTFOLIO_JSON.exists():
        logger.warning("No portfolio JSON found at %s", PORTFOLIO_JSON)
        return PORTFOLIO_MD

    try:
        data = json.loads(PORTFOLIO_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read portfolio JSON: %s", exc)
        return PORTFOLIO_MD

    lines: list[str] = []
    lines.append("# 📝 IHSG Paper Trading — Portfolio Report")
    lines.append("")
    lines.append(f"> **Generated:** {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    lines.append("")
    lines.append("This report shows the current state of the paper trading simulator. "
                 "The simulator executes all scanner signals automatically using IDR 5,000,000 "
                 "starting capital with identical risk management rules as the backtester "
                 "(slippage, fees, trailing stops, take-profit levels).")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── Portfolio Overview ────────────────────────────────────────
    initial = data.get("initial_capital", 5_000_000)
    equity = data.get("equity", 0)
    realized_pnl = data.get("total_realized_pnl", 0)
    unrealized_pnl = data.get("total_unrealized_pnl", 0)
    market_value = data.get("total_market_value", 0)
    heat = data.get("portfolio_heat_pct", 0)
    win_rate = data.get("win_rate", 0)
    total_return = data.get("total_return_pct", 0)

    return_emoji = "🟢" if total_return >= 0 else "🔴"

    lines.append("## 💰 Portfolio Overview")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Starting Capital | {_fmt_idr(initial)} |")
    lines.append(f"| Current Equity | {_fmt_idr(equity)} |")
    lines.append(f"| Total Return | {return_emoji} {_fmt_pct(total_return)} |")
    lines.append(f"| Realized P&L | {_fmt_idr(realized_pnl)} |")
    lines.append(f"| Unrealized P&L | {_fmt_idr(unrealized_pnl)} |")
    lines.append(f"| Market Value (Positions) | {_fmt_idr(market_value)} |")
    lines.append(f"| Portfolio Heat | {heat:.2f}% _(max 6%)_ |")
    lines.append(f"| Win Rate | {win_rate:.1f}% |")
    lines.append("")

    # ── Explanation of Key Metrics ────────────────────────────────
    lines.append("<details>")
    lines.append("<summary>📖 What do these metrics mean?</summary>")
    lines.append("")
    lines.append("- **Equity** = Starting capital + all realized P&L. This is the \"bank balance\" after closing trades.")
    lines.append("- **Realized P&L** = Total profit/loss from closed trades (after slippage + broker fees).")
    lines.append("- **Unrealized P&L** = Paper profit/loss on open positions based on current market prices.")
    lines.append("- **Market Value** = Current value of all open positions at market price.")
    lines.append("- **Portfolio Heat** = Total risk exposure as % of initial capital. Capped at 6% to prevent catastrophic drawdowns.")
    lines.append("- **Win Rate** = Percentage of closed trades that were profitable.")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    # ── Open Positions ────────────────────────────────────────────
    positions = data.get("positions", {})
    if positions:
        lines.append(f"## 📊 Open Positions ({len(positions)})")
        lines.append("")

        for ticker, pos in positions.items():
            entry_price = pos.get("entry_price", 0)
            current_price = pos.get("current_price")
            unrealized = pos.get("unrealized_pnl")
            unrealized_pct = pos.get("unrealized_pnl_pct")

            # Handle NaN values from JSON
            if current_price is not None and isinstance(current_price, float) and math.isnan(current_price):
                current_price = None
            if unrealized is not None and isinstance(unrealized, float) and math.isnan(unrealized):
                unrealized = None
            if unrealized_pct is not None and isinstance(unrealized_pct, float) and math.isnan(unrealized_pct):
                unrealized_pct = None

            pnl_emoji = ""
            if unrealized is not None:
                pnl_emoji = "🟢" if unrealized >= 0 else "🔴"

            lines.append(f"### {ticker}")
            lines.append("")
            lines.append(f"| Detail | Value |")
            lines.append(f"|--------|-------|")
            lines.append(f"| Engine | {_engine_explanation(pos.get('engine', '?'))} |")
            lines.append(f"| Entry Date | {pos.get('entry_date', '?')} |")
            lines.append(f"| Entry Price | {_fmt_idr(entry_price)} _(raw: {_fmt_idr(pos.get('raw_entry_price'))})_ |")
            lines.append(f"| Shares | {pos.get('shares', 0):,} ({pos.get('shares', 0) // 100} lots) |")
            lines.append(f"| Position Value | {_fmt_idr(entry_price * pos.get('shares', 0))} |")

            if current_price is not None:
                lines.append(f"| Current Price | {_fmt_idr(current_price)} |")
                lines.append(f"| Unrealized P&L | {pnl_emoji} {_fmt_idr(unrealized)} ({_fmt_pct(unrealized_pct)}) |")

            lines.append(f"| Stop Loss | {_fmt_idr(pos.get('stop_loss'))} |")
            lines.append(f"| Trailing Stop | {_fmt_idr(pos.get('trailing_stop'))} |")
            lines.append(f"| Take Profit | {_fmt_idr(pos.get('take_profit'))} |")
            lines.append(f"| Highest High | {_fmt_idr(pos.get('highest_high'))} |")
            lines.append(f"| Risk Amount | {_fmt_idr(pos.get('risk_amount'))} |")
            lines.append(f"| Regime at Entry | {_regime_badge(pos.get('regime', '?'))} |")
            lines.append(f"| Last Updated | {pos.get('last_updated', '?')} |")
            lines.append("")

    else:
        lines.append("## 📊 Open Positions")
        lines.append("")
        lines.append("_No open positions._")
        lines.append("")

    # ── Closed Trades ─────────────────────────────────────────────
    closed = data.get("closed_trades", [])
    if closed:
        # Calculate stats
        wins = [t for t in closed if t.get("pnl", 0) > 0]
        losses = [t for t in closed if t.get("pnl", 0) <= 0]
        total_wins = sum(t.get("pnl", 0) for t in wins)
        total_losses = sum(t.get("pnl", 0) for t in losses)
        avg_win = total_wins / len(wins) if wins else 0
        avg_loss = total_losses / len(losses) if losses else 0
        avg_holding = sum(t.get("holding_days", 0) for t in closed) / len(closed) if closed else 0

        lines.append(f"## 📈 Closed Trades ({len(closed)})")
        lines.append("")

        lines.append("### Performance Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Trades | {len(closed)} |")
        lines.append(f"| Wins | ✅ {len(wins)} |")
        lines.append(f"| Losses | ❌ {len(losses)} |")
        lines.append(f"| Win Rate | {(len(wins) / len(closed) * 100) if closed else 0:.1f}% |")
        lines.append(f"| Total Realized P&L | {_fmt_idr(realized_pnl)} |")
        lines.append(f"| Average Win | {_fmt_idr(avg_win)} |")
        lines.append(f"| Average Loss | {_fmt_idr(avg_loss)} |")
        lines.append(f"| Average Holding Period | {avg_holding:.1f} days |")
        lines.append("")

        # Trade log table
        lines.append("### Trade Log")
        lines.append("")
        lines.append("| # | Ticker | Engine | Entry → Exit | P&L | P&L % | Reason | Days |")
        lines.append("|---|--------|--------|-------------|-----|-------|--------|------|")

        for i, t in enumerate(reversed(closed), 1):
            pnl = t.get("pnl", 0)
            pnl_emoji = "✅" if pnl > 0 else "❌"
            entry = t.get("entry_price", 0)
            exit_p = t.get("exit_price", 0)
            lines.append(
                f"| {i} "
                f"| {pnl_emoji} {t.get('ticker', '?')} "
                f"| {t.get('engine', '?')} "
                f"| {_fmt_idr(entry)} → {_fmt_idr(exit_p)} "
                f"| {_fmt_idr(pnl)} "
                f"| {_fmt_pct(t.get('pnl_pct'))} "
                f"| {t.get('exit_reason', '?')} "
                f"| {t.get('holding_days', 0)}d |"
            )
        lines.append("")

        # Cost analysis
        lines.append("### Cost Analysis")
        lines.append("")
        lines.append("Every trade includes realistic costs (same as backtester):")
        lines.append("")
        lines.append("| Cost Type | Rate |")
        lines.append("|-----------|------|")
        lines.append("| Slippage | 0.15% per side |")
        lines.append("| Buy Fee | 0.15% (broker) |")
        lines.append("| Sell Fee | 0.25% (broker + tax) |")
        lines.append("")

        total_slippage = sum(t.get("slippage_entry", 0) + t.get("slippage_exit", 0) for t in closed)
        total_fees = sum(t.get("fee_entry", 0) + t.get("fee_exit", 0) for t in closed)
        lines.append(f"- **Total Slippage Paid:** {_fmt_idr(total_slippage)}")
        lines.append(f"- **Total Fees Paid:** {_fmt_idr(total_fees)}")
        lines.append(f"- **Total Transaction Costs:** {_fmt_idr(total_slippage + total_fees)}")
        lines.append("")

    else:
        lines.append("## 📈 Closed Trades")
        lines.append("")
        lines.append("_No trades closed yet._")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_This report is generated automatically by the IHSG Swing Trading System. "
                 "Do not edit manually — it will be overwritten on the next scan._")

    # Write markdown
    PORTFOLIO_MD.parent.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_MD.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Portfolio markdown saved to %s", PORTFOLIO_MD)
    return PORTFOLIO_MD
