# Validation log

- Date: 2026-10-12 (Asia/Shanghai).
- Environment: `/opt/anaconda3/bin/python` (Conda `base`, Python 3.12.2).
- Installed versions: NumPy 1.26.4, SciPy 1.13.1, nibabel 5.4.2, nilearn 0.14.1, pytest 8.x, nbclient 0.10.x, matplotlib 3.x.
- Deterministic tests: **23 passed**.
- Real-data notebooks: **46/46 executed successfully** with a downloaded OpenNeuro ds000114 `sub-01/ses-test` finger-foot-lips BOLD NIfTI (23.3 MiB) and task-level JSON sidecar. Each notebook loaded the real NIfTI, printed pre-processing metadata/metrics, produced a matplotlib time-series visualization, and completed its function call.
- Dataset snapshot: downloaded directly from the public S3 object URLs on 2026-10-12; no full-dataset claim is made. The data files are ignored by Git; reproduce with the URLs in `data/README.md`.
- Limitations: the sample has no subject-level motion or physiological recording in the downloaded subset, so motion/physiology demonstrations derive explicitly labeled signals or model regressors; they are API demonstrations, not claims about scanner motion or physiology quality.
