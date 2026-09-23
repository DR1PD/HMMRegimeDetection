"""Market-data loading for P3 (2.2). Explicit parameters — the notebook
version closed over CONFIG (a notebook-global read, now removed).
"""
from common.data import download_prices


def load_close(ticker, cache_name, start, end):
    """Adjusted close via common.data.download_prices (cache-first, ROADMAP 2.1).
    Returns a 1-col DataFrame; callers squeeze to Series."""
    return download_prices(ticker, start, end,
                           cache_name=cache_name)
