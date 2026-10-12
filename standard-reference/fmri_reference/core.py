"""Small, explicit reference primitives; array convention is time x features."""
from fractions import Fraction
import json
from pathlib import Path
import numpy as np
import nibabel as nib
from scipy import signal
from nibabel.processing import resample_to_output, resample_from_to

def timeseries(x):
    x=np.asarray(x,dtype=np.float64)
    if x.ndim!=2 or x.shape[0]<2 or x.shape[1]<1 or not np.isfinite(x).all():
        raise ValueError('Expected finite time x features array with >=2 samples')
    return x

def geometry(img):
    a=np.asarray(img.affine)
    if a.shape!=(4,4) or not np.isfinite(a).all() or abs(np.linalg.det(a[:3,:3]))<1e-10:
        raise ValueError('Missing, singular or nonfinite affine')
    if img.header.get_xyzt_units()[0]!='mm':
        raise ValueError('Spatial units must explicitly be mm')
    q,qcode=img.get_qform(coded=True);s,scode=img.get_sform(coded=True)
    return {'shape':list(img.shape),'orientation':list(nib.aff2axcodes(a)),
            'spacing_mm':nib.affines.voxel_sizes(a).tolist(),
            'qform_code':int(qcode),'sform_code':int(scode),
            'qform_sform_disagree':bool(qcode and scode and not np.allclose(q,s,atol=1e-3)),
            'affine_ras_mm':a.tolist()}

def timing(img,metadata):
    if len(img.shape)!=4:raise ValueError('BOLD must be 4D')
    if 'VolumeTiming' in metadata:raise ValueError('Variable TR needs an explicit irregular-time workflow')
    tr=float(metadata['RepetitionTime'])
    if not np.isfinite(tr) or tr<=0:raise ValueError('TR must be positive seconds')
    unit=img.header.get_xyzt_units()[1]
    factor={'sec':1,'msec':1e-3,'usec':1e-6}.get(unit)
    if factor is None:raise ValueError('Unknown NIfTI time unit')
    if not np.isclose(img.header.get_zooms()[3]*factor,tr,rtol=1e-4):raise ValueError('JSON/header TR conflict')
    n=img.shape[3]
    return {'tr_seconds':tr,'sampling_hz':1/tr,'nyquist_hz':.5/tr,'n_volumes':n,
            'sample_span_seconds':(n-1)*tr,'nominal_duration_seconds':n*tr,
            'onsets_seconds':(np.arange(n)*tr).tolist()}

def canonical(img):
    geometry(img)
    return nib.as_closest_canonical(img)

def resample_volume(img,spacing,order=1):
    geometry(img)
    spacing=np.asarray(spacing,dtype=float)
    if len(img.shape)!=3 or spacing.shape!=(3,) or not np.isfinite(spacing).all() or (spacing<=0).any():
        raise ValueError('Expected 3D volume and positive three-axis spacing')
    if order not in (0,1,3):raise ValueError('Use nearest for labels, linear/cubic for continuous images')
    # Grid resampling changes sampling spacing, not the acquired point-spread function.
    out=resample_to_output(img,voxel_sizes=spacing,order=order)
    out.header.set_xyzt_units('mm')
    return out

def fd_power(parameters,radius_mm=50.):
    """Columns: tx,ty,tz in mm, rx,ry,rz in radians, same rotation convention."""
    p=np.asarray(parameters,dtype=float)
    if p.ndim!=2 or p.shape[1]!=6 or p.shape[0]<2 or not np.isfinite(p).all() or not np.isfinite(radius_mm) or radius_mm<=0:
        raise ValueError('Expected finite Nx6 parameters and positive head radius')
    delta=np.abs(np.diff(p,axis=0))
    # First FD is undefined, never a measured zero.
    return np.r_[np.nan,delta[:,:3].sum(1)+radius_mm*delta[:,3:].sum(1)]

def dvars(x):
    x=timeseries(x)
    return np.r_[np.nan,np.sqrt(np.mean(np.diff(x,axis=0)**2,axis=1))]

def tsnr(x):
    x=timeseries(x);sd=x.std(axis=0,ddof=1)
    return np.divide(x.mean(0),sd,out=np.full_like(sd,np.nan),where=sd>np.finfo(float).eps)

def segments(keep,min_length=1):
    keep=np.asarray(keep)
    if keep.ndim!=1 or keep.dtype!=bool or min_length<1:raise ValueError('Boolean mask and positive length required')
    changes=np.diff(np.r_[False,keep,False].astype(int));starts=np.flatnonzero(changes==1);ends=np.flatnonzero(changes==-1)
    return [(int(a),int(b)) for a,b in zip(starts,ends) if b-a>=min_length]

def censor(fd,dv,fd_limit,dvars_limit,min_segment=5):
    f=np.asarray(fd,float);d=np.asarray(dv,float)
    if f.ndim!=1 or f.shape!=d.shape or fd_limit<=0 or dvars_limit<=0:raise ValueError('Invalid QC thresholds/shapes')
    # Undefined first derivatives are conservatively censored. Raw DVARS is in intensity units.
    keep=np.isfinite(f)&np.isfinite(d)&(f<=fd_limit)&(d<=dvars_limit)
    result=np.zeros_like(keep)
    for a,b in segments(keep,min_segment):result[a:b]=True
    return result

def crop_or_pad(x,length):
    x=timeseries(x)
    if not isinstance(length,int) or length<2:raise ValueError('Positive window >=2')
    out=np.zeros((length,x.shape[1]));valid=np.zeros(length,dtype=bool);n=min(length,len(x));out[:n]=x[:n];valid[:n]=True
    return out,valid

