"""
ML4T Enhancement 3: Gradient Boosting (XGBoost) Entry Engine.

Provides a predictive entry engine that uses a pre-trained XGBoost model
to evaluate stocks entering the Trade Bucket. Instead of triggering on
a simple technical pattern, the model outputs a probability of a
successful trade based on the full set of alpha factors and technical
indicators.

The model is trained offline via ``scripts/train_models.py`` and saved
to ``data/models/xgb_entry_model.joblib``. The daily scan loads the
pre-trained model for inference only — zero training overhead at scan time.

Feature vector for each stock:
  - 5 formulaic alpha factors (from StockProfile)
  - RSI, ATR%, Hurst, trend strength, volume ratio
  - Additional derived features (momentum, volatility regime)
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from config.settings import (
    ATR_PERIOD,
    ML_ENTRY_ENABLED,
    ML_ENTRY_THRESHOLD,
    ML_ENTRY_MODEL_FILE,
    ML_MODELS_DIR,
    REGIME_SMA_SHORT,
)
from core.indicators import atr, rsi, sma, volume_ratio
from core.regime import RegimeSnapshot

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.adaptive import StockProfile
    from core.engines import BaseEngine, EntrySignal

logger = logging.getLogger(__name__)


def _build_feature_vector(
    df: pd.DataFrame,
    profile: "StockProfile | None",
) -> np.ndarray | None:
    """
    Build a feature vector for XGBoost prediction from OHLCV data + alpha factors.

    Returns a 1D numpy array of features, or None if insufficient data.
    """
    if len(df) < 60 or profile is None:
        return None

    try:
        last_close = float(df["Close"].iloc[-1])

        # Technical indicators
        rsi_14 = rsi(df["Close"], period=14)
        last_rsi = float(rsi_14.iloc[-1]) if not pd.isna(rsi_14.iloc[-1]) else 50.0

        atr_series = atr(df, period=ATR_PERIOD)
        last_atr = float(atr_series.iloc[-1]) if not pd.isna(atr_series.iloc[-1]) else 0.0
        atr_pct = last_atr / last_close if last_close > 0 else 0.02

        vol_ratio = volume_ratio(df, period=20)
        last_vol = float(vol_ratio.iloc[-1]) if not pd.isna(vol_ratio.iloc[-1]) else 1.0

        sma50 = sma(df["Close"], REGIME_SMA_SHORT)
        sma_dist = (last_close - float(sma50.iloc[-1])) / float(sma50.iloc[-1]) if not pd.isna(sma50.iloc[-1]) else 0.0

        # Returns
        ret_5 = float(df["Close"].pct_change(5).iloc[-1]) if len(df) >= 6 else 0.0
        ret_20 = float(df["Close"].pct_change(20).iloc[-1]) if len(df) >= 21 else 0.0

        # Feature vector: 15 features
        features = np.array([
            # Alpha factors from profile (5)
            profile.alpha_momentum,
            profile.alpha_mean_reversion,
            profile.alpha_liquidity,
            profile.alpha_volatility_regime,
            profile.alpha_money_flow,
            # Technical indicators (7)
            last_rsi / 100.0,           # Normalize to 0-1
            atr_pct,
            profile.mean_reversion_score,  # Hurst
            profile.trend_strength,
            last_vol,
            sma_dist,
            profile.typical_range_pct / 100.0,
            # Returns (2)
            ret_5,
            ret_20,
            # Volatility (1)
            profile.atr_pct,
        ])

        # Handle NaN/Inf
        features = np.nan_to_num(features, nan=0.0, posinf=5.0, neginf=-5.0)
        return features

    except Exception as e:
        logger.debug("Feature vector build error: %s", e)
        return None


# Feature names for model interpretability
FEATURE_NAMES = [
    "alpha_momentum", "alpha_mean_reversion", "alpha_liquidity",
    "alpha_volatility_regime", "alpha_money_flow",
    "rsi_14_norm", "atr_pct", "hurst", "trend_strength",
    "volume_ratio", "sma50_dist", "typical_range_norm",
    "ret_5d", "ret_20d", "volatility",
]


class GradientBoostEngine:
    """
    XGBoost-based predictive entry engine (ML4T Enhancement 3).

    Uses a pre-trained Gradient Boosting model to evaluate stocks
    for entry signals. The model predicts the probability of a
    successful trade (positive P&L within 20 days).

    The model is loaded from ``data/models/xgb_entry_model.joblib``
    at first use and cached for the session.

    If no model file exists, the engine silently skips (never fires).

    Priority: 3 (highest — ML-validated high confidence)
    Allowed regimes: BULL, CAUTION
    """

    name = "gradient_boost_entry"
    priority = 3

    def __init__(self) -> None:
        self._model = None
        self._model_loaded = False

    def _load_model(self) -> bool:
        """Load the pre-trained XGBoost model from disk."""
        if self._model_loaded:
            return self._model is not None

        self._model_loaded = True
        model_path = ML_MODELS_DIR / ML_ENTRY_MODEL_FILE

        if not model_path.exists():
            logger.debug(
                "XGBoost model not found at %s. "
                "Run 'python -m scripts.train_models' to train.",
                model_path,
            )
            return False

        try:
            import joblib
            self._model = joblib.load(model_path)
            logger.info("Loaded XGBoost entry model from %s", model_path)
            return True
        except Exception as e:
            logger.warning("Failed to load XGBoost model: %s", e)
            return False

    def scan(
        self,
        df: pd.DataFrame,
        ticker: str,
        regime: RegimeSnapshot,
        profile: "StockProfile | None" = None,
    ) -> "EntrySignal | None":
        """Evaluate a stock using the XGBoost model."""
        from core.engines import EntrySignal

        if not ML_ENTRY_ENABLED:
            return None

        # Regime gate
        if not regime.allows_engine(self.name):
            return None

        # Load model on first use
        if not self._load_model():
            return None

        # Build feature vector
        features = _build_feature_vector(df, profile)
        if features is None:
            return None

        try:
            # Predict probability
            proba = self._model.predict_proba(features.reshape(1, -1))[0]
            win_prob = proba[1] if len(proba) > 1 else proba[0]

            if win_prob < ML_ENTRY_THRESHOLD:
                return None

            last_close = float(df["Close"].iloc[-1])
            atr_series = atr(df, period=ATR_PERIOD)
            last_atr = float(atr_series.iloc[-1]) if not pd.isna(atr_series.iloc[-1]) else 0.0
            vol_ratio_series = volume_ratio(df, period=20)
            last_vol = float(vol_ratio_series.iloc[-1]) if not pd.isna(vol_ratio_series.iloc[-1]) else 1.0

            score = self.priority * win_prob * max(last_vol, 1.0)

            return EntrySignal(
                engine=self.name,
                ticker=ticker,
                price=round(last_close, 2),
                score=round(score, 2),
                priority=self.priority,
                details={
                    "ml_probability": round(win_prob, 4),
                    "ml_threshold": ML_ENTRY_THRESHOLD,
                    "atr": round(last_atr, 2),
                    "volume_ratio": round(last_vol, 2),
                    "model": "xgboost",
                    "features": len(FEATURE_NAMES),
                },
            )

        except Exception as e:
            logger.debug("[%s] XGBoost prediction error: %s", ticker, e)
            return None


# ── Model Training ───────────────────────────────────────────────────────────


class XGBoostTrainer:
    """
    Trains the XGBoost entry model from historical backtesting data.

    Labels are derived from forward 20-day returns:
      - Win (1): if price increased > 2% in the next 20 days
      - Loss (0): otherwise

    Uses time-series cross-validation to avoid look-ahead bias.
    """

    def train(
        self,
        all_data: dict[str, pd.DataFrame],
        profiles: dict[str, "StockProfile"],
    ) -> object | None:
        """
        Train XGBoost on labeled historical data.

        Parameters
        ----------
        all_data : dict[str, pd.DataFrame]
            Ticker -> full OHLCV DataFrame.
        profiles : dict[str, StockProfile]
            Ticker -> computed StockProfile.

        Returns
        -------
        object | None
            Trained XGBoost classifier, or None if training fails.
        """
        try:
            import xgboost as xgb
            from sklearn.model_selection import TimeSeriesSplit
            from sklearn.metrics import accuracy_score, classification_report
            import joblib
        except ImportError as e:
            logger.error("Required packages not installed for training: %s", e)
            return None

        from config.settings import (
            ML_ENTRY_N_ESTIMATORS,
            ML_ENTRY_MAX_DEPTH,
            ML_ENTRY_LEARNING_RATE,
            ML_LSTM_PREDICTION_HORIZON,
        )

        logger.info("Building training dataset for XGBoost entry model...")

        all_features = []
        all_labels = []

        for ticker, df in all_data.items():
            if ticker not in profiles or len(df) < 100:
                continue

            profile = profiles[ticker]

            # Compute forward returns for labeling
            fwd_return = df["Close"].shift(-ML_LSTM_PREDICTION_HORIZON) / df["Close"] - 1.0

            # Build features for each trading day
            for i in range(60, len(df) - ML_LSTM_PREDICTION_HORIZON):
                sub_df = df.iloc[:i + 1]
                features = _build_feature_vector(sub_df, profile)
                if features is None:
                    continue

                label = 1 if fwd_return.iloc[i] > 0.02 else 0
                all_features.append(features)
                all_labels.append(label)

        if len(all_features) < 100:
            logger.warning("Insufficient training data (%d samples)", len(all_features))
            return None

        X = np.array(all_features)
        y = np.array(all_labels)

        logger.info(
            "Training XGBoost: %d samples, %d features, %.1f%% positive",
            len(y), X.shape[1], np.mean(y) * 100,
        )

        # Time-series cross-validation
        tscv = TimeSeriesSplit(n_splits=5)

        model = xgb.XGBClassifier(
            n_estimators=ML_ENTRY_N_ESTIMATORS,
            max_depth=ML_ENTRY_MAX_DEPTH,
            learning_rate=ML_ENTRY_LEARNING_RATE,
            eval_metric="logloss",
            use_label_encoder=False,
            random_state=42,
        )

        # Train on all data (CV used for evaluation only)
        cv_scores = []
        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            model.fit(X_train, y_train)
            preds = model.predict(X_val)
            score = accuracy_score(y_val, preds)
            cv_scores.append(score)

        logger.info("CV Accuracy: %.3f ± %.3f", np.mean(cv_scores), np.std(cv_scores))

        # Final training on all data
        model.fit(X, y)

        # Save model
        ML_MODELS_DIR.mkdir(parents=True, exist_ok=True)
        model_path = ML_MODELS_DIR / ML_ENTRY_MODEL_FILE
        joblib.dump(model, model_path)
        logger.info("XGBoost model saved to %s", model_path)

        # Log feature importance
        importances = model.feature_importances_
        sorted_idx = np.argsort(importances)[::-1]
        logger.info("Top features:")
        for idx in sorted_idx[:5]:
            name = FEATURE_NAMES[idx] if idx < len(FEATURE_NAMES) else f"feat_{idx}"
            logger.info("  %s: %.4f", name, importances[idx])

        return model
