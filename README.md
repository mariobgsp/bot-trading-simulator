# IHSG Swing Trading System (v4.0.0 — ML4T)

A highly rigorous, accuracy-first swing trading application specifically designed for the Indonesian Stock Exchange (IHSG).

This system automates daily data ingestion, technical scanning, market regime detection, **adaptive per-stock signal detection**, entry signal generation, risk management, backtesting, **daily JSON tracking**, and live execution through a structured, 8-phase architecture.

## 🏗️ Architecture

1. **Infrastructure & Data Engineering (`core/ingestion.py`, `core/data_cleaner.py`)**
   - Ingests daily OHLCV data for 591 curated IHSG tickers.
   - Handles splits, NaN gaps, and extreme volume spikes.
   - Stores data locally in optimized Parquet format (`data/ohlcv/`).
   - Rate-limited `yfinance` integration to prevent IP bans.
   - ⭐ **ML4T**: Wavelet denoising (Daubechies-4) and Kalman filter smoothing for noise reduction.

2. **Master Scanner Engine (`core/scanner.py`)**
   - Scans the universe of stocks through a strict "Tri-Bucket" triage pipeline:
     - **Avoid Bucket**: Filters out illiquid stocks (< IDR 2B ADTV), penny stocks (< IDR 50), stocks far below their SMA(200) (>5%), and stocks reporting earnings within 48 hours.
     - **Wait Bucket**: Parks stocks setting up for a trade (e.g., tight consolidation, approaching Fair Value Gaps, Wyckoff Phase B accumulation, or VSA squat candles).
     - **Trade Bucket**: The highest confidence, ready-to-execute signals (max 5 per day).
   - **Adaptive Detector Integration**: After passing Avoid filters, each stock gets a personalized `StockProfile` computed from its own 2-year history.

3. **Adaptive Per-Stock Detector (`core/adaptive.py`)** ⭐ NEW
   - Computes a statistical profile for each stock from up to 2 years of history.
   - Replaces fixed global thresholds with stock-specific ones:
     - **RSI Oversold/Overbought**: 10th/90th percentile of the stock's own RSI distribution.
     - **Volume Spike Threshold**: 90th percentile of the stock's own volume ratio.
     - **Typical Range**: Median of rolling 20-day price ranges.
     - **ATR%**: Normalized volatility (ATR/Close).
     - **Hurst Exponent**: Mean-reversion vs trending tendency.
     - **Trend Strength**: Linear regression slope over 60 days.
   - Makes the system MORE sensitive for stable blue-chip stocks and MORE conservative for volatile stocks.

4. **Market Regime & Entry Engines (`core/regime.py`, `core/engines.py`, `core/ml_engine.py`, `core/deep_engine.py`)**
   - **Regime Filter**: Classifies the broader IHSG composite (`^JKSE`) as `BULL`, `CAUTION`, or `BEAR` based on the Hurst exponent.
   - ⭐ **ML Regime**: PCA + K-Means clustering provides an unsupervised second opinion on the market regime with confidence scores.
   - **Entry Engines** (8 engines, adaptive + ML-enhanced thresholds):
     - _Priority 3: Gradient Boost Entry_ ⭐ ML4T — XGBoost model predicting trade success probability from alpha factors.
     - _Priority 3: LSTM Direction_ ⭐ ML4T — Universal LSTM model predicting 20-day directional probability.
     - _Priority 3: FVG Pullback_ — Pullback into Fair Value Gap. Active in BULL, CAUTION.
     - _Priority 2: Momentum Breakout_ — Breakout from tight consolidation. Active in BULL only.
     - _Priority 2: EMA Crossover_ — EMA(9)/EMA(21) crossover with RSI and volume confirmation. Active in BULL, CAUTION.
     - _Priority 2: Volume Climax Reversal_ — Selling climax exhaust reversal. Active in BULL, CAUTION.
     - _Priority 1: Buying on Weakness (B.O.W.)_ — Capitulation reversal with adaptive oversold detection. Active in ALL regimes.
     - _Priority 1: Wyckoff Phase C Spring_ — False breakdown below range low. Active in CAUTION, BEAR.

