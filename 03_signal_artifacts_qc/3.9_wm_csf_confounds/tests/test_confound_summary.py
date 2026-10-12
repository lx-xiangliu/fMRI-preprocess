import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from confound_summary import confound_summary

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert confound_summary(x)['n_timepoints']==4
