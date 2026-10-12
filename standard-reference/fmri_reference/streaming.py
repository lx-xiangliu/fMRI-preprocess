"""Bounded-memory full-mask QC for uncompressed or indexed NIfTI input."""
import numpy as np
import nibabel as nib
from .core import geometry

def stream_qc(image_path,mask,min_sd=1e-12):
    """Returns original-intensity DVARS and ddof=1 tSNR without loading 4D data.

    Use uncompressed .nii for predictable mmap behavior. gzip needs indexed_gzip
    for efficient random access; this function makes no claimed runtime advantage.
    Mask must already be independently checked in the image's world grid.
    """
    img=nib.load(str(image_path),mmap=True,keep_file_open=True);geometry(img)
    mask=np.asarray(mask)
    if len(img.shape)!=4 or mask.shape!=img.shape[:3] or mask.dtype!=bool or not mask.any() or img.shape[3]<2:
        raise ValueError('4D image and nonempty matching boolean mask required')
    mean=np.zeros(mask.sum(),float);m2=mean.copy();previous=None;dv=np.full(img.shape[3],np.nan)
    for t in range(img.shape[3]):
        values=np.asarray(img.dataobj[...,t],dtype=np.float64)[mask]
        if not np.isfinite(values).all():raise ValueError(f'Nonfinite input at volume {t}')
        delta=values-mean;mean+=delta/(t+1);m2+=delta*(values-mean)
        if previous is not None:dv[t]=np.sqrt(np.mean((values-previous)**2))
        previous=values
    sd=np.sqrt(m2/(img.shape[3]-1));ts=np.divide(mean,sd,out=np.full_like(mean,np.nan),where=sd>min_sd)
    return {'dvars':dv,'tsnr':ts,'temporal_mean':mean,'sample_std':sd,'n_voxels':int(mask.sum()),'n_volumes':img.shape[3]}
