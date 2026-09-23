"""build_features leak discipline against the REAL package (migrated from the
repo-level recipe tests). Outlier-free inputs by construction, so the
documented full-sample-winsorization residue (owned by ROADMAP 3.1) is a
no-op and the scaler discipline can be tested exactly."""
import numpy as np
import pandas as pd

from hmmlab import build_features


def _toy_inputs(T=800, seed=4):
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2016-01-01', periods=T, freq='B')
    # bounded, outlier-free draws: winsorize clips nothing
    spy_ret = pd.Series(np.clip(rng.normal(0.0003, 0.008, T), -0.02, 0.02), index=idx)
    vix = pd.Series(18 + np.clip(rng.normal(0, 1.5, T), -4, 4).cumsum() * 0.05, index=idx)
    return spy_ret, vix


def test_feature_pipeline_exactly_invariant_to_future_data():
    """Delete-the-future on the REAL pipeline, now EXACT (ROADMAP 3.1): with
    causal expanding-window winsorization + the frozen-IS scaler, features
    through the cutoff are bit-identical whether or not post-cutoff data
    exists. (Until 3.1 this test pinned the measured full-sample-quantile
    residue: bulk drift < 5e-3, clipped extremes up to ~0.1 sigma — see git
    history; that residue is now zero by construction.)"""
    spy_ret, vix = _toy_inputs()
    cutoff = spy_ret.index[500]
    full, _, _ = build_features(spy_ret, vix, 21, scaler_fit_end=cutoff)
    trunc, _, _ = build_features(spy_ret[spy_ret.index <= cutoff],
                                 vix[vix.index <= cutoff], 21, scaler_fit_end=cutoff)
    diff = np.abs(full.loc[trunc.index].values - trunc.values)
    assert diff.max() < 1e-12


def test_observation_vector_is_exactly_three_features():
    """The spec's correlation/yield-curve features are NOT implemented
    (reconciliation 1.7): the vector is (return, realized_vol, vix_change).
    [Restored — accidentally truncated by the 3.1 test rewrite.]"""
    spy_ret, vix = _toy_inputs()
    scaled, raw, scaler = build_features(spy_ret, vix, 21, scaler_fit_end=spy_ret.index[-1])
    assert list(scaled.columns) == ['return', 'realized_vol', 'vix_change']
