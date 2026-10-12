import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from scanner_drift import scanner_drift

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert len(scanner_drift(np.arange(4.)))==2
