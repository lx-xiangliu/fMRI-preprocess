"""Shared utilities for the fMRI preprocessing reference repository.

Only dataset access, I/O and plotting helpers live here. Method implementations
live in each sub-category's ``src/`` package.
"""
from .paths import data_root, repo_root, aomic, DatasetFiles
from .io import load_bold, load_json_sidecar, load_confounds, load_physio, get_tr

__all__ = ["data_root", "repo_root", "aomic", "DatasetFiles", "load_bold",
           "load_json_sidecar", "load_confounds", "load_physio", "get_tr"]
