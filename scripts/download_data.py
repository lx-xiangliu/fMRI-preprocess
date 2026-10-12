#!/usr/bin/env python
"""Download the reference subset of AOMIC (OpenNeuro, CC0) listed in data_manifest.txt.

Usage: python scripts/download_data.py [--dest DIR] [--workers 6]
Default destination: $FMRI_REF_DATA or <repo>/data. Files already present are skipped.
Source: public OpenNeuro S3 bucket (https://s3.amazonaws.com/openneuro.org/), no login.
"""
import argparse
import concurrent.futures as cf
import os
import urllib.request
from pathlib import Path

BASE = "https://s3.amazonaws.com/openneuro.org/"
HERE = Path(__file__).resolve().parent


def fetch(key: str, dest: Path) -> str:
    out = dest / key
    if out.exists() and out.stat().st_size > 0:
        return "skip"
    out.parent.mkdir(parents=True, exist_ok=True)
    err = None
    for _ in range(3):
        try:
            urllib.request.urlretrieve(BASE + key, str(out) + ".part")
            os.replace(str(out) + ".part", out)
            return "ok"
        except Exception as e:  # noqa: BLE001
            err = e
    return f"FAIL {err}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default=os.environ.get("FMRI_REF_DATA", HERE.parent / "data"))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--manifest", default=HERE / "data_manifest.txt")
    a = ap.parse_args()
    keys = [k.strip() for k in open(a.manifest) if k.strip()]
    dest = Path(a.dest)
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for k, s in zip(keys, ex.map(lambda k: fetch(k, dest), keys)):
            if s.startswith("FAIL"):
                print(k, s)
    print(f"done: {len(keys)} files -> {dest}")


if __name__ == "__main__":
    main()
