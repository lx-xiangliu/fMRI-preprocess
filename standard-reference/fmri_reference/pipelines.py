"""Build reviewable external commands; execution and tool-specific QC are separate."""
import re
from pathlib import Path

def fmriprep_command(bids_root,output_root,work_root,image,subject,nthreads=4):
    """Pinned container command for a participant without surface reconstruction.

    image must contain an immutable digest, never a mutable latest tag. Requires
    externally installed Docker, templates, BIDS validation and appropriate QC.
    This builder has not run fMRIPrep in the delivered environment.
    """
    bids=Path(bids_root).resolve();out=Path(output_root).resolve();work=Path(work_root).resolve()
    if not (bids/'dataset_description.json').is_file():raise FileNotFoundError('BIDS dataset_description missing')
    if not re.fullmatch(r'[A-Za-z0-9]+',subject):raise ValueError('subject label must omit sub- and contain alphanumerics')
    if not re.fullmatch(r'[^\s]+@sha256:[0-9a-f]{64}',image):raise ValueError('Immutable image@sha256 digest required')
    if not isinstance(nthreads,int) or nthreads<1:raise ValueError('Positive thread count required')
    if bids==out or bids in out.parents or out in bids.parents or bids==work or bids in work.parents or work in bids.parents or out==work:
        raise ValueError('Input/output/work must be separate, nonnested roots')
    return ['docker','run','--rm','--cpus',str(nthreads),'-v',f'{bids}:/data:ro','-v',f'{out}:/out','-v',f'{work}:/work',image,
            '/data','/out','participant','--participant-label',subject,'--fs-no-reconall','--nthreads',str(nthreads),
            '--omp-nthreads',str(min(nthreads,4)),'--output-spaces','T1w','MNI152NLin2009cAsym:res-2','--work-dir','/work']
