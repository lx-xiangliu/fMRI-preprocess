import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from resolution_report import resolution_report

def test_smoke():
    x=np.arange(24,dtype=float).reshape(2,3,4)
    assert resolution_report(x, affine=np.eye(4))['shape']==(2,3,4)
