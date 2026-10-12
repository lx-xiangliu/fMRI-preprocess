"""Reusable, dependency-light helpers for Raw/Residual Artifacts.

Functions accept NumPy arrays or NiBabel images. Optional dependencies are imported
inside the function so metadata/QC utilities remain usable in minimal environments.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Mapping

def _np():
    import numpy as np
    return np

def robust_outlier_mask(data: Any, **kwargs):
    """Flag voxelwise or volume-wise robust outliers.

    Parameters are deliberately explicit in the source and documented in README.md.
    """
    np = _np()
    if 'robust_outlier_mask' == 'compare_shape':
        shape = tuple(data.shape) if hasattr(data, 'shape') else tuple(np.asarray(data).shape)
        reference = kwargs.get('reference_shape')
        return {'shape': shape, 'matches': reference is None or shape == tuple(reference)}
    if 'robust_outlier_mask' == 'canonicalize_orientation':
        import nibabel as nib
        return nib.as_closest_canonical(data)
    if 'robust_outlier_mask' == 'voxel_spacing':
        if hasattr(data, 'header'): return tuple(float(x) for x in data.header.get_zooms()[:3])
        return tuple(float(x) for x in kwargs['affine'][:3,:3].diagonal())
    if 'robust_outlier_mask' == 'resolution_report':
        aff = data.affine if hasattr(data, 'affine') else np.asarray(kwargs['affine'])
        shape = tuple(data.shape[:3]) if hasattr(data, 'shape') else tuple(np.asarray(data).shape[:3])
        zooms = np.sqrt((aff[:3,:3] ** 2).sum(axis=0))
        return {'shape': shape, 'voxel_sizes_mm': zooms.tolist(), 'fov_mm': (zooms*np.asarray(shape)).tolist()}
    if 'robust_outlier_mask' == 'coordinate_report':
        aff = np.asarray(data.affine if hasattr(data, 'affine') else data)
        ref = kwargs.get('reference_affine')
        return {'affine': aff.tolist(), 'matches': ref is None or np.allclose(aff, ref, atol=kwargs.get('atol',1e-3))}
    if 'robust_outlier_mask' == 'validate_tr':
        tr = data.get('RepetitionTime') if isinstance(data, Mapping) else float(data)
        tr = float(tr)
        if tr <= 0: raise ValueError('RepetitionTime must be positive seconds')
        expected = kwargs.get('expected')
        return {'tr_seconds': tr, 'matches': expected is None or abs(tr-float(expected)) <= kwargs.get('tol',1e-4)}
    if 'robust_outlier_mask' == 'resample_time_series':
        x = np.asarray(data, dtype=float); old = float(kwargs['old_tr']); new = float(kwargs['new_tr'])
        if x.ndim != 1: raise ValueError('data must be one-dimensional for this helper')
        t_old=np.arange(x.size)*old; n=max(1,int(round(t_old[-1]/new))+1)
        return np.interp(np.arange(n)*new,t_old,x)
    if 'robust_outlier_mask' == 'match_timepoints':
        x=np.asarray(data); n=int(kwargs['n_timepoints'])
        if n < 1: raise ValueError('n_timepoints must be positive')
        if x.shape[-1] >= n: return x[..., :n]
        pad=np.repeat(x[..., -1:], n-x.shape[-1], axis=-1); return np.concatenate([x,pad],axis=-1)
    if 'robust_outlier_mask' == 'duration_seconds':
        n = int(kwargs.get('n_timepoints', data)); tr=float(kwargs['tr']);
        if n < 1 or tr <= 0: raise ValueError('n_timepoints and tr must be positive')
        return n*tr
    if 'robust_outlier_mask' == 'framewise_displacement':
        m=np.asarray(data,dtype=float);
        if m.ndim != 2 or m.shape[1] not in (6,12): raise ValueError('motion must be (time,6) or (time,12)')
        radius=float(kwargs.get('head_radius_mm',50.0)); d=np.vstack([np.zeros((1,m.shape[1])),np.diff(m,axis=0)]);
        if m.shape[1]>=6: d[:,3:6] *= radius
        return np.abs(d[:,:6]).sum(axis=1)
    if 'robust_outlier_mask' == 'dvars':
        x=np.asarray(data,dtype=float);
        if x.ndim < 2: raise ValueError('data must have time as the last axis')
        d=np.diff(x,axis=-1); return np.sqrt(np.mean(d*d,axis=tuple(range(x.ndim-1))))
    if 'robust_outlier_mask' == 'detect_nonsteady_state':
        x=np.asarray(data,dtype=float); means=x.reshape((-1,x.shape[-1])).mean(axis=0); delta=np.r_[0,np.abs(np.diff(means))]; med=np.median(delta); mad=np.median(np.abs(delta-med))+1e-12; return np.flatnonzero((delta-med)/mad > kwargs.get('threshold',6.0)).tolist()
    if 'robust_outlier_mask' == 'robust_outlier_mask':
        x=np.asarray(data,dtype=float); med=np.nanmedian(x); mad=np.nanmedian(np.abs(x-med))+1e-12; return np.abs(x-med)/(1.4826*mad) > kwargs.get('z',5.0)
    if 'robust_outlier_mask' == 'coverage_and_tsnr':
        x=np.asarray(data,dtype=float); brain=np.nanmean(x,axis=-1)>kwargs.get('background',0); coverage=float(brain.mean()); mu=np.nanmean(x,axis=-1); sd=np.nanstd(x,axis=-1,ddof=1); tsnr=np.divide(mu,sd,out=np.zeros_like(mu),where=sd>0); return {'coverage':coverage,'median_tsnr':float(np.nanmedian(tsnr[brain])) if np.any(brain) else 0.0}
    if 'robust_outlier_mask' == 'affine_registration_qc':
        a=np.asarray(data,dtype=float); ref=np.asarray(kwargs['reference_affine'],dtype=float); return {'finite':bool(np.isfinite(a).all()),'determinant':float(np.linalg.det(a[:3,:3])),'max_affine_error':float(np.max(np.abs(a-ref)))}
    if 'robust_outlier_mask' == 'physiological_regressors':
        t=np.asarray(data,dtype=float); order=int(kwargs.get('order',2)); cols=[np.ones(t.size)];
        for k in range(1,order+1): cols += [np.sin(2*np.pi*k*t/kwargs['period']), np.cos(2*np.pi*k*t/kwargs['period'])]
        return np.column_stack(cols)
    if 'robust_outlier_mask' == 'scanner_drift':
        x=np.asarray(data,dtype=float); t=np.linspace(-1,1,x.size); return np.polyfit(t,x,kwargs.get('order',1))
    if 'robust_outlier_mask' == 'confound_summary':
        x=np.asarray(data,dtype=float); return {'n_timepoints':int(x.shape[0]),'mean':float(np.nanmean(x)),'std':float(np.nanstd(x,ddof=1))}
    if 'robust_outlier_mask' == 'non_neural_components':
        x=np.asarray(data,dtype=float); u,s,v=np.linalg.svd(x-x.mean(0),full_matrices=False); return {'singular_values':s.tolist(),'variance_explained':(s*s/np.sum(s*s)).tolist()}
    if 'robust_outlier_mask' == 'mean_scale': return float(np.nanmean(np.asarray(data,dtype=float)))
    if 'robust_outlier_mask' == 'variance_scale': return float(np.nanvar(np.asarray(data,dtype=float),ddof=1))
    if 'robust_outlier_mask' == 'percent_signal_change':
        x=np.asarray(data,dtype=float); baseline=np.nanmean(x,axis=-1,keepdims=True); return np.divide((x-baseline)*100,baseline,out=np.zeros_like(x),where=baseline!=0)
    if 'robust_outlier_mask' == 'dynamic_range':
        x=np.asarray(data,dtype=float); lo,hi=np.nanpercentile(x,[2,98]); return {'p02':float(lo),'p98':float(hi),'robust_range':float(hi-lo)}
    raise RuntimeError('unreachable')
