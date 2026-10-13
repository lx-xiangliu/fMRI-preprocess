"""Execute real-data examples and write an honest per-notebook ledger."""
import os,sys,json,time,argparse
from pathlib import Path
import nbformat
from nbclient import NotebookClient

def main(root,kinds=None):
    root=Path(root).resolve();sys.path.insert(0,str(root))
    from fmri_reference.catalog import CATEGORIES
    k=root/'.jupyter/kernels/fmri-reference';k.mkdir(parents=True,exist_ok=True)
    (k/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Python (fMRI reference)','language':'python'}))
    os.environ['JUPYTER_PATH']=str(root/'.jupyter')+os.pathsep+os.environ.get('JUPYTER_PATH','')
    previous=root/'reports/notebook_execution.json'
    ledger=json.loads(previous.read_text()) if kinds and previous.exists() else []
    began=time.time()
    for big,small,title,kind,*rest in CATEGORIES:
        if kinds and kind not in kinds:continue
        for p in sorted((root/big/small/'few_shots').glob('*.ipynb')):
            start=time.time();row={'path':str(p.relative_to(root)),'kind':kind,'status':'RUNNING','python_executable':sys.executable}
            try:
                n=nbformat.read(p,as_version=4);NotebookClient(n,timeout=240,kernel_name='fmri-reference',resources={'metadata':{'path':str(root)}}).execute();nbformat.write(n,p)
                row['status']='EXECUTED';session='retest' if 'retest' in p.name else 'test'
                metrics=json.loads((root/big/small/'results'/session/'metrics.json').read_text());row['evidence_status']=metrics['evidence_status']
            except Exception as e:row.update(status='FAILED',error=str(e))
            row['elapsed_seconds']=time.time()-start
            ledger=[r for r in ledger if r['path']!=row['path']];ledger.append(row);print(row['status'],row['path'],row.get('error','')[:500],flush=True)
            (root/'reports/notebook_execution.json').write_text(json.dumps(ledger,indent=2))
    summary={'scope':'Teaching examples and numerical/prerequisite validation; NOT complete scientific pipeline benchmark',
        'categories':len(CATEGORIES),'executed':sum(r['status']=='EXECUTED' for r in ledger),'failed':sum(r['status']=='FAILED' for r in ledger),
        'elapsed_seconds':time.time()-began,'notebooks':ledger,
        'mature_pipeline_comparison':'NOT_RUN','scientifically_optimal_implementation':'INSUFFICIENT_EVIDENCE',
        'unmeasured':['formal FD','standardized DVARS','nonsteady-state labels','anatomical brain coverage','nonlinear normalization','SDC','real RETROICOR','aCompCor denoising','ICA-AROMA/tedana','downstream pretraining utility'],
        'test_results':'See pytest_report.txt and pytest.xml; notebook execution does not replace invariant tests'}
    (root/'reports/validation_summary.json').write_text(json.dumps(summary,indent=2))
    if summary['failed']:raise SystemExit(1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--kinds',nargs='*');a=p.parse_args();main(a.root,a.kinds)
