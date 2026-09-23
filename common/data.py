"""Shared data loading and cleaning (ROADMAP 2.1 — extracted from notebooks).

Contract (do not change without updating all three projects):
- download_prices(tickers, start, end) -> adjusted close DataFrame, cached to data/
- download_ff_factors(start, end)      -> real Ken French daily factors; NO proxy fallback (AUDIT P1-4)
- clean_prices(prices, ...)            -> (prices, ret_log, ret_simple, cleaning_log)
  NOTE: returns BOTH log and simple returns, explicitly named (AUDIT G-2).
"""
import time
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def download_prices(tickers, start, end, cache_name=None, data_dir=None,
                    chunk=20, retries=3):
    """Adjusted close prices, cache-first.

    Downloads in chunks with retries (Yahoo rate-limits bulk requests — a
    single 200-ticker call can return an empty frame). If cache_name exists
    under data/, no network is touched, so results are pinned to the snapshot
    the backtests were run on (vendor adjusted prices mutate over time).

    Returns: DataFrame of adjusted closes (columns = tickers with any data).
    """
    data_dir = Path(data_dir) if data_dir else DATA_DIR
    data_dir.mkdir(exist_ok=True)
    cache = data_dir / cache_name if cache_name else None
    if cache is not None and cache.exists():
        return pd.read_parquet(cache)

    import yfinance as yf
    if isinstance(tickers, str):
        tickers = [tickers]
    frames = []
    for i in range(0, len(tickers), chunk):
        batch = list(tickers[i:i + chunk])
        for attempt in range(retries):
            try:
                df = yf.download(batch, start=start, end=end,
                                 auto_adjust=True, progress=False)['Close']
                if df.dropna(axis=1, how='all').shape[1] > 0:
                    frames.append(df)
                    break
            except Exception:
                pass
            time.sleep(10 * (attempt + 1))
        else:
            raise RuntimeError(f"download failed for batch starting {batch[0]!r}")
        time.sleep(1)
    px = pd.concat(frames, axis=1).dropna(axis=1, how='all')
    if cache is not None:
        px.to_parquet(cache)
    return px


def download_ff_factors(start, end, cache_name='ff_factors_daily.parquet',
                        data_dir=None):
    """Real Ken French daily FF3 factors (Mkt-RF, SMB, HML, RF), cache-first.

    Hard requirement — there is deliberately NO proxy fallback (AUDIT P1-4):
    if pandas_datareader or the Dartmouth library is unavailable, this raises
    rather than silently fabricating factors.

    Values are decimal returns (the library publishes percent; divided by 100
    here). The famafrench reader returns a PeriodIndex under pandas 3 —
    converted to timestamps.
    """
    data_dir = Path(data_dir) if data_dir else DATA_DIR
    data_dir.mkdir(exist_ok=True)
    cache = data_dir / cache_name
    if cache.exists():
        return pd.read_parquet(cache)

    import pandas_datareader.data as web  # ImportError here is intentional
    ff = web.DataReader('F-F_Research_Data_Factors_daily', 'famafrench',
                        start, end)[0] / 100
    ff.index = ff.index.to_timestamp()
    ff.to_parquet(cache)
    return ff


def clean_prices(prices, max_missing=0.05, max_gap_days=3, winsorize_std=5.0):
    """Cleaning pipeline shared by all three projects (extracted verbatim).

    Rules, in order:
      1. Drop assets with > max_missing fraction of missing values.
      2. Forward-fill gaps of <= max_gap_days; drop remaining NaN rows.
      3. Log returns: r_log = ln(P_t / P_{t-1}).
      4. Winsorize each asset's log returns at mean ± winsorize_std sigmas
         (statistics computed pre-clip, per column).
      5. Simple returns: r_simple = expm1(r_log) — portfolio aggregation must
         use these (AUDIT G-2); log returns stay for estimation and
         time-aggregation.

    Returns: (prices, ret_log, ret_simple, cleaning_log)
    """
    log = []
    missing_pct = prices.isna().mean()
    keep = missing_pct[missing_pct <= max_missing].index
    removed = [c for c in prices.columns if c not in keep]
    prices = prices[keep].copy()
    log.append(f"Removed {len(removed)} assets with >{max_missing*100:.0f}% missing data")

    prices = prices.ffill(limit=max_gap_days).dropna()

    ret_log = np.log(prices / prices.shift(1)).dropna()

    means, stds = ret_log.mean(), ret_log.std()
    lower, upper = means - winsorize_std * stds, means + winsorize_std * stds
    n_clipped = 0
    for col in ret_log.columns:
        mask = (ret_log[col] < lower[col]) | (ret_log[col] > upper[col])
        n_clipped += int(mask.sum())
        ret_log[col] = ret_log[col].clip(lower[col], upper[col])
    log.append(f"Winsorized {n_clipped} observations at ±{winsorize_std}σ")
    log.append(f"Final: {ret_log.shape[1]} assets, {ret_log.shape[0]} days")

    ret_simple = np.expm1(ret_log)
    return prices, ret_log, ret_simple, log