5. **Risk Management Engine (`core/risk.py`, `core/portfolio.py`)**
   - Deterministic ATR-based mathematics.
   - Calculates Stop-Loss (1.5x ATR) and Chandelier Trailing Stops (2.0x ATR).
   - Dynamic position sizing forcing equal risk across trades (default 2% of capital), rounding to IDX lot sizes (100 shares).
   - **Portfolio Heat tracking**: Caps maximum simultaneous open risk at 6% of total capital.
   - Regime-adjusted risk: Halves position sizes in CAUTION (1%), quarters them in BEAR (0.5%).
   - **20-Day Reversal Exit**: Monitors positions for profit-maximizing exits within the first 20 holding days.
   - ⭐ **ML4T**: Bayesian stochastic volatility estimation (PyMC) for dynamic risk sizing based on posterior vol distributions.

6. **Daily Output Dashboard (`core/report.py`, `scripts/daily.py`, `core/alerts.py`)**
   - Unified daily workflow combining all the above into a single execution step.
   - Generates formatted console reports and a dark-themed `.html` dashboard showing portfolio heat and actionable Trade Cards.
   - CRITICAL-level alert logging for new signals.
   - **Reversal exit checking** for open positions on each daily run.

7. **Backtesting Engine (`core/backtester.py`, `core/backtest_report.py`)**
   - Event-driven replay through the same scanner + engines + risk manager. Zero look-ahead bias.
   - Automatic 3.5-year Training / 1.5-year Blind Test split.
   - Hardcoded slippage (0.15% per side) and IDX broker fees (0.15% buy, 0.25% sell).
   - **20-Day Reversal Exit simulation** with profit-lock and bearish reversal detection.
   - **Report Card**: Win Rate, Expected Value, Max Drawdown (⚠️ >15%), Sharpe Ratio, Profit Factor (⚠️ <1.5), Win/Loss Streaks.

8. **Live Execution & Failsafes (`core/broker.py`, `core/failsafes.py`, `core/bracket_order.py`)**
   - Abstract broker adapter with `SimulatedBroker` for testing.
   - **Fat Finger Guard**: Hard limit of 1,000 shares / IDR 2.5M per order.
   - **Daily Drawdown Breaker**: Halts all trading if the account drops 3% in a single day.
   - **Bracket Orders**: Sends Buy + Stop-Loss + Take-Profit (3x ATR) simultaneously.
   - Cron-ready execution CLI scheduled for 15:50 WIB.

## ⭐ Key Features (v4.0.0 — ML4T)

### ML4T Enhancement 1: Advanced Feature Engineering & Denoising ⭐ NEW
- **Wavelet Denoising**: Daubechies-4 wavelet with soft thresholding removes high-frequency noise from Close prices while preserving trend structure.
- **Kalman Filter**: State-space model provides an optimally smoothed "true" price estimate.
- **Formulaic Alpha Factors** (WorldQuant-inspired, pure numpy/pandas — no TA-Lib):
  - **Momentum Alpha**: Normalized rate-of-change capturing short-term directional strength.
  - **Mean Reversion Alpha**: Bollinger Band z-score measuring distance from rolling mean.
  - **Liquidity Alpha**: VWAP deviation capturing position relative to volume-weighted price.
  - **Volatility Regime Alpha**: Realized vol z-score detecting regime shifts.
  - **Money Flow Alpha**: Chaikin Money Flow capturing buying/selling pressure.

### ML4T Enhancement 2: Unsupervised Market Regime Engine ⭐ NEW
- **PCA + K-Means clustering** on rolling market features (returns, volatility, volume, trend)
- Provides a regime confidence score alongside the traditional Hurst-based classification
- Logs regime disagreements for analysis (Hurst remains ground truth)

### ML4T Enhancement 3: XGBoost Entry Engine ⭐ NEW
- **Gradient Boosting Classifier** trained on all 591 tickers using formulaic alphas + technical indicators
- Predicts probability of successful trade (P&L > 2% in 20 days)
- Only fires when probability exceeds 60% (configurable threshold)
- Time-series cross-validated to avoid look-ahead bias
- Model saved to `data/models/xgb_entry_model.joblib`

