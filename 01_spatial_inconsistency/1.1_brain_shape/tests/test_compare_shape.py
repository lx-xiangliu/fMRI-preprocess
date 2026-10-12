import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from compare_shape import compare_shape

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert compare_shape(x, reference_shape=x.shape)['matches']
