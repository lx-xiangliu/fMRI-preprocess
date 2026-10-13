"""Presentation figures for real ds000114 data. No simulated scientific results."""
from pathlib import Path
import json
import numpy as np
import nibabel as nib
from scipy import signal, stats
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import FancyBboxPatch
from IPython.display import display, HTML

COLORS={'navy':'#20324D','teal':'#148F91','coral':'#E87958','gold':'#E3B65A','muted':'#69768A','light':'#EEF3F8','ink':'#273449'}
CMAP=LinearSegmentedColormap.from_list('report_teal',['#F1F6F5','#A9D6D0','#3EAAA7','#13757C','#173A54'])
DIV=LinearSegmentedColormap.from_list('report_div',['#227F94','#C3DFE6','#FAFAF7','#F4CEB9','#C96348'])

def setup_style():
    chosen=None
    for p in ['/System/Library/Fonts/STHeiti Medium.ttc','/System/Library/Fonts/Hiragino Sans GB.ttc','/System/Library/Fonts/Supplemental/Songti.ttc']:
        if Path(p).is_file():
            font_manager.fontManager.addfont(p);chosen=font_manager.FontProperties(fname=p).get_name();break
    available={x.name for x in font_manager.fontManager.ttflist}
    if chosen is None:
        chosen=next((x for x in ['Noto Sans CJK SC','Microsoft YaHei','SimHei'] if x in available),'DejaVu Sans')
    mpl.rcParams.update({'font.family':['DejaVu Sans'],'font.size':12,'axes.titlesize':15,
        'axes.labelsize':12,'figure.facecolor':'white','axes.facecolor':'white','axes.edgecolor':'#C9D2DF',
        'axes.labelcolor':COLORS['ink'],'text.color':COLORS['ink'],'xtick.color':COLORS['muted'],
        'ytick.color':COLORS['muted'],'axes.spines.top':False,'axes.spines.right':False,
        'axes.unicode_minus':False,'savefig.facecolor':'white','figure.dpi':115,'savefig.dpi':180,
        'axes.prop_cycle':mpl.cycler(color=[COLORS['teal'],COLORS['coral'],COLORS['navy'],COLORS['gold']])})
    return chosen

def install_notebook_style():
    display(HTML('''<style>
    .fmri-report {font-family:-apple-system,BlinkMacSystemFont,"Noto Sans CJK SC","Microsoft YaHei",sans-serif;color:#273449;line-height:1.7}
    .fmri-report .hero {background:linear-gradient(120deg,#20324D,#176F79);border-radius:18px;padding:30px 34px;color:white;margin:8px 0 22px}
    .fmri-report .hero h1 {font-size:32px;font-weight:750;margin:6px 0 10px;color:white;border:0;line-height:1.35}
    .fmri-report .eyebrow {font-size:12px;letter-spacing:2px;opacity:.85}
    .fmri-report .section {border-left:5px solid #148F91;padding:0 0 0 15px;margin:28px 0 14px}
    .fmri-report .section h2 {font-size:25px;line-height:1.3;color:#20324D;margin:3px 0}
    .fmri-report .section small {color:#69768A;font-size:12px;letter-spacing:1.5px}
    .fmri-report .cards {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:18px 0}
    .fmri-report .card {background:#F3F7FA;border-radius:12px;padding:16px 18px;border-top:3px solid #148F91}
    .fmri-report .card b {display:block;color:#20324D;font-size:25px;line-height:1.25;margin:4px 0}
    .fmri-report .card span {font-size:12px;color:#69768A}
    .fmri-report .note {background:#FFF5EB;border-left:4px solid #E3B65A;padding:12px 16px;border-radius:6px;margin:14px 0;font-size:14px}
    .fmri-report .result {background:#EEF8F6;border-left:4px solid #148F91;padding:12px 16px;border-radius:6px;margin:14px 0;font-size:14px}
    .fmri-report table {border-collapse:collapse;width:100%;font-size:14px;margin:14px 0}
    .fmri-report th {background:#20324D;color:white;text-align:left;padding:12px 14px}
    .fmri-report td {padding:11px 14px;border-bottom:1px solid #E4EAF0;text-align:left}
    .fmri-report tr:nth-child(even) td {background:#F6F9FB}
    .fmri-report pre {font-size:13px;line-height:1.6;background:#F4F7FA;padding:18px;border-radius:12px;color:#20324D;overflow-x:auto}
    </style>'''))

