"""Human-locked, reference-free KdV-B experiment runner.

The agent edits only candidate.py among Python sources. Run next trial with:
    python experiment.py
Other commands: status, inspect, smoke, select --trial N --reason TEXT.

Final reference-based assessment lives outside this agent workspace.
"""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import torch

HERE = Path(__file__).resolve().parent
RUNS = HERE / 'runs'
DATA = HERE / 'data/development_cases.csv'
COORDS = HERE / 'data/coordinates.npz'
RECEIPT = HERE / 'data/coordinates_verified.json'
CANDIDATE = HERE / 'candidate.py'
BASELINE = HERE / 'baseline_trial46.py'
TRIALS = 75
EXPLORATION_END = 35
MIN_NOVEL = 15
MIN_ACTIVATION = 5
MIN_OPTIMIZER = 5
BUDGET_SECONDS = 300.0
MAX_STEPS = 200000
BATCH_SIZE = 4096
MAX_PARAMS = 250000
MAX_SNAPSHOTS = 12
IC_TOL = 1e-3
BC_TOL = 1e-3
VAL_CHUNK = 2048
SEED = 1729
BASELINE_SHA256 = 'f17f97beac032bccedf62cec21f9bf2e6835cd5f07215de9a4fe7149d49a444b'
PRE = ['Hypothesis','Proposed method change','Training objective used',
       'Expected effect','Evidence from previous experiments','Literature and novelty assessment']
POST = ['Observed results','Agent decision','Reason for decision']
RESEARCH_CATEGORIES = ('activation','optimizer','other','none')


def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def out_folder(n): return RUNS / f'experiment_{n:03d}'
def dump(path, val):
    path = Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_text(json.dumps(val,indent=2,sort_keys=True,allow_nan=False)+'\n')
    tmp.replace(path)
def read_json(p):return json.loads(Path(p).read_text())
def write_csv(path,rows,fields=None):
    rows=list(rows);path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if fields is None:fields=list(rows[0]) if rows else []
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

def device_choice():
    req=os.environ.get('KDV_DEVICE','auto').lower()
    if req=='auto':req='cuda' if torch.cuda.is_available() else ('mps' if hasattr(torch.backends,'mps') and torch.backends.mps.is_available() else 'cpu')
    if req not in ('cpu','cuda','mps'):raise ValueError('KDV_DEVICE must be auto/cpu/cuda/mps')
    if req=='cuda' and not torch.cuda.is_available():raise ValueError('CUDA unavailable')
    if req=='mps' and not torch.backends.mps.is_available():raise ValueError('MPS unavailable')
    return torch.device(req)
def sync(device):
    if device.type=='cuda':torch.cuda.synchronize(device)
    if device.type=='mps':torch.mps.synchronize()

def coordinates():
    if not COORDS.is_file() or not RECEIPT.is_file():
        raise FileNotFoundError('Run human_only_KdV_B/prepare.py before the first trial; source grid must be verified.')
    receipt=read_json(RECEIPT)
    if receipt.get('coordinates_sha256')!=sha(COORDS):
        raise ValueError('Coordinate file differs from verified preparation receipt')
    with np.load(COORDS,allow_pickle=False) as z:
        if set(z.files)!={'t_star','x_star'}:raise ValueError('Coordinates must not contain reference labels')
        t=np.asarray(z['t_star']).ravel();x=np.asarray(z['x_star']).ravel()
    if len(t)!=201 or len(x)!=512 or not(np.all(np.diff(t)>0) and np.all(np.diff(x)>0)):
        raise ValueError('Expected original KdV 201 x 512 ordered reference grid')
    if not(np.isclose(t[0],0) and np.isclose(t[-1],1) and np.isclose(x[0],-1) and np.isclose(x[-1],1)):
        raise ValueError('Unexpected domain')
    return t.astype('float64'),x.astype('float64')
def cases():
    with DATA.open(newline='') as f:rows=list(csv.DictReader(f))
    if [r['case_id'] for r in rows]!=['dev_01','dev_02','dev_03']:
        raise ValueError('Expected exactly the three original development cases')
    for r in rows:
        r['amplitude_1']=float(r['amplitude_1']);r['amplitude_2']=float(r['amplitude_2'])
        r['frequency_1']=int(r['frequency_1']);r['frequency_2']=int(r['frequency_2'])
    return rows

