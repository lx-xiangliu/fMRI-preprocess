import numpy as np
import nibabel as nib
import pytest
from fmri_reference.streaming import stream_qc
from fmri_reference.core import dvars,tsnr

def test_stream_qc_independent_vectorized_oracle(tmp_path):
    rng=np.random.default_rng(11);data=rng.normal(100,3,(3,4,5,20)).astype(np.float32);mask=np.indices(data.shape[:3]).sum(0)%2==0
    img=nib.Nifti1Image(data,np.diag([2.,2.,2.,1.]));img.header.set_xyzt_units('mm','sec');p=tmp_path/'raw.nii';nib.save(img,p)
    out=stream_qc(p,mask);x=data[mask].T.astype(float)
    np.testing.assert_allclose(out['dvars'],dvars(x),rtol=1e-12,equal_nan=True);np.testing.assert_allclose(out['tsnr'],tsnr(x),rtol=1e-12)

def test_stream_qc_rejects_empty_mask(tmp_path):
    img=nib.Nifti1Image(np.ones((3,4,5,3)),np.eye(4));img.header.set_xyzt_units('mm','sec');p=tmp_path/'raw.nii';nib.save(img,p)
    with pytest.raises(ValueError):stream_qc(p,np.zeros((3,4,5),bool))
