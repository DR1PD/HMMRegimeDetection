"""Shared plotting theme — single source of truth for the dark research aesthetic.

Extracted from the project notebooks (ROADMAP 2.1). Import and call apply_theme()
instead of redefining rcParams per notebook.
"""
import matplotlib.pyplot as plt

COLORS = {
    'primary':  '#00d4aa',  # teal-green — our strategy / signal
    'contrast': '#ff6b6b',  # coral — main comparison
    'alt1':     '#4ecdc4',  # light teal
    'alt2':     '#ffd93d',  # gold
    'alt3':     '#c084fc',  # purple
    'neutral':  '#6b7280',  # gray — passive benchmarks
    'accent':   '#3b82f6',  # blue
    'danger':   '#ef4444',  # red — drawdowns / noise
    'warn':     '#f59e0b',  # amber
}


def apply_theme():
    """Apply the dark research theme. Call once at the top of each notebook."""
    plt.style.use('dark_background')
    plt.rcParams.update({
        'figure.figsize': (14, 6),
        'font.family': 'monospace',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'axes.edgecolor': '#444444',
        'axes.facecolor': '#0a0a0a',
        'figure.facecolor': '#0a0a0a',
        'grid.color': '#222222',
        'grid.alpha': 0.5,
        'text.color': '#cccccc',
        'axes.labelcolor': '#cccccc',
        'xtick.color': '#888888',
        'ytick.color': '#888888',
    })