def initial_condition(x,case):
    return (case['amplitude_1']*torch.cos(math.pi*case['frequency_1']*x)
           +case['amplitude_2']*torch.cos(math.pi*case['frequency_2']*x))
def physics_residual(model,tx):
    tx=tx.detach().clone().requires_grad_(True)
    u=model(tx)
    if u.shape!=(len(tx),1) or not bool(torch.isfinite(u).all()):
        raise ValueError('Model returned invalid output')
    du=torch.autograd.grad(u.sum(),tx,create_graph=True)[0]
    ut,ux=du[:,0:1],du[:,1:2]
    uxx=torch.autograd.grad(ux.sum(),tx,create_graph=True)[0][:,1:2]
    uxxx=torch.autograd.grad(uxx.sum(),tx,create_graph=True)[0][:,1:2]
    return ut+u*ux+0.022**2*uxxx

def physics_components(model,tx,case,x_ic):
    ph=physics_residual(model,tx).square().mean()
    ic_tx=torch.cat((torch.zeros_like(x_ic),x_ic),dim=1)
    ic=(model(ic_tx)-initial_condition(x_ic,case)).square().mean()
    return ph,ic

def period_mismatch(model,t,device,chunk=64):
    totals=[0.,0.,0.];count=0
    for i in range(0,len(t),chunk):
        tt=torch.as_tensor(t[i:i+chunk],dtype=torch.float32,device=device).reshape(-1,1)
        sides=[]
        for x in [-1.,1.]:
            tx=torch.cat((tt,torch.full_like(tt,x)),dim=1).requires_grad_(True)
            u=model(tx)
            ux=torch.autograd.grad(u.sum(),tx,create_graph=True)[0][:,1:2]
            uxx=torch.autograd.grad(ux.sum(),tx,create_graph=True)[0][:,1:2]
            sides.append((u,ux,uxx))
        for j in range(3):totals[j]+=float(((sides[0][j]-sides[1][j])**2).sum().detach())
        count+=len(tt)
    return [z/count for z in totals]

