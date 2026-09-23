"""Schema-validated config loading (ROADMAP 2.3).

Each project's parameters live in projects/<name>/config.yaml — generated
mechanically from the notebooks' CONFIG dicts, never hand-typed. This loader
fails LOUDLY: missing keys, unknown keys, wrong types, or malformed dates all
raise ConfigError with the offending key named. No silent defaults anywhere —
a config that doesn't match its schema is a stopped run, not a guess.
"""
import re
from datetime import datetime
from pathlib import Path

import yaml


class ConfigError(ValueError):
    pass


_DATE = 'date'  # YYYY-MM-DD string, validated

SCHEMAS = {
    'p1': {
        'tickers': list, 'start_date': _DATE, 'end_date': _DATE,
        'is_end': _DATE, 'oos_start': _DATE,
        'lookback_days': int, 'rebal_frequency': int,
        'gamma': float, 'kappa': float, 'w_max': float, 'tau_max': float,
        'c_prop': float, 'c_impact': float,
        'ewma_halflife': int, 'shrinkage_method': str,
        'var_confidence': float, 'cvar_confidence': float,
    },
    'p2': {
        'tickers': list, 'start_date': _DATE, 'end_date': _DATE,
        'is_end': _DATE, 'oos_start': _DATE,
        'lookback_days': int, 'rebal_frequency': int,
        'w_max': float, 'c_prop': float, 'c_impact': float,
    },
    'p3': {
        'start_date': _DATE, 'end_date': _DATE, 'is_end': _DATE,
        'oos_start': _DATE,
        'vol_window': int, 'corr_window': int,
        'n_regimes_test': list, 'n_em_restarts': int,
        'em_max_iter': int, 'em_tol': float,
        'rebal_frequency': int, 'lookback_hmm': int,
        'equity_ticker': str, 'bond_ticker': str,
        'c_prop': float, 'var_confidence': float,
    },
}

_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def _check(key, value, expected):
    if expected is _DATE:
        if not (isinstance(value, str) and _DATE_RE.match(value)):
            raise ConfigError(f"{key}: expected YYYY-MM-DD date string, got {value!r}")
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            raise ConfigError(f"{key}: invalid calendar date {value!r} ({e})")
    elif expected is float:
        # ints are acceptable floats; bools are not
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ConfigError(f"{key}: expected number, got {type(value).__name__}")
    elif expected is int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ConfigError(f"{key}: expected int, got {type(value).__name__}")
    elif not isinstance(value, expected):
        raise ConfigError(f"{key}: expected {expected.__name__}, got {type(value).__name__}")


def load_config(path, project):
    """Load and validate a project config.yaml.

    Args:
        path: path to the yaml file (str or Path)
        project: schema key — 'p1', 'p2', or 'p3'

    Returns: plain dict, exactly the yaml contents (no defaults injected).
    Raises: ConfigError on missing/unknown keys, type or date violations.
    """
    schema = SCHEMAS[project]
    path = Path(path)
    if not path.exists():
        raise ConfigError(f"config file not found: {path}")
    cfg = yaml.safe_load(path.read_text())
    if not isinstance(cfg, dict):
        raise ConfigError(f"{path}: top level must be a mapping")

    missing = sorted(set(schema) - set(cfg))
    unknown = sorted(set(cfg) - set(schema))
    if missing:
        raise ConfigError(f"{path}: missing required keys {missing}")
    if unknown:
        raise ConfigError(f"{path}: unknown keys {unknown} — schema and yaml must agree exactly")
    for key, expected in schema.items():
        _check(key, cfg[key], expected)
    return cfg
