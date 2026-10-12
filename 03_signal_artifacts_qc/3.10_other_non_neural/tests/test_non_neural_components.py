import pytest
np = pytest.importorskip("numpy")
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from non_neural_components import non_neural_components

def test_smoke():
    x=np.arange(24,dtype=float).reshape(4,6)
    assert len(non_neural_components(x)['singular_values'])>0
