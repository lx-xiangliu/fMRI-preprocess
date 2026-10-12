import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from coordinate_report import coordinate_report

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert coordinate_report(np.eye(4))['matches']
