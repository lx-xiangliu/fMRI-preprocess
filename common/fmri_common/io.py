"""Minimal, explicit I/O helpers."""
from __future__ import annotations

import json
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd


def load_json_sidecar(path: str | Path) -> dict:
    with open(path) as f:
        return json.load(f)


def get_tr(img_or_path, sidecar: str | Path | None = None) -> float:
    """Return TR in seconds. The BIDS sidecar is authoritative; the NIfTI
    pixdim[4] is used only as fallback (its unit depends on xyzt_units)."""
    if sidecar is not None and Path(sidecar).exists():
        meta = load_json_sidecar(sidecar)
        if "RepetitionTime" in meta:
            return float(meta["RepetitionTime"])
    img = nib.load(img_or_path) if isinstance(img_or_path, (str, Path)) else img_or_path
    tr = float(img.header.get_zooms()[3])
    unit = img.header.get_xyzt_units()[1]
    if unit == "msec":
        tr /= 1000.0
    elif unit == "usec":
        tr /= 1e6
    return tr


def load_bold(path: str | Path, n_vols: int | None = None) -> nib.Nifti1Image:
    """Load a 4D BOLD image; optionally keep only the first ``n_vols`` volumes
    (useful to keep notebooks fast)."""
    img = nib.load(str(path))
    if n_vols is not None:
        img = img.slicer[..., :n_vols]
    return img


def load_confounds(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", na_values="n/a")


def load_physio(tsv_gz: str | Path, json_path: str | Path | None = None):
    """Load BIDS physio. Returns (DataFrame, sampling_frequency, start_time)."""
    tsv_gz = Path(tsv_gz)
    if json_path is None:
        json_path = Path(str(tsv_gz).replace(".tsv.gz", ".json"))
    meta = load_json_sidecar(json_path)
    df = pd.read_csv(tsv_gz, sep="\t", header=None, names=meta["Columns"])
    return df, float(meta["SamplingFrequency"]), float(meta.get("StartTime", 0.0))


def masked_timeseries(img: nib.Nifti1Image, mask: nib.Nifti1Image) -> np.ndarray:
    """Return (T, V) array of in-mask voxels. Requires identical grids."""
    if img.shape[:3] != mask.shape[:3] or not np.allclose(img.affine, mask.affine, atol=1e-3):
        raise ValueError("Image and mask are not on the same voxel grid.")
    m = np.asarray(mask.dataobj) > 0
    return np.asarray(img.dataobj, dtype=np.float32)[m].T
