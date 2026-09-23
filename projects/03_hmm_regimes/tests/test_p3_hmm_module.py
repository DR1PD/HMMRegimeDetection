"""fit_hmm_with_restarts + the filtering core against the real package."""
import numpy as np

from hmmlab import fit_hmm_with_restarts, filtered_probabilities


def _regime_data(T=400, seed=0):
    rng = np.random.default_rng(seed)
    states = (np.arange(T) // 100) % 2
    return np.where(states[:, None] == 0,
                    rng.normal(0, 1, (T, 3)), rng.normal(0, 4, (T, 3)))


def test_restarts_fit_and_log_convergence():
    X = _regime_data()
    model, score, log = fit_hmm_with_restarts(X, 2, n_restarts=3, max_iter=50)
    assert model is not None and len(log) == 3
    assert any(e.get('converged') for e in log)


def test_filtered_probabilities_causal_via_package():
    X = _regime_data()
    model, _, _ = fit_hmm_with_restarts(X, 2, n_restarts=2, max_iter=50)
    t = 250
    full = filtered_probabilities(model, X)
    trunc = filtered_probabilities(model, X[:t])
    assert np.allclose(full[:t], trunc, atol=1e-10)
