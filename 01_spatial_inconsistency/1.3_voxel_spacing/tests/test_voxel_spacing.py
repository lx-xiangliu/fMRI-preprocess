import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from voxel_spacing import voxel_spacing

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert len(voxel_spacing(x, affine=np.eye(4)))==3
