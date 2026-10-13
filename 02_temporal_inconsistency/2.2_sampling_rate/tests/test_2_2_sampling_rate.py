"""Scientific prerequisite negative control for sampling; numerical invariants in root tests."""
import pytest
from fmri_reference.demo import error_example

def test_sampling_invalid_input_must_not_silently_run():
    with pytest.raises((ValueError,FileNotFoundError)):
        error_example("sampling")
