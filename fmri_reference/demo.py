"""Real-data demonstration recipes with explicit evidence boundaries."""
import json,time
from pathlib import Path
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from nilearn import image as niimg
from nilearn import signal as nisignal
from .core import *

def _summary(x):
    return {'shape':list(x.shape),'mean_abs':float(np.abs(x.mean(0)).mean()),'median_sample_std':float(np.median(x.std(0,ddof=1))),
            'q01':float(np.quantile(x,.01)),'q99':float(np.quantile(x,.99))}

def error_example(kind):
    """Rejected implementation, captured in notebooks as a deliberate negative example."""
    if kind in ['shape','motion','physio','compcor','components','coverage']:
        return require_inputs([Path('/missing_scientific_inputs')/kind])
    if kind in ['tr','sampling','duration']:return temporal_resample(np.ones((10,2)),0,2)
    if kind in ['mean','variance','amplitude','range']:return scale(np.zeros((10,2)),'psc' if kind=='amplitude' else 'zscore')
    if kind in ['points','segments']:return segments(np.ones(10,dtype=int))
    if kind in ['spacing','orientation','coordinates','resolution','registration']:
        bad=nib.Nifti1Image(np.ones((3,3,3)),np.eye(4));bad.header.set_xyzt_units('unknown');return geometry(bad)
    if kind=='drift':return drift_basis(20,2.,high_pass=.3)
    return dvars(np.array([[np.nan,0],[1,2]]))

