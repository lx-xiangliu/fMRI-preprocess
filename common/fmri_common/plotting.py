"""Plotting helpers shared by notebooks."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def savefig(fig, results_dir: str | Path, name: str, dpi: int = 110) -> Path:
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    out = results_dir / f"{name}.png"
    fig.savefig(out, dpi=dpi, bbox_inches="tight")
    return out


def carpet(ax, ts: np.ndarray, tr: float | None = None, title: str = ""):
    """Carpet plot of a (T, V) array, voxel-wise z-scored."""
    z = (ts - ts.mean(0)) / (ts.std(0) + 1e-8)
    ext = None if tr is None else [0, ts.shape[0] * tr, 0, ts.shape[1]]
    ax.imshow(z.T, aspect="auto", cmap="gray", vmin=-2, vmax=2, interpolation="none",
              extent=ext)
    ax.set_xlabel("time (s)" if tr else "volume")
    ax.set_ylabel("voxel")
    ax.set_title(title)
