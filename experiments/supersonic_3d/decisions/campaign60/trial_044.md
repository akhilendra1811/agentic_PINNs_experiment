# Trial 044

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:43; kind=refinement; mechanism_id=wider_rwf_film_immediate_density_model.

## Parent methods and evidence

Trial043 is the parent and current lowest finite result: L_val0.12657819355491223, weighted physics0.04193881132879733, IC relative MSE0.08463938222611489. Removing the density hold in its RWF/FiLM/input-skip configuration improved030s physics and IC. IC error remains the larger score term. This trial tests more main-network capacity at the same time budget; no checkpoint reuse.

## Novelty claim

Explicit width/capacity refinement, not a new activation, optimiser or mechanism. Increase main hidden width128->256 and all dependent input-skip/FiLM output dimensions, keeping depth and the conditioner hidden width32 fixed. RWF/Snake/FiLM lineage remains credited in the parent. No new literature novelty claim or additional lookup is needed for this numerical refinement.

## Hypothesis and proposed change

Primary hypothesis: a wider immediate-density model fits the initial field and dynamics better enough to outweigh lower throughput. Main affine shapes become19->256, five(256+19)->256,256->5; six Snake units and five RWF hidden maps remain. Conditioner1->32->3072 produces6x2x256 modulation pairs; all scale/shift formulas and zero final conditioner head remain. Only14 width-dependent integer AST constants change from043; entire trainer and optimisers unchanged. Total462405parameters,352000hidden directions,110405auxiliary. CPU/native MPS checks passed for shapes/counts, identity FiLM, zero new input-skip columns, finite raw outputs/third feature derivatives/all-parameter gradients. Initialisation algorithm is unchanged but tensor sizes alter initial functions and subsequent RNG consumption, so capacity is not causally isolated from initialisation or compute. No PDE fitting/new coordinates in checks.

## Training objective and setup

Frozen L_val=.2early+.3middle+.5late+IC_relative_MSE unchanged. Immediate densityrho=rho0 exp(clamp(t*raw_rho,-4,4));same seven main affines, six Snake activations, periodic19features, repeated input skips and bounded time-FiLM;462405parameters under750000.352000hidden RWF direction parameters use Adan lr.001,betas(.98,.92,.99),eps1e-8;110405auxiliary including1280log-scales use unrectified AdaBelief lr.001,betas(.9,.999),eps1e-12. Canonical F=sumfivePDE+sumthreeIC absolute MSE, allcoef1. First80%1024PDE/1024IC replacement-pool batches;final20%full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No total points-per-step cap;8192 per context call.750seconds,fresh weights,seed82/training823001,MPS,only frozen pools. Every larger-network cost counts inside the budget; actual counters recorded afterrun.

## Expected outcome

Falsifiable target L_val<0.12657819355491223, with lower IC error and any physics gain large enough to compensate for lost updates. Wider differentiated graphs may reduce stochastic and full-pool steps, require smaller line-search steps or become less stable; more capacity may overfit finite pools. Report all windows/components, throughput, parameters and density/mass/periodicity diagnostics without eligibility gates. One fit is not statistical significance or general neural-scaling/numerical-accuracy evidence.

## Observed results

Actual metrics, metadata and complete history follow; all numerical diagnostics and run.log read. 8118 initial updates+11 completed CG attempts(10 accepted),21 line values,0 restarts/nonfinite proposals. Counters imply33 complete full-pool evaluations:11 completed-attempt gradients+21 line values+one full gradient in the final unfinished deadline-limited attempt. They reconcile11612832 PDE/10787832 IC evaluations and8943 physics calls; the unfinished attempt restores base parameters and adds no optimiser step. Training742.177106 seconds,462405parameters. No partial pool pass is needed for reconciliation. No execution error.

```json
{
  "metrics": {
    "L_val": 0.12336329941335011,
    "physics_weighted": 0.04678062252396187,
    "ic_relative_l2": 0.27673575282096863,
    "ic_relative_mse": 0.07658267688938825,
    "windows": {
      "early": {
        "continuity": 0.041947493988709963,
        "momentum": 0.04645299967160172,
        "poisson": 0.004680089968192207,
        "total": 0.0930805836285039
      },
      "middle": {
        "continuity": 0.012771489073773602,
        "momentum": 0.012524508278894834,
        "poisson": 0.003641114737253443,
        "total": 0.02893711208992188
      },
      "late": {
        "continuity": 0.019204882283721435,
        "momentum": 0.013994655294829505,
        "poisson": 0.005767206764018118,
        "total": 0.038966744342569054
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9927695393562317,
        "0.5": 0.9924896359443665,
        "0.8": 0.9963027238845825
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0072304606437683105,
        "0.5": -0.007510364055633545,
        "0.8": -0.0036972761154174805
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.17028415203094482,
        "0.5": 0.41428902745246887,
        "0.8": 0.6884883046150208
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.4219998121261597,
        "0.5": 2.2838003635406494,
        "0.8": 3.555757999420166
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.43787744641304016,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.384185791015625e-06
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
    "training_seconds": 742.1771064580535,
    "optimizer_steps": 8129,
    "physics_calls": 8943,
    "pde_training_evaluations": 11612832,
    "ic_training_evaluations": 10787832,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2496,
      "loss": 0.4014361500740051,
      "elapsed_seconds": 187.51250341703417,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2555904; IC_eval=2555904"
    },
    {
      "step": 5051,
      "loss": 0.3352621793746948,
      "elapsed_seconds": 375.05518404202303,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5172224; IC_eval=5172224"
    },
    {
      "step": 7606,
      "loss": 0.3459237813949585,
      "elapsed_seconds": 562.5034396250267,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7788544; IC_eval=7788544"
    },
    {
      "step": 8129,
      "loss": 0.2923785662278533,
      "elapsed_seconds": 742.1766003330122,
      "note": "final full PR+; PDE_eval=11612832; IC_eval=10787832; PDE_draws=8412832; IC_draws=8387832; cg=11; accepted=10; full=100000/75000; micro=4096; lines=21; nf=0; restarts=0"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 11612832,
    "IC_eval": 10787832,
    "PDE_draws": 8412832,
    "IC_draws": 8387832,
    "cg": 11,
    "accepted": 10,
    "lines": 21,
    "nf": 0,
    "restarts": 0,
    "complete_full_evaluations": 33,
    "uncompleted_attempt_full_gradients": 1
  }
}
```

## Decision and interpretation

New lowest finite score. Total improves043 by0.0032148941 (2.54%). IC MSE falls0.0080567053, while weighted physics rises0.0048418112. All window totals worsen; middle/late Poisson improve but early Poisson and continuity/momentum generally worsen.8118 initial updates versus04314446 and33 full evaluations versus68 show capacity/compute tradeoff. Retain044 by total only despite higher physics; no diagnostic gates. Width, initial function/RNG and throughput are not isolated, and this small single-fit gain is not statistical significance or general scaling/numerical-accuracy proof. Required fresh1800-second finalist comparison remains pending after60 attempts.