def run_demo(root,kind,session='test',variant=0,outdir=None):
    root=Path(root);outdir=Path(outdir or root/'reports/demo');outdir.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter();s=load_sample(root,session);x=s['signals'];tr=s['timing']['tr_seconds'];t=np.arange(len(x))*tr
    y=x.copy();ta=t;labels=['Raw','Processed/diagnostic'];status='REAL_DATA_PRIMITIVE_EXECUTED';limitations=[]
    metrics={'input':str(s['path'].relative_to(root)),'session':session,'kind':kind,'tr_seconds':tr,'n_input':len(x),
             'feature_scope':'128 deterministic voxels from estimated EPI mask, not full brain','before':_summary(x),
             'production_pipeline':'NOT_RUN','scientific_best_method':'INSUFFICIENT_EVIDENCE'}
    fig=None
    if kind=='orientation':
        im=s['mean_image'];out=canonical(im);r=out.as_reoriented(nib.orientations.ornt_transform(nib.orientations.io_orientation(out.affine),nib.orientations.io_orientation(im.affine)))
        metrics.update(before_geometry=geometry(im),after_geometry=geometry(out),inverse_reorientation_max_error=float(np.max(np.abs(r.get_fdata()-im.get_fdata()))))
        fig,ax=plt.subplots(1,2,figsize=(9,4))
        for a,v,title in zip(ax,[im,out],['Native storage axes','Canonical storage axes']):a.imshow(v.get_fdata()[:,:,v.shape[2]//2].T,cmap='gray',origin='lower');a.set_title(title);a.axis('off')
    elif kind=='spacing':
        im=s['mean_image'];spacing=(4.,4.,4.) if variant==0 else (3.,3.,3.);out=resample_volume(im,spacing,order=1);nearest=resample_volume(im,spacing,order=0)
        metrics.update(before_geometry=geometry(im),after_geometry=geometry(out),linear_nearest_mae=float(np.mean(np.abs(out.get_fdata()-nearest.get_fdata()))),requested_spacing_mm=list(spacing),anti_alias_proof='NOT_ESTABLISHED')
        fig,ax=plt.subplots(1,3,figsize=(12,4))
        for a,v,title in zip(ax,[im,out,nearest],['Native','Linear','Nearest (labels only)']):a.imshow(v.get_fdata()[:,:,v.shape[2]//2].T,cmap='gray',origin='lower');a.set_title(title);a.axis('off')
    elif kind=='resolution':
        im=s['mean_image'];out=niimg.smooth_img(im,4. if variant==0 else 2.)
        metrics.update(applied_fwhm_mm=4. if variant==0 else 2.,before_spatial_std=float(im.get_fdata().std()),after_spatial_std=float(out.get_fdata().std()),effective_psf='NOT_MEASURED')
        fig,ax=plt.subplots(1,2,figsize=(9,4))
        for a,v,title in zip(ax,[im,out],['Unsmoothed','Gaussian smooth']):a.imshow(v.get_fdata()[:,:,v.shape[2]//2].T,cmap='gray',origin='lower');a.set_title(title);a.axis('off')
    elif kind=='coordinates':
        ijk=np.array([[0,0,0],(np.array(s['image'].shape[:3])-1)/2.]);ras=nib.affines.apply_affine(s['image'].affine,ijk);back=nib.affines.apply_affine(np.linalg.inv(s['image'].affine),ras);lps=ras*np.array([-1,-1,1])
        metrics.update(voxel_indices=ijk.tolist(),ras_mm=ras.tolist(),lps_mm=lps.tolist(),roundtrip_error=float(np.max(np.abs(back-ijk))),geometry=s['geometry'])
        fig,ax=plt.subplots(figsize=(8,4));ax.plot(ras.T,'o-',label='RAS');ax.plot(lps.T,'x--',label='LPS');ax.set_xticks([0,1,2],['x','y','z']);ax.set_ylabel('mm');ax.legend()
    elif kind=='shape':
        anat=root/'data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_T1w.nii.gz';a=nib.load(anat)
        metrics.update(bold_geometry=s['geometry'],t1_geometry=geometry(a),nonlinear_normalization='NOT_RUN',anatomical_correspondence='NOT_MEASURED')
        status='REAL_DATA_INPUT_AUDIT_ONLY';limitations.append('No template/skull stripping/nonlinear warp: geometry comparison is not anatomical normalization.')
        fig,ax=plt.subplots(1,2,figsize=(9,4))
        for z,v,title in zip(ax,[s['mean_image'],a],['BOLD native','T1w native, different grid']):z.imshow(v.get_fdata()[:,:,v.shape[2]//2].T,cmap='gray',origin='lower');z.set_title(title);z.axis('off')
    elif kind in ['tr','sampling']:
        outtr=5. if kind=='sampling' else (3. if variant==0 else 2.)
        y,ta=temporal_resample(x,tr,outtr)
        metrics.update(tr_out_seconds=outtr,n_output=len(y),output_span_seconds=float(ta[-1]),nyquist_before_hz=.5/tr,nyquist_after_hz=.5/outtr)
        # Naive point selection is an explicitly bad comparison for downsampling.
        if kind=='sampling':metrics['naive_decimation_rmse_vs_antialias']=float(np.sqrt(np.mean((x[::2][:len(y)]-y)**2)))
    elif kind=='points':
        length=200 if variant==0 else 128;y,valid=crop_or_pad(x,length);ta=np.arange(len(y))*tr
        metrics.update(n_output=len(y),n_real=int(valid.sum()),padding_count=int((~valid).sum()),valid_mask=valid.tolist(),after_valid_only=_summary(y[valid]))
        labels[1]='Crop/pad, padding masked';limitations.append('All training statistics/attention/loss must use validity mask.')
    elif kind=='duration':
        seconds=120 if variant==0 else 180;keep=t<seconds;y=x[keep];ta=t[keep]
        metrics.update(clock=s['timing'],window_seconds=seconds,window_sample_span_seconds=float(ta[-1]-ta[0]),n_output=len(y))
    elif kind=='motion':
        metrics.update(fd='NOT_MEASURED',motion_parameters='MISSING',raw_dvars_median=float(np.nanmedian(dvars(x))))
        status='REAL_DATA_DIAGNOSTIC_ONLY';limitations.append('No MCFLIRT/3dvolreg output: no measured FD, no motion exclusion decision.')
        fig,ax=plt.subplots(2,1,figsize=(9,5),sharex=True);ax[0].plot(t,x.mean(1));ax[0].set_ylabel('Raw mean');ax[1].plot(t,dvars(x));ax[1].set_ylabel('Raw DVARS (not FD)');ax[1].set_xlabel('Original time (s)')
    elif kind=='dvars':
        dv=dvars(x);normalized=scale(x,'zscore');dvn=dvars(normalized)
        metrics.update(raw_dvars_median=float(np.nanmedian(dv)),zscored_signal_dvars_median=float(np.nanmedian(dvn)),standardized_dvars='NOT_MEASURED',first_volume='UNDEFINED')
        fig,ax=plt.subplots(2,1,figsize=(9,5),sharex=True);ax[0].plot(t,dv);ax[0].set_ylabel('Raw intensity DVARS');ax[1].plot(t,dvn);ax[1].set_ylabel('DVARS of z-score\nNOT standardized DVARS');ax[1].set_xlabel('Original time (s)')
    elif kind=='segments':
        keep=np.ones(len(x),bool);keep[20:24]=False;keep[27:30]=False;retained=np.zeros(len(x),bool)
        for a,b in segments(keep,5):retained[a:b]=True
        y=x[retained];ta=t[retained];metrics.update(segment_bounds_original=segments(retained,5),injected_gaps=[20,21,22,23,27,28,29],injection_label='CONTROLLED_ERROR_EXAMPLE_NOT_REAL_QC',nonsteady_labels='NOT_AVAILABLE',original_indices=np.flatnonzero(retained).tolist())
        limitations.append('Gap injection illustrates segmentation; it is not evidence that these real volumes are bad.')
    elif kind in ['artifacts','drift']:
        b=drift_basis(len(x),tr,.008);y,q=regress(x,drift=b);metrics.update(regression=q,high_pass_hz=.008,design_residual_max_abs=float(np.max(np.abs(b.T@y))))
        if kind=='drift':
            other=nisignal.clean(x,detrend=True,standardize=False,low_pass=None,high_pass=.008,t_r=tr)
            metrics.update(nilearn_butterworth_std=float(np.median(other.std(0,ddof=1))),dct_butterworth_rmse=float(np.sqrt(np.mean((y-other)**2))),method_comparison='Different filters; neither established scientifically superior')
        else:
            fig,ax=plt.subplots(2,1,figsize=(10,5),sharex=True);ax[0].imshow(scale(x,'zscore').T,aspect='auto',extent=[t[0],t[-1],0,x.shape[1]],cmap='RdBu_r',vmin=-3,vmax=3);ax[0].set_title('Raw carpet, scale for display only');ax[1].imshow(scale(y,'zscore').T,aspect='auto',extent=[t[0],t[-1],0,x.shape[1]],cmap='RdBu_r',vmin=-3,vmax=3);ax[1].set_title('DCT residual, not fully artifact corrected');ax[1].set_xlabel('Time (s)')
        limitations.append('DCT removal is not susceptibility correction or proof of neural signal preservation.')
    elif kind=='coverage':
        v=tsnr(x);metrics.update(raw_tsnr_median=float(np.nanmedian(v)),raw_tsnr_q10=float(np.nanquantile(v,.1)),brain_coverage='NOT_MEASURED',mask_scope='Estimated EPI mask does not provide expected anatomical brain coverage')
        fig,ax=plt.subplots(1,2,figsize=(9,4));ax[0].hist(v[np.isfinite(v)],bins=30);ax[0].set_xlabel('Raw tSNR, 128 voxels');ax[1].imshow(s['mask'][:,:,s['mask'].shape[2]//2].T,origin='lower',cmap='gray');ax[1].set_title('Estimated EPI mask');ax[1].axis('off')
    elif kind=='registration':
        from .registration import rigid
        import SimpleITK as sitk
        sitk.ProcessObject.SetGlobalDefaultNumberOfThreads(1)
        anat=nib.load(root/'data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_T1w.nii.gz')
        f=resample_volume(anat,(4,4,4));m=resample_volume(s['mean_image'],(4,4,4));fp=outdir/'fixed_4mm.nii.gz';mp=outdir/'moving_4mm.nii.gz';op=outdir/'rigid_bold_to_t1.nii.gz';nib.save(f,fp);nib.save(m,mp)
        report=rigid(fp,mp,op,'mi');metrics.update(registration=report,scan_exclusion='REVIEW_REQUIRED')
        warped=nib.load(op);unregistered=resample_from_to(m,f,order=1)
        fig,ax=plt.subplots(1,3,figsize=(12,4));z=f.shape[2]//2
        for aa,bb,title in zip(ax,[None,unregistered,warped],['T1w','Header resampling only','Rigid MI overlay']):
            aa.imshow(f.get_fdata()[:,:,z].T,cmap='gray',origin='lower')
            if bb is not None:aa.imshow(bb.get_fdata()[:,:,z].T,cmap='hot',alpha=.45,origin='lower')
            aa.set_title(title);aa.axis('off')
        limitations.append('No brain extraction/BBR/SDC. Objective change cannot authorize scan inclusion.')
    elif kind in ['physio','compcor','components']:
        b=drift_basis(len(x),tr,.008);noise,_=regress(x,drift=b);pc,ev=compcor(noise,5)
        metrics.update(pca_explained_variance_ratio=ev.tolist(),pca_scope='Illustrative BRAIN signals, NOT validated noise ROI',neural_noise_labels='NOT_AVAILABLE',denoising='NOT_RUN')
        status='REAL_DATA_DECOMPOSITION_ONLY'
        if kind=='physio':metrics.update(physiological_recordings='MISSING',retroicor='NOT_RUN')
        if kind=='compcor':metrics.update(wm_csf_mask='MISSING',acompcor='NOT_RUN')
        if kind=='components':metrics.update(single_echo=True,tedana='NOT_APPLICABLE_TO_PRIMARY_DATA',ica_aroma='NOT_RUN')
        fig,ax=plt.subplots(1,2,figsize=(10,4));ax[0].plot(t,pc);ax[0].set_title('PCA: no noise labels, no removal');ax[0].set_xlabel('Time (s)');ax[1].bar(np.arange(1,6),ev);ax[1].set_title('Variance fraction (not efficacy)')
        limitations.append('Required scientific inputs absent; no component was removed. See supplemental dataset manifest.')
    elif kind=='mean':
        y=scale(x,'center');metrics.update(center_mean_max_abs=float(np.max(np.abs(y.mean(0)))),variance_preserved_max_error=float(np.max(np.abs(y.var(0,ddof=1)-x.var(0,ddof=1)))))
    elif kind=='variance':
        y=scale(x,'zscore');other=nisignal.clean(x,detrend=False,standardize='zscore_sample',filter=False)
        metrics.update(nilearn_max_abs_error=float(np.max(np.abs(y-other))),output_mean_max_abs=float(np.max(np.abs(y.mean(0)))),output_std_max_error=float(np.max(np.abs(y.std(0,ddof=1)-1))))
    elif kind=='amplitude':
        y=scale(x,'psc');other=nisignal.clean(x,detrend=False,standardize='psc',filter=False)
        metrics.update(nilearn_max_abs_error=float(np.max(np.abs(y-other))),unit='percent_of_original_mean',zscore_median_std=float(np.median(scale(x,'zscore').std(0,ddof=1))))
    elif kind=='range':
        y=scale(x,'robust');z=scale(x,'zscore');metrics.update(robust_q01=float(np.quantile(y,.01)),robust_q99=float(np.quantile(y,.99)),zscore_q01=float(np.quantile(z,.01)),zscore_q99=float(np.quantile(z,.99)),clipping_applied=False)
    else:raise ValueError('Unknown category recipe')
    metrics['after']=_summary(y);metrics['evidence_status']=status;metrics['limitations']=limitations
    if fig is None:
        fig,ax=plt.subplots(2,1,figsize=(9,5));ax[0].plot(t,x[:,0]);ax[0].set_title(labels[0]);ax[0].set_xlabel('Original time (s)');ax[1].plot(ta,y[:,0]);ax[1].set_title(labels[1]);ax[1].set_xlabel('Physical time (s)')
        if kind=='segments':ax[1].clear();ax[1].scatter(ta,y[:,0],s=8);ax[1].set_title('Retained points on ORIGINAL time axis');ax[1].set_xlabel('Time (s)')
        if kind=='points' and metrics['padding_count']:
            ax[1].axvspan(metrics['n_real']*tr,ta[-1],alpha=.15,color='red',label='Padding: invalid');ax[1].legend()
    fig.suptitle(f'{kind} | sub-01 ses-{session} | {status}',fontsize=10);fig.tight_layout();fig.savefig(outdir/'comparison.png',dpi=130)
    metrics['elapsed_seconds']=time.perf_counter()-start
    (outdir/'metrics.json').write_text(json.dumps(metrics,indent=2,allow_nan=False))
    return metrics,fig
