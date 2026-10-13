"""原始与残余伪影. See README for scientific preconditions and evidence limits."""
from fmri_reference.core import drift_basis as apply
from fmri_reference.demo import run_demo, error_example

def demonstrate(root, session="test", variant=0, outdir=None):
    return run_demo(root, "artifacts", session, variant, outdir)