def validate(model,case,t,x,device,chunk=VAL_CHUNK,smoke=False):
    model.eval()
    if smoke:t=t[:2];x=x[:16]
    n=len(t)*len(x);total=0.
    for i in range(0,n,chunk):
        ix=np.arange(i,min(n,i+chunk))
        tx=np.column_stack((t[ix//len(x)],x[ix%len(x)])).astype('float32')
        inp=torch.tensor(tx,device=device)
        total+=float(physics_residual(model,inp).detach().square().sum())
    xx=torch.tensor(x.astype('float32'),device=device).reshape(-1,1)
    with torch.no_grad():
        ic=float(((model(torch.cat((torch.zeros_like(xx),xx),dim=1))-initial_condition(xx,case))**2).mean())
    bc=period_mismatch(model,t,device)
    return dict(val_physics=total/n,val_ic=ic,val_full=total/n+ic,
                val_bc_u=bc[0],val_bc_ux=bc[1],val_bc_uxx=bc[2],val_bc_total=sum(bc),
                validation_grid_points=n,ic_points=len(x))

def load_candidate(path):
    spec=importlib.util.spec_from_file_location('kdv_b_candidate_'+sha(path)[:12],path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    if not callable(getattr(mod,'build_model',None)) or not callable(getattr(mod,'train_model',None)):
        raise ValueError('candidate.py needs build_model(case) and train_model(model,case,train_t,context)')
    return mod

def state_cpu(model):return {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
class TrainingBatchStream:
    def __init__(self,device,seed,batch_size=BATCH_SIZE):
        self.device=device;self.batch_size=batch_size;self.count=0
        self.generator=torch.Generator(device=device.type if device.type in ('cpu','cuda') else 'cpu').manual_seed(seed)
    def next(self):
        self.count+=1
        pts=torch.rand((self.batch_size,2),generator=self.generator,device=self.device if self.device.type!='mps' else 'cpu')
        pts[:,1]=pts[:,1]*2-1
        return pts.to(self.device)
class TrainingContext:
    def __init__(self,model,device,x_ic,case,seconds=BUDGET_SECONDS,max_steps=MAX_STEPS):
        self.model=model;self.device=device;self.x_ic=x_ic;self.case=case
        self.start=time.monotonic();self.seconds=float(seconds);self.deadline=self.start+self.seconds
        self.max_steps=int(max_steps);self.steps=0;self.snapshots=[]
    def remaining_seconds(self):return max(0.,self.deadline-time.monotonic())
    def should_stop(self):return time.monotonic()>=self.deadline or self.steps>=self.max_steps
    def physics_components(self,model,tx,case):return physics_components(model,tx,case,self.x_ic)
    def optimizer_step(self,opt,closure=None):
        if self.should_stop():raise TimeoutError('Budget reached')
        r=opt.step(closure) if closure is not None else opt.step();self.steps+=1;return r
    def record(self,step,train_loss,note=''):
        if len(self.snapshots)>=MAX_SNAPSHOTS:raise ValueError('Maximum 12 snapshots')
        sync(self.device)
        if not math.isfinite(float(train_loss)):raise ValueError('Nonfinite loss')
        self.snapshots.append(dict(step=int(step),reported_train_objective=float(train_loss),
            time_seconds=time.monotonic()-self.start,note=str(note)[:150],state=state_cpu(self.model)))

def worker(candidate,case,out,seed,smoke=False):
    torch.set_num_threads(max(1,min(4,torch.get_num_threads())))
    random.seed(seed);np.random.seed(seed%(2**32-1));torch.manual_seed(seed)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(seed)
    t,x=coordinates();device=device_choice();mod=load_candidate(candidate)
    model=mod.build_model(case).to(device=device,dtype=torch.float32)
    nparams=sum(p.numel() for p in model.parameters() if p.requires_grad)
    if not 1<=nparams<=MAX_PARAMS:raise ValueError(f'Parameter count {nparams} outside [1,{MAX_PARAMS}]')
    x_ic=torch.tensor(x.astype('float32'),device=device).reshape(-1,1)
    stream=TrainingBatchStream(device,seed+101,batch_size=16 if smoke else BATCH_SIZE)
    ctx=TrainingContext(model,device,x_ic,case,seconds=25 if smoke else BUDGET_SECONDS,
                        max_steps=2 if smoke else MAX_STEPS)
    model.train();mod.train_model(model,case,stream,ctx);sync(device)
    elapsed=time.monotonic()-ctx.start
    if elapsed>ctx.seconds+3:raise TimeoutError(f'Candidate took {elapsed:.2f}s > {ctx.seconds+3:.2f}s')
    if not (1 if smoke else 2)<=len(ctx.snapshots)<=MAX_SNAPSHOTS:raise ValueError('Need 2-12 snapshots per case')
    if not 1<=ctx.steps<=ctx.max_steps:raise ValueError('No counted optimizer steps, or step cap exceeded')
    final_state=state_cpu(model);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/'snapshots').mkdir(exist_ok=True);(out/'checkpoints').mkdir(exist_ok=True)
    history=[];best=None;cid=case['case_id']
    for i,snap in enumerate(ctx.snapshots,1):
        model.load_state_dict(snap['state']);v=validate(model,case,t,x,device,smoke=smoke)
        history.append(dict(step=snap['step'],time_seconds=snap['time_seconds'],
                            reported_train_objective=snap['reported_train_objective'],**v))
        torch.save(dict(state_dict=snap['state'],step=snap['step'],training_seconds=snap['time_seconds']),
                   out/'snapshots'/f'{cid}_step_{snap["step"]:06d}_{i:02d}.pt')
        if best is None or v['val_full']<best[0]['val_full']:best=(v,snap)
    model.load_state_dict(final_state)
    final=validate(model,case,t,x,device,smoke=smoke)
    model_hash=sha(candidate)
    for kind,state,val,step in [('final',final_state,final,ctx.steps),
                                ('best',best[1]['state'],best[0],best[1]['step'])]:
        torch.save(dict(state_dict=state,case=case,candidate_sha256=model_hash,seed=seed,
                        kind=kind,validation=val,training_seconds=elapsed,step=step),
                   out/'checkpoints'/f'{cid}_{kind}.pt')
    write_csv(out/f'history_{cid}.csv',history)
    # Agent receives predicted fields but never reference values.
    with torch.no_grad():
        pred=[]
        for i in range(0,len(t)*len(x),8192):
            ix=np.arange(i,min(i+8192,len(t)*len(x)))
            tx=np.column_stack((t[ix//len(x)],x[ix%len(x)])).astype('float32')
            pred.append(model(torch.tensor(tx,device=device)).detach().cpu().numpy().ravel())
    pred=np.concatenate(pred).reshape(len(t),len(x))
    np.savez_compressed(out/f'predictions_{cid}.npz',t=t,x=x,u_pred=pred)
    figs=out/'plots'/cid;figs.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(7,3.5));im=ax.pcolormesh(t,x,pred.T,shading='auto')
    fig.colorbar(im,ax=ax);ax.set(xlabel='t',ylabel='x',title=f'{cid}: prediction, unlabeled')
    fig.tight_layout();fig.savefig(figs/'u_prediction.png',dpi=120);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,3.5))
    ax.semilogy([z['step'] for z in history],[max(z['val_full'],1e-15) for z in history],label='Val total')
    ax.semilogy([z['step'] for z in history],[max(z['val_physics'],1e-15) for z in history],label='PDE MSE')
    ax.set(xlabel='Optimizer steps',ylabel='Reference-free loss');ax.legend()
    fig.tight_layout();fig.savefig(figs/'loss_curve.png',dpi=120);plt.close(fig)
    metrics=dict(case_id=cid,val_total=final['val_full'],val_physics=final['val_physics'],
                 val_ic=final['val_ic'],val_bc_total=final['val_bc_total'],
                 val_bc_u=final['val_bc_u'],val_bc_ux=final['val_bc_ux'],val_bc_uxx=final['val_bc_uxx'],
                 params=nparams,train_seconds=elapsed,optimizer_steps=ctx.steps,training_batches=stream.count,
                 seed=seed,device=str(device),scored_checkpoint='final',
                 best_posthoc_val_total=best[0]['val_full'])
    dump(out/f'metrics_{cid}.json',metrics)
    return metrics

def sections_complete(doc,heads):
    for h in heads:
        m=re.search(r'^## '+re.escape(h)+r'\s*\n(.*?)(?=^## |\Z)',doc,re.M|re.S)
        if not m or len(m.group(1).strip())<20 or '[FILL' in m.group(1):return False
    return True

def research_record(n):
    p=out_folder(n)/'research_record.json'
    if not p.exists():raise FileNotFoundError(f'Create {p} before running the experiment')
    d=read_json(p)
    if d.get('trial')!=n:raise ValueError('research_record.json trial mismatch')
    category=d.get('category')
    if category not in RESEARCH_CATEGORIES:raise ValueError('category must be activation/optimizer/other/none')
    claimed=d.get('novelty_credit')
    if type(claimed) is not bool:raise ValueError('novelty_credit must be Boolean')
    if not isinstance(d.get('hypothesis'),str) or len(d['hypothesis'])<30:raise ValueError('Write a substantive hypothesis')
    if not isinstance(d.get('change_summary'),str) or len(d['change_summary'])<20:raise ValueError('Write a clear method change')
    priority=d.get('exploration_priority')
    if not isinstance(priority,dict):
        raise ValueError('Provide exploration_priority with four integer components')
    ranges={'novelty':3,'literature':2,'information_gain':2,'feasibility':2}
    for key,maximum in ranges.items():
        value=priority.get(key)
        if type(value) is not int or not 0<=value<=maximum:
            raise ValueError(f'exploration_priority.{key} must be an integer 0..{maximum}')
    if claimed and priority['novelty']<2:
        raise ValueError('Novelty credit requires a genuinely different mechanism (priority novelty >= 2)')
    if not claimed and priority['novelty']>1:
        raise ValueError('High novelty priority needs a credited substantive novelty record')
    if claimed:
        if category=='none':raise ValueError('Novelty cannot use category none')
        if not isinstance(d.get('novelty_key'),str) or len(d['novelty_key'].strip())<5:
            raise ValueError('Provide a specific novelty_key for a distinct method, not a hyperparameter tweak')
        urls=d.get('source_urls',[])
        if not isinstance(urls,list) or not urls or not all(isinstance(v,str) and v.startswith(('https://','http://')) for v in urls):
            raise ValueError('A literature-based novelty test needs real source URLs')
        if not isinstance(d.get('distinctness_rationale'),str) or len(d['distinctness_rationale'])<40:
            raise ValueError('Explain why this is a genuinely different method')
    else:
        if category=='none':pass
    return d

def novelty_counts(before):
    seen=set();counts=dict(novel=0,activation=0,optimizer=0,other=0)
    for n in range(1,min(before,EXPLORATION_END+1)):
        p=out_folder(n)
        state=p/'status.json'
        if not state.exists():continue
        status=read_json(state).get('status')
        # A crash before completing all three cases is recorded as an attempted
        # experiment, but cannot earn quota credit for a full comparison.
        if status != 'completed':continue
        rec=research_record(n)
        if rec['novelty_credit']:
            key=rec['novelty_key'].strip().lower()
            if key in seen:raise ValueError(f'Duplicate novelty key on trial {n}: {key}')
            seen.add(key)
            counts['novel']+=1;counts[rec['category']]+=1
    return counts

def quota_status(n,proposed):
    counts=novelty_counts(n)
    if n<=EXPLORATION_END and proposed['novelty_credit']:
        key=proposed['novelty_key'].strip().lower()
        keys={read_json(out_folder(k)/'research_record.json')['novelty_key'].strip().lower()
              for k in range(1,n) if (out_folder(k)/'status.json').exists()
              and read_json(out_folder(k)/'status.json')['status']=='completed'
              and read_json(out_folder(k)/'research_record.json').get('novelty_credit')}
        if key in keys:raise ValueError('Novelty_key already used: distinct method required')
        if sha(CANDIDATE)==BASELINE_SHA256 and n>1:raise ValueError('Novelty claimed but candidate still matches baseline')
        counts['novel']+=1;counts[proposed['category']]+=1
    if n==1 and sha(CANDIDATE)!=BASELINE_SHA256:
        raise ValueError('Trial 001 must run the exact original trial-46 source (SHA mismatch)')
    if n==1 and proposed['novelty_credit']:
        raise ValueError('Baseline confirmation cannot claim novelty')
    if n<=EXPLORATION_END:
        remaining=EXPLORATION_END-n
        deficits=[max(0,MIN_NOVEL-counts['novel']),
                  max(0,MIN_ACTIVATION-counts['activation'])+max(0,MIN_OPTIMIZER-counts['optimizer'])]
        if max(deficits)>remaining:
            raise ValueError(f'This trial would make exploration quota impossible; counts={counts}, remaining={remaining}')
    if n==EXPLORATION_END and (counts['novel']<MIN_NOVEL or counts['activation']<MIN_ACTIVATION or counts['optimizer']<MIN_OPTIMIZER):
        raise ValueError('Novelty quota unmet at trial 35')
    if n>EXPLORATION_END and (counts['novel']<MIN_NOVEL or counts['activation']<MIN_ACTIVATION or counts['optimizer']<MIN_OPTIMIZER):
        raise ValueError('Cannot enter trial 036+: required first-35 COMPLETED novelty quota was not met')
    return counts

def protocol():
    return dict(experiment_sha256=sha(HERE/'experiment.py'),development_cases_sha256=sha(DATA),
                coordinates_sha256=sha(COORDS),requirements_sha256=sha(HERE/'requirements.txt'),
                baseline_sha256=sha(BASELINE),budget_seconds=BUDGET_SECONDS,
                max_optimizer_steps=MAX_STEPS,max_params=MAX_PARAMS,batch_size=BATCH_SIZE,
                trials=TRIALS,device=str(device_choice()),seed=SEED)
def next_trial():
    for n in range(1,TRIALS+1):
        p=out_folder(n)/'status.json'
        if not p.exists():
            if n>1:
                prev=out_folder(n-1)/'decision.md'
                if not prev.exists() or not sections_complete(prev.read_text(),POST):
                    raise RuntimeError('Previous trial needs complete post-run decision.md')
            return n
        if read_json(p).get('status') not in ('completed','failed'):
            raise RuntimeError(f'Trial {n} incomplete; inspect before proceeding')
    raise RuntimeError('All 75 attempts have finished; use select')
def refresh_results():
    rows=[]
    for n in range(1,TRIALS+1):
        folder=out_folder(n);p=folder/'status.json'
        if not p.exists():continue
        status=read_json(p)['status']
        if status not in ('completed','failed'):continue
        s=read_json(folder/'summary.json') if (folder/'summary.json').exists() else {}
        rec=research_record(n)
        rows.append(dict(trial=n,method_lineage=f'prior_50_plus_B_{n:03d}',status=status,
                         novelty_credit=rec['novelty_credit'],category=rec['category'],
                         novelty_key=rec.get('novelty_key',''),mean_validation_loss=s.get('mean_validation_loss',''),
                         worst_validation_loss=s.get('worst_validation_loss',''),
                         mean_ic_loss=s.get('mean_ic_loss',''),mean_bc_loss=s.get('mean_bc_loss',''),
                         params=s.get('params',''),eligible=s.get('eligible','')))
    write_csv(HERE/'results.csv',rows,['trial','method_lineage','status','novelty_credit','category','novelty_key',
                                     'mean_validation_loss','worst_validation_loss','mean_ic_loss','mean_bc_loss','params','eligible'])

def run_next():
    if sha(BASELINE)!=BASELINE_SHA256:raise ValueError('Baseline file modified; restore exact winner source')
    coordinates();n=next_trial();folder=out_folder(n)
    decision=folder/'decision.md'
    if not decision.exists() or not sections_complete(decision.read_text(),PRE):
        raise RuntimeError('Agent must write the six substantive pre-run decision sections in decision.md')
    proposed=research_record(n);novelty=quota_status(n,proposed)
    if not (HERE/'research_log.md').exists() or not (HERE/'internet_use.md').exists():
        raise FileNotFoundError('Keep both research_log.md and internet_use.md')
    if n>1 and protocol()!=read_json(out_folder(1)/'protocol.json'):
        raise ValueError('Locked protocol has changed from Trial 001')
    if n==1 and folder.exists() and any(q.name not in ('decision.md','research_record.json') for q in folder.iterdir()):
        raise ValueError('Trial 001 folder contains unexpected outputs')
    folder.mkdir(parents=True,exist_ok=True)
    dump(folder/'protocol.json',protocol())
    shutil.copy2(CANDIDATE,folder/'candidate.py')
    dump(folder/'status.json',dict(trial=n,status='running',started=now(),candidate_sha256=sha(CANDIDATE),novelty_counts=novelty))
    results=[]
    try:
        for idx,case in enumerate(cases()):
            print(f'Trial {n:03d} | {case["case_id"]} ({idx+1}/3)',flush=True)
            cmd=[sys.executable,str(HERE/'experiment.py'),'_worker','--candidate',str(folder/'candidate.py'),
                 '--case-json',json.dumps(case),'--out',str(folder),'--seed',str(SEED+97*idx)]
            done=subprocess.run(cmd,capture_output=True,text=True,timeout=BUDGET_SECONDS+300)
            with (folder/'run.log').open('a') as f:f.write(f'\n### {case["case_id"]} exit {done.returncode}\n'+done.stdout+'\n'+done.stderr)
            if done.returncode:raise RuntimeError(f'Case {case["case_id"]} failed: {done.stderr[-2500:]}')
            row=read_json(folder/f'metrics_{case["case_id"]}.json')
            results.append(row);write_csv(folder/'metrics_partial.csv',results)
            print(f"val={row['val_total']:.6g}; IC={row['val_ic']:.6g}; BC={row['val_bc_total']:.6g}",flush=True)
        write_csv(folder/'metrics.csv',results)
        vals=[r['val_total'] for r in results]
        summ=dict(trial=n,mean_validation_loss=float(np.mean(vals)),worst_validation_loss=max(vals),
                  std_validation_loss=float(np.std(vals,ddof=1)),
                  mean_ic_loss=float(np.mean([r['val_ic'] for r in results])),
                  mean_bc_loss=float(np.mean([r['val_bc_total'] for r in results])),
                  ic_eligible=all(r['val_ic']<=IC_TOL for r in results),
                  periodic_eligible=all(r['val_bc_total']<=BC_TOL for r in results),
                  params=results[0]['params'],total_training_seconds=sum(r['train_seconds'] for r in results),
                  selection='Agent chooses from reference-free evidence; novelty is not a score',
                  official_checkpoint='final',per_case={r['case_id']:r for r in results})
        summ['eligible']=summ['ic_eligible'] and summ['periodic_eligible']
        dump(folder/'summary.json',summ);dump(folder/'status.json',dict(trial=n,status='completed',ended=now()))
        print(json.dumps(summ,indent=2))
    except Exception as exc:
        dump(folder/'status.json',dict(trial=n,status='failed',error=str(exc),ended=now()))
        with (folder/'run.log').open('a') as f:f.write('\nFAILURE: '+str(exc)+'\n')
        raise
    finally:refresh_results()

def select(n,reason):
    if len(reason.strip())<40:raise ValueError('Selection rationale needs at least 40 characters')
    if (RUNS/'final_selection.json').exists():raise FileExistsError('Selection already frozen')
    for k in range(1,TRIALS+1):
        p=out_folder(k)
        if not (p/'status.json').exists() or read_json(p/'status.json')['status'] not in ('completed','failed'):
            raise RuntimeError('Finish all 75 attempts before selecting')
        if not sections_complete((p/'decision.md').read_text(),PRE+POST):
            raise RuntimeError(f'Incomplete decision.md in trial {k}')
    counts=novelty_counts(EXPLORATION_END+1)
    if counts['novel']<MIN_NOVEL or counts['activation']<MIN_ACTIVATION or counts['optimizer']<MIN_OPTIMIZER:
        raise ValueError('Required early-stage novelty quota not met')
    folder=out_folder(n)
    if read_json(folder/'status.json')['status']!='completed':raise ValueError('Winner not completed')
    summ=read_json(folder/'summary.json')
    if not summ['eligible']:raise ValueError('Winner fails fixed IC or periodicity eligibility')
    source=folder/'candidate.py';destination=RUNS/'selected_candidate.py'
    if destination.exists():raise FileExistsError('selected_candidate already exists')
    shutil.copy2(source,destination)
    ckp=RUNS/'selected_checkpoints';ckp.mkdir(exist_ok=False)
    for case in cases():
        for suffix in ('final','best'):
            name=f"{case['case_id']}_{suffix}.pt";shutil.copy2(folder/'checkpoints'/name,ckp/name)
    dump(RUNS/'final_selection.json',dict(selected_trial=n,origin='B continuation after prior 50',
          frozen_at=now(),reason=reason,novelty_counts=counts,selected_candidate_sha256=sha(source),
          baseline_candidate_sha256=BASELINE_SHA256,summary=summ,protocol=protocol()))
    print('Frozen B winner',n)

def inspect():
    t,x=coordinates()
    print(json.dumps(dict(trials=TRIALS,training_seconds_per_case=BUDGET_SECONDS,
        development_cases=[z['case_id'] for z in cases()],seeds_per_case=1,device=str(device_choice()),
        max_params=MAX_PARAMS,reference_labels_present=False,coordinates=[len(t),len(x)],
        first_35_novelty_min=MIN_NOVEL,activation_min=MIN_ACTIVATION,optimizer_min=MIN_OPTIMIZER),indent=2))
def smoke():
    out=RUNS/'_smoke';out.mkdir(parents=True,exist_ok=True)
    print(json.dumps(worker(BASELINE,cases()[0],out,SEED,smoke=True),indent=2))
def status():
    refresh_results();s=[]
    for n in range(1,TRIALS+1):
        p=out_folder(n)/'status.json'
        if p.exists():s.append((n,read_json(p)['status']))
    print('Attempts:',len(s),'/',TRIALS,'Latest:',s[-3:]);print('Early novelty:',novelty_counts(EXPLORATION_END+1))
    print('Final selection:',(RUNS/'final_selection.json').exists())

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='command')
    for cmd in ('inspect','smoke','status'):sub.add_parser(cmd)
    sel=sub.add_parser('select');sel.add_argument('--trial',type=int,required=True)
    sel.add_argument('--reason',required=True)
    worker_parser=sub.add_parser('_worker');worker_parser.add_argument('--candidate',required=True)
    worker_parser.add_argument('--case-json',required=True);worker_parser.add_argument('--out',required=True)
    worker_parser.add_argument('--seed',type=int,required=True)
    a=ap.parse_args()
    if a.command is None:run_next()
    elif a.command=='inspect':inspect()
    elif a.command=='smoke':smoke()
    elif a.command=='status':status()
    elif a.command=='select':select(a.trial,a.reason)
    elif a.command=='_worker':print(json.dumps(worker(Path(a.candidate),json.loads(a.case_json),Path(a.out),a.seed)))
if __name__=='__main__':main()
