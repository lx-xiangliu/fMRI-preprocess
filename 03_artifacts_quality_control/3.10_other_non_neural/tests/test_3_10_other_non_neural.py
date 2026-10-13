"""Scientific prerequisite negative control for components; numerical invariants in root tests."""
import pytest
from fmri_reference.demo import error_example

def test_components_invalid_input_must_not_silently_run():
    with pytest.raises((ValueError,FileNotFoundError)):
        error_example("components")
