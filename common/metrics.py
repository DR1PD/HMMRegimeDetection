"""Shared performance metrics (ROADMAP 2.1) — one tested implementation.

All functions take SIMPLE-return series (AUDIT G-2); log returns are for
estimation and time-aggregation only, never for cross-asset metrics.
`summary()` reproduces the notebooks' compute_metrics dict key-for-key so it
can be imported as a drop-in replacement.
"""
import numpy as np

TRADING_DAYS = 252


def annualized_return(ret_simple):
    """Arithmetic annualization: mean daily simple return × 252."""
    return ret_simple.mean() * TRADING_DAYS


def annualized_vol(ret_simple):
    """Std of daily simple returns × sqrt(252)."""
    return ret_simple.std() * np.sqrt(TRADING_DAYS)


def sharpe(ret_simple, rf_annual=0.025):
    """(mean daily excess / daily std) × sqrt(252)."""
    r = ret_simple.dropna()
    if r.std() == 0:
        return 0.0
    return (r.mean() - rf_annual / TRADING_DAYS) / r.std() * np.sqrt(TRADING_DAYS)


def sharpe_se(sr, n_days):
    """Lo (2002) standard error of an annualized Sharpe estimate:
    SE ≈ sqrt((1 + 0.5·SR²) / T_years)."""
    t_years = n_days / TRADING_DAYS
    return np.sqrt((1 + 0.5 * sr ** 2) / t_years)


def max_drawdown(ret_simple):
    """Worst peak-to-trough decline of the compounded equity curve."""
    cum = (1 + ret_simple).cumprod()
    peak = cum.cummax()
    return ((cum - peak) / peak).min()


def sortino(ret_simple, rf_annual=0.025):
    """(annualized return − rf) / annualized downside deviation."""
    r = ret_simple.dropna()
    down = r[r < 0]
    if len(down) == 0 or down.std() == 0:
        return 0.0
    return (annualized_return(r) - rf_annual) / (down.std() * np.sqrt(TRADING_DAYS))


def calmar(ret_simple):
    """Annualized return / |max drawdown|."""
    mdd = abs(max_drawdown(ret_simple))
    return annualized_return(ret_simple) / mdd if mdd > 0 else 0.0


def var_cvar(ret_simple, level=0.95):
    """Historical VaR and CVaR at the given confidence level.
    VaR = the (1−level) quantile of daily returns; CVaR = mean return in the
    tail at or beyond VaR."""
    r = ret_simple.dropna()
    var = np.percentile(r, 100 * (1 - level))
    tail = r[r <= var]
    cvar = tail.mean() if len(tail) > 0 else var
    return var, cvar


def turnover(w_new, w_old):
    """One-rebalance L1 turnover: Σ|Δw|."""
    return float(np.abs(np.asarray(w_new) - np.asarray(w_old)).sum())


def hhi(w):
    """Herfindahl–Hirschman concentration of weights: Σ w²
    (1/n for equal weight; 1.0 for a single position)."""
    return float((np.asarray(w) ** 2).sum())


def summary(ret_simple, rf_annual=0.025):
    """Drop-in replacement for the notebooks' compute_metrics(ret) dict.

    Same keys, same formulas: ann_ret, ann_vol, sharpe, sharpe_se,
    sharpe_ci_lo/hi (±1.96·SE), max_dd, sortino, var95, cvar95, n_days
    (+ calmar). Returns NaNs for series shorter than 30 observations.
    """
    r = ret_simple.dropna()
    keys = ['ann_ret', 'ann_vol', 'sharpe', 'sharpe_se', 'sharpe_ci_lo',
            'sharpe_ci_hi', 'max_dd', 'sortino', 'var95', 'cvar95',
            'calmar', 'n_days']
    if len(r) < 30:
        return {k: np.nan for k in keys}
    sr = sharpe(r, rf_annual)
    se = sharpe_se(sr, len(r))
    var95, cvar95 = var_cvar(r, 0.95)
    return {
        'ann_ret': annualized_return(r),
        'ann_vol': annualized_vol(r),
        'sharpe': sr,
        'sharpe_se': se,
        'sharpe_ci_lo': sr - 1.96 * se,
        'sharpe_ci_hi': sr + 1.96 * se,
        'max_dd': max_drawdown(r),
        'sortino': sortino(r, rf_annual),
        'var95': var95,
        'cvar95': cvar95,
        'calmar': calmar(r),
        'n_days': len(r),
    }
