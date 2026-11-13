# Trial 047

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:44; kind=refinement; mechanism_id=half_budget_full_pool_pr_finish.

## Parent methods and evidence

Trial044 supplies the leading width256 immediate-density RWF/FiLM model: L_val0.12336329941335011, physics0.04678062252396187, IC0.07658267688938825. Its742seconds contained8118 initial updates but only11 completed full-pool PR+ attempts. Width128043 had lower physics but higher IC;045/046 did not beat044.

## Novelty claim

Explicit training-budget split refinement of the established PR+/Armijo pipeline, not a new optimiser or literature novelty. No new literature lookup required; retain parent classical PR+ provenance.

## Hypothesis and proposed change

Change exactly one executable scalar from.8 to.5 in the stochastic-loop cumulative_fraction condition. Model initialisation, optimiser recurrences, all batch sizes, full-pool objective, line search and deadline rollback remain identical. More full-pool optimisation may lower physics sufficiently to compensate for fewer stochastic IC updates. Equal time and unequal update counts are the intended comparison.

## Training objective and setup

Canonical F=sumfivePDE+sumthreeIC absolute MSE, all coefficients1. Same462405parameter width256 periodic19-feature RWF/FiLM/Snake/input-skip model as044, immediate density and unconstrained potential. Hidden directions Adan lr.001 betas(.98,.92,.99) eps1e-8; auxiliaries AdaBelief lr.001 betas(.9,.999) eps1e-12. First50%1024PDE/1024IC replacement-pool batches; remaining50% PR+/Armijo full100000PDE/75000IC via4096/3072microbatches+tail. No total point cap;8192per context call. Fresh750second MPS fit, physical82/RNG823001, frozen data/scorer unchanged.

## Expected outcome

Target L_val<0.12336329941335011, hypothesising lower weighted physics without a larger IC penalty. Earlier switch may leave the nonlinear model undertrained or stagnate in line search. Report all components, diagnostics and actual stochastic/CG/evaluation counts with no eligibility gates. Single-fit timing variability and trajectory dependence limit causal/statistical conclusions.

## Observed results

Actual metrics, metadata and complete history follow; run.log and all diagnostics read.4952 initial updates+30 completed CG attempts(28 accepted),51 line values,5 restarts,0 nonfinite proposals.81 complete full-pool evaluations reconcile13170848 PDE/11145848 IC evaluations and6977 physics calls. Training742.802324 seconds,462405parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.12310839192730305,
    "physics_weighted": 0.03965088854812371,
    "ic_relative_l2": 0.28889012336730957,
    "ic_relative_mse": 0.08345750337917934,
    "windows": {
      "early": {
        "continuity": 0.03293379872004916,
        "momentum": 0.03503519769740721,
        "poisson": 0.0058779997387567486,
        "total": 0.07384699615621312
      },
      "middle": {
        "continuity": 0.01078241674089635,
        "momentum": 0.011789571921233644,
        "poisson": 0.004102398492040481,
        "total": 0.026674387154170476
      },
      "late": {
        "continuity": 0.014692512275087973,
        "momentum": 0.01224819403715335,
        "poisson": 0.006817640029018559,
        "total": 0.03375834634125988
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9925107955932617,
        "0.5": 0.9903576374053955,
        "0.8": 0.9910233020782471
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.007489204406738281,
        "0.5": -0.009642362594604492,
        "0.8": -0.00897669792175293
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.16493704915046692,
        "0.5": 0.40430015325546265,
        "0.8": 0.673659086227417
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3995293378829956,
        "0.5": 2.2248728275299072,
        "0.8": 3.4531028270721436
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.30502402782440186,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.8477439880371094e-06
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
    "training_seconds": 742.8023241250194,
    "optimizer_steps": 4982,
    "physics_calls": 6977,
    "pde_training_evaluations": 13170848,
    "ic_training_evaluations": 11145848,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2470,
      "loss": 0.3907933831214905,
      "elapsed_seconds": 187.5569073749939,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2529280; IC_eval=2529280"
    },
    {
      "step": 4952,
      "loss": 0.3460295498371124,
      "elapsed_seconds": 375.02038683299907,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5070848; IC_eval=5070848"
    },
    {
      "step": 4982,
      "loss": 0.3239958882331848,
      "elapsed_seconds": 742.8018195829936,
      "note": "final full PR+; PDE_eval=13170848; IC_eval=11145848; PDE_draws=5170848; IC_draws=5145848; cg=30; accepted=28; full=100000/75000; micro=4096; lines=51; nf=0; restarts=5"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 13170848,
    "IC_eval": 11145848,
    "PDE_draws": 5170848,
    "IC_draws": 5145848,
    "cg": 30,
    "accepted": 28,
    "lines": 51,
    "nf": 0,
    "restarts": 5,
    "complete_full_evaluations": 81,
    "uncompleted_attempt_full_gradients": 0
  }
}
```

## Decision and interpretation

New lowest finite total, improving044 by0.0002549075 (0.207%). Weighted physics falls0.0071297340 while IC MSE rises0.0068748265. All physics window totals, continuity and momentum improve; every Poisson term worsens.4952 stochastic updates versus8118 and81 full evaluations versus33 quantify the intended time-allocation tradeoff. Retain047 by total alone, with no diagnostic gates. The small one-fit margin does not establish significance or an optimal split; timing/RNG path differences remain. Fresh matched1800-second finalists still required after60 attempts.
