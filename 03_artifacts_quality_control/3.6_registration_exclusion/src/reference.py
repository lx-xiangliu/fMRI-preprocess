"""配准失败与剔除. See README for scientific preconditions and evidence limits."""
from fmri_reference.registration import rigid as apply
from fmri_reference.demo import run_demo, error_example

def demonstrate(root, session="test", variant=0, outdir=None):
    return run_demo(root, "registration", session, variant, outdir)
