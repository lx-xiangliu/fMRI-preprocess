"""动态范围差异. See README for scientific preconditions and evidence limits."""
from fmri_reference.core import scale as apply
from fmri_reference.demo import run_demo, error_example

def demonstrate(root, session="test", variant=0, outdir=None):
    return run_demo(root, "range", session, variant, outdir)
