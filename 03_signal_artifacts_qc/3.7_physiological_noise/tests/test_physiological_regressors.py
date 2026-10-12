import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from physiological_regressors import physiological_regressors

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert physiological_regressors(np.arange(4.),period=2.0).shape[0]==4
