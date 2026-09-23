"""G-2 regression tests (ROADMAP 1.1): portfolio aggregation must use simple returns.

The defect: all three backtests computed portfolio return as w · r_log.
A portfolio's one-period return is w · r_simple exactly; the weighted sum of
log returns is neither the portfolio's simple nor its log return, and by
Jensen's inequality (log is concave) it systematically understates growth —
worst for diversified portfolios, which is where the rebalancing premium lives.
"""
import numpy as np


def _toy_returns(T=20 * 252, seed=42):
    rng = np.random.default_rng(seed)
    # 2 assets, deliberately different vols so the convexity gap is visible
    return rng.normal(0.0004, [0.010, 0.030], size=(T, 2))


def test_weighted_simple_returns_equal_exact_portfolio_accounting():
    """w · r_simple is EXACTLY the portfolio's one-period return."""
    r_simple = _toy_returns()
    w = np.array([0.5, 0.5])
    # Direct accounting: split $1 by w, let each leg grow one day, re-mark.
    end_value = w[0] * (1 + r_simple[:, 0]) + w[1] * (1 + r_simple[:, 1])
    assert np.allclose(end_value - 1, r_simple @ w, atol=1e-15)


def test_weighted_log_returns_understate_growth():
    """The G-2 formula w · r_log compounds to strictly less wealth (Jensen)."""
    r_simple = _toy_returns()
    w = np.array([0.5, 0.5])
    r_log = np.log1p(r_simple)

    wealth_correct = np.prod(1 + r_simple @ w)
    wealth_bugged = np.prod(1 + r_log @ w)  # what the backtests computed

    assert wealth_bugged < wealth_correct

    # The gap is material at 20y horizon: understated CAGR by tens of bps/yr
    years = len(r_simple) / 252
    cagr_correct = wealth_correct ** (1 / years) - 1
    cagr_bugged = wealth_bugged ** (1 / years) - 1
    assert (cagr_correct - cagr_bugged) > 0.0010  # > 10 bps/yr on this toy


def test_gap_grows_with_diversification():
    """The discarded Jensen term is the diversification premium: a 50/50 mix
    loses more to the bug than a concentrated 95/5 mix — so the bug biases
    strategy *rankings* against diversified portfolios, not just levels."""
    r_simple = _toy_returns()
    r_log = np.log1p(r_simple)

    def cagr_gap(w):
        w = np.asarray(w)
        years = len(r_simple) / 252
        correct = np.prod(1 + r_simple @ w) ** (1 / years)
        bugged = np.prod(1 + r_log @ w) ** (1 / years)
        return correct - bugged

    assert cagr_gap([0.5, 0.5]) > cagr_gap([0.95, 0.05])
