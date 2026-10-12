import pytest
from fmri_common import aomic, get_tr, load_physio


def _have_data():
    try:
        return aomic().bold.exists()
    except FileNotFoundError:
        return False


pytestmark = pytest.mark.skipif(not _have_data(), reason="reference data not downloaded")


def test_tr_from_sidecar():
    f = aomic(task="restingstate")
    assert get_tr(f.bold, f.bold_json) == pytest.approx(0.75)
    f = aomic(task="workingmemory")
    assert get_tr(f.bold, f.bold_json) == pytest.approx(2.0)


def test_physio_loads():
    f = aomic(task="restingstate")
    df, fs, start = load_physio(f.physio, f.physio_json)
    assert fs > 0 and len(df) > 0
