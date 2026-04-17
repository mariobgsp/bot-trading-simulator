# 📊 IHSG Swing Trading — Daily Report (17-04-2026)

> **Date:** 17-04-2026
> **Last Updated:** 2026-04-17T13:49:13.679760+00:00

---

## How to Read This Report

This report contains today's market analysis (regime, trade signals, wait list) and the current state of the paper trading portfolio. Each day generates a separate report file.

---

## 📅 2026-04-17

### 🕐 Midday Evaluation

> ✅ **No macro veto** — Market conditions are acceptable.

- **IHSG Daily Change:** 🟢 +0.20%

_No alerts triggered._


### 🔴 BEAR Market Regime — Daily Scan

> The market is range-bound or random-walk (Hurst 0.45–0.55). Only B.O.W. and Wyckoff Spring engines are active. Position sizes are quartered.

| Indicator | Value |
|-----------|-------|
| IHSG Close | IDR 7,634 |
| SMA(50) | IDR 7,719 |
| SMA(200) | IDR 7,979 |
| ATR(14) | IDR 150 |
| Hurst Exponent | 0.55 |

#### 📋 Scan Summary

| Metric | Count |
|--------|-------|
| Total Scanned | 958 |
| With Data | 958 |
| ❌ Avoid (filtered) | 757 |
| ⏳ Wait (setting up) | 52 |
| ✅ Trade (actionable) | 0 |
| ⏭️ Skipped | 0 |

#### 🎯 Trade Signals

_No trade signals today._

#### ⏳ Wait List (20 stocks setting up)

| Ticker | Condition | Price |
|--------|-----------|-------|
| ABMM | Price is in a tight trading range — watching for breakout | IDR 3,020 |
| AALI | Price is in a tight trading range — watching for breakout | IDR 7,350 |
| ANTM | Price is approaching a Fair Value Gap zone — watching for pullback entry | IDR 4,040 |
| AUTO | Price is in a tight trading range — watching for breakout | IDR 2,770 |
| BBNI | Price is in a tight trading range — watching for breakout | IDR 4,270 |
| BBRI | Price is in a tight trading range — watching for breakout | IDR 3,670 |
| BELL | Price is approaching a Fair Value Gap zone — watching for pullback entry | IDR 152 |
| BJBR | Price is in a tight trading range — watching for breakout | IDR 820 |
| BJTM | Price is in a tight trading range — watching for breakout | IDR 575 |
| BMRI | Price is in a tight trading range — watching for breakout | IDR 4,980 |
| BNBR | Price is approaching a Fair Value Gap zone — watching for pullback entry | IDR 124 |
| BNGA | Price is in a tight trading range — watching for breakout | IDR 1,770 |
| DMAS | Price is in a tight trading range — watching for breakout | IDR 133 |
| DSNG | Price is in a tight trading range — watching for breakout | IDR 1,405 |
| DPUM | Price is approaching a Fair Value Gap zone — watching for pullback entry | IDR 157 |
| ELSA | Volume Spread Analysis detected a squat candle — high volume, narrow range, possible reversal setup | IDR 850 |
| ELPI | Price is approaching a Fair Value Gap zone — watching for pullback entry | IDR 1,325 |
| ESSA | Volume Spread Analysis detected a squat candle — high volume, narrow range, possible reversal setup | IDR 770 |
| GJTL | Price is in a tight trading range — watching for breakout | IDR 1,055 |
| HRTA | Price is approaching a Fair Value Gap zone — watching for pullback entry | IDR 2,760 |

#### 📝 Paper Trading Activity

| Metric | Value |
|--------|-------|
| Equity | IDR 4,433,228 |
| Total Return | 🔴 -12.72% |
| Open Positions | 0 |

**Trades Closed Today:**

| Ticker | P&L | P&L % | Exit Reason | Held |
|--------|-----|-------|-------------|------|
| ❌ SKBM | IDR -49,908 | -16.59% | 📉 Trailing Stop — Price fell below the Chandelier trailing stop level | 5 days |


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
| Market Value (Positions) | IDR 0 |
| Portfolio Heat | 0.00% _(max 6%)_ |
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

## 📊 Open Positions

_No open positions._

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