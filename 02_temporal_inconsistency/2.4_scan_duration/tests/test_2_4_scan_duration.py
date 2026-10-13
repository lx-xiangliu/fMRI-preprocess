"""Scientific prerequisite negative control for duration; numerical invariants in root tests."""
import pytest
from fmri_reference.demo import error_example

def test_duration_invalid_input_must_not_silently_run():
    with pytest.raises((ValueError,FileNotFoundError)):
        error_example("duration")
