import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from validate_tr import validate_tr

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert validate_tr({'RepetitionTime': 2.0})['tr_seconds']==2.0
