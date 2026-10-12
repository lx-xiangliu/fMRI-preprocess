import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from percent_signal_change import percent_signal_change

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert percent_signal_change(x).shape==x.shape
