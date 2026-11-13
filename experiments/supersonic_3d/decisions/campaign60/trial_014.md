# Trial 014

Research metadata (locked on preparation): research_area=optimisation; parents=trial:13; kind=mechanism; mechanism_id=multiadam_taskwise_moments.

## Parent methods and evidence

Closed Trial013 source parent for same two tasks/model/full-pool finish: total0.2110811079,physics0.0666888350,IC MSE0.1443922729,24305/31853 pairs conflicted. Lowest finite Trial011 remains0.1678472594 (physics0.0725275773,IC0.0953196821). ConFIG reduced physics but IC deteriorated; test per-coordinate task conditioning instead of common-direction SGD. No trained parent weights,checkpoints or state reused.

## Novelty claim

Distinct known optimisation mechanism MultiAdam task-wise moments, credited Yao et al., https://proceedings.mlr.press/v202/yao23c.html and full Algorithm2 https://proceedings.mlr.press/v202/yao23c/yao23c.pdf . Separate first/second moments and bias corrections per task, then mean normalised update; not scalar tuning or a scalar task loss weight. Use two explicit groups (summed five physics components and summed three IC components) to control parent task partition. Paper recommends separate PDE groups; this two-group configuration is disclosed, not a claim to reproduce its PDE-grouping experiments or theoretical guarantees for Euler-Poisson.

## Hypothesis and proposed change

Hypothesis: independent per-task adaptive moments improve IC/physics compromise enough to beat011. For each parameter and task i in{P,I}, m_i=.99m_i+.01g_i, v_i=.99v_i+.01g_i^2, initially0. Bias correct both by1-.99^t. Update parameter-=.001*mean_i[mhat_i/(sqrt(vhat_i)+1e-8)]. No decay,clipping,extra aggregate moments or conflict projection. Autograd.grad separately extracts P and I gradients from one context call,unused parameters become zeros. All parameters participate; no parent hidden/auxiliary split. Keep negative task-dot count diagnostic. CPU/native MPS three-step formula,bias correction,partitioned state,zero gradients and positive task-rescaling checks passed. Parent model/task-gradient/PR+ AST and mathematical full-phase equality passed; no PINN fits/coordinates in checks. Risks: task normalisation can overemphasise noisy near-zero gradients, opposing directions still possible,more optimiser state/overhead and choice of grouping matter.

## Training objective and setup

Fresh unchanged P sine model,seven Linear layers,width128,85765 parameters,three spatial harmonics,Xavier/bias.01,density startup.05. Tasks P=continuity+momentum_x+momentum_y+momentum_z+Poisson, I=IC_x+IC_y+IC_z, absolute MSE components weight1. First80% of750s: MultiAdam lr.001,betas(.99,.99),eps1e-8;1024PDE/1024IC pooled replacement per update,one residual/IC evaluation with two reverse sweeps. These initial batches are choices,not a total cap. Final phase unchanged ordinary summed P+I with all100000PDE/75000IC cached once via cycle,25 separately weighted microbatches max4096PDE/3072IC per full gradient/value. Same PR+ restart,Armijo c1=1e-4,four halved proposals,alpha seed rules,>12s attempt reserve/4s chunk/8s proposal deadline and rollback. All overhead charged within budget. Return task moments/step/CG,counters; record draws/evaluations/CG/search/restarts/nonfinite and conflicts. Fixed pools only,no coordinate generation/perturbation,validation/reference access or updates after checkpoint.

## Expected outcome

Expect L_val below0.1678472594,with IC improvement over013 while retaining enough physics quality for net gain. Higher total contradicts net hypothesis irrespective of component or throughput improvement. Read actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts and record overhead. Finite total alone ranks,no diagnostic gates. A single local grouping/time-limited fit cannot establish statistical significance,general MultiAdam superiority,exact scale invariance with finite epsilon or numerical-solution accuracy. Count failures honestly,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.32421 initial updates,32414 conflicting pairs;110 CG attempts,106 accepted,176 line values,19 restarts,0 nonfinite proposals.286 complete full-pool evaluations exactly reconcile,no partial evaluations. No warnings/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.2255088716231095,
    "physics_weighted": 0.12046148207149467,
    "ic_relative_l2": 0.32411015033721924,
    "ic_relative_mse": 0.10504738955161486,
    "windows": {
      "early": {
        "continuity": 0.1745444459831352,
        "momentum": 0.033050621095177805,
        "poisson": 0.010817129000272494,
        "total": 0.2184121960785855
      },
      "middle": {
        "continuity": 0.029852366677361047,
        "momentum": 0.01821325740898243,
        "poisson": 0.01611412262809857,
        "total": 0.06417974671444204
      },
      "late": {
        "continuity": 0.02421949771117583,
        "momentum": 0.020393597520577712,
        "poisson": 0.07043714245113636,
        "total": 0.1150502376828899
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.990645170211792,
        "0.5": 0.9777519702911377,
        "0.8": 0.9750359654426575
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.009354829788208008,
        "0.5": -0.022248029708862305,
        "0.8": -0.02496403455734253
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.081212118268013,
        "0.5": 0.24806280434131622,
        "0.8": 0.4266396164894104
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.1792540550231934,
        "0.5": 1.6564961671829224,
        "0.8": 2.3545334339141846
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.5341821908950806,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.086162567138672e-06
    },
    "window_weights": {
      "early": 0.2,
      "middle": 0.3,
      "late": 0.5
    },
    "time_windows": {
      "early": [
        0.0,
        0.2
      ],
      "middle": [
        0.2,
        0.5
      ],
      "late": [
        0.5,
        0.8
      ]
    },
    "warning": "Reference-free residual score, NOT numerical-solution accuracy"
  },
  "run_metadata": {
    "device": "mps",
    "params": 85765,
    "training_seconds": 738.8065468330169,
    "optimizer_steps": 32531,
    "physics_calls": 39571,
    "pde_training_evaluations": 61799104,
    "ic_training_evaluations": 54649104,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 10021,
      "loss": 0.5794087648391724,
      "elapsed_seconds": 187.51791804202367,
      "note": "MultiAdam before full PR+; PDE_eval=10261504; IC_eval=10261504"
    },
    {
      "step": 20215,
      "loss": 0.5684798955917358,
      "elapsed_seconds": 375.0163950829883,
      "note": "MultiAdam before full PR+; PDE_eval=20700160; IC_eval=20700160"
    },
    {
      "step": 30385,
      "loss": 0.5686140060424805,
      "elapsed_seconds": 562.5102955829934,
      "note": "MultiAdam before full PR+; PDE_eval=31114240; IC_eval=31114240"
    },
    {
      "step": 32531,
      "loss": 0.49900606740266085,
      "elapsed_seconds": 738.8058972500148,
      "note": "MultiAdam/PR+; cf=32414; PDE_eval=61799104; IC_eval=54649104; PDE_draws=33299104; IC_draws=33274104; cg=110; accepted=106; full=100000/75000; micro=4096; lines=176; nf=0; restarts=19"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported. Total0.2255088716 exceeds leader011 by0.0576616122 (34.35%),physics higher0.0479339048,IC MSE higher0.0097277074. Versus parent013 IC improves0.0393448834 but physics worsens0.0537726471,net+0.0144277637. All physics windows worsen versus013. 32414/32421 task pairs have negative dot products; this is diagnostic,not a rejection gate or proof of mechanism. Retain finite result without IC/physical gates. This two-group local configuration does not establish general MultiAdam ranking or significance.
