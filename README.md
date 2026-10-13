# fMRI preprocessing reference

This repository contains the reference library and presentation notebook developed
for auditable fMRI preprocessing. The earlier root-level scaffolding has been removed.

- [Reference library and method comparisons](standard-reference/README.md)
- [English presentation notebook](standard-reference/reports/presentation/fmri_preprocessing_report.ipynb)
- [Notebook environment instructions](standard-reference/reports/presentation/ENVIRONMENT.md)
- [Validated dataset and access conditions](standard-reference/DATASET.md)
- [Scientific validation scope](standard-reference/reports/RESULTS.md)

The existing local project interpreter is `standard-reference/.venv/bin/python`.
The notebook uses the **Python (fMRI Project .venv)** kernel. Keeping the library
at `standard-reference/` preserves the current local data and environment paths.

The library contains four categories and 23 subcategories. Numerical checks and
real-data demonstrations are reported separately from unrun production workflows
and unmeasured scientific outcomes. No universally optimal method is claimed.

Raw MRI data, Python environments, machine-local kernels and caches are excluded
from Git. Frozen download manifests and dependency locks are included in the library.
