"""run_regime_backtest: explicit-parameter signature + smoke invariants."""
import inspect

import numpy as np
import pandas as pd

from hmmlab import build_features, run_regime_backtest


def test_signature_has_no_global_dependencies():
    params = list(inspect.signature(run_regime_backtest).parameters)
    assert 'vix' in params and 'n_regimes' in params
    assert 'scaler_ref' not in params  # dead since 1.2, removed at extraction


def test_backtest_smoke_allocations_bounded():
    rng = np.random.default_rng(1)
    T = 400
    idx = pd.date_range('2015-01-01', periods=T, freq='B')
    spy_ret = pd.Series(np.clip(rng.normal(0.0003, 0.01, T), -0.03, 0.03), index=idx)
    tlt_ret = pd.Series(np.clip(rng.normal(0.0001, 0.006, T), -0.02, 0.02), index=idx)
    vix = pd.Series(18 + np.clip(rng.normal(0, 1.5, T), -4, 4).cumsum() * 0.05, index=idx)
    scaled, raw, _ = build_features(spy_ret, vix, 21, scaler_fit_end=idx[200])
    cfg = {'lookback_hmm': 120, 'rebal_frequency': 21}
    bt = run_regime_backtest(spy_ret, tlt_ret, scaled, raw, vix, cfg,
                             n_regimes=2, verbose=False)
    assert set(bt) == {'hmm_switch', 'buy_hold', 'sixty_forty',
                       'vix_switch', 'vol_switch'}
    alloc = np.array(bt['hmm_switch']['alloc_equity'])
    assert ((alloc >= 0) & (alloc <= 1)).all()
    for s in bt:
        assert np.isfinite(bt[s]['returns']).all()
