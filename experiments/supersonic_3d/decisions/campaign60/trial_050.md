# Trial 050

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:47; kind=refinement; mechanism_id=momentum_mean_and_global_relative_ic_training.

## Parent methods and evidence

Trial047 supplies the leading width256 RWF/FiLM immediate-density model and50/50 schedule: total0.12310839192730305, physics0.03965088854812371, IC0.08345750337917934. Existing training sums three momentum and three absolute IC component MSEs, whereas frozen validation uses momentum mean and IC relative MSE.048 bandwidth and049 local IC solves did not improve total.

## Novelty claim

Explicit scalar loss-normalisation refinement, not a new PINN mechanism. Use only fixed training target energy and unchanged owner component losses. No new literature lookup or novelty claim. This is partial alignment of component weights; uniform pooled time sampling remains different from frozen window weighting.

## Hypothesis and proposed change

Set training F=C+(Mx+My+Mz)/3+P+(Ix+Iy+Iz)/E, E=mean_over75000_train_points(sum_three_targets_squared), floor1e-12. Stream all IC targets once via4096 cycle calls before updates, transfer targets toCPUfloat64 for fixed energy reduction, count75000 extra IC draws but no model evaluations. E is constant, not minibatch-dependent; full-pool accumulation therefore computes exactly the pooled relative IC objective. No validation labels/coords used. CPU/native MPS actual-loss-closure synthetic values/gradients/counters passed, and unequal microbatch accumulation exactly matches pooled relative IC MSE. The first harness failed because extracted nonlocal counters lacked bindings; corrected harness bindings, no candidate change. AST verifies unchanged model/optimiser/direction code. No PDE fitting or new coordinates in checks. Model and all optimiser recurrences unchanged; full-pool PR uses the same new objective as stochastic training.

## Training objective and setup

Same462405parameter model as047: width256, five RWF hidden directions, six Snake, bounded time FiLM, periodic19features and input skips, immediate density. Directions Adan lr.001 betas(.98,.92,.99) eps1e-8; auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. First50%1024PDE/1024IC replacement-pool updates, remaining PR+/Armijo full100000PDE/75000IC via4096/3072microbatches+tail. E reduction/setup counts inside750seconds. No total point cap;8192 per context call. Fresh MPS seed82/RNG823001; frozen scorer, validation formula and pools unchanged.

## Expected outcome

Target L_val<0.12310839192730305 through better component balance, possibly lower continuity/Poisson while momentum or IC absolute errors rise. Weighting can still harm all terms or cause line-search changes. Record E, every window/component, actual counts and density/mass/periodicity without gates. Sampling RNG changes due extra initial cycle draw are a confound. No claim of fully score-matched time objective, statistical significance or numerical-reference accuracy.

## Observed results

Actual metrics, metadata and complete history follow; run.log and all diagnostics read.5115 initial updates+32 completed CG attempts(28 accepted),53 line values,1 restart,0 nonfinite proposals.85 complete full-pool evaluations reconcile13737760 PDE/11612760 IC evaluations and7240 physics calls.5387760 IC draws include75000 target-only energy-estimation draws and75000 cache draws; target-only pass has no model evaluations. Fixed E logged to7significant digits3.567659 (IC component coefficient approximately0.2802958, momentum each1/3). Training742.163241 seconds,462405parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.1146599961747031,
    "physics_weighted": 0.018807728169454165,
    "ic_relative_l2": 0.30960017442703247,
    "ic_relative_mse": 0.09585226800524893,
    "windows": {
      "early": {
        "continuity": 0.007870663835387941,
        "momentum": 0.02393722472754615,
        "poisson": 0.0015402068402047648,
        "total": 0.03334809540313886
      },
      "middle": {
        "continuity": 0.002364589429284137,
        "momentum": 0.009495536929435488,
        "poisson": 0.001013576210578732,
        "total": 0.012873702569298356
      },
      "late": {
        "continuity": 0.004893911808159713,
        "momentum": 0.009758692333730381,
        "poisson": 0.0018993924941836811,
        "total": 0.016551996636073776
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9986486434936523,
        "0.5": 0.9996637105941772,
        "0.8": 1.0018740892410278
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0013513565063476562,
        "0.5": -0.0003362894058227539,
        "0.8": 0.001874089241027832
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.15839961171150208,
        "0.5": 0.3950296938419342,
        "0.8": 0.6740089654922485
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3788204193115234,
        "0.5": 2.1753947734832764,
        "0.8": 3.4603354930877686
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.30701741576194763,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.4007091522216797e-06
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
    "training_seconds": 742.1632413750049,
    "optimizer_steps": 5147,
    "physics_calls": 7240,
    "pde_training_evaluations": 13737760,
    "ic_training_evaluations": 11612760,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2553,
      "loss": 0.13056421279907227,
      "elapsed_seconds": 187.55542504100595,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2614272; IC_eval=2614272"
    },
    {
      "step": 5115,
      "loss": 0.11637544631958008,
      "elapsed_seconds": 375.03971195803024,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5237760; IC_eval=5237760"
    },
    {
      "step": 5147,
      "loss": 0.10447247186675668,
      "elapsed_seconds": 742.1628104579868,
      "note": "final full PR+; PDE_eval=13737760; IC_eval=11612760; PDE_draws=5337760; IC_draws=5387760; cg=32; accepted=28; full=100000/75000; micro=4096; lines=53; nf=0; restarts=1; E=3.567659"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 13737760,
    "IC_eval": 11612760,
    "PDE_draws": 5337760,
    "IC_draws": 5387760,
    "cg": 32,
    "accepted": 28,
    "lines": 53,
    "nf": 0,
    "restarts": 1,
    "ic_energy_logged_7sig": 3.567659,
    "complete_full_evaluations": 85,
    "uncompleted_attempt_full_gradients": 0,
    "extra_ic_target_only_draws": 75000
  }
}
```

## Decision and interpretation

New lowest finite total: L_val improves047 by0.0084483958 (6.86%). Physics falls0.0208431604 (52.6%) while IC MSE rises0.0123947646. Every continuity, momentum and Poisson window component improves despite reduced momentum/IC training coefficients. Relative-IC/mean-momentum normalisation is supported for this exploratory fit, but the two coefficient changes and altered sampling RNG were combined, so their separate effects are unknown. Uniform training time distribution still differs from validation windows.5115 stochastic updates/85 full evaluations are similar to0474952/81. Retain050 by total alone despite worse IC diagnostic; no gates. No statistical significance, general optimiser/theorem or numerical-reference accuracy claim. Continue051-060 classical optimisation, then fresh1800-second five-finalist plus P/B/W comparison.
