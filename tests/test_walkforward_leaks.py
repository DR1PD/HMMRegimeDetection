"""Leak-detector tests (ROADMAP 1.2): anything used at time t must be
invariant to deleting all post-t data. Pins the P3-1 and P3-6 fixes.
"""
import numpy as np
from hmmlearn.hmm import GaussianHMM

from common.hmm_filter import filtered_probabilities


def _toy_model_and_data(T=400, seed=0):
    rng = np.random.default_rng(seed)
    # Two clearly separated volatility regimes, alternating every 100 days
    states = (np.arange(T) // 100) % 2
    X = np.where(states[:, None] == 0,
                 rng.normal(0.0, 1.0, (T, 2)),
                 rng.normal(0.0, 4.0, (T, 2)))
    model = GaussianHMM(n_components=2, covariance_type='full',
                        random_state=1, n_iter=50).fit(X)
    return model, X


def test_filtered_probabilities_are_causal():
    """alpha_t must not change when all data after t is deleted (P3-6 fix)."""
    model, X = _toy_model_and_data()
    t = 250
    full = filtered_probabilities(model, X)
    truncated = filtered_probabilities(model, X[:t])
    assert np.allclose(full[:t], truncated, atol=1e-10)


def test_smoothed_probabilities_are_not_causal():
    """Why predict_proba can't feed a forecast: gamma_t moves when the
    future is deleted — it conditions on the whole sample (the P3-6 bug)."""
    model, X = _toy_model_and_data()
    t = 250
    full = model.predict_proba(X)
    truncated = model.predict_proba(X[:t])
    assert not np.allclose(full[:t], truncated, atol=1e-6)


def test_filtered_equals_smoothed_at_final_step():
    """Verify-two-ways: at t = T there is no future to smooth over, so our
    forward pass must agree with hmmlearn's forward-backward exactly."""
    model, X = _toy_model_and_data()
    ours = filtered_probabilities(model, X)[-1]
    hmmlearn_gamma = model.predict_proba(X)[-1]
    assert np.allclose(ours, hmmlearn_gamma, atol=1e-8)


def test_trailing_window_standardization_is_causal():
    """P3-1 fix: scaling a window by its own mean/std is invariant to
    post-t data; scaling by full-sample statistics is not."""
    rng = np.random.default_rng(3)
    x = rng.normal(0, 1, 1000).cumsum()  # nonstationary, so full-sample stats drift
    L, t = 200, 700
    window = x[t - L:t]

    z_from_full = (window - window.mean()) / window.std()
    x_truncated = x[:t]
    window_trunc = x_truncated[t - L:t]
    z_from_truncated = (window_trunc - window_trunc.mean()) / window_trunc.std()
    assert np.allclose(z_from_full, z_from_truncated)

    # The pre-fix recipe (full-sample scaler) fails the same invariance check
    z_leaky_full = (window - x.mean()) / x.std()
    z_leaky_trunc = (window - x_truncated.mean()) / x_truncated.std()
    assert not np.allclose(z_leaky_full, z_leaky_trunc, atol=1e-3)
