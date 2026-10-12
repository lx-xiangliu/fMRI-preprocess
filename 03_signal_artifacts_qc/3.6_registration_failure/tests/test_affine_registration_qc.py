import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from affine_registration_qc import affine_registration_qc

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert affine_registration_qc(np.eye(4),reference_affine=np.eye(4))['finite']
