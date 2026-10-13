# Existing project environment

Kernel: **Python (fMRI Project .venv)** (`fmri-reference`).

Interpreter: `/Users/liuxiang/fMRI-preprocess/standard-reference/.venv/bin/python`.
The environment already existed; no new Python environment is used. Notebook
metadata points to it. The kernelspec supplies the repository
root and plotting-helper path, so launch-directory differences do not break imports.

Reopen the notebook after configuration. If the editor retains an earlier kernel
selection, select **Python (fMRI Project .venv)** once and choose Run All.

This environment inherits system site packages. Unrelated torchaudio/torch and
Streamlit dependency conflicts, if reported by pip check, are logged separately;
they are not reconfigured for this notebook. The notebook is verified end to end.
