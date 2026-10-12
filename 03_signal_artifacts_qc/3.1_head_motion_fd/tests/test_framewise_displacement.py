import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from framewise_displacement import framewise_displacement

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert framewise_displacement(np.zeros((4,6))).shape==(4,)
