# Trial 049

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:47,trial:37; kind=refinement; mechanism_id=wide_rwf_full_ic_proximal_readout.

## Parent methods and evidence

Trial047 supplies the best total0.12310839192730305 with physics0.03965088854812371 and IC MSE0.08345750337917934. Trial037 supplies periodic full-IC proximal linear-head solves; its earlier width128/density-hold model scored0.17649304238395086 and failed to beat028. This is an explicitly exploratory combination under a much improved model, not evidence that037 already worked.

## Novelty claim

Known block least-squares/proximal readout correction, with parent037 VarPro lineage credited. Not exact variable projection of the nonlinear PINN loss: only IC velocity head is solved, PDE loss is not in the linear system, hidden features are fixed per solve, and optimiser moments are retained. No new lookup or novelty claim.

## Hypothesis and proposed change

Combine047 model/RWF parameter groups and50/50 split with037 full-IC head correction every256 initial updates before fraction.48. Design H has256 hidden features plus bias; solve(G/N+.001I)B=C/N+.001B_old in CPUfloat64, streaming all75000 IC points through4096 cycle chunks. Commit velocity head rows1:4 only after complete finite solve and proximal-objective check. Same462405 parameters/fresh initial weights. CPU/native MPS checks confirm identical parent initial parameters/outputs and257-column design reproduces velocity head; CPUfloat64 synthetic normal-equation stationarity and proximal decrease passed. AST confirms037 trainer copied with only declared dimension/split/RWF grouping changes. No PDE fit/new training coordinates in checks. Extra IC fitting may improve the larger score term but can increase PDE error and reduce throughput.

## Training objective and setup

Canonical F=sumfivePDE+sumthreeIC absolute MSE, coefficient1. Width256 RWF/FiLM/Snake/input skips with immediate density as047. Hidden directions Adan lr.001 betas(.98,.92,.99) eps1e-8; auxiliaries AdaBelief lr.001 betas(.9,.999) eps1e-12, including head moments retained after solves. First50%1024PDE/1024IC replacement-pool gradients plus proximal corrections; final50%full PR+/Armijo100000PDE/75000IC using4096/3072microbatches+tail. Count extra direct IC feature evaluations beyond owner context. No total point cap,8192 per context call only. Fresh MPS750seconds, physical82/RNG823001, frozen score/pools unchanged.

## Expected outcome

Target L_val<0.12310839192730305 through better IC fitting without larger physics cost. Head solves may disturb dynamics or optimiser state, numerical normal-equation conditioning is ridge-regularised, and CPU transfers/solves count within time. Report actual corrections, complete/partial IC passes, all components and diagnostics without gates. One fit cannot establish general VarPro superiority or reference accuracy.

## Observed results

Actual metrics, metadata and complete history follow; run.log and all diagnostics read.5100 initial updates+19 completed IC head solves+31 CG attempts(28 accepted),54 line values,1 restart,0 nonfinite proposals.85 complete full-pool evaluations reconcile13722400 PDE and11597400 owner IC evaluations, plus1425000 direct IC feature evaluations =13022400 full IC evaluations.7225 physics calls;5150 total updates. Training738.552690 seconds,462405parameters.19/19 completed solves passed proximal checks; no partial IC pass or execution error.

```json
{
  "metrics": {
    "L_val": 0.13239658470328564,
    "physics_weighted": 0.04274460576479454,
    "ic_relative_l2": 0.2994194030761719,
    "ic_relative_mse": 0.08965197893849108,
    "windows": {
      "early": {
        "continuity": 0.03433134248577852,
        "momentum": 0.03333313905281238,
        "poisson": 0.007131204043337902,
        "total": 0.0747956855819288
      },
      "middle": {
        "continuity": 0.011385219378175418,
        "momentum": 0.012082898327506036,
        "poisson": 0.004777681060498362,
        "total": 0.028245798766179817
      },
      "late": {
        "continuity": 0.016524679104303552,
        "momentum": 0.012548513896618043,
        "poisson": 0.009550265036188072,
        "total": 0.03862345803710967
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9919673204421997,
        "0.5": 0.9879533648490906,
        "0.8": 0.98750239610672
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.008032679557800293,
        "0.5": -0.012046635150909424,
        "0.8": -0.01249760389328003
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1558683216571808,
        "0.5": 0.38461771607398987,
        "0.8": 0.6478882431983948
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3712151050567627,
        "0.5": 2.14046049118042,
        "0.8": 3.3234994411468506
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.34909117221832275,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 5.245208740234375e-06
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
    "params": 462405,
    "training_seconds": 738.5526901670382,
    "optimizer_steps": 5150,
    "physics_calls": 7225,
    "pde_training_evaluations": 13722400,
    "ic_training_evaluations": 11597400,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2554,
      "loss": 0.4439915418624878,
      "elapsed_seconds": 187.5552611250314,
      "note": "readout ls=9; ICtrain=0.36993->0.34008; PDE_eval=2606080; IC_eval=3281080"
    },
    {
      "step": 5119,
      "loss": 0.3900243639945984,
      "elapsed_seconds": 375.0277960000094,
      "note": "readout ls=19; ICtrain=0.31513->0.29934; PDE_eval=5222400; IC_eval=6647400"
    },
    {
      "step": 5150,
      "loss": 0.35671977372840047,
      "elapsed_seconds": 738.5523210419924,
      "note": "final full PR+; PDE_eval=13722400; IC_eval=13022400; PDE_draws=5322400; IC_draws=6722400; cg=31; accepted=28; full=100000/75000; micro=4096; lines=54; nf=0; restarts=1; ls=19; lf=1425000; la=19"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 13722400,
    "IC_eval": 13022400,
    "PDE_draws": 5322400,
    "IC_draws": 6722400,
    "cg": 31,
    "accepted": 28,
    "lines": 54,
    "nf": 0,
    "restarts": 1,
    "ls": 19,
    "lf": 1425000,
    "la": 19,
    "complete_full_evaluations": 85,
    "uncompleted_attempt_full_gradients": 0
  }
}
```

## Decision and interpretation

Combination does not improve total: L_val rises0.0092881928 (7.54%) versus047. Physics rises0.0030937172 and IC MSE rises0.0061944756. All window totals worsen; early momentum improves but all continuity/Poisson and middle/late momentum worsen. Local IC training objective decreases in all19 completed solves (recorded last pairs0.36993->0.34008 and0.31513->0.29934), yet joint end-of-training IC validation worsens. Local head optimality, retained optimiser moments, subsequent nonlinear updates and PDE compatibility are distinct. Extra1425000 IC evaluations are included in full accounting. Retain finite evidence without gates;047 remains leader. No general least-squares/VarPro verdict or significance/reference-accuracy claim; final1800-second comparison remains pending after60.
