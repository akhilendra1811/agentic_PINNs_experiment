# Trial 013

Research metadata (locked on preparation): research_area=optimisation; parents=trial:11; kind=mechanism; mechanism_id=config_two_task_descent.

## Parent methods and evidence

Closed Trial011 source only, current best total0.1678472594, physics0.0725275773,IC MSE0.0953196821. Trial012 SAM total0.1798897218 worsened both weighted components with half the initial updates. Across006-012 physics/IC tradeoffs suggest task-gradient interactions deserve a direct test. Model, additive components and full-pool PR+ retained; initial optimiser replaced globally. Fresh weights only; no parent checkpoint or states imported.

## Novelty claim

Distinct optimisation mechanism basic two-task ConFIG, credited to Liu,Chu,Thuerey https://arxiv.org/html/2408.11104v2 Section3.1 equations2-3 and Section3.2. Known method, no global scientific novelty. Unlike prior PCGrad this uses equal unit-gradient projection direction with conflict-dependent length. This is basic ConFIG with SGD, not M-ConFIG, no momentum/adaptive elementwise scaling claimed to preserve conflict freedom. For two nonzero non-antiparallel gradients, normalised unit-vector sum is algebraically equivalent to normalised pseudoinverse direction. Degenerate handling disclosed below.

## Hypothesis and proposed change

Hypothesis: balancing physics/IC gradient directions lowers total versus011 despite losing adaptive preconditioning. Form gP=gradient of summed five PDE MSEs and gI=gradient of summed three IC MSEs from same context call, separate autograd.grad (allow_unused zeros, first retains graph). With nP=||gP|| and nI=||gI||, u=normalise(gP/nP+gI/nI); d=max(0,(gP+gI) dot u)*u. All parameters SGD step -=.01*d, zero momentum/decay. If a task norm<1e-12 return other gradient; if bisector norm<1e-6 return zero (near-antiparallel degeneracy), record counts. Nonfinite task norms raise. Log original negative dot products and degeneracies. Positive first-order projections do not guarantee finite-step loss decrease or global/final-phase conflict freedom. CPU random-vector comparison with pseudoinverse passed20 cases; CPU/native MPS positive/equal normalised projections,antiparallel/zero task and unused-gradient checks passed. Model/full PR+ AST and entire mathematical full-phase equality passed. No PINN fit/coordinate sampling in checks. Risks: SGD conditioning,task normalisation suppressing priorities,stationary Pareto tradeoff and extra backward cost.

## Training objective and setup

Fresh P sine architecture: seven Linear,width128,85765 parameters,three spatial harmonics,Xavier/bias.01,density startup.05. Tasks F_P=continuity+momentum_x+momentum_y+momentum_z+Poisson; F_I=IC_x+IC_y+IC_z, absolute MSE components weight1. First80% of750seconds uses two-task ConFIG +SGD(lr.01,momentum0,decay0) on all parameters, gradient assignment from d. Initial1024PDE/1024IC with pool replacement is a control choice, not a cap; one residual/IC forward evaluation with separate reverse sweeps per update. Last phase uses unchanged summed F_P+F_I and PR+ on all100000PDE/75000IC cached exactly once via cycle,25 exact separately weighted microbatches max4096PDE/3072IC. Armijo c1=1e-4,up to4 halved proposals,same seed/restart rules,>12s attempt reserve/4s chunk/8s proposal checks and rollback to last accepted iterate. All overhead in budget. Return SGD state/step/CG and task counters, log actual draws/evaluations/CG/search/restarts/nonfinite counts. Frozen coordinates only,no perturbations/generation,validation or reference access. No post-checkpoint updates.

## Expected outcome

Expect total below0.1678472594 through a better physics/IC compromise; larger total falsifies net hypothesis even if conflict counts,one component or throughput improve. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log; reconcile point counts separately from backward sweeps. Finite total only ranks, no diagnostic gates. This single matched-time fit tests the specific SGD-ConFIG hybrid with full-pool PR+ and cannot establish general optimiser ranking,statistical significance or trajectory accuracy. Count failures honestly, no ID rerun.

## Observed results

All actual records and diagnostics read. 31853 initial updates,24305 conflicting pairs,0 degeneracies;111 CG attempts,107 accepted,176 line values,16 restarts,0 nonfinite proposals.287 full evaluations reconcile exactly,no partial evaluations or warnings/execution failure. Full records:

```json
{
  "metrics": {
    "L_val": 0.21108110788127185,
    "physics_weighted": 0.06668883497172903,
    "ic_relative_l2": 0.3799898326396942,
    "ic_relative_mse": 0.14439227290954282,
    "windows": {
      "early": {
        "continuity": 0.12115778337417489,
        "momentum": 0.026548826565502868,
        "poisson": 0.010583573206317618,
        "total": 0.15829018314599538
      },
      "middle": {
        "continuity": 0.012095421274739324,
        "momentum": 0.014342124887009497,
        "poisson": 0.0071437759674018025,
        "total": 0.033581322129150624
      },
      "late": {
        "continuity": 0.01562675995321136,
        "momentum": 0.01770267074602666,
        "poisson": 0.016583372708331514,
        "total": 0.04991280340756954
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.993130087852478,
        "0.5": 0.9855911731719971,
        "0.8": 0.9832205772399902
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.006869912147521973,
        "0.5": -0.01440882682800293,
        "0.8": -0.016779422760009766
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.0864204466342926,
        "0.5": 0.26320087909698486,
        "0.8": 0.4646604061126709
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.1979565620422363,
        "0.5": 1.7255795001983643,
        "0.8": 2.524137258529663
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.314108282327652,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.0265579223632812e-06
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
    "training_seconds": 739.5463943330105,
    "optimizer_steps": 31964,
    "physics_calls": 39028,
    "pde_training_evaluations": 61317472,
    "ic_training_evaluations": 54142472,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9987,
      "loss": 0.7974621057510376,
      "elapsed_seconds": 187.51745337503962,
      "note": "ConFIG-SGD before full PR+; PDE_eval=10226688; IC_eval=10226688"
    },
    {
      "step": 19924,
      "loss": 0.6944465637207031,
      "elapsed_seconds": 375.0046032500104,
      "note": "ConFIG-SGD before full PR+; PDE_eval=20402176; IC_eval=20402176"
    },
    {
      "step": 29860,
      "loss": 0.6377924084663391,
      "elapsed_seconds": 562.5192547499901,
      "note": "ConFIG-SGD before full PR+; PDE_eval=30576640; IC_eval=30576640"
    },
    {
      "step": 31964,
      "loss": 0.6129865851253271,
      "elapsed_seconds": 739.5457497499883,
      "note": "ConFIG/PR+; cf=24305; zero=0; PDE_eval=61317472; IC_eval=54142472; PDE_draws=32717472; IC_draws=32692472; cg=111; accepted=107; full=100000/75000; micro=4096; lines=176; nf=0; restarts=16"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported: total rose0.0432338485 (25.76%) versus011. Physics fell0.0058387423 while IC MSE rose0.0490725908. Early physics improved substantially, middle/late worsened. 24305 of31853 initial task pairs conflicted (76.3%),zero degeneracies. Smaller physics does not promote this higher total; no IC threshold excludes it. Retain finite result,011 remains leader. This specific basic ConFIG-SGD configuration is not a general ConFIG verdict;conditioning/step size and task geometry are not isolated. No significance or numerical-reference accuracy claim.
