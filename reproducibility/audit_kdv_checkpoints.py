#!/usr/bin/env python3
"""Optional CPU-only independent checkpoint inference. Requires original kdv.mat."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
import numpy as np
from scipy.io import loadmat
import torch
ROOT=Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--reference',type=Path,required=True);args=parser.parse_args()
 expected='0df03aee69597c8913f7120324303f663db617be3789b9ff35beb29303b1c087'
 assert hashlib.sha256(args.reference.read_bytes()).hexdigest()==expected,'Unexpected reference bytes'
 d=loadmat(args.reference);ref=d['usol'];t=d['t'].ravel();x=d['x'].ravel();assert ref.shape==(201,512)
 source=ROOT/'methods/source_snapshots/kdv067_corrected.py'
 assert hashlib.sha256(source.read_bytes()).hexdigest()=='94ce8f7fa29dbb035192bad0efa65f841db89884cf408d456b21433337a60d2a'
 spec=importlib.util.spec_from_file_location('frozen_kdv',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 case=dict(case_id='test_01',amplitude_1=1.,frequency_1=1,amplitude_2=0.,frequency_2=0)
 torch.set_num_threads(4)
 # Explicit safe globals for the RNG metadata and version in these source checkpoints.
 torch.serialization.add_safe_globals([np._core.multiarray._reconstruct,np.ndarray,np.dtype,np.dtypes.UInt32DType,torch.torch_version.TorchVersion])
 tt,xx=np.meshgrid(t,x,indexing='ij');coords=torch.from_numpy(np.stack([tt.ravel(),xx.ravel()],axis=1)).float()
 audit=json.loads((ROOT/'experiments/kdv/evidence/corrected_three_seeds/curation_checkpoint_verification.json').read_text())
 result=[]
 for row in audit['runs']:
  seed=row['seed'];p=ROOT/f'experiments/kdv/evidence/corrected_three_seeds/seed_{seed}/final.pt'
  assert hashlib.sha256(p.read_bytes()).hexdigest()==row['checkpoint_sha256']
  state=torch.load(p,map_location='cpu',weights_only=True);assert state['step']==200000
  assert {int(v['step']) for v in state['optimizer_state']['state'].values()}=={200000}
  model=mod.build_model(case).eval();model.load_state_dict(state['state_dict'])
  with torch.inference_mode():pred=np.concatenate([model(q).numpy().ravel() for q in coords.split(2048)]).reshape(ref.shape)
  rel=float(np.linalg.norm(pred.astype(float)-ref)/np.linalg.norm(ref))
  # CPU/library kernels can vary slightly. This checks consistency, not bitwise identity.
  assert abs(rel-row['saved_prediction_relative_l2'])<1e-7
  result.append({'seed':seed,'cpu_reload_relative_l2':rel,'saved_MPS_relative_l2':row['saved_prediction_relative_l2']})
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
