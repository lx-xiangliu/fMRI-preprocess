import pytest
from fmri_reference.pipelines import fmriprep_command

def test_mutable_container_ref_rejected(tmp_path):
    bids=tmp_path/'bids';bids.mkdir();(bids/'dataset_description.json').write_text('{}')
    with pytest.raises(ValueError,match='digest'):fmriprep_command(bids,tmp_path/'out',tmp_path/'work','nipreps/fmriprep:latest','01')

def test_command_protects_input_and_subject_arguments(tmp_path):
    bids=tmp_path/'bids with spaces';bids.mkdir();(bids/'dataset_description.json').write_text('{}');digest='nipreps/fmriprep@sha256:'+'a'*64
    command=fmriprep_command(bids,tmp_path/'out',tmp_path/'work',digest,'01');assert str(bids)+':/data:ro' in command
    with pytest.raises(ValueError):fmriprep_command(bids,tmp_path/'out',tmp_path/'work',digest,'01;bad')
