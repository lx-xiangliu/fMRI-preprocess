"""Path resolution for the reference datasets (no hard-coded absolute paths).

The data root is resolved in this order:
1. environment variable ``FMRI_REF_DATA``
2. ``<repo_root>/data``
Run ``python scripts/download_data.py`` to populate it.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def data_root() -> Path:
    env = os.environ.get("FMRI_REF_DATA")
    root = Path(env) if env else repo_root() / "data"
    if not root.exists():
        raise FileNotFoundError(
            f"Data root {root} not found. Run `python scripts/download_data.py` "
            "or set FMRI_REF_DATA.")
    return root


SPACE_MNI = "MNI152NLin2009cAsym"


@dataclass(frozen=True)
class DatasetFiles:
    """BIDS paths for one subject/task of an AOMIC dataset."""
    dataset: str
    sub: str
    task: str
    acq: str | None

    @property
    def _ent(self) -> str:
        s = f"sub-{self.sub}_task-{self.task}"
        return s + (f"_acq-{self.acq}" if self.acq else "")

    @property
    def raw_dir(self) -> Path:
        return data_root() / self.dataset / f"sub-{self.sub}"

    @property
    def prep_dir(self) -> Path:
        return data_root() / self.dataset / "derivatives" / "fmriprep" / f"sub-{self.sub}"

    # raw
    @property
    def bold(self) -> Path:
        return self.raw_dir / "func" / f"{self._ent}_bold.nii.gz"

    @property
    def bold_json(self) -> Path:
        return self.raw_dir / "func" / f"{self._ent}_bold.json"

    @property
    def events(self) -> Path:
        return self.raw_dir / "func" / f"{self._ent}_events.tsv"

    @property
    def physio(self) -> Path:
        return self.raw_dir / "func" / f"{self._ent}_recording-respcardiac_physio.tsv.gz"

    @property
    def physio_json(self) -> Path:
        return self.raw_dir / "func" / f"{self._ent}_recording-respcardiac_physio.json"

    @property
    def t1w(self) -> Path:
        return self.raw_dir / "anat" / f"sub-{self.sub}_T1w.nii.gz"

    # fMRIPrep derivatives
    def prep_bold(self, space: str = "T1w") -> Path:
        return self.prep_dir / "func" / f"{self._ent}_space-{space}_desc-preproc_bold.nii.gz"

    def prep_mask(self, space: str = "T1w") -> Path:
        return self.prep_dir / "func" / f"{self._ent}_space-{space}_desc-brain_mask.nii.gz"

    def prep_boldref(self, space: str = "T1w") -> Path:
        return self.prep_dir / "func" / f"{self._ent}_space-{space}_boldref.nii.gz"

    def prep_aseg(self, space: str = "T1w") -> Path:
        return self.prep_dir / "func" / f"{self._ent}_space-{space}_desc-aseg_dseg.nii.gz"

    @property
    def confounds(self) -> Path:
        return self.prep_dir / "func" / f"{self._ent}_desc-confounds_regressors.tsv"

    def anat(self, suffix: str, space: str | None = None) -> Path:
        """e.g. suffix='desc-preproc_T1w', 'label-WM_probseg', 'desc-brain_mask'."""
        sp = f"_space-{space}" if space else ""
        return self.prep_dir / "anat" / f"sub-{self.sub}{sp}_{suffix}.nii.gz"

    @property
    def retroicor(self) -> Path:
        return (data_root() / self.dataset / "derivatives" / "physiology" / f"sub-{self.sub}"
                / "physio" / f"{self._ent}_recording-respcardiac_desc-retroicor_regressors.tsv")


def aomic(sub: str = "0001", task: str = "restingstate", dataset: str = "ds002785") -> DatasetFiles:
    """Convenience constructor with AOMIC acquisition labels filled in.

    ds002785 (PIOP1): restingstate -> acq-mb3 (TR 0.75 s), workingmemory -> acq-seq (TR 2 s)
    ds002790 (PIOP2): restingstate -> acq-seq (TR 2 s)
    ds003097 (ID1000): moviewatching -> no acq (TR 2.2 s)
    """
    acq_map = {
        ("ds002785", "restingstate"): "mb3",
        ("ds002785", "workingmemory"): "seq",
        ("ds002790", "restingstate"): "seq",
        ("ds003097", "moviewatching"): None,
    }
    if (dataset, task) not in acq_map:
        raise KeyError(f"Unknown dataset/task combination: {dataset}/{task}")
    return DatasetFiles(dataset, sub, task, acq_map[(dataset, task)])
