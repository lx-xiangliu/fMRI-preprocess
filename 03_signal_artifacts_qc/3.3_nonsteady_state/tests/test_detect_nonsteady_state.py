import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from detect_nonsteady_state import detect_nonsteady_state

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert isinstance(detect_nonsteady_state(x),list)
