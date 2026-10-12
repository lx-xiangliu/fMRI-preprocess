# References and provenance

The repository uses citable, maintained specifications and tools. URLs are canonical project URLs; release versions are recorded where the upstream project publishes them. A commit hash is only recorded when this repository has fetched it; no unverified hash is invented.

- Gorgolewski et al. (2016), *The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments*, Scientific Data, DOI: 10.1038/sdata.2016.44. BIDS specification: https://bids-specification.readthedocs.io/
- Esteban et al. (2019), *fMRIPrep: a robust preprocessing pipeline for functional MRI*, Nature Methods, DOI: 10.1038/s41592-018-0235-4. Official repository: https://github.com/nipreps/fmriprep (release tags are preferred; pin a commit in production).
- Abraham et al. (2014), *Machine learning for neuroimaging with scikit-learn*, Frontiers in Neuroinformatics, DOI: 10.3389/fninf.2014.00014. Nilearn: https://github.com/nilearn/nilearn
- The NiBabel developers, NiBabel documentation: https://nipy.org/nibabel/ ; repository: https://github.com/nipy/nibabel
- Jenkinson et al. (2012), *FSL*, NeuroImage, DOI: 10.1016/j.neuroimage.2011.10.026. Official repository: https://git.fmrib.ox.ac.uk/fsl/fsl
- Cox (1996), AFNI, *Computers and Biomedical Research*; official repository: https://github.com/afni/afni
- Esteban et al. (2017), *MRIQC: advancing the automatic prediction of image quality in MRI*, PLOS ONE, DOI: 10.1371/journal.pone.0184661. Repository: https://github.com/nipreps/mriqc
- Power et al. (2012), *Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion*, NeuroImage, DOI: 10.1016/j.neuroimage.2011.10.052.
- Ciric et al. (2017), *Benchmarking confound regression strategies for the control of motion artifact in resting-state fMRI*, NeuroImage, DOI: 10.1016/j.neuroimage.2016.12.023.
- Behzadi et al. (2007), *A component based noise correction method (CompCor) for BOLD and perfusion based fMRI*, NeuroImage, DOI: 10.1016/j.neuroimage.2007.04.042.
- DuPre et al. (2021), *tedana: A Python package for multi-echo independent component analysis*, Journal of Open Source Software, DOI: 10.21105/joss.02739. Repository: https://github.com/ME-ICA/tedana
- Poldrack et al. (2013), *Toward open sharing of task-based fMRI data: the OpenfMRI project*, Frontiers in Neuroinformatics, DOI: 10.3389/fninf.2013.00012. OpenNeuro: https://openneuro.org/

## Evidence status

The small functions in `src/` are auditable implementations of the stated equations and API contracts. Tests exercise deterministic array cases. Dataset notebooks require a local BIDS download and are not claimed to have been run until their output is saved under `results/`.

## 本小类映射

推荐先阅读 BIDS、NiBabel 和 fMRIPrep 的相关章节，再根据数据条件选择本函数 `resolution_report`。该函数不替代完整 fMRIPrep/FSL/AFNI 工作流。

## Verified upstream source snapshots (queried 2026-10-12)

These hashes are the upstream `HEAD` values returned by `git ls-remote` on the query date, not historical release pins. Pin a tagged release or vendor a commit before production use.

- fMRIPrep: `21a490fb89acee54baca06dd0ca04a2297659e97` — https://github.com/nipreps/fmriprep
- Nilearn: `c5f6c737c8fc610ceba5f3aaa797695a3e6476a5` — https://github.com/nilearn/nilearn
- NiBabel: `2f7c14298ab8f5cea66d0f2f89cd38eff6b3438c` — https://github.com/nipy/nibabel
- MRIQC: `f61290947f6aa79e143e38e314bfd63c09d7384f` — https://github.com/nipreps/mriqc
- tedana: `1f433185fec67af2ef32529f3ac2b2ce5c9cbc90` — https://github.com/ME-ICA/tedana
- AFNI: `929a3750851dcc26df4d3f73ec036095f04233a8` — https://github.com/afni/afni
