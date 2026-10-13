import json,time,sys
from pathlib import Path
import numpy as np
import nibabel as nib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fmri_reference.streaming import stream_qc
from fmri_reference.core import load_sample,dvars,tsnr
rows=[]
for session in ['test','retest']:
 s=load_sample(ROOT,session);im=s['image'];out=ROOT/'data/cache'/f'{session}_bold.nii';out.parent.mkdir(parents=True,exist_ok=True)
 # Cache is a derivative; raw input remains checksum-protected and unchanged.
 nib.save(im,out);start=time.perf_counter();r=stream_qc(out,s['mask']);elapsed=time.perf_counter()-start
 direct=s['data'][s['mask']].T.astype(float)
 dverror=float(np.nanmax(np.abs(r['dvars']-dvars(direct))));tserror=float(np.nanmax(np.abs(r['tsnr']-tsnr(direct))))
 assert dverror<1e-8 and tserror<1e-8
 row={'session':session,'n_voxels':r['n_voxels'],'n_volumes':r['n_volumes'],'raw_dvars_median':float(np.nanmedian(r['dvars'])),
      'raw_tsnr_median':float(np.nanmedian(r['tsnr'])),'dvars_vectorized_max_error':dverror,'tsnr_vectorized_max_error':tserror,
      'elapsed_seconds_uncompressed_stream':elapsed,'mask_scope':'Full estimated EPI mask, NOT verified anatomical coverage','mature_pipeline':'NOT_RUN','fd':'NOT_MEASURED'}
 rows.append(row);print(row,flush=True)
 (ROOT/'reports/full_mask_qc.json').write_text(json.dumps(rows,indent=2))
