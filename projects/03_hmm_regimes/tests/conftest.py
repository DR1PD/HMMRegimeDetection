"""Make src/hmmlab and the repo root (common/) importable for these tests."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent / 'src'), str(HERE.parent.parent.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)