### ML4T Enhancement 4: LSTM Direction Engine ⭐ NEW
- **Universal 2-layer LSTM** trained on 60-day OHLCV sequences across all tickers
- Predicts probability of upward price movement over next 20 days
- Only fires when probability exceeds 65%
- Architecture: LSTM(64)→Dropout→LSTM(64)→Dropout→Dense(32)→Dense(1, sigmoid)
- Model saved as TF SavedModel to `data/models/lstm_direction_model/`

### ML4T Enhancement 5: Bayesian Risk Management ⭐ NEW
- **PyMC stochastic volatility model** estimates posterior distribution of market volatility
- Dynamic risk sizing: reduces position sizes in high-volatility regimes, increases in low-vol
- Market-wide estimation (IHSG composite) to avoid per-ticker overhead
- Graceful fallback to static ATR-based risk if PyMC is unavailable

### Weekly Model Training ⭐ NEW
- Separate `weekly-train.yml` GitHub Actions workflow trains all ML models every Sunday
- Models improve automatically as new data accumulates
- Trained artifacts committed back to repo for daily scan consumption

### Markdown Reports ⭐ NEW
- `data/daily_tracking.md` — Human-readable daily scan and midday evaluation report
- `data/paper_portfolio.md` — Human-readable portfolio status, positions, and trade history
- Auto-generated from JSON data after every scan, committed by workflows
- Includes explanations of regimes, engines, exit reasons, and all trading concepts

### Adaptive Per-Stock Detection
Instead of fixed global thresholds, the system learns each stock's personality:
- **BBCA** (stable blue chip): RSI oversold at 38, volume spike at 1.6x → more sensitive detection
- **Mining stocks** (volatile): RSI oversold at 22, volume spike at 2.8x → more conservative detection

### 20-Day Reversal Exit (Profit Maximizer)
- **Within 20 days**: If position has unrealized profit and detects bearish reversal (2+ bearish candles), exit to lock in gains
- **Profit erosion protection**: If peak profit was high but has dropped to 50% of its peak, lock in remaining profit
- **After 20 days**: No forced exit — trailing stop manages the position naturally

### EMA Crossover Engine
A new trend-following signal that catches momentum entries the strict Breakout engine misses:
- EMA(9) crosses above EMA(21) with volume and RSI confirmation
- Uses adaptive per-stock thresholds for RSI and volume bounds

### Paper Trading Simulator
Runs automatically alongside the daily scan, simulating real-money execution against the scanner's signals:
- Starts with a configured virtual balance (default IDR 5,000,000).
- Applies identical risk management logic as the backtester (slippage, fees, Chandelier trailing stops, bracket order TPs).
- Outputs a dedicated performance summary into both the console and the HTML daily report.
- Saves its exact state to `data/paper_portfolio.json` for session continuity.

### Daily JSON Tracking ⭐ NEW
All scan results, trade signals, paper trading activity, and midday evaluation outcomes are persisted into `data/daily_tracking.json`:
- **Daily scan entries**: regime, scan summary (avoid/wait/trade counts), trade signal details, wait signals, and paper trading actions (entries with full position sizing, exits with P&L).
- **Midday evaluation entries**: macro veto status, IHSG daily change, gap-and-crap alerts, fakeout breakout vetoes.
- Each entry is date-stamped and type-tagged (`daily_scan` or `midday_eval`) for easy querying.
- Re-runs on the same day replace the existing entry (idempotent).

### GitHub Contribution Attribution ⭐ NEW
Workflow commits are now attributed to the repository owner's GitHub account instead of `github-actions[bot]`, ensuring every daily and midday run shows as a green contribution square on the GitHub profile.

## 🚀 Usage

### 1. Unified Daily Workflow (Start Here)

```bash
python -m scripts.daily
```

_Options:_

