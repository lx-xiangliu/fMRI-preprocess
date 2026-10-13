"""Download ONLY frozen manifest objects; never silently select a new dataset version."""
import hashlib,json,argparse
from pathlib import Path
import requests

def download(root):
    root=Path(root).resolve();rows=json.loads((root/'provenance/data_manifest.json').read_text())
    for r in rows:
        if r['status']!='DOWNLOADED_AND_VALIDATED':raise ValueError('Manifest contains unvalidated source: '+r['path'])
        p=root/'data/ds000114'/r['path'];p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists():
            tmp=p.with_name(p.name+'.part')
            try:
                with requests.get(r['url'],stream=True,timeout=(30,120)) as response:
                    response.raise_for_status()
                    with tmp.open('wb') as f:
                        for block in response.iter_content(2**20):f.write(block)
                verify(tmp,r);tmp.replace(p)
            finally:
                if tmp.exists():tmp.unlink()
        verify(p,r);print('VALIDATED',r['path'])

def verify(p,row):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(2**20),b''):h.update(block)
    if p.stat().st_size!=row['bytes'] or h.hexdigest()!=row['sha256']:raise ValueError('Checksum mismatch: '+str(p))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=a.parse_args();download(args.root)
