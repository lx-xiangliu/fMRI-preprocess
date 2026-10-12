# Reference dataset: Amsterdam Open MRI Collection (AOMIC)

All examples in this repository use a small subset of **AOMIC**, so that every sub-category is
demonstrated on the same real, public, multimodal data.

| | PIOP1 (primary) | PIOP2 (supplement) | ID1000 (supplement) |
|---|---|---|---|
| OpenNeuro | [ds002785](https://openneuro.org/datasets/ds002785) | [ds002790](https://openneuro.org/datasets/ds002790) | [ds003097](https://openneuro.org/datasets/ds003097) |
| Dataset DOI | 10.18112/openneuro.ds002785.v2.0.0 | 10.18112/openneuro.ds002790.v2.0.0 | 10.18112/openneuro.ds003097.v1.2.1 |
| License | CC0 | CC0 | CC0 |
| Access | public, no login | public, no login | public, no login |
| Subjects used here | sub-0001, 0002, 0003 | sub-0001 | sub-0001 |
| BOLD used | restingstate acq-mb3 (80×80×36×480, 3×3×3.3 mm, **TR 0.75 s**, multiband 3); workingmemory acq-seq (80×80×37×162, **TR 2 s**) + events | restingstate acq-seq (80×80×36×240, TR 2 s) | moviewatching (42×64×54×290, 3.3×3×3 mm, **TR 2.2 s**, SliceTiming) |
| Other modalities used | T1w (1 mm), cardiac + respiratory physiology (496 Hz), task events, (DWI exists, not downloaded) | T1w, physiology | physiology, movie stimulus (not downloaded) |
| Derivatives used | fMRIPrep 1.4.1 (space-T1w BOLD, MNI152NLin2009cAsym masks/boldref, confounds, anat segmentations, transforms), MRIQC group IQMs, RETROICOR regressors | – | – |

Scanner: Philips 3T (all datasets; data converted with dcm2niix, see sidecars).

**Paper**: Snoek, L., van der Miesen, M.M., Beemsterboer, T., van der Leij, A., Eigenhuis, A., &
Scholte, H.S. (2021). The Amsterdam Open MRI Collection, a set of multimodal MRI datasets for
individual difference analyses. *Scientific Data* 8, 85. https://doi.org/10.1038/s41597-021-00870-6

Why AOMIC: BIDS-organised, CC0, includes structural MRI + fMRI + physiology + DWI + task events,
ships fMRIPrep/MRIQC derivatives (allowing direct numerical comparison of our implementations
against reference tool outputs), and its three sub-datasets differ in TR (0.75/2/2.2 s), matrix,
voxel size and acquisition (multiband vs sequential) — i.e. the very heterogeneity a foundation
model must handle — while coming from one site, isolating protocol effects from site effects.

Limitations (honest): single vendor (Philips) and single site, so vendor/site intensity effects
can only be partially illustrated; only 3+1+1 subjects are downloaded, so group-level statistics
(e.g. QC-FC) are illustrative, not conclusive.

## Download

```bash
python scripts/download_data.py            # ~2.5 GB into ./data (or $FMRI_REF_DATA)
```
The exact file list is in `scripts/data_manifest.txt` (pulled from the public OpenNeuro S3 bucket
`s3://openneuro.org`). Code accesses data only through `fmri_common.aomic(...)` — see
`common/fmri_common/paths.py`.

## Layout (BIDS)
```
data/ds002785/
  sub-0001/anat/sub-0001_T1w.nii.gz
  sub-0001/func/sub-0001_task-restingstate_acq-mb3_{bold.nii.gz,bold.json,recording-respcardiac_physio.tsv.gz}
  derivatives/fmriprep/sub-0001/{anat,func}/...
  derivatives/physiology/sub-0001/physio/*_desc-retroicor_regressors.tsv
  derivatives/mriqc/group_{bold,T1w}.tsv
data/ds002790/sub-0001/...
data/ds003097/sub-0001/...
```
