import numpy as np
import nibabel as nib
import pytest
from fmri_reference.core import *

def image(data=None,affine=None):
    a=np.diag([2.,3.,4.,1.]) if affine is None else affine
    im=nib.Nifti1Image(np.arange(120,dtype=float).reshape(4,5,6) if data is None else data,a);im.header.set_xyzt_units('mm','sec');return im

def test_world_reorientation_roundtrip():
    a=np.diag([-2.,3.,4.,1.]);a[0,3]=6;im=image(affine=a);out=canonical(im)
    for idx in np.ndindex(im.shape):
        world=nib.affines.apply_affine(im.affine,idx);j=np.rint(nib.affines.apply_affine(np.linalg.inv(out.affine),world)).astype(int)
        assert im.get_fdata()[idx]==out.get_fdata()[tuple(j)]

def test_resampling_world_landmark():
    im=image();o=resample_volume(im,[2,3,4],1);np.testing.assert_allclose(o.get_fdata(),im.get_fdata());np.testing.assert_allclose(o.affine,im.affine)

def test_label_nearest_no_new_classes():
    im=image((np.indices((4,5,6))[0]%2).astype(float));out=resample_volume(im,[1,2,3],0);assert set(np.unique(out.get_fdata()))<={0.,1.}

@pytest.mark.parametrize('unit',['unknown','meter','micron'])
def test_unknown_spatial_units_rejected(unit):
    im=image();im.header.set_xyzt_units(unit);pytest.raises(ValueError,geometry,im)

def test_geometry_reports_qform_disagreement():
    im=image();im.set_qform(np.eye(4),1);im.set_sform(np.diag([2.,3.,4.,1.]),1);assert geometry(im)['qform_sform_disagree']

def test_timing_units_and_duration():
    im=image(np.ones((2,2,2,10)));im.header.set_xyzt_units('mm','msec');im.header.set_zooms([2,3,4,2000]);d=timing(im,{'RepetitionTime':2});assert d['sample_span_seconds']==18 and d['nominal_duration_seconds']==20

def test_tr_conflict_rejected():
    im=image(np.ones((2,2,2,10)));im.header.set_zooms([2,3,4,2]);pytest.raises(ValueError,timing,im,{'RepetitionTime':3})

def test_irregular_timing_rejected():
    im=image(np.ones((2,2,2,10)));pytest.raises(ValueError,timing,im,{'VolumeTiming':list(range(10))})

def test_fd_units_and_first_undefined():
    p=np.zeros((3,6));p[1,0]=1;p[2,0]=1;p[2,3]=.02;f=fd_power(p);assert np.isnan(f[0]);np.testing.assert_allclose(f[1:],[1,1])

def test_dvars_analytic_and_first_undefined():
    x=np.array([[0,0],[3,4],[6,8]]);d=dvars(x);assert np.isnan(d[0]);np.testing.assert_allclose(d[1:],np.sqrt(12.5))

def test_tsnr_constant_undefined():
    assert np.isnan(tsnr(np.ones((10,1)))[0])

def test_censor_short_segment_does_not_bridge_gap():
    f=np.array([np.nan,0,0,0,1,0,0,0,0,0]);d=np.array([np.nan,0,0,0,0,0,0,0,0,0]);m=censor(f,d,.5,1,min_segment=4);assert np.flatnonzero(m).tolist()==[5,6,7,8,9]

def test_padding_mask_excludes_zeros():
    x=np.full((5,2),3.);y,k=crop_or_pad(x,9);assert k.sum()==5;assert y[k].mean()==3;assert not k[5:].any()

def test_temporal_antialias():
    t=np.arange(1000)*.5;x=np.sin(2*np.pi*.8*t)[:,None];y,tt=temporal_resample(x,.5,2.)
    assert tt[-1]<=t[-1];assert np.std(y[20:-20])<.01

def test_temporal_retains_low_frequency():
    t=np.arange(1000)*.5;x=np.sin(2*np.pi*.04*t)[:,None];y,tt=temporal_resample(x,.5,2.)
    assert np.sqrt(np.mean((y[20:-20,0]-np.sin(2*np.pi*.04*tt[20:-20]))**2))<.005

def test_joint_projection_orthogonal_with_censoring():
    rng=np.random.default_rng(7);c=rng.normal(size=(100,3));b=drift_basis(100,2);x=c@rng.normal(size=(3,2))+b@rng.normal(size=(b.shape[1],2))+rng.normal(size=(100,2));keep=np.ones(100,bool);keep[10:15]=False
    y,q=regress(x,c,keep,b);a=np.column_stack([np.ones(100),c,b]);assert np.max(np.abs(a[keep].T@y))<1e-10;assert q['original_indices'][10]==15

def test_regression_rank_dof_counts_duplicate_intercept_once():
    x=np.random.default_rng(9).normal(size=(20,2));_,q=regress(x,np.ones((20,3)));assert q['rank']==1 and q['algebraic_dof']==19

def test_insufficient_dof_rejected():
    pytest.raises(ValueError,regress,np.ones((10,2)),np.eye(10))

def test_scale_invariants():
    x=np.random.default_rng(1).normal(20,2,(100,3));z=scale(x,'zscore');np.testing.assert_allclose(z.mean(0),0,atol=1e-13);np.testing.assert_allclose(z.std(0,ddof=1),1)
    np.testing.assert_allclose(scale(x,'center').var(0,ddof=1),x.var(0,ddof=1));np.testing.assert_allclose(scale(x*5,'psc'),scale(x,'psc'),atol=1e-12)

@pytest.mark.parametrize('method',['psc','zscore','robust'])
def test_degenerate_scale_rejected(method):pytest.raises(ValueError,scale,np.zeros((10,3)),method)

def test_compcor_known_rank_subspace():
    t=np.linspace(-1,1,50);noise=np.column_stack([t,2*t,3*t,np.sin(t)]);u,ev=compcor(noise,2);np.testing.assert_allclose(u.T@u,np.eye(2),atol=1e-12);assert ev.sum()==pytest.approx(1)

def test_phase_basis_periodicity():
    p=np.arange(20)[:,None]/4;np.testing.assert_allclose(phase_regressors(p),phase_regressors(p+2*np.pi),atol=1e-13)

def test_coverage_expected_denominator():
    e=np.array([True,True,False]);o=np.array([True,False,True]);assert coverage(o,e)==.5

def test_missing_inputs_not_silent_fallback():pytest.raises(FileNotFoundError,require_inputs,['/this_file_does_not_exist.nii.gz'])

@pytest.mark.parametrize('bad',[np.array([[np.nan],[1]]),np.ones((1,3)),np.ones(10),np.zeros((10,0))])
def test_invalid_timeseries_rejected(bad):pytest.raises(ValueError,timeseries,bad)
