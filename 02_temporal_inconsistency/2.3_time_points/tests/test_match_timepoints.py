import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from match_timepoints import match_timepoints

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert match_timepoints(x,n_timepoints=8).shape[-1]==8
