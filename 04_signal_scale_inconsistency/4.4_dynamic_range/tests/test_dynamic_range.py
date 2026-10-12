import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from dynamic_range import dynamic_range

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert dynamic_range(x)['robust_range']>=0
