# Trial 015

Research metadata (locked on preparation): research_area=optimisation; parents=trial:13; kind=mechanism; mechanism_id=extragradient_predictor_corrector.

## Parent methods and evidence

Closed Trial013 source retains P model,SGD lr.01 and full-pool PR+; total.2110811079,physics.0666888350,IC.1443922729. Trial014 task-wise conditioning scored.2255088716. Best011 total.1678472594 remains ranking target. Test descent predictor/corrector in place of task-gradient surgery,using summed objective rather than normalising task directions. No trained states,weights or checkpoints reused. This is the fifteenth distinct initial optimisation mechanism; next block changes representations.

## Novelty claim

Known extragradient predictor-corrector methodology,attributed to Korpelevich and reviewed in primary Gorbunov,Loizou,Gidel https://arxiv.org/html/2110.04261 . Standard unconstrained recurrence predictor=theta-eta*gradientF(theta),corrector=theta-eta*gradientF(predictor). Here F is the sampled scalar PINN loss gradient,using the same batch twice. Distinct from SAM adverse ascent (012) and ConFIG gradient geometry(013),not a scalar-only optimizer change. No claim of global novelty or applicability of monotone variational-inequality convergence theorems to nonconvex stochastic Euler-Poisson PINNs.

## Hypothesis and proposed change

Hypothesis: a second gradient after a descent prediction stabilises rapidly changing directions and improves total score below011. Both predictor and corrector eta=.01,plain SGD,no momentum,decay or clipping. Compute full summed-loss gradient at base;save exact base;temporarily set weights=base-.01*g;clear gradients;compute second gradient on identical stored coordinates/targets;finally restore exact base;SGD uses second gradient from that base. Never step from the predictor. Require8s before second pass;deadline interruption restores without corrector,other errors restore then propagate. Synthetic CPU/native MPS anisotropic quadratic formula and exact interruption rollback passed;model/full-PR AST and mathematical entire full-phase equality passed. No PINN training or coordinate sampling in checks. Risks: two-pass cost,unpreconditioned stiffness,SGD step scale and nonconvex/stochastic bias may dominate any stability benefit.

## Training objective and setup

Fresh unchanged P sine model,seven Linear,width128,85765 parameters,three spatial harmonics,Xavier/bias.01,density startup.05. F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE components weight1. First80% of750s: extraSGD predictor/corrector eta.01 above,1024PDE/1024IC replacement pool batches,reused for both passes. Controlled initial batch choice,not a total cap. Last phase caches all100000PDE/75000IC once via cycle,25 separately weighted microbatches max4096PDE/3072IC for every complete gradient/value. Same PR+ descent restart,Armijo c1=1e-4,up to4 halved proposals,alpha seed rules,>12s attempt reserve/4s chunk/8s proposal checks and exact last-accepted rollback. All copy/sampling/backward/search overhead within750s. Return SGD state,step,CG and predictor counts;log actual draws,repeated point evaluations,EG probes,CG/search/restarts/nonfinite counts. Frozen coordinates only,no new/perturbed locations,validation/reference access or updates after checkpoint.

## Expected outcome

Expect finite L_val below.1678472594,with enough IC recovery over013 and physics preservation for net gain. A higher total falsifies net hypothesis regardless of any component/training loss/throughput improvement. Read all metrics/windows/IC/density/mass/periodicity/history/metadata/log and reconcile two initial evaluations per completed step plus any interrupted first pass and repeated full-pool work. Only finite total ranks,no IC/physical gates. One local matched-time run cannot establish statistical significance,general extraSGD advantage or trajectory accuracy;negative results and failures retained,no ID rerun.

## Observed results

Execution failed, worker returncode1: FloatingPointError: Nonfinite residual in canonical physics_components. Traceback points to candidate line155, second/probe evaluate_chunk during initial extragradient stage. Exact-base finally rollback is in frozen source; the process aborted without checkpoint scoring. Started2026-11-11T01:07:47.970839+00:00,finished01:08:13.070605+00:00,about25.10seconds worker wall time (not an actual training-duration measurement). No metrics.json,run_metadata.json or history.json was produced; validation loss,PDE/IC diagnostics,steps and point counts are unavailable and are not invented. Full exposed status/log:

```json
{
  "trial": 15,
  "state": "failed",
  "parents": "trial:13",
  "kind": "mechanism",
  "research_area": "optimisation",
  "mechanism_id": "extragradient_predictor_corrector",
  "created_at": "2026-11-11T01:07:13.166321+00:00",
  "started": "2026-11-11T01:07:47.970839+00:00",
  "returncode": 1,
  "finished": "2026-11-11T01:08:13.070605+00:00"
}
```

```text

== 2026-11-11T01:07:47.980678+00:00 starting ==
Traceback (most recent call last):
  File "/Users/user/Desktop/CC_PINN_3D_Supersonic_Novelty50/engine/experiment.py", line 588, in <module>
    main()
    ~~~~^^
  File "/Users/user/Desktop/CC_PINN_3D_Supersonic_Novelty50/engine/experiment.py", line 583, in main
    train_worker(Path(a.source),Path(a.out),float(a.seconds),Path(a.train_data),
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 Path(a.validation_data),a.seed,a.quick,a.training_seed)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/user/Desktop/CC_PINN_3D_Supersonic_Novelty50/engine/experiment.py", line 113, in train_worker
    state = method.train_model(model, dict(case), train['train_domain'], train['train_ic'], ctx, resume=None)
  File "/Users/user/Desktop/CC_PINN_3D_Supersonic_Novelty50/agent_workspace/runs/experiment_015/candidate.py", line 155, in train_model
    last = evaluate_chunk(q, ic, targets, 1., 1., True)
  File "/Users/user/Desktop/CC_PINN_3D_Supersonic_Novelty50/agent_workspace/runs/experiment_015/candidate.py", line 130, in evaluate_chunk
    parts = context.physics_components(model, q, ic, case, ic_targets=targets)
  File "/Users/user/Desktop/CC_PINN_3D_Supersonic_Novelty50/engine/core.py", line 318, in physics_components
    return physics_components(model, q, ic_q, targets, case)
  File "/Users/user/Desktop/CC_PINN_3D_Supersonic_Novelty50/engine/core.py", line 181, in physics_components
    raise FloatingPointError('Nonfinite residual')
FloatingPointError: Nonfinite residual

```

## Decision and interpretation

Count this as failed attempt015,do not rerun this ID or modify frozen source. No finite score exists,so it cannot enter ranking. The unpreconditioned lr.01 probe encountered a nonfinite residual; synthetic arithmetic correctness did not establish PINN numerical stability. No evidence isolates exact completed step count or a general extragradient disadvantage. The net hypothesis was not demonstrated. Next block uses best finite011 and changes activations; no fix/retrain hidden under015.
