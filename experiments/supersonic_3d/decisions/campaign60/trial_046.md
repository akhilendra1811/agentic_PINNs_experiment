# Trial 046

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:44,trial:32; kind=refinement; mechanism_id=initial_potential_gate_on_wide_rwf.

## Parent methods and evidence

Trial044 supplies the width256 RWF/FiLM/Snake/input-skip immediate-density model and unchanged trainer: L_val0.12336329941335011, physics0.04678062252396187, IC0.07658267688938825. Trial032 supplies the already tested initial-potential time gate, but its Fourier initial-jet constraints are not copied. This combination keeps unconstrained learned initial velocity.

## Novelty claim

Known hard-constraint trial-function refinement: phi=t*raw_phi, not a new method. Parent032 credits the Lagaris hard-constraint principle; this algebraic combination needs no new literature lookup. Uniform initial density and periodic Poisson imply spatially constant initial potential; choose its zero gauge.

## Hypothesis and proposed change

Enforcing exact zero initial potential may reduce early Poisson/momentum error without the IC representation bottleneck of032. One executable return expression changes: retain rho and all three velocities, replace raw_phi with t*raw_phi. Architecture462405 parameters and all initial tensors remain identical to044 for the same RNG. Entire training function unchanged. CPU/native MPS synthetic checks passed: identical fresh parameters to044; unchanged rho/velocities; zero initial phi, spatial gradient and Laplacian; later phi time gate and finite all-parameter output-loss gradients. No training or new PDE coordinates used in checks. Multiplication by time also changes later function/gradient geometry, so initial constraint is not isolated from parameterisation effects.

## Training objective and setup

Unchanged canonical F=sumfivePDE+sumthreeIC absolute MSE, all coefficients1. Main19->256,five275->256 RWF maps,256->5; six Snake, bounded FiLM1->32->3072, periodic19features, repeated input skips. Directions Adan lr.001 betas(.98,.92,.99) eps1e-8; auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. First80%1024 PDE/1024 IC pool batches, final20%PR+/Armijo full100000 PDE/75000 IC through4096/3072 microbatches+tail. No total point cap,8192 per call only. Fresh750second MPS fit, seed82/RNG823001, only fixed training pools, frozen score unchanged.

## Expected outcome

Target L_val<0.12336329941335011 through lower early physics without larger IC penalty. The time gate may slow potential fitting away from zero or alter conditioning; reduced initial residual alone need not improve total. Report all windows, IC, density/mass/periodicity, counts and timing without gates. No statistical significance or reference-solution accuracy claim.

## Observed results

Actual metrics, metadata and complete history follow; run.log and all diagnostics read.8250 initial updates+11 completed CG attempts(10 accepted),23 line values,1 restart,0 nonfinite proposals.34 complete full-pool evaluations reconcile11848000 PDE/10998000 IC evaluations and9100 physics calls. Training740.578309 seconds,462405parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.12546171423236452,
    "physics_weighted": 0.049715301245006775,
    "ic_relative_l2": 0.275220662355423,
    "ic_relative_mse": 0.07574641298735774,
    "windows": {
      "early": {
        "continuity": 0.04655866444035764,
        "momentum": 0.05046704276368701,
        "poisson": 0.0013540254785089647,
        "total": 0.09837973268255362
      },
      "middle": {
        "continuity": 0.013632364434188719,
        "momentum": 0.01355316079164473,
        "poisson": 0.003842441287505598,
        "total": 0.03102796651333905
      },
      "late": {
        "continuity": 0.018986210780816175,
        "momentum": 0.014980580864515064,
        "poisson": 0.007495137863657431,
        "total": 0.04146192950898867
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9912259578704834,
        "0.5": 0.9872802495956421,
        "0.8": 0.9835308790206909
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.008774042129516602,
        "0.5": -0.01271975040435791,
        "0.8": -0.016469120979309082
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1719922125339508,
        "0.5": 0.4184934198856354,
        "0.8": 0.69364333152771
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.4263617992401123,
        "0.5": 2.289795160293579,
        "0.8": 3.5975239276885986
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3510882258415222,
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
    "training_seconds": 740.5783092920319,
    "optimizer_steps": 8261,
    "physics_calls": 9100,
    "pde_training_evaluations": 11848000,
    "ic_training_evaluations": 10998000,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2571,
      "loss": 0.40222638845443726,
      "elapsed_seconds": 187.50347058300395,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2632704; IC_eval=2632704"
    },
    {
      "step": 5153,
      "loss": 0.3374050557613373,
      "elapsed_seconds": 375.04946870799176,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5276672; IC_eval=5276672"
    },
    {
      "step": 7734,
      "loss": 0.30841952562332153,
      "elapsed_seconds": 562.5451911669807,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7919616; IC_eval=7919616"
    },
    {
      "step": 8261,
      "loss": 0.29044826701283455,
      "elapsed_seconds": 740.5779792499961,
      "note": "final full PR+; PDE_eval=11848000; IC_eval=10998000; PDE_draws=8548000; IC_draws=8523000; cg=11; accepted=10; full=100000/75000; micro=4096; lines=23; nf=0; restarts=1"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 11848000,
    "IC_eval": 10998000,
    "PDE_draws": 8548000,
    "IC_draws": 8523000,
    "cg": 11,
    "accepted": 10,
    "lines": 23,
    "nf": 0,
    "restarts": 1,
    "complete_full_evaluations": 34,
    "uncompleted_attempt_full_gradients": 0
  }
}
```

## Decision and interpretation

Initial-potential gate does not improve total: L_val rises0.0020984148 (1.70%) versus044. IC MSE falls0.0008362639 but weighted physics rises0.0029346787. Early Poisson improves0.0033260645, yet every window total worsens; middle/late Poisson rise. Exact initial constraint does not guarantee better dynamics. Retain finite evidence with no diagnostic gates;044 remains leader. Same fresh parameter tensors improve comparability, but time gating changes later conditioning and equal-time training trajectory, so no general hard-constraint verdict or statistical significance claim. Finalists remain pending after60 attempts.
