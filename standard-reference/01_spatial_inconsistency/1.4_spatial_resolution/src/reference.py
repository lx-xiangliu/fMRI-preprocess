"""空间分辨率差异. See README for scientific preconditions and evidence limits."""
from nilearn.image import smooth_img as apply
from fmri_reference.demo import run_demo, error_example

def demonstrate(root, session="test", variant=0, outdir=None):
    return run_demo(root, "resolution", session, variant, outdir)