def html(text):display(HTML('<div class="fmri-report">'+text+'</div>'))
def section(number,title,subtitle=''):
    html(f'<div class="section"><small>{number}</small><h2>{title}</h2><div>{subtitle}</div></div>')
def cards(items):
    html('<div class="cards">'+''.join(f'<div class="card"><span>{a}</span><b>{b}</b><span>{c}</span></div>' for a,b,c in items)+'</div>')
def note(text,kind='note'):html(f'<div class="{kind}">{text}</div>')
def table(headers,rows):
    html('<table><thead><tr>'+''.join('<th>'+str(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table>')

def finish(fig,name,out):
    fig.savefig(Path(out)/(name+'.png'),bbox_inches='tight',dpi=180)
    display(fig);plt.close(fig)

def _plane(a,axis,fraction=.5):
    idx=int(round((a.shape[axis]-1)*fraction));return np.take(a,idx,axis=axis).T

def _image(ax,a,title,vmin=None,vmax=None,cmap='gray'):
    ax.imshow(a,origin='lower',cmap=cmap,vmin=vmin,vmax=vmax,interpolation='nearest')
    ax.set_title(title,pad=12);ax.set_xticks([]);ax.set_yticks([])
    for spine in ax.spines.values():spine.set_visible(False)

def _lim(a):
    values=a[np.isfinite(a)&(a>0)]
    return np.percentile(values,[1,99]) if len(values) else (0,1)

def modalities(t1,bold,dwi,out):
    volumes=[t1,bold,dwi];titles=['T1w | Structural MRI','BOLD | Functional MRI','DWI b=0 | Diffusion MRI']
    fig,axs=plt.subplots(2,3,figsize=(13.5,7.5),layout='constrained')
    for j,(im,title) in enumerate(zip(volumes,titles)):
        im=nib.as_closest_canonical(im);a=im.get_fdata();lo,hi=_lim(a)
        _image(axs[0,j],_plane(a,2),title,lo,hi)
        _image(axs[1,j],_plane(a,0),'Sagittal view',lo,hi)
    fig.suptitle('Multimodal inputs from the same participant',fontsize=22,fontweight='bold',color=COLORS['navy'])
    finish(fig,'01_multimodal_input',out)

def workflow(out):
    fig,ax=plt.subplots(figsize=(14.2,2.6));ax.set_xlim(0,15);ax.set_ylim(0,2.4);ax.axis('off')
    steps=[('Inputs','Geometry / TR\nChecksums'),('Space','Orientation / grid\nAlignment'),('Time','Sampling / windows\nValidity masks'),('Signal','Drift model\nJoint projection'),('QC + scale','Metrics / transforms\nEvidence')]
    for i,(title,sub) in enumerate(steps):
        x=.1+i*3;ax.add_patch(FancyBboxPatch((x,.55),2.55,1.2,boxstyle='round,pad=.14,rounding_size=.15',fc='#EEF6F6',ec='#B9D9D7',lw=1.1))
        ax.text(x+1.27,1.35,title,ha='center',va='center',fontsize=17,color=COLORS['navy'],fontweight='bold')
        ax.text(x+1.27,.9,sub,ha='center',va='center',fontsize=11,color=COLORS['muted'])
        if i<4:ax.annotate('',xy=(x+2.91,1.15),xytext=(x+2.7,1.15),arrowprops={'arrowstyle':'->','color':COLORS['teal'],'lw':2})
    ax.text(7.5,.08,'Conceptual organization. Production steps require their own inputs and validation.',ha='center',fontsize=11,color=COLORS['muted'])
    finish(fig,'02_workflow',out)

def task_context(events,t,raw_signal,out):
    fig,axs=plt.subplots(2,1,figsize=(13.5,5.5),layout='constrained',sharex=True,gridspec_kw={'height_ratios':[1.3,1]})
    axs[0].plot(t,raw_signal,color=COLORS['navy'],lw=1.5);axs[0].set_ylabel('Mean raw intensity');axs[0].set_title('Raw BOLD example: context before preprocessing');axs[0].grid(axis='y',alpha=.12)
    for j,(name,c) in enumerate([('Finger',COLORS['teal']),('Foot',COLORS['coral']),('Lips',COLORS['gold'])]):
        blocks=[(float(r.onset),float(r.duration)) for r in events.itertuples() if r.trial_type==name]
        axs[1].broken_barh(blocks,(j-.32,.64),facecolors=c,alpha=.9)
    axs[1].set_yticks([0,1,2],['Finger','Foot','Lips']);axs[1].set_ylim(-.65,2.65);axs[1].set_xlabel('Original acquisition time / s');axs[1].set_xlim(0,t[-1]);axs[1].set_title('Published task events; no task-response model fitted')
    fig.suptitle('Task structure | Preserve acquisition times and event metadata',fontsize=19,fontweight='bold')
    finish(fig,'01b_task_context',out)

def orientation(native,canon,error,out):
    fig,axs=plt.subplots(1,2,figsize=(12.5,5.3),layout='constrained');lo,hi=_lim(native.get_fdata())
    _image(axs[0],_plane(native.get_fdata(),2),'Before | LAS storage axes',lo,hi)
    _image(axs[1],_plane(canon.get_fdata(),2),'After | RAS storage axes',lo,hi)
    for ax,label in zip(axs,['First storage axis: right to left','First storage axis: left to right']):ax.set_xlabel(label,color=COLORS['muted']);ax.set_xticks([])
    fig.suptitle(f'Lossless reorientation | Round-trip intensity error = {error:.1e}',fontsize=19,fontweight='bold')
    finish(fig,'03_orientation',out)

def spacing(im4,im3,mae,out):
    fig,axs=plt.subplots(1,3,figsize=(14,5),layout='constrained');lo,hi=_lim(im4.get_fdata())
    a=im4.get_fdata();b=im3.get_fdata()
    _image(axs[0],_plane(a,2),'4 mm reference grid',lo,hi)
    _image(axs[1],_plane(b,2),'3 mm linear resampling',lo,hi)
    # Physical world-space center coordinates on an axis-aligned shared demonstration grid.
    for im,color,label in [(im4,COLORS['coral'],'4 mm'),(im3,COLORS['teal'],'3 mm')]:
        x=im.affine[0,3]+np.arange(im.shape[0])*im.affine[0,0];y=im.affine[1,3]+np.arange(im.shape[1])*im.affine[1,1]
        xx,yy=np.meshgrid(x,y);keep=(np.abs(xx)<15)&(np.abs(yy)<15)
        axs[2].scatter(xx[keep],yy[keep],s=16,alpha=.75,color=color,label=label)
    axs[2].set_aspect('equal');axs[2].set_xlabel('World x / mm');axs[2].set_ylabel('World y / mm');axs[2].legend(frameon=False);axs[2].set_title('Sample centers in the same physical region')
    fig.suptitle('Voxel spacing | A denser grid does not add acquired information',fontsize=19,fontweight='bold')
    finish(fig,'04_spacing',out)

def smoothing(before,after,mask,out):
    a=before.get_fdata();b=after.get_fdata();diff=b-a;lo,hi=_lim(a);z=a.shape[2]//2
    fig,axs=plt.subplots(1,3,figsize=(14,5),layout='constrained')
    _image(axs[0],a[:,:,z].T,'Before | No added smoothing',lo,hi)
    _image(axs[1],b[:,:,z].T,'After | 4 mm FWHM',lo,hi)
    vmax=float(np.percentile(np.abs(diff[mask]),99));im=axs[2].imshow(diff[:,:,z].T,origin='lower',cmap=DIV,vmin=-vmax,vmax=vmax,interpolation='nearest');axs[2].set_title('Difference | Smoothed - original');axs[2].axis('off');fig.colorbar(im,ax=axs[2],fraction=.045,pad=.02,label='Original intensity units')
    fig.suptitle('Spatial smoothing | Lower local variation, greater neighborhood mixing',fontsize=19,fontweight='bold')
    finish(fig,'05_smoothing',out)

def registration(fixed,before,after,report,out):
    fa=fixed.get_fdata();ba=before.get_fdata();aa=after.get_fdata();lo,hi=_lim(fa)
    fig,axs=plt.subplots(2,3,figsize=(13,8),layout='constrained')
    for row,vol in enumerate([ba,aa]):
        vlo,vhi=_lim(vol);norm=np.clip((vol-vlo)/(vhi-vlo),0,1)
        for col,axis in enumerate([0,1,2]):
            _image(axs[row,col],_plane(fa,axis),['Sagittal view','Coronal view','Axial view'][col],lo,hi)
            axs[row,col].contour(_plane(norm,axis),levels=[.25,.5,.75],colors=[COLORS['teal']],linewidths=[.7,1,1.2],alpha=.85)
            axs[row,col].text(.03,.05,'Before: header-based resampling' if row==0 else 'After: rigid MI registration',transform=axs[row,col].transAxes,color='white',fontsize=11,bbox={'facecolor':COLORS['navy'],'alpha':.82,'edgecolor':'none','pad':5})
    fig.suptitle('BOLD to T1w | Grayscale: T1w; teal contours: BOLD',fontsize=19,fontweight='bold')
    finish(fig,'06_registration',out)

def temporal(x,y,tin,tout,tr_in,tr_out,out):
    i=64;baseline=x[:,i].mean();fig=plt.figure(figsize=(14,7),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[1,1.25]);ax=fig.add_subplot(gs[0,:])
    ax.plot(tin,x[:,i]-baseline,color=COLORS['coral'],lw=1.3,alpha=.85,label='Original: 2.5 s/sample')
    ax.plot(tout,y[:,i]-baseline,color=COLORS['teal'],lw=1.4,label='Anti-aliased: 5 s/sample');ax.set_xlabel('Physical time / s');ax.set_ylabel('Intensity - original mean');ax.legend(frameon=False,ncol=2);ax.grid(axis='y',alpha=.13)
    a=fig.add_subplot(gs[1,0]);take=tin<=100;a.plot(tin[take],x[take,i]-baseline,'o-',ms=4,color=COLORS['coral'],alpha=.8,label='Original');take=tout<=100;a.plot(tout[take],y[take,i]-baseline,'s-',ms=5,color=COLORS['teal'],label='Resampled');a.set_title('First 100 seconds | Sample times');a.set_xlabel('Physical time / s');a.set_ylabel('Intensity - original mean');a.legend(frameon=False)
    a=fig.add_subplot(gs[1,1])
    for arr,tr,c,l in [(x,tr_in,COLORS['coral'],'Original'),(y,tr_out,COLORS['teal'],'Resampled')]:
        f,p=signal.welch(arr[:,i],fs=1/tr,nperseg=min(64,len(arr)),detrend='constant');a.semilogy(f,np.maximum(p,1e-8),color=c,lw=2,label=l)
    a.axvspan(.5/tr_out,.5/tr_in,color=COLORS['gold'],alpha=.15);a.axvline(.5/tr_out,color=COLORS['muted'],ls='--',lw=1);a.set_xlabel('Frequency / Hz');a.set_ylabel('PSD / intensity squared * s');a.set_title('Nyquist limit and retained frequencies');a.legend(frameon=False)
    fig.suptitle('Temporal resampling | FIR low-pass + polyphase downsampling',fontsize=19,fontweight='bold')
    finish(fig,'07_temporal_resampling',out)

def windows(x,cropped,padded,valid,tr,out):
    base=x[:,64].mean();fig,axs=plt.subplots(3,1,figsize=(13.5,8),layout='constrained',sharex=True)
    axs[0].plot(np.arange(len(x)),x[:,64]-base,color=COLORS['navy'],lw=1.4);axs[0].axvspan(0,len(cropped)-1,color=COLORS['teal'],alpha=.1);axs[0].set_title(f'Original run | {len(x)} acquired samples')
    axs[1].plot(np.arange(len(cropped)),cropped[:,64]-base,color=COLORS['teal'],lw=1.5);axs[1].set_title(f'Fixed window | First {len(cropped)} samples, {len(cropped)*tr:.0f} s nominal duration')
    axs[2].plot(np.arange(len(padded))[valid],padded[valid,64]-base,color=COLORS['teal'],lw=1.4);axs[2].axvspan(valid.sum()-.5,len(padded)-.5,color=COLORS['gold'],alpha=.25);axs[2].text(valid.sum()+2,0,'Padding\nmask = 0',color=COLORS['navy'],fontsize=12,va='center');axs[2].set_title(f'Masked padding | {valid.sum()} valid + {(~valid).sum()} padded')
    lim=np.max(np.abs(x[:,64]-base))*1.15
    for ax in axs:ax.set_ylim(-lim,lim);ax.set_ylabel('Valid signal - original mean');ax.grid(axis='y',alpha=.12)
    axs[2].set_xlim(0,len(padded)-1);axs[2].set_xlabel('Original / model sample index; padded positions are not acquired time points')
    fig.suptitle('Sequence length | Information costs of cropping and padding',fontsize=19,fontweight='bold')
    finish(fig,'08_windows',out)

def drift(x,residual,t,high_pass,out):
    centered=x-x.mean(0);trend=x-residual-x.mean(0);i=64
    fig=plt.figure(figsize=(14,9.5),layout='constrained');gs=fig.add_gridspec(3,2,height_ratios=[1,1,1.3]);a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[1,0])
    a.plot(t,centered[:,i],color=COLORS['coral'],lw=1.2,alpha=.8,label='Original, centered');a.plot(t,trend[:,i],color=COLORS['navy'],lw=2.8,label='DCT drift model');a.set_title('Before | Complete acquired series');a.legend(frameon=False,ncol=2,fontsize=10)
    b.plot(t,residual[:,i],color=COLORS['teal'],lw=1.4);b.set_title('After | Complete residual series');b.set_xlabel('Original physical time / s')
    lim=max(np.abs(centered[:,i]).max(),np.abs(residual[:,i]).max())*1.12
    for ax in [a,b]:ax.set_ylabel('Intensity - original mean');ax.set_ylim(-lim,lim);ax.grid(axis='y',alpha=.12)
    zoom=(t>=20)&(t<=450)
    zoomlim=max(np.abs(centered[zoom,i]).max(),np.abs(residual[zoom,i]).max())*1.12
    for row,arr,color,title in [(0,centered,COLORS['coral'],'Before | Detail, 20-450 s'),(1,residual,COLORS['teal'],'After | Detail, 20-450 s')]:
        ax=fig.add_subplot(gs[row,1]);ax.plot(t[zoom],arr[zoom,i],color=color,lw=1.4)
        if row==0:ax.plot(t[zoom],trend[zoom,i],color=COLORS['navy'],lw=2.5)
        ax.set_ylim(-zoomlim,zoomlim);ax.set_xlabel('Original physical time / s');ax.set_ylabel('Intensity - original mean');ax.set_title(title);ax.grid(axis='y',alpha=.12)
    for j,(arr,title) in enumerate([(x,'Before | Carpet plot'),(residual,'After | Carpet plot')]):
        z=(arr-arr.mean(0))/arr.std(0,ddof=1);ax=fig.add_subplot(gs[2,j]);im=ax.imshow(z.T,aspect='auto',origin='lower',extent=[t[0],t[-1],0,x.shape[1]],cmap=DIV,vmin=-3,vmax=3);ax.set_title(title);ax.set_xlabel('Physical time / s');ax.set_ylabel('128 deterministic example voxels')
    fig.colorbar(im,ax=[fig.axes[-2],fig.axes[-1]],shrink=.8,label='Within-series z-score (display only)')
    fig.suptitle(f'Drift removal | DCT high-pass example: {high_pass:.3f} Hz',fontsize=19,fontweight='bold')
    finish(fig,'09_drift_and_carpet',out)

def scaling(x,z,psc,robust,t,out):
    fig,axs=plt.subplots(2,4,figsize=(16,8),layout='constrained');i=64
    for j,(arr,title,unit,c) in enumerate([(x,'Before | Original signal','Raw intensity',COLORS['gold']),(z,'After | Sample z-score','Sample-SD units',COLORS['teal']),(psc,'After | PSC','Original baseline / %',COLORS['coral']),(robust,'After | Median / MAD','Robust-scale units',COLORS['navy'])]):
        axs[0,j].plot(t,arr[:,i],color=c,lw=1.5);axs[0,j].axhline(0,color='#C7D1DE',lw=.8);axs[0,j].set_title(title);axs[0,j].set_xlabel('Physical time / s');axs[0,j].set_ylabel(unit)
        if j==0:
            axs[0,j].lines[-1].remove()
            axs[0,j].axhline(x[:,i].mean(),color=COLORS['muted'],ls='--',lw=1)
        vals=arr.ravel();lo,hi=np.percentile(vals,[.5,99.5]);xx=np.linspace(lo,hi,240);density=stats.gaussian_kde(vals);axs[1,j].fill_between(xx,density(xx),color=c,alpha=.16);axs[1,j].plot(xx,density(xx),color=c,lw=2);axs[1,j].set_xlabel(unit);axs[1,j].set_ylabel('Descriptive density');axs[1,j].set_title('Pooled values | Display only')
    fig.suptitle('Signal scaling | Original baseline and transformed values',fontsize=19,fontweight='bold')
    finish(fig,'10_scaling',out)

def qc(raw_dvars,clean_dvars,t,tsnr_volume,mask,out):
    fig=plt.figure(figsize=(14,8),layout='constrained');gs=fig.add_gridspec(2,3,height_ratios=[1,1.4]);ax=fig.add_subplot(gs[0,:]);ax.plot(t,raw_dvars,color=COLORS['coral'],lw=1.5,label='Original raw DVARS');ax.plot(t,clean_dvars,color=COLORS['teal'],lw=1.5,alpha=.85,label='Raw DVARS of DCT residuals');ax.set_xlabel('Original physical time / s');ax.set_ylabel('RMS intensity change');ax.set_title('Between-volume changes | Matched intensity units and voxel set');ax.legend(frameon=False,ncol=2);ax.grid(axis='y',alpha=.13)
    vals=tsnr_volume[mask];vmax=float(np.percentile(vals[np.isfinite(vals)],98));caxes=[]
    for j,axis in enumerate([0,1,2]):
        ax=fig.add_subplot(gs[1,j]);img=_plane(tsnr_volume,axis);im=ax.imshow(img,origin='lower',cmap=CMAP,vmin=0,vmax=vmax,interpolation='nearest');ax.set_title(['Original tSNR | Sagittal','Original tSNR | Coronal','Original tSNR | Axial'][j]);ax.axis('off');caxes.append(ax)
    fig.colorbar(im,ax=caxes,shrink=.8,label='Original temporal mean / sample SD')
    fig.suptitle('Quality control | Inspect changes within valid metric scope',fontsize=19,fontweight='bold')
    finish(fig,'11_quality_control',out)

def reproducibility(errors,out):
    fig,axs=plt.subplots(1,2,figsize=(13,4.8),layout='constrained')
    labels=['test','retest'];xx=np.arange(2)
    for key,c,offset,label in [('zscore',COLORS['teal'],-.17,'Sample z-score'),('psc',COLORS['coral'],.17,'PSC')]:
        vals=[errors[s][key] for s in labels];axs[0].bar(xx+offset,vals,.3,color=c,label=label)
    axs[0].set_yscale('log');axs[0].set_xticks(xx,labels);axs[0].set_ylabel('Maximum absolute error vs. Nilearn');axs[0].set_title('Numerical agreement across implementations');axs[0].legend(frameon=False)
    axs[1].axis('off')
    for y,num,title,sub in [(.82,'46 / 46','Real-data notebooks executed','Spatial, temporal, signal and scaling examples'),(.48,'59 / 59','Key checks passed','Invariants, preconditions and misuse guards'),(.14,'2 runs','Few-shot real-data validation','Insufficient to establish scientific superiority')]:
        axs[1].text(.02,y,num,fontsize=26,color=COLORS['teal'],fontweight='bold',va='center');axs[1].text(.34,y+.035,title,fontsize=15,color=COLORS['navy'],va='center');axs[1].text(.34,y-.045,sub,fontsize=11,color=COLORS['muted'],va='center')
    fig.suptitle('Validation | Mathematical agreement and scientific scope',fontsize=19,fontweight='bold')
    finish(fig,'12_reproducibility',out)
