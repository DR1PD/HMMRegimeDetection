"""HMM fitting with restarts + model selection (extracted verbatim, 2.2).

The filtering core (causal forward pass) lives in common/hmm_filter.py —
shared with the tests and the forecast study since ROADMAP 1.2.
"""
import numpy as np
from hmmlearn.hmm import GaussianHMM

from common.hmm_filter import filtered_probabilities  # re-exported filtering core


def fit_hmm_with_restarts(X, n_components, n_restarts=10, max_iter=200, tol=1e-4):
    """
    Fit Gaussian HMM with multiple random restarts.
    Returns the best model (highest log-likelihood).
    """
    best_model = None
    best_score = -np.inf
    convergence_log = []
    
    for restart in range(n_restarts):
        model = GaussianHMM(
            n_components=n_components,
            covariance_type='full',
            n_iter=max_iter,
            tol=tol,
            random_state=restart * 42,
            verbose=False,
        )
        
        try:
            model.fit(X)
            score = model.score(X)
            convergence_log.append({
                'restart': restart, 'score': score,
                'converged': model.monitor_.converged,
                'n_iter': model.monitor_.iter,
            })
            
            if score > best_score:
                best_score = score
                best_model = model
        except Exception as e:
            convergence_log.append({'restart': restart, 'score': np.nan, 'error': str(e)})
    
    return best_model, best_score, convergence_log


def compute_bic(model, X):
    """Compute BIC for a fitted HMM."""
    T, d = X.shape
    K = model.n_components
    
    # Parameters: K-1 initial probs + K*(K-1) transition + K*d means + K*d*(d+1)/2 covariances
    n_params = (K - 1) + K * (K - 1) + K * d + K * d * (d + 1) // 2
    
    log_likelihood = model.score(X)  # TOTAL log-likelihood (P3-7 fix)
    bic = -2 * log_likelihood + n_params * np.log(T)
    aic = -2 * log_likelihood + 2 * n_params
    
    return bic, aic, n_params, log_likelihood


def compute_bic(model, X):
    """Compute BIC/AIC for a fitted HMM (P3-7 FIXED, ROADMAP 3.2).

    hmmlearn's .score(X) returns the TOTAL log-likelihood — it is used
    directly. (The pre-3.2 version multiplied it by T under a comment
    claiming a per-sample average, inflating the likelihood ~T-fold and
    degenerating K selection to max-likelihood; regression-tested in
    tests/test_p3_bic_module.py, where correct BIC recovers a known K and
    the old formula picks the grid max.)"""
    T, d = X.shape
    K = model.n_components
    
    # Parameters: K-1 initial probs + K*(K-1) transition + K*d means + K*d*(d+1)/2 covariances
    n_params = (K - 1) + K * (K - 1) + K * d + K * d * (d + 1) // 2
    
    log_likelihood = model.score(X)  # TOTAL log-likelihood (P3-7 fix)
    bic = -2 * log_likelihood + n_params * np.log(T)
    aic = -2 * log_likelihood + 2 * n_params
    
    return bic, aic, n_params, log_likelihood
