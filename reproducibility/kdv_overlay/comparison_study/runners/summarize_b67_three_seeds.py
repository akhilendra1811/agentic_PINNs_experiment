"""Audit three same-device corrected runs and report sample SD (ddof=1)."""
import csv
import hashlib
import json
import os
from pathlib import Path
import tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'kdv-mpl-cache'))
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'comparison_study/outputs'
OUT=BASE/'winner_b067_trapezoid_three_seeds'
SEEDS=[99417,99418,99419]


def folder(seed):
    return BASE/('winner_b067_trapezoid_200k' if seed==99417 else f'winner_b067_trapezoid_local_seed_{seed}')


def write_csv(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)


def main():
    rows=[];histories=[];configs=[];preds=[];metrics=[]
    for seed in SEEDS:
        p=folder(seed);c=json.loads((p/'config.json').read_text());configs.append({k:v for k,v in c.items() if k!='seed'})
        s=json.loads((p/'summary.json').read_text());assert s['status']=='complete' and s['step']==200000
        assert c['seed']==seed and c['device']=='mps'
        audit=json.loads((p/'independent_verification.json').read_text());assert audit['optimizer_step_counters']==[200000]
        with np.load(p/'prediction_reference.npz') as z:
            t,x,ref,pred=[z[k] for k in ['t','x','u_ref','u_pred']]
        if preds:
            assert np.array_equal(t,tt) and np.array_equal(x,xx) and np.array_equal(ref,reference)
        else:tt,xx,reference=t,x,ref
        err=pred.astype(float)-ref.astype(float)
        rel=float(np.sqrt(np.sum(err**2)/np.sum(ref**2)));rmse=float(np.sqrt(np.mean(err**2)))
        assert abs(rel-s['final_metrics']['relative_l2'])<1e-13
        crossed=s['first_below_paper']
        rows.append(dict(seed=seed,steps=200000,relative_l2=rel,rmse=rmse,max_abs_error=float(abs(err).max()),
                         run_loop_minutes=s['loop_elapsed_seconds']/60,
                         first_observed_below_paper_step='' if crossed is None else crossed['step']))
        with (p/'reference_error_history.csv').open() as f:h=list(csv.DictReader(f))
        assert [int(float(r['step'])) for r in h]==list(range(0,200001,1000))
        histories.append(np.array([float(r['relative_l2']) for r in h]));preds.append(pred);metrics.append(audit)
    assert all(c==configs[0] for c in configs[1:]),'Configuration differs beyond seed'
    OUT.mkdir(exist_ok=True)
    write_csv(OUT/'per_seed_metrics.csv',rows)
    stats={key:dict(mean=float(np.mean([r[key] for r in rows])),sample_sd=float(np.std([r[key] for r in rows],ddof=1))) for key in ['relative_l2','rmse','max_abs_error']}
    result=dict(n=3,seeds=SEEDS,steps=200000,device='mps',torch_version=configs[0]['torch_version'],statistics=stats,
                qualification='Same-device fixed-method replication of a test-informed corrected variant; sample SD is not a confidence interval. Reference labels were diagnostic only.')
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    values=np.stack(histories);mean=values.mean(axis=0);sd=values.std(axis=0,ddof=1);steps=np.arange(0,200001,1000)
    write_csv(OUT/'error_mean_sd_by_step.csv',[dict(step=int(k),mean_relative_l2=float(m),sample_sd=float(s)) for k,m,s in zip(steps,mean,sd)])
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    def export(fig,name):
        for ext in ['png','pdf']:fig.savefig(OUT/(name+'.'+ext),dpi=200,bbox_inches='tight')
        plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
    for ax in axes:
        for seed,y in zip(SEEDS,values):ax.semilogy(steps,y,alpha=.4,lw=.9,label=f'Seed {seed}')
        ax.semilogy(steps,mean,color='#6f4798',lw=1.8,label='Mean of 3 seeds')
        # Nonpositive SD lower bounds cannot be shown on a log axis; mask those intervals.
        lower=mean-sd
        ax.fill_between(steps,lower,mean+sd,where=lower>0,alpha=.2,color='#6f4798',label='Mean +/- sample SD')
        ax.scatter([200000],[4.27e-4],marker='*',s=85,color='black',zorder=5,label='Published PirateNet endpoint')
        ax.set(xlabel='Optimizer updates',ylabel='Relative $L^2$ error');ax.grid(alpha=.2)
    axes[0].legend(fontsize=7)
    axes[0].set_title('Full training history')
    axes[1].set_title('Late training: zoomed x and y axes')
    axes[1].set_xlim(100000,205000)
    late=steps>=100000
    positive_lower=(mean-sd)[late]
    positive_lower=positive_lower[positive_lower>0]
    bottom=min(values[:,late].min(),positive_lower.min(),4.27e-4)*.8
    top=max(values[:,late].max(),(mean+sd)[late].max(),4.27e-4)*1.2
    axes[1].set_ylim(bottom,top)
    fig.suptitle('Corrected winner 67 | fixed method, three MPS seeds; SD is across seeds')
    export(fig,'three_seed_error_curves')
    fig,ax=plt.subplots(figsize=(6,4),layout='constrained')
    ax.scatter([0]*3,[r['relative_l2'] for r in rows],color='#6f4798',label='Individual seeds')
    ax.errorbar([.15],[stats['relative_l2']['mean']],yerr=[stats['relative_l2']['sample_sd']],fmt='o',capsize=5,color='#6f4798',label='Mean +/- sample SD')
    ax.scatter([1],[4.27e-4],marker='*',s=100,color='black',label='Published endpoint; SD unavailable')
    ax.set_yscale('log');ax.set_xticks([0,1],['Corrected B67\n3 seeds, 200k','Published PirateNet\n200k']);ax.set_ylabel('Relative $L^2$ error');ax.legend(fontsize=7);ax.grid(axis='y',alpha=.2)
    export(fig,'three_seed_final_errors')
    # Fields are visual summaries; error statistics remain per-seed, not ensemble errors.
    predictions=np.stack(preds).astype(np.float64)
    absolute_errors=np.abs(predictions-reference[None,:,:])
    mean_prediction=predictions.mean(axis=0)
    mean_absolute_error=absolute_errors.mean(axis=0)
    sd_absolute_error=absolute_errors.std(axis=0,ddof=1)
    np.savez_compressed(OUT/'three_seed_fields.npz',t=tt,x=xx,u_ref=reference,
                        u_pred_by_seed=predictions,u_pred_mean=mean_prediction,
                        absolute_error_mean=mean_absolute_error,absolute_error_sample_sd=sd_absolute_error)
    field_min=min(reference.min(),predictions.min())
    field_max=max(reference.max(),predictions.max())
    error_max=absolute_errors.max()
    fig,axes=plt.subplots(1,3,figsize=(13,3.6),layout='constrained')
    for i,(ax,field,title) in enumerate(zip(axes,[reference,mean_prediction,mean_absolute_error],
            ['Numerical reference','Corrected method 67: mean prediction','Mean absolute error across 3 seeds'])):
        limits=dict(vmin=field_min,vmax=field_max) if i<2 else dict(vmin=0,vmax=error_max)
        im=ax.pcolormesh(tt,xx,field.T,shading='auto',cmap='viridis',rasterized=True,**limits)
        fig.colorbar(im,ax=ax);ax.set(title=title,xlabel='$t$',ylabel='$x$')
    fig.suptitle('Cosine KdV | 200,000 updates per seed; common field scales')
    export(fig,'three_seed_solution_summary')
    fig,axes=plt.subplots(3,3,figsize=(12,9),layout='constrained')
    for row,(seed,pred,error) in enumerate(zip(SEEDS,predictions,absolute_errors)):
        for col,(field,title) in enumerate(zip([reference,pred,error],
                ['Numerical reference',f'Method 67: seed {seed}',f'Absolute error: seed {seed}'])):
            ax=axes[row,col]
            limits=dict(vmin=field_min,vmax=field_max) if col<2 else dict(vmin=0,vmax=error_max)
            im=ax.pcolormesh(tt,xx,field.T,shading='auto',cmap='viridis',rasterized=True,**limits)
            fig.colorbar(im,ax=ax);ax.set(title=title,xlabel='$t$',ylabel='$x$')
    fig.suptitle('All three seeds | same reference and shared color scales across rows')
    export(fig,'per_seed_solution_and_error')
    fig,ax=plt.subplots(figsize=(5.5,3.7),layout='constrained')
    im=ax.pcolormesh(tt,xx,sd_absolute_error.T,shading='auto',cmap='viridis',rasterized=True,vmin=0)
    fig.colorbar(im,ax=ax);ax.set(title='Absolute error: sample SD across 3 seeds',xlabel='$t$',ylabel='$x$')
    export(fig,'three_seed_absolute_error_sd')
    table='\n'.join(f"| {r['seed']} | {r['relative_l2']:.6e} | {r['rmse']:.6e} | {r['first_observed_below_paper_step'] or 'Not observed'} |" for r in rows)
    (OUT/'README.md').write_text(f'''# Corrected winner 67: three-seed results

Each seed trained from fresh weights to exactly 200,000 updates on the cosine KdV test. Identical corrected source, protocol, schedule, batch size, device and PyTorch version; only seed differs. Full per-seed checkpoints and plots remain in their individual folders.

| Seed | Relative L2 | RMSE | First checked step below published error |
|---|---:|---:|---:|
{table}

Relative L2: **{stats['relative_l2']['mean']:.6e} +/- {stats['relative_l2']['sample_sd']:.6e}** (mean +/- sample SD, n=3).
RMSE: **{stats['rmse']['mean']:.6e} +/- {stats['rmse']['sample_sd']:.6e}**.

Sample SD uses denominator n-1. Error bands are computed from individual seed errors, not errors of an ensemble prediction. Intervals with nonpositive mean-SD lower bounds are omitted on the log plot. Published PirateNet is a single 200,000-step marker, with no invented training trajectory or SD. Reference values were diagnostic only. This is replication of a test-informed correction, not untouched-holdout evidence or an equal-FLOP PirateNet experiment.

![Error curves](three_seed_error_curves.png)

![Final errors](three_seed_final_errors.png)

![Reference, mean prediction and mean absolute error](three_seed_solution_summary.png)

The mean-prediction panel is a field visualization only. The error panel averages each seed's absolute error; it is not the absolute error of the mean prediction. The reference is fixed. All field panels use a common field color range, and per-seed error panels share one error scale.

![Reference, prediction and absolute error for each seed](per_seed_solution_and_error.png)

![Sample SD of absolute error](three_seed_absolute_error_sd.png)
''')
    manifest=[dict(path=str(p.relative_to(OUT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256.json']
    (OUT/'SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