def temporal_resample(x,tr_in,tr_out):
    x=timeseries(x)
    if not np.isfinite([tr_in,tr_out]).all() or min(tr_in,tr_out)<=0:raise ValueError('TR must be positive')
    ratio=Fraction(float(tr_in)/float(tr_out)).limit_denominator(1000)
    if not np.isclose(float(ratio),tr_in/tr_out,rtol=1e-6):raise ValueError('TR ratio approximation inaccurate')
    y=signal.resample_poly(x,ratio.numerator,ratio.denominator,axis=0,padtype='line')
    t=np.arange(len(y))*tr_out
    # Restrict to source sample support; no invented tail beyond final acquired onset.
    take=t<=(len(x)-1)*tr_in+1e-8
    return y[take],t[take]

def drift_basis(n,tr,high_pass=.008):
    if n<3 or not np.isfinite([tr,high_pass]).all() or tr<=0 or not 0<high_pass<.5/tr:raise ValueError('Invalid high-pass/Nyquist')
    # DCT-II cosine drift + intercept, following SPM/Nilearn convention.
    order=min(int(np.floor(2*n*tr*high_pass)),n-2)
    t=np.arange(n)+.5
    return np.column_stack([np.ones(n)]+[np.cos(np.pi*k*t/n) for k in range(1,order+1)])

def regress(x,confounds=None,keep=None,drift=None,min_dof=5):
    x=timeseries(x);n=len(x)
    keep=np.ones(n,bool) if keep is None else np.asarray(keep)
    if keep.shape!=(n,) or keep.dtype!=bool:raise ValueError('keep must be boolean original-time mask')
    columns=[np.ones((n,1))]
    for c in [confounds,drift]:
        if c is not None:
            c=np.asarray(c,float)
            if c.ndim!=2 or len(c)!=n or not np.isfinite(c).all():raise ValueError('Finite confounds must match original time axis')
            columns.append(c)
    design=np.column_stack(columns);rank=int(np.linalg.matrix_rank(design[keep])) if keep.any() else 0
    dof=int(keep.sum())-rank
    if dof<min_dof:raise ValueError('Too few residual algebraic degrees of freedom')
    beta=np.linalg.lstsq(design[keep],x[keep],rcond=None)[0]
    residual=x[keep]-design[keep]@beta
    return residual,{'rank':rank,'retained':int(keep.sum()),'algebraic_dof':dof,'original_indices':np.flatnonzero(keep).tolist()}

def scale(x,method='zscore'):
    x=timeseries(x);mu=x.mean(0);sd=x.std(0,ddof=1)
    if method=='center':return x-mu
    if method=='zscore':
        if (sd<=1e-12).any():raise ValueError('Constant features require explicit exclusion')
        return (x-mu)/sd
    if method=='psc':
        if (np.abs(mu)<=1e-8).any():raise ValueError('PSC requires nonzero pre-regression baseline')
        return 100*(x-mu)/np.abs(mu)
    if method=='robust':
        med=np.median(x,axis=0);mad=1.4826*np.median(np.abs(x-med),axis=0)
        if (mad<=1e-12).any():raise ValueError('Degenerate robust scale')
        return (x-med)/mad
    raise ValueError('Unknown scale method')

def compcor(noise,n_components=5):
    noise=timeseries(noise)
    if not 1<=n_components<min(noise.shape):raise ValueError('Invalid component count')
    # Noise must already be restricted to verified eroded tissue masks and high-pass filtered.
    sd=noise.std(0,ddof=1)
    if (sd<=1e-12).any():raise ValueError('Constant noise features')
    u,s,_=np.linalg.svd((noise-noise.mean(0))/sd,full_matrices=False)
    return u[:,:n_components],(s[:n_components]**2/np.sum(s**2))

def phase_regressors(phases,order=2):
    phases=np.asarray(phases,float)
    if phases.ndim!=2 or not np.isfinite(phases).all() or not isinstance(order,int) or order<1:raise ValueError('Valid synchronized phases required')
    return np.column_stack([f(k*phases[:,j]) for j in range(phases.shape[1]) for k in range(1,order+1) for f in [np.sin,np.cos]])

def coverage(observed,expected):
    o=np.asarray(observed);e=np.asarray(expected)
    if o.shape!=e.shape or o.dtype!=bool or e.dtype!=bool or not e.any():raise ValueError('Nonempty expected boolean mask in same verified world grid required')
    return float((o&e).sum()/e.sum())

def require_inputs(paths):
    missing=[str(p) for p in paths if not Path(p).is_file()]
    if missing:raise FileNotFoundError('Required scientific inputs absent: '+', '.join(missing))

def load_sample(root,session='test',max_features=128):
    root=Path(root);base=root/'data/ds000114'
    path=base/f'sub-01/ses-{session}/func/sub-01_ses-{session}_task-fingerfootlips_bold.nii.gz'
    require_inputs([path,base/'task-fingerfootlips_bold.json'])
    img=nib.load(path);meta=json.loads((base/'task-fingerfootlips_bold.json').read_text());geo=geometry(img);clock=timing(img,meta)
    data=img.get_fdata(dtype=np.float32)
    mean=nib.Nifti1Image(data.mean(-1),img.affine,img.header);mean.header.set_xyzt_units('mm','sec')
    from nilearn.masking import compute_epi_mask
    mask=compute_epi_mask(mean).get_fdata().astype(bool)
    flat=np.flatnonzero(mask.ravel())
    if len(flat)<max_features:raise ValueError('Insufficient EPI mask voxels')
    selected=flat[np.linspace(0,len(flat)-1,max_features,dtype=int)]
    x=data.reshape(-1,data.shape[-1])[selected].T.astype(float)
    return {'image':img,'mean_image':mean,'data':data,'mask':mask,'signals':x,'selected_flat_indices':selected,'metadata':meta,'geometry':geo,'timing':clock,'path':path}
