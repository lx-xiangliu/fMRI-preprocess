import pytest
np = pytest.importorskip("numpy")
nib = pytest.importorskip("nibabel")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from canonicalize_orientation import canonicalize_orientation

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert canonicalize_orientation(nib.Nifti1Image(x.reshape(2,3,4), np.eye(4))) is not None
