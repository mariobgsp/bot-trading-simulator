"""
Unified daily workflow for the IHSG swing trading system.

Runs the complete morning routine in a single command:
  1. Fetch market regime (IHSG composite)
  2. Scan all stored tickers through Avoid/Wait/Trade pipeline
  3. Generate console report
  4. Save HTML report to reports/
  5. Fire alerts for any Trade signals

Usage:
    python -m scripts.daily
    python -m scripts.daily --tickers BBCA BBRI TLKM ASII UNVR
    python -m scripts.daily --check-earnings
    python -m scripts.daily --no-html
    python -m scripts.daily --capital 200000000
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import DEFAULT_CAPITAL, LOG_DATE_FORMAT, LOG_FORMAT
from core.alerts import fire_heat_warning, fire_regime_alert, fire_trade_alert
from core.database import ParquetStore
from core.portfolio import Portfolio
from core.regime import MarketRegime, RegimeSnapshot, RegimeType
from core.report import generate_console_report, generate_html_report
from core.scanner import MasterScanner


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("yfinance").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("peewee").setLevel(logging.WARNING)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="IHSG Daily Scan - Complete Morning Workflow",
    )
    parser.add_argument(
        "--tickers", nargs="+", default=None,
        help="Specific tickers (default: all stored)",
    )
    parser.add_argument(
        "--check-earnings", action="store_true",
        help="Check for upcoming earnings (slower)",
    )
    parser.add_argument(
        "--no-html", action="store_true",
        help="Skip HTML report generation",
    )
    parser.add_argument(
        "--capital", type=float, default=DEFAULT_CAPITAL,
        help=f"Portfolio capital (default: IDR {DEFAULT_CAPITAL:,.0f})",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger("scripts.daily")

    logger.info("=" * 60)
    logger.info("IHSG Daily Workflow - Starting")
    logger.info("=" * 60)

    # ── Step 1: Regime ─────────────────────────────────────────────
    logger.info("[1/5] Fetching market regime...")
    try:
        regime_obj = MarketRegime(period="1y")
        regime = regime_obj.get_snapshot()
    except Exception as e:
        logger.warning("Regime fetch failed, using CAUTION: %s", e)
        regime = RegimeSnapshot(
            regime=RegimeType.CAUTION,
            close=0, sma_short=0, sma_long=0, atr_value=0,
            as_of_date="error",
        )

    fire_regime_alert(regime.regime.value, regime.close,
                      regime.sma_short, regime.sma_long)

    # ── Step 2: Scan ───────────────────────────────────────────────
    logger.info("[2/5] Scanning tickers...")
    store = ParquetStore()
    scanner = MasterScanner(store)

    if args.tickers:
        tickers = [t.replace(".JK", "").upper() for t in args.tickers]
    else:
        tickers = store.list_tickers()

    if not tickers:
        logger.error("No tickers to scan. Run ingestion first.")
        sys.exit(1)

    start = time.time()
    result = scanner.scan_universe(
        tickers, check_earnings=args.check_earnings, regime=regime,
    )
    elapsed = time.time() - start

    # ── Step 3: Portfolio ──────────────────────────────────────────
    logger.info("[3/5] Loading portfolio...")
    portfolio = Portfolio.load()

    # Check heat
    from config.settings import MAX_PORTFOLIO_HEAT_PCT
    fire_heat_warning(portfolio.heat, MAX_PORTFOLIO_HEAT_PCT)

    # ── Step 4: Reports ────────────────────────────────────────────
    logger.info("[4/5] Generating reports...")

    # Console report
    console_report = generate_console_report(result, regime, portfolio, elapsed)
    print(console_report)

    # HTML report
    if not args.no_html:
        html_path = generate_html_report(result, regime, portfolio, elapsed)
        logger.info("HTML report: %s", html_path)

    # ── Step 5: Alerts ─────────────────────────────────────────────
    logger.info("[5/5] Processing alerts...")

    for entry in result.trade:
        fire_trade_alert(
            ticker=entry.ticker,
            signal=entry.signal,
            price=entry.price,
            details=entry.details,
        )

    if not result.trade:
        logger.info("No trade signals today.")

    logger.info("Daily workflow complete.")


if __name__ == "__main__":
    main()