- `--tickers ASII BBCA TLKM` : Scan specific tickers only.
- `--check-earnings` : Fetch upcoming earnings dates (slower).
- `--no-html` : Skip generating the HTML dashboard.
- `--capital 200000000` : Custom portfolio capital.

### 2. Backtesting

```bash
python -m scripts.backtest
python -m scripts.backtest --tickers BBCA BBRI ASII TLKM UNVR
python -m scripts.backtest --capital 200000000
```

### 3. Live Execution

```bash
python -m scripts.execute --dry-run    # Simulate without placing orders
python -m scripts.execute              # Live mode (requires broker setup)
```

### 4. Individual Subsystems

```bash
python -m scripts.ingest               # Phase 1: Ingest OHLCV data
python -m scripts.scan                 # Phase 2: Raw scanner
python -m scripts.regime               # Phase 3: Market regime check
python -m scripts.risk --ticker ASII   # Phase 4: Risk calculator
```

## 🛠️ GitHub Actions Automation

The system is configured to run entirely hands-off via GitHub Actions:

- **Schedule**: Automatically runs the `daily.py` workflow at 23:30 WIB every weekday.
- **Midday Scan**: Runs mid-day evaluation at 12:15 WIB for macro veto and gap-and-crap detection.
- **Caching**: Parquet OHLCV data is cached across runs to vastly speed up ingestion.
- **Artifacts**: HTML reports and Alert Logs are uploaded as workflow artifacts (30-day retention).
- **Persistence**: Portfolio state (`data/portfolio.json`), paper portfolio (`data/paper_portfolio.json`), daily tracking log (`data/daily_tracking.json`), and **Markdown reports** (`data/daily_tracking.md`, `data/paper_portfolio.md`) are automatically committed back to the repository.
- **Model Training**: ML models are retrained weekly via `weekly-train.yml` and saved to `data/models/`.
- **Contribution Attribution**: All automated commits are attributed to the repository owner (`mariobgsp`) so they count toward GitHub contribution history.

To enable, simply push code to the `main` branch. You can also trigger a manual run with custom tickers from the "Actions" tab.

## 📦 Requirements

- Python 3.12+
- `pandas >= 2.0`
- `numpy >= 1.24`
- `yfinance >= 0.2.36`
- `pyarrow >= 14.0` (for Parquet storage)
- `scikit-learn >= 1.3` (for PCA, clustering, ML regime)
- `PyWavelets >= 1.5` (for wavelet denoising)
- `pykalman >= 0.9.7` (for Kalman filter denoising)
- `xgboost >= 2.0` (for gradient boosting entry engine)
- `joblib >= 1.3` (for model serialization)
- `tensorflow >= 2.15` _(optional — LSTM engine)_
- `pymc >= 5.10` _(optional — Bayesian risk)_

Install via:

```bash
pip install -r requirements.txt
```

## 📝 Changelog

- feat: v4.0.0 — ML4T architecture upgrade: wavelet/Kalman denoising, formulaic alphas, PCA/clustering regime, XGBoost entry engine, LSTM direction engine, Bayesian risk, markdown reports, weekly training workflow
- feat: v3.1.0 — daily JSON tracking for scan results / trade signals / paper trading / midday evaluations, GitHub contribution attribution for workflow commits
- feat: add paper trading simulator tracking trades directly from daily scan signals
- feat: v3.0.0 — adaptive per-stock detector, EMA crossover engine, 20-day reversal exit with profit maximization, relaxed thresholds, more sensitive signal generation
- feat: add midday scan github actions workflow (098339d)
- feat: complete Phase 2, 3, 5, 6.5 trading engine upgrades (ed5525a)
- chore: update scheduler to 11:30 PM WIB weekdays (ae9f086)
- fix(ci): gracefully handle missing portfolio file (4673050)
- fix: tolerate expected yfinance download failures in ingest script (6def7a1)
- feat: complete Phase 6 and 7 (Backtesting Engine and Live Execution) (2dbb44d)
- fix: remove nonexistent --resume flag from github actions (10384e3)
- feat: complete Phase 1-5 master architecture (v1.0.0) (fe9cf49)
- Initial commit (dfbc690)
