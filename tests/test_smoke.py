"""Repo-level smoke test: the environment imports its core dependencies."""


def test_core_imports():
    import cvxpy, hmmlearn, sklearn, statsmodels, yfinance  # noqa: F401


def test_common_imports():
    from common.plotting import COLORS, apply_theme  # noqa: F401
    assert 'primary' in COLORS
