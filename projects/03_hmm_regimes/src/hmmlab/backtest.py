"""Walk-forward regime-switching backtest (extracted verbatim, 2.2).

Structural changes only: vix and n_regimes are explicit parameters (the
notebook version read both from globals); the unused scaler_ref parameter
(dead since the 1.2 P3-1 fix) is removed.
"""
import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM


def run_regime_backtest(spy_ret, tlt_ret, features_scaled_full, features_raw_full,
                        vix, config, n_regimes, hmm_seed=42, verbose=True):
    """
    Walk-forward regime-switching backtest.
    At each rebalance: fit HMM on trailing data, infer current regime, allocate.
    """
    lookback = config['lookback_hmm']
    rebal_freq = config['rebal_frequency']
    
    # Align data
    common = spy_ret.index.intersection(tlt_ret.index).intersection(features_scaled_full.index)
    # G-2 fix: spy_ret/tlt_ret are LOG returns (HMM features need them); the
    # equity/bond mix w·r_spy + (1-w)·r_tlt is only valid on SIMPLE returns.
    spy_r = np.expm1(spy_ret.reindex(common))
    tlt_r = np.expm1(tlt_ret.reindex(common))
    feats = features_scaled_full.reindex(common)
    
    all_dates = common[lookback:]
    rebal_dates = all_dates[::rebal_freq]
    
    # Strategy storage
    strategies = {
        'hmm_switch': {'alloc_equity': [], 'returns': [], 'dates': []},
        'buy_hold': {'returns': [], 'dates': []},
        'sixty_forty': {'returns': [], 'dates': []},
        'vix_switch': {'returns': [], 'dates': []},
        'vol_switch': {'returns': [], 'dates': []},
    }
    
    current_alloc = 1.0  # start fully invested
    vix_aligned = vix.reindex(common).ffill()
    raw_feats = features_raw_full.reindex(common)
    
    for idx, rebal_date in enumerate(rebal_dates):
        if idx == len(rebal_dates) - 1:
            break
        
        # Trailing window
        end_loc = common.get_loc(rebal_date)
        start_loc = max(0, end_loc - lookback)
        # P3-1 fix: standardize the window with ITS OWN trailing mean/std —
        # both are measurable at the rebalance date. No full-sample scaler.
        win = raw_feats.iloc[start_loc:end_loc]
        mu_win, sd_win = win.mean(), win.std()
        X_trail = ((win - mu_win) / sd_win).values
        
        # ── FIT HMM ON TRAILING DATA ──
        try:
            hmm = GaussianHMM(n_components=n_regimes, covariance_type='full',
                               n_iter=100, tol=1e-3, random_state=hmm_seed, verbose=False)
            hmm.fit(X_trail)
            
            # Get current state probability (last observation)
            probs = hmm.predict_proba(X_trail)[-1]
            
            # Sort regimes by vol (using HMM means)
            hmm_means_raw = hmm.means_ * sd_win.values + mu_win.values  # window stats, not a global scaler
            vol_order = np.argsort(hmm_means_raw[:, 1])
            
            # Allocation: based on probability-weighted regime vol
            # Low-vol regime → equity, High-vol → defensive
            equity_weight = 0.0
            for rank, orig_k in enumerate(vol_order):
                if rank == 0:  # lowest vol
                    equity_weight += probs[orig_k] * 1.0
                elif rank == len(vol_order) - 1:  # highest vol
                    equity_weight += probs[orig_k] * 0.0
                else:  # middle
                    equity_weight += probs[orig_k] * 0.5
            
            equity_weight = np.clip(equity_weight, 0, 1)
            
        except Exception:
            equity_weight = 0.5  # fallback
        
        # ── BENCHMARKS ──
        vix_now = vix_aligned.iloc[end_loc] if end_loc < len(vix_aligned) else 20
        vol_now = raw_feats.iloc[end_loc]['realized_vol'] if end_loc < len(raw_feats) else 0.15
        
        vix_equity = 1.0 if vix_now < 20 else (0.0 if vix_now > 30 else 0.5)
        vol_equity = 1.0 if vol_now < 0.15 else (0.0 if vol_now > 0.25 else 0.5)
        
        # ── FORWARD RETURNS ──
        next_rebal = rebal_dates[idx+1] if idx+1 < len(rebal_dates) else common[-1]
        fwd = common[(common > rebal_date) & (common <= next_rebal)]
        
        if len(fwd) == 0:
            continue
        
        for day in fwd:
            r_spy = spy_r.loc[day]
            r_tlt = tlt_r.loc[day] if day in tlt_r.index else 0.0
            
            strategies['hmm_switch']['returns'].append(equity_weight * r_spy + (1-equity_weight) * r_tlt)
            strategies['hmm_switch']['dates'].append(day)
            strategies['hmm_switch']['alloc_equity'].append(equity_weight)
            
            strategies['buy_hold']['returns'].append(r_spy)
            strategies['buy_hold']['dates'].append(day)
            
            strategies['sixty_forty']['returns'].append(0.6 * r_spy + 0.4 * r_tlt)
            strategies['sixty_forty']['dates'].append(day)
            
            strategies['vix_switch']['returns'].append(vix_equity * r_spy + (1-vix_equity) * r_tlt)
            strategies['vix_switch']['dates'].append(day)
            
            strategies['vol_switch']['returns'].append(vol_equity * r_spy + (1-vol_equity) * r_tlt)
            strategies['vol_switch']['dates'].append(day)
        
        if verbose and idx % 20 == 0:
            print(f"  Rebalance {idx+1}/{len(rebal_dates)-1} at {rebal_date.date()} | equity alloc: {equity_weight:.2f}")
    
    # Convert to Series
    for s in strategies:
        strategies[s]['returns'] = pd.Series(strategies[s]['returns'], index=strategies[s]['dates'])
    
    return strategies
