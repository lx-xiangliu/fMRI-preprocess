"""Scientific prerequisite negative control for resolution; numerical invariants in root tests."""
import pytest
from fmri_reference.demo import error_example

def test_resolution_invalid_input_must_not_silently_run():
    with pytest.raises((ValueError,FileNotFoundError)):
        error_example("resolution")
