import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from dvars import dvars

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert np.allclose(dvars(x), np.sqrt(np.mean(np.diff(x,axis=-1)**2,axis=0)))
