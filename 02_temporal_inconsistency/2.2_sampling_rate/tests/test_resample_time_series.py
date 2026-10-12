import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from resample_time_series import resample_time_series

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert resample_time_series(np.arange(5.),old_tr=2,new_tr=1).size==9
