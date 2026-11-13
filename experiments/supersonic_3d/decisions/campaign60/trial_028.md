# Trial 028

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:25; kind=mechanism; mechanism_id=repeated_periodic_input_skip_connections.

## Parent methods and evidence

Trial025 is the parent: L_val=0.16374612321085807, physics=0.06730568805350672, IC_relative_MSE=0.09644043515735135. Trial027 temporal experts scored0.1801340132213194, worse in both terms. Return to the best single bounded-time-FiLM/Snake backbone; retain its training procedure. This combines established FiLM and input-skip ideas, not a globally novel architecture.

## Novelty claim

Mechanism: concatenate all19 original periodic/time features into each of the five main hidden affine layers. This creates direct feature paths absent from025. NeRF AppendixA (https://arxiv.org/html/2003.08934v2) supplies known input-concatenation precedent; its fifth-layer skip, ReLU renderer and sampling are not reproduced. Local repeated skips differ from prior additive residuals, expanded Fourier input and separate experts. No new frequencies or coordinates are generated.

## Hypothesis and proposed change

Primary hypothesis: preserving direct access to the periodic basis throughout the conditioned backbone improves the IC/physics tradeoff at equal time. Expand five128x128 weights to128x147, copy the freshly initialised parent-shaped128 columns and zero the19 new columns; biases preserved. No trained state reused. Concatenate original features before those five affine operations. Conditioner, Snake, forward density transform, optimisers and entire train_model are AST-identical to025. CPU/native MPS synthetic-feature checks passed:148677 parameters, parent main tensors equal, initial raw map and feature derivatives through third order agree within tolerances, finite all-parameter gradients, nonzero skip-block gradients. Conditioner and subsequent sampling RNG streams can differ because expansion consumes random draws; this is not a perfectly isolated causal ablation.

## Training objective and setup

Canonical training F=continuity+mom_x+mom_y+mom_z+poisson+IC_x+IC_y+IC_z absolute MSE, coefficients all1. Owner validation unchanged:0.2early+0.3middle+0.5late+IC_relative_MSE. Seven main affine layers, width128, six Snake activations, five repeated19-feature skips, time FiLM1->32->1536; total148677 parameters (94080 hidden-matrix Adan,54597 auxiliary AdaBelief). First80%: Adan lr0.001 betas(.98,.92,.99),eps1e-8 on hidden matrices; unrectified AdaBelief lr0.001 betas(.9,.999),eps1e-12 on others;1024PDE/1024IC replacement pool batches. Final20%: parent full-pool PR+ with Armijo search on all100000PDE/75000IC,4096/3072 microbatches plus tail. No total per-step point cap;8192 per context call only.750seconds,750000parameter cap,seed82/train823001, fresh weights, native MPS. Frozen pools/scorer untouched; actual evaluations recorded.

## Expected outcome

Falsifiable target: L_val below0.16374612321085807 through lower IC error without enough extra physics error to erase the gain; report all windows/components. Skips may instead amplify derivative errors, overfit low modes or reduce full-pool steps through increased AD cost. Zero initial skip weights may delay their use. Density, mass and periodicity remain diagnostics, never eligibility gates; a single shared-seed run supports only exploratory comparisons.

## Observed results

Actual metrics, metadata and complete history follow; all diagnostics and run.log read. 14643 initial updates+25 CG attempts(24 accepted),44 line values,2 restarts,0 nonfinite proposals,69 complete full-pool evaluations reconcile21894432 PDE/20169432 IC evaluations and16368 physics calls. Training740.685732 seconds,148677parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.16293784616066054,
    "physics_weighted": 0.0682361379091252,
    "ic_relative_l2": 0.30773642659187317,
    "ic_relative_mse": 0.09470170825153534,
    "windows": {
      "early": {
        "continuity": 0.1791681846335281,
        "momentum": 0.03352845569649165,
        "poisson": 0.004293291955952833,
        "total": 0.21698993228597258
      },
      "middle": {
        "continuity": 0.010357345622062496,
        "momentum": 0.012378356738969153,
        "poisson": 0.00411585929014498,
        "total": 0.02685156165117663
      },
      "late": {
        "continuity": 0.01453050623355774,
        "momentum": 0.012270321104424234,
        "poisson": 0.006764538575173414,
        "total": 0.033565365913155384
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.994926393032074,
        "0.5": 0.9904887676239014,
        "0.8": 0.9892330169677734
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005073606967926025,
        "0.5": -0.009511232376098633,
        "0.8": -0.010766983032226562
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10993221402168274,
        "0.5": 0.3319567143917084,
        "0.8": 0.5939452052116394
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2681097984313965,
        "0.5": 1.9859013557434082,
        "0.8": 3.1519827842712402
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.4328068792819977,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.6226043701171875e-06
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
    "params": 148677,
    "training_seconds": 740.6857319160481,
    "optimizer_steps": 14668,
    "physics_calls": 16368,
    "pde_training_evaluations": 21894432,
    "ic_training_evaluations": 20169432,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4460,
      "loss": 0.5130055546760559,
      "elapsed_seconds": 187.5258477080497,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4567040; IC_eval=4567040"
    },
    {
      "step": 9080,
      "loss": 0.4570132791996002,
      "elapsed_seconds": 375.01437283301493,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9297920; IC_eval=9297920"
    },
    {
      "step": 13713,
      "loss": 0.42809128761291504,
      "elapsed_seconds": 562.5249224160216,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=14042112; IC_eval=14042112"
    },
    {
      "step": 14668,
      "loss": 0.4028170555830002,
      "elapsed_seconds": 740.6851720830309,
      "note": "final full PR+; PDE_eval=21894432; IC_eval=20169432; PDE_draws=15094432; IC_draws=15069432; cg=25; accepted=24; full=100000/75000; micro=4096; lines=44; nf=0; restarts=2"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 21894432,
    "IC_eval": 20169432,
    "PDE_draws": 15094432,
    "IC_draws": 15069432,
    "cg": 25,
    "accepted": 24,
    "lines": 44,
    "nf": 0,
    "restarts": 2
  }
}
```

## Decision and interpretation

New lowest finite score: L_val falls0.0008082771 (0.49%) versus025. IC MSE improves0.0017387269 while physics rises0.0009304499;early/middle totals worsen and late improves. Net hypothesis supported only in this exploratory fit. Retain by total without diagnostic gates. Small gap, changed parameter count/RNG/GEMM and equal-time throughput prevent a reliable causal or significance claim;1800-second finalists remain necessary after all60 attempts.
