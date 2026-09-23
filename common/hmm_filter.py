"""Causal (filtered) HMM state probabilities — forward pass only.

P3-6: hmmlearn's predict_proba returns SMOOTHED posteriors gamma_t(k) =
P(state_t | x_1..T), which condition on the entire sample — data after t
included — so they cannot feed a forecast made at time t. The filtered
probabilities alpha_t(k) = P(state_t | x_1..t) use only data through t.

Math: log-space forward recursion
    log a_1(k) = log pi_k + log b_k(x_1)
    log a_t(k) = log b_k(x_t) + logsumexp_j( log a_{t-1}(j) + log A_{jk} )
normalized per step so each row sums to 1. b_k is the Gaussian emission
density built from the model's public means_/covars_ (no private hmmlearn
API). This is also the first slice of the Phase 4.1 hand-rolled HMM core.

Verified two ways (tests/test_walkforward_leaks.py): alpha_t is invariant
to deleting all post-t data, and alpha_T equals hmmlearn's gamma_T at the
final step, where filtering and smoothing coincide by definition.
"""
import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_normal


def _emission_loglik(model, X):
    """(T, K) matrix of log N(x_t; mu_k, Sigma_k) from public attributes."""
    X = np.asarray(X)
    out = np.empty((len(X), model.n_components))
    for k in range(model.n_components):
        out[:, k] = multivariate_normal.logpdf(
            X, mean=model.means_[k], cov=model.covars_[k], allow_singular=True
        )
    return out


def filtered_probabilities(model, X):
    """alpha_t(k) = P(state_t = k | x_1..t) for a fitted GaussianHMM.

    Args:
        model: fitted hmmlearn GaussianHMM (any covariance_type with dense covars_)
        X: (T, d) observation matrix

    Returns:
        (T, K) array; row t uses only observations 1..t (causal).
    """
    log_b = _emission_loglik(model, X)
    log_A = np.log(model.transmat_ + 1e-300)
    log_alpha = np.empty_like(log_b)
    log_alpha[0] = np.log(model.startprob_ + 1e-300) + log_b[0]
    for t in range(1, len(log_b)):
        log_alpha[t] = log_b[t] + logsumexp(log_alpha[t - 1][:, None] + log_A, axis=0)
    log_alpha -= logsumexp(log_alpha, axis=1, keepdims=True)
    return np.exp(log_alpha)
