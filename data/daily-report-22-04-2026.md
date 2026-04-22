# 📊 IHSG Swing Trading — Daily Report (22-04-2026)

> **Date:** 22-04-2026
> **Last Updated:** 2026-04-22T07:05:24.121590+00:00

---

## How to Read This Report

This report contains today's market analysis (regime, trade signals, wait list) and the current state of the paper trading portfolio. Each day generates a separate report file.

---

## 📅 2026-04-22

### 🕐 Midday Evaluation

> ✅ **No macro veto** — Market conditions are acceptable.

- **IHSG Daily Change:** 🔴 -0.26%

_No alerts triggered._


---

# 📝 Paper Trading — Portfolio Overview

This report shows the current state of the paper trading simulator. The simulator executes all scanner signals automatically using IDR 5,000,000 starting capital with identical risk management rules as the backtester (slippage, fees, trailing stops, take-profit levels).

---

## 💰 Portfolio Overview

| Metric | Value |
|--------|-------|
| Starting Capital | IDR 5,000,000 |
| Current Equity | IDR 4,433,228 |
| Total Return | 🔴 -12.72% |
| Realized P&L | IDR -636,016 |
| Unrealized P&L | IDR 0 |
| Market Value (Positions) | IDR 2,626,859 |
| Portfolio Heat | 4.64% _(max 6%)_ |
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

## 📊 Open Positions (3)

### WIIM

| Detail | Value |
|--------|-------|
| Engine | ⚡ Quick Swing Trade — Short-term RSI momentum shift with EMA reclaim and volume |
| Entry Date | 2026-04-21 |
| Entry Price | IDR 1,971 _(raw: IDR 1,965)_ |
| Shares | 400 (4 lots) |
| Position Value | IDR 788,360 |
| Current Price | IDR 0 |
| Unrealized P&L | 🟢 IDR 0 (+0.00%) |
| Stop Loss | IDR 1,785 |
| Trailing Stop | IDR 1,785 |
| Take Profit | IDR 2,343 |
| Highest High | IDR 1,965 |
| Risk Amount | IDR 74,358 |
| Regime at Entry | 🟢 BULL |
| Last Updated |  |

### SKBM

| Detail | Value |
|--------|-------|
| Engine | ⚡ Quick Swing Trade — Short-term RSI momentum shift with EMA reclaim and volume |
| Entry Date | 2026-04-21 |
| Entry Price | IDR 752 _(raw: IDR 750)_ |
| Shares | 300 (3 lots) |
| Position Value | IDR 225,675 |
| Current Price | IDR 0 |
| Unrealized P&L | 🟢 IDR 0 (+0.00%) |
| Stop Loss | IDR 518 |
| Trailing Stop | IDR 518 |
| Take Profit | IDR 1,222 |
| Highest High | IDR 750 |
| Risk Amount | IDR 70,394 |
| Regime at Entry | 🟢 BULL |
| Last Updated |  |

### BBTN

| Detail | Value |
|--------|-------|
| Engine | ⚡ Quick Swing Trade — Short-term RSI momentum shift with EMA reclaim and volume |
| Entry Date | 2026-04-21 |
| Entry Price | IDR 1,344 _(raw: IDR 1,340)_ |
| Shares | 1,200 (12 lots) |
| Position Value | IDR 1,612,824 |
| Current Price | IDR 0 |
| Unrealized P&L | 🟢 IDR 0 (+0.00%) |
| Stop Loss | IDR 1,271 |
| Trailing Stop | IDR 1,271 |
| Take Profit | IDR 1,490 |
| Highest High | IDR 1,340 |
| Risk Amount | IDR 87,426 |
| Regime at Entry | 🟢 BULL |
| Last Updated |  |

## 📈 Closed Trades (8)

### Performance Summary

| Metric | Value |
|--------|-------|
| Total Trades | 8 |
| Wins | ✅ 0 |
| Losses | ❌ 8 |
| Win Rate | 0.0% |
| Total Realized P&L | IDR -636,016 |
| Average Win | IDR 0 |
| Average Loss | IDR -79,502 |
| Average Holding Period | 1.2 days |

### Trade Log

| # | Ticker | Engine | Entry → Exit | P&L | P&L % | Reason | Days |
|---|--------|--------|-------------|-----|-------|--------|------|
| 1 | ❌ SKBM | quick_swing_trade | IDR 752 → IDR 627 | IDR -49,908 | -16.59% | trailing_stop | 5d |
| 2 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,798 | IDR -69,244 | -8.78% | trailing_stop | 1d |
| 3 | ❌ BBTN | quick_swing_trade | IDR 1,344 → IDR 1,280 | IDR -76,992 | -4.77% | trailing_stop | 1d |
| 4 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,797 | IDR -69,528 | -8.82% | trailing_stop | 1d |
| 5 | ❌ BBTN | quick_swing_trade | IDR 1,344 → IDR 1,274 | IDR -90,792 | -5.20% | trailing_stop | 0d |
| 6 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,782 | IDR -94,380 | -9.58% | trailing_stop | 0d |
| 7 | ❌ BBTN | quick_swing_trade | IDR 1,344 → IDR 1,274 | IDR -90,792 | -5.20% | trailing_stop | 1d |
| 8 | ❌ WIIM | quick_swing_trade | IDR 1,971 → IDR 1,782 | IDR -94,380 | -9.58% | trailing_stop | 1d |

### Cost Analysis

Every trade includes realistic costs (same as backtester):

| Cost Type | Rate |
|-----------|------|
| Slippage | 0.15% per side |
| Buy Fee | 0.15% (broker) |
| Sell Fee | 0.25% (broker + tax) |

- **Total Slippage Paid:** IDR 36
- **Total Fees Paid:** IDR 48
- **Total Transaction Costs:** IDR 85

---

_This report is generated automatically by the IHSG Swing Trading System. Do not edit manually — it will be overwritten on the next scan._