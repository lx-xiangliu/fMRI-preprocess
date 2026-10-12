import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from coverage_and_tsnr import coverage_and_tsnr

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert 0 <= coverage_and_tsnr(x)['coverage'] <= 1
