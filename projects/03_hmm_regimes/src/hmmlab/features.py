"""HMM feature construction (extracted verbatim, 2.2).

Scaler discipline (P3-1, fixed in 1.2): fit through scaler_fit_end only.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def build_features(spy_ret, vix, vol_window=21, scaler_fit_end=None,
                   winsorize_min_periods=252):
    """
    Build multivariate feature matrix for HMM.
    
    Features:
      1. Daily log return (standardized)
      2. Realized volatility (21-day rolling std, annualized, standardized)
      3. VIX daily change (standardized)
    
    Returns: (features_df, scaler)
    """
    df = pd.DataFrame(index=spy_ret.index)
    
    # Feature 1: Daily return
    df['return'] = spy_ret
    
    # Feature 2: Realized volatility (annualized)
    df['realized_vol'] = spy_ret.rolling(vol_window).std() * np.sqrt(252)
    
    # Feature 3: VIX daily change
    vix_aligned = vix.reindex(spy_ret.index).ffill()
    df['vix_change'] = vix_aligned.pct_change()
    
    # Drop NaN
    df = df.dropna()
    
    # Winsorize extreme values — CAUSALLY (ROADMAP 3.1, closing the 1.2/1.7
    # residue): each observation is clipped at expanding-window quantiles
    # computed from data up to and including t only. The first
    # winsorize_min_periods observations are unclipped (NaN bounds = no clip);
    # every bound is measurable at the time it is applied, so the feature
    # pipeline is exactly invariant to deleting post-t data.
    for col in df.columns:
        lower = df[col].expanding(winsorize_min_periods).quantile(0.001)
        upper = df[col].expanding(winsorize_min_periods).quantile(0.999)
        df[col] = df[col].clip(lower=lower, upper=upper)

    # Standardize (zero mean, unit variance).
    # P3-1 fix: fit the scaler through scaler_fit_end ONLY (frozen-IS), so
    # OOS means/vols never touch any standardized feature. The walk-forward
    # backtest goes further and rescales each trailing window with its own
    # statistics (see run_regime_backtest).
    scaler = StandardScaler()
    fit_df = df if scaler_fit_end is None else df.loc[:scaler_fit_end]
    scaler.fit(fit_df)
    features_scaled = scaler.transform(df)
    features_df = pd.DataFrame(features_scaled, index=df.index, columns=df.columns)
    
    return features_df, df, scaler
