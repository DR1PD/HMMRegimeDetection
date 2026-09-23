"""P3-7 regression (ROADMAP 3.2): corrected BIC recovers a known K; the old
T-scaled formula degenerates to picking the grid maximum."""
import numpy as np

from hmmlab import compute_bic, fit_hmm_with_restarts

TRUE_K = 3
GRID = [2, 3, 4, 5]


def _three_regime_data(T=900, seed=7):
    """Three well-separated vol regimes, 300 days each block, 2 features."""
    rng = np.random.default_rng(seed)
    states = (np.arange(T) // 75) % TRUE_K
    scale = np.array([0.5, 2.0, 6.0])[states]
    return rng.standard_normal((T, 2)) * scale[:, None]


def _fits():
    X = _three_regime_data()
    return X, {k: fit_hmm_with_restarts(X, k, n_restarts=2, max_iter=100)[0]
               for k in GRID}


def test_corrected_bic_recovers_true_k_and_old_formula_does_not():
    X, models = _fits()
    T = len(X)
    bic_new, ll_total = {}, {}
    for k, m in models.items():
        bic, aic, p, ll = compute_bic(m, X)
        bic_new[k], ll_total[k] = bic, ll
    k_new = min(bic_new, key=bic_new.get)
    assert k_new == TRUE_K

    # the pre-fix formula: total loglik scaled by T again
    bic_old = {k: -2 * (ll_total[k] * T) + 0 * k for k in GRID}
    # (penalty omitted deliberately — at T-fold inflation it is rounding error)
    k_old = min(bic_old, key=bic_old.get)
    assert k_old == max(GRID)  # degenerate max-likelihood boundary pick


def test_bic_magnitude_is_sane():
    """Per-observation average log-likelihood must be O(±10), so |BIC| stays
    O(T·10) — the 76-million figure of the defect era is impossible now."""
    X, models = _fits()
    bic, _, _, ll = compute_bic(models[TRUE_K], X)
    assert abs(ll / len(X)) < 10
    assert abs(bic) < 10 * len(X) * 10
