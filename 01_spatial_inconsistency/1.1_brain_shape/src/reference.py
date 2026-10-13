"""脑形态差异. See README for scientific preconditions and evidence limits."""
from fmri_reference.pipelines import fmriprep_command as apply
from fmri_reference.demo import run_demo, error_example

def demonstrate(root, session="test", variant=0, outdir=None):
    return run_demo(root, "shape", session, variant, outdir)
