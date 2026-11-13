# Trial 045

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:44; kind=refinement; mechanism_id=intermediate_width_rwf_film_immediate_density.

## Parent methods and evidence

Trial044 (parent) scores0.12336329941335011: physics0.04678062252396187, IC MSE0.07658267688938825. Trial043 width128 scores0.12657819355491223: physics0.04193881132879733, IC0.08463938222611489. Width256 improved total through IC despite worse physics and fewer updates. Test intermediate capacity, fresh weights.

## Novelty claim

Explicit numerical width refinement, not a new scientific mechanism. RWF, Snake, bounded FiLM and input skips retain the credited parent lineage. No new literature lookup is needed for this capacity refinement.

## Hypothesis and proposed change

Width192 may balance width128 throughput and width256 IC fitting. Change only14 executable integer AST constants:256->192 and275->211. Main19->192, five211->192 hidden RWF maps,192->5; conditioner1->32->2304 reshaped6x2x192. Total285381 parameters,202560 direction and82821 auxiliary parameters including960 log scales. Trainer AST identical. CPU and native MPS checks passed: parameter counts/shapes, zero skip columns, identity FiLM, finite third feature derivatives and output-loss gradients for every parameter. An initial diagnostic incorrectly required third-derivative loss gradients for affine biases; those vanish mathematically, so the check was corrected to output-loss gradients. No model/source adjustment or training occurred during checks. Initial tensor sizes alter fresh functions/RNG as well as compute, so capacity is not isolated.

## Training objective and setup

Canonical training F=continuity+mom_x+mom_y+mom_z+Poisson+IC_x+IC_y+IC_z, all absolute MSE coefficient1. Six Snake activations, periodic19 features, repeated input skips, bounded FiLM, immediate rho=rho0 exp(clamp(t*raw_rho,-4,4)). Directions Adan lr.001 betas(.98,.92,.99) eps1e-8; auxiliaries unrectified AdaBelief lr.001 betas(.9,.999) eps1e-12. First80%1024 PDE/1024 IC replacement-pool updates; final20% full-pool PR+/Armijo100000 PDE/75000 IC using4096/3072 microbatches and tail. No total points per step cap;8192 per call only. Fresh MPS fit750seconds, physical82/RNG823001, <=750000 parameters. Frozen validation and pools unchanged.

## Expected outcome

Target L_val<0.12336329941335011 through IC/physics balance. More updates than256 may help physics while retaining IC capacity; either component can worsen. Report every window, counts, density/mass/periodicity without gates. One fresh fit does not establish statistical significance or numerical-reference accuracy.

## Observed results

Actual metrics, metadata and complete history follow; run.log and all diagnostics read. 10610 initial updates plus16 CG attempts(15 accepted),29 line values,0 restarts/nonfinite proposals.45 complete full-pool evaluations reconcile15364640 PDE/14239640 IC evaluations and11735 physics calls. Training741.919793 seconds,285381parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.12361616801817572,
    "physics_weighted": 0.045293269642870906,
    "ic_relative_l2": 0.27986228466033936,
    "ic_relative_mse": 0.07832289837530482,
    "windows": {
      "early": {
        "continuity": 0.03982595664536893,
        "momentum": 0.044138589550006935,
        "poisson": 0.0039895913078121506,
        "total": 0.087954137503188
      },
      "middle": {
        "continuity": 0.012216925836170392,
        "momentum": 0.01262877415569495,
        "poisson": 0.004223168684338183,
        "total": 0.029068868676203525
      },
      "late": {
        "continuity": 0.017472790227943787,
        "momentum": 0.01390501746029216,
        "poisson": 0.006585755390508543,
        "total": 0.03796356307874449
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9915903806686401,
        "0.5": 0.988451361656189,
        "0.8": 0.9878438115119934
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.008409619331359863,
        "0.5": -0.011548638343811035,
        "0.8": -0.012156188488006592
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.17040960490703583,
        "0.5": 0.4154052436351776,
        "0.8": 0.6922645568847656
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.4184987545013428,
        "0.5": 2.280751943588257,
        "0.8": 3.5519051551818848
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3759740889072418,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 3.0994415283203125e-06
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
    "params": 285381,
    "training_seconds": 741.919793292007,
    "optimizer_steps": 10626,
    "physics_calls": 11735,
    "pde_training_evaluations": 15364640,
    "ic_training_evaluations": 14239640,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 3310,
      "loss": 0.4079417288303375,
      "elapsed_seconds": 187.53790608304553,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=3389440; IC_eval=3389440"
    },
    {
      "step": 6622,
      "loss": 0.3494962751865387,
      "elapsed_seconds": 375.04430066701025,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=6780928; IC_eval=6780928"
    },
    {
      "step": 9946,
      "loss": 0.33511045575141907,
      "elapsed_seconds": 562.5527242500102,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=10184704; IC_eval=10184704"
    },
    {
      "step": 10626,
      "loss": 0.3019755491986871,
      "elapsed_seconds": 741.9193272080156,
      "note": "final full PR+; PDE_eval=15364640; IC_eval=14239640; PDE_draws=10964640; IC_draws=10939640; cg=16; accepted=15; full=100000/75000; micro=4096; lines=29; nf=0; restarts=0"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 15364640,
    "IC_eval": 14239640,
    "PDE_draws": 10964640,
    "IC_draws": 10939640,
    "cg": 16,
    "accepted": 15,
    "lines": 29,
    "nf": 0,
    "restarts": 0,
    "complete_full_evaluations": 45,
    "uncompleted_attempt_full_gradients": 0
  }
}
```

## Decision and interpretation

Width192 does not improve the parent total: L_val rises0.0002528686 (0.205%). Physics falls0.0014873529 but IC MSE rises0.0017402215. Early/late totals improve, middle slightly worsens.10610 initial updates and45 full evaluations lie between128/256-width throughput. Retain finite evidence;044 remains leader solely by L_val. This small single-fit gap is not significant evidence of an optimal width, and initialisation/RNG and equal-time compute are confounded. Five fresh1800-second finalist fits remain pending after all60 attempts.
