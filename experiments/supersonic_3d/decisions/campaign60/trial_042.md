# Trial 042

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:32; kind=refinement; mechanism_id=higher_bandwidth_initial_velocity_time_jets.

## Parent methods and evidence

Trial032 is the successfully closed parent: L_val0.17884705815945587, weighted physics0.014895506627969641, IC relative MSE0.16395155153148622. Its compatible initial jets reduced physics by78% versus028 but IC error dominated. Current best028 scores0.16293784616066054. This refinement tests whether restricted initial Fourier bandwidth contributed to032s IC weakness. Interrupted041 has no score and is not used as performance evidence or a weight source.

## Novelty claim

Explicit numerical representation refinement, not a new mechanism: increase the initial-velocity Fourier cube cutoff from3 to5. Independent nonzero +/- representatives increase171->665 and learned initial-velocity coefficients1026->3990. The PDE-compatible time-jet mechanism and all optimisers/losses remain those of032. Fourier bases and hard-constraint trial solutions are established; no literature novelty claim. This is allowed within the041-050 refinement block and is a new source/fit, not a rerun of interrupted041.

## Hypothesis and proposed change

Primary hypothesis: higher initial-velocity bandwidth reduces IC error enough to preserve032s physics advantage and beat028 total. The only executable AST changes from032 are the three mode-generation ranges(-3,4)->(-5,6); all formulas use the resulting mode count automatically, including sqrt(mode count) normalisation. Same zero initial Fourier coefficients and identical fresh correction-network state/RNG draws; initial field map is identical before learning. Extra coefficient dimensions and their gradient scaling are part of the refinement, so bandwidth is not separated from parameter geometry or cost. CPU/native MPS tests verified665modes,3990coefficients,152667parameters, identical initial correction/field map, periodicity and initial five-PDE cancellation with nonzero disposable test coefficients (max1.86e-9CPU/1.49e-8MPS). No additional training coordinates or PINN fits in checks.

## Training objective and setup

Frozen L_val=.2early+.3middle+.5late+IC_relative_MSE unchanged. Same032 fields: learned periodic u, d=divu, a=(u dot grad)u;rho=rho0 exp(clamp(-td+t^2R,-4,4)),v=u-ta+t^2V,phi=tF. Correction network retains028seven-affine width128/sixSnake/five19-feature input skips/bounded time-FiLM.152667parameters:94080hidden weights Adan lr.001,betas(.98,.92,.99),eps1e-8;58587auxiliary including3990initial coefficients AdaBelief lr.001,betas(.9,.999),eps1e-12. Entire032trainer AST unchanged: canonical sumfivePDE+sumthreeIC absolute MSE allcoef1;first80%1024PDE/1024IC replacement-pool batches,final20%full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No total points-per-step cap;8192 per context call.750seconds,fresh weights,seed82/training823001,MPS,750000parameter cap,only frozen pools. Actual counts afterrun.

## Expected outcome

Falsifiable target: IC relative MSE below032s0.1639515515 and L_val below028s0.1629378462, without physics deterioration erasing the gain. More high-frequency initial modes can raise divergence/advection derivatives, exponent saturation and correction demands; larger basis/AD work may reduce updates. The initial Fourier bandwidth explanation is a hypothesis, not an established cause. Report all windows/components/counts and density/mass/periodicity diagnostics without eligibility gates. One fresh shared-seed fit does not establish significance or numerical-reference accuracy.

## Observed results

Actual metrics, metadata and complete history follow; all numerical diagnostics and run.log read. 9372 initial updates+14 completed CG attempts(13 accepted),27 line values,2 restarts,0 nonfinite proposals. Actual counters imply42 complete full-pool evaluations:14 completed-attempt gradients+27 line evaluations+one complete gradient in the final unfinished deadline-limited attempt. No partial pool pass is needed to reconcile13796928 PDE/12746928 IC evaluations and10422 physics calls. The final unfinished attempt restores its base parameters by the documented deadline handler; it does not add an optimiser step. Training742.445666 seconds,152667parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.15255327074817465,
    "physics_weighted": 0.033184611706952465,
    "ic_relative_l2": 0.3454976975917816,
    "ic_relative_mse": 0.11936865904122218,
    "windows": {
      "early": {
        "continuity": 0.005832540522277363,
        "momentum": 0.005600192165248792,
        "poisson": 0.001149797426370969,
        "total": 0.012582530113897122
      },
      "middle": {
        "continuity": 0.009917620954563977,
        "momentum": 0.010671733254094887,
        "poisson": 0.0046384374001178395,
        "total": 0.025227791608776702
      },
      "late": {
        "continuity": 0.02097649340666695,
        "momentum": 0.016468528879167343,
        "poisson": 0.008754514117245763,
        "total": 0.046199536403080055
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9950001239776611,
        "0.5": 0.9890922904014587,
        "0.8": 0.9867079257965088
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004999876022338867,
        "0.5": -0.01090770959854126,
        "0.8": -0.013292074203491211
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.14908485114574432,
        "0.5": 0.3737786114215851,
        "0.8": 0.6318250894546509
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3713610172271729,
        "0.5": 2.121239423751831,
        "0.8": 3.229196548461914
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.22183261811733246,
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
    "params": 152667,
    "training_seconds": 742.4456664160243,
    "optimizer_steps": 9386,
    "physics_calls": 10422,
    "pde_training_evaluations": 13796928,
    "ic_training_evaluations": 12746928,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2913,
      "loss": 0.5339246988296509,
      "elapsed_seconds": 187.53655862505548,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2982912; IC_eval=2982912"
    },
    {
      "step": 5857,
      "loss": 0.47995516657829285,
      "elapsed_seconds": 375.0177445410518,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5997568; IC_eval=5997568"
    },
    {
      "step": 8785,
      "loss": 0.4604770541191101,
      "elapsed_seconds": 562.5174453750369,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=8995840; IC_eval=8995840"
    },
    {
      "step": 9386,
      "loss": 0.45612280862405896,
      "elapsed_seconds": 742.4396554580308,
      "note": "final full PR+; PDE_eval=13796928; IC_eval=12746928; PDE_draws=9696928; IC_draws=9671928; cg=14; accepted=13; full=100000/75000; micro=4096; lines=27; nf=0; restarts=2"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 13796928,
    "IC_eval": 12746928,
    "PDE_draws": 9696928,
    "IC_draws": 9671928,
    "cg": 14,
    "accepted": 13,
    "lines": 27,
    "nf": 0,
    "restarts": 2,
    "complete_full_evaluations": 42,
    "uncompleted_attempt_full_gradients": 1
  }
}
```

## Decision and interpretation

New lowest finite score. Versus032, total improves0.0262937874 (14.70%), IC MSE falls0.0445828925, while physics rises0.0182891051 and all physics windows worsen. Versus028, total improves0.0103845754 (6.37%), physics falls0.0350515262 while IC MSE is higher0.0246669508. Retain042 by total alone despite its higher IC error than028; no diagnostic gates. The bandwidth-refinement hypothesis is supported in this fit, but added coefficient dimensions/normalisation and lower throughput are not isolated, and no statistical significance or numerical-reference accuracy is established. Final matched1800-second comparison remains required after60 attempts.
