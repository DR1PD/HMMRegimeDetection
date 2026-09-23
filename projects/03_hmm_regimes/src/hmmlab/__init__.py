"""P3 strategy package (DESIGN Section L via src-layout; ROADMAP 2.2).

The causal filtering core is common/hmm_filter.py (shared repo-wide).
"""
from common.hmm_filter import filtered_probabilities

from .data import load_close
from .features import build_features
from .hmm_model import fit_hmm_with_restarts, compute_bic
from .backtest import run_regime_backtest
