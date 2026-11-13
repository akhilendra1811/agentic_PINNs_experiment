#!/usr/bin/env python3
"""Validate curated source hashes, local links and aggregate metrics; no training."""
from pathlib import Path
import csv,hashlib,json,math,re,statistics,sys
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
def near(a,b):assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-13),(a,b)
def rows(path):
 with (ROOT/path).open(newline='') as f:return list(csv.DictReader(f))
def main():
 manifest=read('reproducibility/provenance.json')
 for item in manifest:
  p=ROOT/item['file'];assert p.is_file(),p
  assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],p
  assert p.stat().st_size==item['bytes'],p
 # Verify portable curated Markdown. Verbatim historical evidence is checked by hash instead.
 broken=[]
 for p in ROOT.rglob('*.md'):
  if '/evidence/' in str(p) or '/decisions/' in str(p):continue
  for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   if re.match(r'^[a-zA-Z]+:',target) or target.startswith('#'):continue
   dest=(p.parent/unquote(target.split('#')[0])).resolve()
   if not dest.exists():broken.append((str(p.relative_to(ROOT)),target))
 assert not broken,broken
 bench=read('experiments/sitnikov/evidence/benchmark_comparison.json')
 baseline=bench[0];winner=next(x for x in bench if '049' in x['trial'])
 for entry in [baseline,winner]:
  assert len(entry['per_case'])==10
  for field in ['z_rmse','v_rmse']:near(statistics.mean(x[field] for x in entry['per_case']),entry['mean_'+field])
 sit={f:100*(1-winner['mean_'+f]/baseline['mean_'+f]) for f in ['z_rmse','v_rmse']}
 krows=rows('experiments/kdv/evidence/corrected_three_seeds/per_seed_metrics.csv')
 assert [int(x['seed']) for x in krows]==[99417,99418,99419]
 assert all(int(x['steps'])==200000 for x in krows)
 kvals=[float(x['relative_l2']) for x in krows];ks=read('experiments/kdv/evidence/corrected_three_seeds/summary.json')['statistics']['relative_l2']
 near(statistics.mean(kvals),ks['mean']);near(statistics.stdev(kvals),ks['sample_sd'])
 kaudit=read('experiments/kdv/evidence/corrected_three_seeds/curation_checkpoint_verification.json')
 for row,expected in zip(kaudit['runs'],kvals):
  near(row['saved_prediction_relative_l2'],expected);assert row['grid_points']==201*512 and row['step']==200000
  seed=row['seed'];p=ROOT/f'experiments/kdv/evidence/corrected_three_seeds/seed_{seed}/final.pt'
  assert hashlib.sha256(p.read_bytes()).hexdigest()==row['checkpoint_sha256']
  assert row['cpu_prediction_max_abs_difference']<1e-5
 original=read('experiments/kdv/evidence/historical_200k/summary.json');assert original['step']==200000
 euler={}
 for regime,seeds in [('supersonic',[419,733,947]),('subsonic',[9,38])]:
  vals={m:[] for m in ['trial_069','paper_P']}
  for seed in seeds:
   for model in vals:
    v=read(f'experiments/euler069/evidence/{regime}/seed_{seed}/{model}/full_volume_256.json')
    assert v['cells']==256**3 and v['time']==0.8;vals[model].append(v['density_rms_delta'])
  means={m:statistics.mean(v) for m,v in vals.items()};means['reduction_percent']=100*(1-means['trial_069']/means['paper_P']);euler[regime]=means
 ext=read('experiments/euler056/evidence/extended_summary.json');new={}
 for model in ['P','selected']:
  modelvals={field:[] for field in ['density_relative_l2','density_rms_log2_ratio','velocity_vector_relative_l2']}
  for rng in [823001,823002,823003]:
   v=read(f'experiments/euler056/evidence/rng_{rng}/{model}/full_grid_metrics.json')
   assert v['grid']==[256]*3 and v['time']==0.8 and v['groups']['all']['n_cells']==256**3
   for field in modelvals:modelvals[field].append(v['groups']['all'][field])
  for field,vals in modelvals.items():
   near(statistics.mean(vals),ext[model]['all'][field]['mean']);near(statistics.stdev(vals),ext[model]['all'][field]['sample_sd'])
  new[model]={f:{'mean':statistics.mean(v),'sample_sd':statistics.stdev(v)} for f,v in modelvals.items()}
 selection=read('experiments/euler056/evidence/final_selection.json');scores=selection['all_matched_1800_second_scores']
 assert min(scores,key=scores.get)==selection['selected_method']=='trial_056'
 closure=read('experiments/euler056/evidence/search_closure_audit.json');assert closure['closed_attempts']==60 and closure['finite']==58 and len(closure['failures'])==2
 report={'source_files_hash_verified':len(manifest),'curated_markdown_targets':'pass','sitnikov_reduction_percent':sit,'kdv_three_run_relative_l2':ks,'published_piratenet_over_kdv_mean':0.000427/ks['mean'],'euler069_density_rms_log2':euler,'euler056_extended':new,'new_final_selection':'trial_056','scope':'Saved-file arithmetic and provenance; fresh CPU KdV inference is recorded separately. No training or numerical reference simulation.'}
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
