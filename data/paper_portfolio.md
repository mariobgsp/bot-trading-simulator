# 📝 IHSG Paper Trading — Portfolio Report

> **Generated:** 2026-04-15 23:01:26 UTC

This report shows the current state of the paper trading simulator. The simulator executes all scanner signals automatically using IDR 5,000,000 starting capital with identical risk management rules as the backtester (slippage, fees, trailing stops, take-profit levels).

---

## 💰 Portfolio Overview

| Metric | Value |
|--------|-------|
| Starting Capital | IDR 5,000,000 |
| Current Equity | IDR 4,413,892 |
| Total Return | 🔴 -11.72% |
| Realized P&L | IDR -586,108 |
| Unrealized P&L | IDR -47,724 |
| Market Value (Positions) | IDR 1,866,000 |
| Portfolio Heat | 3.63% _(max 6%)_ |
| Win Rate | 0.0% |

<details>
<summary>📖 What do these metrics mean?</summary>

- **Equity** = Starting capital + all realized P&L. This is the "bank balance" after closing trades.
- **Realized P&L** = Total profit/loss from closed trades (after slippage + broker fees).
- **Unrealized P&L** = Paper profit/loss on open positions based on current market prices.
- **Market Value** = Current value of all open positions at market price.
- **Portfolio Heat** = Total risk exposure as % of initial capital. Capped at 6% to prevent catastrophic drawdowns.
- **Win Rate** = Percentage of closed trades that were profitable.

</details>

## 📊 Open Positions (2)

### SKBM

| Detail | Value |
|--------|-------|
| Engine | ⚡ Quick Swing Trade — Short-term RSI momentum shift with EMA reclaim and volume |
| Entry Date | 2026-04-12 |
| Entry Price | IDR 752 _(raw: IDR 750)_ |
| Shares | 400 (4 lots) |
| Position Value | IDR 300,900 |
| Current Price | IDR 630 |
| Unrealized P&L | 🔴 IDR -48,900 (-16.25%) |
| Stop Loss | IDR 518 |
| Trailing Stop | IDR 619 |
| Take Profit | IDR 1,222 |
| Highest High | IDR 750 |
| Risk Amount | IDR 93,858 |
| Regime at Entry | 🟢 BULL |
| Last Updated | 2026-04-15 |

### BBTN

| Detail | Value |
|--------|-------|
| Engine | ⚡ Quick Swing Trade — Short-term RSI momentum shift with EMA reclaim and volume |
| Entry Date | 2026-04-14 |
| Entry Price | IDR 1,344 _(raw: IDR 1,340)_ |
| Shares | 1,200 (12 lots) |
| Position Value | IDR 1,612,824 |
| Current Price | IDR 1,345 |
| Unrealized P&L | 🟢 IDR 1,176 (+0.07%) |
| Stop Loss | IDR 1,271 |
| Trailing Stop | IDR 1,309 |
| Take Profit | IDR 1,490 |
| Highest High | IDR 1,380 |
| Risk Amount | IDR 87,426 |
| Regime at Entry | 🟢 BULL |
| Last Updated | 2026-04-15 |

## 📈 Closed Trades (7)

### Performance Summary

| Metric | Value |
|--------|-------|
| Total Trades | 7 |
| Wins | ✅ 0 |
| Losses | ❌ 7 |
| Win Rate | 0.0% |
| Total Realized P&L | IDR -586,108 |
| Average Win | IDR 0 |
| Average Loss | IDR -83,730 |
| Average Holding Period | 0.7 days |

### Trade Log

| # | Ticker | Engine | Entry → Exit | P&L | P&L % | Reason | Days |
|---|--------|--------|-------------|-----|-------|--------|------|
| 1 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,798 | IDR -69,244 | -8.78% | trailing_stop | 1d |
| 2 | ❌ BBTN | quick_swing_trade | IDR 1,344 → IDR 1,280 | IDR -76,992 | -4.77% | trailing_stop | 1d |
| 3 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,797 | IDR -69,528 | -8.82% | trailing_stop | 1d |
| 4 | ❌ BBTN | quick_swing_trade | IDR 1,344 → IDR 1,274 | IDR -90,792 | -5.20% | trailing_stop | 0d |
| 5 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,782 | IDR -94,380 | -9.58% | trailing_stop | 0d |
| 6 | ❌ BBTN | quick_swing_trade | IDR 1,344 → IDR 1,274 | IDR -90,792 | -5.20% | trailing_stop | 1d |
| 7 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,782 | IDR -94,380 | -9.58% | trailing_stop | 1d |

### Cost Analysis

Every trade includes realistic costs (same as backtester):

| Cost Type | Rate |
|-----------|------|
| Slippage | 0.15% per side |
| Buy Fee | 0.15% (broker) |
| Sell Fee | 0.25% (broker + tax) |

- **Total Slippage Paid:** IDR 34
- **Total Fees Paid:** IDR 45
- **Total Transaction Costs:** IDR 80

---

_This report is generated automatically by the IHSG Swing Trading System. Do not edit manually — it will be overwritten on the next scan._